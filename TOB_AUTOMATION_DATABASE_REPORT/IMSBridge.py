import pandas as pd
import DatabaseConnection

class IMSBridge :
  IMSBridgeDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In IMSBridge",conn)
    #mainExcel.writeHeaderToSheet("IMSBridge", wb)
    self.readDataFrame(conn)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.CheckForSubChannels(conn,mainExcel,wb)


  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.IMSBridge "
      self.IMSBridgeDataFrame = pd.read_sql(sqlst, conn)



  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.IMSBridgeDataFrame.__len__())
      subChannelsList = self.IMSBridgeDataFrame['SubChannel'].values.tolist()
      #expectedSubchannels = set(mainExcel.channelList)
      expectedSubchannels = set(mainExcel.IMSBridgeList)
      """expectedSubchannels = {"Cash",
                        "Commercial",
                        "Employer",
                        "Managed Medicaid",
                        "MA-PD",
                        "Medicare Other",
                        "Other Third Party",
                        "PBM",
                        "PDP",
                        "State Medicaid",
                        "TRICARE",
                        "VA"}"""
      print("subChannelsList",subChannelsList)
      result = expectedSubchannels.difference(set(subChannelsList))
      if (result.__len__() == 0):

          mainExcel.Module = "IMSBridge"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "IMSBridge"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present" + expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.IMSBridgeDataFrame.__len__())
    expectedcolumnnames = {"IMSID","IMSPlanName","EntityID","SubChannel","RxType","DisplayName"}
    presentColumnList = self.IMSBridgeDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        mainExcel.Module = "IMSBridge"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        self.failed = self.failed + 1

        mainExcel.Module = "IMSBridge"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)