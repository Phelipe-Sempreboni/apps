import React, { useState, useEffect } from 'react';

const DatasetList = () => {
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    // Fetch datasets from API
    fetch('/api/datasets')
      .then(response => response.json())
      .then(data => setDatasets(data));
  }, []);

  return (
    <div className="container">
      {datasets.map(dataset => (
        <div key={dataset.id} className="card">
          <h2>{dataset.name}</h2>
          <p>{dataset.description}</p>
        </div>
      ))}
    </div>
  );
};

export default DatasetList;
