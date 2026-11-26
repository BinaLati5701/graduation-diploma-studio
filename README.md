# Graduation Diploma & Regalia Studio
#### Video Demo: <URL HERE>
#### Description:
**Graduation Diploma & Regalia Studio** is an interactive Python application that allows users to customize academic regalia, generate an animated cap-toss celebration GIF, and download a personalized, print-ready diploma PDF. Designed for both non-technical visitors (via a live browser interface) and technical reviewers (via modular, unit-tested Python source code), the project integrates Object-Oriented Programming (OOP), external REST API consumption, programmatic multi-frame image animation, and HTML-to-PDF rendering.

### Features & Architecture
* **Object-Oriented Domain Model (`Graduate` Class):** Encapsulates recipient name validation, degree title formatting, honors distinctions, and academic regalia RGB color mappings using structured dictionaries and lists.
* **External REST API Integration (`fetch_quote`):** Queries the ZenQuotes public API via `requests` to retrieve an inspirational graduation quote dynamically, complete with timeout handling and a built-in fallback quote for uninterrupted offline execution.
* **Programmatic GIF Animation (`generate_regalia_gif`):** Uses `Pillow` (`PIL.Image` and `PIL.ImageDraw`) to synthesize multi-frame academic regalia graphics—cycling through four gown styles before displaying the recipient's selected gown, celebratory confetti, and a mortarboard cap-toss animation saved as a looping `.gif`.
* **HTML-to-PDF Certificate Generation (`create_diploma_pdf`):** Uses `fpdf2` (`FPDF` and `write_html`) to generate a landscape A4 certificate featuring color-matched double borders, formatted HTML typography, an embedded regalia graphic, and a `&copy; 2026 Sabina Dovlati` copyright footer.
* **Automated Unit Testing (`test_project.py`):** Comprehensive `pytest` test suite covering API offline fallback behavior via `monkeypatch`, GIF file generation, and PDF rendering using isolated temporary directories (`tmp_path`).
* **Interactive Web Interface (`app.py`):** Streamlit frontend that renders live regalia animations and provides one-click PDF downloads directly in the browser.

### File Breakdown
* `project.py` — Core Python module containing `Graduate`, `main()`, `fetch_quote()`, `generate_regalia_gif()`, and `create_diploma_pdf()`.
* `test_project.py` — `pytest` unit test suite validating the top-level functions in `project.py`.
* `app.py` — Interactive Streamlit web UI for live browser demos.
* `requirements.txt` — Required third-party Python packages (`requests`, `pillow`, `fpdf2`, `streamlit`, `pytest`).
* `README.md` — Project documentation and architectural overview.

### How to Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt