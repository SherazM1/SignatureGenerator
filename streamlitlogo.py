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


def get_base64_img(file):
    """Convert uploaded image file to a base64 data URL."""
    return base64.b64encode(file.read()).decode("utf-8")


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


# ────────────────────────────────────────────────
# Text fields
# ────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name", value="Brittany Teague")
    title = st.text_input("Job Title", value="Director of Business Development")
    phone = st.text_input("Phone Number", value="918-440-1925")
    email = st.text_input("Email", value="bteague@soapboxretail.com")

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
# Build signature HTML
# ────────────────────────────────────────────────
fields = {
    "name": name,
    "title": title,
    "phone": phone,
    "email": email,
    "website_1": website_1,
    "website_1_url": website_1_url,
    "website_2": website_2,
    "website_2_url": website_2_url,
    "address_line_1": address_line_1,
    "address_line_2": address_line_2,
    "social_line": social_line,
    "logo_url": logo_url,
    "company_website": company_website,
}

signature_html = EMAIL_SIGNATURE_TEMPLATE.format(**fields)

# Wrap in a minimal HTML document for download/opening
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
