import os
from h1st_saas import config
import yaml
import tempfile


class GatewayController:
    def __init__(self):
        os.makedirs(config.TRAEFIK_CONF_DIR, exist_ok=True)

    def setup(self, wid, endpoint):
        cfg_id = "wb-" + wid

        cfg = {'http': {'services': {}, 'routers': {}}}

        cfg['http']['routers'][cfg_id] = {
            'rule': f"PathPrefix(`/project/{wid}/`)",
            'service': cfg_id,
            'middlewares': ['strip_project'],
        }

        cfg['http']['services'][cfg_id] = {
            'loadBalancer': {
                'servers': [{'url': endpoint}]
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            yaml.dump(cfg, f)
            f.flush()

            os.rename(f.name, os.path.join(config.TRAEFIK_CONF_DIR, cfg_id + ".yml"))

    def destroy(self, wid):
        f = os.path.join(config.TRAEFIK_CONF_DIR, "wb-" + wid + ".yml")

        if os.path.exists(f):
            os.unlink(f)
            return True

        return False

    def sync_all(self):
        # TODO: sync all gateway instances
        pass
