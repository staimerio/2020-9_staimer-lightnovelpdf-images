# Retic
from retic import Request, Response, Next

# Services
from retic.services.validations import validate_obligate_fields
from retic.services.responses import success_response_service, error_response_service
import services.images.images as images


def upload_from_url(req: Request, res: Response, next: Next):
    """Upload images from urls"""

    """Check that all parameters are valid"""
    _validate = validate_obligate_fields({
        u'urls': req.param('urls'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The param {} is necesary.".format(_validate["error"])
            )
        )
    """Upload images"""
    _uploaded_images = images.upload_from_url_watermark(
        req.param("urls"),
        req.param("width"),
        req.param("height"),
        req.param("watermark_code"),
        req.param("headers"),
        req.param("left_crop"),
        req.param("top_crop"),
        req.param("right_crop"),
        req.param("bottom_crop"),
    )
    """Check if the response has any problem"""
    if _uploaded_images['valid'] is False:
        return res.bad_request(_uploaded_images)

    """Transform data response"""
    _data_response = {
        u"images": _uploaded_images.get('data')
    }
    """Response to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg='Images uploaded.'
        )
    )
