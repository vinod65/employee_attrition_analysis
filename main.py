import sqlite3

# Step 1: Connect to SQLite and create the database file
conn = sqlite3.connect("hr.db")  # This will create 'hr.db' in your project folder
cursor = conn.cursor()

# Step 2: Create the employee_data table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee_data (
    EmployeeID INTEGER,
    Age INTEGER,
    Department TEXT,
    Education TEXT,
    Gender TEXT,
    JobRole TEXT,
    MonthlyIncome REAL,
    YearsAtCompany INTEGER,
    Attrition TEXT
)
''')

# Step 3: Insert sample data
sample_data = [
    (1001, 29, 'Sales', 'Bachelors', 'Male', 'Sales Executive', 4200, 2, 'Yes'),
    (1002, 35, 'HR', 'Masters', 'Female', 'HR Manager', 6200, 5, 'No'),
    (1003, 41, 'IT', 'Bachelors', 'Male', 'Developer', 7000, 7, 'No'),
    (1004, 28, 'IT', 'Bachelors', 'Female', 'Developer', 3900, 1, 'Yes'),
    (1005, 33, 'Sales', 'Masters', 'Male', 'Sales Manager', 5500, 4, 'No'),
    (1006, 25, 'HR', 'Bachelors', 'Female', 'HR Assistant', 3000, 2, 'Yes')
]

# Optional: Clear old data (only for testing)
cursor.execute("DELETE FROM employee_data")

# Insert data
cursor.executemany("INSERT INTO employee_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_data)

# Save and close
conn.commit()
conn.close()

print("Database and table created with sample data.")

import pandas as pd

# Reopen the database and read the data
conn = sqlite3.connect("hr.db")
df = pd.read_sql_query("SELECT * FROM employee_data", conn)
conn.close()

# Display the data
print(df)

# Step 1: Add a numeric column for Attrition
df['Attrition_Flag'] = df['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)

# Step 2: Gender-wise Attrition
print("\nGender-wise Attrition:")
print(df[df['Attrition'] == 'Yes']['Gender'].value_counts())

# Step 3: Department-wise Attrition
print("\nDepartment-wise Attrition:")
print(df[df['Attrition'] == 'Yes']['Department'].value_counts())

# Step 4: Avg Monthly Income of employees who left
print("\nAverage Monthly Income of Employees Who Left:")
print(df[df['Attrition'] == 'Yes']['MonthlyIncome'].mean())

# Step 5: Import visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

# Chart 1: Gender-wise Attrition
plt.figure(figsize=(6, 4))
sns.countplot(x='Gender', hue='Attrition', data=df)
plt.title("Attrition by Gender")
plt.show()

# Chart 2: Department-wise Attrition
plt.figure(figsize=(6, 4))
sns.countplot(x='Department', hue='Attrition', data=df)
plt.title("Attrition by Department")
plt.show()

# Chart 3: Income vs Attrition
plt.figure(figsize=(6, 4))
sns.boxplot(x='Attrition', y='MonthlyIncome', data=df)
plt.title("Monthly Income vs Attrition")
plt.show()

# Export to Excel
with pd.ExcelWriter("employee_attrition_report.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='All_Employees', index=False)
    
    # Employees who left
    df[df['Attrition'] == 'Yes'].to_excel(writer, sheet_name='Attrition_Only', index=False)

    # Summary statistics
    summary = {
        "Total Employees": [len(df)],
        "Employees Left": [df['Attrition'].value_counts().get('Yes', 0)],
        "Avg Income (Left)": [df[df['Attrition'] == 'Yes']['MonthlyIncome'].mean()]
    }
    pd.DataFrame(summary).to_excel(writer, sheet_name='Summary', index=False)

print("\nExcel report saved as 'employee_attrition_report.xlsx'")



