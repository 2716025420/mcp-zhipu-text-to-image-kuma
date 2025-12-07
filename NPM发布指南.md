# NPM 发布完整指南

本文档详细说明如何将 MCP 服务器发布到 NPM。

## 前置准备

### 1. 注册 NPM 账号

访问 https://www.npmjs.com/signup 注册账号。

### 2. 验证邮箱

NPM 要求验证邮箱才能发布包。

### 3. 安装 Node.js

确保已安装 Node.js 16.0.0 或更高版本：

```bash
node --version
npm --version
```

## 发布前检查清单

### ✅ 1. 更新 package.json

编辑 `package.json`，更新以下信息：

```json
{
  "name": "mcp-zhipu-text-to-image",  // 确保名称唯一
  "version": "1.0.0",
  "description": "MCP server for text-to-image generation using Zhipu AI CogView-4 API",
  "author": "Your Name <your.email@example.com>",  // 更新作者信息
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/mcp-zhipu-text-to-image.git"  // 更新仓库地址
  }
}
```

### ✅ 2. 检查包名是否可用

```bash
npm search mcp-zhipu-text-to-image
```

如果已存在，需要更换包名。

### ✅ 3. 确保所有必要文件存在

```
✓ varable_try_mcp.py
✓ requirements.txt
✓ package.json
✓ run.js
✓ README.md
✓ LICENSE
✓ .gitignore
```

### ✅ 4. 测试本地安装

```bash
# 在项目目录外测试
cd ..
npm install -g ./mcp3

# 测试运行
mcp-zhipu-text-to-image --help
```

### ✅ 5. 创建 Git 仓库（推荐）

```bash
git init
git add .
git commit -m "Initial commit"

# 创建 GitHub 仓库后
git remote add origin https://github.com/yourusername/mcp-zhipu-text-to-image.git
git push -u origin main
```

## 发布步骤

### 步骤 1: 登录 NPM

```bash
npm login
```

输入：
- Username（用户名）
- Password（密码）
- Email（邮箱）
- One-time password（如果启用了 2FA）

### 步骤 2: 检查发布内容

```bash
npm pack --dry-run
```

这会显示将要发布的文件列表，确认无误。

### 步骤 3: 发布到 NPM

```bash
npm publish
```

如果是第一次发布，可能需要添加 `--access public`：

```bash
npm publish --access public
```

### 步骤 4: 验证发布

访问 https://www.npmjs.com/package/mcp-zhipu-text-to-image 查看包页面。

### 步骤 5: 测试安装

```bash
# 全局安装
npm install -g mcp-zhipu-text-to-image

# 测试运行
mcp-zhipu-text-to-image
```

## 更新版本

### 版本号规则（语义化版本）

格式：`主版本号.次版本号.修订号` (例如: 1.2.3)

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

### 更新命令

```bash
# 修订号 +1 (1.0.0 -> 1.0.1)
npm version patch

# 次版本号 +1 (1.0.0 -> 1.1.0)
npm version minor

# 主版本号 +1 (1.0.0 -> 2.0.0)
npm version major
```

### 发布新版本

```bash
# 1. 更新版本号
npm version patch

# 2. 推送到 Git（如果有）
git push && git push --tags

# 3. 发布到 NPM
npm publish
```

## 发布后配置

### 1. 添加 NPM 徽章到 README

```markdown
[![npm version](https://badge.fury.io/js/mcp-zhipu-text-to-image.svg)](https://www.npmjs.com/package/mcp-zhipu-text-to-image)
[![npm downloads](https://img.shields.io/npm/dm/mcp-zhipu-text-to-image.svg)](https://www.npmjs.com/package/mcp-zhipu-text-to-image)
```

### 2. 更新 GitHub 仓库描述

在 GitHub 仓库设置中：
- 添加描述
- 添加主题标签：`mcp`, `text-to-image`, `zhipu`, `ai`
- 添加网站链接：NPM 包页面

### 3. 创建 GitHub Release

```bash
# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

在 GitHub 上创建 Release，关联标签。

## 常见问题

### Q: 包名已被占用

**A**: 更改 `package.json` 中的 `name` 字段，例如：
- `mcp-zhipu-image-gen`
- `@yourusername/mcp-zhipu-text-to-image` (使用作用域)

### Q: 发布失败：需要验证邮箱

**A**: 
1. 登录 NPM 网站
2. 查看邮箱中的验证邮件
3. 点击验证链接

### Q: 发布失败：403 Forbidden

**A**: 
1. 确认已登录：`npm whoami`
2. 检查包名是否已存在
3. 如果是私有包，添加 `--access public`

### Q: 如何撤销已发布的版本？

**A**: 
```bash
# 撤销特定版本（发布后 72 小时内）
npm unpublish mcp-zhipu-text-to-image@1.0.0

# 撤销整个包（谨慎使用）
npm unpublish mcp-zhipu-text-to-image --force
```

**注意**：撤销后的版本号不能再次使用。

### Q: 如何废弃某个版本？

**A**: 
```bash
npm deprecate mcp-zhipu-text-to-image@1.0.0 "此版本存在严重bug，请升级到 1.0.1"
```

## 最佳实践

### 1. 使用 .npmignore

创建 `.npmignore` 文件，排除不需要发布的文件：

```
# 测试文件
test/
*.test.js

# 开发配置
.vscode/
.idea/

# 环境变量
.env
.env.local

# 文档草稿
docs/drafts/
```

### 2. 添加 prepublish 脚本

在 `package.json` 中：

```json
{
  "scripts": {
    "prepublishOnly": "npm test",
    "test": "python -m pytest"
  }
}
```

### 3. 使用语义化版本

严格遵循语义化版本规范，让用户清楚了解更新内容。

### 4. 维护 CHANGELOG

创建 `CHANGELOG.md` 记录每个版本的变更：

```markdown
# Changelog

## [1.0.1] - 2025-12-08
### Fixed
- 修复 API 超时问题

## [1.0.0] - 2025-12-08
### Added
- 初始版本发布
- 支持文本生成图片功能
```

### 5. 添加关键词

在 `package.json` 中添加相关关键词，提高可发现性：

```json
{
  "keywords": [
    "mcp",
    "model-context-protocol",
    "text-to-image",
    "image-generation",
    "zhipu",
    "cogview",
    "ai",
    "claude",
    "fastmcp"
  ]
}
```

## 发布检查清单

发布前确认：

- [ ] 代码已测试通过
- [ ] README 文档完整
- [ ] package.json 信息正确
- [ ] LICENSE 文件存在
- [ ] .gitignore 配置正确
- [ ] 版本号符合语义化规范
- [ ] Git 提交已推送
- [ ] 本地测试安装成功
- [ ] NPM 账号已登录

## 推广建议

### 1. 提交到 Awesome 列表

- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

### 2. 社交媒体分享

- Twitter/X
- Reddit (r/MachineLearning, r/artificial)
- Hacker News

### 3. 撰写博客文章

介绍项目的开发过程和使用方法。

### 4. 制作演示视频

展示如何在 Claude Desktop 中使用。

## 维护建议

### 定期更新

- 修复 bug
- 更新依赖
- 添加新功能
- 改进文档

### 响应用户反馈

- 及时回复 GitHub Issues
- 考虑用户的功能请求
- 修复报告的 bug

### 监控下载量

使用 NPM 统计查看包的使用情况：
- https://www.npmjs.com/package/mcp-zhipu-text-to-image

---

**祝发布顺利！** 🎉

如有问题，欢迎提交 Issue 或联系作者。
