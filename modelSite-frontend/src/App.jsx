// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Navbar from '../src/components/Navbar/navbar'
import Home from '../src/pages/Home/home'
import Login from '../src/pages/Login/login'
import About from '../src/pages/About/about'
import Models from '../src/pages/Models/models'
function App() {
  return (
    <Router>
      <Navbar />
      <main style={{ padding: 20 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/about" element={<About />} />
          <Route path="/models" element={<Models />} />
          
        </Routes>
      </main>
    </Router>
  )
}

export default App
