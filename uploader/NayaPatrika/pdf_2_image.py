import PyPDF2
from wand.image import Image
import io
import os


def pdf_page_to_png(src_pdf, pagenum=0, resolution=250, ):
    dst_pdf = PyPDF2.PdfFileWriter()
    dst_pdf.addPage(src_pdf.getPage(pagenum))

    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    img = Image(file=pdf_bytes, resolution=resolution)
    img.convert("png")

    return img


def pdf_2_png():
    im = Image(filename='./date.pdf', resolution=150)
    for i, page in enumerate(im.sequence):
        with Image(page) as page_image:
            page_image.format = 'png'
            page_image.alpha_channel = False
            page_image.save(filename='{pageno}.png'.format(pageno=i))
            if i == 0:
                cover_image = page_image
                cover_image.transform("", "150")
                cover_image.save(filename='{page_no}_cover.png'.format(page_no=i))
            page_image.transform("", "120")
            page_image.save(filename='{page_no}_small.png'.format(page_no=i))


pdf_2_png()

#
# file_path = os.path.join(os.curdir, 'date.pdf')
#
# src_pdf = PyPDF2.PdfFileReader(open(file_path, "rb"))
#
# # What follows is a lookup table of page numbers within sample_log.pdf and the corresponding filenames.
# pages = src_pdf.getNumPages()
# # Convert each page to a png image.
# for page in range(pages):
#     big_filename = str(page) + ".png"
#     small_filename = str(page) + "_small" + ".png"
#
#     img = pdf_page_to_png(src_pdf, pagenum=page)
#     img.save(filename=big_filename)
#
#     # Ensmallen
#     img.transform("", "150")
#     img.save(filename=small_filename)
