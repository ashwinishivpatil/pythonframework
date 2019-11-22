import pandas as pd
import DatabaseConnection

class Formulary :
  FormularyDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In Formulary",conn)
    #mainExcel.writeHeaderToSheet("Formulary", wb)
    self.readDataFrame(conn)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.checkForBalnkSpaces(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)


  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.Formulary "
      self.FormularyDataFrame = pd.read_sql(sqlst, conn)

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.FormularyDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "Formulary"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Formulary Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "Formulary"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Formulary  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the Formulary table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.FormularyDataFrame.__len__())
    expectedcolumnnames = {"FormularyID","FormularyName","MasterFormularyID"}
    presentColumnList = self.FormularyDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        mainExcel.Module = "Formulary"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        mainExcel.Module = "Formulary"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription ="Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Informational"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")
      expectedList = ["FormularyID","FormularyName"]
      null_columns = self.FormularyDataFrame.columns[self.FormularyDataFrame.isnull().any()].tolist()
      print(null_columns)
      if (list(null_columns).__contains__(expectedList)):
          result = set(null_columns).difference(set(expectedList))
      else:
          result = ""
      if(result.__len__() == 0):
          mainExcel.Module = "Formulary"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult =  "Blank space should not present any of the columns given' 'FormularyID','FormularyName' column"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          mainExcel.Module = "Formulary"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult =  "Blank space should not present any of the columns given' 'FormularyID','FormularyName' column"
          mainExcel.TestFailDescription =  "Blanks are Present for other Coulmns"+str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)