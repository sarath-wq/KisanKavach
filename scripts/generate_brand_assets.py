"""
KisanKavach - Brand Asset & Splash Screen Generator
Processes media_1789532169218.jpg and produces:
- Web assets (logo.png, logo-shield.png, icon.png, icon-192.png, icon-512.png)
- Android splash screens across all 11 densities (portrait & landscape)
- Android launcher icons (ic_launcher, ic_launcher_round, ic_launcher_foreground)
"""

import os
from PIL import Image, ImageDraw

SRC_LOGO = r"C:/Users/ACER/.gemini/antigravity/brain/38925bf4-5e20-4f48-94c1-995f735978fb/.user_uploaded/media_1789532169218.jpg"
PUBLIC_DIR = r"d:\KisanKavach\public"
ANDROID_RES_DIR = r"d:\KisanKavach\android\app\src\main\res"


def make_transparent(img, threshold=245):
    img = img.convert("RGBA")
    raw = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = raw[x, y]
            if r >= threshold and g >= threshold and b >= threshold:
                raw[x, y] = (255, 255, 255, 0)
            elif r >= 230 and g >= 230 and b >= 230:
                avg = (r + g + b) // 3
                alpha = int((255 - avg) * (255 / (255 - 230)))
                raw[x, y] = (r, g, b, max(0, min(255, alpha)))
    return img


def main():
    if not os.path.exists(SRC_LOGO):
        print("Source logo not found:", SRC_LOGO)
        return

    print("Loading source logo:", SRC_LOGO)
    src_img = Image.open(SRC_LOGO).convert("RGBA")

    # 1. Bounding Boxes
    # Full logo content (shield + text): (104, 145, 936, 841)
    full_crop = src_img.crop((104, 145, 936, 841))
    
    # Shield only crop: (290, 145, 734, 642)
    shield_crop = src_img.crop((290, 145, 734, 642))

    # Transparent versions
    full_transparent = make_transparent(full_crop)
    shield_transparent = make_transparent(shield_crop)

    # -------------------------------------------------------------
    # WEB ASSETS
    # -------------------------------------------------------------
    print("Generating Web Assets...")
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    # public/logo.png: Full brand logo centered on transparent square 512x512
    logo_512 = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    full_w, full_h = full_transparent.size
    scale = 480 / max(full_w, full_h)
    resized_full = full_transparent.resize((int(full_w * scale), int(full_h * scale)), Image.Resampling.LANCZOS)
    rw, rh = resized_full.size
    logo_512.paste(resized_full, ((512 - rw) // 2, (512 - rh) // 2), resized_full)
    logo_512.save(os.path.join(PUBLIC_DIR, "logo.png"), "PNG")
    logo_512.save(os.path.join(PUBLIC_DIR, "logo-full.png"), "PNG")
    print("Saved public/logo.png and public/logo-full.png")

    # public/logo-shield.png: Shield emblem only on transparent square 512x512
    shield_512 = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    sw, sh = shield_transparent.size
    scale_s = 480 / max(sw, sh)
    resized_shield = shield_transparent.resize((int(sw * scale_s), int(sh * scale_s)), Image.Resampling.LANCZOS)
    rsw, rsh = resized_shield.size
    shield_512.paste(resized_shield, ((512 - rsw) // 2, (512 - rsh) // 2), resized_shield)
    shield_512.save(os.path.join(PUBLIC_DIR, "logo-shield.png"), "PNG")
    shield_512.save(os.path.join(PUBLIC_DIR, "icon.png"), "PNG")
    print("Saved public/logo-shield.png and public/icon.png")

    # PWA icons (192 and 512)
    icon_192 = shield_512.resize((192, 192), Image.Resampling.LANCZOS)
    icon_192.save(os.path.join(PUBLIC_DIR, "icon-192.png"), "PNG")
    shield_512.save(os.path.join(PUBLIC_DIR, "icon-512.png"), "PNG")
    print("Saved public/icon-192.png and public/icon-512.png")

    # -------------------------------------------------------------
    # ANDROID SPLASH SCREENS
    # -------------------------------------------------------------
    print("Generating Android Splash Screens across all densities...")
    # Splash specifications: (relative_folder, width, height, is_portrait)
    splash_specs = [
        ("drawable", 480, 800, True),
        ("drawable-port-mdpi", 320, 480, True),
        ("drawable-port-hdpi", 480, 800, True),
        ("drawable-port-xhdpi", 720, 1280, True),
        ("drawable-port-xxhdpi", 960, 1600, True),
        ("drawable-port-xxxhdpi", 1280, 1920, True),
        ("drawable-land-mdpi", 480, 320, False),
        ("drawable-land-hdpi", 800, 480, False),
        ("drawable-land-xhdpi", 1280, 720, False),
        ("drawable-land-xxhdpi", 1600, 960, False),
        ("drawable-land-xxxhdpi", 1920, 1280, False),
    ]

    for folder, w, h, is_portrait in splash_specs:
        target_dir = os.path.join(ANDROID_RES_DIR, folder)
        os.makedirs(target_dir, exist_ok=True)
        splash_file = os.path.join(target_dir, "splash.png")

        # Crisp Pure White Background
        splash_img = Image.new("RGBA", (w, h), (255, 255, 255, 255))

        # Determine scaling for full brand logo
        if is_portrait:
            # Target width: 62% of screen width
            target_w = int(w * 0.64)
            scale = target_w / full_w
            target_h = int(full_h * scale)
        else:
            # Target height: 60% of screen height
            target_h = int(h * 0.60)
            scale = target_h / full_h
            target_w = int(full_w * scale)

        scaled_logo = full_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Center in canvas
        pos_x = (w - target_w) // 2
        pos_y = (h - target_h) // 2
        splash_img.paste(scaled_logo, (pos_x, pos_y), scaled_logo.convert("RGBA"))

        splash_img.convert("RGB").save(splash_file, "PNG")
        print(f"Generated {folder}/splash.png ({w}x{h})")

    # -------------------------------------------------------------
    # ANDROID LAUNCHER ICONS (MIPMAP)
    # -------------------------------------------------------------
    print("Generating Android Launcher Icons...")
    icon_specs = [
        ("mipmap-mdpi", 48, 108),
        ("mipmap-hdpi", 72, 162),
        ("mipmap-xhdpi", 96, 216),
        ("mipmap-xxhdpi", 144, 324),
        ("mipmap-xxxhdpi", 192, 432),
    ]

    for folder, icon_size, fg_size in icon_specs:
        target_dir = os.path.join(ANDROID_RES_DIR, folder)
        os.makedirs(target_dir, exist_ok=True)

        # 1. Standard ic_launcher.png (White background with shield)
        ic_standard = Image.new("RGBA", (icon_size, icon_size), (255, 255, 255, 255))
        s_target = int(icon_size * 0.82)
        s_scaled = shield_transparent.resize((s_target, s_target), Image.Resampling.LANCZOS)
        pos = (icon_size - s_target) // 2
        ic_standard.paste(s_scaled, (pos, pos), s_scaled)
        ic_standard.save(os.path.join(target_dir, "ic_launcher.png"), "PNG")

        # 2. Round ic_launcher_round.png
        ic_round = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ic_round)
        draw.ellipse((0, 0, icon_size, icon_size), fill=(255, 255, 255, 255))
        ic_round.paste(s_scaled, (pos, pos), s_scaled)
        ic_round.save(os.path.join(target_dir, "ic_launcher_round.png"), "PNG")

        # 3. Adaptive Foreground ic_launcher_foreground.png
        ic_fg = Image.new("RGBA", (fg_size, fg_size), (0, 0, 0, 0))
        # Android adaptive icon safe zone is 66% (fg_size * 0.62)
        fg_target = int(fg_size * 0.62)
        fg_scaled = shield_transparent.resize((fg_target, fg_target), Image.Resampling.LANCZOS)
        fg_pos = (fg_size - fg_target) // 2
        ic_fg.paste(fg_scaled, (fg_pos, fg_pos), fg_scaled)
        ic_fg.save(os.path.join(target_dir, "ic_launcher_foreground.png"), "PNG")

        print(f"Generated {folder} launcher icons ({icon_size}x{icon_size})")

    print("\nALL BRAND ASSETS & ANDROID SPLASH SCREENS GENERATED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
