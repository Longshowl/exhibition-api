"""
展会信息查询相关工具
"""
from typing import Dict, List, Optional
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from cozeloop.decorator import observe


@tool
@observe
def search_exhibition_info(exhibition_name: str, runtime: ToolRuntime = None) -> str:
    """
    搜索展会的官方网站、官方公众号等基本信息。
    
    Args:
        exhibition_name: 展会名称，如"广交会"、"CES展"、"进博会"等
        
    Returns:
        包含展会官网链接、公众号、时间地点等信息的字符串
    """
    ctx = runtime.context if runtime else new_context(method="search.exhibition")
    client = SearchClient(ctx=ctx)
    
    # 构建搜索查询
    query = f"{exhibition_name} 官网 官方网站"
    
    try:
        # 搜索展会官网
        response = client.web_search(
            query=query,
            count=5,
            need_summary=True
        )
        
        results = []
        results.append(f"## {exhibition_name} 展会信息\n")
        
        if response.web_items:
            results.append("### 官方网站与相关信息：\n")
            for i, item in enumerate(response.web_items, 1):
                results.append(f"{i}. **{item.title}**")
                results.append(f"   - 来源：{item.site_name}")
                results.append(f"   - 链接：{item.url}")
                if item.snippet:
                    results.append(f"   - 简介：{item.snippet[:150]}...")
                results.append("")
        
        if response.summary:
            results.append("\n### AI摘要：\n")
            results.append(response.summary)
        
        return "\n".join(results)
        
    except Exception as e:
        return f"搜索展会信息失败: {str(e)}"


@tool
@observe
def search_exhibitor_list(exhibition_name: str, runtime: ToolRuntime = None) -> str:
    """
    搜索展会的参展商名录、参展企业名单等信息。
    
    Args:
        exhibition_name: 展会名称，如"广交会参展商"、"CES展参展名单"等
        
    Returns:
        包含参展商名单、企业列表等信息的字符串
    """
    ctx = runtime.context if runtime else new_context(method="search.exhibitor")
    client = SearchClient(ctx=ctx)
    
    # 构建多个搜索查询以获取更全面的信息
    queries = [
        f"{exhibition_name} 参展商名录",
        f"{exhibition_name} 参展企业名单",
        f"{exhibition_name} 展商列表"
    ]
    
    all_results = []
    seen_urls = set()
    
    try:
        for query in queries:
            response = client.web_search(
                query=query,
                count=5,
                need_summary=True
            )
            
            if response.web_items:
                for item in response.web_items:
                    if item.url not in seen_urls:
                        seen_urls.add(item.url)
                        all_results.append({
                            "title": item.title,
                            "url": item.url,
                            "site_name": item.site_name,
                            "snippet": item.snippet
                        })
        
        # 格式化输出
        output = []
        output.append(f"## {exhibition_name} 参展商信息\n")
        output.append(f"共找到 {len(all_results)} 条相关信息\n")
        
        if all_results:
            output.append("\n### 参展商名录来源：\n")
            for i, item in enumerate(all_results[:10], 1):  # 限制显示前10条
                output.append(f"{i}. **{item['title']}**")
                output.append(f"   - 来源：{item['site_name']}")
                output.append(f"   - 链接：{item['url']}")
                if item['snippet']:
                    output.append(f"   - 摘要：{item['snippet'][:150]}...")
                output.append("")
        else:
            output.append("暂未找到相关参展商名录信息，建议访问展会官网查看。")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"搜索参展商名录失败: {str(e)}"


@tool
@observe
def search_exhibition_by_keywords(
    keywords: str,
    location: Optional[str] = None,
    date_range: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    根据关键词搜索相关展会信息。
    
    Args:
        keywords: 搜索关键词，如"电子展"、"汽车展"、"消费品展"等
        location: 可选，展会地点，如"深圳"、"上海"、"广州"等
        date_range: 可选，时间范围，如"2025年3月"、"最近"等
        
    Returns:
        包含相关展会列表和链接的字符串
    """
    ctx = runtime.context if runtime else new_context(method="search.exhibition.keywords")
    client = SearchClient(ctx=ctx)
    
    # 构建搜索查询
    query_parts = [keywords]
    if location:
        query_parts.append(location)
    if date_range:
        query_parts.append(date_range)
    
    query = " ".join(query_parts) + " 展会"
    
    try:
        response = client.web_search(
            query=query,
            count=10,
            need_summary=True,
            time_range="1m"  # 搜索最近一个月的信息
        )
        
        results = []
        results.append(f"## 关键词搜索结果：{keywords}\n")
        
        if location:
            results.append(f"地区筛选：{location}")
        if date_range:
            results.append(f"时间筛选：{date_range}")
        results.append("")
        
        if response.web_items:
            results.append(f"找到 {len(response.web_items)} 个相关展会：\n")
            for i, item in enumerate(response.web_items, 1):
                results.append(f"{i}. **{item.title}**")
                results.append(f"   - 来源：{item.site_name}")
                results.append(f"   - 链接：{item.url}")
                if item.snippet:
                    results.append(f"   - 简介：{item.snippet[:150]}...")
                results.append("")
        else:
            results.append("未找到相关展会信息，请尝试其他关键词。")
        
        if response.summary:
            results.append("\n### 综合摘要：\n")
            results.append(response.summary)
        
        return "\n".join(results)
        
    except Exception as e:
        return f"搜索失败: {str(e)}"
