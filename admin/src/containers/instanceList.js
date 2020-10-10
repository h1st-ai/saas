import React from 'react';
import WorkbenchService from '../services/workbench';

export default class InstanceList extends React.Component {
  constructor(props) {
      super(props)

      this.svc = new WorkbenchService();

      this.timer = null;

      this.state = {
          items: [],
          error: null
      }
  }

  componentDidMount() {
    this.pollForUpdates();
  }

  componentWillUnmount() {
    if (this.timer) {
      clearTimeout(this.timer);
    }
  }

  pollForUpdates() {
    if (this.timer) {
      clearTimeout(this.timer);
    }

    this.svc.listInstances()
      .then(data => {
        this.setState({items: data})
        this.timer = setTimeout(() => this.pollForUpdates(), 3000);
      })
      .catch(err => {
        this.setState({error: err})
      })
  }

  async drainInstance(item) {
    await this.svc.drainInstance(item.id)

    this.pollForUpdates()
  }

  render() {
      const items = this.state.items.map(
          item => {
              return (
                  <tr key={item.ec2InstanceId}>
                      <td>
                      {item.ec2InstanceId}<br/>
                      <div className="subTitle">{item.capacityProviderName}</div>
                      </td>
                      <td>{this.renderStatus(item)}</td>
                      <td>
                        {item.runningTasksCount} / {item.pendingTasksCount}
                      </td>
                      <td>
                        {item.resources.CPU.available} / {item.resources.CPU.total}
                      </td>
                      <td>
                        {item.resources.MEMORY.available} / {item.resources.MEMORY.total}
                      </td>
                      <td>{this.renderActions(item)}</td>
                  </tr>
              )
          }
      );

      return (
          <table className="table table-sm table-striped">
              <thead className="thead-dark">
              <tr>
                  <th>ID</th>
                  <th>Status</th>
                  <th>Tasks</th>
                  <th>CPU</th>
                  <th>Memory</th>
                  <th></th>
              </tr>
              </thead>
              <tbody>{items}</tbody>
          </table>
      );
  }

  renderStatus(item) {
      if (item.status === 'ACTIVE') {
          return <span className="badge badge-primary">{item.status}</span>
      } else {
          return <span className="badge badge-secondary">{item.status}</span>
      }
  }

  renderActions(item) {
      return [
        <button key="drain" onClick={() => this.drainInstance(item)} className="btn btn-sm btn-outline-danger">Drain</button>
      ]
  }
}
