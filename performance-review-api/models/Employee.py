from pydantic import BaseModel

class Employee(BaseModel):
    id: int
    employee_id: str
    name: str
    department: str
    email: str
    status: str