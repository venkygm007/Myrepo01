import pandas as pd

data = {
    "EmpID": [1, 2, 3],
    "Name": ["Ravi", "Sita", "Arjun"],
    "Department": ["IT", "HR", "Finance"],
    "Salary": [60000, 55000, 65000]
}

df = pd.DataFrame(data)
df.to_csv("employees.csv", index=False)

print("employees.csv created successfully")
