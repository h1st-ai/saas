## Workbench Controller

REST API to manage the workbench contaienr instances.
To start:

  * Install all requirements in requirements.txt
  * Run `./server.sh`

Config will be read via environment variables defined in `config.py`.
If there is a `.env` on the current directory, it will also read from that file.

Default port is `8999`.


## API

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

```
POST /workbenches
Content-Type: application/json
{
  "user_id": "xyz"
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

Query status of a workbench. IMPORTANT: call this after creating/starting workbench to make sure status is **running**

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

