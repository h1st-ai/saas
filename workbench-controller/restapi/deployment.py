from flask import Blueprint, current_app, request, json
from h1st_saas import DeploymentController
from .auth import auth_require
from .util import get_user_id

bp = Blueprint('deployment_api', __name__)

@bp.route("/deployments")
@auth_require()
def all():
    return {
        "success": True,
        "items": DeploymentController().all(get_user_id())
    }


@bp.route("/deployments", methods=["POST"])
@auth_require()
def deploy():
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
        dc = DeploymentController()
        did = dc.launch(uid, data.get('deployment_name', ''))

        return {
            'success': True,
            'item': {
                'user_id': uid,
                'deployment_id': did,
            }
        }, 201
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to launch new deployment',
                'reason': str(ex),
            }
        }, 500


@bp.route("/deployments/<did>")
@auth_require()
def get(did):
    uid = get_user_id()

    try:
        return {
            "success": True,
            "item": DeploymentController().get(uid, did, True)
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to get deployment status',
                'reason': str(ex),
            }
        }, 500


@bp.route("/deployments/<did>", methods=["DELETE"])
@auth_require()
def undeploy(did):
    uid = get_user_id()

    try:
        DeploymentController().destroy(uid, did)

        return {
            "success": True,
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to delete deployment',
                'reason': str(ex)
            }
        }, 500


@bp.route("/deployments/<did>/start", methods=["POST"])
@auth_require()
def start(did):
    uid = get_user_id()
    try:
        DeploymentController().start(uid, did)

        return {
            "success": True,
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to start deployment',
                'reason': str(ex)
            }
        }, 500


@bp.route("/deployments/<did>/stop", methods=["POST"])
@auth_require()
def stop(did):
    uid = get_user_id()
    try:
        DeploymentController().stop(uid, did)

        return {
            "success": True,
        }
    except Exception as ex:
        return {
            'success': False,
            'error': {
                'message': 'Unable to stop deployment',
                'reason': str(ex)
            }
        }, 500
