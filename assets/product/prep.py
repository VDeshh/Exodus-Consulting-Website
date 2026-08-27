# -*- coding: utf-8 -*-
"""Prepare real Fennec product screenshots for the Exodus site.
Crops browser chrome, removes empty/QA regions, blurs guest PII.
Fractional coords so it is resolution independent. Verify output via the contact sheet.
"""
import os
from PIL import Image, ImageFilter, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "shots")
os.makedirs(OUT, exist_ok=True)

# name: (src, crop(x0,y0,x1,y1) fractions of ORIGINAL, [blur boxes as fractions of CROPPED])
RECIPES = {
    # Floor plan editor + table inspector. Crop away the toolbar row (holds the "test" plan name
    # and "Unsaved changes"), keeping the canvas and the inspector panel.
    "floorplan-editor": ("cap-2.png", (0.000, 0.085, 1.000, 1.000), [(0.020, 0.958, 0.120, 0.999)]),

    # Event builder with live customer preview. Crop away the debug banner AND the pending
    # reservation bar at the top (which carries a guest name, email and phone).
    "event-builder":    ("cap-3.png", (0.000, 0.082, 1.000, 1.000), [(0.020, 0.958, 0.120, 0.999)]),

    # Campaign composer + live email preview. Blur every guest-name / address occurrence.
    "campaign-composer":("cap-6.png", (0.000, 0.000, 1.000, 1.000),
                         [(0.388, 0.476, 0.448, 0.500),   # audience "Just <name>"
                          (0.363, 0.656, 0.473, 0.682),   # subject field
                          (0.363, 0.716, 0.413, 0.742),   # body greeting
                          (0.828, 0.328, 0.938, 0.352),   # phone preview subject
                          (0.843, 0.362, 0.908, 0.383),   # phone preview to-address
                          (0.828, 0.384, 0.868, 0.405),   # phone preview greeting
                          (0.020, 0.970, 0.108, 0.999)]), # sidebar account email

    # Email template designer (VIP Bottle Drop + colour tokens). Blur the draft title only.
    "email-designer":   ("cap-7.png", (0.000, 0.000, 1.000, 1.000), [(0.024, 0.012, 0.145, 0.042)]),

    # Ferry AI assistant panel, cropped to the card itself (the previous crop cut
    # the panel off and showed empty dashboard tiles). Blur the faint ghost text
    # behind the composer, which carries a guest name.
    "ferry-assistant":  ("cap-1.png", (0.832, 0.440, 0.995, 0.920),
                         [(0.000, 0.795, 1.000, 0.890)]),

    # Guest pass / member profile. Blur name + phone + pass id.
    "guest-pass":       ("cap-8.png", (0.000, 0.020, 1.000, 0.960),
                         [(0.190, 0.205, 0.420, 0.270)]),  # "Shiven L" + phone block

    # Guest-facing discover feed. No PII.
    "discover-feed":    ("cap-9.png", (0.000, 0.022, 1.000, 0.960), []),

    # Public event page. Crop before the empty "No packages" state; blur the pass bar.
    "event-page":       ("cap-10.png", (0.000, 0.030, 1.000, 0.690),
                         [(0.055, 0.905, 0.420, 0.985)]),  # "Welcome back ... Fennec Pass FP-..."

    # Live table selection on a real venue floor. Crop above the booking form (which holds PII).
    "table-select":     ("cap-11.png", (0.000, 0.000, 1.000, 0.745), []),
}


def blur_box(img, box):
    w, h = img.size
    x0, y0, x1, y1 = [int(round(v)) for v in
                      (box[0] * w, box[1] * h, box[2] * w, box[3] * h)]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w, x1), min(h, y1)
    if x1 <= x0 or y1 <= y0:
        return
    region = img.crop((x0, y0, x1, y1))
    # heavy pixelation + blur so text is unrecoverable
    small = region.resize((max(1, region.width // 22), max(1, region.height // 12)), Image.BILINEAR)
    region = small.resize(region.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(6))
    img.paste(region, (x0, y0))


MAXW = 2000
for name, (src, crop, blurs) in RECIPES.items():
    p = os.path.join(RAW, src)
    if not os.path.exists(p):
        print("MISSING", src); continue
    im = Image.open(p).convert("RGB")
    W, H = im.size
    box = (int(crop[0] * W), int(crop[1] * H), int(crop[2] * W), int(crop[3] * H))
    im = im.crop(box)
    for b in blurs:
        blur_box(im, b)
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    out = os.path.join(OUT, name + ".jpg")
    im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"{name:20s} {im.size}  {round(os.path.getsize(out)/1024)}KB")

# contact sheet for verification
import glob
files = sorted(glob.glob(os.path.join(OUT, "*.jpg")))
cols, tw = 2, 900
thumbs = []
for f in files:
    t = Image.open(f)
    t.thumbnail((tw, 2000))
    thumbs.append((os.path.basename(f), t))
rows = (len(thumbs) + cols - 1) // cols
rh = max(t.height for _, t in thumbs) + 34
sheet = Image.new("RGB", (cols * tw + 30, rows * rh + 20), (14, 14, 18))
d = ImageDraw.Draw(sheet)
for i, (nm, t) in enumerate(thumbs):
    r, c = divmod(i, cols)
    x, y = 10 + c * (tw + 10), 10 + r * rh
    d.text((x, y), nm, fill=(224, 177, 72))
    sheet.paste(t, (x, y + 18))
sheet.save(os.path.join(HERE, "contact-sheet.jpg"), "JPEG", quality=72, optimize=True)
print("sheet:", sheet.size)
