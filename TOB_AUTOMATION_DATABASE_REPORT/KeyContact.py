import pandas as pd
import DatabaseConnection

class KeyContact :
  KeyContactDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In KeyContact",conn)
    #mainExcel.writeHeaderToSheet("KeyContact", wb)
    self.readDataFrame(conn)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.CheckZipCodeLength(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.KeyContact "
      self.KeyContactDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.KeyContactDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "KeyContact"
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
            mainExcel.Module = "KeyContact"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The KeyContact  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the KeyContact table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.KeyContactDataFrame.__len__())
    expectedcolumnnames = {"PersonnelID","EntityID","FirstName","LastName","Suffix1","Suffix2","Position","StreetAddress","City","State","Zip","Phone"}
    presentColumnList = self.KeyContactDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        self.passed = self.passed + 1
        mainExcel.Module = "KeyContact"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present" + str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        mainExcel.Module = "KeyContact"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present" + str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Informational"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def CheckZipCodeLength(self,conn,mainExcel,wb):
      print(self.KeyContactDataFrame.__len__())

      zipCodeDataFrame = self.KeyContactDataFrame.loc[self.KeyContactDataFrame['Zip'].map(str).apply(len) != 5]
      entityList = pd.Series(zipCodeDataFrame['EntityID']).values
      if (entityList.__len__() == 0):
          mainExcel.Module = "KeyContact"
          mainExcel.TestCaseName = "Check for ZIP code column "
          mainExcel.ExpectedResult = "Zip code length should be 5 digit"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "KeyContact"
          mainExcel.TestCaseName = "Check for ZIP code column "
          mainExcel.ExpectedResult = "Zip code length should be 5 digit"
          mainExcel.TestFailDescription = "Zip code in not present,or length is not 5 for specified Personal ID" + entityList.__str__()
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)