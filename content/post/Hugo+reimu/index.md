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

答案：~装逼~ 学习！！博客本身不复杂，但它包含了很多内容，其实大一就应该试着做做的，但信息差还有游戏（悲）耽误了学习进度，姑且算是卷绩点了吧。从学习路径来看，搭建博客是一个成本可控、反馈周期短的项目。所以have a try！

寒假开始时先试着跟着gpt走了一个flask小框架（差点就去学后端了）深似海啊，还是先搭一个博客练练手。

## 第一阶段：选择主题

我的 Hugo 之旅始于知名的 **Stack 主题**。它设计简洁、文档完善，是许多人的入门之选。

但在那之前，我在hugo的path路径上吃了点亏。首先我学到了path路径就是用户变量里面的一个变量，直接在后面加就可以（悲）。

但是我就是不想要一键部署（犟种），原本stack是有examplesites的文件我可以用那个直接改，后面被一键部署替代，我看新的demo文件头大的要死。这个卡了一天多。所以如果你愿意用GitHub一键部署，stack其实还是个很好的选择。

**所以，换个主题吧**

在一次偶然的主题探索中，我发现了 **D-Sketon**大佬 开发的 **hugo-theme-reimu**。它基于东方Project的“博丽灵梦”角色风格，瞬间吸引了我的目光。（其实我不是二次元）

{{< gallery >}}
![Reimu主题截图-首页](https://fastly.jsdelivr.net/gh/D-Sketon/hugo-theme-reimu/images/screenshot.png)
{{</gallery>}}

不仅仅是颜值，它的**功能清单**更让我震惊：
- 🎵 内置 APlayer + Meting 音乐播放器
- 💬 支持多达7种评论系统（我选择了 Utterances）
- 🖱️ 灵梦鼠标指针、烟花特效等丰富的交互细节
- 📦 无数实用的短代码（相册、标签页、折叠框等）
- 🌙 完美的暗黑模式与动态主题色支持

不错不错，我把博客打扮的很二次元，营造一种**味大的一批，一看就很强**的赶脚。

## 第三阶段：配置

迁移过程并非一帆风顺，我遇到了几个典型问题，但相比之前还是很好解决的。

下面把整个流程打出来：

先下载hugo本体：https://gohugo.io/ 
然后记得配置path。

在hugo文件夹命令行内运行

```cmd
hugo version
```
检验是否安装成功。

```cmd
hugo new site myblog#或者你的文件夹名 自行创建
cd myblog
git init
```

而后看到官方出的几行教程，请仔细阅读。有助于你理解搭建过程。

### 一般来说 有两种方法下载主题
1. 使用git或直接下载压缩包解压https://github.com/D-Sketon/hugo-theme-reimu.git

2. submodule 方式
这样做的好处是：
主题版本可追踪
仓库结构清晰
便于 CI 拉取

当然也可以用官网的hugo-reimu-template 小白很舒服

### 此处介绍1方法（我就是这样的，个人感觉更不更新无所谓）

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

而后参考官网readme文档里的创建配置章节，把数据配置（config文件夹）和静态资源复制到blog文件夹内容

然后可自行阅读config的params文件配置代码 官网里有详细对应组件开启方式（笑）

完成各自配置之后
此时直接在命令行运行
```cmd
# 在博客文件内
hugo server
```
然后打开命令控制行给的本地网址（ctrl+点击）
即可看到自己的网站喵~

### 部署至github

主要是静态网站没必要配置到服务器上，我也没那个心力了，于是就跟着教程配置到GitHub actions上。建议看这里https://github.com/peaceiris/actions-hugo 的教程再搭配ai食用。

大体就是再创建一个.github\workflows文件夹 写hugo.yml文件。
本人代码如下 可跑
```yal
name: Deploy Hugo Site to GitHub Pages

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false


jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true

      - name: Build
        run: hugo --minify

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

GitHub Pages 不会运行 Hugo，它只托管静态文件。
所以必须借助 GitHub Actions。
流程是：
git push
GitHub Actions 执行 hugo build
生成 public/
部署到 Pages

遇到一些faliure可以抽查gpt啥的。反正最后在GitHub运行起来就蛮不错的

### 网站的额外功能 如评论 播放器 
暂缺嘻嘻

## 文章更新 
按照content/post/文章名/index.md（可在文件夹里加图片方便插入）或者content/post/文章名.md格式整理自己的文章后 把本地的更新推送到github上

仍然是使用*git* ~其实我也不会用哈哈 慢慢学着用~

第一步：添加所有更改

```cmd
git add .
```
这条命令会将你所有新的修改（包括新文章、修改的配置等）标记为“待提交”。

第二步：创建提交记录（给这次更新起个名字）

```cmd
git commit -m "发布新文章：《你的文章标题》"
```
将引号内的 《你的文章标题》 换成你实际的文章标题，例如 git commit -m "发布新文章：《我的Hugo之旅》"。这条命令相当于给你的这次更新拍个快照、贴个标签。

第三步：推送到云端，触发自动部署

```cmd
git push
```
这条命令会将你本地的“快照”推送到GitHub。这是最关键的一步，因为它会触发我们之前配置好的 GitHub Actions 工作流，自动开始构建并部署你的新网站。
然后等待终端完成后去看看GitHub action任务是否允许成功（等待一小会）
成功之后便可去看你的新网页啦

{{< alertBlockquote type="note" >}} **注意**：在本机上验证网站允许正常再推送会好一点 {{</alertBlockquote>}}

然后很高兴你成功搭建了自己的网站*开心喵*
快去告诉小伙伴吧！