import pandas as pd
import DatabaseConnection
class Person :
  personDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In Person",conn)
    #mainExcel.writeHeaderToSheet("Person", wb)
    self.readDataFrame(conn)
    self.validateTheColumns(conn,mainExcel,wb)
    self.chekcForUniqueRecords(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.Person "
      self.personDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())


  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.personDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "Person"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Person Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "Person"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Person  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the Person table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
  def validateTheColumns(self,conn,mainExcel, wb):
      global passed,failed
      ExpectedList = {'PersonID','FirstName','LastName','Suffix1','Suffix2'}
      pcolumnList = self.personDataFrame.columns.tolist()
      result = set(ExpectedList).difference(set(pcolumnList))
      print(result)
      if (result.__len__() == 0):
              mainExcel.Module = "Person"
              mainExcel.TestCaseName = "Check Column Names"
              mainExcel.ExpectedResult = "The given columns should be present"+ExpectedList.__str__()
              mainExcel.TestFailDescription = "None"
              mainExcel.TestFailSeverity = "None"
              mainExcel.TestCaseStatus = "PASSED"
              DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
              self.failed = self.failed + 1
              mainExcel.Module = "Person"
              mainExcel.TestCaseName = "Check Column Names"
              mainExcel.ExpectedResult = "The given columns should be present" + ExpectedList.__str__()
              mainExcel.TestFailDescription = "Give columns are not present"+result.__str__()
              mainExcel.TestFailSeverity = "Critical"
              mainExcel.TestCaseStatus = "FAILED"
              DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def chekcForUniqueRecords(self,conn,mainExcel,wb):
      print("Check For UniqueRecords")
      indexValues = self.personDataFrame[self.personDataFrame.duplicated(['PersonID', 'FirstName', 'LastName'])]
      print(indexValues)
      if (indexValues.__len__() == 0):
          mainExcel.Module = "Person"
          mainExcel.TestCaseName = "Check the Unique records"
          mainExcel.ExpectedResult = "The combination of PersonID,Fname and Lname should be unique"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1
          mainExcel.Module = "Person"
          mainExcel.TestCaseName = "Check the Unique records"
          mainExcel.ExpectedResult = "The combination of PersonID,Fname and Lname should be unique"
          mainExcel.TestFailDescription = "The Uniques Columns Are not present" + indexValues.__str__()
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)