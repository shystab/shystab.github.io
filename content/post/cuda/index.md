---
title: "CUDA 学习记录"
date: 2026-05-29T16:00:00+08:00
lastmod: 2026-05-29T16:00:00+08:00
author: "Shysta"
draft: false

summary: "CUDA 算子练习清单与易忘点"
description: "个人 CUDA 学习记录：算子练习进度、实现思路和容易忘记的细节"

categories: ["学习"]
tags: ["CUDA", "GPU编程", "算子"]

cover: "/images/forteenth.jpg"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["CUDA", "算子", "学习记录"]
---

纯记录，不分享。练习进度和容易忘的东西都堆这。

## 算子练习清单

| 算子 | 状态 | 思路 / 易忘点 |
|------|:----:|--------------|
| 向量加法 Vector Add | ⬜ | |
| 矩阵乘法 GEMM | ✅ | |
| 规约 Reduction | ✅ | |
| 前缀和 Scan | ⬜ | |
| 转置 Transpose | ⬜ | |
| Softmax | ⬜ | |
| 卷积 Convolution | ⬜ | |
| 直方图 Histogram | ⬜ | |
| 排序 Sort | ⬜ | |
| 稀疏矩阵 SpMV | ⬜ | |

## 易忘点

| 主题 | 要点 |
|------|------|
| 线程层次 | Block 是资源分配和同步的边界，Warp 是执行调度的最小单元（固定 32 线程） |
| 内存层次 | 寄存器 > shared memory > 全局内存，全局内存访问不合并就慢 |
| Tiling | 不是为了减少访存总量，而是提高数据复用率 |
| Occupancy | 受寄存器 / shared memory / block 大小限制 |
| ncu | 先看 Speed of Light 判断是访存受限还是计算受限 |
