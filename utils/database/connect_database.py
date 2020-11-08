import pymysql
import os

# Connect to the database
connection = pymysql.connect(host=os.environ['DB_HOST'],
                             user='root',
                             password=os.environ['DB_PASS'],
                             db='kekbot')
cursor = connection.cursor()
sql = "INSERT INTO `employee` (`EmployeeID`, `Ename`, `DeptID`, `Salary`, `Dname`, `Dlocation`) VALUES (%s, %s, %s, %s, %s, %s)"