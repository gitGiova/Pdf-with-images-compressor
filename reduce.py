import os
import sys
import fitz  
import img2pdf
import logging

logging.basicConfig(level=logging.INFO)

def compress_pdf_with_images(input_pdf, output_pdf, quality, zoom=1.5):
    """
    This program is in charge of compressing image-based PDFs by converting each page into a 
    JPEG image, applying compression, and then reassembling the PDF while maintaining the original order.
    To set the compression level you can set these two parameters:
    - quality: in a range from 1 to 100 it is inversally propottiona to the final dimension
    - zoom: resolution of the images (ones merged in the pdf).
    """
    logging.info("Starting the compression of the PDF...")

    logging.info(f"Opening the provided PDF: {input_pdf}")
    
    try:
        doc = fitz.open(input_pdf)

    except Exception as e:
        logging.error(f"Error while opening the PDF: {e}")
        sys.exit(1)
 
    pages = len(doc)
    tmp_images = []
    
    mat = fitz.Matrix(zoom, zoom)
    
    logging.info(f"Processing {pages} pages...")
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat)
        tmp_file_name = f"tmp_page_{i:03d}.jpg"
        jpeg_bytes = pix.tobytes(output="jpg", jpg_quality=quality)
        with open(tmp_file_name, "wb") as img_file:
            img_file.write(jpeg_bytes)
        tmp_images.append(tmp_file_name)
        logging.info("percentage: " + str((i+1)/pages*100) + "%")

    logging.info(f"Images have been created and compressed, creating the new PDF...")
    try:
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(tmp_images))
        logging.info(f"PDF has been successfully created!")
    except Exception as e:
        logging.error(f"Error while creating the PDF: {e}")
    finally:
        logging.info("Cleaning up temporary files...")
        for x in tmp_images:
            if os.path.exists(x):
                os.remove(x)

    logging.info(f"Operation has been completed")


if __name__ == "__main__":
    compress_pdf_with_images(
        input_pdf="relazione.pdf", 
        output_pdf="relazione_compressa.pdf", 
        quality=70,  
        zoom=1.2
    )