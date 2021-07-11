import io
import sys
import os
import logging
import time
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

def handle(req):
    #return b"Hello", 200, {"Content-type": "application/octet-stream"}
    logging.debug("> handle")
    buf = io.BytesIO()
    with Image.open(io.BytesIO(req)) as im:
        # Do not use comma to separate the parameters in logging.debug
        # It will cause "TypeError: not all arguments converted during string formatting"
        logging.debug("  original "+str(im.mode)+" "+str(im.size))
        # manipulate the image while reading it from a file
        im.draft("L", (100, 100))
        logging.debug("  draft "+str(im.mode)+" "+str(im.size))
        #im = im.convert("L")
        try:
            im.save(buf, format='JPEG')
        except OSError:
            logging.debug("< handle")
            return "cannot process input file", 500, {"Content-type": "text/plain"}
        byte_im = buf.getvalue()
        logging.debug("< handle")
        # Return a binary response
        return byte_im, 200, {"Content-type": "application/octet-stream"}
