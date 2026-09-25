"""3D YouTube banner: a loss landscape with a gradient-descent path.

Run:  pip install numpy matplotlib pillow && python make_3d_banner.py
Output: youtube-banner-3d.png (2560x1440; title stays inside YouTube's
1546x423 center area that every device shows).
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "youtube-banner-3d.png")
W, H = 2560, 1440

BG = (13, 17, 38)
FG = (240, 242, 250)
ACC = (255, 184, 76)
TEAL = (94, 234, 212)
FONTS = "/usr/share/fonts/truetype/dejavu/"


def loss(x, y):
    """A bowl with a few ripples, so the path has something to roll through."""
    return 0.35 * x**2 + 0.6 * y**2 + 0.9 * np.sin(1.3 * x) * np.cos(1.1 * y) + 3


def grad(x, y):
    dx = 0.7 * x + 0.9 * 1.3 * np.cos(1.3 * x) * np.cos(1.1 * y)
    dy = 1.2 * y - 0.9 * 1.1 * np.sin(1.3 * x) * np.sin(1.1 * y)
    return dx, dy


def render_surface():
    x = np.linspace(-4.2, 4.2, 220)
    y = np.linspace(-3.2, 3.2, 180)
    X, Y = np.meshgrid(x, y)
    Z = loss(X, Y)

    # gradient descent from a high corner
    px, py, path = 3.9, 2.9, []
    for _ in range(90):
        path.append((px, py, loss(px, py)))
        gx, gy = grad(px, py)
        px, py = px - 0.08 * gx, py - 0.08 * gy
    path = np.array(path)

    cmap = LinearSegmentedColormap.from_list(
        "brand", [(0.05, 0.25, 0.42), (0.20, 0.62, 0.66), (0.37, 0.92, 0.83), (0.75, 0.80, 0.55)]
    )
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    fig.patch.set_alpha(0)
    ax = fig.add_axes([-0.12, -0.35, 1.24, 1.7], projection="3d")
    ax.set_facecolor((0, 0, 0, 0))
    ax.plot_surface(X, Y, Z, cmap=cmap, rstride=3, cstride=3, linewidth=0.25,
                    edgecolor=(0.05, 0.07, 0.15, 0.55), antialiased=True, alpha=0.95)
    ax.view_init(elev=32, azim=-58)
    ax.set_box_aspect((1.6, 1.2, 0.55))
    ax.set_axis_off()
    # project the path to pixel coords so it can be drawn on top in PIL
    from mpl_toolkits.mplot3d import proj3d
    fig.canvas.draw()
    xs, ys, _ = proj3d.proj_transform(path[:, 0], path[:, 1], path[:, 2] + 0.05, ax.get_proj())
    pix = ax.transData.transform(np.column_stack([xs, ys]))
    screen = [(float(px_), float(H - py_)) for px_, py_ in pix]
    tmp = os.path.join(HERE, "_surface.png")
    fig.savefig(tmp, transparent=True, dpi=100)
    plt.close(fig)
    img = Image.open(tmp).convert("RGBA").resize((W, H))
    os.remove(tmp)
    return img, screen


def draw_path(base, pts):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.line(pts, fill=ACC + (170,), width=26, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(glow)
    d = ImageDraw.Draw(base)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.line([(x0, y0), (x1, y1)], fill=ACC, width=8)
    for x, y in pts:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=ACC)
    x, y = pts[0]
    d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=ACC)
    x, y = pts[-1]
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([x - 60, y - 60, x + 60, y + 60], fill=(255, 255, 255, 140))
    base.alpha_composite(halo.filter(ImageFilter.GaussianBlur(22)))
    d.ellipse([x - 24, y - 24, x + 24, y + 24], fill=FG, outline=ACC, width=6)


def main():
    base = Image.new("RGBA", (W, H), BG + (255,))
    surface, path_px = render_surface()
    base.alpha_composite(surface)

    # dark oval behind the title so it reads over the surface
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).ellipse([W / 2 - 900, H / 2 - 330, W / 2 + 900, H / 2 + 330], fill=215)
    shade = shade.filter(ImageFilter.GaussianBlur(120))
    base.paste(Image.new("RGBA", (W, H), BG + (255,)), (0, 0), shade)

    draw_path(base, path_px)

    d = ImageDraw.Draw(base)
    title = "ML From Scratch"
    f = ImageFont.truetype(FONTS + "DejaVuSans-Bold.ttf", 140)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2 + 5, H / 2 - 165 + 6), title, font=f, fill=(0, 0, 0, 160))  # soft drop shadow
    d.text(((W - tw) / 2, H / 2 - 165), title, font=f, fill=FG)
    d.rectangle([W / 2 - 95, H / 2 + 10, W / 2 + 95, H / 2 + 17], fill=TEAL)
    sub = "One algorithm a week  ·  Python + NumPy"
    f2 = ImageFont.truetype(FONTS + "DejaVuSans.ttf", 54)
    sw = d.textlength(sub, font=f2)
    d.text(((W - sw) / 2, H / 2 + 45), sub, font=f2, fill=ACC)

    base.convert("RGB").save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
