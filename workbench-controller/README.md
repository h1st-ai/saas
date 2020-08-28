## Workbench Controller

REST API to manage the workbench contaienr instances.
To start:

  * Install all requirements in requirements.txt
  * Run `./server.sh`

Config will be read via environment variables defined in `config.py`.
If there is a `.env` on the current directory, it will also read from that file.

Default port is `8999`.


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
IMPORTANT: call this after creating/starting workbench to make sure status is **running**

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
IMPORTANT: call this after creating/starting workbench to make sure status is **running**

```
GET /workbenches/{wid}
Content-Type: application/json

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
IMPORTANT: call this after creating/starting workbench to make sure status is **running**

```
POST /workbenches/{wid}/start

Response
{
  "success": true
}
```

Stop a workbench. If the workbench is already stopped, then this API does nothing
```
POST /workbenches/{wid}/stop

Response
{
  "success": true
}
```
