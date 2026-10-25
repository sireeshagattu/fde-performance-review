import type Employee from '../../interfaces/Employee';
import React,{useState, useEffect } from 'react';   
interface EmployeeDropdownProps {
  value: number | "";
  onChange: (employeeId: number) => void;
}

export default function EmployeeDropdown({
  value,
  onChange,
}: EmployeeDropdownProps) {
  const [employees, setEmployees] = useState<Employee[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/employees")
      .then((res) => res.json())
      .then((data) => setEmployees(data));
  }, []);

  return (
    <select
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
    >
      <option value="">Select Employee</option>

      {employees.map((employee) => (
        <option key={employee.id} value={employee.id}>
          {employee.employee_id} - {employee.name}
        </option>
      ))}
    </select>
  );
}

