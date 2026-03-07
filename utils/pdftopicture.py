import fitz
from PIL import Image
import io

def PDFtoPicture(pdf_path):
    """
    PDF to Picture
    :param pdf_path: PDF path
    :return: List[PIL.Image]
    """

    images = []

    pdf = fitz.open(pdf_path)

    for page_index in range(len(pdf)):
        page = pdf.load_page(page_index)

        pix = page.get_pixmap(dpi=300)

        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))

        images.append(image)

    pdf.close()

    return images