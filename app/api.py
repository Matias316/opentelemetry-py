from flask import Flask, request
from random import randint
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/log-based-on-random-int")
def log_based_on_random_int():
    result = str(get_random_int())
    if int(result) > 5:
        logger.warning("Value greater than 5: %s", result)
    else:
        logger.warning("Value smaller than 5: %s", result)
    return result

def get_random_int():
    return randint(0,10)