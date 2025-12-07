# 文生图 MCP 服务器

[![npm version](https://badge.fury.io/js/mcp-zhipu-text-to-image-kuma.svg)](https://www.npmjs.com/package/mcp-zhipu-text-to-image-kuma)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于 FastMCP 框架实现的文本生成图片 MCP 服务器，集成智谱 API (CogView-4)。

## 特性

- ✅ 基于 MCP (Model Context Protocol) 标准协议
- ✅ 集成智谱 CogView-4 图片生成 API
- ✅ 支持 stdio 传输模式（标准 MCP 模式）
- ✅ 完整的日志记录和错误处理
- ✅ 支持 Claude Desktop、Cline 等 MCP 客户端
- ✅ 可通过 NPM 安装和使用

## 快速开始

### 方式一：通过 NPM 安装（推荐）

```bash
npm install -g mcp-zhipu-text-to-image-kuma
```

### 方式二：从源码安装

```bash
git clone https://github.com/2716025420/mcp-zhipu-text-to-image-kuma.git
cd mcp-zhipu-text-to-image-kuma
pip install -r requirements.txt
```

## 环境要求

- Python 3.8 或更高版本
- 智谱 API Key（从 [智谱 AI 开放平台](https://open.bigmodel.cn/) 获取）

## 配置

### 1. 获取 API Key

访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)，注册并获取 API Key。

### 2. 配置环境变量

创建 `.env` 文件（或设置系统环境变量）：

```env
ZHIPU_API_KEY=your_actual_api_key_here
```

## 使用方法

### 在 Claude Desktop 中使用

编辑 Claude Desktop 配置文件：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

添加以下配置：

```json
{
  "mcpServers": {
    "mcp-zhipu-text-to-image-kuma": {
      "command": "python",
      "args": ["F:\\mcp3\\varable_try_mcp.py"],
      "env": {
        "ZHIPU_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

如果通过 NPM 安装，可以使用：

```json
{
  "mcpServers": {
    "mcp-zhipu-text-to-image-kuma": {
      "command": "npx",
      "args": ["-y", "mcp-zhipu-text-to-image-kuma"],
      "env": {
        "ZHIPU_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

重启 Claude Desktop，即可在对话中使用文生图功能。

### 在 Cline (VS Code) 中使用

打开 Cline 设置，添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "mcp-zhipu-text-to-image-kuma": {
      "command": "python",
      "args": ["F:\\mcp3\\varable_try_mcp.py"],
      "env": {
        "ZHIPU_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 直接运行

```bash
# 从源码运行
python varable_try_mcp.py

# 或通过 NPM 运行
npm start
```

## 工具说明

### generate_image

根据提示词生成图片。

**参数**:
- `prompt` (必需): 图片描述提示词，例如 "小猫在玩耍"
- `size` (可选): 图片尺寸，默认 "1024x1024"
- `quality` (可选): 图片质量，默认 "standard"

**返回示例**:
```json
{
  "input_prompt": "小猫在玩耍",
  "output_urls": [
    "https://open.bigmodel.cn/image-output/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.png"
  ],
  "created": 1735689600,
  "content_filter": [
    {
      "role": "assistant",
      "level": 1
    }
  ]
}
```

**错误示例**:
```json
{
  "error": "API 错误: 无效的Authorization Token，请检查token是否正确或已过期",
  "error_code": "INVALID_AUTH_TOKEN",
  "input_prompt": "小猫在玩耍"
}
```

## 使用示例

在 Claude Desktop 中：

```
用户: 请使用文生图工具生成一张小猫在玩耍的图片

Claude: 好的，我来为您生成图片...
[调用 generate_image 工具]

生成成功！图片链接：
https://open.bigmodel.cn/image-output/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.png
```

## 项目结构

```
mcp3/
├── varable_try_mcp.py    # MCP 服务器主程序
├── requirements.txt       # Python 依赖
├── package.json           # NPM 配置
├── run.js                 # NPM 启动脚本
├── .env                   # 环境变量配置 (API Key)
├── .gitignore             # Git 忽略文件
├── LICENSE                # MIT 许可证
└── README.md              # 项目说明文档
```

## API 配置

- **模型**: cogView-4-250304
- **API 端点**: https://open.bigmodel.cn/api/paas/v4/images/generations
- **超时时间**: 60 秒

## 日志输出

服务器运行时会输出详细的日志信息：
- 服务启动信息
- API 调用请求
- API 响应状态
- 错误信息

## 发布到 NPM

### 准备工作

1. 注册 NPM 账号：https://www.npmjs.com/signup
2. 登录 NPM：
   ```bash
   npm login
   ```

### 发布步骤

1. 更新 `package.json` 中的信息（名称、作者、仓库等）
2. 确保所有文件都已提交到 Git
3. 发布到 NPM：
   ```bash
   npm publish
   ```

### 更新版本

```bash
# 补丁版本（bug 修复）
npm version patch

# 次要版本（新功能）
npm version minor

# 主要版本（破坏性更改）
npm version major

# 发布新版本
npm publish
```

## 故障排查

### Claude Desktop 无法连接

1. 检查配置文件路径是否正确
2. 确保 Python 路径正确（使用绝对路径）
3. 查看日志文件：
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`
   - Mac: `~/Library/Logs/Claude/mcp*.log`

### API Key 无效

1. 检查 `.env` 文件格式（无引号，无空格）
2. 验证 API Key 是否过期
3. 确认 API Key 有图片生成权限

### 请求超时

1. 检查网络连接
2. 验证智谱 API 服务状态
3. 增加超时时间（修改代码中的 timeout 参数）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 相关链接

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [FastMCP 文档](https://gofastmcp.com/)
- [智谱 AI 开放平台](https://open.bigmodel.cn/)
- [Claude Desktop](https://claude.ai/download)

## 更新日志

### v1.0.0 (2025-12-08)

- 🎉 首次发布
- ✅ 支持文本生成图片功能
- ✅ 集成智谱 CogView-4 API
- ✅ 支持 stdio 传输模式
- ✅ 完整的日志和错误处理

---

**作者**: Your Name  
**最后更新**: 2025-12-08
