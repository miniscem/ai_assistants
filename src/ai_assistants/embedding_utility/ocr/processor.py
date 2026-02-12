"""OCR and PDF text extraction using pymupdf and pytesseract."""

import logging
from dataclasses import dataclass, field
from pathlib import Path

import fitz  # pymupdf
import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp"}
MIN_TEXT_LENGTH = 50  # Threshold for OCR fallback on PDF pages


@dataclass
class ExtractedPage:
    """Text extracted from a single page."""

    text: str
    page_number: int
    source_file: str


@dataclass
class ExtractionResult:
    """Result of extracting text from a file."""

    pages: list[ExtractedPage] = field(default_factory=list)
    source_file: str = ""
    success: bool = True
    error: str = ""


def _extract_from_pdf(file_path: Path) -> ExtractionResult:
    """Extract text from a PDF, falling back to OCR for scanned pages."""
    result = ExtractionResult(source_file=file_path.name)

    try:
        doc = fitz.open(str(file_path))
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().strip()

            # Fall back to OCR if text extraction yields minimal content
            if len(text) < MIN_TEXT_LENGTH:
                logger.debug(
                    "Page %d of %s has minimal text, using OCR fallback.",
                    page_num + 1,
                    file_path.name,
                )
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                text = pytesseract.image_to_string(img).strip()

            if text:
                result.pages.append(ExtractedPage(
                    text=text,
                    page_number=page_num + 1,
                    source_file=file_path.name,
                ))
        doc.close()
    except Exception as e:
        result.success = False
        result.error = str(e)
        logger.exception("Failed to extract text from PDF: %s", file_path.name)

    return result


def _extract_from_image(file_path: Path) -> ExtractionResult:
    """Extract text from an image using OCR."""
    result = ExtractionResult(source_file=file_path.name)

    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img).strip()
        if text:
            result.pages.append(ExtractedPage(
                text=text,
                page_number=1,
                source_file=file_path.name,
            ))
    except Exception as e:
        result.success = False
        result.error = str(e)
        logger.exception("Failed to extract text from image: %s", file_path.name)

    return result


def extract_text(file_path: Path) -> ExtractionResult:
    """Extract text from a supported file (PDF or image).

    Args:
        file_path: Path to the input file.

    Returns:
        ExtractionResult with extracted pages.
    """
    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        return ExtractionResult(
            source_file=file_path.name,
            success=False,
            error=f"Unsupported file type: {suffix}",
        )

    if suffix == ".pdf":
        return _extract_from_pdf(file_path)
    return _extract_from_image(file_path)
