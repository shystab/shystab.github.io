---
title: "nju-ics-prepare"
date: 2026-03-25T16:30:00+08:00
lastmod: 2026-03-25T16:30:00+08:00
author: "Shysta"

draft: false
summary: "ics学习前置内容"
description: "ics路程漫漫啊"

categories: ["学习"]
tags: ["ics"] 

cover: "/images/ninth.jpg" 

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["ics"]
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

## git使用

| 操作 | 命令 |
| ---- | ---- |
| 克隆仓库 | `git clone <url>` |
| 查看状态 | `git status` |
| 添加文件 | `git add <file>` 或 `git add .` |
| 提交变更 | `git commit -m "message"` |
| 推送 | `git push` |
| 拉取 | `git pull` |
| 创建分支 | `git branch <branch>` |
| 切换分支 | `git checkout <branch>` |
| 合并分支 | `git merge <branch>` |
| 查看历史 | `git log` |

### 更详细的 Git 操作

#### 一、分支管理

- **查看所有分支**：`git branch -a`（包括远程分支）
- **创建并切换到新分支**：`git checkout -b <branch>`
- **删除本地分支**：`git branch -d <branch>`（安全删除）或 `git branch -D <branch>`（强制删除）
- **删除远程分支**：`git push origin --delete <branch>`
- **重命名当前分支**：`git branch -m <new-name>`
- **查看分支跟踪关系**：`git branch -vv`

#### 二、提交操作

- **修改最后一次提交**：`git commit --amend`（可修改提交信息或添加漏掉的文件）
- **暂存修改**：`git stash`（临时保存工作目录的修改）
- **恢复暂存**：`git stash pop`（恢复最近一次暂存）
- **查看暂存列表**：`git stash list`
- **选择性暂存**：`git stash push -p`（交互式选择要暂存的内容）

#### 三、撤销与回退

- **撤销工作目录的修改**：`git checkout -- <file>`（危险！不可恢复）
- **撤销已暂存的文件**：`git reset HEAD <file>`（将文件从暂存区移回工作区）
- **回退到指定提交**：
  - `git reset --soft <commit>`：保留修改，只回退提交历史
  - `git reset --mixed <commit>`：默认，回退提交历史并取消暂存
  - `git reset --hard <commit>`：彻底丢弃所有修改，谨慎使用！
- **查看操作记录**：`git reflog`（查看所有 HEAD 变更，可用于恢复误删分支或提交）

#### 四、远程仓库操作

- **添加远程仓库**：`git remote add origin <url>`
- **查看远程仓库**：`git remote -v`
- **拉取远程分支**：`git fetch origin`（只下载不合并）
- **拉取并合并**：`git pull origin <branch>`（相当于 `fetch` + `merge`）
- **推送并建立跟踪**：`git push -u origin <branch>`（首次推送时使用）
- **查看提交差异**：`git diff origin/main..HEAD`（比较本地与远程 main 分支）

#### 五、标签管理

- **创建标签**：`git tag v1.0`（轻量标签）或 `git tag -a v1.0 -m "version 1.0"`（带注释标签）
- **查看所有标签**：`git tag`
- **推送标签到远程**：`git push origin --tags`
- **删除标签**：`git tag -d v1.0`（本地）和 `git push origin --delete tag v1.0`（远程）

#### 六、合并与变基

- **合并分支**：`git merge <branch>`（保留分支历史）
- **变基**：`git rebase <branch>`（使提交历史线性整洁，但会改写历史）
- **交互式变基**：`git rebase -i HEAD~3`（修改最近 3 次提交）

> PA 提示：每个 PA 阶段结束后及时提交，方便回退和对比。
PS：vscode的git真好用 

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