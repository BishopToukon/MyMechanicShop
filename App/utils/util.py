from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

SECRET_KEY = "a super secret, secret key"
ALGORITHM = "HS256"


def encode_token(customer_id):
    """
    Generate a JWT for a specific customer.
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
        'sub': str(customer_id)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError

SECRET_KEY = "your_secret_key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the Authorization header is present
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            customer_id = data.get("sub")  # Extract customer_id from the token payload
        except JWTError:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(customer_id, *args, **kwargs)

    return decorated