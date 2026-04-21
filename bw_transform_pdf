import fitz
import cv2
import numpy as np


def bw_editorial(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray,(5,5),0)

    bw = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        5
    )

    return bw


input_pdf = "input.pdf"
output_pdf = "output_bw.pdf"

doc = fitz.open(input_pdf)
new_doc = fitz.open()

print("Processing...")

for page in doc:

    mat = fitz.Matrix(2.5,2.5)
    pix = page.get_pixmap(matrix=mat)

    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h,pix.w,pix.n)

    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    bw = bw_editorial(img)

    bw_rgb = cv2.cvtColor(bw, cv2.COLOR_GRAY2RGB)

    ok, buffer = cv2.imencode(".jpg", bw_rgb, [int(cv2.IMWRITE_JPEG_QUALITY),90])

    new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
    new_page.insert_image(new_page.rect, stream=buffer.tobytes())


doc.close()

new_doc.save(output_pdf)
new_doc.close()

print("DONE")
