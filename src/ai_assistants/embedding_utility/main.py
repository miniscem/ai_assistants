"""CLI entry point for the embedding utility."""

import argparse
import logging
import sys
from pathlib import Path

from ai_assistants.embedding_utility.pipeline import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def run_embedding_utility() -> None:
    """CLI entry point for the embed command."""
    parser = argparse.ArgumentParser(
        description="Process documents and upload embeddings to Azure AI Search.",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help="Directory containing input files (default: from config).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=None,
        help="Chunk size in characters (default: from config).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract, chunk, and embed without uploading to Azure.",
    )
    parser.add_argument(
        "--single-file",
        type=Path,
        default=None,
        help="Process a single file instead of scanning a directory.",
    )

    args = parser.parse_args()

    result = run_pipeline(
        input_dir=args.input_dir,
        single_file=args.single_file,
        chunk_size=args.chunk_size,
        dry_run=args.dry_run,
    )

    # Print summary
    print(
        f"\nProcessing complete: {result.successful_files}/{result.total_files} "
        f"files successful, {result.failed_files} failed"
    )
    print(
        f"Total chunks uploaded: {result.total_chunks_uploaded}, "
        f"failed: {result.total_chunks_failed}"
    )

    if result.failed_files > 0:
        print("\nFailed files:")
        for fr in result.file_results:
            if not fr.success:
                print(f"  - {fr.file_name}: {fr.error}")

    sys.exit(1 if result.failed_files == result.total_files and result.total_files > 0 else 0)
