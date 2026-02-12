"""Text chunking with character-based sliding window and boundary-aware splitting."""

from dataclasses import dataclass


@dataclass
class TextChunk:
    """A chunk of text with positional metadata."""

    text: str
    chunk_index: int
    start_char: int
    end_char: int


def _find_split_point(text: str, target: int, window: int = 100) -> int:
    """Find the best split point near target, preferring sentence then word boundaries."""
    start = max(0, target - window)
    end = min(len(text), target + window)
    search_region = text[start:end]

    # Prefer sentence boundaries
    for sep in [". ", ".\n", "\n\n", "\n"]:
        idx = search_region.rfind(sep)
        if idx != -1:
            return start + idx + len(sep)

    # Fall back to word boundaries
    space_idx = search_region.rfind(" ")
    if space_idx != -1:
        return start + space_idx + 1

    # Last resort: split at target
    return target


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap_fraction: float = 0.1,
) -> list[TextChunk]:
    """Split text into overlapping chunks with boundary-aware splitting.

    Args:
        text: The text to chunk.
        chunk_size: Target size of each chunk in characters.
        overlap_fraction: Fraction of chunk_size to use as overlap (default 10%).

    Returns:
        List of TextChunk objects.
    """
    if not text or not text.strip():
        return []

    overlap = int(chunk_size * overlap_fraction)
    chunks: list[TextChunk] = []
    pos = 0
    index = 0

    while pos < len(text):
        end = pos + chunk_size

        if end >= len(text):
            # Last chunk: take everything remaining
            chunk_text_str = text[pos:].strip()
            if chunk_text_str:
                chunks.append(TextChunk(
                    text=chunk_text_str,
                    chunk_index=index,
                    start_char=pos,
                    end_char=len(text),
                ))
            break

        # Find a good split point near the target end
        split_at = _find_split_point(text, end)
        chunk_text_str = text[pos:split_at].strip()

        if chunk_text_str:
            chunks.append(TextChunk(
                text=chunk_text_str,
                chunk_index=index,
                start_char=pos,
                end_char=split_at,
            ))
            index += 1

        # Advance by stride from the actual split point
        pos = split_at - overlap
        if pos <= chunks[-1].start_char if chunks else 0:
            # Avoid infinite loop if split point didn't advance
            pos = split_at

    return chunks
