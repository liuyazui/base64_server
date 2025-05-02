"""
Base64编码解码MCP服务器

这个MCP服务器提供Base64编码和解码功能，支持文本和图片的转换。
"""

import base64
import io
import os
from typing import Optional

from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from PIL import Image as PILImage

# 创建MCP服务器实例
mcp = FastMCP("Base64编码解码服务器")

# === 工具实现 ===


@mcp.tool()
def base64_encode_text(text: str) -> str:
    """将文本转换为Base64编码

    Args:
        text: 要编码的文本

    Returns:
        Base64编码结果
    """
    try:
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        return f"Base64编码结果: {encoded}"
    except Exception as e:
        return f"编码失败: {str(e)}"


@mcp.tool()
def base64_decode_text(encoded: str) -> str:
    """将Base64编码解码为文本

    Args:
        encoded: Base64编码的字符串

    Returns:
        解码后的文本
    """
    try:
        # 清理输入，移除可能的前缀和空白
        encoded = encoded.strip()
        if "Base64编码结果:" in encoded:
            encoded = encoded.split("Base64编码结果:")[1].strip()

        # 验证是否为有效的Base64字符串
        if not all(
            c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
            for c in encoded
        ):
            return "错误: 输入包含非Base64字符"

        # 尝试解码
        decoded = base64.b64decode(encoded).decode("utf-8")
        return f"Base64解码结果: {decoded}"
    except Exception as e:
        return f"解码失败: {str(e)}"


@mcp.tool()
def base64_encode_image(image_path: str) -> str:
    """将图片转换为Base64编码

    Args:
        image_path: 图片文件路径

    Returns:
        Base64编码结果
    """
    try:
        if not os.path.exists(image_path):
            return f"错误: 文件 '{image_path}' 不存在"

        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")

        # 获取MIME类型
        img = PILImage.open(image_path)
        mime_type = f"image/{img.format.lower()}"

        # 返回可在HTML中使用的Data URL格式
        data_url = f"data:{mime_type};base64,{encoded}"
        encoded_preview = f"图片Base64编码结果 (前100字符): {encoded[:100]}..."
        data_url_preview = f"完整Data URL (前100字符): {data_url[:100]}..."
        return f"{encoded_preview}\n\n{data_url_preview}"
    except Exception as e:
        return f"图片编码失败: {str(e)}"


@mcp.tool()
def base64_decode_image(
    encoded: str, output_path: str, mime_type: str = "image/png"
) -> str:
    """将Base64编码解码为图片

    Args:
        encoded: Base64编码的字符串
        output_path: 输出图片的路径
        mime_type: 图片的MIME类型 (默认为image/png)

    Returns:
        解码结果
    """
    try:
        # 清理输入，移除可能的前缀和空白
        encoded = encoded.strip()

        # 如果输入是Data URL格式，提取实际的Base64部分
        if encoded.startswith("data:"):
            # 分离MIME类型和Base64内容
            header, encoded = encoded.split(",", 1)
            if ";base64" not in header:
                return "错误: 输入不是有效的Base64编码的Data URL"
            # 提取MIME类型但不使用，因为我们使用参数中的mime_type

        # 解码Base64
        image_data = base64.b64decode(encoded)

        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存图片
        with open(output_path, "wb") as image_file:
            image_file.write(image_data)

        return f"图片已成功解码并保存到 {output_path}"
    except Exception as e:
        return f"图片解码失败: {str(e)}"


# === 资源实现 ===


@mcp.resource("encode://base64/text/{text}")
def get_base64_encoded_text(text: str) -> str:
    """获取文本的Base64编码

    Args:
        text: 要编码的文本

    Returns:
        Base64编码结果
    """
    try:
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        return encoded
    except Exception as e:
        return f"编码失败: {str(e)}"


@mcp.resource("decode://base64/text/{encoded}")
def get_base64_decoded_text(encoded: str) -> str:
    """获取Base64编码的解码结果

    Args:
        encoded: Base64编码的字符串

    Returns:
        解码后的文本
    """
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        return decoded
    except Exception as e:
        return f"解码失败: {str(e)}"


@mcp.resource("encode://base64/image/{image_path}")
def get_base64_encoded_image(image_path: str) -> Optional[Image]:
    """获取图片的Base64编码并返回图片

    Args:
        image_path: 图片文件路径

    Returns:
        图片对象
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"文件 '{image_path}' 不存在")

    try:
        # 读取图片并返回MCP Image对象
        img = PILImage.open(image_path)
        format_lower = img.format.lower() if img.format else "png"

        # 返回MCP Image对象
        return Image(data=img.tobytes(), format=format_lower)
    except Exception as e:
        raise ValueError(f"图片编码失败: {str(e)}")


@mcp.resource("decode://base64/image/{encoded}")
def get_base64_decoded_image(encoded: str) -> Optional[Image]:
    """获取Base64编码的解码图片

    Args:
        encoded: Base64编码的字符串

    Returns:
        解码后的图片对象
    """
    try:
        # 清理输入，移除可能的前缀
        if encoded.startswith("data:"):
            # 分离MIME类型和Base64内容
            header, encoded = encoded.split(",", 1)

        # 解码Base64
        image_data = base64.b64decode(encoded)

        # 使用PIL创建图片
        img = PILImage.open(io.BytesIO(image_data))
        format_lower = img.format.lower() if img.format else "png"

        # 返回MCP Image对象
        return Image(data=img.tobytes(), format=format_lower)
    except Exception as e:
        raise ValueError(f"图片解码失败: {str(e)}")


# === 提示模板实现 ===


@mcp.prompt()
def base64_usage_guide() -> list[base.Message]:
    """提供Base64服务的基本使用指南"""
    return [
        base.UserMessage("如何使用Base64编码解码服务？"),
        base.AssistantMessage(
            "我可以帮你进行Base64编码和解码，支持文本和图片。\n\n"
            "**文本编码**：使用`base64_encode_text`工具\n"
            "**文本解码**：使用`base64_decode_text`工具\n"
            "**图片编码**：使用`base64_encode_image`工具\n"
            "**图片解码**：使用`base64_decode_image`工具\n\n"
            "你也可以通过资源直接获取编码结果，例如：\n"
            "`encode://base64/text/Hello`将返回'Hello'的Base64编码"
        ),
    ]


@mcp.prompt()
def encode_text_prompt(text: str) -> list[base.Message]:
    """文本编码提示模板"""
    return [
        base.UserMessage(f"请将以下文本进行Base64编码：\n\n{text}"),
        base.AssistantMessage("我将使用base64_encode_text工具来完成这个任务。"),
    ]


@mcp.prompt()
def encode_image_prompt(image_path: str) -> list[base.Message]:
    """图片编码提示模板"""
    return [
        base.UserMessage(f"请将位于{image_path}的图片进行Base64编码"),
        base.AssistantMessage("我将使用base64_encode_image工具来完成这个任务。"),
    ]


@mcp.prompt()
def error_handling_prompt(error_message: str) -> list[base.Message]:
    """错误处理提示模板"""
    return [
        base.UserMessage(f"我遇到了这个错误：{error_message}"),
        base.AssistantMessage("让我帮你分析这个错误并提供解决方案。"),
    ]


if __name__ == "__main__":
    # 运行MCP服务器
    mcp.run()
