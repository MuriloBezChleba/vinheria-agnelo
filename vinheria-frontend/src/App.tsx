import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import {Registro} from './pages/registro'

function App() {
  
  return (
    <BrowserRouter>
      <Routes>
          <Route path='registro' element={<Registro/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
