from random import randint
from flask import jsonify

def register_routes(app, logger, tracer, meter):

    # Create a counter instrument
    random_value_counter = meter.create_counter("random_group.values", description="The number of ocurrences by random value")

    @app.route("/")
    def home():
        return "Opentelemetry-py home page!"

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
    

    @app.route("/health/ready")
    def readiness():
        # Check dependencies connectivity
        data = {"status" : "ready"}
        return jsonify(data), 200
    
    @app.route("/health/live")
    def liveness():
        data = {"status" : "alive"}
        return jsonify(data), 200