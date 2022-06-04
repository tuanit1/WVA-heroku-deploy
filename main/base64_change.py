import base64
def encode_Str(values):
    return base64.b64encode(values.encode('utf-8')).decode('utf-8')
    
def decode_Str(values):
    return base64.b64decode(values).decode('utf-8')