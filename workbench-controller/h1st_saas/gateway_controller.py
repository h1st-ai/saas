import os
from h1st_saas import config
import yaml
import tempfile
import shutil


class GatewayController:
    """
    Generate traefik config file to allow routing from public to private workbench instance
    
    See https://doc.traefik.io/traefik/getting-started/configuration-overview/ for configuration information
    """
    
    def __init__(self):
        os.makedirs(config.TRAEFIK_CONF_DIR, exist_ok=True)

    def setup(self, wid, endpoint):
        cfg_id = "wb-" + wid
        
        # this is required to translate the path between the public url and the workbench instance
        # because the workbench instance works under root (/) while the public url works under /project/xyz
        mw = ['strip_project']

        if config.TRAEFIK_AUTH_MIDDLEWARE:
            mw = [config.TRAEFIK_AUTH_MIDDLEWARE] + mw

        cfg = {'http': {'services': {}, 'routers': {}}}

        cfg['http']['routers'][cfg_id] = {
            'rule': f"PathPrefix(`/project/{wid}/`)",
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

    def destroy(self, wid):
        f = os.path.join(config.TRAEFIK_CONF_DIR, "wb-" + wid + ".yml")

        if os.path.exists(f):
            os.unlink(f)
            return True

        return False

    def sync_all(self):
        # TODO: sync all gateway instances
        pass
