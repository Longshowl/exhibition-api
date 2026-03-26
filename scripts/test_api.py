"""
API服务测试脚本
直接测试API功能，无需启动服务器
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.exhibition_core import (
    search_exhibition_info_core,
    search_exhibitor_list_core
)
from tools.excel_generation_core import (
    generate_exhibitor_excel_core
)

def test_search_exhibition():
    """测试展会信息查询"""
    print("=" * 60)
    print("测试1: 查询广交会信息")
    print("=" * 60)
    
    result = search_exhibition_info_core("广交会")
    print(result[:500] + "...\n")
    print("✅ 展会信息查询测试通过\n")


def test_search_exhibitors():
    """测试展商名录搜索"""
    print("=" * 60)
    print("测试2: 搜索广交会参展商")
    print("=" * 60)
    
    result = search_exhibitor_list_core("广交会")
    print(result[:500] + "...\n")
    print("✅ 展商名录搜索测试通过\n")


def test_generate_excel():
    """测试Excel生成"""
    print("=" * 60)
    print("测试3: 生成Excel表格")
    print("=" * 60)
    
    exhibitors_data = [
        {"公司名称": "华为技术有限公司", "展位号": "A01", "主营业务": "通信设备"},
        {"公司名称": "比亚迪股份有限公司", "展位号": "A02", "主营业务": "新能源汽车"},
        {"公司名称": "大疆创新科技有限公司", "展位号": "A03", "主营业务": "无人机"}
    ]
    
    result = generate_exhibitor_excel_core(exhibitors_data, "test_exhibitors")
    print(result)
    print("✅ Excel生成测试通过\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("展会信息查询助手 - API功能测试")
    print("=" * 60 + "\n")
    
    try:
        test_search_exhibition()
        test_search_exhibitors()
        test_generate_excel()
        
        print("=" * 60)
        print("所有测试通过！API服务准备就绪")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
