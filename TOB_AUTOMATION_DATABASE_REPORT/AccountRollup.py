import pandas as pd
import DatabaseConnection


class AccountRollup :
  AccountRollupDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In AccountRollup",conn)
    #mainExcel.writeHeaderToSheet("AccountRollup", wb)
    self.readDataFrame(conn)
    self.checkForData(conn,mainExcel,wb)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.CheckForSubChannels(conn,mainExcel,wb)
    self.checkForBalnkSpaces(conn,mainExcel,wb)
    self.checkFormularyID(conn,mainExcel,wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.AccountRollup "
      self.AccountRollupDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
      print("Check for Data Exists or not ")
      if (self.AccountRollupDataFrame.__len__() > 0):
          self.passed = self.passed + 1
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
          mainExcel.ExpectedResult = "The Account Rollup Table should contain data"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
          # mainExcel.writeToSheet("Entity", wb)

      else:
          print("FAILED")
          self.failed = self.failed + 1
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
          mainExcel.ExpectedResult = "The Account Rollup Table should contain data"
          mainExcel.TestFailDescription = "Data is not present in the Account Rollup table"
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.AccountRollupDataFrame.__len__())
    expectedcolumnnames = {"ParentEntityID","EntityID","SubChannel","FormularyID" }
    presentColumnList = self.AccountRollupDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        self.passed = self.passed + 1
        mainExcel.Module = "AccountRollup"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult =  "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        self.failed = self.failed+1
        mainExcel.Module = "AccountRollup"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult =  "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.AccountRollupDataFrame.__len__())
      subChannelsList = self.AccountRollupDataFrame['SubChannel'].values.tolist()
      #expectedSubchannels =set(mainExcel.channelList)
      expectedSubchannels = set(mainExcel.accountrollupExpectedSubChannelsList)
      """expectedSubchannels = {"Cash",
                            "Commercial",
                            "CVS FEP",
                            "Employer",
                            "MA",
                            "MA-PD",
                            "Managed Medicaid",
                            "Medicare Other",
                            "Other Third Party",
                            "PBM",
                            "PDP",
                            "SPP",
                            "State Medicaid",
                            "TRICARE",
                            "VA"}"""
      print("subChannelsList",subChannelsList)
      print("expectedSubchannels",expectedSubchannels)
      result = expectedSubchannels.difference(set(subChannelsList))
      if (result.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")
      expectedList = ['ParentEntityID', 'EntityID', 'SubChannel']
      null_columns = self.AccountRollupDataFrame.columns[self.AccountRollupDataFrame.isnull().any()].tolist()
      print(null_columns)
      result = set(null_columns).difference(set(expectedList))
      print(result)
      if(result.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns given'ParentEntityID', 'EntityID', 'SubChannel' column"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns given'ParentEntityID', 'EntityID', 'SubChannel' column"
          mainExcel.TestFailDescription = "Blanks are Present for other Coulmns"+str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkFormularyID(self,conn,mainExcel, wb):
      print("Check for -1 formulary ID")
      negativeFormularyID = self.AccountRollupDataFrame.loc[self.AccountRollupDataFrame['FormularyID'] == -1]

      if(negativeFormularyID.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Check the FormularyID column"
          mainExcel.ExpectedResult = "It should not contain -1"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          self.failed = self.failed+1
          mainExcel.Module = "AccountRollup"
          mainExcel.TestCaseName = "Check the FormularyID column"
          mainExcel.ExpectedResult = "It should not contain -1"
          mainExcel.TestFailDescription = "-1 are present for Some Entity ID"
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def saveResultToDataBase(self,conn,mainExcel):
       print("Saving result to Database")

       cursor = conn.cursor()
       cursor.execute(
           'EXEC dbo.uspQCProcessLogDtl @QLID = ? ,@Module = ?,@TestCaseName = ?,@ExpectedResult = ?,@TestFailDescription = ?,@TestFailSeverity = ?,@TestCaseStatus = ?',mainExcel.QLID,mainExcel.Module,mainExcel.TestCaseName,mainExcel.ExpectedResult,mainExcel.TestFailDescription,mainExcel.TestFailSeverity,mainExcel.TestCaseStatus)

       conn.commit()