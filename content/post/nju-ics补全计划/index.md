---
title: "NJU ICS 前置准备"
date: 2026-03-25T16:30:00+08:00
lastmod: 2026-09-14T10:00:00+08:00
author: "Shysta"
draft: false
summary: "ICS PA 前置：Git、Linux 命令、Vim、GCC/Make、GDB、Tmux"
description: "NJU ICS PA 实验的前置准备，整理 Git 工作流、Linux 常用命令、二进制工具、Vim、GCC/Makefile 和 GDB 调试"

categories: ["学习"]
tags: ["ics", "Git", "Linux", "Vim", "Tmux", "GDB", "GCC", "Makefile"]

cover: "/images/cover-09.jpg"

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["ICS", "PA", "Git", "Linux", "Vim", "Tmux", "GDB", "GCC", "Makefile", "NJU"]
---
# ICS 前置准备

我跟着 21 年的：[ics-pa-gitbook](https://nju-projectn.github.io/ics-pa-gitbook/ics2021/index.html)

每年的内容应该变化不大。[25 年的在这](https://ysyx.oscc.cc/docs/ics-pa/)

## Git 使用

PA 全程都要跟 Git 打交道——clone 项目、提交代码、拉取更新。下面从最开始的配置一路讲到多 remote 场景。

### 一、初次使用：先告诉 Git 你是谁

装完 Git 第一件事不是 clone，是配置身份。没有这个，commit 会报错：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

`--global` 表示全局生效，一次配置就不用再管了。也可以不加 `--global` 给单个仓库单独配置。

顺便可以设一下默认编辑器（不然可能会卡进 Vim 出不来）：

```bash
git config --global core.editor "vim"
```

查看当前配置：

```bash
git config --list
```

### 二、推送之前：你要先解决认证

要把代码推到 GitHub，得让 GitHub 知道你是谁。目前主流两种方式：

**方式一：SSH Key（推荐）**

```bash
# 1. 生成密钥对（一路回车就行）
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 2. 查看公钥内容
cat ~/.ssh/id_ed25519.pub
```

复制输出的内容，打开 GitHub → Settings → SSH and GPG keys → New SSH key，粘贴保存。

之后 `git clone` 时记得用 SSH 地址（`:xxx/xxx.git`）而不是 HTTPS 地址，就不用每次输密码了。

**方式二：Personal Access Token（HTTPS 用）**

如果走 HTTPS 协议，GitHub 从 2021 年起就不支持密码认证了，得用 token。去 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) 生成一个，复制保存好。之后 push 时用户名输你的 GitHub 用户名，密码输这个 token。

### 三、origin 到底是什么

很多教程让你直接 `git push origin main`，但从来不说 `origin` 是什么。

`origin` 是一个 **远程仓库的别名**（也就是 URL 的快捷方式）。它不是你敲出来的，是 `git clone` 自动创建的：

```bash
git clone https://github.com/xxx/repo.git
# Git 自动做了这件事（等价于）：
git remote add origin https://github.com/xxx/repo.git
```

所以 `git push origin main` = "推送到别名为 origin 的那个远程仓库的 main 分支"。

查看所有 remote：

```bash
git remote -v
# origin  https://github.com/xxx/repo.git (fetch)
# origin  https://github.com/xxx/repo.git (push)
```

这个别名可以随便起，叫 `mygit`、`upstream`、`backup` 都行，`origin` 只是 clone 时的默认值。

### 四、克隆别人的仓库，推到自己的仓库

PA 的场景：你要 clone 官方项目，然后推到自己的 GitHub 仓库。这会遇到两个 remote：

```bash
# 1. 克隆官方仓库（自动得到 origin）
git clone https://github.com/NJU-ProjectN/ics-pa.git
cd ics-pa

# 2. 在 GitHub 上新建一个你自己的空仓库（不要勾选任何初始化选项）
#    然后把它添加为第二个 remote
git remote add mygit https://github.com/你的用户名/你的仓库名.git

# 3. 推送到自己的仓库
git push -u mygit main

# 4. 之后如果官方仓库有更新，从 origin 拉
git pull origin main

# 5. 自己的修改推到自己仓库，用 mygit
git push mygit main
```

所以如果你之前看到同时有 `origin` 和 `mygit`，就是这个原因——一个指向原项目，一个指向你自己的 fork。

习惯上：
- `origin` = 你主要推送的远程（自己的仓库）
- `upstream` = 原作者的仓库（只拉取不推送）

但叫什么完全是你自己定的。

### 五、完整工作流（以 PA 为例）

```bash
# 1. 克隆
git clone <你的仓库 SSH 地址>
cd ics-pa

# 2. 开发... vim 写代码，make 编译

# 3. 提交（建议每完成一个小功能就提交一次）
git add .
git status                   # 检查改了啥，养成习惯
git commit -m "完成 PA1 第一阶段"

# 4. 推送
git push origin main

# 5. 拉取官方更新
git pull origin main
```

> PA 提示：每个阶段结束记得提交并 push，方便回退和对比。养成 add → commit → push 的习惯。

### 六、常用操作速查

| 操作 | 命令 |
| ---- | ---- |
| 查看状态 | `git status` |
| 添加文件 | `git add <file>` / `git add .` |
| 提交变更 | `git commit -m "message"` |
| 推送 | `git push origin <branch>` |
| 拉取 | `git pull origin <branch>` |
| 查看历史 | `git log --oneline --graph` |
| 创建并切换分支 | `git checkout -b <branch>` |
| 取消暂存 | `git reset HEAD <file>` |
| 修改最后一次提交 | `git commit --amend` |
| 回退（保留修改） | `git reset --soft <commit>` |
| 回退（丢弃修改） | `git reset --hard <commit>`（慎用） |
| 查看所有操作记录 | `git reflog` |
| 暂存当前修改 | `git stash` |
| 恢复暂存 | `git stash pop` |

PS：vscode 的 Git 图形界面确实好用，但命令行也要会用，SSH 到服务器上就只有命令行。

## Linux 常用命令

PA 全程在 Linux 下操作，这些命令必须熟。

### 文件与目录

| 命令 | 作用 |
| ---- | ---- |
| `ls -al` | 列出所有文件（含隐藏） |
| `cd <dir>` | 切换目录 |
| `pwd` | 显示当前路径 |
| `cp -r <src> <dst>` | 复制（递归） |
| `mv <src> <dst>` | 移动 / 重命名 |
| `rm -rf <dir>` | 删除（慎用） |
| `mkdir -p <dir>` | 创建多级目录 |
| `cat` / `less <file>` | 查看文件 |
| `find . -name "*.c"` | 按名查找 |
| `grep -rn "xxx" .` | 递归搜索内容 |
| `chmod +x <file>` | 加执行权限 |
| `ln -s <target> <link>` | 软链接 |
| `wc -l <file>` | 统计行数 |

### 进程与作业

| 命令 | 作用 |
| ---- | ---- |
| `ps aux` | 查看进程 |
| `kill -9 <pid>` | 强杀进程 |
| `top` / `htop` | 实时监控 |
| `Ctrl+C` | 中断当前程序 |
| `Ctrl+Z` | 挂起，`fg` 恢复前台 |
| `<cmd> &` | 后台运行 |

### 管道与重定向

| 语法 | 作用 |
| ---- | ---- |
| `cmd > file` | 输出重定向到文件（覆盖） |
| `cmd >> file` | 追加 |
| `cmd 2>&1` | 错误输出也一起 |
| `a \| b` | 管道，a 的输出喂给 b |

### 易忘点

- `man <cmd>` 查手册，`<cmd> --help` 快速帮助
- `Tab` 补全，`Ctrl+R` 反向搜索历史命令
- `~` 家目录，`.` 当前目录，`..` 上级目录

## 二进制工具

PA1 要观察 ELF 文件结构，常用的几个：

| 命令 | 作用 |
| ---- | ---- |
| `file <bin>` | 查看文件类型 |
| `objdump -d <bin>` | 反汇编 |
| `objdump -h <bin>` | 查看段头 |
| `readelf -h <bin>` | 查看 ELF 头 |
| `readelf -S <bin>` | 查看 section |
| `nm <bin>` | 查看符号表 |
| `xxd <file>` | 十六进制查看 |

## Vim 使用

Vim 是终端下的文本编辑器，PA 全程都要用。

### 基本模式
- **普通模式（Normal）**：默认进入，用于移动光标、删除、复制粘贴等。
- **插入模式（Insert）**：按 `i` 进入，可编辑文本；按 `Esc` 返回普通模式。
- **命令模式（Command）**：按 `:` 进入，可执行保存、退出、查找等命令。

### 常用操作

| 操作 | 命令 | 说明 |
| ---- | ---- | ---- |
| 保存文件 | `:w` | 保存当前修改 |
| 退出 Vim | `:q` | 未修改时直接退出 |
| 强制退出 | `:q!` | 不保存修改，强制退出 |
| 保存并退出 | `:wq` / `ZZ` | 保存后关闭 |
| 光标移动 | `h` `j` `k` `l` | 左下上右 |
| 文件头 / 尾 | `gg` / `G` | 跳到顶部 / 底部 |
| 行首 / 行尾 | `0` / `$` | |
| 下一个 / 上一个单词 | `w` / `b` | |
| 删除字符 / 整行 | `x` / `dd` | |
| 撤销 / 重做 | `u` / `Ctrl+r` | |
| 复制整行 / 粘贴 | `yy` / `p` | |
| 插入 | `i`（前）/ `a`（后）/ `o`（下行） | |
| 搜索 | `/关键词`，`n` / `N` 跳转 | |
| 清除高亮 | `:nohl` | |
| 全文替换 | `:%s/old/new/g` | |
| 折叠 / 展开 | `za`，`zR` 全展开，`zM` 全折叠 | |
| 垂直 / 水平分屏 | `:vs <file>` / `:sp <file>` | |

直接输入 **vimtutor** 有官方教程。

[菜鸟教程 vim](https://www.runoob.com/linux/linux-vim.html)

## GCC 与 Make

### GCC 编译过程
一个 C 程序的编译通常分为四个阶段：
1. **预处理**（`-E`）：处理 `#include`、`#define`
2. **编译**（`-S`）：生成汇编代码
3. **汇编**（`-c`）：生成目标文件
4. **链接**：生成可执行文件

### 常用 GCC 选项

| 选项 | 说明 |
| ---- | ---- |
| `-o <file>` | 指定输出文件名 |
| `-g` | 生成调试信息 |
| `-Wall` | 开启常见警告 |
| `-Wextra` | 额外警告 |
| `-O2` | 优化等级 2 |
| `-std=c99` | 指定 C 标准 |
| `-I<dir>` | 添加头文件路径 |
| `-L<dir>` | 添加库文件路径 |
| `-l<name>` | 链接指定库（如 `-lm`） |

### Makefile 基础

```makefile
CC = gcc
CFLAGS = -Wall -g
TARGET = myprog
OBJS = main.o util.o

$(TARGET): $(OBJS)
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET) $(OBJS)

.PHONY: clean
```

## GDB 基础使用

### 一、前提
编译代码时必须加 `-g`（生成调试信息）
```bash
gcc -g test.c -o test
gdb ./test
```

| 命令 | 简写 | 作用 |
|------|------|------|
| run | r | 运行程序 |
| break 行号/函数 | b | 设置断点 |
| next | n | 单步执行（不进入函数） |
| step | s | 单步执行（进入函数） |
| print 变量 | p | 查看变量值 |
| continue | c | 继续运行到下一个断点 |
| list | l | 显示源代码 |
| finish | - | 运行到当前函数结束 |
| quit | q | 退出 GDB |

### 常用命令示例
```bash
b main        # 在 main 函数打断点
b 20          # 在第 20 行打断点
p a           # 查看变量 a
p arr         # 看数组 arr
p &a          # 查看地址
```

### 基础调试流程
1. 启动 gdb
2. 设置断点
3. run 运行
4. n / s 单步执行
5. p 查看变量
6. 找到问题后 quit 退出

## Tmux 终端复用器

Tmux 让你在一个终端窗口中同时管理多个会话、窗口和面板，特别适合远程开发和长时间运行的任务。

### 基本概念
- **会话（Session）**：独立的工作环境，可以断开后重新连接
- **窗口（Window）**：会话内的标签页
- **面板（Pane）**：窗口内的分屏区域

### 常用快捷键（前缀 `Ctrl+b`）

| 操作 | 快捷键 |
| ---- | ------ |
| 新建会话（终端外） | `tmux new -s name` |
| 分离会话 | `Ctrl+b d` |
| 重新连接 | `tmux attach -t name` |
| 查看会话列表 | `tmux ls` |
| 垂直 / 水平分屏 | `Ctrl+b %` / `Ctrl+b "` |
| 切换面板 | `Ctrl+b 方向键` |
| 新建 / 切换窗口 | `Ctrl+b c` / `Ctrl+b n`（下）`Ctrl+b p`（上） |
| 关闭面板 | `Ctrl+b x` |
| 重命名窗口 | `Ctrl+b ,` |
| 调整面板大小 | `Ctrl+b 方向键` 或 `Alt+方向键` |
| 切换布局 | `Ctrl+b Space` |
| 复制模式 | `Ctrl+b [`，`Space` 选择，`Enter` 复制，`Ctrl+b ]` 粘贴 |

> **PA 建议**：开一个 Tmux 会话分三个面板——代码编辑区、编译运行区、GDB 调试区，效率高很多。

### 自定义配置示例

加到 `~/.tmux.conf`：

```conf
set -g prefix C-a
unbind C-b
bind C-a send-prefix
set -g mouse on
bind r source-file ~/.tmux.conf \; display "Reloaded!"
```

[tmux教程](https://www.ruanyifeng.com/blog/2019/10/tmux.html)

# 目前进度

当前完成 pa0，完成大部分环境搭建。

- [x] pa0
- [x] pa1
- [ ] pa2
- [ ] pa3
- [ ] pa4
