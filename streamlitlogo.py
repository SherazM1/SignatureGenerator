from template import EMAIL_SIGNATURE_TEMPLATE
from html import escape
import streamlit as st
import streamlit.components.v1 as components


st.title("Email Signature Generator")

st.markdown(
    """
    **How to use:**  
    1. Enter your hosted logo URL and fill in the fields below  
    2. Click **Download signature as HTML**  
    3. Open the downloaded HTML file in your browser  
    4. Select the signature, copy it, and paste it into Outlook's signature editor  
    """
)


# ────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────
def build_logo_html(logo_urls, company_website: str) -> str:
    """
    Build stacked logo HTML for up to 3 hosted logo URLs.
    Outlook handles normal HTTPS image URLs more reliably than base64 data URIs.
    """
    hosted_logo_urls = [
        logo_url.strip()
        for logo_url in logo_urls[:3]
        if logo_url.strip().lower().startswith("https://")
    ]

    if not hosted_logo_urls:
        return ""

    logo_count = len(hosted_logo_urls)

    if logo_count == 1:
        padding_bottom = 0
    elif logo_count == 2:
        padding_bottom = 12
    else:  # 3 logos
        padding_bottom = 8

    safe_company_website = escape(company_website.strip(), quote=True)
    logo_blocks = []

    for idx, logo_url in enumerate(hosted_logo_urls):
        safe_logo_url = escape(logo_url, quote=True)
        is_last = idx == logo_count - 1
        bottom_space = 0 if is_last else padding_bottom

        img_html = (
            f'<img src="{safe_logo_url}" alt="logo" width="125" '
            f'style="display:block;width:125px;height:auto;'
            f'margin:0 auto;border:0;outline:none;text-decoration:none;">'
        )

        logo_blocks.append(
            f'<div style="width:100%;text-align:center;padding-bottom:{bottom_space};">'
            f'<a href="{safe_company_website}" target="_blank" '
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
# Hosted logo URLs
# ────────────────────────────────────────────────
logo_url_1 = st.text_input(
    "Hosted logo URL",
    value="",
    placeholder="https://example.com/logo.png",
)
logo_url_2 = st.text_input(
    "Hosted logo URL 2 (optional)",
    value="",
    placeholder="https://example.com/logo-2.png",
)
logo_url_3 = st.text_input(
    "Hosted logo URL 3 (optional)",
    value="",
    placeholder="https://example.com/logo-3.png",
)

logo_urls = [logo_url_1, logo_url_2, logo_url_3]
invalid_logo_urls = [
    logo_url.strip()
    for logo_url in logo_urls
    if logo_url.strip() and not logo_url.strip().lower().startswith("https://")
]

if invalid_logo_urls:
    st.warning("Logo URLs must be hosted HTTPS URLs. Non-HTTPS logo URLs will be ignored.")


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

logo_html = build_logo_html(logo_urls, company_website)


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
