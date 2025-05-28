from opentelemetry import trace, metrics
from flask import Flask
from random import randint
from dotenv import load_dotenv
import logging

# Making sure .env vars are loaded
load_dotenv()

# Obtain tracer and assign a module name
tracer = trace.get_tracer("opentelemetry-py-app.tracer")

# Obtain a meter and assign a module name
meter = metrics.get_meter("opentelemetry-py-app.meter")

# Create a counter instrument
random_value_counter = meter.create_counter("random_group.values", description="The number of ocurrences by random value")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/log-based-on-random-int")
def log_based_on_random_int():
    # Create a new span that will be child of current one
    with tracer.start_as_current_span("inner_span") as roll_span:
        result = str(get_random_int())
        roll_span.set_attribute("random_value.value", result)
        
        # Add 1 to the counter for the given random value
        random_value_counter.add(1, {"random_value.value": result})
        
        if int(result) > 5:
            logger.warning("Value greater than 5: %s", result)
        else:
            logger.warning("Value smaller than 5: %s", result)
        return result

def get_random_int():
    return randint(0,10)