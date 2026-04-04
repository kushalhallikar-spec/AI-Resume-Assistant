import PyPDF2
import io


def extract_text_from_pdf(file) -> str:
    """Extract and clean text from an uploaded PDF file."""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

    # Basic cleanup
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return text
