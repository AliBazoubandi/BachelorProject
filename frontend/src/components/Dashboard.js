import React from 'react';
import { Link } from 'react-router-dom';
import './Dashboard.css';

function Dashboard() {
    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>Network Analysis Dashboard</h1>
                <p>Welcome! Select a category below to view the data.</p>
            </header>

            <div className="dashboard-grid">
                <Link to="/high-traffic-ips" className="dashboard-card">
                    <h2>High Traffic IPs</h2>
                    <p>View the IP addresses with the most traffic.</p>
                </Link>

                <Link to="/protocol-usage" className="dashboard-card">
                    <h2>Protocol Usage</h2>
                    <p>Analyze the usage of different network protocols.</p>
                </Link>

                <Link to="/anomalies" className="dashboard-card">
                    <h2>Anomalies</h2>
                    <p>Check for unusual patterns and anomalies in the network.</p>
                </Link>

                <Link to="/ip-clusters" className="dashboard-card">
                    <h2>IP Clusters</h2>
                    <p>View the clustering of IP addresses based on network traffic.</p>
                </Link>
            </div>
        </div>
    );
}

export default Dashboard;