## Workbench Controller

REST API to manage the workbench contaienr instances.
To start:

  * Install all requirements in requirements.txt
  * Run `./server.sh`

Config will be read via environment variables defined in `config.py`.
If there is a `.env` on the current directory, it will also read from that file.

Default port is `8999`.

## Workbench Image

Workbench controller uses image from `394497726199.dkr.ecr.us-west-1.amazonaws.com/h1st/workbench:latest`.
Push to that repo, then start/stop again to use latest image.

Currently, it always deploy latest image from the container, versioning will come later.

**IMPORTANT**: Workbench controller overrides the command of the container to do some setup before starting the workbench.
To update the command, go to `config.py` and edit the `WB_BOOT_COMMAND`.

## Workbench Storage

All the file systems of the workbences are stored under EFS. The EFS is mounted and symlink to current working folder.

## Deployment

To deploy

```
PUSH=yes ./build.sh && ./deploy.sh
```

Currently, it is deployed manually on `10.30.0.142`, and the permissions was created manually for user `h1st_saas`.

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

IMPORTANT: call /workbenches/{wid} after creating/starting workbench until the status is **running**

```
POST /workbenches?user_id=xyz
Content-Type: application/json
{
  "workbench_name": "AutoCyber"
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
    "public_endpoint": "https://cloud.h1st.ai/project/xyz"
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
