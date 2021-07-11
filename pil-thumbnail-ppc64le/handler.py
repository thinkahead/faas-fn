import io
import sys
import os
import logging
import time
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

def handle(req):
    logging.debug("> handle thumbnail")
    buf = io.BytesIO()
    with Image.open(io.BytesIO(req)) as im:
        im.thumbnail((128, 128))
        try:
            im.save(buf, format='JPEG')
        except OSError:
            logging.debug("< handle thumbnail")
            return "cannot process input file", 500, {"Content-type": "text/plain"}
        byte_im = buf.getvalue()
        logging.debug("< handle thumbnail")
        # Return a binary response
        return byte_im, 200, {"Content-type": "application/octet-stream"}
