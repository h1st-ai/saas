import os

RESTAPI_URL_PREFIX = os.environ.get('RESTAPI_URL_PREFIX', '/')
RESTAPI_AUTH_JWT_KEY = os.environ.get('RESTAPI_AUTH_JWT_KEY', None)
RESTAPI_AUTH_DEBUG_KEY = os.environ.get('RESTAPI_AUTH_DEBUG_KEY', None)

TRAEFIK_CONF_DIR = os.environ.get(
    'TRAEFIK_CONF_DIR', 
    os.path.dirname(__file__) + '/../traefik-config'
)

# no trailing slash
BASE_URL = "https://cloud.h1st.ai/project"
WB_BOOT_COMMAND = "exec node /home/theia/src-gen/backend/main.js /home/project/workspace --hostname=0.0.0.0"

ECS_CLUSTER = "H1st"
ECS_TASK_DEFINITION = "workbench"

DYNDB_TABLE = "H1st_saas_workbench"

# make aws sdk works correctly
AWS_REGION = "us-west-1"
os.environ['AWS_DEFAULT_REGION'] = AWS_REGION
