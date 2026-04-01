from template import EMAIL_SIGNATURE_TEMPLATE
import streamlit as st
import base64


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


def build_signature_row(signature_urls: list[str]) -> str:
    """
    Build one row that renders up to 3 signature images cleanly.
    Returns empty string when no signature images are uploaded.
    """
    if not signature_urls:
        return ""

    cells = []
    for idx, sig_url in enumerate(signature_urls):
        right_pad = "8px" if idx < len(signature_urls) - 1 else "0"
        cells.append(
            f'<td style="padding:0 {right_pad} 0 0;border:none;vertical-align:middle;">'
            f'<img src="{sig_url}" alt="signature {idx + 1}" '
            f'style="display:block;height:28px;width:auto;border:0;outline:none;text-decoration:none;">'
            f"</td>"
        )

    return (
        '<tr><td style="padding-top:8px;border:none;">'
        '<table cellpadding="0" cellspacing="0" border="0" '
        'style="border-collapse:collapse;border:none;">'
        f"<tr>{''.join(cells)}</tr>"
        "</table>"
        "</td></tr>"
    )


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
logo_file = st.file_uploader(
    "Upload the company logo (single image)",
    type=["png", "jpg", "jpeg"],
)

if logo_file is not None:
    filetype = logo_file.type.split("/")[-1]
    base64_img = get_base64_img(logo_file)
    logo_url = f"data:image/{filetype};base64,{base64_img}"
else:
    logo_url = ""

# Signature uploads (up to 3)
signature_files = st.file_uploader(
    "Upload signature images (up to 3)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

if signature_files and len(signature_files) > 3:
    st.warning("Only the first 3 signature images will be used.")

signature_urls = []
for sig_file in (signature_files or [])[:3]:
    sig_filetype = sig_file.type.split("/")[-1]
    sig_base64 = get_base64_img(sig_file)
    signature_urls.append(f"data:image/{sig_filetype};base64,{sig_base64}")

signatures_row = build_signature_row(signature_urls)


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
    "logo_url": logo_url,
    "company_website": company_website,
    "details_rows": details_rows,
    "signatures_row": signatures_row,
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
st.markdown(signature_html, unsafe_allow_html=True)


# ────────────────────────────────────────────────
# Download as HTML
# ────────────────────────────────────────────────
st.download_button(
    "Download signature as HTML",
    data=html_document,
    file_name="signature.html",
    mime="text/html",
)
