"""Company presets and reusable HTML rendering, independent of Streamlit."""
from dataclasses import dataclass
from html import escape
from pathlib import Path
import base64
import re
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent
ADDRESS = '609 SW 8th St #140 - Bentonville, AR'

@dataclass(frozen=True)
class Preset:
    label: str
    filename: str
    width: int
    height: int
    websites: tuple[str, ...]
    logo_link: str | None
    address: str = ADDRESS

PRESETS = {
    'soapbox': Preset('Soapbox', 'soapbox-v1.png', 125, 79, ('www.soapboxretail.com',), 'https://www.soapboxretail.com'),
    'kendal-king': Preset('Kendal King', 'kendal-king-v2.png', 119, 126, ('www.kendalking.com',), 'https://www.kendalking.com'),
    'kkg': Preset('KKG Inc.', 'kkg-v1.png', 120, 128, ('www.kendalking.com', 'www.soapboxretail.com'), None),
    'soapbox-studio': Preset('Soapbox Photo Studio', 'soapbox-studio-v1.png', 138, 109, ('www.soapboxretail.com',), 'https://www.soapboxretail.com', '2503 SE J St. #15 - Bentonville, Arkansas'),
}

def validate(name, title, email, phone):
    errors = []
    for label, value in [('Full name', name), ('Job title', title)]:
        if not value.strip():
            errors.append(f'{label} is required.')
    if not re.fullmatch(r'[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+', email.strip()):
        errors.append('Enter a valid email address.')
    if phone.strip() and (not re.fullmatch(r'[+\d().\s-]+', phone.strip()) or len(re.sub(r'\D', '', phone)) < 7):
        errors.append('Enter a complete phone number using digits, spaces, +, parentheses, or hyphens, or leave it blank.')
    return errors

def image_source(preset, asset_base_url=''):
    if not asset_base_url:
        data = (ROOT / 'assets/prepared' / preset.filename).read_bytes()
        return 'data:image/png;base64,' + base64.b64encode(data).decode('ascii')
    parsed = urlsplit(asset_base_url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('SIGNATURE_ASSET_BASE_URL must be an HTTPS directory URL without credentials, query, or fragment.')
    return asset_base_url.rstrip('/') + '/' + preset.filename

def render_signature(key, name, title, email, phone='', asset_base_url=''):
    preset = PRESETS[key]
    esc = lambda value: escape(value.strip(), quote=True)
    image = (f'<img src="{esc(image_source(preset, asset_base_url))}" alt="{esc(preset.label)}" '
             f'width="{preset.width}" height="{preset.height}" '
             f'style="display:block;width:{preset.width}px;height:{preset.height}px;border:0;">')
    if preset.logo_link:
        image = f'<a href="{esc(preset.logo_link)}" style="text-decoration:none;">{image}</a>'
    link_style = 'font-family:Arial,sans-serif;font-size:12px;color:#000000 !important;text-decoration:none !important;'
    items = [f'<strong style="font-family:Arial,sans-serif;font-size:14px;color:#000000;">{esc(name)}</strong>', f'<strong style="font-size:12px;">{esc(title)}</strong>']
    if phone.strip():
        number = re.sub(r'[^+\d]', '', phone)
        items.append(f'<a href="tel:{quote(number, safe="+")}" style="{link_style}">{esc(phone)}</a>')
    items.append(f'<a href="mailto:{quote(email.strip(), safe="@.+")}" style="{link_style}">{esc(email)}</a>')
    items.extend(f'<a href="https://{site}" style="{link_style}">{site}</a>' for site in preset.websites)
    items.append(esc(preset.address))
    rows = ''.join(f'<tr><td style="padding:0 0 {2 if i == len(items)-1 else 4}px;font-family:Arial,sans-serif;font-size:12px;line-height:1.35;color:#000000;">{item}</td></tr>' for i, item in enumerate(items))
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;">'
            f'<tr><td width="150" align="center" valign="middle" style="width:150px;padding:4px 18px 4px 0;border-right:1px solid #bdbdbd;">{image}</td>'
            f'<td valign="middle" style="padding:4px 0 4px 18px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">{rows}</table></td></tr></table>')

def document(signature):
    return '<!doctype html><html><head><meta charset="utf-8"><title>Email signature</title></head><body style="margin:20px;background:#ffffff;">' + signature + '</body></html>'
