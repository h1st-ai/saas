import os

AWS_REGION = "us-west-1"

DYNDB_TABLE = "H1st_saas_workbench"

TRAEFIK_CONF_DIR = os.environ.get(
    'TRAEFIK_CONF_DIR', 
    os.path.dirname(__file__) + '/../traefik-conf'
)

# no trailibg slash
BASE_URL = "https://cloud.h1st.ai/project"

ECS_CLUSTER = "H1st"
ECS_TASK_DEFINITION = "workbench"

# make aws sdk works correctly
os.environ['AWS_DEFAULT_REGION'] = AWS_REGION
