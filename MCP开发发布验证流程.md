# MCP 开发-发布-验证完整流程

本文档详细介绍如何开发、发布和验证一个 MCP (Model Context Protocol) 服务器。

---

## 目录

1. [MCP 简介](#1-mcp-简介)
2. [开发阶段](#2-开发阶段)
3. [本地测试](#3-本地测试)
4. [发布部署](#4-发布部署)
5. [客户端验证](#5-客户端验证)
6. [常见问题](#6-常见问题)

---

## 1. MCP 简介

### 1.1 什么是 MCP？

MCP (Model Context Protocol) 是一个开放协议，用于在 AI 应用和外部数据源/工具之间建立标准化的连接。

### 1.2 MCP 架构

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Client    │ ◄─────► │ MCP Server  │ ◄─────► │  External   │
│  (Claude,   │   MCP   │  (FastMCP)  │   API   │   Service   │
│   etc.)     │ Protocol│             │         │ (智谱 API)   │
└─────────────┘         └─────────────┘         └─────────────┘
```

### 1.3 传输方式

MCP 支持多种传输方式：
- **SSE (Server-Sent Events)**: HTTP 流式传输，适合 Web 应用
- **stdio**: 标准输入/输出，适合本地进程通信
- **WebSocket**: 双向通信，适合实时应用

---

## 2. 开发阶段

### 2.1 环境准备

#### 2.1.1 检查 Python 版本

```bash
python --version
# 需要 Python 3.8+
```

#### 2.1.2 创建项目目录

```bash
mkdir my-mcp-server
cd my-mcp-server
```

#### 2.1.3 创建虚拟环境（推荐）

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 2.2 安装依赖

#### 2.2.1 创建 requirements.txt

```txt
fastmcp
httpx
python-dotenv
```

#### 2.2.2 安装依赖包

```bash
pip install -r requirements.txt
```

### 2.3 编写 MCP 服务器

#### 2.3.1 基本结构

```python
from fastmcp import FastMCP
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 MCP 实例
mcp = FastMCP("我的MCP服务")

# 定义工具
@mcp.tool()
async def my_tool(param: str) -> dict:
    """工具描述"""
    logger.info(f"收到请求: {param}")
    return {"result": "success"}

# 运行服务器
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8008, path="/mcp")
```

#### 2.3.2 配置环境变量

创建 `.env` 文件：

```env
API_KEY=your_api_key_here
DEBUG=true
```

在代码中加载：

```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
```

### 2.4 添加日志

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.info("服务器启动")
logger.debug("调试信息")
logger.error("错误信息")
```

---

## 3. 本地测试

### 3.1 启动 MCP 服务器

```bash
python varable_try_mcp.py
```

预期输出：

```
2025-12-08 01:25:00 - __main__ - INFO - 启动文生图 MCP 服务器...
2025-12-08 01:25:00 - __main__ - INFO - 服务地址: http://0.0.0.0:8008
INFO:     Uvicorn running on http://0.0.0.0:8008 (Press CTRL+C to quit)
```

### 3.2 测试方法

#### 3.2.1 方法一：使用 Python 脚本测试

创建 `test_mcp.py`:

```python
import asyncio
import httpx
import json

async def test_mcp():
    url = "http://localhost:8008/mcp"
    
    # MCP 请求格式
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "generate_image",
            "arguments": {
                "prompt": "小猫在玩耍"
            }
        }
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, json=request)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

asyncio.run(test_mcp())
```

运行测试：

```bash
python test_mcp.py
```

#### 3.2.2 方法二：使用 curl 测试

```bash
curl -X POST http://localhost:8008/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "generate_image",
      "arguments": {
        "prompt": "小猫在玩耍"
      }
    }
  }'
```

#### 3.2.3 方法三：使用 MCP Inspector

MCP Inspector 是官方提供的调试工具：

```bash
# 安装 MCP Inspector
npm install -g @modelcontextprotocol/inspector

# 启动 Inspector
mcp-inspector
```

然后在浏览器中访问 `http://localhost:5173`，配置连接到你的 MCP 服务器。

### 3.3 验证工具列表

获取服务器提供的所有工具：

```bash
curl -X POST http://localhost:8008/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'
```

预期响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "generate_image",
        "description": "根据提示词生成图片",
        "inputSchema": {
          "type": "object",
          "properties": {
            "prompt": {
              "type": "string",
              "description": "图片描述提示词"
            }
          }
        }
      }
    ]
  }
}
```

---

## 4. 发布部署

### 4.1 本地发布（stdio 模式）

#### 4.1.1 修改传输方式

```python
if __name__ == "__main__":
    # stdio 模式用于本地客户端
    mcp.run(transport="stdio")
```

#### 4.1.2 创建配置文件

对于 Claude Desktop 等客户端，创建配置文件：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "文生图服务": {
      "command": "python",
      "args": ["F:\\mcp3\\varable_try_mcp.py"],
      "env": {
        "ARK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 4.2 远程部署（SSE 模式）

#### 4.2.1 使用 Docker 部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY varable_try_mcp.py .
COPY .env .

EXPOSE 8008

CMD ["python", "varable_try_mcp.py"]
```

构建和运行：

```bash
# 构建镜像
docker build -t my-mcp-server .

# 运行容器
docker run -p 8008:8008 --env-file .env my-mcp-server
```

#### 4.2.2 使用云服务部署

**Railway / Render / Fly.io 等平台**:

1. 创建 `Procfile`:
```
web: python varable_try_mcp.py
```

2. 设置环境变量在平台控制台

3. 推送代码到 Git 仓库

4. 连接仓库并部署

#### 4.2.3 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /mcp {
        proxy_pass http://localhost:8008/mcp;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4.3 发布到 NPM（可选）

如果要让其他人更容易使用你的 MCP 服务器：

#### 4.3.1 创建 package.json

```json
{
  "name": "mcp-text-to-image",
  "version": "1.0.0",
  "description": "MCP server for text-to-image generation",
  "main": "varable_try_mcp.py",
  "bin": {
    "mcp-text-to-image": "varable_try_mcp.py"
  },
  "keywords": ["mcp", "text-to-image", "ai"],
  "author": "Your Name",
  "license": "MIT"
}
```

#### 4.3.2 发布

```bash
npm publish
```

---

## 5. 客户端验证

### 5.1 Claude Desktop 集成

#### 5.1.1 配置 Claude Desktop

编辑配置文件（位置见 4.1.2）：

**stdio 模式（本地）**:

```json
{
  "mcpServers": {
    "文生图服务": {
      "command": "python",
      "args": ["F:\\mcp3\\varable_try_mcp.py"],
      "env": {
        "ARK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**SSE 模式（远程）**:

```json
{
  "mcpServers": {
    "文生图服务": {
      "url": "http://your-server.com:8008/mcp",
      "transport": "sse"
    }
  }
}
```

#### 5.1.2 重启 Claude Desktop

完全退出并重新启动 Claude Desktop 应用。

#### 5.1.3 验证连接

在 Claude Desktop 中：

1. 查看是否出现工具图标（🔧）
2. 尝试使用命令："请使用文生图工具生成一张小猫在玩耍的图片"
3. 检查是否能看到工具调用和返回结果

#### 5.1.4 查看日志

**Windows**:
```
%APPDATA%\Claude\logs\mcp*.log
```

**Mac**:
```
~/Library/Logs/Claude/mcp*.log
```

### 5.2 使用 MCP Client SDK

#### 5.2.1 Python Client

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_mcp_server():
    server_params = StdioServerParameters(
        command="python",
        args=["varable_try_mcp.py"],
        env={"ARK_API_KEY": "your_key"}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 列出工具
            tools = await session.list_tools()
            print(f"可用工具: {tools}")
            
            # 调用工具
            result = await session.call_tool(
                "generate_image",
                arguments={"prompt": "小猫在玩耍"}
            )
            print(f"结果: {result}")
```

#### 5.2.2 TypeScript/JavaScript Client

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "python",
  args: ["varable_try_mcp.py"],
  env: { ARK_API_KEY: "your_key" }
});

const client = new Client({
  name: "test-client",
  version: "1.0.0"
}, {
  capabilities: {}
});

await client.connect(transport);

// 列出工具
const tools = await client.listTools();
console.log("可用工具:", tools);

// 调用工具
const result = await client.callTool({
  name: "generate_image",
  arguments: { prompt: "小猫在玩耍" }
});
console.log("结果:", result);
```

### 5.3 使用 Cline (VS Code 扩展)

#### 5.3.1 安装 Cline

在 VS Code 中搜索并安装 "Cline" 扩展。

#### 5.3.2 配置 MCP 服务器

打开 Cline 设置，添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "文生图服务": {
      "command": "python",
      "args": ["F:\\mcp3\\varable_try_mcp.py"],
      "env": {
        "ARK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### 5.3.3 使用工具

在 Cline 聊天中请求使用工具：
```
请使用文生图工具生成一张夕阳下的海滩图片
```

### 5.4 使用 Continue (VS Code/JetBrains)

#### 5.4.1 配置 Continue

编辑 `~/.continue/config.json`:

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "python",
          "args": ["F:\\mcp3\\varable_try_mcp.py"],
          "env": {
            "ARK_API_KEY": "your_api_key_here"
          }
        }
      }
    ]
  }
}
```

### 5.5 使用自定义客户端

#### 5.5.1 HTTP 客户端示例

```python
import requests
import json

def call_mcp_tool(url, tool_name, arguments):
    """调用 MCP 工具"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    return response.json()

# 使用示例
result = call_mcp_tool(
    "http://localhost:8008/mcp",
    "generate_image",
    {"prompt": "小猫在玩耍"}
)

print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## 6. 常见问题

### 6.1 连接问题

#### Q: Claude Desktop 无法连接到 MCP 服务器

**A**: 检查以下几点：

1. **配置文件路径是否正确**
   ```bash
   # Windows
   echo %APPDATA%\Claude\claude_desktop_config.json
   
   # Mac
   echo ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Python 路径是否正确**
   ```json
   {
     "command": "python",  // 或 "python3" 或完整路径
     "args": ["F:\\mcp3\\varable_try_mcp.py"]  // 使用绝对路径
   }
   ```

3. **查看日志文件**
   ```bash
   # Windows
   type %APPDATA%\Claude\logs\mcp-server-文生图服务.log
   
   # Mac
   cat ~/Library/Logs/Claude/mcp-server-文生图服务.log
   ```

4. **手动测试服务器**
   ```bash
   python varable_try_mcp.py
   # 确保没有错误输出
   ```

#### Q: SSE 连接超时

**A**: 
1. 检查防火墙设置
2. 确保端口 8008 未被占用
3. 增加超时时间配置

### 6.2 工具调用问题

#### Q: 工具列表为空

**A**: 
1. 确保使用 `@mcp.tool()` 装饰器
2. 检查工具函数是否为 async 函数
3. 验证服务器是否正确启动

#### Q: 工具调用返回错误

**A**: 
1. 检查参数类型是否匹配
2. 查看服务器日志输出
3. 验证 API Key 是否正确配置

### 6.3 环境变量问题

#### Q: .env 文件未加载

**A**: 
1. 确保安装了 `python-dotenv`
2. 检查 `.env` 文件位置（应与脚本同目录）
3. 使用 `load_dotenv()` 显式加载

#### Q: API Key 无效

**A**: 
1. 检查 `.env` 文件格式（无引号，无空格）
   ```env
   ARK_API_KEY=your_actual_key_here
   ```
2. 验证 API Key 是否过期
3. 测试 API Key 是否有效：
   ```bash
   curl -H "Authorization: Bearer YOUR_KEY" \
     https://open.bigmodel.cn/api/paas/v4/models
   ```

### 6.4 性能问题

#### Q: 请求超时

**A**: 
1. 增加超时时间
   ```python
   async with httpx.AsyncClient(timeout=120.0) as client:
   ```
2. 检查网络连接
3. 验证外部 API 响应时间

#### Q: 并发请求失败

**A**: 
1. 使用连接池
2. 添加请求限流
3. 增加服务器资源

### 6.5 调试技巧

#### 启用详细日志

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### 使用 MCP Inspector

```bash
npm install -g @modelcontextprotocol/inspector
mcp-inspector
```

#### 监控网络请求

```bash
# 使用 tcpdump 或 Wireshark 监控
tcpdump -i any -A port 8008
```

---

## 7. 最佳实践

### 7.1 安全性

1. **不要在代码中硬编码密钥**
   ```python
   # ❌ 错误
   API_KEY = "sk-xxxxx"
   
   # ✅ 正确
   API_KEY = os.getenv("ARK_API_KEY")
   ```

2. **使用 HTTPS**
   ```python
   # 生产环境使用 HTTPS
   mcp.run(transport="sse", host="0.0.0.0", port=443, ssl=True)
   ```

3. **添加认证**
   ```python
   from fastapi import Header, HTTPException
   
   async def verify_token(authorization: str = Header(None)):
       if authorization != f"Bearer {SECRET_TOKEN}":
           raise HTTPException(status_code=401)
   ```

### 7.2 错误处理

```python
@mcp.tool()
async def robust_tool(param: str) -> dict:
    try:
        # 业务逻辑
        result = await some_operation(param)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"参数错误: {e}")
        return {"success": False, "error": "参数无效"}
    except Exception as e:
        logger.error(f"未知错误: {e}", exc_info=True)
        return {"success": False, "error": "服务器内部错误"}
```

### 7.3 性能优化

1. **使用连接池**
   ```python
   client = httpx.AsyncClient(timeout=60.0)
   
   @mcp.tool()
   async def optimized_tool(param: str):
       response = await client.post(url, json=data)
       return response.json()
   ```

2. **添加缓存**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_cached_data(key: str):
       return expensive_operation(key)
   ```

3. **异步处理**
   ```python
   import asyncio
   
   async def batch_process(items):
       tasks = [process_item(item) for item in items]
       return await asyncio.gather(*tasks)
   ```

### 7.4 文档化

```python
@mcp.tool()
async def well_documented_tool(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard"
) -> dict:
    """
    根据提示词生成图片
    
    Args:
        prompt: 图片描述提示词，例如"小猫在玩耍"
        size: 图片尺寸，支持 "1024x1024", "512x512" 等
        quality: 图片质量，"standard" 或 "hd"
    
    Returns:
        包含以下字段的字典:
        - input_prompt: 输入的提示词
        - output_urls: 生成的图片 URL 列表
        - created: 创建时间戳
    
    Raises:
        ValueError: 当参数无效时
        APIError: 当 API 调用失败时
    
    Example:
        >>> await generate_image("小猫在玩耍")
        {
            "input_prompt": "小猫在玩耍",
            "output_urls": ["https://..."],
            "created": 1735689600
        }
    """
    # 实现代码
```

---

## 8. 资源链接

### 官方文档
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [FastMCP 文档](https://gofastmcp.com/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

### 工具和 SDK
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

### 示例项目
- [MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

### 社区
- [MCP Discord](https://discord.gg/mcp)
- [GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions)

---

## 9. 总结

本文档涵盖了 MCP 服务器从开发到验证的完整流程：

1. ✅ **开发**: 使用 FastMCP 框架快速开发
2. ✅ **测试**: 多种测试方法确保功能正常
3. ✅ **部署**: 本地和远程部署方案
4. ✅ **验证**: 多个客户端集成验证
5. ✅ **调试**: 常见问题解决方案

通过遵循本流程，您可以快速开发、部署和验证自己的 MCP 服务器。

---

**最后更新**: 2025-12-08
**版本**: 1.0.0
