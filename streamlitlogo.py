from template import EMAIL_SIGNATURE_TEMPLATE
import streamlit as st
import streamlit.components.v1 as components
import base64
from collections import deque
from io import BytesIO
from PIL import Image


st.title("Email Signature Generator")

st.markdown(
    """
    **How to use:**  
    1. Upload your logo and fill in the fields below  
    2. Click **Download signature as HTML**  
    3. Open the downloaded HTML file in your browser  
    4. Select the signature, copy it, and paste it into Outlook's signature editor  
    """
)


# ────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────
def get_base64_img(file):
    """Convert uploaded image file to a base64 data URL."""
    return base64.b64encode(file.read()).decode("utf-8")


def _crop_logo_padding(image: Image.Image) -> Image.Image:
    """Crop transparent or edge-connected near-white padding without trimming artwork."""
    image = image.convert("RGBA")
    width, height = image.size
    pixels = image.load()

    alpha_bbox = image.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
    if alpha_bbox and alpha_bbox != (0, 0, width, height):
        return image.crop(alpha_bbox)

    def is_near_white(x: int, y: int) -> bool:
        r, g, b, a = pixels[x, y]
        return a > 8 and r >= 245 and g >= 245 and b >= 245

    visited = set()
    queue = deque()

    for x in range(width):
        for y in (0, height - 1):
            if (x, y) not in visited and is_near_white(x, y):
                visited.add((x, y))
                queue.append((x, y))

    for y in range(height):
        for x in (0, width - 1):
            if (x, y) not in visited and is_near_white(x, y):
                visited.add((x, y))
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (
                0 <= nx < width
                and 0 <= ny < height
                and (nx, ny) not in visited
                and is_near_white(nx, ny)
            ):
                visited.add((nx, ny))
                queue.append((nx, ny))

    content_bbox = None
    for y in range(height):
        for x in range(width):
            if (x, y) not in visited:
                if content_bbox is None:
                    content_bbox = [x, y, x + 1, y + 1]
                else:
                    content_bbox[0] = min(content_bbox[0], x)
                    content_bbox[1] = min(content_bbox[1], y)
                    content_bbox[2] = max(content_bbox[2], x + 1)
                    content_bbox[3] = max(content_bbox[3], y + 1)

    return image.crop(tuple(content_bbox)) if content_bbox else image


def _preprocess_logo_image(file) -> str:
    """Crop outer padding and re-encode the uploaded logo as PNG base64."""
    image = Image.open(BytesIO(file.getvalue())).convert("RGBA")
    image = _crop_logo_padding(image)

    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return base64.b64encode(output.getvalue()).decode("utf-8")


def build_logo_html(uploaded_files, company_website: str) -> str:
    """
    Build stacked logo HTML for up to 3 uploaded logos.
    Crop outer padding so square/tall logos can fill the logo column better
    without forcing blurry width/height rendering in HTML.
    """
    if not uploaded_files:
        return ""

    logo_count = min(len(uploaded_files), 3)

    if logo_count == 1:
        rendered_width = 170
        padding_bottom = 0
    elif logo_count == 2:
        max_width = 170
        padding_bottom = 12
    else:  # 3 logos
        max_width = 165
        padding_bottom = 8

    logo_blocks = []

    for idx, logo_file in enumerate(uploaded_files[:3]):
        base64_img = _preprocess_logo_image(logo_file)
        logo_url = f"data:image/png;base64,{base64_img}"

        is_last = idx == logo_count - 1
        bottom_space = 0 if is_last else padding_bottom
        if logo_count == 1:
            img_html = (
                f'<img src="{logo_url}" alt="logo" width="{rendered_width}" '
                f'style="display:block;width:{rendered_width}px;height:auto;'
                f'margin:0 auto;border:0;outline:none;text-decoration:none;">'
            )
        else:
            img_html = (
                f'<img src="{logo_url}" alt="logo" '
                f'style="display:block;max-width:{max_width}px;width:auto;height:auto;'
                f'margin:0 auto;border:0;outline:none;text-decoration:none;">'
            )

        logo_blocks.append(
            f'<div style="width:100%;text-align:center;padding-bottom:{bottom_space};">'
            f'<a href="{company_website}" target="_blank" '
            f'style="text-decoration:none;display:inline-block;border:none;">'
            f'{img_html}'
            f'</a>'
            f'</div>'
        )

    return "\n".join(logo_blocks)


def make_row(inner_html: str, is_last: bool = False) -> str:
    """Return a single table row with consistent spacing."""
    padding = "2px" if is_last else "4px"
    return f'<tr><td style="padding-bottom:{padding};border:none;">{inner_html}</td></tr>'


def build_details_rows(
    name: str,
    title: str,
    phone: str,
    email: str,
    website_1: str,
    website_1_url: str,
    website_2: str,
    website_2_url: str,
    address_line_1: str,
    address_line_2: str,
    social_line: str,
) -> str:
    """
    Build the right-hand text block rows dynamically based on which fields are filled.
    Empty fields simply don't generate a row, so spacing always looks clean.

    NOTE: Outlook loves forcing hyperlinks to blue. We hard-override link styling
    with inline CSS + !important so links stay black and non-underlined.
    """
    items = []

    if name.strip():
        items.append(
            f'<span style="font-size:14px;font-weight:bold;color:#000000;">{name}</span>'
        )

    if title.strip():
        items.append(
            f'<span style="font-size:12px;font-weight:bold;color:#000000;">{title}</span>'
        )

    if phone.strip():
        items.append(
            f'<a href="tel:{phone}" '
            f'style="font-size:12px;color:#000000 !important;'
            f'text-decoration:none !important;">{phone}</a>'
        )

    if email.strip():
        items.append(
            f'<a href="mailto:{email}" '
            f'style="font-size:12px;color:#000000 !important;'
            f'text-decoration:none !important;">{email}</a>'
        )

    if website_1.strip():
        items.append(
            f'<a href="{website_1_url}" '
            f'style="font-size:12px;color:#000000 !important;'
            f'text-decoration:none !important;">{website_1}</a>'
        )

    if website_2.strip():
        items.append(
            f'<a href="{website_2_url}" '
            f'style="font-size:12px;color:#000000 !important;'
            f'text-decoration:none !important;">{website_2}</a>'
        )

    if address_line_1.strip():
        items.append(
            f'<span style="font-size:12px;color:#000000;">{address_line_1}</span>'
        )

    if address_line_2.strip():
        items.append(
            f'<span style="font-size:12px;color:#000000;">{address_line_2}</span>'
        )

    if social_line.strip():
        items.append(
            f'<span style="font-size:11px;color:#000000;">{social_line}</span>'
        )

    # Turn items into rows with consistent spacing, slightly tighter on the last line
    rows = []
    for idx, html in enumerate(items):
        is_last = idx == len(items) - 1
        rows.append(make_row(html, is_last=is_last))

    return "\n".join(rows)



# ────────────────────────────────────────────────
# Logo upload
# ────────────────────────────────────────────────
logo_files = st.file_uploader(
    "Upload company logo(s) - up to 3 images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

if logo_files and len(logo_files) > 3:
    st.warning("Only the first 3 uploaded logos will be used.")


# ────────────────────────────────────────────────
# Text fields
# ────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name", value="Raz")
    title = st.text_input("Job Title", value="MVP")
    phone = st.text_input("Phone Number", value="555-555-5555")
    email = st.text_input("Email", value="smukhtar@soapboxretail.com")

with col2:
    website_1 = st.text_input("Website 1 (text)", value="www.soapboxretail.com")
    website_1_url = st.text_input(
        "Website 1 URL",
        value="https://www.soapboxretail.com",
    )
    website_2 = st.text_input("Website 2 (text, optional)", value="")
    website_2_url = st.text_input(
        "Website 2 URL (optional)",
        value="",
    )

address_line_1 = st.text_input(
    "Address line 1",
    value="609 SW 8th St #140 - Bentonville, AR",
)
address_line_2 = st.text_input(
    "Address line 2 (optional)",
    value="",
)
social_line = st.text_input(
    "Extra line (optional)",
    value="",
)

company_website = st.text_input(
    "Company website (logo link)",
    value="https://www.soapboxretail.com",
)

logo_html = build_logo_html(logo_files, company_website)


# ────────────────────────────────────────────────
# Build dynamic rows + full HTML
# ────────────────────────────────────────────────
details_rows = build_details_rows(
    name,
    title,
    phone,
    email,
    website_1,
    website_1_url,
    website_2,
    website_2_url,
    address_line_1,
    address_line_2,
    social_line,
)

fields = {
    "logo_html": logo_html,
    "details_rows": details_rows,
}

signature_html = EMAIL_SIGNATURE_TEMPLATE.format(**fields)

html_document = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
{signature_html}
</body>
</html>
"""


# ────────────────────────────────────────────────
# Preview
# ────────────────────────────────────────────────
st.markdown("### Signature Preview")
components.html(html_document, height=280, scrolling=False)


# ────────────────────────────────────────────────
# Download as HTML
# ────────────────────────────────────────────────
st.download_button(
    "Download signature as HTML",
    data=html_document,
    file_name="signature.html",
    mime="text/html",
)
