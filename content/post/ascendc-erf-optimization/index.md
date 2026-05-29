---
title: "AscendC 算子优化复盘：一场没进决赛的比赛"
date: 2026-05-29T16:30:00+08:00
lastmod: 2026-05-29T16:30:00+08:00
author: "Shysta"
draft: false

summary: "一次 CANNJudge Erf 算子比赛的完整复盘，从 CUDA 视角迁移到 AscendC，到公式选择、路径分治、Tiling 优化，再到各种踩坑记录"
description: "本文详细记录了我参加 AscendC Erf 算子优化比赛的全过程，包括从 CUDA 到 AscendC 的概念迁移、Erf 近似公式选择、Direct/Medium/Large 三路径分治策略、UB 布局优化，以及比赛过程中积累的踩坑经验。虽然最终没有进入决赛，但过程本身收获很大。"

categories: ["比赛"]
tags: ["AscendC", "CANN", "算子优化", "Erf", "华为昇腾", "AI芯片"]

cover: "/images/fifteenth.png"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["AscendC", "Erf", "算子优化", "CANN", "910B", "Tiling"]
---

## 背景

前段时间参加了华为那边的 CANNJudge Erf 算子比赛。目标是在 Ascend 910B 上优化 Erf（误差函数）算子，`float32` 逐元素运算，覆盖各种 shape 共 15 个测试点。

结果嘛——没进决赛（笑）。但整个过程覆盖了 AscendC 算子开发里非常典型的一堆问题，从工程结构到公式选型，从路径分治到 UB 布局，从同步到评测噪声。这些经验比进决赛本身可能更有价值，至少下次再碰 AscendC 不会那么慌了。

## 从 CUDA 到 AscendC：不只是换了个名字

之前刚学了点 CUDA 的基础（上一篇写了），原本以为 CUDA 到 AscendC 只是 API 换皮，上手才发现抽象边界完全不一样。

CUDA 写 kernel，你直接面对 thread/block/grid，数据搬运大多靠编译器帮你安排。AscendC 写自定义算子，你得同时处理：

- host 侧的 tiling 计算
- kernel 侧的流水编排
- UB buffer 管理
- 算子注册和 tiling key 选择

一个 AscendC 算子工程通常分成两边：

| 侧 | 位置 | 职责 |
|----|------|------|
| `op_host` | Host CPU | shape 推导、tiling、blockDim、tilingKey |
| `op_kernel` | AI Core | 数据搬运 + 向量计算 |

在 Erf 项目里，`op_host` 根据输入总长度决定走哪条路径，`op_kernel` 通过编译期模板参数 `IS_SPLIT` 选择不同的 kernel 类：

```cpp
if constexpr (IS_SPLIT == 0) {
    KernelErfLarge<DT_X> op;
} else if constexpr (IS_SPLIT == 4) {
    KernelErfMediumAligned<DT_X> op;
} else if constexpr (IS_SPLIT == 5) {
    KernelErfDirectStatic<DT_X> op;
}
```

这和 CUDA 里一个 kernel 包打天下不太一样。AscendC 把场景提前变成编译期分支，减少运行时判断，也方便不同 shape 使用完全不同的 UB 布局。

### TilingKey 是什么

TilingKey 可以理解为 host 给 kernel 的一把钥匙：host 根据输入规模选一个 key，编译系统提前为这些 key 生成不同特化版本。

最后 Erf 保留了这些路径：

| IS_SPLIT | 路径 | 用途 |
|----------|------|------|
| 0 | Large | 大数据，TQue 双缓冲 |
| 1 | Medium fallback | 非整除/非对齐时兜底 |
| 4 | MediumAligned | 中等数据对齐路径 |
| 5 | DirectStatic | 小数据非对齐 |
| 7 | DirectStaticAligned | 小数据对齐 |

### UB、TQue、TBuf 都是啥

AscendC 里性能绕不开 UB（Unified Buffer）。AI Core 不是直接在 GM 上算的，流程是：

```text
GM → UB → 计算 → UB → GM
```

几个关键概念：

| 名称 | 作用 |
|------|------|
| `TPipe` | 管理队列、buffer 和事件资源 |
| `TQue` | 搬运相关队列，配合 EnQue/DeQue/FreeTensor |
| `TBuf` | 纯计算用的临时 buffer |
| `LocalTensor` | UB 上的一段 tensor 视图 |
| `GlobalTensor` | GM 上的一段 tensor 视图 |

小 shape 上 TQue 的便利性不一定免费。Direct 路径如果只是搬入→算→搬出，静态 LocalTensor 有时比完整 TQue 流水更轻。

## 优化过程

### 公式：Erf 没那么简单

Erf 是逐元素算子，最直白的写法 `y[i] = erf(x[i])` 看起来简单，但在 AscendC 上要回答一堆问题：用什么近似公式？tile 多大？小数据要不要 TQue？中等数据用几核？

早期用重公式，后来改成 **rational 近似**：

```text
erf(x) ~= x * P(x²) / Q(x²)
```

精度稳，但有 `Div`。后来又试了 **poly9**：

```text
z = x * x
y = x * (((D4*z + D3)*z + D2)*z + D1)*z + D0
```

少了 `Div`，但 Horner 链依赖更长。实际结果说明不能只看"有没有 Div"来判断速度——小 shape 上 rational 反而更稳，大 shape 上 poly9 更适合吞吐。

最后稳定组合：
- Direct（小数据）：rational
- Medium/Large（中大数据）：poly9
- 输出 clamp 到 [-1, 1] 保平安

### 路径分治：Direct / Medium / Large

最稳定的设计不是一个万能 kernel，而是三条路：

```cpp
if (total_length <= max_tile) {
    // Direct：小数据，少框架开销
} else if (total_length <= max_tile * 4) {
    // Medium：中数据，调 blockDim 和 per-core 对齐
} else {
    // Large：大数据，保双缓冲流水
}
```

**Direct** 面向小数据，单核执行，对齐用 DataCopy，非对齐用 DataCopyPad，用静态 LocalTensor 避免 TQue 开销。核心思路不是"算得快"，而是"别为了几百个元素启动太复杂的机制"。

**Medium** 是最难调的一段。数据量不小但还没大到吞吐主导。最后调了个搜索策略：尽量找 `total_length % block_dim == 0` 且 `per_core % 8 == 0` 的 blockDim，能命中就走 MediumAligned，否则 queue fallback。

**Large** 反而基本没动——早期已经接近满分了，继续改很可能把稳定的吞吐改坏。

### UB 布局：删掉不用的 buffer

公式切到 poly9 后，一些 rational 需要的中间 buffer 不再需要。MediumAligned 里 buffer 从四个减到三个，对微秒级算子来说还挺有价值的——少一次 buffer 初始化，少一段 UB 空间，也可能减少 bank 冲突概率。

不过在 Direct 上没有照搬这个思路，因为 Direct 保留 rational，还是需要 denominator buffer。

## 踩坑记录

### 评测噪声是最大的敌人

微秒级测试点非常容易被平台噪声影响。一次结果里某个点快了 0.5us，不代表真的优化了。

建议做法是**路径归因**：

| 路径 | 测试点 |
|------|--------|
| Direct | 1、4、7、10、13 |
| Medium | 2、5、8、11 |
| Large | 3、6、9、12、14、15 |

只改 Direct 时只评价 Direct 的点，其他点的变化先按噪声处理。这条纪律不遵守，会不断把噪声当成优化，越调越乱。

### Direct 多核不是银弹

直觉上多核并行应该更快。但小 shape 上不一定，因为多核启动、每核初始化、GM 地址分片、同步这些开销加起来，可能比单核省下的计算时间还多。Direct 单核路线反而更稳。

### 公式优化要先跑全域误差

试过 poly7，结果 WA。后来长记性了：公式优化先用脚本扫全域误差，再进平台测性能。精度和性能要一起看，不能只看一边。

### RegBase / MicroAPI 当前环境不可用

官方资料里能看到 RegBase、MicroAPI 这类写法，理论上很适合 Horner 链这种场景。但当前 CANN 8.5 + 910B 环境里编译直接失败。这条路不要反复试，除非版本变了。

### 不要随便删同步

`DataCopy` 是异步的，TQue 的 `EnQue/DeQue` 或手动 `SetFlag/WaitFlag` 都是在建立 MTE 和 Vector 之间的顺序。

比赛里反复遇到：某条路径删同步看似更快，换个 shape 或一次评测就 WA。同步优化要非常谨慎。

### 保留实验日志

这次最有价值的产物之一不是最终代码，而是 `erf_optimization_trials.md`。它记录了哪些公式试过、哪些 tiling 改过、哪些 split 编译失败、哪些方案 WA。

长时间优化最怕"忘记已经试过什么"。实验日志是防止原地打转的最低成本工具。

## 虽然没进决赛

但这次比赛让我把 AscendC 的算子开发流程完整走了一遍。从 CUDA 迁移过来，认知上的转换是最难的——不只是学新 API，而是要理解不同的抽象层次和优化思路。

一些通用经验以后也能复用：

1. 先按 shape 分治，再考虑公式优化
2. 小数据优先减少固定开销
3. 中等数据的 tiling 是最容易拉开差距的地方
4. 大数据稳定后不要过度微调
5. 官方资料要看，但不能不验证
6. 所有失败实验都要记录

比赛结果不理想，但学到的这些东西，以后总会用到的。

![最高的一次分数捏](ascendc比赛 最高的一次分数.jpg)

**关注塔菲喵**

---

**相关资源：**
- [hugo-theme-reimu 官方文档](https://github.com/D-Sketon/hugo-theme-reimu)
- [AscendC 官方文档](https://www.hiascend.com/document)
