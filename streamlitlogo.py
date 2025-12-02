# streamlitlogo.py

import base64
import io

import streamlit as st
from html2image import Html2Image  # add html2image to requirements.txt
from template import EMAIL_SIGNATURE_TEMPLATE


st.title("Email Signature Generator")

st.markdown(
    """
    **How to use:**  
    1. Upload your logo and fill in the fields below  
    2. Preview the signature  
    3. Download as **HTML** (for copy-paste into Outlook) or **PNG image**  
    4. In Outlook, paste the signature into a new signature and adjust formatting if needed  
    """
)


def get_base64_img(file):
    return base64.b64encode(file.read()).decode("utf-8")


# ────────────────────────────────────────────────
# Inputs
# ────────────────────────────────────────────────
logo_file = st.file_uploader("Upload the company logo (single image)", type=["png", "jpg", "jpeg"])

if logo_file is not None:
    filetype = logo_file.type.split("/")[-1]
    base64_img = get_base64_img(logo_file)
    logo_url = f"data:image/{filetype};base64,{base64_img}"
else:
    logo_url = ""

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name", value="Rhonda Stinson")
    title = st.text_input("Job Title", value="Director of Accounting + Administration")
    phone = st.text_input("Phone Number", value="913-449-2123")
    email = st.text_input("Email", value="rstinson@kendalking.com")

with col2:
    website_1 = st.text_input("Website 1 (text)", value="www.soapboxretail.com")
    website_1_url = st.text_input("Website 1 URL", value="https://www.soapboxretail.com")
    website_2 = st.text_input("Website 2 (text)", value="www.kendalkinggroup.com")
    website_2_url = st.text_input("Website 2 URL", value="https://www.kendalkinggroup.com")

address_line_1 = st.text_input("Address line 1", value="609 SW 8th St #140 - Bentonville, AR")
address_line_2 = st.text_input("Address line 2", value="PO Box 1160, Smithville, MO 64089")
social_line = st.text_input("Social / extra line (optional)", value="")

company_website = st.text_input("Company website (logo link)", value="https://www.kendalkinggroup.com")


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

# Wrap for standalone HTML file / image rendering
html_document = f"""
<!DOCTYPE html>
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


# ────────────────────────────────────────────────
# Copy HTML (for power-users / other tools)
# ────────────────────────────────────────────────
with st.expander("Show raw HTML for copying"):
    st.text_area("HTML", html_document, height=240)

    # Simple browser-side copy button using JS
    st.markdown(
        """
        <button onclick="navigator.clipboard.writeText(document.querySelector('textarea').value)">
            Copy HTML to clipboard
        </button>
        """,
        unsafe_allow_html=True,
    )


# ────────────────────────────────────────────────
# Download as PNG image
# ────────────────────────────────────────────────
st.markdown("### Download as image")

if st.button("Generate PNG image"):
    try:
        from html2image import Html2Image

        # You can tweak size here if needed
        hti = Html2Image(size=(800, 200))

        # Render to a PNG file in the current directory
        hti.screenshot(
            html_str=html_document,
            save_as="signature.png",
        )

        with open("signature.png", "rb") as f:
            png_bytes = f.read()

        st.image(png_bytes, caption="Generated signature image")
        st.download_button(
            "Download PNG",
            data=png_bytes,
            file_name="signature.png",
            mime="image/png",
        )
    except FileNotFoundError:
        st.error(
            "PNG generation isn't supported on this server because a headless "
            "Chrome/Chromium browser isn't installed. "
            "You can still use the HTML download and copy it into Outlook."
        )
    except Exception as e:
        st.error(
            "Something went wrong while generating the image. "
            "PNG export works best when running this app locally."
        )
