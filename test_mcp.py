"""
测试脚本 - 验证文生图 MCP 服务器功能
"""
import asyncio
import httpx
import json

# MCP 服务器地址
MCP_SERVER_URL = "http://localhost:8008/mcp"

async def test_mcp_server():
    """测试 MCP 服务器的 generate_image 工具"""
    
    print("=" * 60)
    print("测试文生图 MCP 服务器")
    print("=" * 60)
    
    # 测试用例
    test_cases = [
        {
            "prompt": "小猫在玩耍",
            "description": "基础测试 - 小猫在玩耍"
        },
        {
            "prompt": "夕阳下的海滩",
            "description": "测试 - 夕阳下的海滩"
        }
    ]
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n测试用例 {i}: {test_case['description']}")
            print(f"提示词: {test_case['prompt']}")
            print("-" * 60)
            
            # 构建 MCP 请求
            mcp_request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": "tools/call",
                "params": {
                    "name": "generate_image",
                    "arguments": {
                        "prompt": test_case["prompt"]
                    }
                }
            }
            
            try:
                print("正在发送请求...")
                response = await client.post(
                    MCP_SERVER_URL,
                    json=mcp_request,
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print("响应内容:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(f"请求失败: {response.text}")
                    
            except Exception as e:
                print(f"发生错误: {str(e)}")
            
            print("-" * 60)
            
            # 只测试第一个用例,避免消耗过多 API 配额
            if i == 1:
                print("\n提示: 为节省 API 配额,仅执行第一个测试用例")
                break
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    print("注意: 请确保 MCP 服务器正在运行 (python varable_try_mcp.py)")
    print("注意: 请确保 .env 文件中已配置有效的 ZHIPU_API_KEY\n")
    
    asyncio.run(test_mcp_server())
