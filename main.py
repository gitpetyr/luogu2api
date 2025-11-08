from fastapi import FastAPI, HTTPException, Cookie, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from authmgr import login
from problems_mgr import (
    craw_probleminfo, 
    craw_statement, 
    submit_problem, 
    craw_submission_info, 
    craw_submission_status,
    languages_map
)
from miscellaneous import craw_article, craw_paste

app = FastAPI(
    title="洛谷API",
    description="非官方的洛谷API接口",
    version="1.0.0"
)

class LoginRequest(BaseModel):
    username: str
    password: str

class SubmitRequest(BaseModel):
    language: str
    code: str
    enable_o2: bool = False

async def get_cookies(
    cookies: str = Query(default=None)
) -> Dict[str, str]:
    if not cookies:
        return {}
    try:
        import json
        return json.loads(cookies)
    except:
        return {}

@app.post("/api/auth/login")
async def api_login(request: LoginRequest):
    """
    登录洛谷账号
    """
    result = login(request.username, request.password)
    if not result["success"]:
        raise HTTPException(
            status_code=401,
            detail=result
        )
    return result

@app.get("/api/problem/{problem_id}")
async def get_problem_info(
    problem_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取题目信息
    """
    result = craw_probleminfo(problem_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )
    return result

@app.get("/api/problem/{problem_id}/statement")
async def get_problem_statement(
    problem_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取题目描述
    """
    result = craw_statement(problem_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Problem statement not found"
        )
    return result

@app.post("/api/problem/{problem_id}/submit")
async def submit_code(
    problem_id: str,
    request: SubmitRequest,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    提交代码
    """
    try:
        submission_id = submit_problem(
            problem_id,
            request.language,
            request.code,
            request.enable_o2,
            cookies
        )
        return {"submission_id": submission_id}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/record/{record_id}")
async def get_submission_info(
    record_id: int,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取提交记录信息
    """
    result = craw_submission_info(record_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )
    return result

@app.get("/api/record/{record_id}/status")
async def get_submission_status(
    record_id: int,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取提交状态
    """
    result = craw_submission_status(record_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Submission status not found"
        )
    return result

@app.get("/api/article/{article_id}")
async def get_article(
    article_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取文章内容
    """
    result = craw_article(article_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )
    return result

@app.get("/api/paste/{paste_id}")
async def get_paste(
    paste_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取剪贴板内容
    """
    result = craw_paste(paste_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Paste not found"
        )
    return result

@app.get("/api/languages")
async def get_supported_languages():
    """
    获取支持的编程语言列表
    """
    return languages_map

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
