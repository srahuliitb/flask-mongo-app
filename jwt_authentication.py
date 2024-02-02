import jwt

# key = "secret"
# encoded_jwt = jwt.encode({"some": "payload"}, key, algorithm="HS256")
# print(encoded_jwt)

def jwt_encode(dict_obj, secret_key):
    return jwt.encode(dict_obj, secret_key, algorithm='HS256')

def jwt_decode(encoded, secret_key):
    return jwt.decode(encoded, secret_key, options={"verify_signature": True}, algorithms='HS256')

