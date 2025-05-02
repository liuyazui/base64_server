# Base64 Encoding and Decoding MCP Server

A simple and efficient MCP server focused on providing Base64 encoding and decoding functionality, supporting Base64 conversion for both text and images.

## Features

- Text Base64 encoding and decoding
- Image Base64 encoding and decoding
- Support for Data URL format
- Simple and easy-to-use API
- Dependency management using uv

## Installation

### Using uv

```bash
# Create virtual environment
uv venv

# Activate virtual environment (Linux/macOS)
source .venv/bin/activate

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install package (development mode)
uv pip install -e .

# Install package with development dependencies
uv pip install -e ".[dev]"
```

## Usage

### Testing with MCP Inspector

```bash
# Test the server using MCP Inspector
uv run mcp dev base64_server.py
```

### Integration with MCP client

1. Add server configuration:

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

## API Reference

### Tools

- **base64_encode_text(text: str) -> str**: Convert text to Base64 encoding
- **base64_decode_text(encoded: str) -> str**: Decode Base64 encoding to text
- **base64_encode_image(image_path: str) -> str**: Convert image to Base64 encoding
- **base64_decode_image(encoded: str, output_path: str, mime_type: str = "image/png") -> str**: Decode Base64 encoding to image

### Resources

- **encode://base64/text/{text}**: Get Base64 encoding of text
- **decode://base64/text/{encoded}**: Get decoded result of Base64 encoding
- **encode://base64/image/{image_path}**: Get Base64 encoding of image
- **decode://base64/image/{encoded}**: Get decoded image from Base64 encoding

### Prompts

- **base64_usage_guide()**: Provides basic usage guide for Base64 service
- **encode_text_prompt(text: str)**: Text encoding prompt template
- **encode_image_prompt(image_path: str)**: Image encoding prompt template
- **error_handling_prompt(error_message: str)**: Error handling prompt template

Usage examples:

```python
# Get usage guide prompt
messages = await client.get_prompt("base64_usage_guide")

# Get text encoding prompt
messages = await client.get_prompt("encode_text_prompt", {"text": "Hello World"})
```

## Development

## License

MIT
