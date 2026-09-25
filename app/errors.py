from flask import jsonify


def register_error_handlers(app):
    """Register application-wide error handlers"""

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({
            "error": str(error)
        }), 400
