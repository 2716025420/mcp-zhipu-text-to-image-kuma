我想通过fastmcp框架编写一个实现mcp server的脚手架工程。
1. 运行环境需要使用python 3.8版本以上，请你先检查环境是否满足，如果不满足请帮我创建。​
2. 请你参考这个项目https://github.com/jlowin/fastmcp，请你帮我实现。代码文件保存到mcpdemo.py中，host使用0.0.0.0，端口使用8008。
3. 使用fastmcp框架，生成一个根据输入图片和提示词生成一个新的创意图片的 MCP 服务，使用/mcp路由形式，用户只需要上传参考的url链接（input_url），根据提示词的描述，生成用户想要的效果。需要输出是参考图片的url链接（input_url），API请求后得到的所有图片的url链接（output_url）。
---输入示例---​
用户输入的提示词：小猫在玩耍
---示例结束---
---输出示例---​
输入提示词：×××××××××××​
输出图片链接：[output_url1,output_url2,......]
---示例结束---
4. 程序写入到varable_try_mcp.py文件，host使用0.0.0.0，端口号使用8008。​
5. 生成依赖requirments.txt​
6. 通过命令pip install -r requirments.txt，安装环境依赖。​
7. 下面是API请求的格式。
---curl请求示例---​
curl --request POST \
  --url https://open.bigmodel.cn/api/paas/v4/images/generations \
  --header 'Authorization: Bearer <你的智谱API_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "cogView-4-250304",
  "prompt": "小猫在玩耍",
  "size": "1024x1024",
  "quality": "standard"
}'
---示例结束---
---成功响应示例---​
{
  "created": 1735689600,
  "data": [
    {
      "url": "https://open.bigmodel.cn/image-output/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.png"
    }
  ],
  "content_filter": [
    {
      "role": "assistant",
      "level": 1
    }
  ]
}
---示例结束---
---错误响应示例---​
{
  "error": {
    "code": "INVALID_AUTH_TOKEN",
    "message": "无效的Authorization Token，请检查token是否正确或已过期"
  }
}
---示例结束---
8. 生成.env文件，将ARK_API_KEY写到.env文件中，当前的ARK_API_KEY是××××××××××××××××，要能支持多种api_key格式，不仅仅是以sk开关的api_key。后面API请求从这里获取，方便维护。
9. 在MCP被调用时，增加后台日志输出，以方便调试。
10. 项目创建后，你要进行测试，实时监控终端的输出信息，根据终端提供的信息不断进行优化和调整，完全测试好后，能够正常运行后再交付给我。