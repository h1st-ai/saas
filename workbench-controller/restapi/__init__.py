from flask import Blueprint, current_app, request
from h1st_saas.workbench_controller import WorkbenchController

bp = Blueprint('restapi', __name__)

@bp.route("/workbenches")
def workbenches_list():
    return {
        "success": True,
        "items": WorkbenchController().list_workbench("bao")
    }

@bp.route("/workbenches", methods=["POST"])
def workbenches_launch():
    data = request.get_json()
    if not data or 'user_id' not in data or not data['user_id']:
        return {
            'success': False,
            'error': {
                'message': 'Request body must be JSON object with "user_id" field',
            }
        }, 400

    try:
        wb = WorkbenchController()
        wid = wb.launch(data['user_id'])

        return {
            'success': True,
            'item': {
                'user_id': data['user_id'],
                'workbench_id': wid,
            }
        }, 201
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to launch new workbench',
                'reason': str(ex),
            }
        }, 500

@bp.route("/workbenches/<wid>")
def workbenches_get(wid):
    return {
        "success": True,
        "item": WorkbenchController().get("bao", wid)
    }
