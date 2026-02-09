---
title: "Hugo：我的博客与 Reimu 主题探索之旅"
date: 2026-02-05T20:30:00+08:00
lastmod: 2026-02-05T20:30:00+08:00
author: "Shysta"
draft: false

summary: "记录一次完整的博客搭建过程：为何放弃Stack 主题，最终投入 Hugo 与 Reimu 主题的怀抱，并解决一系列配置与部署问题的全过程。"
description: "本文详细记录了博主从 尝试 Stack 主题后，最终选择并深度定制 Reimu 主题的完整历程。涵盖了主题选择、功能配置、问题排查以及利用 GitHub Actions 自动化部署的实战经验。"

categories: ["技术实践"]
tags: ["Hugo", "博客", "Reimu", "主题", "GitHub Pages", "心得"]

cover: "/images/third.jpg" 

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["Hugo", "Reimu主题", "博客搭建", "静态网站"]
weight: 1
---

## 前言：为什么想搭建博客

答案：*装逼* 或者说是学习历程吧，原本想学后端或者前端的，也试着跑了一个flask框架，但这些学习周期有些长，所以搭建了一个博客，后面找实习也方便些。

## 第一阶段：stack主题

我的 Hugo 之旅始于知名的 **Stack 主题**。它设计简洁、文档完善，是许多人的入门之选。

但在那之前，我在hugo的path路径上吃了点亏。首先我学到了path路径就是用户变量里面的一个变量，直接在后面加就可以（悲）。

{{< alertBlockquote type="note" >}}
**Stack 主题的优点**：安装简单，响应式设计优秀，对于写纯文字博客非常友好。此外现在的一键部署也很方便。
{{</alertBlockquote>}}

但是我就是不想要一键部署，原本stack是有examplesites的文件我可以用那个直接改，后面被一键部署替代，我看新的demo文件头大的要死。这个卡了一天多。

1.  **风格过于通用**：虽然精致，但缺乏让我眼前一亮的个性元素，比如我不能搞得味大一点。
2.  **功能拓展性**：想要集成一些偏“二次元”或趣味性的小部件（如看板娘、特效）较为困难，或者说对我比较困难。
3.  **审美疲劳**：它的设计语言在众多技术博客中太常见了。

**于是，我决定继续寻找那个能让我“心动”的主题。**

## 第二阶段：遇见 Reimu，一见钟情

在一次偶然的主题探索中，我发现了 **D-Sketon** 开发的 **hugo-theme-reimu**。它基于东方Project的“博丽灵梦”角色风格，瞬间吸引了我的目光。（其实我不是二次元）

{{< gallery >}}
![Reimu主题截图-首页](https://fastly.jsdelivr.net/gh/D-Sketon/hugo-theme-reimu/images/screenshot.png)
{{</gallery>}}

不仅仅是颜值，它的**功能清单**更让我震惊：
- 🎵 内置 APlayer + Meting 音乐播放器
- 💬 支持多达7种评论系统（我选择了 Utterances）
- 🖱️ 灵梦鼠标指针、烟花特效等丰富的交互细节
- 📦 无数实用的短代码（相册、标签页、折叠框等）
- 🌙 完美的暗黑模式与动态主题色支持

我意识到，这就是我想要的——一个**味大的一批，又能很好的装逼**的主题。

## 第三阶段：配置

迁移过程并非一帆风顺，我遇到了几个典型问题，但相比之前还是很好解决的。

下面把整个流程打出来：

先下载hugo本体：https://gohugo.io/配置path。

在hugo文件夹命令行内运行

```cmd
hugo version
```
检验是否安装成功。

```cmd
hugo new site myblog
cd myblog
git init
```

而后看到官方出的几行教程，请仔细阅读。有助于你理解搭建过程。

首先你要有git（尽量）：
```cmd
# 在 Hugo 站点目录下执行
git submodule add https://github.com/D-Sketon/hugo-theme-reimu.git themes/reimu
```
或者你直接去github里面下载压缩包：https://github.com/D-Sketon然后将其解压至theme文件夹内。（名改成reimu）

{{< details "hugo.toml里声明" >}}
### 项目根目录下的 hugo.toml 文件
theme = “reimu”

baseURL = ‘https://你的用户名.github.
io/‘ # 部署前切记修改此项！

languageCode = ‘zh-CN’

{{< /details >}}

此时直接在命令行运行
```cmd
# 在博客文件内
hugo server
```

### 部署至github

主要是静态网站没必要配置到服务器上，我也没那个心力了，于是就跟着教程配置到GitHub actions上。建议看这里https://github.com/peaceiris/actions-hugo 的教程再搭配ai食用。

大体就是再创建一个.github\workflows文件夹 写hugo.yml文件。

遇到一些faliure可以抽查gpt啥的。反正最后在GitHub运行起来就蛮不错的