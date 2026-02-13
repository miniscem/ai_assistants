"""Azure AI Search client for uploading document chunks."""

import hashlib
import logging
from datetime import datetime, timezone

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

from ai_assistants.embedding_utility.search.schema import create_index_definition
from ai_assistants.shared.config import settings

logger = logging.getLogger(__name__)


def _generate_chunk_id(source_file: str, chunk_index: int) -> str:
    """Generate a deterministic chunk ID for idempotent re-processing."""
    content = f"{source_file}:{chunk_index}"
    return hashlib.sha256(content.encode()).hexdigest()


class AzureSearchClient:
    """Client for interacting with Azure AI Search."""

    def __init__(
        self,
        endpoint: str = "",
        api_key: str = "",
        index_name: str = "",
    ) -> None:
        self.endpoint = endpoint or settings.azure_search_endpoint
        self.api_key = api_key or settings.azure_search_api_key
        self.index_name = index_name or settings.azure_search_index_name
        self._credential = AzureKeyCredential(self.api_key)
        self._index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=self._credential,
        )
        self._search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self._credential,
        )

    @staticmethod
    def _model_suffix(model_name: str) -> str:
        """Extract a short suffix from a model name (e.g. 'intfloat/e5-large-v2' → 'e5-large-v2')."""
        return model_name.rsplit("/", 1)[-1]

    def ensure_index_exists(self, vector_dimensions: int, model_name: str = "") -> None:
        """Create or update the search index.

        If the index already exists with incompatible settings, retries with
        a model-specific index name (``{index}-{model_suffix}``).
        """
        index_def = create_index_definition(self.index_name, vector_dimensions)
        try:
            self._index_client.create_or_update_index(index_def)
        except HttpResponseError as exc:
            if exc.error and exc.error.code == "OperationNotAllowed" and model_name:
                suffix = self._model_suffix(model_name)
                new_name = f"{self.index_name}-{suffix}"
                logger.warning(
                    "Index '%s' is incompatible (%s). Retrying with '%s'.",
                    self.index_name,
                    exc.message,
                    new_name,
                )
                self.index_name = new_name
                index_def = create_index_definition(new_name, vector_dimensions)
                self._index_client.create_or_update_index(index_def)
                self._search_client = SearchClient(
                    endpoint=self.endpoint,
                    index_name=self.index_name,
                    credential=self._credential,
                )
            else:
                raise
        logger.info("Index '%s' is ready.", self.index_name)

    def upload_chunks(
        self,
        chunks: list[dict],
        batch_size: int = 100,
    ) -> tuple[int, int]:
        """Upload document chunks in batches.

        Each chunk dict should have: content, content_vector, source_file,
        chunk_index, page_number.

        Returns:
            Tuple of (success_count, fail_count).
        """
        success_count = 0
        fail_count = 0
        now = datetime.now(timezone.utc).isoformat()

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            documents = []
            for chunk in batch:
                doc = {
                    "id": _generate_chunk_id(
                        chunk["source_file"], chunk["chunk_index"]
                    ),
                    "content": chunk["content"],
                    "content_vector": chunk["content_vector"],
                    "source_file": chunk["source_file"],
                    "chunk_index": chunk["chunk_index"],
                    "page_number": chunk["page_number"],
                    "embedding_model": chunk.get("embedding_model", ""),
                    "created_at": now,
                }
                documents.append(doc)

            try:
                result = self._search_client.merge_or_upload_documents(documents)
                for item in result:
                    if item.succeeded:
                        success_count += 1
                    else:
                        fail_count += 1
                        logger.warning(
                            "Failed to upload chunk %s: %s",
                            item.key,
                            item.error_message,
                        )
            except Exception:
                logger.exception("Batch upload failed for batch starting at %d", i)
                fail_count += len(batch)

        return success_count, fail_count

    def delete_by_source_file(self, source_file: str) -> int:
        """Delete all chunks for a given source file.

        Returns:
            Number of documents deleted.
        """
        results = self._search_client.search(
            search_text="*",
            filter=f"source_file eq '{source_file}'",
            select=["id"],
        )
        doc_ids = [{"id": r["id"]} for r in results]
        if not doc_ids:
            return 0

        self._search_client.delete_documents(doc_ids)
        logger.info("Deleted %d chunks for '%s'.", len(doc_ids), source_file)
        return len(doc_ids)
