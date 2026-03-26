"""
Excel文档生成核心逻辑（无装饰器，可直接调用）
"""
from typing import List, Dict, Any, Optional
from coze_coding_dev_sdk import DocumentGenerationClient, XLSXConfig
import json


def generate_exhibitor_excel_core(
    exhibitors_data: List[Dict[str, Any]],
    file_name: str = "exhibitor_list"
) -> str:
    """
    将展商信息列表生成Excel表格文件。
    
    Args:
        exhibitors_data: 展商信息列表，每个元素是一个字典
        file_name: 生成的Excel文件名（不含扩展名，必须为英文）
        
    Returns:
        Excel文件的下载链接（24小时有效）
    """
    try:
        # 配置Excel样式
        config = XLSXConfig(
            header_bg_color="4472C4",  # 蓝色表头
            auto_width=True  # 自动调整列宽
        )
        
        client = DocumentGenerationClient(xlsx_config=config)
        
        # 生成Excel
        url = client.create_xlsx_from_list(
            data=exhibitors_data,
            title=file_name,
            sheet_name="展商名单"
        )
        
        return f"Excel文件已生成成功！\n\n下载链接：{url}\n\n链接有效期：24小时"
        
    except Exception as e:
        return f"生成Excel失败: {str(e)}"


def convert_json_to_excel_core(
    json_data: str,
    file_name: str = "data_export"
) -> str:
    """
    将JSON格式的数据转换为Excel表格。
    
    Args:
        json_data: JSON格式的字符串，包含数组数据
        file_name: 生成的Excel文件名（不含扩展名，必须为英文）
        
    Returns:
        Excel文件的下载链接（24小时有效）
    """
    try:
        # 解析JSON
        data = json.loads(json_data)
        
        if not isinstance(data, list):
            return "错误：JSON数据必须是数组格式"
        
        if not data:
            return "错误：JSON数据为空"
        
        config = XLSXConfig(
            header_bg_color="4472C4",
            auto_width=True
        )
        
        client = DocumentGenerationClient(xlsx_config=config)
        
        url = client.create_xlsx_from_list(
            data=data,
            title=file_name,
            sheet_name="数据"
        )
        
        return f"JSON数据已转换为Excel！\n\n数据行数：{len(data)}\n\n下载链接：{url}\n\n链接有效期：24小时"
        
    except json.JSONDecodeError as e:
        return f"JSON解析失败: {str(e)}"
    except Exception as e:
        return f"转换失败: {str(e)}"
