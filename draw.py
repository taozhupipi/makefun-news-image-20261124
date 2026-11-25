#!/usr/bin/env python3
"""Draw entry.png: a 1024x1024 infographic summing up the world news of
Tuesday 24 November 2026. Eight stories in a two-by-four grid, drawn
entirely with Pillow primitives; nothing is downloaded or copied in.

Every fact on the image was verified against reporting published on
24 November 2026 (Reuters, BBC, CBS, FT, Just Security).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (247, 244, 238)          # warm paper
NAVY = (16, 32, 58)           # header
GOLD = (214, 164, 58)         # header accent
PANEL = (255, 255, 255)
PANEL_EDGE = (226, 219, 203)
INK = (18, 30, 56)            # headline
BODY = (64, 70, 84)           # body text
MUTED = (122, 117, 104)

HEADER_H = 124
FOOTER_H = 26
MARGIN = 16
GAP = 12
GRID_TOP = HEADER_H + MARGIN
GRID_BOTTOM = H - MARGIN - FOOTER_H - 8
PANEL_W = (W - 2 * MARGIN - GAP) // 2                    # 490
PANEL_H = (GRID_BOTTOM - GRID_TOP - 3 * GAP) // 4        # 199
# Headlines stop short of the icon column at the panel's top right,
# so no letter can ever sit under an icon.
HEAD_W = PANEL_W - 36 - 84
BODY_W = PANEL_W - 36

# (tag, tag colour, headline, body, icon)
STORIES = [
    ("TECH \u00b7 USA", (99, 151, 0),
     "Nvidia rally fades",
     "Shares slide 6% a day after Huang's return; the CEO admits a "
     "conduct breach.",
     "chip"),
    ("USA \u00b7 TRADE", (29, 78, 216),
     "New US tariffs loom",
     "Trump is poised to unveil duties after a probe of excess "
     "capacity in 16 partners.",
     "box"),
    ("UKRAINE \u00b7 WAR", (109, 48, 130),
     "Strike kills 2 in Zaporizhzhia",
     "An overnight Russian attack hits flats; 40 are wounded, among "
     "them four children.",
     "shield"),
    ("MIDDLE EAST \u00b7 WAR", (185, 28, 28),
     "Hamas security chief killed",
     "Israeli strikes kill Naeem Abu Nahel in Gaza; six others are "
     "also dead.",
     "rocket"),
    ("USA \u00b7 SECURITY", (0, 121, 121),
     "CIA hit by cyberattack",
     "The CIA and another US spy agency are breached; officials say "
     "key systems are safe.",
     "lock"),
    ("UK \u00b7 ECONOMY", (176, 124, 8),
     "UK energy bills to jump 26%",
     "Household bills are forecast to rise about \u00a3443 a year from "
     "January.",
     "bolt"),
    ("AFRICA \u00b7 MIGRATION", (71, 85, 105),
     "175 migrants missing off Senegal",
     "Contact is lost with a Europe-bound boat that left Dakar two "
     "weeks ago.",
     "boat"),
    ("CHINA \u00b7 TECH", (146, 46, 46),
     "Huawei convicted in US trial",
     "A jury finds corporate espionage and sanctions evasion.",
     "gavel"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns lines that each fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, cx, cy, kind, color):
    """Simple pictogram inside a tinted circle centred at (cx, cy)."""
    r = 28
    tint = tuple(min(255, c + 200) for c in color)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tint)
    if kind == "chip":
        d.rectangle([cx - 13, cy - 13, cx + 13, cy + 13],
                    outline=color, width=4)
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)
        for dx in (-8, 0, 8):
            d.line([cx + dx, cy - 19, cx + dx, cy - 13], fill=color, width=3)
            d.line([cx + dx, cy + 13, cx + dx, cy + 19], fill=color, width=3)
            d.line([cx - 19, cy + dx, cx - 13, cy + dx], fill=color, width=3)
            d.line([cx + 13, cy + dx, cx + 19, cy + dx], fill=color, width=3)
    elif kind == "box":
        # shipping box with a tape cross
        d.rectangle([cx - 15, cy - 11, cx + 15, cy + 13],
                    outline=color, width=4)
        d.line([cx, cy - 11, cx, cy + 13], fill=color, width=3)
        d.line([cx - 15, cy + 1, cx + 15, cy + 1], fill=color, width=3)
        d.polygon([(cx - 15, cy - 11), (cx - 7, cy - 18),
                   (cx + 7, cy - 18), (cx + 15, cy - 11)], fill=color)
    elif kind == "shield":
        d.polygon([(cx, cy - 16), (cx + 14, cy - 10), (cx + 14, cy + 2),
                   (cx, cy + 17), (cx - 14, cy + 2), (cx - 14, cy - 10)],
                  outline=color, width=4)
        d.line([cx - 6, cy + 1, cx - 1, cy + 6], fill=color, width=4)
        d.line([cx - 1, cy + 6, cx + 8, cy - 6], fill=color, width=4)
    elif kind == "rocket":
        import math
        ux, uy = 0.7071, -0.7071   # nose direction
        vx, vy = 0.7071, 0.7071    # perpendicular
        nx, ny = cx + 14 * ux, cy + 14 * uy
        bx, by = cx - 8 * ux, cy - 8 * uy
        w = 5
        d.polygon([(nx, ny),
                   (bx + w * vx, by + w * vy),
                   (bx - w * vx, by - w * vy)], fill=color)
        d.polygon([(bx + w * vx, by + w * vy),
                   (bx - 4 * ux + 8 * vx, by - 4 * uy + 8 * vy),
                   (bx - 2 * ux, by - 2 * uy)], fill=color)
        d.polygon([(bx - w * vx, by - w * vy),
                   (bx - 4 * ux - 8 * vx, by - 4 * uy - 8 * vy),
                   (bx - 2 * ux, by - 2 * uy)], fill=color)
        fx, fy = bx - 2 * ux, by - 2 * uy
        d.polygon([(fx + 4 * vx, fy + 4 * vy),
                   (fx - 10 * ux, fy - 10 * uy),
                   (fx - 4 * vx, fy - 4 * vy)], fill=(234, 88, 12))
    elif kind == "lock":
        d.rounded_rectangle([cx - 13, cy - 2, cx + 13, cy + 16], radius=4,
                            outline=color, width=4)
        d.arc([cx - 8, cy - 14, cx + 8, cy + 2], 180, 360, fill=color,
              width=4)
        d.ellipse([cx - 3, cy + 4, cx + 3, cy + 10], fill=color)
    elif kind == "bolt":
        d.polygon([(cx + 4, cy - 18), (cx - 9, cy + 2), (cx - 1, cy + 2),
                   (cx - 4, cy + 18), (cx + 9, cy - 3), (cx + 1, cy - 3)],
                  fill=color)
    elif kind == "boat":
        # hull, mast and sail
        d.line([cx, cy - 16, cx, cy + 6], fill=color, width=4)
        d.polygon([(cx + 2, cy - 15), (cx + 2, cy + 4), (cx + 13, cy + 4)],
                  fill=color)
        d.polygon([(cx - 16, cy + 6), (cx + 16, cy + 6),
                   (cx + 11, cy + 16), (cx - 11, cy + 16)], fill=color)
        d.arc([cx - 18, cy + 12, cx + 18, cy + 22], 0, 180, fill=color,
              width=3)
    elif kind == "gavel":
        # gavel head and handle, diagonal
        d.line([cx - 12, cy + 12, cx + 12, cy - 12], fill=color, width=5)
        d.rectangle([cx - 14, cy - 14, cx - 4, cy - 4], fill=color)
        d.rectangle([cx + 4, cy + 4, cx + 14, cy + 14], fill=color)
        d.line([cx - 16, cy + 16, cx + 16, cy + 16], fill=color, width=3)


def draw_panel(d, x, y, story):
    tag, color, headline, body, icon = story
    d.rounded_rectangle([x, y, x + PANEL_W, y + PANEL_H], radius=14,
                        fill=PANEL, outline=PANEL_EDGE, width=2)
    px, py = x + 18, y + 14
    # tag pill
    tag_f = font(BOLD, 19)
    tw = d.textlength(tag, font=tag_f)
    d.rounded_rectangle([px, py, px + tw + 20, py + 26], radius=13,
                        fill=color)
    d.text((px + 10, py + 3), tag, font=tag_f, fill=(255, 255, 255))
    # icon, top right, clear of the headline column
    draw_icon(d, x + PANEL_W - 46, y + 40, icon, color)
    # headline, up to two lines, kept out of the icon column
    head_f = font(BOLD, 28)
    lines = wrap(d, headline, head_f, HEAD_W)[:2]
    hy = y + 48
    for line in lines:
        d.text((px, hy), line, font=head_f, fill=INK)
        hy += 32
    # body, up to three lines, full panel width
    body_f = font(REG, 20)
    blines = wrap(d, body, body_f, BODY_W)[:3]
    by = y + 48 + 32 * len(lines) + 4
    for line in blines:
        d.text((px, by), line, font=body_f, fill=BODY)
        by += 24


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W, HEADER_H], fill=NAVY)
    d.rectangle([0, HEADER_H - 6, W, HEADER_H], fill=GOLD)
    title_f = font(BOLD, 54)
    title = "TUESDAY 24 NOVEMBER 2026"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 16), title, font=title_f, fill=(255, 255, 255))
    sub_f = font(BOLD, 23)
    sub = "T H E   W O R L D   T O D A Y   \u00b7   E I G H T   S T O R I E S"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 82), sub, font=sub_f, fill=GOLD)
    # grid
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = MARGIN + col * (PANEL_W + GAP)
        y = GRID_TOP + row * (PANEL_H + GAP)
        draw_panel(d, x, y, story)
    # footer: sources
    foot_f = font(REG, 16)
    foot = ("Sources: Reuters  \u00b7  BBC  \u00b7  CBS  \u00b7  FT  "
            "\u00b7  Just Security")
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, H - FOOTER_H - 2), foot, font=foot_f, fill=MUTED)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
