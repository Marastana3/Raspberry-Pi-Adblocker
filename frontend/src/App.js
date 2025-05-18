import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => setMessage("Error connecting to backend"));
  }, []);

  return (
    <div style={{ padding: "2rem", fontSize: "1.5rem" }}>
      <h1>AdGuardX Dashboard</h1>
      <p>Backend says: {message}</p>
    </div>
  );
}

export default App;

