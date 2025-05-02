"""
Base64编码解码功能演示
"""

import os
import sys
import tempfile
from pathlib import Path

from PIL import Image

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 导入要使用的函数
import importlib.util

spec = importlib.util.spec_from_file_location(
    "base64_server_module", str(project_root / "base64_server.py")
)
base64_server_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base64_server_module)

# 从模块中获取函数
base64_encode_text = base64_server_module.base64_encode_text
base64_decode_text = base64_server_module.base64_decode_text
base64_encode_image = base64_server_module.base64_encode_image
base64_decode_image = base64_server_module.base64_decode_image


def create_demo_image(path, color=(255, 0, 0), size=(200, 100), text="Demo Image"):
    """创建演示图片"""
    from PIL import ImageDraw, ImageFont

    # 创建彩色背景图片
    img = Image.new("RGB", size, color=color)
    draw = ImageDraw.Draw(img)

    # 添加文本
    try:
        # 尝试加载系统字体
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        # 如果无法加载系统字体，使用默认字体
        font = ImageFont.load_default()

    # 计算文本位置（居中）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    # 绘制文本
    draw.text(position, text, fill=(255, 255, 255), font=font)

    # 保存图片
    img.save(path)
    return path


def demo_text_encoding():
    """演示文本编码和解码"""
    print("\n=== 文本Base64编码和解码演示 ===\n")

    # 用户输入文本
    text = input("请输入要编码的文本: ")

    # 编码
    encode_result = base64_encode_text(text)
    print(f"\n编码结果:\n{encode_result}")

    # 从结果中提取编码后的字符串
    encoded = encode_result.split("Base64编码结果:")[1].strip()

    # 解码
    decode_result = base64_decode_text(encoded)
    print(f"\n解码结果:\n{decode_result}")

    print("\n演示完成！")


def demo_image_encoding():
    """演示图片编码和解码"""
    print("\n=== 图片Base64编码和解码演示 ===\n")

    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建演示图片
        image_path = create_demo_image(
            os.path.join(temp_dir, "demo.png"), color=(0, 128, 255), text="Base64 Demo"
        )
        print(f"已创建演示图片: {image_path}")

        # 编码
        encode_result = base64_encode_image(image_path)
        print(f"\n编码结果:\n{encode_result}")

        # 设置输出路径
        output_dir = os.path.dirname(image_path)
        output_path = os.path.join(output_dir, "decoded_demo.png")

        # 直接使用原始图片创建Data URL
        # 这样可以避免从输出文本中提取Data URL的问题
        with open(image_path, "rb") as f:
            import base64

            image_data = f.read()
            encoded = base64.b64encode(image_data).decode("utf-8")
            data_url = f"data:image/png;base64,{encoded}"

        print("\n已创建完整的Data URL用于解码")

        # 解码图片
        print("\n正在解码图片...")
        decode_result = base64_decode_image(data_url, output_path)
        print(f"\n解码结果:\n{decode_result}")

        # 验证解码后的图片是否存在
        if os.path.exists(output_path):
            print(f"\n解码后的图片已保存到: {output_path}")

            # 在这里，我们可以尝试打开图片，但在控制台环境中无法显示
            # 所以只是通知用户图片已保存
            print("请在文件管理器中查看解码后的图片。")
        else:
            print("\n错误: 解码后的图片不存在")

    print("\n演示完成！")


if __name__ == "__main__":
    print("=" * 60)
    print("Base64编码解码功能演示")
    print("=" * 60)

    while True:
        print("\n请选择演示类型:")
        print("1. 文本Base64编码和解码")
        print("2. 图片Base64编码和解码")
        print("0. 退出")

        choice = input("\n请输入选项 (0-2): ")

        if choice == "1":
            demo_text_encoding()
        elif choice == "2":
            demo_image_encoding()
        elif choice == "0":
            print("\n感谢使用！再见！")
            break
        else:
            print("\n无效选项，请重新选择。")
