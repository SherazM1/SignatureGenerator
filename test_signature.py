import os
import unittest
from unittest.mock import patch
from html.parser import HTMLParser
from signature import PRESETS, render_signature, validate, image_source

class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class SignatureTests(unittest.TestCase):
    def test_presets_and_escaping(self):
        for key, preset in PRESETS.items():
            html = render_signature(key, '<script>alert(1)</script>', 'Sales & Marketing', 'person@soapboxretail.com', asset_base_url='https://images.example.com/signatures')
            tags = Tags(html).tags
            self.assertNotIn('<script>', html)
            self.assertIn('Sales &amp; Marketing', html)
            images = [attrs for tag, attrs in tags if tag == 'img']
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0]['width'], str(preset.width))
            self.assertNotIn('data:image', html)
            links = [attrs['href'] for tag, attrs in tags if tag == 'a']
            self.assertFalse(any(link.startswith('tel:') for link in links))
            self.assertEqual(len(links), 3 if key != 'kkg' else 3)
            self.assertIn('mailto:person@soapboxretail.com', links)
        self.assertNotIn('<a', render_signature('kkg', 'A', 'B', 'a@b.com').split('<img')[0])

    def test_validation(self):
        self.assertEqual(validate('A', 'B', 'a@soapboxretail.com', '(479) 555-0123'), [])
        self.assertTrue(validate('', '', 'bad', 'javascript:alert(1)'))

    def test_reference_typography(self):
        html = render_signature('kkg', 'Sheraz Mukhtar', 'Technical Operations Manager', 'smukhtar@soapboxretail.com', '501-422-4282')
        self.assertIn('font-size:14px', html)
        self.assertIn('font-size:12px;line-height:1.35', html)
        self.assertNotIn('font-size:16px', html)
        self.assertNotIn('line-height:19px', html)
        self.assertIn('padding:0 0 4px', html)
        self.assertIn('width="120" height="128"', html)

    def test_studio_address_and_artwork(self):
        html = render_signature('soapbox-studio', 'Dana Smith', 'Accounts & Studio Operations', 'dsmith@soapboxretail.com')
        self.assertIn('2503 SE J St. #15 - Bentonville, Arkansas', html)
        self.assertNotIn('609 SW', html)
        self.assertEqual(PRESETS['soapbox-studio'].label, 'Soapbox Photo Studio')
        self.assertIn('data:image/png;base64,', html)

    def test_config(self):
        for url in ['http://example.com', 'https://example.com?a=1', 'https://user:pass@example.com']:
            with self.assertRaises(ValueError):
                image_source(PRESETS['kkg'], url)

    def test_ui_and_preset_switch_preserve_personal_details(self):
        from streamlit.testing.v1 import AppTest
        with patch.dict(os.environ, {'SIGNATURE_ASSET_BASE_URL': ''}):
            app = AppTest.from_file('streamlitlogo.py').run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.text_input), 4)
            app.text_input[0].set_value('RAZ$$$')
            app.text_input[1].set_value('Title Placeholder')
            app.text_input[2].set_value('example@soapboxretail.com').run()
            app.selectbox[0].set_value('kkg').run()
            self.assertEqual(app.text_input[2].value, 'example@soapboxretail.com')
            app.selectbox[0].set_value('soapbox-studio').run()
            self.assertEqual(app.text_input[2].value, 'example@soapboxretail.com')
            self.assertEqual(len(app.selectbox[0].options), 4)
            self.assertEqual(len(app.get('download_button')), 1)
            self.assertFalse(any('requires the approved hosted' in item.value for item in app.info))
        with patch.dict(os.environ, {'SIGNATURE_ASSET_BASE_URL': 'https://images.example.com/signatures'}):
            app.run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.get('download_button')), 1)

if __name__ == '__main__':
    unittest.main()
