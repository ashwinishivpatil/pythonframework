import pandas as pd
import DatabaseConnection

class PBMServices :
  PBMServicesDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In PBMServices",conn)
    #mainExcel.writeHeaderToSheet("PBMServices", wb)
    self.readDataFrame(conn)
    self.checkForBalnkSpaces(conn,mainExcel, wb)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.CheckForSubChannels(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)
  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.PBMServices "
      self.PBMServicesDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.PBMServicesDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "PBMServices"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The PBMServices Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "PBMServices"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The PBMServices  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the PBMServices table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")
      expectedList = ["OtherProviders","LivesRx"]
      null_columns = self.PBMServicesDataFrame.columns[self.PBMServicesDataFrame.isnull().any()].tolist()
      print(null_columns)
      result = set(null_columns).difference(set(expectedList))
      print(result)
      if(result.__len__() == 0):
          mainExcel.Module = "PBMServices"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult =  "Blank space should not present any of the columns given ProductID,ProductName column"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1
          mainExcel.Module = "PBMServices"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult =  "Blank space should not present any of the columns given ProductID,ProductName column"
          mainExcel.TestFailDescription = "Blanks are Present for other Coulmns"+str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.PBMServicesDataFrame.__len__())
    expectedcolumnnames = {"PBMID","EntityID","SubChannel","Service","LivesRx","ProductType","OtherProviders","MedicalAdministratorID"}
    presentColumnList = self.PBMServicesDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        mainExcel.Module = "PBMServices"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        mainExcel.Module = "PBMServices"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.PBMServicesDataFrame.__len__())
      subChannelsList = self.PBMServicesDataFrame['SubChannel'].values.tolist()
      #expectedSubchannels = set(mainExcel.channelList)
      expectedSubchannels = set(mainExcel.PBMServicesList)
      """expectedSubchannels = {"Commercial",
                            "CVS FEP",
                            "Employer",
                            "Managed Medicaid",
                            "MA-PD",
                            "PDP",
                            "TRICARE","HIX"}"""
      print("subChannelsList",subChannelsList)
      result = expectedSubchannels.difference(set(subChannelsList))
      if (result.__len__() == 0):
          mainExcel.Module = "PBMServices"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "PBMServices"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
