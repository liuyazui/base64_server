"""
测试图片Base64编码和解码功能
"""

import base64
import os
import sys
from pathlib import Path

import pytest
from PIL import Image

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
base64_encode_image = base64_server_module.base64_encode_image
base64_decode_image = base64_server_module.base64_decode_image


def test_encode_image(temp_image_path):
    """测试图片Base64编码功能"""
    result = base64_encode_image(temp_image_path)

    # 验证结果包含预期的前缀
    assert "图片Base64编码结果" in result
    assert "完整Data URL" in result

    # 验证结果包含"data:image/"，表示是有效的Data URL
    assert "data:image/" in result


def test_encode_nonexistent_image():
    """测试编码不存在的图片文件"""
    result = base64_encode_image("nonexistent_image.png")
    assert "错误: 文件" in result
    assert "不存在" in result


def test_decode_image(temp_image_path, temp_output_dir):
    """测试图片Base64解码功能"""
    # 首先编码图片
    encode_result = base64_encode_image(temp_image_path)

    # 验证结果包含Data URL
    assert "完整Data URL" in encode_result

    # 读取原始图片内容并编码
    with open(temp_image_path, "rb") as f:
        image_data = f.read()
    encoded = base64.b64encode(image_data).decode("utf-8")

    # 构造完整的Data URL
    mime_type = "image/png"  # 测试图片是PNG格式
    data_url = f"data:{mime_type};base64,{encoded}"

    # 设置输出路径
    output_path = os.path.join(temp_output_dir, "decoded_image.png")

    # 解码图片
    result = base64_decode_image(data_url, output_path)

    # 验证结果
    assert "图片已成功解码并保存到" in result
    assert output_path in result

    # 验证输出文件存在
    assert os.path.exists(output_path)

    # 验证输出图片可以被打开
    try:
        Image.open(output_path)
    except Exception as e:
        pytest.fail(f"无法打开解码后的图片: {e}")


def test_decode_invalid_base64_image(temp_output_dir):
    """测试解码无效的Base64图片数据"""
    output_path = os.path.join(temp_output_dir, "invalid_image.png")
    result = base64_decode_image("这不是有效的Base64!", output_path)
    # 检查是否包含错误信息，可能是"图片解码失败"或其他错误消息
    assert any(msg in result for msg in ["图片解码失败", "错误", "失败", "无效"])


def test_decode_with_output_dir_creation(temp_output_dir):
    """测试解码时自动创建输出目录"""
    # 创建一个不存在的子目录路径
    nested_dir = os.path.join(temp_output_dir, "nested", "dir")
    output_path = os.path.join(nested_dir, "test_image.png")

    # 创建一个简单的测试图片并编码
    temp_img_path = os.path.join(temp_output_dir, "temp.png")
    img = Image.new("RGB", (10, 10), color="blue")
    img.save(temp_img_path)

    with open(temp_img_path, "rb") as f:
        image_data = f.read()
    encoded = base64.b64encode(image_data).decode("utf-8")

    # 解码到嵌套目录
    result = base64_decode_image(encoded, output_path)

    # 验证结果
    assert "图片已成功解码并保存到" in result
    assert output_path in result

    # 验证目录和文件被创建
    assert os.path.exists(nested_dir)
    assert os.path.exists(output_path)
