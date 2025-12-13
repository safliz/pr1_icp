import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def make_receipt(cart, total_sum):
    template_path = "чек.png"

    if not os.path.exists(template_path):
        raise FileNotFoundError("Файл шаблона чека не найден!")

    # ---------- загрузка шаблона ----------
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # ---------- шрифты с поддержкой кириллицы ----------
    try:
        # Укажите путь к шрифту с русскими буквами, если нужно другой
        font = ImageFont.truetype("C:/Windows/Fonts/DejaVuSans.ttf", 25)  
        font_bold = ImageFont.truetype("C:/Windows/Fonts/DejaVuSans-Bold.ttf", 30)
    except:
        font = ImageFont.load_default()
        font_bold = font

    text_color = (40, 40, 40)

    # ---------- начальные координаты ----------
    x = 40
    y = 800
    line = 40

    # ---------- дата ----------
    draw.text(
        (x, y),
        datetime.now().strftime("Дата: %d.%m.%Y  %H:%M"),
        fill=text_color,
        font=font
    )
    y += line * 2

    # ---------- товары ----------
    for (name, storage), info in cart.items():
        qty = info['Количество']
        price = info['Цена']
        s = qty * price

        draw.text((x, y), f'{name}. . . . . {qty}шт x {price}руб = {s}руб', fill=text_color, font=font)
        y += line

        draw.text(
            (x + 20, y),
            f"Склад: {storage}",
            fill=text_color,
            font=font
        )
        y += int(line * 1.5)

    # ---------- итог ----------
    y += 10
    draw.line((x, y, img.width - x, y), fill=text_color, width=4)
    y += line

    draw.text(
        (x, y),
        f"ИТОГО: {total_sum}",
        fill=text_color,
        font=font_bold
    )

    # ---------- сохранение ----------
    filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(filename)

    return filename
