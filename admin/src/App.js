import React, { useState, useEffect } from 'react';
import WorkbenchList from './containers/workbenchList'
import InstanceList from './containers/instanceList'
import { BASE_URLS } from './services/workbench'
import './App.css';

function App() {
  const [ currentTab, setTab ] = useState(0);
  const [ currentEnv, setEnv ] = useState("prod");

  const tabs = [
    {el: WorkbenchList, title: 'Workbenches'},
    {el: InstanceList, title: 'Instances'},
  ];

  useEffect(() => {
    const env = localStorage.getItem('selectedEnv') || 'prod'
    setEnv(env)
  }, []);

  const changeEnv = (e) => {
    localStorage.setItem('selectedEnv', e.target.value)
    setEnv(e.target.value)
  };

  const navs = tabs.map((tab, idx) => {
    let className = "nav-link";

    if (idx === currentTab) {
      className += " active";
    }

    return <li key={idx} className="nav-item">
      <a onClick={() => setTab(idx)} className={className} href="#/">{tab.title}</a>
    </li>
  });

  const TabEl = tabs[currentTab].el

  return (
    <div className="container">
      <div style={{paddingTop: "1em", paddingBottom: "1em"}}>
        <div style={{ paddingBottom: "1em" }}>
          Server: <select value={currentEnv} onChange={el => changeEnv(el)}>
            {Object.keys(BASE_URLS).map(k => 
              <option value={k} key={k}>{k}</option>)
            }
          </select>
        </div>
        <ul className="nav nav-pills">
          {navs}
        </ul>
      </div>
      <div>
        <TabEl apiUrl={BASE_URLS[currentEnv]} />
      </div>
    </div>
  );
}

export default App;
