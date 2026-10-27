"""Deterministically resize supplied artwork; never redraw brand marks."""
from pathlib import Path
from shutil import copyfile
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'kendal-king': (ROOT / 'assets/kendal_king_large2-72 ppi.png', 119),
    'soapbox': (Path.home() / 'Downloads/SB Logo_Square.png', 125),
    'kkg': (Path.home() / 'Downloads/KKG Inc. Email Signature_Transparent.png', 120),
    'soapbox-studio': (Path.home() / 'Downloads/SoapboxStudio_EmailSignature.png', 138),
}

def main():
    originals = ROOT / 'assets/originals'
    prepared = ROOT / 'assets/prepared'
    originals.mkdir(exist_ok=True)
    prepared.mkdir(exist_ok=True)
    sheet = Image.new('RGB', (360 * len(SOURCES), 400), '#eef2f6')
    draw = ImageDraw.Draw(sheet)
    for index, (key, (source, width)) in enumerate(SOURCES.items()):
        version = 'v2' if key == 'kendal-king' else 'v1'
        original = originals / f'{key}-{version}.png' if key == 'kendal-king' else originals / f'{key}.png'
        if not original.exists():
            copyfile(source, original)
        image = Image.open(original).convert('RGBA')
        image = image.crop(image.getchannel('A').getbbox())
        height = round(image.height * width / image.width)
        # Never invent resolution beyond the source artwork.
        export_width = min(width * 2, image.width)
        image = image.resize((export_width, round(image.height * export_width / image.width)), Image.Resampling.LANCZOS)
        image.save(prepared / f'{key}-{version}.png')
        print(key, width, height)
        x = index * 360
        draw.text((x + 24, 18), f'{key}: {width} x {height} display px', fill='#172b46')
        for top, background in [(50, 'white'), (225, '#252a34')]:
            draw.rectangle((x + 12, top, x + 348, top + 165), fill=background)
            display = image.resize((width, height), Image.Resampling.LANCZOS)
            sheet.paste(display, (x + (360-width)//2, top + (165-height)//2), display)
    sheet.save(ROOT / 'assets/logo-comparison.png')

if __name__ == '__main__':
    main()
