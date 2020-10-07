export default class WorkbenchService {
  baseUrl = "http://10.30.0.142:8999"

  async listWorkbenches() {
    const resp = await fetch(this.baseUrl + '/workbenches?user_id=');
    const data = await resp.json();
    return data.items;
  }

  async startWorkbench(item) {
    const resp = await fetch(this.baseUrl + `/workbenches/${item.workbench_id}/start?user_id=${item.user_id}`, {
      method: 'POST'
    });
    await resp.json();
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
}
