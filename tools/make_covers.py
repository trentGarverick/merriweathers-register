#!/usr/bin/env python3
"""Render typographic cover + hub images for Merriweather's Register."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = "/home/claude/fonts/"
INK   = (43, 36, 25)      # warm near-black
RED   = (158, 43, 37)     # Doris's red pencil
TEAL  = (47, 111, 106)    # Mild River
CREAM = (247, 241, 225)
PAPER = (252, 248, 238)

def playfair(size, wght=900):
    f = ImageFont.truetype(F + "PlayfairDisplay.ttf", size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

def caveat(size, wght=600):
    f = ImageFont.truetype(F + "Caveat.ttf", size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

def crimson(size, style="Regular"):
    return ImageFont.truetype(F + f"CrimsonText-{style}.ttf", size)

def elite(size):
    return ImageFont.truetype(F + "SpecialElite-Regular.ttf", size)

def paper_bg(w, h):
    img = Image.new("RGB", (w, h), CREAM)
    # subtle noise
    noise = Image.effect_noise((w // 2, h // 2), 14).resize((w, h)).convert("L")
    img = Image.composite(Image.new("RGB", (w, h), (236, 228, 206)), img, noise.point(lambda p: p // 6))
    # vignette
    vig = Image.new("L", (w, h), 0)
    dv = ImageDraw.Draw(vig)
    dv.ellipse([-w * 0.25, -h * 0.25, w * 1.25, h * 1.25], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(min(w, h) // 8))
    img = Image.composite(img, Image.new("RGB", (w, h), (231, 221, 197)), vig)
    return img

def tracked(draw, xy, text, font, fill, tracking=0, anchor=None, center_x=None):
    """Draw text with letter tracking; if center_x given, center the tracked text there."""
    if tracking == 0 and center_x is None:
        draw.text(xy, text, font=font, fill=fill, anchor=anchor); return
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (center_x - total / 2) if center_x is not None else xy[0]
    y = xy[1]
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += cw + tracking
    return total

def hrule(d, x0, x1, y, w=3, fill=INK):
    d.rectangle([x0, y, x1, y + w - 1], fill=fill)

def double_rule(d, x0, x1, y, heavy=5, light=2, gap=5, fill=INK):
    hrule(d, x0, x1, y, heavy, fill)
    hrule(d, x0, x1, y + heavy + gap, light, fill)
    return y + heavy + gap + light

def diamond(d, cx, cy, r, fill=INK):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)

def center(d, y, text, font, fill=INK, W=1400):
    d.text((W / 2, y), text, font=font, fill=fill, anchor="ma")
    bbox = d.textbbox((W / 2, y), text, font=font, anchor="ma")
    return bbox[3]

# ─────────────────────────────────────────────── COVER 1400x1978
W, H = 1400, 1978
img = paper_bg(W, H)
d = ImageDraw.Draw(img)
M = 70  # margin

# border: outer heavy + inner light
d.rectangle([M - 26, M - 26, W - M + 26, H - M + 26], outline=INK, width=5)
d.rectangle([M - 14, M - 14, W - M + 14, H - M + 14], outline=INK, width=2)

y = M + 4
# top eyebrow
eb = crimson(30, "SemiBold")
tracked(d, (0, y), "GENTLE RAPIDS' MOST TRUSTED SOURCE OF WHOLLY INVENTED NEWS", eb, INK, tracking=4, center_x=W / 2)
y += 46
hrule(d, M, W - M, y, 2); y += 26

# nameplate
mw = caveat(112, 680)
d.text((W / 2, y), "Merriweather's", font=mw, fill=TEAL, anchor="ma")
y += 118
reg = playfair(204, 900)
tracked(d, (0, y), "REGISTER", reg, INK, tracking=10, center_x=W / 2)
y += 252
sub = playfair(54, 700)
tracked(d, (0, y), "OF AGREEABLE OCCURRENCES", sub, INK, tracking=12, center_x=W / 2)
y += 80

# motto with diamonds
motto = crimson(36, "Italic")
mtw = d.textlength("All the News That's Fit to Invent", font=motto)
d.text((W / 2, y), "All the News That's Fit to Invent", font=motto, fill=INK, anchor="ma")
diamond(d, W / 2 - mtw / 2 - 40, y + 26, 8); diamond(d, W / 2 + mtw / 2 + 40, y + 26, 8)
y += 62

# dateline bar between rules
hrule(d, M, W - M, y, 2); y += 12
dl = crimson(29, "SemiBold")
d.text((M + 8, y), "VOL. I, No. 1", font=dl, fill=INK)
d.text((W / 2, y), "GENTLE RAPIDS, OHIO — WEDNESDAY, JUNE 10, 2026", font=dl, fill=INK, anchor="ma")
d.text((W - M - 8, y), "PRICE: TWO CENTS*", font=dl, fill=INK, anchor="ra")
y += 44
y = double_rule(d, M, W - M, y, heavy=7, light=2) + 50

# lead headline — auto-fit so no line exceeds the inner frame
lead_lines = ["MAN RETURNS LIBRARY BOOK", "47 YEARS OVERDUE; TOWN", "RESPONDS WITH PARADE"]
max_w = W - 2 * M - 24
size = 88
while size > 40:
    hl = playfair(size, 900)
    if max(d.textlength(t, font=hl) for t in lead_lines) <= max_w:
        break
    size -= 2
for line in lead_lines:
    y = center(d, y, line, hl) + 8
y += 22
deck = crimson(36, "Italic")
for line in ['Fine of $861.35 Forgiven "On Account of Everyone Being So Pleased" —',
             'Marching Band Reports Having the Time of Their Lives']:
    y = center(d, y, line, deck) + 6
y += 30

# rule with diamond
hrule(d, M + 160, W - M - 160, y, 2); diamond(d, W / 2, y + 1, 10); y += 28

# teasers
t_big = playfair(46, 800)
t_small = crimson(29, "SemiBold")

# teaser 1 with the strikethrough gag
line1 = "COUNCIL MEETING ENDS IN CHAOS"
lw = d.textlength(line1, font=t_big)
x0 = W / 2 - lw / 2
d.text((x0, y), line1, font=t_big, fill=INK)
chaos_x = x0 + d.textlength("COUNCIL MEETING ENDS IN ", font=t_big)
chaos_w = d.textlength("CHAOS", font=t_big)
# red strike through CHAOS
d.line([chaos_x - 6, y + 34, chaos_x + chaos_w + 6, y + 27], fill=RED, width=6)
# handwritten correction
cv = caveat(52, 700)
d.text((chaos_x + chaos_w / 2, y - 44), "confetti!", font=cv, fill=RED, anchor="ma")
y += 64
y = center(d, y, "Vote Was 7–0, With One Councilman Resting Productively  ·  Page 4", t_small) + 30

def teaser(y, big, small):
    y = center(d, y, big, t_big) + 8
    y = center(d, y, small, t_small) + 28
    return y

y = teaser(y, "WHICH DUCK IS FRIENDLIEST?", "Our Six-Month Investigation Finally Concludes  ·  B. Quill, Esq., Page 8")
y = teaser(y, "THIS DAY IN HISTORY", "66 Million Years of Good News, Fully Footnoted  ·  Prof. Bunkle, Page 9")

hrule(d, M + 160, W - M - 160, y, 2); diamond(d, W / 2, y + 1, 10); y += 28
y = center(d, y, "INSIDE: The Weekly Pelican Fact (Page 6, As Negotiated)  ·  Stupid Poems  ·  Sound Counsel", t_small) + 8
y = center(d, y, "PERSONALS: Weird? Lonely? Own Dice? See the Back Pages", t_small) + 8

# bottom bar
by = H - M - 64
hrule(d, M, W - M, by - 16, 2)
foot = crimson(27, "Italic")
d.text((W / 2, by + 2), "*Negotiable. This newspaper contains no facts whatsoever. You're welcome. — The Management",
       font=foot, fill=INK, anchor="ma")

# Doris's stamp (rotated)
stamp = Image.new("RGBA", (470, 124), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, 466, 120], radius=14, outline=RED + (200,), width=5)
sf = elite(33)
sd.text((235, 38), "EDITED FOR HAPPINESS", font=sf, fill=RED + (200,), anchor="mm")
sd.text((235, 84), "— D.P.", font=sf, fill=RED + (200,), anchor="mm")
stamp = stamp.rotate(-7, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (W - M - stamp.width - 6, M + 96), stamp)

img.save("/home/claude/register/images/vol1no1-cover.png", optimize=True)
print("cover ok", img.size)

# ─────────────────────────────────────────────── HUB 1280x768
W2, H2 = 1280, 768
hub = paper_bg(W2, H2)
d = ImageDraw.Draw(hub)
M2 = 54
d.rectangle([M2 - 22, M2 - 22, W2 - M2 + 22, H2 - M2 + 22], outline=INK, width=4)
d.rectangle([M2 - 12, M2 - 12, W2 - M2 + 12, H2 - M2 + 12], outline=INK, width=2)

y = M2 + 14
tracked(d, (0, y), "GENTLE RAPIDS' MOST TRUSTED SOURCE OF WHOLLY INVENTED NEWS", crimson(24, "SemiBold"), INK, tracking=3, center_x=W2 / 2)
y += 40
hrule(d, M2 + 30, W2 - M2 - 30, y, 2); y += 22
d.text((W2 / 2, y), "Merriweather's", font=caveat(86, 680), fill=TEAL, anchor="ma"); y += 96
tracked(d, (0, y), "REGISTER", playfair(150, 900), INK, tracking=8, center_x=W2 / 2); y += 186
tracked(d, (0, y), "OF AGREEABLE OCCURRENCES", playfair(38, 700), INK, tracking=9, center_x=W2 / 2); y += 64
m2 = crimson(30, "Italic")
mw2 = d.textlength("All the News That's Fit to Invent", font=m2)
d.text((W2 / 2, y), "All the News That's Fit to Invent", font=m2, fill=INK, anchor="ma")
diamond(d, W2 / 2 - mw2 / 2 - 34, y + 22, 7); diamond(d, W2 / 2 + mw2 / 2 + 34, y + 22, 7)
y += 58
hrule(d, M2 + 30, W2 - M2 - 30, y, 2); y += 18
d.text((W2 / 2, y), "SERVING GENTLE RAPIDS SINCE 1987, PROBABLY  ·  EVERY STORY GUARANTEED FALSE AND PLEASANT",
       font=crimson(24, "SemiBold"), fill=INK, anchor="ma")

hub.save("/home/claude/register/register-hub.png", optimize=True)
print("hub ok", hub.size)
