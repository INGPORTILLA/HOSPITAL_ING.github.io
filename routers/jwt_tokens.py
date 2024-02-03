from jwt import encode, decode

def generate_jwt_token(data: dict):
    token: str = encode(payload=data, key="ING", algorithm="HS256")
    return token

def validate_jwt_token(token: str) -> dict:
    data:dict = decode(token, key="ING", algorithms=["HS256"])
    return data
    

            