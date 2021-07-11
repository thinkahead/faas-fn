import io
import sys
import os
import logging
import time
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

def handle(req):
    logging.debug("> handle bw")
    buf = io.BytesIO()
    with Image.open(io.BytesIO(req)) as im:
        im = im.convert("L")
        try:
            im.save(buf, format='JPEG')
        except OSError:
            logging.debug("< handle bw")
            return "cannot process input file", 500, {"Content-type": "text/plain"}
        byte_im = buf.getvalue()
        logging.debug("< handle bw")
        # Return a binary response
        return byte_im, 200, {"Content-type": "application/octet-stream"}
