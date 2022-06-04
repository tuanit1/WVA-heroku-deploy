import requests
import json

SERVER_URL = "https://musicfreeworld.com/public/naosteam/watchvideoapp/"
UPLOAD_VIDEO = "https://musicfreeworld.com/public/naosteam/watchvideoapp/uploadImage.php"
IMAGE_DIR = "https://musicfreeworld.com/public/naosteam/watchvideoapp/image/"
DEFAULT_ONESIGNAL_APP_ID = "3819b4be-9a92-441f-9c75-f4d2ae2f9e85"
DEFAULT_REST_API_KEY = "ZWEzOGU0NjAtZmQ0MC00MzhjLTlkMmQtNGZhNGFmZWM4YjQ4"

def executePostRequest(param):
    data = {
        'data': json.dumps(param)
    }
    res = requests.post(SERVER_URL, data=data)
    return json.loads(res.content)
