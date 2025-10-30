// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from '../src/components/Navbar/navbar'
import Home from '../src/pages/Home/home'
// import Login from '../src/pages/Login/login'
import './App.css'

function App() {
  return (
    <Router>
      <Navbar />
      <main style={{ padding: 20 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          {/* <Route path="/login" element={<Login />} /> */}
        </Routes>
      </main>
    </Router>
  )
}

export default App
