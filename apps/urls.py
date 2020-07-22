# Retic
from retic import App as app

"""Define all other apps"""
BACKEND_IMGUR = {
    u"base_url": app.config.get('APP_BACKEND_IMGUR'),
    u"image": "/image",
}

APP_BACKEND = {
    u"imgur": BACKEND_IMGUR,
}

"""Add Backend apps"""
app.use(APP_BACKEND, "backend")
