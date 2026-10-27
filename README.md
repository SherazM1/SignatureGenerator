# Company email signatures

A Streamlit signature builder with four single-logo presets. 

## Run

```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlitlogo.py
```

The old checked-out `.venv` references a missing Python 3.11 installation. Use an
available Python installation or create a new environment before running it.


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


## Validation

```powershell
python -m unittest -v test_signature
```

Checks cover one logo per preset, escaping of employee text, company links,
optional phone, email validation, deployment URL validation, form fields, keeping
personal information when switching presets, and export availability.


