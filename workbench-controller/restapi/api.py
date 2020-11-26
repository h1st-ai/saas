from flask import Blueprint, current_app, request, json, make_response
from werkzeug.exceptions import HTTPException
from h1st_saas.workbench_controller import WorkbenchController
from h1st_saas.workbench_access_controller import WorkbenchAccessController
from h1st_saas.infra_controller import InfraController
from .auth import auth_require

bp = Blueprint('restapi', __name__)

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


@bp.route("/workbenches")
@auth_require()
def workbenches_list():
    return {
        "success": True,
        "items": WorkbenchAccessController().list_workbenches(get_user_id())
    }


@bp.route("/workbenches", methods=["POST"])
@auth_require()
def workbenches_launch():
    data = request.get_json()
    if not data:
        data = {}

    if data and not isinstance(data, dict):
        return {
            'success': False,
            'error': {
                'message': 'Request body must be JSON object',
            }
        }, 400

    uid = get_user_id()

    try:
        wb = WorkbenchController()
        wid = wb.launch(uid, data)

        return {
            'success': True,
            'item': {
                'user_id': uid,
                'workbench_id': wid,
            }
        }, 201
    except Exception as ex:
        current_app.logger.exception('Unable to launch workbench')
        return {
            'success': False,
            'error': {
                'message': 'Unable to launch new workbench',
                'reason': str(ex),
            }
        }, 500


@bp.route("/workbenches/<wid>")
@auth_require()
def workbenches_get(wid):
    uid = get_user_id()

    try:
        return {
            "success": True,
            "item": WorkbenchController().get(uid, wid, True)
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to get workbench status',
                'reason': str(ex),
            }
        }, 500


@bp.route("/workbenches/<wid>", methods=["DELETE"])
@auth_require()
def workbenches_delete(wid):
    uid = get_user_id()

    try:
        WorkbenchController().destroy(uid, wid)
        WorkbenchAccessController().cleanup(wid)

        return {
            "success": True,
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to delete workbench',
                'reason': str(ex)
            }
        }, 500


@bp.route("/workbenches/<wid>/start", methods=["POST"])
@auth_require()
def workbenches_start(wid):
    uid = get_user_id()
    try:
        WorkbenchController().start(uid, wid)

        return {
            "success": True,
        }
    except Exception as ex:
        current_app.logger.exception('Unable to start workbench')
        return {
            'success': False,
            'error': {
                'message': 'Unable to start workbench',
                'reason': str(ex)
            }
        }, 500


@bp.route("/workbenches/<wid>/stop", methods=["POST"])
@auth_require()
def workbenches_stop(wid):
    uid = get_user_id()
    try:
        WorkbenchController().stop(uid, wid)

        return {
            "success": True,
        }
    except Exception as ex:
        current_app.logger.exception('Unable to stop workbench')
        return {
            'success': False,
            'error': {
                'message': 'Unable to stop workbench',
                'reason': str(ex)
            }
        }, 500


@bp.route("/workbenches/<wid>/shares", methods=["GET"])
@auth_require()
def workbenches_shares(wid):
    uid = get_user_id()
    try:
        shares = WorkbenchAccessController().list_shares(workbench_id=wid)

        return {
            "items": shares,
            "success": True,
        }
    except Exception as ex:
        current_app.logger.exception('Unable to retrieve shares')
        return {
            'success': False,
            'error': {
                'message': 'Unable to retrieve shares',
                'reason': str(ex)
            }
        }, 500


@bp.route("/workbenches/<wid>/shares", methods=["POST"])
@auth_require()
def workbenches_add_shares(wid):
    data = request.get_json()
    if not data:
        data = {}

    if not isinstance(data.get('items'), list):
        return {
            'success': False,
            'error': {
                'message': 'Request body must be JSON object',
            }
        }, 400

    uid = get_user_id()
    try:
        WorkbenchAccessController().add_shares(data['items'])

        return {
            "items": WorkbenchAccessController().list_shares(workbench_id=wid),
            "success": True,
        }
    except Exception as ex:
        current_app.logger.exception('Unable to add share')
        return {
            'success': False,
            'error': {
                'message': 'Unable to add share',
                'reason': str(ex)
            }
        }, 500

@bp.route("/instances", methods=["GET"])
@auth_require()
def instances_get():
    try:
        instances = InfraController().list_instances()
        return {
            'success': True,
            'items': list(instances.values())
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to retrieve instance list',
                'reason': str(ex)
            }
        }, 500


@bp.route("/instances/<iid>/drain", methods=["POST"])
@auth_require()
def instance_drain(iid):
    try:
        InfraController().drain_instance(iid)

        return {
            "success": True,
        }
    except Exception as ex:
        current_app.logger.exception('Unable to drain instance')
        return {
            'success': False,
            'error': {
                'message': 'Unable to drain instance',
                'reason': str(ex)
            }
        }, 500


@bp.route("/instances/<iid>/start", methods=["POST"])
@auth_require()
def instance_start(iid):
    try:
        InfraController().start_instance(iid)

        return {"success": True}
    except Exception as ex:
        current_app.logger.exception('Unable to start instance')
        return {
            'success': False,
            'error': {
                'message': 'Unable to start instance',
                'reason': str(ex)
            }
        }, 500


@bp.route("/instances/<iid>/stop", methods=["POST"])
@auth_require()
def instance_stop(iid):
    try:
        InfraController().stop_instance(iid)

        return {"success": True}
    except Exception as ex:
        current_app.logger.exception('Unable to stop instance')
        return {
            'success': False,
            'error': {
                'message': 'Unable to stop instance',
                'reason': str(ex)
            }
        }, 500


@bp.route("/providers", methods=["GET"])
@auth_require()
def provider_get():
    try:
        providers = InfraController().list_providers()
        return {
            'success': True,
            'items': list(providers.values())
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to retrieve provider list',
                'reason': str(ex)
            }
        }, 500





