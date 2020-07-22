# Retic
from retic import App as app

# Requests
import requests

# Constantes
URL_IMAGE = app.apps['backend']['imgur']['base_url'] + \
    app.apps['backend']['imgur']['image']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Authorization': 'Client-ID ' + app.config.get('IMGUR_CLIENT_ID')
}


def upload_image(image):
    """Upload a image to imgur and return a object

    :param image: Image to upload
    """

    """Prepare payload for the request"""
    _payload = {
        u'image': image
    }
    """Upload the file"""
    _uploaded_image = requests.post(
        URL_IMAGE,
        data=_payload,
        headers=HEADERS
    )
    """Get the JSON from the response"""
    _uploaded_image_json = _uploaded_image.json()
    """Return data"""
    return _uploaded_image_json
