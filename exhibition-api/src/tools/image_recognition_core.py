"""
图片识别核心逻辑（无装饰器，可直接调用）
"""
from typing import Dict, List, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
import json


def recognize_exhibitors_from_image_core(image_url: str) -> str:
    """
    识别展会现场图片中的展商信息。
    
    Args:
        image_url: 展会现场图片的URL地址
        
    Returns:
        识别出的展商信息列表
    """
    ctx = new_context(method="image.recognition")
    client = LLMClient(ctx=ctx)
    
    # 构建提示词
    system_prompt = """你是一个专业的展会信息识别助手。你的任务是分析展会现场图片，识别并提取其中的展商信息。

请仔细观察图片中的所有文字和标志，提取以下信息（如果可见）：
1. 公司名称/品牌名称
2. 展位号
3. 联系方式（电话、邮箱、微信等）
4. 展示的产品类型或主营业务
5. 其他可见的重要信息

请以结构化的JSON格式返回识别结果，格式如下：
{
  "exhibitors": [
    {
      "company_name": "公司名称",
      "booth_number": "展位号",
      "contact_info": {
        "phone": "电话",
        "email": "邮箱",
        "wechat": "微信"
      },
      "business_type": "主营业务",
      "products": "展示产品",
      "notes": "其他备注信息"
    }
  ],
  "summary": "整体识别情况说明"
}

如果某个字段无法识别，请设为null。确保返回有效的JSON格式。"""

    try:
        # 构建多模态消息
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=[
                {
                    "type": "text",
                    "text": "请识别这张展会现场图片中的展商信息。"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ])
        ]
        
        # 调用视觉模型
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-vision-250815",
            temperature=0.3
        )
        
        # 处理响应内容
        content = response.content
        if isinstance(content, str):
            result_text = content
        elif isinstance(content, list):
            # 提取文本部分
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            result_text = " ".join(text_parts)
        else:
            result_text = str(content)
        
        # 尝试解析JSON
        try:
            # 提取JSON部分（可能包含在markdown代码块中）
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                json_str = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                json_str = result_text[json_start:json_end].strip()
            else:
                json_str = result_text
            
            # 解析JSON
            result_data = json.loads(json_str)
            
            # 格式化输出
            output_lines = []
            output_lines.append("## 图片识别结果\n")
            
            if "exhibitors" in result_data and result_data["exhibitors"]:
                output_lines.append(f"识别到 {len(result_data['exhibitors'])} 个展商信息：\n")
                
                for i, exhibitor in enumerate(result_data["exhibitors"], 1):
                    output_lines.append(f"### 展商 {i}")
                    if exhibitor.get("company_name"):
                        output_lines.append(f"- **公司名称**：{exhibitor['company_name']}")
                    if exhibitor.get("booth_number"):
                        output_lines.append(f"- **展位号**：{exhibitor['booth_number']}")
                    
                    contact_info = exhibitor.get("contact_info", {})
                    if any(contact_info.values()):
                        output_lines.append("- **联系方式**：")
                        if contact_info.get("phone"):
                            output_lines.append(f"  - 电话：{contact_info['phone']}")
                        if contact_info.get("email"):
                            output_lines.append(f"  - 邮箱：{contact_info['email']}")
                        if contact_info.get("wechat"):
                            output_lines.append(f"  - 微信：{contact_info['wechat']}")
                    
                    if exhibitor.get("business_type"):
                        output_lines.append(f"- **主营业务**：{exhibitor['business_type']}")
                    if exhibitor.get("products"):
                        output_lines.append(f"- **展示产品**：{exhibitor['products']}")
                    if exhibitor.get("notes"):
                        output_lines.append(f"- **备注**：{exhibitor['notes']}")
                    output_lines.append("")
            else:
                output_lines.append("未能从图片中识别到明确的展商信息。")
            
            if result_data.get("summary"):
                output_lines.append(f"\n**识别说明**：{result_data['summary']}")
            
            return "\n".join(output_lines)
            
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回原始文本
            return f"## 图片识别结果\n\n{result_text}"
        
    except Exception as e:
        return f"图片识别失败: {str(e)}"


def batch_recognize_exhibitors_core(image_urls: List[str]) -> str:
    """
    批量识别多张展会现场图片中的展商信息。
    
    Args:
        image_urls: 展会现场图片URL列表
        
    Returns:
        整合后的展商信息列表
    """
    ctx = new_context(method="image.batch_recognition")
    client = LLMClient(ctx=ctx)
    
    system_prompt = """你是一个专业的展会信息识别助手。请分析提供的多张展会现场图片，识别并整合所有展商信息。

请识别每张图片中的：
1. 公司名称/品牌名称
2. 展位号
3. 联系方式
4. 主营业务

如果同一公司在多张图片中出现，请合并信息。以JSON格式返回：
{
  "exhibitors": [
    {
      "company_name": "公司名称",
      "booth_number": "展位号",
      "contact_info": {"phone": "", "email": "", "wechat": ""},
      "business_type": "主营业务",
      "source_images": ["图片索引"]
    }
  ],
  "total_found": 展商总数
}"""

    try:
        # 构建多图片消息
        content_blocks = [
            {
                "type": "text",
                "text": f"请识别这 {len(image_urls)} 张展会图片中的所有展商信息，并整合去重。"
            }
        ]
        
        for img_url in image_urls:
            content_blocks.append({
                "type": "image_url",
                "image_url": {"url": img_url}
            })
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=content_blocks)
        ]
        
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-vision-250815",
            temperature=0.3
        )
        
        # 处理响应
        content = response.content
        if isinstance(content, str):
            result_text = content
        elif isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            result_text = " ".join(text_parts)
        else:
            result_text = str(content)
        
        # 尝试解析并格式化输出
        try:
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                json_str = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                json_str = result_text[json_start:json_end].strip()
            else:
                json_str = result_text
            
            result_data = json.loads(json_str)
            
            output = []
            output.append("## 批量识别结果\n")
            output.append(f"共处理 {len(image_urls)} 张图片\n")
            
            if "exhibitors" in result_data and result_data["exhibitors"]:
                output.append(f"识别到 {len(result_data['exhibitors'])} 个展商\n")
                
                for i, exhibitor in enumerate(result_data["exhibitors"], 1):
                    output.append(f"{i}. **{exhibitor.get('company_name', '未知公司')}**")
                    if exhibitor.get("booth_number"):
                        output.append(f"   展位号：{exhibitor['booth_number']}")
                    output.append("")
            else:
                output.append("未识别到展商信息")
            
            return "\n".join(output)
            
        except json.JSONDecodeError:
            return f"## 批量识别结果\n\n{result_text}"
        
    except Exception as e:
        return f"批量识别失败: {str(e)}"
