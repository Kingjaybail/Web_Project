// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Navbar from '../src/components/Navbar/navbar'
import Home from '../src/pages/Home/home'
import Login from '../src/pages/Login/login'
import About from '../src/pages/About/about'
import Models from '../src/pages/Models/models'
import Comparisons from '../src/pages/Comparisons/comparisons';
import Signup from '../src/pages/Signup/signup'
import ProtectedRoute from '../src/components/protectedroute/ProtectedRoute'

function App() {
  return (
    <Router>
      <Navbar />
      <main style={{ padding: 20 }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route
            path="/about"
            element={
              <ProtectedRoute>
                <About />
              </ProtectedRoute>
            }
          />
          <Route
            path="/models"
            element={
              <ProtectedRoute>
                <Models />
              </ProtectedRoute>
            }
          />
        <Route
          path="/comparisons"
          element={
            <ProtectedRoute>
              <Comparisons />
            </ProtectedRoute>
          }
        />
        </Routes>
      </main>
    </Router>
  )
}

export default App
