import React from 'react';
import WorkbenchService from '../services/workbench';

export default class InstanceList extends React.Component {
  constructor(props) {
      super(props)

      this.svc = new WorkbenchService(props.apiUrl);

      this.timer = null;

      this.state = {
          items: [],
          error: null
      }
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (nextProps.apiUrl !== this.props.apiUrl) {
      this.svc = new WorkbenchService(nextProps.apiUrl);
      this.pollForUpdates()
    }

    return true
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

  async startInstance(item) {
    await this.svc.startInstance(item.id)

    this.pollForUpdates()
  }

  async stopInstance(item) {
    await this.svc.stopInstance(item.id)

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
                        <strong>CPU</strong>: {item.resources.CPU.available} / {item.resources.CPU.total}<br/>
                        <strong>Memory</strong>: {item.resources.MEMORY.available} / {item.resources.MEMORY.total}<br/>
                        {item.resources.GPU ? 
                          <div>
                            <strong>GPU</strong>: {item.resources.GPU.available} / {item.resources.GPU.total}<br/>
                          </div> :
                          ""
                        }
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
                  <th>Resource</th>
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
    let buttons = []

    if (!item.capacityProviderName) {
      if (!item.agentConnected) {
        buttons.push(
          <button key="start" onClick={() => this.startInstance(item)} className="btn btn-sm btn-outline-secondary">Start</button>
        )
      } else {
        buttons.push(
          <button key="stop" onClick={() => this.stopInstance(item)} className="btn btn-sm btn-outline-secondary">Stop</button>
        )
      }

      buttons.push(" ")
    }

    buttons.push(
      <button key="drain" onClick={() => this.drainInstance(item)} className="btn btn-sm btn-outline-danger">Drain</button>
    )

    return buttons
  }
}
