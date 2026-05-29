---
title: "nju-ics-prepare"
date: 2026-03-25T16:30:00+08:00
lastmod: 2026-05-29T22:00:00+08:00
author: "Shysta"

draft: false
summary: "ICS 前置学习内容：Vim、Tmux、Git、GCC、Makefile、GDB"
description: "为 NJU ICS PA 实验做准备，整理 Vim 操作、Tmux 终端复用、Git 完整工作流（含配置/认证/多 remote）、GCC编译、Makefile 和 GDB 调试的基础知识"

categories: ["学习"]
tags: ["ics", "Git", "Vim", "Tmux", "GDB", "GCC", "Makefile"]

cover: "/images/ninth.jpg" 

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["ICS", "PA", "Vim", "Tmux", "Git", "GDB", "GCC", "Makefile", "NJU"]
---
# ics学习前置
我看的是21年的
https://nju-projectn.github.io/ics-pa-gitbook/ics2021/index.html文档内容 

每年的内容应该不会有什么变化 

[25年的在这里](https://ysyx.oscc.cc/docs/ics-pa/)
## Vim 使用

Vim 是一个强大的文本编辑器，在终端环境下非常高效。掌握 Vim 的基本操作对后续的 PA（编程作业）很有帮助。

### 基本模式
- **普通模式（Normal）**：默认进入模式，用于移动光标、删除、复制粘贴等。
- **插入模式（Insert）**：按 `i` 进入，可编辑文本；按 `Esc` 返回普通模式。
- **命令模式（Command）**：按 `:` 进入，可执行保存、退出、查找等命令。

### 常用操作
#### 一、基础文件操作
| 操作         | 命令          | 说明                     |
|--------------|---------------|--------------------------|
| 保存文件     | `:w`          | 保存当前修改             |
| 退出 Vim     | `:q`          | 未修改时直接退出         |
| 强制退出     | `:q!`         | 不保存修改，强制退出     |
| 保存并退出   | `:wq` / `ZZ`  | 保存文件后关闭 Vim       |

#### 二、光标移动操作
| 操作         | 命令          | 说明                     |
|--------------|---------------|--------------------------|
| 左/下/上/右  | `h` `j` `k` `l` | 基础光标移动           |
| 跳转到文件头 | `gg`          | 快速回到代码顶部         |
| 跳转到文件尾 | `G`           | 快速跳转到代码底部       |
| 跳转到行首   | `0`           | 光标移至当前行最前端     |
| 跳转到行尾   | `$`           | 光标移至当前行最后端     |
| 下一个单词   | `w`           | 按单词向后快速移动       |
| 上一个单词   | `b`           | 按单词向前快速移动       |

#### 三、文本编辑操作
| 操作         | 命令          | 说明                     |
|--------------|---------------|--------------------------|
| 删除字符     | `x`           | 删除光标所在位置字符     |
| 删除整行     | `dd`          | 删除当前整行代码         |
| 撤销操作     | `u`           | 撤销上一步修改           |
| 重做撤销     | `Ctrl + r`    | 恢复被撤销的操作         |
| 复制整行     | `yy`          | 复制当前行代码           |
| 粘贴内容     | `p`           | 在光标后方粘贴           |
| 光标前插入   | `i`           | 进入编辑模式，光标前输入|
| 光标后插入   | `a`           | 进入编辑模式，光标后输入|
| 下方新建行   | `o`           | 光标下新建行并编辑       |

#### 四、搜索与替换
| 操作         | 命令          | 说明                     |
|--------------|---------------|--------------------------|
| 向下搜索     | `/关键词`     | 查找代码中的指定内容     |
| 向上搜索     | `?关键词`     | 反向查找指定内容         |
| 下一个结果   | `n`           | 跳转到下一个匹配项       |
| 上一个结果   | `N`           | 跳转到上一个匹配项       |
| 清除高亮     | `:nohl`       | 取消搜索后的高亮显示     |
| 全文替换     | `:%s/old/new/g` | 全局替换文本内容       |

#### 五、代码折叠（阅读源码必备）
| 操作         | 命令          | 说明                     |
|--------------|---------------|--------------------------|
| 折叠/展开    | `za`          | 切换当前代码块折叠状态   |
| 全部展开     | `zR`          | 一键展开所有折叠代码     |
| 全部折叠     | `zM`          | 一键折叠所有代码块       |

#### 六、分屏操作（多文件对照查看）
| 操作         | 命令                | 说明                     |
|--------------|---------------------|--------------------------|
| 垂直分屏     | `:vs 文件名`        | 左右分屏打开文件         |
| 水平分屏     | `:sp 文件名`        | 上下分屏打开文件         |
| 切换分屏     | `Ctrl + w + 方向键` | 在分屏窗口之间切换光标   |

以及 直接输入**vimtutor**的教程

[菜鸟教程 vim](https://www.runoob.com/linux/linux-vim.html)

## Tmux 终端复用器
Tmux 让你在一个终端窗口中同时管理多个会话、窗口和面板，特别适合远程开发和长时间运行的任务。

### 基本概念
- **会话（Session）**：独立的工作环境，可以断开后重新连接
- **窗口（Window）**：会话内的标签页。
- **面板（Pane）**：窗口内的分屏区域。

### 常用快捷键（前缀 `Ctrl+b`）
| 操作 | 快捷键 |
| ---- | ------ |
| 新建会话（终端外） | `tmux new -s name` |
| 分离会话 | `Ctrl+b d` |
| 重新连接 | `tmux attach -t name` |
| 查看会话列表 | `tmux ls` |
| 垂直分屏 | `Ctrl+b %` |
| 水平分屏 | `Ctrl+b "` |
| 切换面板 | `Ctrl+b 方向键` |
| 新建窗口 | `Ctrl+b c` |
| 切换窗口 | `Ctrl+b n`（下一个）、`Ctrl+b p`（上一个） |
| 关闭面板 | `Ctrl+b x` |
| 重命名窗口 | `Ctrl+b ,` |

### 常用命令（终端内）
- `tmux new -s work`：创建名为 work 的会话
- `tmux attach -t work`：重新连接
- `tmux kill-session -t work`：结束会话
- `tmux list-sessions`：列出所有会话

> **PA 建议**：在 PA 实验时，可以打开一个 Tmux 会话，分为三个面板：代码编辑区、编译运行区、GDB 调试区，效率会高很多。

### 高级面板管理
- **调整面板大小**：按住前缀键（`Ctrl+b`）后，再按方向键（`↑↓←→`）即可微调面板边界；或者按住前缀键后，按 `Alt+方向键` 进行更大步长的调整。
- **交换面板位置**：`Ctrl+b {`（向左交换） / `Ctrl+b }`（向右交换）。
- **将面板转换为独立窗口**：`Ctrl+b !`（将当前面板拆分为一个新窗口）。
- **关闭当前面板**：`Ctrl+b x` 或直接输入 `exit`。
- **面板布局切换**：`Ctrl+b Space` 循环切换几种预设布局（平铺、主次、垂直、水平等）。

### 复制模式与缓冲区
Tmux 支持在终端内复制文本，类似于 Vim 的复制模式。
1. **进入复制模式**：`Ctrl+b [`。
2. **移动光标**：使用 Vim 风格按键（`h`/`j`/`k`/`l`）或方向键。
3. **开始选择**：按 `Space` 进入选择模式，移动光标划定区域。
4. **复制选定内容**：按 `Enter` 将选中文本存入 Tmux 缓冲区。
5. **粘贴**：`Ctrl+b ]`（粘贴最近一次复制的内容）。
6. **查看缓冲区列表**：`Ctrl+b =`（列出历史缓冲区，可选择粘贴）。

### 会话恢复（持久化）
使用插件 `tmux-resurrect` 可以保存会话状态（窗口、面板、工作目录），重启后一键恢复。
1. 安装 TPM（Tmux Plugin Manager）后，在 `~/.tmux.conf` 中添加：
   ```conf
   set -g @plugin 'tmux-plugins/tmux-resurrect'
   ```
2. 保存当前会话：`Ctrl+b Ctrl+s`。
3. 恢复上次保存的会话：`Ctrl+b Ctrl+r`。

### 自定义配置示例
将以下内容添加到 `~/.tmux.conf` 可以优化体验：
```conf
# 将前缀键改为 Ctrl+a（更顺手）
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# 鼠标支持（允许用鼠标选择窗格、调整大小）
set -g mouse on

# 设置窗格边框颜色
set -g pane-border-style fg=colour240
set -g pane-active-border-style fg=colour39

# 快捷键：快速重新加载配置
bind r source-file ~/.tmux.conf \; display "Reloaded!"
```

[tmux教程](https://www.ruanyifeng.com/blog/2019/10/tmux.html)

## Git 使用

PA 全程都要跟 Git 打交道——clone 项目、提交代码、拉取更新。下面从最开始的配置一路讲到多 remote 场景，都是实际会用到的内容。

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
#                        ↑ 这个 URL 在你的 GitHub 仓库页面能看到

# 3. 推送到自己的仓库
git push -u mygit main
#        ↑ 这里用的是 mygit，不是 origin

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

# 2. 开发...
#    vim 写代码
#    make 编译

# 3. 提交（建议每完成一个小功能就提交一次）
git add .                    # 暂存所有修改
git status                   # 检查到底改了啥（养成习惯）
git commit -m "完成 PA1 第一阶段"

# 4. 推送到远程
git push origin main

# 5. 如果官方有更新，拉取
git pull origin main

# 6. 如果只想下载更新但不自动合并
git fetch origin
git log --oneline origin/main..HEAD  # 看看本地比远程多了什么
git merge origin/main                # 手动合并
```

> PA 提示：每个阶段结束后记得提交并 push，方便回退和对比。养成 add → commit → push 的习惯。

### 六、常用操作速查

#### 基础操作

| 操作 | 命令 |
| ---- | ---- |
| 克隆仓库 | `git clone <url>` |
| 查看状态 | `git status` |
| 添加文件 | `git add <file>` 或 `git add .` |
| 提交变更 | `git commit -m "message"` |
| 推送 | `git push origin <branch>` |
| 拉取 | `git pull origin <branch>` |
| 查看历史 | `git log --oneline --graph` |

#### 分支

| 操作 | 命令 |
| ---- | ---- |
| 创建并切换 | `git checkout -b <branch>` |
| 查看所有分支 | `git branch -a` |
| 删除本地分支 | `git branch -d <branch>` |
| 删除远程分支 | `git push origin --delete <branch>` |
| 重命名分支 | `git branch -m <new-name>` |

#### 撤销与回退

| 操作 | 命令 |
| ---- | ---- |
| 撤销未暂存的修改 | `git checkout -- <file>` |
| 取消暂存 | `git reset HEAD <file>` |
| 修改最后一次提交 | `git commit --amend` |
| 回退到指定提交（保留修改） | `git reset --soft <commit>` |
| 回退并丢弃修改 | `git reset --hard <commit>`（慎用） |
| 查看所有操作记录 | `git reflog` |

#### 远程仓库

| 操作 | 命令 |
| ---- | ---- |
| 添加远程仓库 | `git remote add <别名> <url>` |
| 查看远程列表 | `git remote -v` |
| 删除远程 | `git remote remove <别名>` |
| 拉取远程但不合并 | `git fetch <别名>` |
| 首次推送并建立跟踪 | `git push -u <别名> <分支>` |

#### 暂存与合并

| 操作 | 命令 |
| ---- | ---- |
| 暂存当前修改 | `git stash` |
| 恢复暂存 | `git stash pop` |
| 合并分支 | `git merge <branch>` |
| 变基 | `git rebase <branch>` |
| 交互式变基 | `git rebase -i HEAD~3` |

PS：vscode 的 Git 图形界面确实好用，但命令行也要会用，毕竟 SSH 到服务器上就只有命令行。 

## make gcc

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



## GDB 基础使用教程

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
b main #在 main 函数打断点
b 20 #在第 20 行打断点
p a #查看变量 a
p arr #看数组 arr
p &a #查看内存 / 地址内容
```

### 基础调试流程
1. 启动 gdb
2. 设置断点
3. run 运行
4. n /s 单步执行
5. p 查看变量
6. 找到问题后 quit 退出

# 目前进度
当前完成pa0 完成大部分环境搭建 

- [x]pa0
- [x]pa1
- []pa2
- []pa3
- []pa4