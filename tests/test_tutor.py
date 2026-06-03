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
