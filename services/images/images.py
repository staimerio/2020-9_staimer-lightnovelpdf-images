"""Services for Images controller"""

# Retic
from retic import env, App as app

# Requests
import requests

# Pil
from PIL import Image

# Io
import io

# Base64
import base64

# Uuid
import uuid

# Asyncio
import asyncio

# Aiohttp
import aiohttp

# Services
from retic.services.responses import success_response_service, error_response_service
import services.imgur.imgur as imgur

# Utils
from services.general.general import isfile, rmfile

# Contants
PUBLIC_WATERMARKS_FOLDER = app.config.get('PUBLIC_WATERMARKS_FOLDER')
PUBLIC_IMAGES_FOLDER = app.config.get('PUBLIC_IMAGES_FOLDER')
PUBLIC_IMG_NOT_FOUND = app.config.get('PUBLIC_IMG_NOT_FOUND')


def upload_from_url_watermark(
    urls, width, height, watermark_code=None, headers={},
    left_crop=None, top_crop=None, right_crop=None, bottom_crop=None
):
    """Upload images from urls and if the watermarks params contains some
    watermark these will add to images, one in each corner

    :param urls: List of images urls to upload
    :param watermark_code: Code of the watermark to add on each image
    """
    """Define all variables"""
    _images = []
    max = 5
    try:
        async def get_download_item_req(url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:
                    idx = 0
                    _downloaded_image = await response.read()
                    if _downloaded_image:
                        if watermark_code or left_crop or top_crop or right_crop or bottom_crop:
                            """If watermark exists, add to image"""
                            _downloaded_image = img_watermark(
                                _downloaded_image,
                                width,
                                height,
                                watermark_code,
                                left_crop=left_crop, top_crop=top_crop, right_crop=right_crop, bottom_crop=bottom_crop
                            )
                    else:
                        """Upload image base"""
                        _downloaded_image = open(
                            PUBLIC_IMG_NOT_FOUND, "rb").read()
                    while idx < max:
                        """Upload image to storage"""
                        # _uploaded_image = await imgur.async_upload_image(
                        #     _downloaded_image,
                        # )
                        _uploaded_image = imgur.upload_image(
                            _downloaded_image,
                        )
                        """Check if it has any problem"""
                        if not _uploaded_image or _uploaded_image['success'] is False:
                            continue
                        else:
                            """Add image to list"""
                            _images.append((
                                {
                                    **_uploaded_image.get('data'),
                                    u'url': url
                                }
                            ))
                            break

        async def main():
            promises = [get_download_item_req(_url)
                        for _url in urls]
            await asyncio.gather(*promises)

        asyncio.run(main())
        return success_response_service(
            data=_images
        )
    except Exception as err:
        print(err)
        return error_response_service(
            msg=str(err)
        )


def download_img(download_url, headers):
    """Download from the url"""
    req_download = requests.get(download_url, headers=headers)
    """Check if the response has any problem"""
    if req_download.status_code != 200:
        return None
    else:
        """Exit from the loop"""
        return req_download.content


def img_watermark(
    bytes_image,
    width,
    height,
    watermark_code,
    left_crop=None, top_crop=None, right_crop=None, bottom_crop=None
):
    """Load the Image from memory"""
    _base_image = Image.open(io.BytesIO(bytes_image))
    """Crop"""
    _left_crop = left_crop or 0
    _top_crop = top_crop or 0
    _bottom_crop = (
        _base_image.height - bottom_crop) if bottom_crop and bottom_crop < _base_image.height else _base_image.height
    _right_crop = (
        _base_image.height - right_crop) if right_crop and right_crop < _base_image.width else _base_image.width
    if _left_crop or _top_crop or _bottom_crop or _right_crop:
        _base_image = _base_image.crop(
            (_left_crop, _top_crop, _right_crop, _bottom_crop))

    if width or height:
        """Get size from images"""
        _img_width = width or _base_image.width
        _img_height = height or _base_image.height
        """Define the size"""
        _img_size = (_img_width, _img_height,)
        """Resize image"""
        _base_image = _base_image.resize(_img_size)

    """Get the watermark position"""
    if watermark_code:
        """Define file paths"""
        _watermark_path = "{0}/{1}".format(
            PUBLIC_WATERMARKS_FOLDER, watermark_code)
        """Check if mark exists"""
        if not isfile(_watermark_path):
            raise Exception("Watermark not found.")

        """Open the watermark if it exists"""
        _watermark = Image.open(_watermark_path)
        _watermark_width, _watermark_height = _watermark.size
        _position = (
            int((_img_width-_watermark_width)/2),
            _img_height-(_watermark_height+5)
        )
        """Paste watermark into image"""
        _base_image.paste(_watermark, _position, mask=_watermark)

    """Generate id"""
    _img_code = uuid.uuid1().hex
    """Path of the image"""
    _output_image_path = "{0}/{1}.png".format(PUBLIC_IMAGES_FOLDER, _img_code)
    """Save image"""
    _base_image.save(_output_image_path)
    """Open image"""
    with open(_output_image_path, "rb") as image_file:
        _image = base64.b64encode(image_file.read())
    """Delete image"""
    rmfile(_output_image_path)
    """Return Image"""
    return _image
