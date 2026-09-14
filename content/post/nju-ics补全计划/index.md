---
title: "NJU ICS 前置准备"
date: 2026-03-25T16:30:00+08:00
lastmod: 2026-09-14T10:00:00+08:00
author: "Shysta"
draft: false
summary: "ICS PA 前置知识：Git、Linux 命令、二进制工具、Vim、GCC/Make、GDB、Tmux"
description: "NJU ICS PA 实验前置知识整理：Git 工作流、Linux 常用命令、二进制工具、Vim 操作、GCC 与 Makefile、GDB 调试、Tmux"

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

参考资料：

- [ics-pa-gitbook（2021）](https://nju-projectn.github.io/ics-pa-gitbook/ics2021/index.html)
- [PA 文档（2025）](https://ysyx.oscc.cc/docs/ics-pa/)

## Git

### 配置

初次使用需配置身份，否则 `commit` 会失败。

```bash
git config --global user.name "用户名"
git config --global user.email "邮箱"
git config --global core.editor "vim"   # 默认编辑器
git config --list                        # 查看配置
```

### 认证

**SSH（推荐）**

```bash
ssh-keygen -t ed25519 -C "邮箱"
cat ~/.ssh/id_ed25519.pub
```

将输出公钥添加到 GitHub → Settings → SSH and GPG keys。clone 时使用 SSH 地址。

**Personal Access Token（HTTPS）**

GitHub 自 2021 年起不再支持密码认证。在 Settings → Developer settings → Personal access tokens 生成 token，push 时以 token 作为密码。

### remote 与 origin

`origin` 是远程仓库的别名，由 `git clone` 自动创建，等价于：

```bash
git remote add origin <url>
```

```bash
git remote -v          # 查看所有 remote
git remote remove <名> # 删除 remote
```

多 remote 场景（clone 官方仓库并推送到自己的仓库）：

```bash
git clone <官方仓库>
git remote add mygit <自己的仓库>
git push -u mygit main     # 推送到自己的仓库
git pull origin main       # 从官方仓库拉取
git push mygit main        # 后续推送
```

### 常用命令

| 操作 | 命令 |
| ---- | ---- |
| 查看状态 | `git status` |
| 暂存 | `git add <file>` / `git add .` |
| 提交 | `git commit -m "message"` |
| 推送 | `git push origin <branch>` |
| 拉取 | `git pull origin <branch>` |
| 克隆 | `git clone <url>` |
| 查看历史 | `git log --oneline --graph` |

| 操作 | 命令 |
| ---- | ---- |
| 创建并切换分支 | `git checkout -b <branch>` |
| 查看分支 | `git branch -a` |
| 删除本地分支 | `git branch -d <branch>` |
| 删除远程分支 | `git push origin --delete <branch>` |
| 重命名分支 | `git branch -m <new-name>` |

| 操作 | 命令 |
| ---- | ---- |
| 撤销未暂存修改 | `git checkout -- <file>` |
| 取消暂存 | `git reset HEAD <file>` |
| 修改最后一次提交 | `git commit --amend` |
| 回退（保留修改） | `git reset --soft <commit>` |
| 回退（丢弃修改） | `git reset --hard <commit>` |
| 查看操作记录 | `git reflog` |
| 暂存修改 | `git stash` |
| 恢复暂存 | `git stash pop` |

## Linux 常用命令

### 文件与目录

| 命令 | 作用 |
| ---- | ---- |
| `ls -al` | 列出所有文件（含隐藏） |
| `cd <dir>` / `pwd` | 切换目录 / 显示当前路径 |
| `cp -r <src> <dst>` | 复制（递归） |
| `mv <src> <dst>` | 移动 / 重命名 |
| `rm -rf <dir>` | 删除 |
| `mkdir -p <dir>` | 创建多级目录 |
| `cat` / `less <file>` | 查看文件 |
| `find . -name "*.c"` | 按名查找 |
| `grep -rn "xxx" .` | 递归搜索内容 |
| `chmod +x <file>` | 添加执行权限 |
| `ln -s <target> <link>` | 软链接 |
| `wc -l <file>` | 统计行数 |

### 进程与作业

| 命令 | 作用 |
| ---- | ---- |
| `ps aux` | 查看进程 |
| `kill -9 <pid>` | 强制结束进程 |
| `top` / `htop` | 实时监控 |
| `Ctrl+C` | 中断当前程序 |
| `Ctrl+Z` | 挂起，`fg` 恢复前台 |
| `<cmd> &` | 后台运行 |

### 管道与重定向

| 语法 | 作用 |
| ---- | ---- |
| `cmd > file` | 输出重定向到文件（覆盖） |
| `cmd >> file` | 追加 |
| `cmd 2>&1` | 错误输出一并重定向 |
| `a \| b` | 管道，a 的输出作为 b 的输入 |

| 快捷键 | 作用 |
| ---- | ---- |
| `man <cmd>` / `<cmd> --help` | 查看手册 / 快速帮助 |
| `Tab` | 命令补全 |
| `Ctrl+R` | 反向搜索历史命令 |

## 二进制工具

PA1 需要观察 ELF 文件结构。

| 命令 | 作用 |
| ---- | ---- |
| `file <bin>` | 查看文件类型 |
| `objdump -d <bin>` | 反汇编 |
| `objdump -h <bin>` | 查看段头 |
| `readelf -h <bin>` | 查看 ELF 头 |
| `readelf -S <bin>` | 查看 section |
| `nm <bin>` | 查看符号表 |
| `xxd <file>` | 十六进制查看 |

## Vim

### 模式

| 模式 | 进入方式 | 用途 |
| ---- | ---- | ---- |
| 普通模式 | 默认 | 移动光标、删除、复制粘贴 |
| 插入模式 | `i` | 编辑文本，`Esc` 返回 |
| 命令模式 | `:` | 保存、退出、查找替换 |

### 操作

| 操作 | 命令 |
| ---- | ---- |
| 保存 / 退出 / 强制退出 | `:w` / `:q` / `:q!` |
| 保存并退出 | `:wq` 或 `ZZ` |
| 光标移动 | `h` `j` `k` `l` |
| 文件头 / 尾 | `gg` / `G` |
| 行首 / 行尾 | `0` / `$` |
| 上一个 / 下一个单词 | `b` / `w` |
| 删除字符 / 整行 | `x` / `dd` |
| 撤销 / 重做 | `u` / `Ctrl+r` |
| 复制整行 / 粘贴 | `yy` / `p` |
| 插入 | `i`（前）/ `a`（后）/ `o`（下行） |
| 搜索 | `/关键词`，`n` / `N` 跳转 |
| 清除搜索高亮 | `:nohl` |
| 全文替换 | `:%s/old/new/g` |
| 折叠 / 展开 | `za`，`zR` 全展开，`zM` 全折叠 |
| 垂直 / 水平分屏 | `:vs <file>` / `:sp <file>` |

参考：[vimtutor](https://www.runoob.com/linux/linux-vim.html)

## GCC 与 Make

### 编译过程

| 阶段 | 选项 | 输出 |
| ---- | ---- | ---- |
| 预处理 | `-E` | 展开宏与头文件 |
| 编译 | `-S` | 汇编代码 |
| 汇编 | `-c` | 目标文件 |
| 链接 | — | 可执行文件 |

### GCC 选项

| 选项 | 说明 |
| ---- | ---- |
| `-o <file>` | 指定输出文件名 |
| `-g` | 生成调试信息 |
| `-Wall` / `-Wextra` | 开启警告 |
| `-O2` | 优化等级 2 |
| `-std=c99` | 指定 C 标准 |
| `-I<dir>` | 头文件路径 |
| `-L<dir>` | 库文件路径 |
| `-l<name>` | 链接库（如 `-lm`） |

### Makefile

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

## GDB

编译时需加 `-g` 生成调试信息。

```bash
gcc -g test.c -o test
gdb ./test
```

| 命令 | 简写 | 作用 |
| ---- | ---- | ---- |
| run | r | 运行程序 |
| break <行号/函数> | b | 设置断点 |
| next | n | 单步（不进入函数） |
| step | s | 单步（进入函数） |
| print <变量> | p | 查看变量值 |
| continue | c | 运行到下一个断点 |
| list | l | 显示源代码 |
| finish | — | 运行到当前函数结束 |
| quit | q | 退出 |

```bash
b main        # 在 main 函数设断点
b 20          # 在第 20 行设断点
p a           # 查看变量 a
p arr         # 查看数组 arr
p &a          # 查看地址
```

## Tmux

### 概念

| 概念 | 说明 |
| ---- | ---- |
| 会话 Session | 独立工作环境，可断开后重连 |
| 窗口 Window | 会话内的标签页 |
| 面板 Pane | 窗口内的分屏区域 |

### 快捷键（前缀 `Ctrl+b`）

| 操作 | 快捷键 |
| ---- | ---- |
| 分离会话 | `Ctrl+b d` |
| 垂直 / 水平分屏 | `Ctrl+b %` / `Ctrl+b "` |
| 切换面板 | `Ctrl+b 方向键` |
| 新建 / 切换窗口 | `Ctrl+b c` / `Ctrl+b n`、`Ctrl+b p` |
| 关闭面板 | `Ctrl+b x` |
| 重命名窗口 | `Ctrl+b ,` |
| 调整面板大小 | `Ctrl+b 方向键` 或 `Alt+方向键` |
| 切换布局 | `Ctrl+b Space` |
| 复制模式 | `Ctrl+b [`，`Space` 选择，`Enter` 复制，`Ctrl+b ]` 粘贴 |

### 命令

| 命令 | 作用 |
| ---- | ---- |
| `tmux new -s <name>` | 新建会话 |
| `tmux attach -t <name>` | 重新连接 |
| `tmux ls` | 列出会话 |
| `tmux kill-session -t <name>` | 结束会话 |

### 配置

`~/.tmux.conf`：

```conf
set -g prefix C-a
unbind C-b
bind C-a send-prefix
set -g mouse on
bind r source-file ~/.tmux.conf \; display "Reloaded!"
```

参考：[tmux 教程](https://www.ruanyifeng.com/blog/2019/10/tmux.html)

## 进度

- [x] pa0
- [x] pa1
- [ ] pa2
- [ ] pa3
- [ ] pa4
