import os

RESTAPI_URL_PREFIX = os.environ.get('RESTAPI_URL_PREFIX', '/')
RESTAPI_AUTH_JWT_KEY = os.environ.get('RESTAPI_AUTH_JWT_KEY', None)
RESTAPI_AUTH_STATIC_KEY = os.environ.get('RESTAPI_AUTH_STATIC_KEY', None)
RESTAPI_CORS_ORIGIN = os.environ.get('RESTAPI_CORS_ORIGIN', '')

TRAEFIK_CONF_DIR = os.environ.get(
    'TRAEFIK_CONF_DIR', 
    os.path.dirname(__file__) + '/../traefik-config'
)
TRAEFIK_AUTH_MIDDLEWARE = os.environ.get('TRAEFIK_AUTH_MIDDLEWARE', '')

# no trailing slash
BASE_URL = os.environ.get('BASE_URL', 'https://cumulus.h1st.ai/project')
WB_BOOT_COMMAND = "exec /app.sh"

WB_DEFAULT_CPU = int(os.environ.get('WB_DEFAULT_CPU', '1024'))
WB_DEFAULT_RAM = int(os.environ.get('WB_DEFAULT_RAM', '2048'))

# set to public to make sure public endpoint is ready before mark it ready
WB_VERIFY_ENDPOINT = os.environ.get('WB_VERIFY_ENDPOINT', '')

ECS_MAX_WB = int(os.environ.get('ECS_MAX_WB', 0))

ECS_CLUSTER = os.environ.get('ECS_CLUSTER', 'H1st')
ECS_TASK_DEFINITION = os.environ.get('ECS_TASK_DEFINITION', "workbench")

DYNDB_TABLE = os.environ.get('DYNDB_TABLE', 'H1st_saas_workbench')

GA_ID = os.environ.get('GA_ID', 'UA-40192392-8')

# make aws sdk works correctly
AWS_REGION = "us-west-1"
os.environ['AWS_DEFAULT_REGION'] = AWS_REGION
