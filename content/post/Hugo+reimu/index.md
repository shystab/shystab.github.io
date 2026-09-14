---
title: "Hugo Reimu 主题"
date: 2026-02-05T20:30:00+08:00
lastmod: 2026-09-14T10:00:00+08:00
author: "Shysta"
draft: false

summary: "本站使用的 Hugo Reimu 主题介绍与搭建流程"
description: "介绍本站使用的 Hugo Reimu 主题，以及搭建和部署的大致流程"

categories: ["技术实践"]
tags: ["Hugo", "Reimu", "博客"]

cover: "/images/cover-03.jpg"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["Hugo", "Reimu主题", "博客搭建", "GitHub Pages"]
---

## 主题

本站使用 [Hugo](https://gohugo.io/) 搭建，主题为 [hugo-theme-reimu](https://github.com/D-Sketon/hugo-theme-reimu)，作者是 [D-Sketon](https://github.com/D-Sketon)。

主题以东方 Project 的博丽灵梦为风格，主要特性：

- 内置 APlayer + Meting 音乐播放器
- 支持 Utterances、Waline、Twikoo 等多种评论系统
- 暗黑模式与动态主题色
- 相册、标签页、折叠框等实用短代码

## 搭建流程

1. **安装 Hugo**：主题使用 SCSS，需要 extended 版本
2. **创建站点**：

   ```bash
   hugo new site myblog
   cd myblog
   git init
   ```

3. **安装主题**：推荐 submodule 方式，方便跟踪版本

   ```bash
   git submodule add https://github.com/D-Sketon/hugo-theme-reimu.git themes/reimu
   ```

4. **配置**：在 `hugo.toml` 里声明 `theme = "reimu"`，并把主题的 `config`、`data` 复制到项目根目录按需修改
5. **本地预览**：

   ```bash
   hugo server
   ```

## 部署

GitHub Pages 只托管静态文件，需要借助 GitHub Actions 在推送时构建并部署。

大致流程：`git push` → Actions 执行 `hugo --minify` 生成 `public/` → 部署到 Pages。

完整 workflow 见仓库的 `.github/workflows/hugo.yml`。
