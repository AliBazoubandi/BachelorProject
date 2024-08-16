import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import HighTrafficIPs from './components/HighTrafficIPs';
import ProtocolUsage from './components/ProtocolUsage';
import Anomalies from './components/Anomalies';
import IPClusters from './components/IPClusters'; 
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/high-traffic-ips" element={<HighTrafficIPs />} />
          <Route path="/protocol-usage" element={<ProtocolUsage />} />
          <Route path="/anomalies" element={<Anomalies />} />
          <Route path="/ip-clusters" element={<IPClusters />} /> 
        </Routes>
      </div>
    </Router>
  );
}

export default App;
