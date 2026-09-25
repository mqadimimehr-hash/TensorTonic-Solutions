import math, random
from PIL import Image, ImageDraw, ImageFont
import os
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"
BG = (13, 17, 38); ACC = (255, 184, 76); ACC2 = (94, 234, 212); FG = (240, 242, 250); DIM = (60, 70, 110)
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
M = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def network(d, x0, y0, w, h, layers, color, r):
    pts = []
    for i, n in enumerate(layers):
        x = x0 + w * i / (len(layers) - 1)
        pts.append([(x, y0 + h * (j + 1) / (n + 1)) for j in range(n)])
    for a, b in zip(pts, pts[1:]):
        for p in a:
            for q in b:
                d.line([p, q], fill=color, width=2 * K)
    for layer in pts:
        for (x, y) in layer:
            d.ellipse([x - r, y - r, x + r, y + r], fill=BG, outline=ACC2, width=4 * K)

def sigmoid_curve(d, x0, y0, w, h, color, width):
    r = width / 2
    for t in range(3001):
        x = x0 + w * t / 3000
        y = y0 + h - h / (1 + math.exp(-(t / 3000 * 12 - 6)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)

# Banner 2560x1440, safe area 1546x423 centered
K = 2
W, H = 2560 * K, 1440 * K
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
random.seed(3)
for _ in range(60):
    x, y = random.randint(0, W), random.randint(0, H)
    if abs(x - W / 2) < 1150 * K and abs(y - H / 2) < 300 * K:
        continue
    d.text((x, y), random.choice(["σ", "∑", "∇", "eˣ", "log", "θ", "∂", "W", "softmax"]), font=ImageFont.truetype(M, 34 * K), fill=(30, 38, 72))
cx, cy = W // 2, H // 2
network(d, cx - 1120 * K, cy - 170 * K, 260 * K, 340 * K, [3, 4, 2], DIM, 16 * K)
sigmoid_curve(d, cx + 830 * K, cy - 150 * K, 290 * K, 300 * K, ACC, 10 * K)
d.line([(cx + 830 * K, cy + 160 * K), (cx + 1120 * K, cy + 160 * K)], fill=DIM, width=3 * K)
t = "ML From Scratch"
f = ImageFont.truetype(B, 130 * K); tw = d.textlength(t, font=f)
d.text((cx - tw / 2, cy - 150 * K), t, font=f, fill=FG)
s = "One algorithm a week  ·  Python + NumPy"
f2 = ImageFont.truetype(R, 52 * K); sw = d.textlength(s, font=f2)
d.text((cx - sw / 2, cy + 50 * K), s, font=f2, fill=ACC)
d.rectangle([cx - 90 * K, cy + 20 * K, cx + 90 * K, cy + 27 * K], fill=ACC2)
img = img.resize((2560, 1440), Image.LANCZOS)
img.save(OUT + "youtube-banner.png", optimize=True)

# Profile 800x800 (shown as a circle)
S = 1600
p = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(p)
d.ellipse([80, 80, S - 80, S - 80], outline=ACC2, width=28)
sigmoid_curve(d, 340, 880, 920, 340, ACC, 32)
f = ImageFont.truetype(B, 500); tw = d.textlength("ML", font=f)
d.text(((S - tw) / 2, 300), "ML", font=f, fill=FG)
p = p.resize((800, 800), Image.LANCZOS)
p.save(OUT + "profile-picture.png", optimize=True)
