"""
展会信息查询助手 - REST API服务
用于企业微信智能机器人AI+对接
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

# 导入核心函数（无装饰器，可直接调用）
from tools.exhibition_core import (
    search_exhibition_info_core,
    search_exhibitor_list_core,
    search_exhibition_by_keywords_core
)
from tools.image_recognition_core import (
    recognize_exhibitors_from_image_core,
    batch_recognize_exhibitors_core
)
from tools.excel_generation_core import (
    generate_exhibitor_excel_core,
    convert_json_to_excel_core
)

# 创建FastAPI应用
app = FastAPI(
    title="展会信息查询助手API",
    description="提供展会信息查询、展商搜索、图片识别、Excel生成等功能",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 请求模型 ====================

class ExhibitionSearchRequest(BaseModel):
    """展会信息查询请求"""
    exhibition_name: str
    user_id: Optional[str] = None


class ExhibitorSearchRequest(BaseModel):
    """展商名录搜索请求"""
    exhibition_name: str
    user_id: Optional[str] = None


class KeywordSearchRequest(BaseModel):
    """关键词搜索展会请求"""
    keywords: str
    location: Optional[str] = None
    date_range: Optional[str] = None
    user_id: Optional[str] = None


class ImageRecognitionRequest(BaseModel):
    """图片识别请求"""
    image_url: str
    user_id: Optional[str] = None


class BatchImageRecognitionRequest(BaseModel):
    """批量图片识别请求"""
    image_urls: List[str]
    user_id: Optional[str] = None


class ExcelGenerationRequest(BaseModel):
    """Excel生成请求"""
    exhibitors_data: List[Dict[str, Any]]
    file_name: str = "exhibitor_list"
    user_id: Optional[str] = None


class JsonToExcelRequest(BaseModel):
    """JSON转Excel请求"""
    json_data: str
    file_name: str = "data_export"
    user_id: Optional[str] = None


class ChatRequest(BaseModel):
    """对话请求（用于企业微信AI+对接）"""
    query: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


# ==================== 响应模型 ====================

class ApiResponse(BaseModel):
    """统一API响应格式"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None


# ==================== API路由 ====================

@app.get("/")
async def root():
    """API根路径"""
    return {
        "service": "展会信息查询助手API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/api/chat - 对话接口（企业微信AI+主要对接）",
            "/api/search_exhibition - 查询展会信息",
            "/api/search_exhibitors - 搜索参展商名录",
            "/api/search_by_keywords - 关键词搜索展会",
            "/api/recognize_image - 识别图片展商",
            "/api/batch_recognize - 批量识别图片",
            "/api/generate_excel - 生成Excel表格",
            "/api/json_to_excel - JSON转Excel"
        ]
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ApiResponse)
async def chat(request: ChatRequest):
    """
    对话接口（用于企业微信AI+对接）
    根据用户输入自动识别意图并执行相应操作
    """
    try:
        query = request.query.lower()
        
        # 简单的意图识别
        if "展会" in query and ("信息" in query or "官网" in query or "查询" in query):
            # 提取展会名称（简单实现，实际可以用NLP）
            exhibition_name = query.replace("展会", "").replace("信息", "").replace("官网", "").replace("查询", "").strip()
            if exhibition_name:
                result = search_exhibition_info_core(exhibition_name)
                return ApiResponse(success=True, message="展会信息查询成功", data=result)
        
        elif "参展商" in query or "展商" in query or "名录" in query:
            exhibition_name = query.replace("参展商", "").replace("展商", "").replace("名录", "").replace("搜索", "").strip()
            if exhibition_name:
                result = search_exhibitor_list_core(exhibition_name)
                return ApiResponse(success=True, message="参展商名录查询成功", data=result)
        
        elif "excel" in query or "表格" in query:
            return ApiResponse(
                success=True, 
                message="请提供要生成Excel的展商数据",
                data={"hint": "您可以说：帮我把华为、比亚迪、大疆生成Excel表格"}
            )
        
        # 默认返回帮助信息
        help_text = """
我是展会信息查询助手，可以帮您：

1. 查询展会信息：例如"查询广交会信息"
2. 搜索参展商：例如"搜索广交会参展商"
3. 识别图片展商：发送展会图片
4. 生成Excel表格：将信息整理为表格

请问您需要什么帮助？
        """
        return ApiResponse(success=True, message="展会查询助手已就绪", data={"help": help_text})
        
    except Exception as e:
        return ApiResponse(success=False, message="处理失败", error=str(e))


@app.post("/api/search_exhibition", response_model=ApiResponse)
async def search_exhibition(request: ExhibitionSearchRequest):
    """
    查询展会信息
    返回展会官网、时间地点、主办方等信息
    """
    try:
        result = search_exhibition_info_core(request.exhibition_name)
        return ApiResponse(
            success=True,
            message=f"已查询到 {request.exhibition_name} 的相关信息",
            data={"result": result}
        )
    except Exception as e:
        return ApiResponse(success=False, message="查询失败", error=str(e))


@app.post("/api/search_exhibitors", response_model=ApiResponse)
async def search_exhibitors(request: ExhibitorSearchRequest):
    """
    搜索参展商名录
    返回展商名单、企业列表等信息
    """
    try:
        result = search_exhibitor_list_core(request.exhibition_name)
        return ApiResponse(
            success=True,
            message=f"已找到 {request.exhibition_name} 的参展商信息",
            data={"result": result}
        )
    except Exception as e:
        return ApiResponse(success=False, message="搜索失败", error=str(e))


@app.post("/api/search_by_keywords", response_model=ApiResponse)
async def search_by_keywords(request: KeywordSearchRequest):
    """
    根据关键词搜索相关展会
    支持按地区、时间筛选
    """
    try:
        result = search_exhibition_by_keywords_core(
            keywords=request.keywords,
            location=request.location,
            date_range=request.date_range
        )
        return ApiResponse(
            success=True,
            message=f"已找到与 {request.keywords} 相关的展会",
            data={"result": result}
        )
    except Exception as e:
        return ApiResponse(success=False, message="搜索失败", error=str(e))


@app.post("/api/recognize_image", response_model=ApiResponse)
async def recognize_image(request: ImageRecognitionRequest):
    """
    识别展会图片中的展商信息
    提取公司名称、展位号、联系方式等
    """
    try:
        result = recognize_exhibitors_from_image_core(request.image_url)
        return ApiResponse(
            success=True,
            message="图片识别成功",
            data={"result": result}
        )
    except Exception as e:
        return ApiResponse(success=False, message="识别失败", error=str(e))


@app.post("/api/batch_recognize", response_model=ApiResponse)
async def batch_recognize(request: BatchImageRecognitionRequest):
    """
    批量识别多张展会图片
    自动整合去重
    """
    try:
        result = batch_recognize_exhibitors_core(request.image_urls)
        return ApiResponse(
            success=True,
            message=f"已成功识别 {len(request.image_urls)} 张图片",
            data={"result": result}
        )
    except Exception as e:
        return ApiResponse(success=False, message="批量识别失败", error=str(e))


@app.post("/api/generate_excel", response_model=ApiResponse)
async def generate_excel(request: ExcelGenerationRequest):
    """
    生成展商信息Excel表格
    返回下载链接（24小时有效）
    """
    try:
        result = generate_exhibitor_excel_core(
            exhibitors_data=request.exhibitors_data,
            file_name=request.file_name
        )
        return ApiResponse(
            success=True,
            message="Excel表格已生成",
            data={"result": result}
        )
    except Exception as e:
        return ApiResponse(success=False, message="生成失败", error=str(e))


@app.post("/api/json_to_excel", response_model=ApiResponse)
async def json_to_excel(request: JsonToExcelRequest):
    """
    将JSON数据转换为Excel表格
    返回下载链接（24小时有效）
    """
    try:
        result = convert_json_to_excel_core(
            json_data=request.json_data,
            file_name=request.file_name
        )
        return ApiResponse(
            success=True,
            message="JSON已转换为Excel",
            data={"result": result}
        )
    except Exception as e:
        return ApiResponse(success=False, message="转换失败", error=str(e))


# ==================== 启动服务 ====================

if __name__ == "__main__":
    import os
    # Railway会自动分配端口到PORT环境变量
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
