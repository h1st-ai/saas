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

## Deployment

To deploy

```
PUSH=yes ./build.sh && ./deploy.sh
```

Currently, it is deployed manually on `10.30.0.142`, and the permissions was created manually for user `h1st_saas`.

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

Create new workbenches for a user
IMPORTANT: call /workbenches/{wid} after creating/starting workbench until the status is **running**

```
POST /workbenches?user_id=xyz

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

## References

  * ECR requires user to enable long tag ARN setting. This was done manually. See [this](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-modifying-longer-id-settings.html).
