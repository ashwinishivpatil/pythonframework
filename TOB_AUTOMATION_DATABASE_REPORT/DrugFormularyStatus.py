import pandas as pd
import DatabaseConnection
class DrugFormularyStatus :
  DrugFormularyStatus   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In DrugFormularyStatus",conn)
    #mainExcel.writeHeaderToSheet("DrugFormularyStatus", wb)
    self.readDataFrame(conn)
    self.validateColumns(conn,mainExcel, wb)
    self.CheckForSubChannels(conn,mainExcel,wb)
    self.checkCorporateEntity(conn,mainExcel,wb)
    self.validateDrugs(conn,mainExcel,wb)
    self.validateDrugStatusforMedicare(conn,mainExcel,wb)
    self.validateMostCommonCopayandMostCommonIns(conn,mainExcel,wb)
    self.checkForDrugFormularyStatus(conn,mainExcel,wb)
    self.CheckDrugdForEachChannel(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.drugformularystatus "
      self.DrugFormularyStatus = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.DrugFormularyStatus.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "DrugFormularyStatus"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The DrugFormularyStatus Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "DrugFormularyStatus"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The DrugFormularyStatus  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the DrugFormularyStatus table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckDrugdForEachChannel(self,conn,mainExcel,wb):
      print("Checking Drug for each channel")
      count = 0
      errorMessage = ""
      expectedSubchannels = mainExcel.DrugFormularyStatusList
      """expectedSubchannels = ["Commercial",
                            "CVS FEP",
                            "Employer",
                            "MA-PD",
                            "Managed Medicaid",
                            "Medicare Other",
                            "PBM",
                            "PDP",
                            "State Medicaid",
                            "TRICARE",
                            "VA","HIX"]"""
      expectedSDrugs = set(mainExcel.DrugList)
      for each in range(expectedSubchannels.__len__()):
          channel =expectedSubchannels[each]
          dataFrameBasedDrug = self.DrugFormularyStatus.loc[self.DrugFormularyStatus['SubChannel']==channel]
          drugSetBasedChannelandDrug = set(pd.Series(dataFrameBasedDrug['DrugName']).tolist())
          result = expectedSDrugs.difference(drugSetBasedChannelandDrug)
          if (result.__len__() == 0):
              print("")

          else:
              errorMessage = errorMessage +","+channel
              count = count +1
      if (count == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName ="Validate Drugs Based on each Channel"
          mainExcel.ExpectedResult = "For each Channel should all drugs"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName ="Validate Drugs Based on each Channel"
          mainExcel.ExpectedResult = "For each Channel should all drugs"
          mainExcel.TestFailDescription =  "Given Channels does not have all Drugs"+errorMessage
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def validateColumns(self,conn,mainExcel,wb):
      print(self.DrugFormularyStatus.__len__())
      expectedcolumnnames = {  "SubChannel",
                                "MedicalAdministratorID",
                                "FormularyID",
                                "EntityID",
                                "DrugID",
                                "DrugName",
                                "DrugStatus",
                                "CustomDrugStatus",
                                "DrugTier",
                                "MinCoPay",
                                "MaxCoPay",
                                "MostCommonCoPay",
                                "MinCoIns",
                                "MaxCoIns",
                                "MostCommonCoIns"
                            }
      presentColumnList = self.DrugFormularyStatus.columns.tolist()
      result = set(expectedcolumnnames).difference(set(presentColumnList))
      if ((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName ="Validate Column Names"
          mainExcel.ExpectedResult = "Given Coulmn name should be present" + str(expectedcolumnnames)
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


      else:
          print("FAILED")
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName ="Validate Column Names"
          mainExcel.ExpectedResult = "Given Coulmn name should be present" + str(expectedcolumnnames)
          mainExcel.TestFailDescription = "Specified column names are not present" + str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.DrugFormularyStatus.__len__())
      subChannelsList = self.DrugFormularyStatus['SubChannel'].values.tolist()
      expectedSubchannels = set(mainExcel.DrugFormularyStatusList)
      """expectedSubchannels = {"Commercial",
                            "CVS FEP",
                            "Employer",
                            "MA-PD",
                            "Managed Medicaid",
                            "Medicare Other",
                            "PBM",
                            "PDP",
                            "State Medicaid",
                            "TRICARE",
                            "VA","HIX"}"""
      print("subChannelsList",subChannelsList)
      result = expectedSubchannels.difference(set(subChannelsList))
      if (result.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName ="Validate SubChannels Names"
          mainExcel.ExpectedResult =  "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName ="Validate SubChannels Names"
          mainExcel.ExpectedResult =  "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkCorporateEntity(self,conn,mainExcel,wb):
       print(self.DrugFormularyStatus.__len__())
       EntityIdFromFormularyList = self.DrugFormularyStatus['EntityID'].values.tolist()
       EntityFromEntity = self.EntityData[self.EntityData['IsParent'] == 'Y']
       entityList = EntityFromEntity['EntityID'].values.tolist()

       if(set(entityList).issubset(set(EntityIdFromFormularyList))):
           print("FAILED")
           mainExcel.Module = "DrugFormularyStatus"
           mainExcel.TestCaseName = "Check for the Corporate Plans"
           mainExcel.ExpectedResult =  "Corporate Plans should not appear"
           mainExcel.TestFailDescription = "CorporatePlans are present"
           mainExcel.TestFailSeverity = "Critical"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("PASSED")

           mainExcel.Module = "DrugFormularyStatus"
           mainExcel.TestCaseName = "Check for the Corporate Plans"
           mainExcel.ExpectedResult =  "Corporate Plans should not appear"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def validateDrugs(self,conn,mainExcel,wb):
      print(self.DrugFormularyStatus.__len__())
      subDrugList = self.DrugFormularyStatus['DrugName'].values.tolist()
      expectedSDrugs = set(mainExcel.DrugList)
      """expectedSDrugs = {"Aubagio",
                        "Avonex",
                        "Cimzia",
                        "Copaxone 20 mg/ml",
                        "Enbrel",
                        "Gilenya",
                        "Humira",
                        "Lynparza",
                        "Otezla",
                        "Rubraca",
                        "Tecfidera",
                        "Zejula"}"""
      print("subChannelsList",subDrugList)
      result = expectedSDrugs.difference(set(subDrugList))
      if (result.__len__() == 0):
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName = "Check the Drugs"
          mainExcel.ExpectedResult = "Given Drugs name should be present"+expectedSDrugs.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName = "Check the Drugs"
          mainExcel.ExpectedResult = "Given Drugs name should be present"+expectedSDrugs.__str__()
          mainExcel.TestFailDescription =  "Specified Drugs are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def validateDrugStatusforMedicare(self,conn,mainExcel,wb):
      print(self.DrugFormularyStatus.__len__())
      medicareList = ['MA', 'MA-PD', 'PDP', 'Medicare Other']
      entityList = []
      for row in self.DrugFormularyStatus.iterrows():
          subchannel = row[1]['SubChannel']
          drugstatus = row[1]['DrugStatus']
          customDrugStatus = row[1]['CustomDrugStatus']

          if((subchannel in medicareList) & (drugstatus == "NL")):
              print(subchannel)
              if(customDrugStatus != "Not Covered"):
                  entityList.append( row[1]['EntityID'])

      if (entityList.__len__() == 0):

          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName = "Check the CustomDrugFormularyStatus for Medicare when BOT status is 'NL' "
          mainExcel.ExpectedResult =  "Not covered should display"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")

          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName = "Check the CustomDrugFormularyStatus for Medicare when BOT status is 'NL' "
          mainExcel.ExpectedResult =  "Not covered should display"
          mainExcel.TestFailDescription = "Not covered is not display for following entities " + entityList.__str__()
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def validateMostCommonCopayandMostCommonIns(self,conn,mainExcel,wb):
      print("Validate Most Common Copay")
      mostCommonCopayandCoin = self.DrugFormularyStatus[(self.DrugFormularyStatus['MostCommonCoPay'] == '') &(self.DrugFormularyStatus['MostCommonCoIns'] == '') ]
      print("pd.Series(mostCommonCopayandCoin['EntityID']).tolist().__str__()",pd.Series(mostCommonCopayandCoin['EntityID']).tolist().__str__())
      if (mostCommonCopayandCoin.__len__() == 0):

          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName = "Verify Most Common Co-pay and Most Common Co-insurance"
          mainExcel.ExpectedResult =  "If most common Co-pay is blank, Most common co-ins should have a value.If most common co-ins is blank, most common co-pay should have a value"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          self.failed = self.failed + 1
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName =  "Verify Most Common Co-pay and Most Common Co-insurance "
          mainExcel.ExpectedResult =  "If most common Co-pay is blank, Most common co-ins should have a value.If most common co-ins is blank, most common co-pay should have a value"
          mainExcel.TestFailDescription = "Both MostCommon Copay and Most Common Coin is balnk for " + pd.Series(mostCommonCopayandCoin['EntityID']).tolist().__str__()
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForDrugFormularyStatus(self,conn,mainExcel,wb):
      print("Check For DrugFormulary status")
      errorMessage= ""
      errorMessageList = []
      for row in self.DrugFormularyStatus.iterrows():
          entityID = str(row[1]['EntityID'])
          entityChannel = row[1]['SubChannel']
          drugstatus = row[1]['DrugStatus']
          customDrugStatus = row[1]['CustomDrugStatus']

          if(drugstatus == "S"):
              if not (customDrugStatus == "Preferred"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)

          if(drugstatus == "PB"):
              if not (customDrugStatus == "Preferred"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "R"):
              if not (customDrugStatus == "Covered"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "PG"):
              if not (customDrugStatus == "Preferred"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "MED"):
              if not (customDrugStatus == "Covered"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "S-NP"):
              if not (customDrugStatus == "Non-Preferred"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "NP"):
              if not (customDrugStatus == "Non-Preferred"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "NC"):
              if not (customDrugStatus == "Not Covered"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if((drugstatus == "NL" )and (entityChannel == 'HIX' or entityChannel == 'PBM')):
              if not (customDrugStatus == "Unavailable"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "T4"):
              if not (customDrugStatus == "Covered"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "NPB"):
              if not (customDrugStatus == "Non-Preferred"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)
          if(drugstatus == "S-P"):
              if not (customDrugStatus == "Preferred"):

                  errorMessageList.append(entityID + "-" + drugstatus + "-" + entityChannel + "-" + customDrugStatus)

      print(errorMessage)
      if (errorMessage.__len__() == 0):

          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName = "Check relationship between Drug Status level and Custom status"
          mainExcel.ExpectedResult =  "Relationship should match according to bussiness rule"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


      else:
          print("FAILED")
          self.failed = self.failed + 1
          mainExcel.Module = "DrugFormularyStatus"
          mainExcel.TestCaseName = "Check relationship between Drug Status level and Custom status"
          mainExcel.ExpectedResult = "Relationship should match according to bussiness rule"
          mainExcel.TestFailDescription =  "Given combination of( entityid,subchannel,drugstatus) custom drug status are not matched  " + set(errorMessageList).__str__()
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def saveResultToDataBase(self,conn,mainExcel):
       print("Saving result to Database")

       cursor = conn.cursor()
       cursor.execute(
           'EXEC dbo.uspQCProcessLogDtl @QLID = ? ,@Module = ?,@TestCaseName = ?,@ExpectedResult = ?,@TestFailDescription = ?,@TestFailSeverity = ?,@TestCaseStatus = ?',mainExcel.QLID,mainExcel.Module,mainExcel.TestCaseName,mainExcel.ExpectedResult,mainExcel.TestFailDescription,mainExcel.TestFailSeverity,mainExcel.TestCaseStatus)

       conn.commit()