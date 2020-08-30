import os

RESTAPI_URL_PREFIX = os.environ.get('RESTAPI_URL_PREFIX', '/')
RESTAPI_AUTH_JWT_KEY = os.environ.get('RESTAPI_AUTH_JWT_KEY', None)
RESTAPI_AUTH_STATIC_KEY = os.environ.get('RESTAPI_AUTH_STATIC_KEY', None)

TRAEFIK_CONF_DIR = os.environ.get(
    'TRAEFIK_CONF_DIR', 
    os.path.dirname(__file__) + '/../traefik-config'
)

# no trailing slash
BASE_URL = "https://cloud.h1st.ai/project"
WB_BOOT_COMMAND = "exec /app.sh"

WB_DEFAULT_CPU = 1024
WB_DEFAULT_RAM = 2048

ECS_MAX_WB = int(os.environ.get('ECS_MAX_WB', 0))

ECS_CLUSTER = "H1st"
ECS_TASK_DEFINITION = "workbench"

DYNDB_TABLE = "H1st_saas_workbench"

# make aws sdk works correctly
AWS_REGION = "us-west-1"
os.environ['AWS_DEFAULT_REGION'] = AWS_REGION
