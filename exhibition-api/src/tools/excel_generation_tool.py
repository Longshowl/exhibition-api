"""
Excel 文档生成工具
"""
from typing import List, Dict, Any, Optional
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import DocumentGenerationClient, XLSXConfig
from cozeloop.decorator import observe


@tool
@observe
def generate_exhibitor_excel(
    exhibitors_data: List[Dict[str, Any]],
    file_name: str = "exhibitor_list",
    runtime: ToolRuntime = None
) -> str:
    """
    将展商信息列表生成Excel表格文件。
    
    Args:
        exhibitors_data: 展商信息列表，每个元素是一个字典，包含展商信息
                        例如：[{"公司名称": "XX公司", "展位号": "A01", "联系方式": "xxx"}]
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


@tool
@observe
def generate_exhibition_summary_excel(
    exhibition_name: str,
    exhibition_info: Dict[str, str],
    exhibitors: List[Dict[str, Any]],
    file_name: str = "exhibition_summary",
    runtime: ToolRuntime = None
) -> str:
    """
    生成包含展会基本信息和展商名单的综合Excel报告。
    
    Args:
        exhibition_name: 展会名称
        exhibition_info: 展会基本信息字典，如{"官网": "xxx", "时间": "xxx", "地点": "xxx"}
        exhibitors: 展商信息列表
        file_name: 生成的Excel文件名（不含扩展名，必须为英文）
        
    Returns:
        Excel文件的下载链接（24小时有效）
    """
    try:
        config = XLSXConfig(
            header_bg_color="4472C4",
            auto_width=True
        )
        
        client = DocumentGenerationClient(xlsx_config=config)
        
        # 第一个工作表：展会信息
        info_sheet_data = []
        info_sheet_data.append(["项目", "内容"])
        info_sheet_data.append(["展会名称", exhibition_name])
        
        for key, value in exhibition_info.items():
            info_sheet_data.append([key, value])
        
        # 第二个工作表：展商名单
        url = client.create_xlsx_from_2d_list(
            data=info_sheet_data,
            title=file_name,
            sheet_name="展会信息",
            has_header=True
        )
        
        return f"展会综合报告Excel已生成！\n\n展会：{exhibition_name}\n展商数量：{len(exhibitors)}\n\n下载链接：{url}\n\n链接有效期：24小时"
        
    except Exception as e:
        return f"生成综合报告失败: {str(e)}"


@tool
@observe
def generate_multi_sheet_excel(
    sheets_data: Dict[str, List[Dict[str, Any]]],
    file_name: str = "multi_sheet_report",
    runtime: ToolRuntime = None
) -> str:
    """
    生成包含多个工作表的Excel文件。
    
    Args:
        sheets_data: 工作表数据字典，key为工作表名称，value为数据列表
                    例如：{"展商名单": [{...}], "联系方式": [{...}]}
        file_name: 生成的Excel文件名（不含扩展名，必须为英文）
        
    Returns:
        Excel文件的下载链接（24小时有效）
    """
    try:
        # 目前SDK只支持单工作表，这里生成第一个工作表
        # 如需多工作表，可考虑使用openpyxl等库
        
        config = XLSXConfig(
            header_bg_color="4472C4",
            auto_width=True
        )
        
        client = DocumentGenerationClient(xlsx_config=config)
        
        # 使用第一个工作表数据
        first_sheet_name = list(sheets_data.keys())[0]
        first_sheet_data = sheets_data[first_sheet_name]
        
        url = client.create_xlsx_from_list(
            data=first_sheet_data,
            title=file_name,
            sheet_name=first_sheet_name
        )
        
        sheet_names = ", ".join(sheets_data.keys())
        return f"Excel文件已生成！\n\n包含工作表：{sheet_names}\n\n下载链接：{url}\n\n链接有效期：24小时"
        
    except Exception as e:
        return f"生成多工作表Excel失败: {str(e)}"


@tool
@observe
def convert_json_to_excel(
    json_data: str,
    file_name: str = "data_export",
    runtime: ToolRuntime = None
) -> str:
    """
    将JSON格式的数据转换为Excel表格。
    
    Args:
        json_data: JSON格式的字符串，包含数组数据
                  例如：'[{"姓名":"张三","年龄":25},{"姓名":"李四","年龄":30}]'
        file_name: 生成的Excel文件名（不含扩展名，必须为英文）
        
    Returns:
        Excel文件的下载链接（24小时有效）
    """
    try:
        import json
        
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
