import uuid
import os
import json
import psutil
import time

import app_synthesize

from tyrell.logger import get_logger
logger = get_logger('tyrell')
logger.setLevel('DEBUG')

request_config = {
	"title": "How can I convert a new set of lines to markdown indicators?",
	"question": 
"""I'm trying to create a system that converts plaintext English  into markdown indicators that display the worded intent in markdown. Specifically
our system should be able to add header tags # to emphasize headings and other emphasizing tags like _ _ and * *.

Here's what I have:

set.seed(10)
dat <- "Lorem Ipsum \n Dolor Sit Amet"

Desired Conversion:

# Lorem Ipsum
Dolor _Sit_ *Amet*
"""
}

resp_start = time.time()
resp = app_synthesize.synthesize(request_config)
resp_end = time.time()
resp["time"] = resp_end - resp_start
