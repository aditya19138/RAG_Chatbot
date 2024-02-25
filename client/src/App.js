import React, { useState, useEffect } from 'react';
import PDFInput from './components/PDFInput';
import ChatInterface from './components/ChatInterface';

function App() {
  const [showChat, setShowChat] = useState(false); // Add state to control UI transition

  const handlePDFSubmitted = () => {
    setShowChat(true); // Transition to the ChatInterface
  };

  return (
    <div className="App">

      {!showChat ? (
        <PDFInput onSubmit={handlePDFSubmitted} />
      ) : (
        <ChatInterface />
      )}
    </div>
  );
}

export default App;