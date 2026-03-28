---
title: "fastapi后端学习记录-3"
date: 2026-03-18T23:30:00+08:00
lastmod: 2026-03-18T23:30:00+08:00
author: "Shysta"

draft: false
summary: "后端学习日志"
description: "本文记录后端的一些学习历程"

categories: ["fastapi"]
tags: ["Fastapi", "全栈","后端"] 

cover: "/images/seventh.jpg" 

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["Fastapi", "全栈"]
---
## 依赖注入
看看官方内容
> 什么是「依赖注入」¶
> 在编程中，「依赖注入」指的是，你的代码（本文中为路径操作函数）声明其运行所需并要使用的东西：“依赖”。
> 然后，由该系统（本文中为 FastAPI）负责执行所有必要的逻辑，为你的代码提供这些所需的依赖（“注入”依赖）。
> 当你需要以下内容时，这非常有用：
> 共享业务逻辑（同一段代码逻辑反复复用）
> 共享数据库连接
> 实施安全、认证、角色权限等要求
> 以及更多其他内容...

逻辑：把通用的逻辑（逻辑校验、数据库连接、用户认证）剥离出来，按需注入。

```python
# 1. 定义依赖逻辑
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# 2. 注入依赖 (使用 Annotated 模式)
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons
```
这么看来 depend函数和path也是一个dio样

此外依赖可以嵌套 类也被视作可以实例化 所以也可以作为依赖


## 数据库操作 ORM

### 我用的是SQLmodel

在传统开发中，写：
SQLAlchemy 模型（定义数据库表）。
Pydantic 模型（定义 API 接收/返回的 JSON）。
SQLModel 的核心逻辑：
它通过 Python 的多重继承，让一个类既是数据库表，又是 Pydantic 模型。
class User(SQLModel, table=True): —— 这一行代码搞定两件事。
### 核心模式：Session 注入 
无论用哪种库，FastAPI 操作数据库的标准模式都是：定义 Session 依赖 -> 注入路由 -> 自动关闭。
1. 基础配置 (以 SQLModel 为例)
``` python
from sqlmodel import create_engine, Session, SQLModel

sqlite_url = "sqlite:///database.db"
# check_same_thread 仅针对 SQLite
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# 核心依赖：创建并确保关闭 Session
def get_session():
    with Session(engine) as session:
        yield session  # 处理请求时注入 session，处理完后自动跳回这里执行关闭

# 实际使用
SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/users/")
def create_user(user: User, session: SessionDep):
    session.add(user)      # 暂存到内存
    session.commit()       # 提交到硬盘
    session.refresh(user)  # 刷新以获取数据库生成的 ID
    return user
```
### 异步操作 (Async)
追求性能，需要切换到异步模式：
连接字符串：需加前缀，如 sqlite+aiosqlite:///...。
创建引擎：改用 ext.asyncio 提供的 create_async_engine。
函数声明：全部改为 async def，数据库操作加 await
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# 异步引擎
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

# 异步依赖
async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session

# 异步路由
@app.get("/users/")
async def read_users(session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await session.execute(select(User))
    return result.scalars().all()
```
ps 我做的小型项目用sqlite 不太适合异步模式 其实也用不到 大不了需要时候再换数据库成pgsql加sqlalchemy

### 关于yield

**FastAPI 中的 yield 依赖**
FastAPI 支持在依赖项中使用 yield，允许在请求前获取资源，在请求后清理资源（如关闭数据库连接）。这种依赖项称为带 yield 的依赖项。

yield 关键字让一个普通函数变成一个生成器函数。主要用在两个地方：
- 依赖项：管理资源生命周期（如数据库会话的获取与关闭）。
- 路径操作函数：直接 yield 数据，FastAPI 会自动将其包装为流式响应。

## 异步编程
### 事件循环与协程
- **事件循环（Event Loop）**:
事件循环是异步程序的核心调度器，它不断循环，负责：
接收新的任务（协程）
监听已完成的操作（如网络响应）
将结果返回给对应的等待者
- **协程（Coroutine）**:
协程是一种特殊的函数，可以在执行过程中暂停（让出控制权），并在将来恢复。在 Python 中，用 async def 定义的函数就是一个协程函数，调用它不会立即执行，而是返回一个协程对象。
- **任务（Task）**:
任务是对协程的进一步封装，可以并发地运行多个协程。当 await 一个任务时，程序会等待该任务完成；但你可以同时创建多个任务让它们在后台并发执行。
> **await 关键字**: await 用于等待一个可等待对象（如协程、Future、Task）完成，同时释放控制权给事件循环，让其他任务运行。


```python
async def say_after(delay, msg):
    await asyncio.sleep(delay)
    print(msg)

async def main():
    # 创建两个任务，它们会“同时”开始计时
    task1 = asyncio.create_task(say_after(2, "Hello"))
    task2 = asyncio.create_task(say_after(1, "World"))

    print("任务已创建，等待完成...")
    await task1  # 等待 task1 完成
    await task2  # 等待 task2 完成

asyncio.run(main())
# 输出顺序：
# 任务已创建，等待完成...
# World (1秒后)
# Hello (再过1秒后，总共2秒)
```

### 在 FastAPI 中混合同步与异步
async def 路由：在事件循环中运行，适合 IO 密集型操作。 
def 路由：在线程池中运行，不会阻塞事件循环，适合 CPU 密集型或简单操作。

### Python 异步编程的关键库

- asyncio：Python 标准库，提供事件循环、协程、任务等基础工具。
- aiohttp / httpx：支持异步的 HTTP 客户端，用于发送网络请求。
- asyncpg / databases：支持异步的数据库驱动。
- aiofiles：支持异步的文件读写。
- anyio：一个跨平台的异步库，FastAPI 的底层依赖之一，提供更高级的并发原语。

[异步文档](https://www.runoob.com/python3/python-asyncio.html)


## 异常处理
用 HTTPException 抛出标准 HTTP 错误，或自定义异常处理器。
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# 自定义异常处理器
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
```
[官方document](https://fastapi.tiangolo.com/zh/tutorial/handling-errors/#install-custom-exception-handlers)


目前：

- [x] FastAPI 框架基础
- [x] 数据库集成

待学：
- [] WebSocket
- [] openai
- [] ARG