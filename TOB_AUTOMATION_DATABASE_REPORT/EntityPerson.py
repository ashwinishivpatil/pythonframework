import pandas as pd
import DatabaseConnection

class EntityPerson :
  EntityPersonDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In EntityPerson",conn)
    #mainExcel.writeHeaderToSheet("EntityPerson", wb)
    self.readDataFrame(conn)

    self.checkForValidColumns(conn,mainExcel,wb)
    self.chekcForUniqueRecords(conn,mainExcel,wb)
    self.Check_ForEntitySInEntityTab(conn,mainExcel,wb)


  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.EntityPerson "
      self.EntityPersonDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.EntityPersonDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "EntityPerson"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntityPerson Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "EntityPerson"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntityPerson  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the EntityPerson table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.EntityPersonDataFrame.__len__())
    expectedcolumnnames = {'EntityID','PersonID','Position','StreetAddress','City','State','Zip','Phone'}
    presentColumnList = self.EntityPersonDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        mainExcel.Module = "EntityPerson"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult =  "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        mainExcel.Module = "EntityPerson"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult =  "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def chekcForUniqueRecords(self,conn,mainExcel,wb):

    print("Check For UniqueRecords")
    indexValues = self.EntityPersonDataFrame[self.EntityPersonDataFrame.duplicated(['EntityID', 'PersonID', 'Position'])]
    print(indexValues)
    if (indexValues.__len__() == 0):
        mainExcel.Module = "EntityPerson"
        mainExcel.TestCaseName = "Check the Unique records"
        mainExcel.ExpectedResult =  "The combination of EntityID,Fname and Lname should be unique"
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


    else:

        mainExcel.Module = "EntityPerson"
        mainExcel.TestCaseName = "Check the Unique records"
        mainExcel.ExpectedResult =  "The combination of EntityID,Fname and Lname should be unique"
        mainExcel.TestFailDescription =  "The Uniques Columns Are not present" + indexValues.__str__()
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def Check_ForEntitySInEntityTab(self,conn,mainExcel,wb):
    global passed ,failed
    print("Check For entity")
    listofEntityPersonEntities = pd.Series(self.EntityPersonDataFrame['EntityID']).values
    listofEntities = pd.Series(self.EntityData['EntityID']).values
    result = set(listofEntityPersonEntities).difference(set(listofEntities))
    print(result)
    if (result.__len__() == 0):

        mainExcel.Module = "EntityPerson"
        mainExcel.TestCaseName = "check Entity's in Entity TAB"
        mainExcel.ExpectedResult =  "The Entity in Entity Person should be part of Entity TAB"
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)



    else:

        mainExcel.Module = "EntityPerson"
        mainExcel.TestCaseName = "check Entity's in Entity TAB"
        mainExcel.ExpectedResult =  "The Entity in Entity Person should be part of Entity TAB"
        mainExcel.TestFailDescription = "The Specified Entity are not  present" + result.__str__()
        mainExcel.TestFailSeverity = "Informational"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
