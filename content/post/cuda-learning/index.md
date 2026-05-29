---
title: "CUDA 入门与 GEMM 优化：从零到有点懂"
date: 2026-05-29T16:00:00+08:00
lastmod: 2026-05-29T16:00:00+08:00
author: "Shysta"
draft: false

summary: "一个寒假学 CUDA 的小记录，从编程模型到动手优化 GEMM 算子"
description: "本文记录我从零学习 CUDA 的过程，涵盖线程模型、内存层次、性能优化策略，以及 GEMM 算子从朴素版到 Tiling 优化的实战经历。"

categories: ["学习"]
tags: ["CUDA", "GPU编程", "GEMM", "性能优化", "并行计算"]

cover: "/images/forteenth.jpg"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["CUDA", "GEMM", "GPU", "算子优化", "并行计算"]
---

## 为什么突然学 CUDA

为什么学CUDA呢 本质是李老师原本让我看机器学习系统 刚了解到算子 infra这一类概念 以及 被ai工具的冲击给震撼到了 至少是在3月份 我还基本不会用任何agent工具 什么opencode 什么claudecode codex 都不会用 在老师那边一聊天感觉自己缺的东西太多了 后面我开始恶补 以及真切体会到ai的强大 也感叹自己的落后 以及老师让我后边可以尝试ascendc的生态 于是就先学点CUDA。

于是就有了这趟 CUDA 的学习之旅。

学得不算深，但至少把编程模型、内存层次、性能分析这套东西走通了一遍，最后拿 GEMM 算子练了练手，算是把理论和实践串起来了。

## 一、CUDA 到底是什么

**CUDA（Compute Unified Device Architecture）** 是 NVIDIA 的并行计算平台和编程模型。核心思想很简单：GPU 不只是用来渲染的，它还能干大规模并行计算。

CUDA 提供三层接口：

- **驱动 API**（`cu` 前缀）：最底层，控制最细
- **运行时 API**（`cuda` 前缀）：日常写代码主要用这层
- **库**（cuBLAS、cuFFT 等）：高度优化，拿来即用

编程模型的核心是 **异构计算**：CPU（Host）负责逻辑控制和调度，GPU（Device）负责数据并行计算。两者通过 PCIe 传输数据。

### 一个最简单的 Kernel

```cpp
__global__ void VecAdd(float* A, float* B, float* C) {
    int i = threadIdx.x;
    C[i] = A[i] + B[i];
}

int main() {
    VecAdd<<<1, N>>>(A, B, C);
}
```

每个线程通过内置变量拿到自己的唯一 ID，各算各的。这就是 SIMT（Single Instruction, Multiple Thread）—— 你写的是标量代码，硬件自动打包成并行执行。

## 二、线程层次结构

CUDA 的线程组织分三层：

| 层级 | 说明 | 内置变量 |
|------|------|----------|
| **Grid** | 由多个 Block 组成 | `gridDim` |
| **Block** | 由多个 Thread 组成，最多 1024 线程 | `blockDim`, `blockIdx` |
| **Thread** | 最小执行单元 | `threadIdx` |

索引计算是基本功：

```cpp
int idx = blockIdx.x * blockDim.x + threadIdx.x;  // 1D
```

扩展到 2D 也很自然，就是算个偏移量的事。

### Warp —— 真正调度的是它

Block 是逻辑概念，硬件实际调度是以 **Warp** 为单位的。一个 Warp 固定 32 个线程，同一个 Warp 里的线程在同一时刻执行同一条指令。

这意味着：

- Block 大小最好设成 32 的倍数，否则最后一个 Warp 会浪费
- 同一 Warp 内如果有条件分支走不同路径（Warp Divergence），会被串行执行

## 三、内存层次结构

这是 CUDA 优化绕不开的核心。

| 内存类型 | 位置 | 速度 | 容量 | 管理方式 |
|----------|------|------|------|----------|
| 寄存器 | 片上 | 最快 | 极少 | 编译器自动 |
| 共享内存 | 片上 | ~20-30 周期 | 几十 KB | 程序员显式 |
| 全局内存 | 片下 HBM | ~几百周期 | 几十 GB | 显式管理 |
| 常量内存 | 有缓存 | 较快 | 64KB | 只读 |

**关键认知**：共享内存和 L1 缓存物理上是同一块片上 SRAM。区别在于 L1 由硬件自动管理，共享内存由你手写控制。你用 `__shared__` 就是在手动管理这块最快的高速存储。

**寄存器溢出**是个常见坑：每个线程私有变量太多，编译器会把它"溢出"到 Local Memory。Local Memory 名字带"本地"，实际位置在片下显存，速度跟全局内存一样慢。

## 四、性能优化三板斧

### 1. 合并访问（Coalesced Access）

同一 Warp 的 32 个线程访问**连续、对齐**的内存地址时，硬件能合并为一次总线传输。这是最基本也最重要的优化原则。

看你的 ncu 报告，如果 L1 Hit Rate 极低、Sector/Req 比值高，十有八九是访问不合并。

### 2. Tiling 分块

Tiling 的本质不是减少访存总量，而是**提升数据复用率**。把反复需要的数据从全局内存搬到共享内存，让块内所有线程在高速存储上反复使用。

类比：朴素版是每次从远处大仓库拿一个番茄一个鸡蛋；Tiling 版用托盘一次把一道菜的所有食材搬过来，在灶台边加工。

### 3. 延迟隐藏

GPU 的核心哲学：**用大量并行掩盖访存延迟**。Warp A 等数据时，Warp Scheduler 立刻切到 Warp B 执行，计算单元不闲置。

这就是 Occupancy（占用率）的意义：SM 上驻留的 Warp 越多，越容易找到准备好的 Warp 来执行。

## 五、GEMM 优化实战：从 180 到 1000+ GFLOPS

理论知识说完了，拿 GEMM 算子练练手。目标是优化矩阵乘法 `C = A × B`，矩阵大小 2048×2048。

### V0：朴素版

每个线程算一个输出元素，最直接的写法：

```cpp
__global__ void matmul_naive(const float *A, const float *B, float *C,
                              int M, int N, int K) {
    int row = blockDim.y * blockIdx.y + threadIdx.y;
    int col = blockDim.x * blockIdx.x + threadIdx.x;
    if (row < M && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < K; k++)
            sum += A[row * K + k] * B[k * N + col];
        C[row * N + col] = sum;
    }
}
```

用 ncu 一看，L1 Hit Rate 只有 4.49%，Sector/Req 高得离谱。原因很直接：B 矩阵的访存是跳跃的，完全不合并。

测下来 2048 下只有 **~180 GFLOPS**。

### V1：Tiling + Shared Memory

引入 TILE 分块，把数据搬进共享内存：

```cpp
__global__ void matmul_tiled(const float *A, const float *B, float *C,
                              int M, int N, int K) {
    int c_row = blockIdx.y * TILE + threadIdx.y;
    int c_col = blockIdx.x * TILE + threadIdx.x;
    __shared__ float As[TILE][TILE];
    __shared__ float Bs[TILE][TILE];
    float sum = 0.0f;

    for (int t = 0; t < K / TILE; t++) {
        // 协作加载 tile 到 shared memory
        As[threadIdx.y][threadIdx.x] = A[c_row * K + t * TILE + threadIdx.x];
        Bs[threadIdx.y][threadIdx.x] = B[(t * TILE + threadIdx.y) * N + c_col];
        __syncthreads();

        for (int k = 0; k < TILE; k++)
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        __syncthreads();
    }
    C[c_row * N + c_col] = sum;
}
```

改动不大，但效果明显——L1 Hit Rate 上来了，访存变得规整了。性能提升到 **~600 GFLOPS**。

### V2：向量化 + 多行多列

进一步优化：每个线程算 4×4=16 个元素，用 `float4` 向量化加载 B 矩阵：

```cpp
float4 bdata = reinterpret_cast<const float4*>(B + b_row * N + b_col)[0];
Bs[threadIdx.y][4 * threadIdx.x]     = bdata.x;
Bs[threadIdx.y][4 * threadIdx.x + 1] = bdata.y;
Bs[threadIdx.y][4 * threadIdx.x + 2] = bdata.z;
Bs[threadIdx.y][4 * threadIdx.x + 3] = bdata.w;
```

这样每个线程做更多计算，减少了寄存器压力，同时更好地利用内存带宽。

最终性能 **~1000+ GFLOPS**，相比朴素版提升了 5 倍以上。

> 不过小矩阵（512 以下）Tiling 反而比朴素慢，因为 Shared Memory 搬运的开销抵不过收益。这也说明了优化没有银弹，得看具体的 shape。

## 六、学完之后的感受

CUDA 说难不难，说简单也不简单。它的概念其实很清晰——线程、内存、同步，三板斧理解透就能写。但要写得好，需要理解硬件是怎么跑你代码的。

最有价值的是学会了用 **ncu** 看性能数据，而不是凭感觉优化。对着数据改代码，效率高得多。

接下来准备继续折腾，后面可能会写写 AscendC 那边的经历——从 CUDA 迁移到 AscendC 打比赛，又是另一个故事了（笑）。

---

**参考资源：**
- [CUDA 官方编程指南](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
- [Nsight Compute 文档](https://docs.nvidia.com/nsight-compute/)
