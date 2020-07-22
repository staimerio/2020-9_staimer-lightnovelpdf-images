# Retic
from retic import Router

# Controllers
import controllers.images as images

"""Define all routes"""
router = Router()

"""Define all paths - /images"""
router \
    .post("/images/remote", images.upload_from_url)
