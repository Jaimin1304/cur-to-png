import os
import sys
import ctypes
from ctypes import wintypes
from PIL import Image, UnidentifiedImageError

# 定义 Windows API 函数
user32 = ctypes.WinDLL("user32", use_last_error=True)
LoadImage = user32.LoadImageW
LoadImage.argtypes = [
    wintypes.HINSTANCE,
    wintypes.LPCWSTR,
    wintypes.UINT,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.UINT,
]
LoadImage.restype = wintypes.HANDLE


def convert_cursor_to_png(cur_path, png_path):
    # 检查并创建png文件夹
    os.makedirs(png_path, exist_ok=True)

    # 获取cur文件夹中的所有文件
    files = os.listdir(cur_path)

    for file in files:
        file_path = os.path.join(cur_path, file)
        if not file.lower().endswith(".cur") and not file.lower().endswith(".ani"):
            print(f"File type not supported: {file}. Skipped.")
            continue
        try:
            # 使用ctypes加载光标文件
            hcur = LoadImage(None, file_path, 2, 0, 0, 0x00000010 | 0x00000080)
            if not hcur:
                print(f"Failed to load {file}")
                continue

            # 获取光标图像的数据
            icon = Image.open(file_path)

            # 确保图像为正方形
            size = max(icon.width, icon.height)
            new_icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            new_icon.paste(icon, ((size - icon.width) // 2, (size - icon.height) // 2))

            # 保存为png文件
            png_filename = os.path.join(png_path, f"{os.path.splitext(file)[0]}.png")
            new_icon.save(png_filename, "PNG")
            print(f"Converted {file} to {png_filename}")

        except UnidentifiedImageError:
            print(f"Cannot identify image file '{file_path}', skipping this file.")
        except Exception as e:
            print(
                f"An error occurred while processing {file}: {e}, skipping this file."
            )


if __name__ == "__main__":
    # 设置默认路径
    default_cur_directory = os.path.join(os.getcwd(), "cur")
    default_png_directory = os.path.join(os.getcwd(), "png")

    # 如果默认路径不存在，则创建
    if not os.path.exists(default_cur_directory):
        os.makedirs(default_cur_directory)
        print(f"Created directory: {default_cur_directory}")

    if not os.path.exists(default_png_directory):
        os.makedirs(default_png_directory)
        print(f"Created directory: {default_png_directory}")

    # 使用命令行参数，或者使用默认路径
    cur_directory = sys.argv[1] if len(sys.argv) > 1 else default_cur_directory
    png_directory = sys.argv[2] if len(sys.argv) > 2 else default_png_directory

    convert_cursor_to_png(cur_directory, png_directory)
