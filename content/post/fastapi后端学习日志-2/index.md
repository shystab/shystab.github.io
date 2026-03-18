---
title: "fastapi后端学习记录-2"
date: 2026-03-17T23:30:00+08:00
lastmod: 2026-03-17T23:30:00+08:00
author: "Shysta"

draft: false
summary: "后端学习日志"
description: "本文记录后端的一些学习历程"

categories: ["学习"]
tags: ["Fastapi", "全栈","后端"] 

cover: "/images/sixth.jpg" 

toc: true
comments: true
math: false
mermaid: false
copyright: true
outdated: false
sponsor: false

keywords: ["Fastapi", "全栈"]
---
# Fastapi内容


## 框架基石与开发环境
首先是贴一个官网 以及看文档真的看得我很痛苦
[fast官方网站](https://fastapi.tiangolo.com/zh/)

目前官方推荐安装模式
```python
# 官方推荐的标准安装（一步到位）
pip install "fastapi[standard]"
```

虽然我一开始不是这样安装的嘻嘻


### 路径操作装饰器

路由是一种将请求方法+url路径 链接到对应处理函数的映射关系
- 路径：指 URL 中的路径部分，比如 /users、/items/42。
- 操作：指 HTTP 方法（操作），比如 GET、POST、PUT、DELETE 等。
- 装饰器：Python 的一种语法，用于在定义函数时给函数附加额外功能（用 @ 符号）。

**路径操作装饰器的作用是：**
把一个普通的 Python 函数，与一个特定的 HTTP 方法和 URL 路径绑定在一起，告诉 FastAPI：“当用户请求这个路径、使用这个 HTTP 方法时，就自动调用这个函数来处理，并把函数的返回值返回给客户端。

**@app.get("/")**
- @app.	@app.	固定前缀，表示这是 FastAPI 应用实例的方法
- HTTP 方法	get、post 等	指定要处理的 HTTP 方法
- 路径	"/"、"/items/{item_id}"	URL 路径，可以包含参数占位符（如 {item_id}）
- 其他参数	response_model, status_code	可选，用于控制响应格式、状态码、标签、文档描述等（写在括号内）

### 类型提示 (Type Hints)
annonated作为python3.9新提出的 官方推荐作为新写法替换以往内容
bool | None = None则是3.10用于替换optional的


## 请求处理 (Request Handling)

| 参数类型 | 数据来源 | 主要用途 | FastAPI 声明方式 |
| :--- | :--- | :--- | :--- |
| 路径参数 | URL 路径中（如 `/users/42`） | 资源标识（ID） | 函数参数同名 |
| 查询参数 | URL `?` 之后（如 `?page=2`） | 过滤、分页、排序 | 函数参数默认值 |
| 请求体 | HTTP 报文 body（JSON） | 提交创建/更新数据 | Pydantic 模型 |
| 请求头 | HTTP 头部 | 认证、客户端信息 | `Header()` |
| Cookie | 请求头中的 `Cookie` 字段 | 会话管理 | `Cookie()` |
| 表单数据 | `application/x-www-form-urlencoded` | 传统表单提交 | `Form()` |
| 文件上传 | `multipart/form-data` | 上传文件 | `File()` / `UploadFile` |

请求参数的内容 比如路径参数 请求参数都可作为处理函数的参数 分别起到索引和筛选等功能

### 路径操作与参数： 路径参数 查询参数

路径参数：从 URL 路径中捕获参数，使用 Python 类型提示声明类型（也就是说和路劲中一样 变量名也就在路径里）
查询参数：作为URL 中 ? 之后的部分，函数中未在路径中声明的参数会自动解释为查询参数。
> 我可以随意混搭
路径参数和查询参数可以同时存在
而path 和query参数作为其参数声明函数

### 请求体

就是用sqlmodel或者Pydantic 模型定义请求体的数据结构
这样可以传更多的数据 并且有集成的类型校验

`Field` 是 Pydantic 提供的字段函数，用于为模型字段添加额外的验证、元数据、默认值等。它通常用在 Pydantic 模型的属性上。
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., max_length=50, description="物品名称")
    price: float = Field(..., gt=0, le=10000, description="价格必须在0到10000之间")
    tax: float | None = Field(None, ge=0, description="税率（可选）")
```
###　请求头（Header） Cookie 参数

header从请求头中提取数据，常用于获取 User-Agent、Authorization 等。
cookie从请求头的 Cookie 字段中提取特定 Cookie 值。

表单和文件不谈 表单太老了 不用了

## 响应处理

### 返回任意数据
python的优良性质 返回字典等内容很方便
可以直接返回 dict、list、Pydantic 模型，FastAPI 会自动转换为 JSON。

 ```python
@app.get("/hello")
async def hello():
    return {"msg": "hello"}   # 自动 JSON 化
```
也可使用 response_model 指定响应模型
用于过滤输出字段、保证响应格式一致。

```python
from pydantic import BaseModel

class ItemOut(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemOut)
async def create_item(item: Item):
    return item   # 只返回 name 和 price，忽略其他字段
response_model 可以控制输出中哪些字段被包含，并执行响应验证。
```

## pydantic模型

[官方文档](https://pydantic.com.cn/)

后话 目前对field path query body之类的内容理解更好了点 都只是对参数的额外补充。




