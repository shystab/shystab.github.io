---
title: "ChatNovel 项目"
date: 2026-04-19T17:00:00+08:00
lastmod: 2026-09-14T10:00:00+08:00
author: "Shysta"
draft: false

summary: "AI 小说写作助手"
description: "ChatNovel —— 自己鼓捣的 AI 小说写作助手"

categories: ["项目"]
tags: ["AI", "全栈", "FastAPI", "Next.js"]

cover: "/images/cover-13.jpg"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["ChatNovel", "AI写作", "FastAPI", "Next.js"]
---

自己鼓捣的一个 AI 小说写作助手，前后端全栈。写小说的时候想让 AI 帮点忙，就顺手做了这个。

{{< gallery >}}
![主界面](image.png)
![多主题](image_2.png)
{{< /gallery >}}

## 大概是个啥

- 三栏布局：左边章节列表，中间编辑器，右边 AI 对话
- RAG 知识库：把参考文档喂进去，AI 续写时能模仿风格
- 三种主题切换、实时自动保存

## 技术栈

- 后端：FastAPI + SQLModel + ChromaDB
- 前端：Next.js + React
- AI：DeepSeek / OpenAI

## 链接

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [GitHub 仓库](https://github.com/shystab/ChatNovel)

## 想说的

（待补充）
