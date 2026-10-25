import type Employee from '../../interfaces/Employee';
import React,{useState, useEffect } from 'react'; 

interface EmployeeDropdownProps {
  value: number | "";
  onChange: (employeeId: number |"") => void;
  placeholder?: string; // NEW: optional placeholder prop
}

export default function EmployeeDropdown({
  value,
  onChange,
  placeholder = "Select Employee", 
}: EmployeeDropdownProps) {
  const [employees, setEmployees] = useState<Employee[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/employees")
      .then((res) => res.json())
      .then((data) => { console.log(data); setEmployees(data.employees); });
  }, []);

  return (
    <select
      value={value}
      onChange={(e) =>     onChange(e.target.value === "" ? "" : Number(e.target.value))}
    >
      <option value="">{placeholder}</option>

      {employees.map((employee) => (
        <option key={employee.id} value={employee.id}>
          {employee.employee_id} - {employee.name}
        </option>
      ))}
    </select>
  );
}

