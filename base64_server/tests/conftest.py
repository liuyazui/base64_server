"""测试夹具配置"""

import os
import base64
import pytest
from PIL import Image


@pytest.fixture
def sample_text():
    """返回一个示例文本"""
    return "Hello, World! 你好，世界！"


@pytest.fixture
def sample_encoded_text():
    """返回一个示例文本的Base64编码"""
    text = "Hello, World! 你好，世界！"
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


@pytest.fixture
def temp_output_dir(tmpdir):
    """创建一个临时输出目录"""
    output_dir = os.path.join(str(tmpdir), "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


@pytest.fixture
def temp_image_path(tmpdir):
    """创建一个临时测试图片"""
    img_path = os.path.join(str(tmpdir), "test_image.png")
    
    # 创建一个简单的测试图片
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(img_path)
    
    return img_path
