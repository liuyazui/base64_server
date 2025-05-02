# Base64编码解码MCP服务器

[English Version](README_EN.md)

一个简单高效的MCP服务器，专注于提供Base64编码和解码功能，支持文本和图片的Base64转换。

<a href="https://glama.ai/mcp/servers/@liuyazui/base64_server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@liuyazui/base64_server/badge" alt="Base64 Server MCP server" />
</a>

## 功能特点

- 文本Base64编码和解码
- 图片Base64编码和解码
- 支持Data URL格式
- 简单易用的API
- 使用uv进行依赖管理

## 安装

### 使用uv安装

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境（Linux/macOS）
source .venv/bin/activate

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 安装包（开发模式）
uv pip install -e .

# 安装带开发依赖的包
uv pip install -e ".[dev]"
```

## 使用方法

### 使用MCP Inspector测试

```bash
# 使用MCP Inspector测试服务器
uv run mcp dev base64_server.py
```

### 与MCP client集成

1. 添加服务器配置：

   ```json
   {
     "mcpServers": {
        "base64-encoder": {
        "command": "uv",
        "args": [
          "run",
          "--with",
          "mcp[cli]",
          "mcp",
          "run",
          "[path to base64_server.py]"
        ]
      }
     }
   }
   ```

## API参考

### 工具(Tools)

- **base64_encode_text(text: str) -> str**：将文本转换为Base64编码
- **base64_decode_text(encoded: str) -> str**：将Base64编码解码为文本
- **base64_encode_image(image_path: str) -> str**：将图片转换为Base64编码
- **base64_decode_image(encoded: str, output_path: str, mime_type: str = "image/png") -> str**：将Base64编码解码为图片

### 资源(Resources)

- **encode://base64/text/{text}**：获取文本的Base64编码
- **decode://base64/text/{encoded}**：获取Base64编码的解码结果
- **encode://base64/image/{image_path}**：获取图片的Base64编码
- **decode://base64/image/{encoded}**：获取Base64编码的解码图片

### 提示模板(Prompts)

- **base64_usage_guide()**: 提供Base64服务的基本使用指南
- **encode_text_prompt(text: str)**: 文本编码提示模板
- **encode_image_prompt(image_path: str)**: 图片编码提示模板
- **error_handling_prompt(error_message: str)**: 错误处理提示模板

使用示例:

```python
# 获取使用指南提示
messages = await client.get_prompt("base64_usage_guide")

# 获取文本编码提示
messages = await client.get_prompt("encode_text_prompt", {"text": "Hello World"})
```

## 开发

## 许可证

MIT