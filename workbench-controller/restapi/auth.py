from functools import wraps
from flask import request
from h1st_saas import config
import jwt
import logging


logger = logging.getLogger(__name__)


def auth_require():
    def decorator(fn):
        # no auth is enabled, just return original fn
        if not config.RESTAPI_AUTH_STATIC_KEY and not config.RESTAPI_AUTH_JWT_KEY:
            return fn

        @wraps(fn)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            is_authed = False
            auth_reason = "Invalid or missing token"

            if auth_header:
                auth_token = auth_header.split(" ", 1)[-1]
                
                if config.RESTAPI_AUTH_STATIC_KEY and auth_token == config.RESTAPI_AUTH_STATIC_KEY:
                    is_authed = True
                elif config.RESTAPI_AUTH_JWT_KEY:
                    try:
                        decoded_jwt = jwt.decode(
                            auth_token,
                            config.RESTAPI_AUTH_JWT_KEY, algorithms=['HS256'],
                            opions={
                                'require_exp': True,
                                'verify_exp': True
                            }
                        )

                        if 'exp' not in decoded_jwt:
                            raise ValueError('Invalid token, exp claim is missing')

                        is_authed = True
                    except Exception as ex:
                        logger.debug(f'Invalid jwt {ex}')
                        auth_reason = str(ex)

            if not is_authed:
                return {
                    "success": False,
                    "error": {
                        "message": "Unauthorized access",
                        "reason": auth_reason,
                    },
                }, 403

            return fn(*args, **kwargs)

        return decorated

    return decorator
