"""Render the softmax YouTube Short (1080x1920, text-on-screen, no voice).

Run:  pip install pillow imageio-ffmpeg && python make_short.py
Output: softmax-short.mp4 (add music in YouTube's editor or CapCut).
"""
import os
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "softmax-short.mp4")

BG = (13, 17, 38)
FG = (240, 242, 250)
ACC = (255, 184, 76)
TEAL = (94, 234, 212)
RED = (255, 99, 99)
DIM = (140, 150, 190)
CODE_BG = (24, 30, 60)
DY = 220  # push content toward the vertical center

FONTS = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONTS + "DejaVuSans-Bold.ttf"
REG = FONTS + "DejaVuSans.ttf"
MONO = FONTS + "DejaVuSansMono.ttf"
_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def fade(color, a):
    """Blend color toward the background (a=0 invisible, a=1 full)."""
    a = max(0.0, min(1.0, a))
    return tuple(int(BG[i] + (color[i] - BG[i]) * a) for i in range(3))


def appear(t, start, dur=0.35):
    return (t - start) / dur


def center_text(d, y, text, f, color):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y + DY), text, font=f, fill=color)


def code_box(d, y, lines, t, start, colors=None):
    a = appear(t, start)
    if a <= 0:
        return
    y += DY
    size = 50 if max(len(l) for l in lines) <= 26 else 42
    f = font(MONO, size)
    h = 90 * len(lines) + 50
    d.rounded_rectangle([90, y, W - 90, y + h], radius=28, fill=fade(CODE_BG, a))
    for i, line in enumerate(lines):
        c = (colors or {}).get(i, FG)
        d.text((130, y + 35 + 90 * i), line, font=f, fill=fade(c, a))


def footer(d):
    center_text(d, 150 - DY, "ML From Scratch", font(BOLD, 44), DIM)


# ---- scenes: (duration_seconds, draw(d, t)) -------------------------------

def s_hook(d, t):
    center_text(d, 560, "Your softmax", font(BOLD, 120), fade(FG, appear(t, 0)))
    center_text(d, 710, "is broken.", font(BOLD, 120), fade(RED, appear(t, 0.4)))
    code_box(d, 1000, [">>> softmax([1000, 1001, 1002])", "[nan nan nan]"], t, 1.0, {1: RED})


def s_what(d, t):
    center_text(d, 380, "Softmax turns scores", font(BOLD, 72), fade(FG, appear(t, 0)))
    center_text(d, 470, "into probabilities", font(BOLD, 72), fade(ACC, appear(t, 0.2)))
    center_text(d, 620, "p = eᶻ / Σ eᶻ", font(MONO, 76), fade(TEAL, appear(t, 0.6)))
    items = [("cat", 2.0, 0.659), ("dog", 1.0, 0.242), ("bird", 0.1, 0.099)]
    for i, (name, z, p) in enumerate(items):
        start = 1.2 + 0.4 * i
        a = appear(t, start)
        if a <= 0:
            continue
        y = 850 + 190 * i + DY
        grow = max(0.0, min(1.0, (t - start) / 0.8))
        d.text((110, y), f"{name}  z={z}", font=font(MONO, 44), fill=fade(FG, a))
        bar = int(760 * p * grow)
        d.rounded_rectangle([110, y + 70, 110 + max(bar, 8), y + 130], radius=14, fill=fade(ACC, a))
        d.text((140 + bar, y + 72), f"{p * grow:.2f}", font=font(BOLD, 48), fill=fade(FG, a))


def s_bug(d, t):
    center_text(d, 420, "But with big scores...", font(BOLD, 76), fade(FG, appear(t, 0)))
    code_box(d, 620, [">>> np.exp(1000)", "inf", ">>> inf / inf", "nan"], t, 0.6, {1: RED, 3: RED})
    center_text(d, 1250, "Overflow. Training breaks.", font(BOLD, 62), fade(RED, appear(t, 2.2)))


def s_fix(d, t):
    center_text(d, 420, "The fix is one line:", font(BOLD, 80), fade(FG, appear(t, 0)))
    code_box(d, 620, ["z = z - z.max()", "e = np.exp(z)", "p = e / e.sum()"], t, 0.6, {0: ACC})
    center_text(d, 1150, "Subtract the max first", font(BOLD, 62), fade(TEAL, appear(t, 1.8)))


def s_why(d, t):
    center_text(d, 420, "Why it works", font(BOLD, 90), fade(ACC, appear(t, 0)))
    lines = [
        "Shifting every score by the",
        "same amount doesn't change",
        "the softmax output.",
        "",
        "After subtracting the max,",
        "every exponent is ≤ 0,",
        "so eᶻ stays between 0 and 1.",
    ]
    for i, line in enumerate(lines):
        start = 0.5 + (0.3 * i if i < 3 else 1.8 + 0.3 * (i - 4))
        c = TEAL if i >= 4 else FG
        center_text(d, 600 + 80 * i, line, font(REG, 56), fade(c, appear(t, start)))


def s_result(d, t):
    code_box(d, 520, [">>> softmax([1000, 1001, 1002])", "[0.09  0.245  0.665]"], t, 0, {1: TEAL})
    center_text(d, 900, "No crash. Correct answer.", font(BOLD, 70), fade(TEAL, appear(t, 0.8)))
    center_text(d, 1010, "(NumPy/PyTorch do this for you)", font(REG, 46), fade(DIM, appear(t, 1.4)))


def s_outro(d, t):
    center_text(d, 520, "1 ML algorithm", font(BOLD, 96), fade(FG, appear(t, 0)))
    center_text(d, 640, "from scratch", font(BOLD, 96), fade(FG, appear(t, 0.2)))
    center_text(d, 760, "every week", font(BOLD, 96), fade(ACC, appear(t, 0.4)))
    center_text(d, 980, "Follow @MLFromScratchwithGhadimi", font(BOLD, 50), fade(TEAL, appear(t, 1.0)))
    center_text(d, 1070, "Free notes + code in the description", font(REG, 44), fade(DIM, appear(t, 1.4)))


SCENES = [(3.5, s_hook), (6.5, s_what), (5.0, s_bug), (5.0, s_fix), (6.5, s_why), (4.0, s_result), (4.5, s_outro)]


def main():
    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        # silent audio track: some platforms reject video-only uploads
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
        "-c:a", "aac", "-movflags", "+faststart", OUT,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for dur, draw in SCENES:
        for i in range(int(dur * FPS)):
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            footer(d)
            draw(d, i / FPS)
            proc.stdin.write(img.tobytes())
    proc.stdin.close()
    proc.wait()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
