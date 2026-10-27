# Company email signatures

A Streamlit signature builder with four single-logo presets. Employees select
Soapbox, Kendal King, KKG Inc., or Soapbox Photo Studio and enter name, title, email,
and optional phone. Company websites and each preset's address are fixed. Changing company preserves the
employee's details; email domains are never forced by the selected preset.

## Run

```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlitlogo.py
```

The old checked-out `.venv` references a missing Python 3.11 installation. Use an
available Python installation or create a new environment before running it.

## Presets

| Company | Logo display size | Website lines | Logo link |
| --- | --- | --- | --- |
| Soapbox | 125 × 79 px | www.soapboxretail.com | Soapbox website |
| Kendal King | 119 × 126 px | www.kendalking.com | Kendal King website |
| KKG Inc. | 120 × 128 px | Kendal King, then Soapbox | Unlinked |
| Soapbox Photo Studio | 138 × 109 px | www.soapboxretail.com | Soapbox website |

Shared address: 609 SW 8th St #140 - Bentonville, AR.
Studio exception: 2503 SE J St. #15 - Bentonville, Arkansas.
Studio artwork was recovered from the matching embedded image in the supplied
local `signatures_soapboxstudio.zip`; the standalone PNG path was unavailable.

Dimensions are initial reference-based values for review, not a claim of Outlook
pixel parity. See `assets/logo-comparison.png` for light/dark comparisons. Kendal
King now uses the matching high-resolution repository source, exported at twice
display resolution as `kendal-king-v2.png`. All three assets have contrast
limitations on dark backgrounds. Artwork has not been redrawn or recolored.
Typography follows the original renderer: Arial, 14px bold name, 12px other fields,
1.35 line height, and 4px row spacing (2px on the final row).

## Copying a signature

The app reads approved PNG files from `assets/prepared/` on the backend and
includes the image data in the signature. Separate image hosting is not required
by the application. The preview, copy button, and download use bundled artwork;
the application ignores any old `SIGNATURE_ASSET_BASE_URL` setting.

Select the whole signature in the preview, copy it, and paste it into Outlook's
signature settings. A formatted copy button and HTML download are also available
after entering valid details. Clipboard permissions vary by browser; selecting
the preview directly remains available. Open downloaded HTML in a browser to copy
the displayed signature if preferred.

The user has successfully pasted from the preview. Verify that images also survive
saving the signature, sending, receiving, and replying in the Outlook clients used
internally before treating the workflow as validated across those clients.

## Repository structure

- `streamlitlogo.py`: employee form, preview, copy, download, and Outlook guidance.
- `signature.py`: preset configuration, validation, and escaped HTML rendering;
  reusable when integrating the generator into the internal website.
- `assets/originals/`: supplied sources, preserved unchanged.
- `assets/prepared/`: versioned PNG exports with fixed per-preset display dimensions.
- `prepare_assets.py`: repeatable crop/resize and comparison generation. Uses saved
  originals after the first run; initial import paths refer to the supplied files.
- `test_signature.py`: renderer and Streamlit interaction checks.

The obsolete stacked-logo renderer and template were removed. The older large
Kendal King source in `assets/` now supplies the sharp v2 preset export.
Virtual environments, editor settings, bytecode, and local secrets are ignored.

## Validation

```powershell
python -m unittest -v test_signature
```

Checks cover one logo per preset, escaping of employee text, company links,
optional phone, email validation, deployment URL validation, form fields, keeping
personal information when switching presets, and export availability.

Before internal release, install and send real test emails in classic Outlook,
new Outlook, and Outlook on the web (plus Mac if used). Review received messages,
replies, forwards, long names/titles, omitted phone, external image access, dark
mode, and Windows scaling. Browser preview and automated tests do not establish
Outlook compatibility. These client checks remain pending.

[Microsoft Outlook signature instructions](https://support.microsoft.com/en-us/outlook/mail/how-to-add-and-change-an-email-signature-in-outlook)
