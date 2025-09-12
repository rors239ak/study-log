from PIL import Image, ImageEnhance, ImageChops, ImageDraw
from pathlib import Path
import sys, random

def load_src(path):
    if not path.exists():
        return None
    return Image.open(path).convert("RGBA")

def pixelate(img: Image.Image, small=(16,16)):
    w,h = img.size
    side = min(w,h)
    img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
    return img.resize(small, Image.NEAREST)

def save_scaled(img, outpath, scale=(32,32), large_scale=(128,128)):
    out = img.resize(scale, Image.NEAREST)
    out.save(outpath)
    out_large = out.resize(large_scale, Image.NEAREST)
    out_large_path = outpath.with_name(outpath.stem + "_128" + outpath.suffix)
    out_large.save(out_large_path)
    print("Saved:", outpath, "and", out_large_path)

def generate_walk_frames(src_path: Path, name: str, out_dir: Path, small=(16,16), scale=(32,32)):
    img = load_src(src_path)
    if img is None:
        print("No source for", name, src_path); return
    base = pixelate(img, small)
    dirs = ["down","left","right","up"]
    # create 3 frames per dir by offsetting image (simple procedural step)
    for d in dirs:
        for f in range(3):
            frame = base.copy()
            # offset pattern per direction and frame to simulate stepping
            ox, oy = 0,0
            if d == "down":
                oy = (f-1)  # -1,0,1
            elif d == "up":
                oy = -(f-1)
            elif d == "left":
                ox = -(f-1)
            elif d == "right":
                ox = (f-1)
            # slightly jitter and occasionally darken a pixel to simulate limb change
            frame = ImageChops.offset(frame, ox, oy)
            # minor pixel noise for step
            px = frame.load()
            for _ in range(6):
                x = random.randrange(frame.width); y = random.randrange(frame.height)
                r,g,b,a = px[x,y]
                px[x,y] = (max(0,min(255,r+random.randint(-10,10))),
                           max(0,min(255,g+random.randint(-10,10))),
                           max(0,min(255,b+random.randint(-10,10))), a)
            outname = f"{name}_{d}_{f}.png"
            save_scaled(frame, out_dir / outname, scale=scale)

    # also save a simple sprite sheet (rows: dirs, cols: frames)
    sheet_w = scale[0] * 3
    sheet_h = scale[1] * 4
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0,0,0,0))
    for i,d in enumerate(dirs):
        for f in range(3):
            p = out_dir / f"{name}_{d}_{f}.png"
            if p.exists():
                im = Image.open(p).convert("RGBA")
                sheet.paste(im, (f*scale[0], i*scale[1]))
    sheet_path = out_dir / f"{name}_sheet.png"
    sheet.save(sheet_path)
    print("Saved sheet:", sheet_path)

def generate_decor_tiles(out_dir: Path, scale=(32,32)):
    w,h = scale
    # rock
    rock = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(rock)
    d.rectangle([0,0,w,h], fill=(90,90,90,255))
    for i in range(12):
        x = random.randint(2,w-3); y = random.randint(2,h-3)
        d.ellipse([x-3,y-2,x+3,y+2], fill=(70+random.randint(-10,10),70,70))
    save_scaled(rock, out_dir / "rock.png", scale)
    # village (simple house tile)
    house = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(house)
    # ground
    d.rectangle([0,int(h*0.5),w,h], fill=(120,180,80))
    # house body
    d.rectangle([6,10,w-6,int(h*0.6)], fill=(190,140,80))
    # roof
    d.polygon([(w//2,2),(w-6,10),(6,10)], fill=(180,30,30))
    # door
    d.rectangle([w//2-4,int(h*0.6)-6,w//2+4,int(h*0.6)], fill=(80,50,30))
    save_scaled(house, out_dir / "village.png", scale)
    # water
    water = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(water)
    d.rectangle([0,0,w,h], fill=(30,120,200))
    # simple waves
    for y in range(6, h, 6):
        for x in range(0,w,8):
            d.arc([x-6,y-3,x+6,y+3], 0, 180, fill=(80,180,230))
    save_scaled(water, out_dir / "water.png", scale)

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    images_dir = project_root / "images"
    if not images_dir.exists():
        print("images directory not found:", images_dir); sys.exit(1)

    # grass tiles exist already; ensure basic ones present
    generate_decor_tiles(images_dir, scale=(32,32))

    # generate walk frames for classes; prefer specific source if exists, else use archer.png
    classes = {"hero":"hero.png", "wizard":"wizard.png", "assassin":"assassin.png"}
    for cname, fname in classes.items():
        src = images_dir / fname
        if not src.exists():
            # fallback to archer.png if class-specific file missing
            src = images_dir / "archer.png"
        if not src.exists():
            print("No source image for", cname, "- put a source at", images_dir / fname, "or archer.png"); continue
        generate_walk_frames(src, cname, images_dir, small=(16,16), scale=(32,32))

    print("Done.")