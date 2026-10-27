"""Run: python -m streamlit run streamlitlogo.py."""
import json
import streamlit as st
import streamlit.components.v1 as components
from signature import PRESETS, render_signature, document, validate

st.set_page_config(page_title='Company signatures', page_icon='✉', layout='wide')
st.markdown('<style>.block-container{max-width:1200px;padding-top:2.5rem;}</style>', unsafe_allow_html=True)
st.caption('COMPANY TOOLS / EMAIL SIGNATURES')
st.title('Your signature. Ready to send.')
st.write('Choose your company, add your details, and bring your signature into Outlook.')
form, preview = st.columns([1, 1.35], gap='large')
with form:
    st.subheader('1. Choose your company')
    key = st.selectbox('Company', list(PRESETS), format_func=lambda k: PRESETS[k].label)
    preset = PRESETS[key]
    st.caption('Your logo, websites, and office address are included automatically.')
    st.subheader('2. Add your details')
    name = st.text_input('Full name', placeholder='Alex Morgan', max_chars=100, key='employee_name')
    title = st.text_input('Job title', placeholder='Account Manager', max_chars=150, key='employee_title')
    email = st.text_input('Email address', placeholder='Your work email', max_chars=200, key='employee_email')
    phone = st.text_input('Phone number (optional)', placeholder='479-555-0123', max_chars=40, key='employee_phone')

with preview:
    st.subheader('3. Preview your signature')
    st.caption('The preview updates as you type. Sample text fills unfinished required fields.')
    st.caption('Select the complete signature below, copy it, and paste it into Outlook’s signature settings.')
    with st.container(border=True):
        sample = render_signature(key, name or 'Your Name', title or 'Your Job Title', email or 'you@company.com', phone)
        components.html(document(sample), height=285, scrolling=True)
    st.caption(f'{preset.label} · One approved logo')
    with st.expander('Included with this company'):
        st.write('Websites: ' + ', '.join(preset.websites))
        st.write(preset.address)
        st.write('Logo link: ' + (preset.logo_link or 'Unlinked'))
    errors = validate(name, title, email, phone)
    if errors:
        st.info('Complete your name, job title, and email to create your signature.' if not any([name, title, email, phone]) else '\n\n'.join(errors))
    if not errors:
        signature = render_signature(key, name, title, email, phone)
        payload = json.dumps(signature).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
        components.html('''<button id="copy" style="background:#172b46;color:white;border:0;border-radius:8px;padding:12px 20px;cursor:pointer;font:14px Arial;">Copy signature</button>
<p id="status" role="status" style="font:13px Arial;color:#334155;"></p><script>
const html = ''' + payload + ''';
document.getElementById('copy').onclick = async () => {
 const status = document.getElementById('status');
 try {
  if (!navigator.clipboard || typeof ClipboardItem === 'undefined') throw new Error();
  const parsed = new DOMParser().parseFromString(html, 'text/html');
  await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([html],{type:'text/html'}), 'text/plain':new Blob([parsed.body.textContent],{type:'text/plain'})})]);
  status.textContent = 'Copied. Paste into your Outlook signature settings.';
 } catch (_) { status.textContent = 'Your browser could not copy formatting. Download the HTML below, open it, and copy the displayed signature.'; }
};</script>''', height=100)
        st.download_button('Download signature HTML', document(signature), file_name=f'{key}-signature.html', mime='text/html')

with st.expander('Add your signature to Outlook'):
    st.write('Copy your completed signature. In Outlook, open signature settings, create a signature, and paste. Choose when it should appear, then save.')
    st.write('If formatted copy is unavailable, download the HTML, open it in a browser, select the displayed signature, and copy it into Outlook.')
    st.write('Send a test email and check the received message before using your signature.')
    st.link_button('Open Microsoft’s Outlook instructions', 'https://support.microsoft.com/en-us/outlook/mail/how-to-add-and-change-an-email-signature-in-outlook')
