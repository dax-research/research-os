def chunk_text(text, chunk_size=300, overlap=0):
    """Split text into fixed-size word chunks with optional overlap."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if isinstance(chunk_size, bool) or not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be an integer")

    if isinstance(overlap, bool) or not isinstance(overlap, int):
        raise TypeError("overlap must be an integer")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    words = text.strip().split()
    if not words:
        return []

    chunks = []
    step = chunk_size - overlap
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start += step

    return chunks


def create_chunks(paper, chunk_size=300, overlap=0):
    """Create page-aware chunks from a paper dictionary.

    Each chunk keeps its own page number and a sequential chunk_id so the
    downstream embedding and retrieval pipeline can trace the source of the
    text later. When overlap is used, neighboring chunks share words to keep
    more context around boundaries.
    """
    if not isinstance(paper, dict):
        raise TypeError("paper must be a dictionary")

    if isinstance(chunk_size, bool) or not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be an integer")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if isinstance(overlap, bool) or not isinstance(overlap, int):
        raise TypeError("overlap must be an integer")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    pages = paper.get("pages", [])
    if not isinstance(pages, list):
        raise TypeError("paper['pages'] must be a list")

    chunks = []
    chunk_id = 1

    for page in pages:
        if not isinstance(page, dict):
            raise TypeError("each page must be a dictionary")

        page_number = page.get("page_number")
        page_text = page.get("text", "")

        if not isinstance(page_text, str):
            raise TypeError("page text must be a string")

        if not page_text.strip():
            continue

        for text_chunk in chunk_text(page_text, chunk_size=chunk_size, overlap=overlap):
            chunks.append({
                "chunk_id": chunk_id,
                "page_number": page_number,
                "text": text_chunk,
            })
            chunk_id += 1

    return chunks