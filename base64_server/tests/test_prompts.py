"""测试提示模板功能"""

import asyncio
import os

# 导入MCP服务器实例
import sys

import pytest
from mcp.server.fastmcp.prompts import base

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from base64_server import mcp


@pytest.mark.asyncio
async def test_base64_usage_guide():
    """测试基础使用提示"""
    messages = await mcp._prompt_manager.render_prompt("base64_usage_guide")
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"
    assert "如何使用Base64编码解码服务" in messages[0].content.text
    assert "文本编码" in messages[1].content.text
    assert "图片编码" in messages[1].content.text


@pytest.mark.asyncio
async def test_encode_text_prompt():
    """测试文本编码提示"""
    messages = await mcp._prompt_manager.render_prompt(
        "encode_text_prompt", {"text": "Hello"}
    )
    assert len(messages) == 2
    assert "Hello" in messages[0].content.text
    assert "base64_encode_text工具" in messages[1].content.text


@pytest.mark.asyncio
async def test_encode_image_prompt():
    """测试图片编码提示"""
    messages = await mcp._prompt_manager.render_prompt(
        "encode_image_prompt", {"image_path": "/path/to/image.jpg"}
    )
    assert len(messages) == 2
    assert "/path/to/image.jpg" in messages[0].content.text
    assert "base64_encode_image工具" in messages[1].content.text


@pytest.mark.asyncio
async def test_error_handling_prompt():
    """测试错误处理提示"""
    messages = await mcp._prompt_manager.render_prompt(
        "error_handling_prompt", {"error_message": "File not found"}
    )
    assert len(messages) == 2
    assert "File not found" in messages[0].content.text
    assert "分析这个错误" in messages[1].content.text
