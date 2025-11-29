<div align="center">
  <h1>luogu2api</h1>
  <p>简体中文</p>
  <p>
    <img src="https://img.shields.io/badge/python-3.10+-blue" />
    <img src="https://img.shields.io/badge/fastapi-latest-brightgreen" />
    <img src="https://img.shields.io/github/last-commit/gitpetyr/luogu2api" />
    <img src="https://img.shields.io/github/license/gitpetyr/luogu2api" />
  </p>
</div>

一个非官方的洛谷（Luogu） API 服务，洛谷保存站的**轻量**公益实现。（感觉没甚屌用？qwq

> 🎲 随缘维护，欢迎 PR、Issue！

- qq：3673398763
- linux.do：liveless

洛谷保存站：[Luogu Saver](https://github.com/laikit-dev/luogu-saver)

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动，**访问 `/docs` 可以查看 Swagger 交互式文档。**

## API 调用方法

### 1. 登录

**端点：** `POST /api/auth/login`

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "cookie_name": "cookie_value"
  }
}
```

获得的 cookies 可用于后续需要认证的请求。

### 2. 获取题目信息

**端点：** `GET /api/problem/{problem_id}`

```bash
curl "http://localhost:8000/api/problem/P1000"
```

**查询参数：**
- `cookies` (可选): JSON 格式的 cookies，用于获取更多信息

**响应包含：** 题目 ID、标题、难度、提交统计等

### 3. 获取题目描述

**端点：** `GET /api/problem/{problem_id}/statement`

```bash
curl "http://localhost:8000/api/problem/P1000/statement"
```

**响应包含：** 题目背景、描述、输入输出格式、样例、提示等

### 4. 提交代码

**端点：** `POST /api/problem/{problem_id}/submit`

```bash
curl -X POST "http://localhost:8000/api/problem/P1000/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "C++14",
    "code": "#include <iostream>\nint main() { std::cout << \"Hello\"; return 0; }",
    "enable_o2": false,
    "cookies": "{\"cookie_name\": \"cookie_value\"}"
  }'
```

**请求参数：**
- `language`: 编程语言（如 C++14、Python 等）
- `code`: 代码内容
- `enable_o2`: 是否启用 O2 优化，仅**有 O2 优化选项**的才会真正开启（可选，默认 false）
- `cookies`: 登录后的 cookies（必需）

**响应示例：**
```json
{
  "submission_id": 12345678
}
```

### 5. 获取提交记录

**端点：** `GET /api/record/{record_id}`

```bash
curl "http://localhost:8000/api/record/12345678"
```

**响应包含：** 编译信息、评测结果、测试点分组等详细信息

### 6. 获取提交状态

**端点：** `GET /api/record/{record_id}/status`

```bash
curl "http://localhost:8000/api/record/12345678/status"
```

### 7. 获取支持的编程语言

**端点：** `GET /api/languages`

```bash
curl "http://localhost:8000/api/languages"
```

## 注意事项

- 某些端点需要在查询参数中传递 cookies，格式为 JSON 字符串

## 贡献指南

欢迎提交 Issue 和 Pull Request！无论是 bug 修复、功能建议还是代码优化，我都很感谢。由于项目采用随缘维护的策略，建议：

- 保持代码风格一致
- 添加必要的测试或文档说明
