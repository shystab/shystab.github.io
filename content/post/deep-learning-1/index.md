---
title: "DL 学习记录 - HW1 回归"
date: 2026-02-23T20:30:00+08:00
lastmod: 2026-05-29T16:00:00+08:00
author: "Shysta"
draft: false

summary: "李宏毅 HW1 COVID-19 回归"
description: "李宏毅 HW1 回归任务的学习记录"

categories: ["学习"]
tags: ["Deep Learning", "PyTorch", "HW"]

cover: "/images/forth.jpg"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["HW-1", "回归"]
---

## 任务

李宏毅 HW1：COVID-19 回归预测，117 维特征。demo 是两层隐藏层（16、8），SGD 优化器。

## 结果

demo 最后 loss 在 2 左右，改完直接干到 0 附近。~震惊~

## 做了什么

- 网络加宽加深：`64 → 32 → 16 → 1`，每层加 BatchNorm
- 优化器 SGD → Adam
- 学习率从 `1e-5` 直接拉到 `1e-3`

## 易忘点

- SGD 需要极小的学习率才稳，Adam + BN 能扛更大的步长
- BatchNorm 稳定每层输入分布，加速收敛

## 图

demo：
{{< gallery >}}
![train loss](4.png)
![val loss](5.png)
{{< /gallery >}}

我的：
{{< gallery >}}
![train loss/batch](1.png)
![train loss/epoch](2.png)
![val loss](3.png)
{{< /gallery >}}
