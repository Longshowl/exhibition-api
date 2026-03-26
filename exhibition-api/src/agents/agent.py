"""
展会信息智能查询助手 Agent
功能：
1. 查询展会官网、公众号等基本信息
2. 搜索展商名录、参展企业名单
3. 识别展会图片中的展商信息
4. 将信息整合并生成Excel表格
"""
import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# 导入工具
from tools.exhibition_tools import (
    search_exhibition_info,
    search_exhibitor_list,
    search_exhibition_by_keywords
)
from tools.image_recognition_tool import (
    recognize_exhibitors_from_image,
    batch_recognize_exhibitors
)
from tools.excel_generation_tool import (
    generate_exhibitor_excel,
    generate_exhibition_summary_excel,
    convert_json_to_excel
)

# 配置文件路径
LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]

def build_agent(ctx=None):
    """
    构建展会信息查询助手 Agent
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    # 读取配置
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # 获取API配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    # 初始化LLM
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 注册所有工具
    tools = [
        search_exhibition_info,
        search_exhibitor_list,
        search_exhibition_by_keywords,
        recognize_exhibitors_from_image,
        batch_recognize_exhibitors,
        generate_exhibitor_excel,
        generate_exhibition_summary_excel,
        convert_json_to_excel
    ]
    
    # 创建Agent
    agent = create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
    
    return agent
