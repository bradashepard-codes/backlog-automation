from docx import Document


def read_word(path: str) -> str:
    """Extract full text from a Word document, preserving heading hierarchy."""
    doc = Document(path)
    lines = []
    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            level = para.style.name.split()[-1]
            lines.append(f"{'#' * int(level)} {para.text}")
        elif para.text.strip():
            lines.append(para.text)
    return "\n\n".join(lines)
