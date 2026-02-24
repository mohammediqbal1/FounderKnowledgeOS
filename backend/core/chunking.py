def chunk_text(text, chunk_size=800, overlap=150):
    """
    Split text into overlapping chunks.
    
    Args:
        text: The full text to chunk.
        chunk_size: Maximum characters per chunk.
        overlap: Number of overlapping characters between consecutive chunks.
    
    Returns:
        List of text chunks.
    """
    # Clean whitespace
    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks
