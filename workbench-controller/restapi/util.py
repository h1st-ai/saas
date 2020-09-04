from flask import request, make_response
from werkzeug.exceptions import HTTPException

def get_user_id():
    if 'user_id' not in request.args:
        raise HTTPException(
            400, 
            response=make_response({
                'success': False,
                'error': {
                    'message': 'user_id is missing'
                }
            })
        )

    return request.args.get('user_id')
