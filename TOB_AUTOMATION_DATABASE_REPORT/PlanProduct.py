import pandas as pd
import DatabaseConnection

class PlanProduct :
  planProductDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In AccountRollup",conn)
    #mainExcel.writeHeaderToSheet("PlanProduct", wb)
    self.readDataFrame(conn)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.checkForBalnkSpaces(conn,mainExcel, wb)
    self.checkForData(conn, mainExcel, wb)
  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.planProductDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "PlanProduct"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The PlanProduct Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "PlanProduct"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The PlanProduct  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the PlanProduct table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.planproduct "
      self.planProductDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.planProductDataFrame.__len__())
    expectedcolumnnames = {"ProductID","ProductName","FormularyUsed","PBMID"}
    presentColumnList = self.planProductDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if(result.__len__() == 0):
        mainExcel.Module = "PlanProduct"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        self.failed = self.failed + 1
        mainExcel.Module = "PlanProduct"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")
      expectedList = ["FormularyUsed","PBMID"]
      null_columns = self.planProductDataFrame.columns[self.planProductDataFrame.isnull().any()].tolist()
      print(null_columns)
      result = set(null_columns).difference(set(expectedList))
      print(result)
      if(result.__len__() == 0):
          mainExcel.Module = "PlanProduct"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns given ProductID,ProductName column"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          mainExcel.Module = "PlanProduct"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns given ProductID,ProductName column"
          mainExcel.TestFailDescription =  "Blanks are Present for other Coulmns"+str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
