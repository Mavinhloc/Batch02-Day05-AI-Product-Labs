import io
import pytest
from unittest.mock import MagicMock, patch
from src.tutor import extract_text, build_prompt, MAX_DOC_CHARS


class MockFile:
    """Mimics a Streamlit UploadedFile object."""
    def __init__(self, name: str, content: bytes):
        self.name = name
        self._buf = io.BytesIO(content)

    def read(self):
        return self._buf.read()

    def seek(self, pos):
        self._buf.seek(pos)

    def tell(self):
        return self._buf.tell()


# --- extract_text ---

def test_extract_text_txt():
    f = MockFile("notes.txt", "Hello world\nSecond line".encode("utf-8"))
    assert extract_text(f) == "Hello world\nSecond line"


def test_extract_text_txt_unicode():
    f = MockFile("notes.txt", "Xin chào thế giới".encode("utf-8"))
    assert "Xin chào" in extract_text(f)


def test_extract_text_pdf():
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "PDF page content"
    with patch("src.tutor.PdfReader") as MockPdfReader:
        MockPdfReader.return_value.pages = [mock_page]
        f = MockFile("slides.pdf", b"")
        result = extract_text(f)
    assert result == "PDF page content"


def test_extract_text_pdf_multiple_pages():
    pages = [MagicMock(), MagicMock()]
    pages[0].extract_text.return_value = "Page 1"
    pages[1].extract_text.return_value = "Page 2"
    with patch("src.tutor.PdfReader") as MockPdfReader:
        MockPdfReader.return_value.pages = pages
        f = MockFile("slides.pdf", b"")
        result = extract_text(f)
    assert "Page 1" in result
    assert "Page 2" in result


def test_extract_text_docx():
    mock_para = MagicMock()
    mock_para.text = "DOCX paragraph content"
    with patch("src.tutor.Document") as MockDocument:
        MockDocument.return_value.paragraphs = [mock_para]
        f = MockFile("notes.docx", b"")
        result = extract_text(f)
    assert result == "DOCX paragraph content"


def test_extract_text_unknown_format_raises():
    f = MockFile("slides.pptx", b"some content")
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_text(f)


def test_extract_text_truncates_long_file():
    long_text = "x" * (MAX_DOC_CHARS + 1000)
    f = MockFile("notes.txt", long_text.encode("utf-8"))
    result = extract_text(f)
    assert len(result) == MAX_DOC_CHARS
