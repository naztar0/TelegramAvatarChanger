import logging
import os
import random
import colorsys
from io import BytesIO
from pathlib import Path
from PIL import Image
from app import CONFIG


PARTS = (
    'head_hair',
    'body_bottoms',
    'body_tops',
    'main_expressions',
    'face_facial_hair',
    'face_eyes',
    'face_accessories',
    'face_coverings',
    'body_left_hand_accessories',
    'body_right_hand_accessories',
    'full_body_outfits',
    'face_makeup',
    'head_accessories',
)

SIZE = 380, 600
WHITE = (255, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)
ASSETS_PATH = Path('assets/snoo_v2')
BG_PATH = Path('assets/backgrounds')

CHROMA_KEYS = {
    'body_bottoms': WHITE,
    'body_tops': WHITE,
    'main_expressions': WHITE,
    'face_facial_hair': WHITE,
    'face_makeup': WHITE,
    'face_eyes': TRANSPARENT,
    'body_left_hand_accessories': WHITE,
    'body_right_hand_accessories': WHITE,
}

config = CONFIG.get()['snoo']


def chroma_key(img, col=TRANSPARENT):
    new_data = []
    for item in img.getdata():
        percents = (item[0] / 255, item[1] / 255, item[2] / 255)
        green_percent = percents[1] / ((percents[0] + percents[1] + percents[2]) or 1)
        value = max(percents)
        if green_percent > 0.8:
            color_mix_r = int((item[0] * (1 - green_percent) + col[0] * green_percent) * value)
            color_mix_g = int((item[1] * (1 - green_percent) + col[1] * green_percent) / (2 - green_percent) * value)
            color_mix_b = int((item[2] * (1 - green_percent) + col[2] * green_percent) * value)
            color_mix_a = int((item[3] * (1 - green_percent) + col[3] * green_percent))
            new_data.append((color_mix_r, color_mix_g, color_mix_b, color_mix_a))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def rand_color():
    hue = random.randrange(0, 360) / 360
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(hue, 0.6, 1))


def rand_file(path: Path) -> str:
    return path / random.choice([name for name in os.listdir(path)])


def to_square_avatar(img):
    s, vertical_offset = 520, 35
    new_img = Image.new('RGBA', (s, s), rand_color())
    bg = Image.open(rand_file(BG_PATH))
    bg.putalpha(config['bg_alpha'] * 255 // 100)
    new_img.alpha_composite(bg)
    new_img.alpha_composite(img, ((s - SIZE[0]) // 2, (s - SIZE[1]) // 2 - vertical_offset))
    return new_img


def generate_asset(part: str, weight=0.5):
    def enabled():
        if option is not None:
            if isinstance(option, bool):
                return option
            if isinstance(option, str):
                return random.random() < weight
        return random.random() < weight
    option = config.get(part)
    if isinstance(option, int) and not isinstance(option, bool):
        return ASSETS_PATH / part / f'{option}.png'
    if enabled():
        return rand_file(ASSETS_PATH / part)
    return None


async def generate(to_file: str = None, iformat='PNG'):
    result = Image.new('RGBA', SIZE, TRANSPARENT)

    for part in PARTS:
        img = generate_asset(part)
        if img:
            img = Image.open(img)
            if part in CHROMA_KEYS:
                logging.info(f'Chroma keying {part}')
                img = chroma_key(img, CHROMA_KEYS[part])
            logging.info(f'File: {img.filename}')
            result.alpha_composite(img)

    result = to_square_avatar(result)
    if to_file:
        result.save(to_file, iformat)
        return
    buffer = BytesIO()
    result.save(buffer, iformat)
    buffer.seek(0)
    return buffer


__all__ = ['generate']
