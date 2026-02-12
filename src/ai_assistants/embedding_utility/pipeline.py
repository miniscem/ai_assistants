"""Pipeline orchestrator for the embedding utility."""

import logging
from dataclasses import dataclass, field
from pathlib import Path

from ai_assistants.embedding_utility.chunker.text_chunker import chunk_text
from ai_assistants.embedding_utility.config import get_input_directory
from ai_assistants.embedding_utility.embeddings.generator import generate_embeddings
from ai_assistants.embedding_utility.ocr.processor import (
    SUPPORTED_EXTENSIONS,
    extract_text,
)
from ai_assistants.embedding_utility.search.azure_client import AzureSearchClient
from ai_assistants.shared.config import settings

logger = logging.getLogger(__name__)


@dataclass
class FileResult:
    """Result of processing a single file."""

    file_name: str
    success: bool = True
    error: str = ""
    chunks_uploaded: int = 0
    chunks_failed: int = 0


@dataclass
class PipelineResult:
    """Result of the full pipeline run."""

    file_results: list[FileResult] = field(default_factory=list)
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_chunks_uploaded: int = 0
    total_chunks_failed: int = 0


def _get_supported_files(input_dir: Path, single_file: Path | None = None) -> list[Path]:
    """Get list of supported files to process."""
    if single_file:
        if single_file.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [single_file]
        return []

    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(input_dir.glob(f"*{ext}"))
    return sorted(files)


def run_pipeline(
    input_dir: Path | None = None,
    single_file: Path | None = None,
    chunk_size: int | None = None,
    dry_run: bool = False,
) -> PipelineResult:
    """Run the full embedding pipeline.

    Args:
        input_dir: Directory to scan for files. Defaults to config value.
        single_file: Process only this file instead of scanning a directory.
        chunk_size: Override chunk size from config.
        dry_run: If True, skip Azure upload.

    Returns:
        PipelineResult with per-file details.
    """
    input_dir = input_dir or get_input_directory()
    chunk_size = chunk_size or settings.embedding_chunk_size

    files = _get_supported_files(input_dir, single_file)
    result = PipelineResult(total_files=len(files))

    if not files:
        logger.warning("No supported files found in %s", input_dir)
        return result

    # Initialize Azure client and embedding model upfront
    azure_client: AzureSearchClient | None = None
    if not dry_run:
        azure_client = AzureSearchClient()
        azure_client.ensure_index_exists()
    else:
        azure_client = None

    # Pre-load the embedding model
    from ai_assistants.embedding_utility.embeddings.generator import get_model
    get_model()

    for idx, file_path in enumerate(files, 1):
        logger.info("Processing file %d/%d: %s", idx, len(files), file_path.name)
        file_result = FileResult(file_name=file_path.name)

        try:
            # Step 1: Extract text
            extraction = extract_text(file_path)
            if not extraction.success:
                file_result.success = False
                file_result.error = extraction.error
                result.file_results.append(file_result)
                result.failed_files += 1
                logger.error("Extraction failed for %s: %s", file_path.name, extraction.error)
                continue

            if not extraction.pages:
                logger.warning("No text extracted from %s", file_path.name)
                file_result.success = False
                file_result.error = "No text extracted"
                result.file_results.append(file_result)
                result.failed_files += 1
                continue

            # Step 2: Chunk text from all pages
            all_chunks = []
            for page in extraction.pages:
                page_chunks = chunk_text(page.text, chunk_size, overlap_fraction=0.1)
                for chunk in page_chunks:
                    all_chunks.append({
                        "content": chunk.text,
                        "source_file": file_path.name,
                        "chunk_index": len(all_chunks),
                        "page_number": page.page_number,
                    })

            if not all_chunks:
                logger.warning("No chunks generated from %s", file_path.name)
                file_result.success = False
                file_result.error = "No chunks generated"
                result.file_results.append(file_result)
                result.failed_files += 1
                continue

            # Step 3: Generate embeddings
            texts = [c["content"] for c in all_chunks]
            embeddings = generate_embeddings(texts)
            for chunk, embedding in zip(all_chunks, embeddings):
                chunk["content_vector"] = embedding

            # Step 4: Upload to Azure
            if dry_run:
                logger.info(
                    "[DRY RUN] Would upload %d chunks for %s",
                    len(all_chunks),
                    file_path.name,
                )
                file_result.chunks_uploaded = len(all_chunks)
            else:
                assert azure_client is not None
                uploaded, failed = azure_client.upload_chunks(all_chunks)
                file_result.chunks_uploaded = uploaded
                file_result.chunks_failed = failed

            result.successful_files += 1

        except Exception as e:
            file_result.success = False
            file_result.error = str(e)
            result.failed_files += 1
            logger.exception("Pipeline failed for %s", file_path.name)

        result.file_results.append(file_result)
        result.total_chunks_uploaded += file_result.chunks_uploaded
        result.total_chunks_failed += file_result.chunks_failed

    return result
