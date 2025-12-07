#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// 获取 Python 可执行文件路径
const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';

// MCP 服务器脚本路径
const mcpServerPath = path.join(__dirname, 'varable_try_mcp.py');

// 启动 MCP 服务器
const mcpServer = spawn(pythonCommand, [mcpServerPath], {
    stdio: 'inherit',
    env: {
        ...process.env,
        // 从环境变量中读取 API Key
        ZHIPU_API_KEY: process.env.ZHIPU_API_KEY || ''
    }
});

// 处理进程退出
mcpServer.on('close', (code) => {
    if (code !== 0) {
        console.error(`MCP server exited with code ${code}`);
        process.exit(code);
    }
});

// 处理 SIGINT (Ctrl+C)
process.on('SIGINT', () => {
    mcpServer.kill('SIGINT');
    process.exit(0);
});

// 处理 SIGTERM
process.on('SIGTERM', () => {
    mcpServer.kill('SIGTERM');
    process.exit(0);
});
