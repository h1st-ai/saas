## Workbench Controller

TODO
 - [ ] Add a traefik section
 - [ ] Add dynamodb section
 - [ ] Folder structure

REST API to manage the workbench contaienr instances.
To start:

  * Install all requirements in requirements.txt
  * Run `./server.sh`

Config will be read via environment variables defined in `config.py`.
If there is a `.env` on the current directory, it will also read from that file.

Default port is `8999`.

[Architecture](https://drive.google.com/file/d/1tylv9gvNS6XMLHGJ_UVT5CS10SZ_U3Yk/view?usp=sharing)


## Workbench Image

Workbench controller uses image from `394497726199.dkr.ecr.us-west-1.amazonaws.com/h1st/workbench:latest`.

```
REPO=394497726199.dkr.ecr.us-west-1.amazonaws.com
aws ecr get-login-password --region us-west-1 | sudo docker login --username AWS --password-stdin $REPO
docker build . -t h1st/workbench
docker tag h1st/workbench:latest $REPO/h1st/workbench:latest
docker push $REPO/h1st/workbench:latest
```

Current docker file of workbench: https://github.com/h1st-ai/ide

For staging, it will always use the `latest` tag image
For prod, it will use the image defined in `infra/prod/workbench.json`

**IMPORTANT**: Workbench controller overrides the command of the container to do some setup before starting the workbench.
To update the command, go to `config.py` and edit the `WB_BOOT_COMMAND`.

## Troubleshooting

  * Restarting the container inside the instance will make the container unaccessible due to the port is assigned randomly per instance, and ECS does not pick up the updated port.

## Workbench Storage

All the file systems of the workbences are stored under EFS. The EFS is mounted and symlink to current working folder.

## Deployment

To deploy

```
PUSH=yes ./scripts/build.sh && ./scripts/deploy.sh
```

Currently it is deployed manually on `10.30.0.142` (for PROD) and `10.30.128.207` (for STAGING) under `/opt` folder., and the permissions was created manually for user `h1st_saas`.

## Resource Management

The backend relies on ECS to provision the resource for the container. ECS has multiple [providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html) for different instance types, and the backend assigns the workbench to the right provider to minimize the cost and maximize the utilization.

It is also possible to have mix instance types for a single provider and let ECS handles all that, we can explore that in the future.

### Dedicated Instance

It is possible to assign a dedicated EC2 instance for a workbench. When an instance is assigned, it will be started / stopped together with the workbench. When the workbench is deleted, it will also terminate the instance.

## Authentication

To enable authentication, set `RESTAPI_AUTH_STATIC_KEY` or `RESTAPI_AUTH_JWT_KEY` to a secret key in environment or `.env` file.

  * If RESTAPI_AUTH_STATIC_KEY is set, the token is compared with this key
  * If RESTAPI_AUTH_JWT_KEY is set, the token is a JWT token, encoded with HS256. The token must have a valid `exp` claim in future


Currently, the server authentication is not enabled until @khoama is ready.

To authenticate with the API server, use `Authorization` header with bearer token. Example

```
curl -H "Authorization: Bearer xyz" http://server/workbenches?user_id=abc
```

## API

Note: current API requires to pass user via query string. In next version, it will extract directly from keycloak.

List workbenches for a user:

```
GET /workbenches?user_id=xyz

Response
{
  "success": true,
  "items": [
    ...
  ]
}
```

Create new workbenches for a user.

Parameters:
  * `workbench_name`: Use this to pass as an environment variable `WORKBENCH_NAME` to the container
  * `requested_memory`: How much memory in mb to allocate for the instance
  * `requested_cpu`: How many cpu unit to allocate for the instance. 1vCPU = 1024 CPU Unit
  * `requested_gpu`: How many GPU to allocate for the instance (not supported yet)

IMPORTANT: call /workbenches/{wid} after creating/starting workbench until the status is **running**

```
POST /workbenches?user_id=xyz
Content-Type: application/json
{
  "workbench_name": "AutoCyber",
  "requested_memory": 2048,
  "requested_cpu": 1024
}

Response:
{
  "success": true,
  "item": {
    "user_id": "xyz",
    "workbench_id": "abc",
    "public_endpoint": "https://cloud.h1st.ai/project/xyz"
  }
}
```

Get workbench details

```
GET /workbenches/{wid}?user_id=xyz

Response
{
  "success": true,
  "item": {
    "user_id": "xyz",
    "status": "running",
    "workbench_id": "abc",
    "public_endpoint": "https://cloud.h1st.ai/project/xyz",
    "requested_cpu": 123,
    "requested_memory": 123
  }
}
```

Possible statuses: stopped / starting / provisioning / pending / running (these are ECS status)

Start a workbench. If the workbench is already running, then this API does nothing
IMPORTANT: call /workbenches/{wid} after creating/starting workbench until the status is **running**

```
POST /workbenches/{wid}/start?user_id=xyz

Response
{
  "success": true
}
```

Stop a workbench. If the workbench is already stopped, then this API does nothing
```
POST /workbenches/{wid}/stop?user_id=xyz

Response
{
  "success": true
}
```

Destroy a workbench, this will destroy all data of workbecnh
```
DELETE /workbenches/{wid}?user_id=xyz

Response
{
  "success": true
}
```

## References

  * ECR requires user to enable long tag ARN setting. This was done manually. See [this](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-modifying-longer-id-settings.html).
