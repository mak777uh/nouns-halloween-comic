#!/usr/bin/env python3
r"""nouns_halloween.py — 4-панельный комикс с пиксельными Nouns (CC0), нарисованный кодом.

Сюжет: пиксельный Noun идёт за конфетами, дверь открывает «монстр», герой отдаёт свою конфету…
и в последней панели выясняется, что монстр — это ребёнок в маске, а конфета была нужна ему,
чтобы не идти домой. Твист читается визуально: в 4-й панели маска снята и лежит рядом.

Всё рисуется попиксельно (сетка 32×32 на панель) и масштабируется без сглаживания.
"""
from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(r"C:\111\work\comic")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 32, 32
SCALE = 16
PAD = 22

BG = (212, 214, 255)
DARK = (18, 18, 26)
SKIN = (255, 216, 163)
SKIN2 = (222, 176, 128)
WHITE = (255, 255, 255)
ORANGE = (245, 130, 32)
PURPLE = (108, 56, 150)
GREEN = (70, 170, 95)
GREY = (150, 150, 160)
GREY2 = (120, 120, 132)
RED = (196, 46, 46)
YELLOW = (255, 208, 60)
PAPER = (247, 245, 240)


def rect(px, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            px[x, y] = color


def noun(px, x, y, body=ORANGE, hair=None, tall=False, dead=False, mask_off=False):
    hh = 13 if tall else 12
    rect(px, x + 2, y + hh, x + 11, y + hh + 8, body)          # тело
    rect(px, x + 4, y + hh + 8, x + 6, y + hh + 11, body)      # ноги
    rect(px, x + 8, y + hh + 8, x + 10, y + hh + 11, body)
    rect(px, x + 1, y + 2, x + 12, y + hh, SKIN)               # голова
    rect(px, x + 3, y + 5, x + 6, y + 8, WHITE)                # очки
    rect(px, x + 8, y + 5, x + 11, y + 8, WHITE)
    rect(px, x + 3, y + 5, x + 4, y + 6, DARK)
    rect(px, x + 8, y + 5, x + 9, y + 6, DARK)
    rect(px, x + 6, y + 6, x + 8, y + 7, DARK)
    rect(px, x + 6, y + 9, x + 9, y + 10, DARK) if not dead else rect(px, x + 6, y + 9, x + 11, y + 10, DARK)
    if hair:
        rect(px, x + 1, y, x + 12, y + 2, hair)
    return


def candy(px, x, y, color=RED):
    rect(px, x, y, x + 3, y + 3, color)
    rect(px, x + 3, y + 1, x + 4, y + 2, WHITE)


def panel_door(px):
    rect(px, 0, 28, 32, 32, GREY)
    rect(px, 0, 27, 32, 28, GREY2)
    rect(px, 17, 6, 32, 28, PURPLE)          # дом
    rect(px, 19, 10, 28, 27, DARK)           # дверной проём
    rect(px, 25, 16, 27, 18, YELLOW)         # ручка
    noun(px, 2, 9, body=ORANGE)
    candy(px, 13, 20, RED)                   # конфета в руке


def panel_open(px):
    rect(px, 0, 28, 32, 32, GREY)
    rect(px, 0, 27, 32, 28, GREY2)
    rect(px, 17, 6, 32, 28, PURPLE)
    rect(px, 19, 10, 28, 27, (30, 26, 38))   # темнота в проёме
    noun(px, 1, 9, body=ORANGE)
    candy(px, 12, 20, RED)
    # «монстр»: зелёная голова с прорезями глаз
    rect(px, 20, 12, 27, 20, GREEN)
    rect(px, 21, 14, 23, 16, DARK)
    rect(px, 24, 14, 26, 16, DARK)
    rect(px, 21, 18, 26, 19, DARK)           # рот
    rect(px, 22, 17, 23, 18, DARK)


def panel_candy(px):
    rect(px, 0, 28, 32, 32, GREY)
    rect(px, 0, 27, 32, 28, GREY2)
    rect(px, 17, 6, 32, 28, PURPLE)
    rect(px, 19, 10, 28, 27, (30, 26, 38))
    noun(px, 1, 9, body=ORANGE)
    rect(px, 12, 17, 15, 20, RED)            # протянутая конфета
    rect(px, 15, 18, 16, 19, WHITE)
    rect(px, 20, 12, 27, 20, GREEN)
    rect(px, 21, 14, 23, 16, DARK)
    rect(px, 24, 14, 26, 16, DARK)
    rect(px, 21, 18, 26, 19, YELLOW)         # улыбка


def panel_twist(px):
    rect(px, 0, 28, 32, 32, GREY)
    rect(px, 0, 27, 32, 28, GREY2)
    rect(px, 20, 4, 32, 27, PURPLE)          # дом сдвинут вправо, чтобы освободить место
    rect(px, 22, 8, 29, 26, (30, 26, 38))
    noun(px, 0, 10, body=ORANGE)             # герой
    noun(px, 10, 10, body=GREEN)             # «монстр» без маски — обычный Noun
    candy(px, 8, 21, RED)                    # конфеты в руках
    candy(px, 16, 21, RED)
    # маска снята и лежит на земле отдельно от персонажей
    rect(px, 25, 22, 31, 27, GREEN)
    rect(px, 26, 23, 27, 24, DARK)
    rect(px, 28, 23, 29, 24, DARK)
    rect(px, 26, 25, 29, 26, DARK)


def sheet() -> pathlib.Path:
    panels = [(panel_door, "1. TRICK"), (panel_open, "2. OR TREAT?"),
              (panel_candy, "3. HERE — TAKE MINE"), (panel_twist, "4. …IT WAS A KID IN A MASK")]
    PW, PH = W * SCALE, H * SCALE
    title_h, cap_h = 132, 54
    total_w = PAD * 2 + PW * 2 + 12
    total_h = title_h + (PH + cap_h) * 2 + 96
    sh = Image.new("RGB", (total_w, total_h), PAPER)
    d = ImageDraw.Draw(sh)
    f_big = ImageFont.truetype(r"C:\Windows\Fonts\ariblk.ttf", 52)
    f_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 24)
    f_cap = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 27)
    f_foot = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 19)

    d.text((PAD, 26), "TRICK OR TREAT", font=f_big, fill=DARK)
    d.text((PAD, 92), "a four-panel comic · characters: CC0 pixel Nouns · drawn in code", font=f_sub, fill=(105, 105, 115))

    for i, (fn, caption) in enumerate(panels):
        img = Image.new("RGB", (W, H), BG)
        fn(img.load())
        img = img.resize((PW, PH), Image.NEAREST)
        col, row = i % 2, i // 2
        x = PAD + col * (PW + 12)
        y = title_h + row * (PH + cap_h)
        sh.paste(img, (x, y))
        d.rectangle([x, y, x + PW - 1, y + PH - 1], outline=DARK, width=4)
        d.text((x + 2, y + PH + 12), caption, font=f_cap, fill=DARK)

    d.line([PAD, total_h - 60, total_w - PAD, total_h - 60], fill=(200, 200, 205), width=2)
    d.text((PAD, total_h - 46),
           "Dedicated to the public domain under CC0 1.0. Every character is a CC0 pixel Noun; the code is CC0 too.",
           font=f_foot, fill=(105, 105, 115))
    out = OUT / "nouns-halloween-4panel.png"
    sh.save(out)
    print("готово:", out, sh.size)
    return out


if __name__ == "__main__":
    sheet()
