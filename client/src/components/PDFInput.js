
import React, { useState, useEffect } from 'react';

function PDFInput({ onSubmit }) {
  const [loading, setLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8080/embed-and-store', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pdf: selectedPDF }),
      });

      if (response.ok) {
        const data = await response.json();
        setResponseMessage(data.message);
        // Callback to App.js to trigger UI transition
        onSubmit();
      } else {
        setResponseMessage('Error: Something went wrong.');
      }
    } catch (error) {
      console.error('Error:', error);
      setResponseMessage('Error: Something went wrong.');
    } finally {
      setLoading(false);
    }
  }

  const [pdfs, setPdfs] = useState([]);
  const [selectedPDF, setSelectedPDF] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8080/get-pdfs', {
        method: 'GET'
      });

      console.log(response);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setPdfs(data);
    } catch (error) {
      console.error('Error fetching PDFs:', error);
    }
  };

  useEffect(() => {
    console.log('Fetching PDFs...');
    fetchData();
  }, []);

  const handlePDFSelect = async (pdf) => {
    setSelectedPDF(pdf);
  }


  return (
    <div className="pdfinput">
      <div style={{ marginBottom: '150px' }}>
        <h1>PDF Chatbot</h1>
      </div>
      <div style={{ marginBottom: '50px' }}>
        <select onChange={(e) => handlePDFSelect(e.target.value)}>
          <option value="">Select a PDF to ask question</option>
          {pdfs && pdfs.map((pdf, index) => (
            <option key={index} value={pdf}>
              {pdf}
            </option>
          ))}
        </select>
      </div>
      <div>
        <button onClick={handleSubmit} disabled={loading}>
          {loading ? 'Building Index...' : 'Submit'}
        </button>
      </div>
      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
}

export default PDFInput;