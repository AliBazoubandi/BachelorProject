import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Form, Button, Pagination } from 'react-bootstrap';


const IPClusters = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [rowsPerPage] = useState(10);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/api/ipClusters', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setData(response.data);
        setFilteredData(response.data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchData();
  }, []);

  const handleSearch = () => {
    const searchTerm = search.toLowerCase();
    const filtered = data.filter(item =>
      item[0].toLowerCase().includes(searchTerm) // Filtering by IP address
    );
    setFilteredData(filtered);
    setCurrentPage(1); // Reset to first page when searching
  };

  // Pagination logic
  const indexOfLastRow = currentPage * rowsPerPage;
  const indexOfFirstRow = indexOfLastRow - rowsPerPage;
  const currentRows = filteredData.slice(indexOfFirstRow, indexOfLastRow);
  const totalPages = Math.ceil(filteredData.length / rowsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  // Create pagination items
  const paginationItems = [];
  if (totalPages > 1) {
    paginationItems.push(
      <Pagination.Prev
        key="prev"
        onClick={() => handlePageChange(currentPage - 1)}
        disabled={currentPage === 1}
      />
    );

    if (currentPage > 3) {
      paginationItems.push(<Pagination.Ellipsis key="start-ellipsis" />);
    }

    for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
      paginationItems.push(
        <Pagination.Item
          key={i}
          active={i === currentPage}
          onClick={() => handlePageChange(i)}
        >
          {i}
        </Pagination.Item>
      );
    }

    if (currentPage < totalPages - 2) {
      paginationItems.push(<Pagination.Ellipsis key="end-ellipsis" />);
    }

    paginationItems.push(
      <Pagination.Next
        key="next"
        onClick={() => handlePageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
      />
    );
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="data-container">
      <h2>IP Clusters</h2>
      <Form inline className="mb-3">
        <Form.Control
          type="text"
          placeholder="Search by IP address"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <Button variant="primary" onClick={handleSearch}>Search</Button>
      </Form>
      <Table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>IPv4 Address</th>
            <th>Total In Bytes</th>
            <th>Total Out Bytes</th>
            <th>Total In Packets</th>
            <th>Total Out Packets</th>
            <th>Risk Category</th>
          </tr>
        </thead>
        <tbody>
          {currentRows.map((item, index) => (
            <tr key={index}>
              <td>{item[0]}</td>
              <td>{item[1]}</td>
              <td>{item[2]}</td>
              <td>{item[3]}</td>
              <td>{item[4]}</td>
              <td>{item[5]}</td>
              <td>{item[6]}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      <Pagination>{paginationItems}</Pagination>
    </div>
  );
};

export default IPClusters;