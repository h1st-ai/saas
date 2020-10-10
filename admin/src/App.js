import React, { useState } from 'react';
import WorkbenchList from './containers/workbenchList'
import InstanceList from './containers/instanceList'
import './App.css';

function App() {
  const [ currentTab, setTab ] = useState(0)

  const tabs = [
    {el: <WorkbenchList />, title: 'Workbenches'},
    {el: <InstanceList />, title: 'Instances'},
  ];

  const navs = tabs.map((tab, idx) => {
    let className = "nav-link";

    if (idx === currentTab) {
      className += " active";
    }

    return <li key={idx} className="nav-item">
      <a onClick={() => setTab(idx)} className={className} href="#/">{tab.title}</a>
    </li>
  });

  return (
    <div className="container">
      <div style={{paddingTop: "1em", paddingBottom: "1em"}}>
        <ul className="nav nav-pills">
          {navs}
        </ul>
      </div>
      <div>
        {tabs[currentTab].el}
      </div>
    </div>
  );
}

export default App;
