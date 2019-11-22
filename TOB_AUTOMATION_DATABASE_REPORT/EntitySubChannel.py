import pandas as pd
import DatabaseConnection
class EntitySubChannel :
  EntitySubChannelDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In EntitySubChannel",conn)
    #mainExcel.writeHeaderToSheet("EntitySubChannel", wb)
    self.readDataFrame(conn)
    self.CheckForSubChannels(conn,mainExcel,wb)
    self.checkForBalnkSpaces(conn,mainExcel,wb)
    self.checkCorporateEntity(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)
  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.EntitySubChannel "
      self.EntitySubChannelDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.EntitySubChannelDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "EntitySubChannel"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntitySubChannel Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "EntityProductFormulary"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntitySubChannel  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the EntityProductFormulary table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"

  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")
      expectedList = ['EntityID', 'SubChannel']
      null_columns = self.EntitySubChannelDataFrame.columns[self.EntitySubChannelDataFrame.isnull().any()].tolist()
      print(null_columns)
      result = set(null_columns).difference(set(expectedList))
      print(result)
      if (result.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "EntitySubChannel"
          mainExcel.TestCaseName =  "Check Blank space for columns"
          mainExcel.ExpectedResult ="Blank space should not present any of the columns given 'EntityID', 'SubChannel' column"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1

          mainExcel.Module = "EntitySubChannel"
          mainExcel.TestCaseName =  "Check Blank space for columns"
          mainExcel.ExpectedResult ="Blank space should not present any of the columns given 'EntityID', 'SubChannel' column"
          mainExcel.TestFailDescription = "Blanks are Present for other Coulmns" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.EntitySubChannelDataFrame.__len__())
      subChannelsList = self.EntitySubChannelDataFrame['SubChannel'].values.tolist()
      #expectedSubchannels = set(mainExcel.channelList)
      #expectedSubchannels ={"Commercial","CVS","FEP", "Employer", "HIX", "MA", "MA - PD", "Managed Medicaid", "PBM", "PDP", "SPP", "State Medicaid", "TRICARE","VA"}
      #expectedSubchannels = {"Cash","Commercial","CVS FEP","Employer","MA","MA-PD","Managed Medicaid","Medicare Other","Other Third Party","PBM","PDP","SPP","State Medicaid","TRICARE","VA","HIX"}
      expectedSubchannels = set(mainExcel.EntitySubChannelList)
      print("subChannelsList",subChannelsList)
      result = expectedSubchannels.difference(set(subChannelsList))
      if (result.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "EntitySubChannel"
          mainExcel.TestCaseName =   "Validate SubChannels Names"
          mainExcel.ExpectedResult ="Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          mainExcel.Module = "EntitySubChannel"
          mainExcel.TestCaseName =   "Validate SubChannels Names"
          mainExcel.ExpectedResult ="Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def checkCorporateEntity(self,conn,mainExcel,wb):
       print(self.EntitySubChannelDataFrame.__len__())
       EntityIdFromFormularyList = self.EntitySubChannelDataFrame['EntityID'].values.tolist()
       EntityFromEntity = self.EntityData[self.EntityData['EntityType'] == 'EGWP']
       entityList = EntityFromEntity['EntityID'].values.tolist()

       if(set(entityList).issubset(set(EntityIdFromFormularyList))):
           print("PASSED")
           mainExcel.Module = "EntitySubChannel"
           mainExcel.TestCaseName = "check EGWp EntityId from Entity present under EntityID column"
           mainExcel.ExpectedResult = "All EGWP Entities should be persent"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("FAILED")

           mainExcel.Module = "EntitySubChannel"
           mainExcel.TestCaseName = "check EGWp EntityId from Entity present under EntityID column"
           mainExcel.ExpectedResult = "All EGWP Entities should be persent"
           mainExcel.TestFailDescription = "Some Entity Id's are not present"
           mainExcel.TestFailSeverity = "Critical"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)