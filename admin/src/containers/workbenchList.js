import React from 'react';
import WorkbenchService from '../services/workbench';
import { CpuIcon, SyncIcon } from '@primer/octicons-react';

export default class WorkbenchList extends React.Component {
  constructor(props) {
      super(props)

      this.svc = new WorkbenchService();

      this.timer = null;
      this.unmount = false;

      this.state = {
          items: [],
          error: null,
          refreshingItem: null,
      }
  }

  componentDidMount() {
    this.pollForUpdates();
  }

  componentWillUnmount() {
    this.unmount = true;
    if (this.timer) {
      clearTimeout(this.timer);
    }
  }

  pollForUpdates() {
    if (this.timer) {
      clearTimeout(this.timer);
    }

    if (this.unmount) {
      return
    }

    this.svc.listWorkbenches()
      .then(data => {
        this.setState({items: data})
        this.timer = setTimeout(() => this.pollForUpdates(), 3000);
      })
      .catch(err => {
        this.setState({error: err})
      })
  }

  async refreshWorkbench(item) {
    this.setState({ refreshingItem: item.workbench_id });
    try {
      await this.svc.getWorkbench(item);
    } catch (ex) {
      alert(ex)
    }

    setTimeout(() => this.setState({ refreshingItem: null }), 500)
    this.pollForUpdates();
  }

  async startWorkbench(item) {
    try {
      await this.svc.startWorkbench(item);
    } catch (ex) {
      alert(ex)
    }

    this.pollForUpdates();
  }

  async stopWorkbench(item) {
    try {
      await this.svc.stopWorkbench(item);
    } catch (ex) {
      alert(ex)
    }

    this.pollForUpdates();
  }

  async deleteWorkbench(item) {
    if (window.confirm("Do you want to delete this?")) {
      await this.svc.deleteWorkbench(item);
      this.pollForUpdates()
    }
  }

  render() {
      const items = this.state.items.map(
          item => {
              return (
                  <tr key={item.workbench_id}>
                      <td>
                        <a href={`${item.public_endpoint}#/home/project`} target="_blank" rel="noopener noreferrer">
                          {item.workbench_id}
                        </a>
                        <div className="subTitle">
                          {item.allocated_instance_id ? <CpuIcon title="Dedicated" size={12} /> : ""}
                          &nbsp;
                          {item.instance_id || item.allocated_instance_id}
                        </div>
                      </td>
                      <td>
                          {item.workbench_name}
                          <div style={{fontSize: "0.5em"}}>{item.user_id}</div>
                      </td>
                      <td>
                        CPU: <input type="text" size={6} defaultValue={item.requested_cpu} disabled /><br/>
                        RAM: <input type="text" size={6} defaultValue={item.requested_memory} disabled /> <br/>
                      </td>
                      <td>{this.renderStatus(item)}</td>
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
                  <th>Name</th>
                  <th>Resource</th>
                  <th>Status</th>
                  <th></th>
              </tr>
              </thead>
              <tbody>{items}</tbody>
          </table>
      );
  }

  renderStatus(item) {
      if (item.status === 'running') {
          return <span className="badge badge-primary">{item.status}</span>
      } else if (item.status === 'stopped') {
          return <span className="badge badge-secondary">{item.status}</span>
      } else {
        return <span className="badge badge-warning">{item.status}</span>
      }
  }

  renderActions(item) {
      const buttons = []

      if (item.status === 'stopped') {
        buttons.push(
          <button key="start" onClick={() => this.startWorkbench(item)} className="btn btn-sm btn-outline-secondary">Start</button>
        )
      } else {
        buttons.push(
          <button key="stop" onClick={() => this.stopWorkbench(item)} className="btn btn-sm btn-outline-secondary">Stop</button>
        )
      }

      buttons.push(<span key="placeholder"> </span>)

      buttons.push(
        <button key="del" onClick={() => this.deleteWorkbench(item)} className="btn btn-sm btn-outline-danger">Delete</button>
      )

      if (item.status !== "stopped") {
        let btnClass = ""

        if (this.state.refreshingItem === item.workbench_id) {
          btnClass += " rotatingAnimation"
        }

        buttons.push(" ")
        buttons.push(
          <button key="refresh" onClick={() => this.refreshWorkbench(item)} className="btn btn-sm btn-outline-secondary">
            <SyncIcon className={btnClass} />
          </button>
        )
      }

      return buttons;
  }
}
