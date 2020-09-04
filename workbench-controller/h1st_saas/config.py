import os

RESTAPI_URL_PREFIX = os.environ.get('RESTAPI_URL_PREFIX', '/')
RESTAPI_AUTH_JWT_KEY = os.environ.get('RESTAPI_AUTH_JWT_KEY', None)
RESTAPI_AUTH_STATIC_KEY = os.environ.get('RESTAPI_AUTH_STATIC_KEY', None)

TRAEFIK_CONF_DIR = os.environ.get(
    'TRAEFIK_CONF_DIR', 
    os.path.dirname(__file__) + '/../traefik-config'
)
TRAEFIK_AUTH_MIDDLEWARE = os.environ.get('TRAEFIK_AUTH_MIDDLEWARE', '')

# make aws sdk works correctly
AWS_REGION = "us-west-1"
os.environ['AWS_DEFAULT_REGION'] = AWS_REGION

ECS_CLUSTER = "H1st"

# ----------------------------------
# workbench
# ----------------------------------
# no trailing slash
WB_BASE_URL = "https://cloud.h1st.ai/project"

WB_BOOT_COMMAND = "exec /app.sh"

WB_DEFAULT_CPU = 1024
WB_DEFAULT_RAM = 2048

# set to public to make sure public endpoint is ready before mark it ready
WB_VERIFY_ENDPOINT = os.environ.get('WB_VERIFY_ENDPOINT', '')

WB_ECS_MAX = int(os.environ.get('WB_ECS_MAX', 0))

WB_ECS_TASK_DEFINITION = "workbench"

WB_DYNDB_TABLE = "H1st_saas_workbench"


# ----------------------------------
# inference
# ----------------------------------
# no trailing slash
INFERENCE_BASE_URL = "https://cloud.h1st.ai/inference"

INFERENCE_BOOT_COMMAND = "exec /app.sh"

INFERENCE_DEFAULT_CPU = 1024
INFERENCE_DEFAULT_RAM = 2048

# set to public to make sure public endpoint is ready before mark it ready
INFERENCE_VERIFY_ENDPOINT = os.environ.get('INFERENCE_VERIFY_ENDPOINT', '')

INFERENCE_ECS_MAX = int(os.environ.get('INFERENCE_ECS_MAX', 0))

INFERENCE_ECS_TASK_DEFINITION = "inference"

INFERENCE_DYNDB_TABLE = "H1st_saas_inference"