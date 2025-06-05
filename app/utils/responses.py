from flask import jsonify

def error_response(message: str, status_code: int):
    """
    Standardized error payload.

    Args:
        message: The error message string (without the "Error": prefix).
        status_code: HTTP status code to return.

    Returns:
        A Flask response tuple with JSON body {"Error": message} and the given status_code.
    """
    return jsonify({"Error": message}), status_code
