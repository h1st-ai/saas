export const BASE_URLS = {
  staging: 'http://10.30.128.207:8999',
  prod: 'http://10.30.0.142:8999',
  local: 'http://localhost:8999',
}

export default class WorkbenchService {
  constructor(baseUrl = "") {
    if (!baseUrl) {
      baseUrl = BASE_URLS.prod
    }

    this.baseUrl = baseUrl
  }

  async listWorkbenches() {
    const resp = await fetch(this.baseUrl + '/workbenches?user_id=');
    const data = await resp.json();
    return data.items;
  }

  async startWorkbench(item) {
    const resp = await fetch(this.baseUrl + `/workbenches/${item.workbench_id}/start?user_id=${item.user_id}`, {
      method: 'POST'
    });
    const apiResp = await resp.json();

    if (!apiResp.success) {
      throw new Error(apiResp.error.message + "\n" + apiResp.error.reason);
    }
  }

  async getWorkbench(item) {
    const resp = await fetch(this.baseUrl + `/workbenches/${item.workbench_id}?user_id=${item.user_id}`);
    return (await resp.json())['item'];
  }

  async stopWorkbench(item) {
    const resp = await fetch(this.baseUrl + `/workbenches/${item.workbench_id}/stop?user_id=${item.user_id}`, {
      method: 'POST'
    });
    await resp.json();
  }

  async deleteWorkbench(item) {
    const resp = await fetch(this.baseUrl + `/workbenches/${item.workbench_id}?user_id=${item.user_id}`, {
      method: 'DELETE'
    });
    await resp.json();
  }

  async listInstances() {
    const resp = await fetch(this.baseUrl + `/instances`);
    return (await resp.json()).items
  }

  async drainInstance(iid) {
    const resp = await fetch(this.baseUrl + `/instances/${iid}/drain`, {
      method: 'POST'
    });
    return (await resp.json())
  }

  async startInstance(iid) {
    const resp = await fetch(this.baseUrl + `/instances/${iid}/start`, {
      method: 'POST'
    });
    return (await resp.json())
  }

  async stopInstance(iid) {
    const resp = await fetch(this.baseUrl + `/instances/${iid}/stop`, {
      method: 'POST'
    });
    return (await resp.json())
  }
}
