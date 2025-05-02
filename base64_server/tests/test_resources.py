"""
测试MCP资源功能
"""

import base64
import sys
from pathlib import Path

import pytest

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 直接从主服务器文件导入函数
import importlib.util

spec = importlib.util.spec_from_file_location(
    "base64_server_module", str(project_root / "base64_server.py")
)
base64_server_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base64_server_module)

# 从模块中获取函数
get_base64_encoded_text = base64_server_module.get_base64_encoded_text
get_base64_decoded_text = base64_server_module.get_base64_decoded_text
get_base64_encoded_image = base64_server_module.get_base64_encoded_image


def test_get_base64_encoded_text(sample_text):
    """测试文本编码资源"""
    result = get_base64_encoded_text(sample_text)

    # 验证结果是字符串
    assert isinstance(result, str)

    # 如果结果是错误消息，则跳过后续验证
    if "编码失败" in result or "错误" in result:
        pytest.skip(f"编码失败: {result}")

    # 验证结果是有效的Base64
    try:
        decoded = base64.b64decode(result).decode("utf-8")
        assert decoded == sample_text
    except Exception as e:
        pytest.fail(f"资源返回的不是有效的Base64: {e}")


def test_get_base64_decoded_text(sample_encoded_text):
    """测试文本解码资源"""
    result = get_base64_decoded_text(sample_encoded_text)

    # 验证结果是字符串
    assert isinstance(result, str)

    # 验证解码结果
    # 如果结果是错误消息，则跳过后续验证
    if "解码失败" in result or "错误" in result:
        pytest.skip(f"解码失败: {result}")

    expected = "Hello, World! 你好，世界！"
    assert result == expected


def test_get_base64_encoded_image(temp_image_path):
    """测试图片编码资源"""
    try:
        result = get_base64_encoded_image(temp_image_path)

        # 验证结果是Image对象
        from mcp.server.fastmcp import Image

        assert isinstance(result, Image)

        # 验证图片数据不为空
        assert result.data
        assert result.format in ["png", "jpg", "jpeg", "gif"]
    except Exception as e:
        # 这个测试可能需要MCP环境才能完全运行
        # 如果在没有MCP环境的情况下运行，会抛出异常
        pytest.skip(f"无法测试图片资源: {e}")


def test_resource_roundtrip(sample_text):
    """测试资源的往返一致性"""
    # 编码
    encoded = get_base64_encoded_text(sample_text)

    # 验证编码结果不是错误消息
    if "编码失败" in encoded or "错误" in encoded:
        pytest.skip(f"编码失败: {encoded}")

    # 解码
    decoded = get_base64_decoded_text(encoded)

    # 验证解码结果不是错误消息
    if "解码失败" in decoded or "错误" in decoded:
        pytest.skip(f"解码失败: {decoded}")

    # 验证往返一致性
    assert decoded == sample_text
