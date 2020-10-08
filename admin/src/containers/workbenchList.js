import React from 'react';
import WorkbenchService from '../services/workbench';

export default class WorkbenchList extends React.Component {
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
    // this.svc.listWorkbenches()
    //   .then(data => {
    //     this.setState({items: data})
    //     this.pollForUpdates()
    //   })
    //   .catch(err => this.setState({error: err}))
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

    this.svc.listWorkbenches()
      .then(data => {
        this.setState({items: data})
        this.timer = setTimeout(() => this.pollForUpdates(), 3000);
      })
      .catch(err => {
        this.setState({error: err})
      })
  }

  async startWorkbench(item) {
    await this.svc.startWorkbench(item);
    this.pollForUpdates();
  }

  async stopWorkbench(item) {
    await this.svc.stopWorkbench(item);
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
                      </td>
                      <td>
                          {item.workbench_name}
                          <div style={{fontSize: "0.5em"}}>{item.user_id}</div>
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
      } else {
          return <span className="badge badge-secondary">{item.status}</span>
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

      return buttons;
  }
}