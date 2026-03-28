---
title: "fastapi后端学习记录-1"
date: 2026-03-15T23:30:00+08:00
lastmod: 2026-03-15T23:30:00+08:00
author: "Shysta"

draft: false
summary: "后端学习日志"
description: "本文记录后端的一些学习历程"

categories: ["fastapi"]
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
# 后端基础概念

## HTTP协议基础
### 1.1 请求方法（HTTP Methods）

诸如 POST(创造) PUT（完整替换）GET（获取资源）PATCH（部分更新资源）DELETE（删除资源）
后端提供给访问者的接口 接收并返回相应内容

### 1.2 状态码（Status Codes）

服务器用三位数字告诉你请求的结果。就像考试成绩：2xx 是优秀，4xx 是你的问题，5xx 是老师改卷时系统崩了。

- **1xx（信息性）**：请求已收到，继续处理。（很少见）
- **2xx（成功）**：✅ 请求成功处理  
  - 200 OK：一切正常（GET 成功）  
  - 201 Created：资源创建成功（POST 成功）
- **3xx（重定向）**：需要跳转到另一个地址  
  - 301 Moved Permanently：资源永久搬家了  
  - 302 Found：临时跳转
- **4xx（客户端错误）**：❌ 你发错请求了  
  - 400 Bad Request：请求格式不对（比如缺少必要字段）  
  - 401 Unauthorized：没登录或登录失效  
  - 403 Forbidden：登录了但没有权限（比如普通用户想删管理员）  
  - 404 Not Found：资源不存在（URL 写错了）
- **5xx（服务器错误）**：💥 服务器自己出问题了  
  - 500 Internal Server Error：服务器内部错误（代码崩了）  
  - 503 Service Unavailable：服务暂时不可用（比如服务器过载）

### 1.3请求头与响应头（Headers）

#### 请求头（客户端 → 服务器）
当客户端（如浏览器、App）向服务器发送请求时，会在请求头中附带额外的说明，帮助服务器理解如何处理这个请求。  
比如：`Host`、`User-Agent`、`Accept`、`Authorization`、`Cookie`、`Content-Type` 等。

#### 响应头（服务器 → 客户端）
服务器在处理完请求后，会在响应中添加响应头，告诉客户端如何解析返回的数据或执行后续操作。  
比如：`Content-Type`（请求头也有）、`Set-Cookie`、`Cache-Control`、`Access-Control-Allow-Origin` 等。

### 1.4 URL 结构
```text
https://www.example.com:443/path/to/resource?name=alice&page=2#section
\____/ \_____________/ \__/ \______/ \_______________________/ \_______/
 协议         域名         端口         路径               查询参数        片段
```

- 协议：http 或 https（加密的 http）
- 域名：服务器的地址（可解析为 IP）
- 端口：默认 http 80，https 443，可以省略
- 路径：资源在服务器上的位置，如 /users/123
- 查询参数：?key1=value1&key2=value2，用于过滤、排序、分页等
- 片段：前端页面内锚点，不会发送到服务器


##  RESTful API 设计原则

核心原则包括：

- 统一接口：每个资源有唯一URL，通过表示（Representation）进行操作，响应需自描述，且请求无状态。
- 资源导向：URI使用名词表示资源，如/users而非/getUsers。
- 标准HTTP方法：GET（查）、POST（增）、PUT（全量改）、PATCH（部分改）、DELETE（删）。
- 分层系统：支持代理、缓存、负载均衡等中间层。
- 可缓存：利用HTTP缓存头（ETag、Cache-Control）提升性能。

[详情 STFM](https://blog.csdn.net/2603_94941287/article/details/159087263)

## JSON 数据格式

JSON（JavaScript Object Notation）是目前最流行的API数据交换格式。它轻量、易读，几乎所有语言都支持。
```python
{
  "user": {
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com",
    "is_active": true,
    "tags": ["developer", "blogger"],
    "profile": null
  }
}
```
[json介绍](https://www.runoob.com/json/json-tutorial.html)

## Python 编程基础

### 1.Python核心语法

- 变量、数据类型（int、str、list、dict、set、tuple）
- 控制流（if、for、while）
- 函数定义、参数类型、默认参数、*args/**kwargs:
- 类与面向对象编程（继承、特殊方法）

#### 4.11 *args 和 **kwargs
- *args：接受任意数量的位置参数，打包成元组（tuple）。
- **kwargs：接受任意数量的关键字参数，打包成字典（dict）。

而对于面向对象编程 有c++基础会好很多 但有些不一样
```python
class User:
    # 类属性（所有实例共享）
    role = "普通用户"

    # 构造方法：初始化实例属性
    def __init__(self, name, age):
        self.name = name   # 实例属性
        self.age = age

    # 实例方法
    def greet(self):
        return f"你好，我是{self.name}，今年{self.age}岁。"

# 创建实例
alice = User("Alice", 25)
print(alice.greet())       # 输出：你好，我是Alice，今年25岁。
print(alice.role)          # 输出：普通用户

```

继承允许一个类（子类）获取另一个类（父类）的属性和方法，实现代码复用和扩展。
```python
class Admin(User):          # Admin 继承自 User
    role = "管理员"          # 覆盖父类的类属性

    def __init__(self, name, age, permissions):
        # 调用父类的构造方法，初始化 name 和 age
        super().__init__(name, age)
        self.permissions = permissions   # 新增属性

    # 新增方法
    def manage(self):
        return f"{self.name} 正在管理后台。"

    # 重写父类方法
    def greet(self):
        return f"管理员 {self.name}，您好！您有权限：{self.permissions}"

admin = Admin("Bob", 30, ["用户管理", "内容审核"])
print(admin.greet())        # 输出：管理员 Bob，您好！您有权限：['用户管理', '内容审核']
print(admin.manage())       # 输出：Bob 正在管理后台。
```
特殊方法（Magic Methods）
Python 类中以双下划线开头和结尾的方法称为特殊方法（或魔术方法），它们在特定情况下被自动调用。类似析构函数之类 __init__(self,…)

### 类型提示（Type Hints） ⭐️ FastAPI 的核心依赖
基本类型注解（int、str、float、bool）
容器类型（List[int]、Dict[str, Any]）
Optional（新版fastapi已不用 选择shysta= str | none 写法）、Union、Any
Python 3.10+ 新语法：str | None、list[int]
Annotated（Python 3.9+）：附加元数据，FastAPI 常用来组合 Query、Path 等

### 异步编程基础
同步 vs 异步
async / await 关键字
事件循环概念
[异步蟒蛇(bushi)](https://www.runoob.com/python3/python-asyncio.html)


更多内容 [STFW](https://www.runoob.com/python3/python3-tutorial.html)
以及这玩意确实是个及其全的cser网站 刚发现 ~亏大发了~

**本篇速查**

- HTTP 方法：GET 查、POST 增、PUT 全改、PATCH 部分改、DELETE 删
- 常用状态码：200、201、400、401、403、404、500
- 类型提示基础：str | None、list[int]、Annotated
- 异步与同步：async def 用于 IO 密集型操作，普通 def 在线程池运行
