"""
文生图 MCP Server - 基于智谱 API 的文本生成图片服务
使用 fastmcp 框架实现 MCP 协议
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP
import httpx

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 创建 FastMCP 实例
mcp = FastMCP("文生图服务", dependencies=["httpx", "python-dotenv"])

# 智谱 API 配置
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/images/generations"
API_KEY = os.getenv("ARK_API_KEY")

if not API_KEY:
    logger.warning("警告: ARK_API_KEY 未在 .env 文件中设置")


@mcp.tool()
async def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard") -> dict:
    """
    根据提示词生成图片
    
    Args:
        prompt: 图片描述提示词,例如"小猫在玩耍"
        size: 图片尺寸,默认 "1024x1024"
        quality: 图片质量,默认 "standard"
    
    Returns:
        包含输入提示词和输出图片链接的字典
    """
    logger.info(f"收到图片生成请求 - 提示词: {prompt}, 尺寸: {size}, 质量: {quality}")
    
    if not API_KEY:
        error_msg = "错误: ARK_API_KEY 未配置,请在 .env 文件中设置"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "input_prompt": prompt
        }
    
    # 构建请求数据
    request_data = {
        "model": "cogView-4-250304",
        "prompt": prompt,
        "size": size,
        "quality": quality
    }
    
    # 构建请求头
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"正在调用智谱 API...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                ZHIPU_API_URL,
                json=request_data,
                headers=headers
            )
            
            logger.info(f"API 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"图片生成成功")
                
                # 提取图片 URL
                output_urls = [item["url"] for item in result.get("data", [])]
                
                return {
                    "input_prompt": prompt,
                    "output_urls": output_urls,
                    "created": result.get("created"),
                    "content_filter": result.get("content_filter", [])
                }
            else:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "未知错误")
                error_code = error_data.get("error", {}).get("code", "UNKNOWN")
                
                logger.error(f"API 调用失败 - 错误码: {error_code}, 错误信息: {error_msg}")
                
                return {
                    "error": f"API 错误: {error_msg}",
                    "error_code": error_code,
                    "input_prompt": prompt
                }
                
    except httpx.TimeoutException:
        error_msg = "请求超时,请稍后重试"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "input_prompt": prompt
        }
    except Exception as e:
        error_msg = f"发生异常: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "error": error_msg,
            "input_prompt": prompt
        }


if __name__ == "__main__":
    logger.info("启动文生图 MCP 服务器...")
    logger.info(f"API Key 已配置: {'是' if API_KEY else '否'}")
    
    # 使用 stdio 模式运行服务器（标准 MCP 模式）
    mcp.run(transport="stdio")
