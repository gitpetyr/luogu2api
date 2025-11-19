# luogu2api

一个非官方的洛谷（Luogu） API 服务，洛谷保存站的公益实现。

## 主要特性

- 登录洛谷（返回 cookies）
- 获取题目信息（统计、标签、难度等）
- 获取题目完整描述（背景、输入输出、样例）
- 提交代码到指定题目（支持多语言、可尝试自动识别验证码）
- 查询提交记录详情与评测状态
- 获取洛谷文章与剪贴板内容

> 注意：本项目依赖对洛谷网页的解析与提交接口，使用时请遵守洛谷的使用条款与法律法规，合理使用本工具。验证码识别依赖第三方 OCR（ddddocr），识别可能不稳定。

## 本地运行

- Python 3.10+
- 需要安装依赖：FastAPI、Uvicorn、httpx、pydantic、beautifulsoup4、ddddocr、fake-useragent 等

开发模式下启动服务：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

启动后，默认会在 `http://127.0.0.1:8000` 提供服务，FastAPI 自动生成的交互文档在：

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 常用 API 示例

1) 登录（返回 cookies）

POST /api/auth/login

请求示例（JSON）：

```json
{ "username": "your_username", "password": "your_password" }
```

curl 示例：

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
	-H "Content-Type: application/json" \
	-d '{"username":"myuser","password":"mypassword"}'
```

成功返回示例：

```json
{ "success": true, "data": { /* cookies */ } }
```

2) 获取题目信息

GET /api/problem/{problem_id}

示例：

```bash
curl "http://127.0.0.1:8000/api/problem/P1000"
```

3) 获取题目描述

GET /api/problem/{problem_id}/statement

4) 提交代码

POST /api/problem/{problem_id}/submit

请求体（JSON）示例：

```json
{
	"language": "C++14",
	"code": "#include <iostream>\nint main(){std::cout<<\"hi\";}",
	"enable_o2": false
}
```

注意：提交需要提供登录返回的 cookies（作为 query 参数或 header 传入），并且存在验证码重试逻辑。

5) 查询提交记录与评测状态

- GET /api/record/{record_id}
- GET /api/record/{record_id}/status

6) 其它

- GET /api/article/{article_id}
- GET /api/paste/{paste_id}
- GET /api/languages

请以 `http://127.0.0.1:8000/docs` 中的接口文档为准，那里包含交互式说明与示例。

## 已知限制与注意事项

- OCR（验证码识别）并非 100% 准确，可能导致登录或提交失败。
- 通过爬取/解析洛谷页面实现功能，页面结构变化会导致部分接口失效。
- 避免频繁、大量自动化请求。
- 不要把 3K 惹毛了，到时候直接托管

## 贡献

欢迎 Issues / PR：

- 修复解析失败的情况
- 增加更可靠的验证码处理或手动验证码输入流程

在贡献前请先阅读仓库根目录的 `LICENSE` 文件。

## 联系与支持

如需帮助，可以在仓库中提 Issue。

3673398763

---