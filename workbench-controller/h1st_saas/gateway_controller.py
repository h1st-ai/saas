import os
import yaml
import tempfile
import shutil
import h1st_saas.config as config

class GatewayController:
    def __init__(self):
        os.makedirs(config.TRAEFIK_CONF_DIR, exist_ok=True)

    def setup(self, obj_type, obj_id, endpoint):
        if obj_type == 'project':
            cfg_id = "wb-" + obj_id
            mw = ['strip_project']
            path_prefix = f'/project/{obj_id}/'
        elif obj_type == 'deployment':
            cfg_id = "deployment-" + obj_id
            mw = ['strip_deployment']
            path_prefix = f'/deployment/{obj_id}/'
        else:
            raise Exception(f'Gateway for "{obj_type}" is not supported')

        if config.TRAEFIK_AUTH_MIDDLEWARE:
            mw = [config.TRAEFIK_AUTH_MIDDLEWARE] + mw

        cfg = {'http': {'services': {}, 'routers': {}}}

        cfg['http']['routers'][cfg_id] = {
            'rule': f"PathPrefix(`{path_prefix}`)",
            'service': cfg_id,
            'middlewares': mw,
        }

        cfg['http']['services'][cfg_id] = {
            'loadBalancer': {
                'servers': [{'url': endpoint}],
                'healthcheck': {
                    'path': '/',
                    'interval': 10,
                    'timeout': 3,
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            try:
                yaml.dump(cfg, f)
                f.flush()

                shutil.move(f.name, os.path.join(config.TRAEFIK_CONF_DIR, cfg_id + ".yml"))
            except:
                os.unlink(f.name)
                raise

    def destroy(self, obj_type, obj_id):
        if obj_type == 'project':
            cfg_id = "wb-" + obj_id
        elif obj_type == 'deployment':
            cfg_id = "wb-" + obj_id
        else:
            raise Exception(f'Gateway for "{obj_type}" is not supported')

        f = os.path.join(config.TRAEFIK_CONF_DIR, cfg_id + ".yml")

        if os.path.exists(f):
            os.unlink(f)
            return True

        return False

    def sync_all(self):
        # TODO: sync all gateway instances
        pass
