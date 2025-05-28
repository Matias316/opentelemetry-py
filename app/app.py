from opentelemetry import trace, metrics
from flask import Flask
from .routes import register_routes
from dotenv import load_dotenv
import logging

# Making sure .env vars are loaded
load_dotenv()

def create_app():
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Obtain tracer and assign a module name
    tracer = trace.get_tracer("opentelemetry-py-app.tracer")

    # Obtain a meter and assign a module name
    meter = metrics.get_meter("opentelemetry-py-app.meter")

    register_routes(app, logger, tracer, meter)

    return app

app = create_app()