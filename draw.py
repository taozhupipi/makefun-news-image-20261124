"""Draw the 24 November 2026 world-news summary image.

Reads nothing but its own constants: every story is baked into STORIES
below, so the program runs with no network and is fully deterministic.
Usage: python3 draw.py [output_path]  (default: entry.png next to this file)
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette ----
PAPER = (246, 241, 231)      # warm off-white page
INK = (28, 39, 51)           # near-black for headlines
MUTED = (90, 101, 114)       # grey for summaries and footer
CARD = (255, 255, 255)
CARD_LINE = (227, 220, 203)
BAND = (22, 35, 63)          # deep navy header band
GOLD = (232, 169, 61)        # header rule and subtitle
RULE = (232, 169, 61)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
PLAIN = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# ---- the eight stories: tag, tag colour, headline, summary, glyph ----
STORIES = [
    ("TECH · USA", (62, 124, 58), "Nvidia rally fades",
     "Shares slide 6% a day after Huang's return; the CEO admits a conduct breach.",
     "chip"),
    ("USA · TRADE", (43, 94, 167), "New US tariffs loom",
     "Trump is poised to unveil duties after a probe of excess capacity in 16 partners.",
     "bank"),
    ("UKRAINE · WAR", (122, 74, 158), "Strike kills 2 in Zaporizhzhia",
     "An overnight Russian attack hits flats; 40 are wounded, among them four children.",
     "shield"),
    ("MIDDLE EAST · WAR", (179, 55, 47), "Hamas security chief killed",
     "Israeli strikes kill Naeem Abu Nahel in Gaza; six others are also dead.",
     "compass"),
    ("USA · SECURITY", (15, 118, 110), "CIA hit by cyberattack",
     "CIA and another US spy agency breached; officials say key systems are safe.",
     "lock"),
    ("UK · ECONOMY", (154, 107, 15), "UK energy bills to jump 26%",
     "Household bills are forecast to rise about £443 a year from January.",
     "bolt"),
    ("AFRICA · MIGRATION", (74, 85, 104), "175 migrants missing off Senegal",
     "Contact is lost with a Europe-bound boat that left Dakar two weeks ago.",
     "boat"),
    ("CHINA · TECH", (155, 44, 44), "Huawei convicted in US trial",
     "A jury finds corporate espionage and sanctions evasion.",
     "scales"),
]

FOOTER = "Sources: Reuters  ·  BBC  ·  CBS  ·  FT  ·  Just Security"


def font(size, bold=False):
    """Load a DejaVu face; fall back to Pillow's built-in bitmap font."""
    try:
        return ImageFont.truetype(BOLD if bold else PLAIN, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tint(rgb, frac=0.13):
    """Mix a colour toward white to make a pale tint for icon discs."""
    return tuple(round(c + (255 - c) * frac) for c in rgb)


def pill(draw, x, y, label, fill):
    """A small rounded tag with white bold text; returns its width."""
    fnt = font(19, bold=True)
    tw = draw.textlength(label, font=fnt)
    pad_x, h = 11, 29
    draw.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + h], radius=h // 2,
                           fill=fill)
    draw.text((x + pad_x, y + 5), label, font=fnt, fill=(255, 255, 255))
    return tw + 2 * pad_x


def glyph(draw, kind, cx, cy, r, colour):
    """Draw one small pictogram centred at (cx, cy), inside radius r.

    Every glyph is built from plain Pillow primitives (rectangles,
    ellipses, polygons, lines) so the drawing stays deterministic.
    """
    s = r  # half-size of the glyph's bounding box
    if kind == "chip":
        draw.rectangle([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45,
                        cy + s * 0.45], outline=colour, width=4)
        draw.rectangle([cx - s * 0.18, cy - s * 0.18, cx + s * 0.18,
                        cy + s * 0.18], fill=colour)
        for dx in (-1, 0, 1):
            draw.line([cx + dx * s * 0.28, cy - s * 0.72,
                       cx + dx * s * 0.28, cy - s * 0.45], fill=colour,
                      width=3)
            draw.line([cx + dx * s * 0.28, cy + s * 0.45,
                       cx + dx * s * 0.28, cy + s * 0.72], fill=colour,
                      width=3)
            draw.line([cx - s * 0.72, cy + dx * s * 0.28,
                       cx - s * 0.45, cy + dx * s * 0.28], fill=colour,
                      width=3)
            draw.line([cx + s * 0.45, cy + dx * s * 0.28,
                       cx + s * 0.72, cy + dx * s * 0.28], fill=colour,
                      width=3)
    elif kind == "bank":
        draw.polygon([(cx - s * 0.7, cy - s * 0.1), (cx, cy - s * 0.65),
                      (cx + s * 0.7, cy - s * 0.1)], fill=colour)
        for dx in (-0.5, 0, 0.5):
            draw.rectangle([cx + dx * s - s * 0.09, cy + s * 0.05,
                            cx + dx * s + s * 0.09, cy + s * 0.55],
                           fill=colour)
        draw.rectangle([cx - s * 0.7, cy + s * 0.55, cx + s * 0.7,
                        cy + s * 0.68], fill=colour)
    elif kind == "shield":
        draw.polygon([(cx - s * 0.55, cy - s * 0.5), (cx + s * 0.55,
                      cy - s * 0.5), (cx + s * 0.55, cy + s * 0.05),
                      (cx, cy + s * 0.7), (cx - s * 0.55, cy + s * 0.05)],
                     outline=colour, width=4)
        draw.line([cx - s * 0.28, cy + s * 0.02, cx - s * 0.05,
                   cy + s * 0.28], fill=colour, width=4)
        draw.line([cx - s * 0.05, cy + s * 0.28, cx + s * 0.32,
                   cy - s * 0.3], fill=colour, width=4)
    elif kind == "compass":
        draw.ellipse([cx - s * 0.6, cy - s * 0.6, cx + s * 0.6,
                      cy + s * 0.6], outline=colour, width=4)
        draw.polygon([(cx, cy - s * 0.5), (cx + s * 0.16, cy),
                      (cx, cy + s * 0.5), (cx - s * 0.16, cy)],
                     fill=colour)
    elif kind == "lock":
        draw.rounded_rectangle([cx - s * 0.5, cy - s * 0.05, cx + s * 0.5,
                                cy + s * 0.6], radius=6, outline=colour,
                               width=4)
        draw.arc([cx - s * 0.32, cy - s * 0.62, cx + s * 0.32,
                  cy + s * 0.15], start=180, end=360, fill=colour, width=4)
        draw.ellipse([cx - 4, cy + s * 0.2, cx + 4, cy + s * 0.28],
                     fill=colour)
    elif kind == "bolt":
        draw.polygon([(cx + s * 0.15, cy - s * 0.7), (cx - s * 0.35,
                      cy + s * 0.08), (cx - s * 0.02, cy + s * 0.08),
                      (cx - s * 0.15, cy + s * 0.7), (cx + s * 0.35,
                      cy - s * 0.08), (cx + s * 0.02, cy - s * 0.08)],
                     fill=colour)
    elif kind == "boat":
        draw.polygon([(cx - s * 0.6, cy + s * 0.1), (cx + s * 0.6,
                      cy + s * 0.1), (cx + s * 0.35, cy + s * 0.55),
                      (cx - s * 0.35, cy + s * 0.55)], fill=colour)
        draw.polygon([(cx - s * 0.05, cy - s * 0.65), (cx - s * 0.05,
                      cy + s * 0.02), (cx + s * 0.5, cy + s * 0.02)],
                     fill=colour)
        draw.line([cx - s * 0.05, cy - s * 0.65, cx - s * 0.05,
                   cy + s * 0.02], fill=colour, width=3)
    elif kind == "scales":
        draw.line([cx, cy - s * 0.6, cx, cy + s * 0.55], fill=colour,
                  width=4)
        draw.line([cx - s * 0.55, cy - s * 0.45, cx + s * 0.55,
                   cy - s * 0.45], fill=colour, width=4)
        draw.polygon([(cx - s * 0.55, cy - s * 0.45), (cx - s * 0.28,
                      cy + s * 0.1), (cx - s * 0.55 + s * 0.54,
                      cy + s * 0.1)], fill=colour)
        draw.polygon([(cx + s * 0.55, cy - s * 0.45), (cx + s * 0.28,
                      cy + s * 0.1), (cx + s * 0.55 - s * 0.54,
                      cy + s * 0.1)], fill=colour)
        draw.line([cx - s * 0.3, cy + s * 0.55, cx + s * 0.3,
                   cy + s * 0.55], fill=colour, width=4)


def card(draw, x, y, w, h, story):
    """One news card: tag pill, headline, summary, glyph disc top-right."""
    tag, colour, headline, summary, kind = story
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD,
                           outline=CARD_LINE, width=2)
    pad = 20
    # Glyph disc top-right; the headline is kept clear of its column.
    disc_r = 27
    disc_cx = x + w - pad - disc_r
    disc_cy = y + 16 + disc_r
    draw.ellipse([disc_cx - disc_r, disc_cy - disc_r, disc_cx + disc_r,
                  disc_cy + disc_r], fill=tint(colour, 0.85))
    glyph(draw, kind, disc_cx, disc_cy, 17, colour)
    # Tag pill top-left.
    pill(draw, x + pad, y + 16, tag, colour)
    # Headline: bold, at most two lines, never under the disc.
    head_fnt = font(30, bold=True)
    head_w = w - 2 * pad - (2 * disc_r + 14)
    head_lines = wrap(draw, headline, head_fnt, head_w)[:2]
    ty = y + 54
    for line in head_lines:
        draw.text((x + pad, ty), line, font=head_fnt, fill=INK)
        ty += 36
    # Summary: regular, full card width; two lines max under a two-line
    # headline so the text never runs past the card's bottom edge.
    sum_fnt = font(20)
    sum_max = 3 if len(head_lines) == 1 else 2
    sum_lines = wrap(draw, summary, sum_fnt, w - 2 * pad)[:sum_max]
    sy = ty + 6
    for line in sum_lines:
        draw.text((x + pad, sy), line, font=sum_fnt, fill=MUTED)
        sy += 28


def header(draw):
    """Navy band with the date and the subtitle, plus a gold rule."""
    band_h = 118
    draw.rectangle([0, 0, W, band_h], fill=BAND)
    date_fnt = font(56, bold=True)
    date = "TUESDAY 24 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_fnt)
    draw.text(((W - dw) / 2, 24), date, font=date_fnt, fill=(255, 255, 255))
    sub_fnt = font(23, bold=True)
    sub = "THE WORLD TODAY · EIGHT STORIES"
    sw = draw.textlength(sub, font=sub_fnt)
    draw.text(((W - sw) / 2, 86), sub, font=sub_fnt, fill=GOLD)
    draw.rectangle([0, band_h, W, band_h + 4], fill=RULE)


def build():
    """Assemble the whole poster and return the image."""
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    header(draw)
    margin, gap = 24, 16
    top = 140
    card_w = (W - 2 * margin - gap) // 2
    card_h = (H - top - 40 - 3 * gap) // 4
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        cx = margin + col * (card_w + gap)
        cy = top + row * (card_h + gap)
        card(draw, cx, cy, card_w, card_h, story)
    foot_fnt = font(18)
    fw = draw.textlength(FOOTER, font=foot_fnt)
    draw.text(((W - fw) / 2, H - 30), FOOTER, font=foot_fnt, fill=MUTED)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
