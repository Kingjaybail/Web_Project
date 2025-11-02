import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './home.scss';
import router_functions from '../../Routes/routes'; 

const Home = () => {
  const navigate = useNavigate();
  const [status, setStatus] = useState(null);

  const handleConnect = async (routeKey) => {
    setStatus('Connecting...');
    try {
      const result = await router_functions.fetchDataFromFastAPI(routeKey);
      setStatus(result?.message);
    } catch (err) {
      setStatus(err?.message ?? String(err));
    }
  };

  const go = (path) => navigate(path);

  return (
    <main className="home-page">
      <header className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Welcome to ModelSite</h1>
          <p className="hero-desc">
            An app for managing and exploring your models.
          </p>
        </div>
      </header>

      <section className="tiles">
        <div className="tile">
          <h3>Collaborate</h3>
          <p>Share projects and work together in real time.</p>
        </div>
        <div className="tile">
          <h3>Extensible</h3>
          <p>Integrate new model backends and routes easily.</p>
        </div>
        <div className="tile">
          <h3>Fast</h3>
          <p>Optimized frontend for responsive interactions.</p>
        </div>
      </section>
    </main>
  );
};

export default Home;