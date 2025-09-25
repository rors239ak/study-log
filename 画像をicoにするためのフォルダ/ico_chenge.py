import argparse
from pathlib import Path
from PIL import Image

# 出力するアイコンサイズ（Windowsデスクトップ用に複数サイズを含める）
ICON_SIZES = [16, 32, 48, 64, 128, 256]

def make_square_canvas(img: Image.Image, target: int) -> Image.Image:
    # アスペクト比を保って target に収め、正方キャンバスに中央配置
    # 元画像の縦横が異なる場合は白背景にする（デスクトップ用に見やすくするため）
    w, h = img.size
    scale = min(target / w, target / h)
    new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
    resized = img.resize((new_w, new_h), resample=Image.LANCZOS)
    x = (target - new_w) // 2
    y = (target - new_h) // 2

    if w != h:
        # 縦横比が変わる場合は白背景
        canvas = Image.new("RGBA", (target, target), (255, 255, 255, 255))
        if resized.mode == "RGBA":
            canvas.paste(resized, (x, y), resized)
        else:
            canvas.paste(resized, (x, y))
    else:
        # 元が正方形なら透明背景で中央配置
        canvas = Image.new("RGBA", (target, target), (0, 0, 0, 0))
        canvas.paste(resized, (x, y), resized if resized.mode == "RGBA" else None)

    return canvas

def convert_image_to_ico(src: Path, overwrite: bool):
    img = Image.open(src)
    if img.mode not in ("RGBA", "RGB"):
        img = img.convert("RGBA")
    # 大きな正方画像（256x256）を作り、そこから.icoに複数サイズを含めて保存
    base = make_square_canvas(img, 256)
    dst = src.with_suffix(".ico")
    if dst.exists() and not overwrite:
        print(f"Skip (exists): {dst.name}")
        return
    # Pillow に sizes を渡すと内部で各サイズを生成してくれる
    base.save(dst, format="ICO", sizes=[(s, s) for s in ICON_SIZES])
    print(f"Converted: {src.name} -> {dst.name} (sizes: {', '.join(map(str, ICON_SIZES))})")

def main():
    p = argparse.ArgumentParser(description="同フォルダ内の画像を Windows 用 .ico（複数サイズ含む）に変換")
    p.add_argument("--overwrite", action="store_true", help="既存の .ico を上書きする")
    args = p.parse_args()

    base_dir = Path(__file__).resolve().parent
    exts = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tif", "*.webp")

    files = []
    for e in exts:
        files.extend(sorted(base_dir.glob(e)))

    if not files:
        print("変換対象の画像が見つかりません。")
        return

    for f in files:
        try:
            convert_image_to_ico(f, args.overwrite)
        except Exception as ex:
            print(f"Failed: {f.name} -> {ex}")

if __name__ == "__main__":
    main()