"""
测试文本Base64编码和解码功能
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
base64_encode_text = base64_server_module.base64_encode_text
base64_decode_text = base64_server_module.base64_decode_text


def test_encode_text(sample_text):
    """测试文本Base64编码功能"""
    result = base64_encode_text(sample_text)

    # 验证结果包含"Base64编码结果:"前缀
    assert "Base64编码结果:" in result

    # 提取编码结果
    encoded = result.split("Base64编码结果:")[1].strip()

    # 验证编码结果是有效的Base64
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        assert decoded == sample_text
    except Exception as e:
        pytest.fail(f"编码结果不是有效的Base64: {e}")


def test_decode_text(sample_encoded_text):
    """测试文本Base64解码功能"""
    result = base64_decode_text(sample_encoded_text)

    # 验证结果包含"Base64解码结果:"前缀
    assert "Base64解码结果:" in result

    # 提取解码结果
    decoded = result.split("Base64解码结果:")[1].strip()

    # 验证解码结果
    expected = "Hello, World! 你好，世界！"
    assert decoded == expected


def test_encode_decode_roundtrip(sample_text):
    """测试编码后解码的往返一致性"""
    # 编码
    encode_result = base64_encode_text(sample_text)

    # 验证编码结果包含预期前缀
    assert "Base64编码结果:" in encode_result

    encoded = encode_result.split("Base64编码结果:")[1].strip()

    # 解码
    decode_result = base64_decode_text(encoded)

    # 验证解码结果包含预期前缀
    assert "Base64解码结果:" in decode_result

    decoded = decode_result.split("Base64解码结果:")[1].strip()

    # 验证往返一致性
    assert decoded == sample_text


def test_decode_with_prefix():
    """测试解码带有前缀的Base64字符串"""
    encoded = "Base64编码结果: SGVsbG8sIFdvcmxkIQ=="
    result = base64_decode_text(encoded)
    decoded = result.split("Base64解码结果:")[1].strip()
    assert decoded == "Hello, World!"


def test_decode_with_whitespace():
    """测试解码带有空白的Base64字符串"""
    encoded = "  SGVsbG8sIFdvcmxkIQ==  "
    result = base64_decode_text(encoded)
    decoded = result.split("Base64解码结果:")[1].strip()
    assert decoded == "Hello, World!"


def test_encode_empty_string():
    """测试编码空字符串"""
    result = base64_encode_text("")
    encoded = result.split("Base64编码结果:")[1].strip()
    assert encoded == ""


def test_decode_invalid_base64():
    """测试解码无效的Base64字符串"""
    result = base64_decode_text("这不是有效的Base64!")
    assert "错误: 输入包含非Base64字符" in result
