import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'
import EmployeeDropdown from './components/employee/EmployeeDropdown'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <section id="center">
        <EmployeeDropdown
          employees={[]} 
          onSelect={(employee) => console.log(employee)}
        />
       </section>
    </>
  )
}

export default App
