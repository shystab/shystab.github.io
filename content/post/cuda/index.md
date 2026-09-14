---
title: "CUDA 学习记录"
date: 2026-05-29T16:00:00+08:00
lastmod: 2026-09-14T10:00:00+08:00
author: "Shysta"
draft: false

summary: "CUDA 算子练习清单与易忘点"
description: "个人 CUDA 学习记录：算子练习进度、实现思路和容易忘记的细节"

categories: ["学习"]
tags: ["CUDA", "GPU编程", "算子"]

cover: "/images/cover-14.jpg"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["CUDA", "算子", "学习记录"]
---

纯记录，不分享。跟着[杜子源的 CUDA学习之路](https://dlog.com.cn/archive/?category=CUDA%E5%AD%A6%E4%B9%A0%E4%B9%8B%E8%B7%AF)学的，跳着看的。

## 算子练习清单

按他的分类顺序：

| 算子 | 状态 | 思路 / 易忘点 |
|------|:----:|--------------|
| 逐元素操作 Element-wise | ✅ | |
| 规约 Reduce | ✅ | |
| Softmax | ✅ | |
| Norm 系列（LayerNorm / RMSNorm） | ✅ | |
| 扫描 Scan | ⬜ | |
| 矩阵乘法 MatMul | ✅ | |
| 卷积 Convolution | ⬜ | 还没看 |
| Attention | ⬜ | |

## 后面要看的

- vLLM 相关内容（Attention / Sampler / RotaryEmbedding 等）

## 易忘点

| 主题 | 要点 |
|------|------|
| 线程层次 | Block 是资源分配和同步的边界，Warp 是执行调度的最小单元（固定 32 线程） |
| 内存层次 | 寄存器 > shared memory > 全局内存，全局内存访问不合并就慢 |
| Tiling | 不是为了减少访存总量，而是提高数据复用率 |
| Occupancy | 受寄存器 / shared memory / block 大小限制 |
| ncu | 先看 Speed of Light 判断是访存受限还是计算受限 |
