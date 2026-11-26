import os
import pytest
from project import Graduate, fetch_quote, generate_regalia_gif, create_diploma_pdf


def test_fetch_quote(monkeypatch):
    def mock_get(*args, **kwargs):
        raise RuntimeError("Offline test")

    monkeypatch.setattr("requests.get", mock_get)
    quote = fetch_quote()
    assert "Eleanor Roosevelt" in quote


def test_generate_regalia_gif(tmp_path):
    grad = Graduate("Alex Rivera", "B.S. in Computer Science", "Crimson Scholar", "Magna Cum Laude")
    gif_out = tmp_path / "test_regalia.gif"
    result = generate_regalia_gif(grad, str(gif_out))
    assert os.path.exists(result)
    assert gif_out.stat().st_size > 0


def test_create_diploma_pdf(tmp_path):
    grad = Graduate("Jordan Lee", "M.S. in Artificial Intelligence", "Emerald Honors", "Summa Cum Laude")
    gif_out = tmp_path / "test_regalia.gif"
    pdf_out = tmp_path / "test_diploma.pdf"
    generate_regalia_gif(grad, str(gif_out))
    result = create_diploma_pdf(grad, '"Keep learning." - Anonymous', str(gif_out), str(pdf_out))
    assert os.path.exists(result)
    assert pdf_out.stat().st_size > 0