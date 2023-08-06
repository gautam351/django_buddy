import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

#load env variables
load_dotenv()

# function to generate token
def generate_jwt_token(user_id):
    # Define the payload of the token, which typically includes user information and other data
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token will expire in 1 day from now
    }

    # Encode the payload and generate the JWT token
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm='HS256')

    return token

# function to decode token
def verify_jwt_token(token):
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token,  os.getenv("JWT_SECRET"), algorithms=['HS256'])
        user_id = payload.get('user_id')
        # Perform additional authentication and authorization checks if needed

        return user_id
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None
