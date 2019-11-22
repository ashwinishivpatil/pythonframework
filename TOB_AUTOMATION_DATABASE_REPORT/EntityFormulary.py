import pandas as pd
import DatabaseConnection


class EntityFormulary :
  EntityFormularyDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In entityFormulary",conn)
    #mainExcel.writeHeaderToSheet("EntityFormulary", wb)
    self.readDataFrame(conn)
    self.checkForBalnkSpaces(conn,mainExcel,wb)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.CheckForSubChannels(conn,mainExcel,wb)
    self.checkCorporateEntity(conn, mainExcel, wb)
    self.CheckProductLivesForPBM(conn,mainExcel, wb)
    #self.CheckProductLivesForMAPDP(mainExcel, wb)
    self.CheckProductLivesForNotMAPDP(conn,mainExcel, wb)
    self.CheckPercentageLives(conn,mainExcel, wb)
    self.CheckMedicalAdministratorIDForEmployee(conn,mainExcel,wb)
    self.checkforFormularyID(conn,mainExcel,wb)
  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.EntityFormulary "
      self.EntityFormularyDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())
      sqlst = "SELECT * FROM stg.Formulary "
      self.FormularyDataFrame = pd.read_sql(sqlst, conn)


  def checkforFormularyID(self,conn, mainExcel, wb):
      print("Check for the formulary ID")
      formularyIDfromFormulary = pd.Series(self.FormularyDataFrame['FormularyID']).tolist()
      formularyidfromEntityFormulary =  pd.Series(self.EntityFormularyDataFrame['FormularyID']).tolist()
      result = set(formularyidfromEntityFormulary).difference(set(formularyIDfromFormulary))
      if(result.__len__() == 0):
          self.passed = self.passed+1
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Check for the formularyIDs"
          mainExcel.ExpectedResult = "Formulary ID should be part of Formulary Table"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed+1
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Check for the formularyIDs"
          mainExcel.ExpectedResult = "Formulary ID should be part of Formulary Table"
          mainExcel.TestFailDescription = "Some of the formulary ID are not part of the formulary Table "+str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.EntityFormularyDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "EntityFormulary"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntityFormulary Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "EntityFormulary"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntityFormulary  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the EntityFormulary table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")
      expectedList = ['FormularyRxLives', 'LISLives', 'LISLivesPercentage']
      null_columns = self.EntityFormularyDataFrame.columns[self.EntityFormularyDataFrame.isnull().any()].tolist()
      result = set(expectedList).difference(set(null_columns))
      if(result.__len__() == 0):
          self.passed = self.passed+1
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns except FormularyLivesRx column"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed+1
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns except FormularyLivesRx column"
          mainExcel.TestFailDescription = "Blanks are Present for other Coulmns"+str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)




  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.EntityFormularyDataFrame.__len__())
    expectedcolumnnames = {"EntityID","SubChannel","ProductType","FormularyID","FormularyRxLives","IsPrimaryBOT","MedicalAdministratorID","LISLives","LISLivesPercentage" }
    presentColumnList = self.EntityFormularyDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        self.passed = self.passed + 1
        mainExcel.Module = "EntityFormulary"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


    else:
        print("FAILED")
        self.failed = self.failed + 1

        mainExcel.Module = "EntityFormulary"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.EntityFormularyDataFrame.__len__())
      subChannelsList = self.EntityFormularyDataFrame['SubChannel'].values.tolist()
      #expectedSubchannels = set(mainExcel.channelList)
      expectedSubchannels = set(mainExcel.EntityFormularyList)
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
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)



      else:
          print("FAILED")
          self.failed = self.failed + 1
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkCorporateEntity(self,conn,mainExcel,wb):
       print(self.EntityFormularyDataFrame.__len__())
       EntityIdFromFormularyList = self.EntityFormularyDataFrame['EntityID'].values.tolist()
       EntityFromEntity = self.EntityData[self.EntityData['IsParent'] == 'Y']
       entityList = EntityFromEntity['EntityID'].values.tolist()

       if(set(entityList).issubset(set(EntityIdFromFormularyList))):
           print("FAILED")
           self.failed = self.failed + 1
           mainExcel.Module = "EntityFormulary"
           mainExcel.TestCaseName = "Check for the Corporate Plans"
           mainExcel.ExpectedResult = "Corporate Plans should not appear"
           mainExcel.TestFailDescription = "CorporatePlans are present"
           mainExcel.TestFailSeverity = "Critical"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("PASSED")
           mainExcel.Module = "EntityFormulary"
           mainExcel.TestCaseName = "Check for the Corporate Plans"
           mainExcel.ExpectedResult = "Corporate Plans should not appear"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckProductLivesForPBM(self,conn,mainExcel,wb):
       print("Check For PRoduct Lives PBM")
       print(self.EntityFormularyDataFrame.__len__())
       productLivesPBM = self.EntityFormularyDataFrame.loc[(self.EntityFormularyDataFrame['SubChannel'] == 'PBM') & ~(self.EntityFormularyDataFrame['FormularyRxLives'].isnull() )]

       if(productLivesPBM.__len__() == 0):
           print("PASSED")

           mainExcel.Module = "EntityFormulary"
           mainExcel.TestCaseName = "Check Product Lives for PBM"
           mainExcel.ExpectedResult = "Product Lives should be 0 for PBM channel"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("FAILED")
           self.failed = self.failed + 1
           mainExcel.Module = "EntityFormulary"
           mainExcel.TestCaseName = "Check Product Lives for PBM"
           mainExcel.ExpectedResult = "Product Lives should be 0 for PBM channel"
           mainExcel.TestFailDescription = "Specified entity ID's does not have product lives as 0"+str(set(productLivesPBM['EntityID'].values.tolist()))
           mainExcel.TestFailSeverity = "Informational"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)



  def CheckProductLivesForNotMAPDP(self,conn,mainExcel,wb):
       print("Check For PRoduct Lives PBM")
       print(self.EntityFormularyDataFrame.__len__())
       productLivesMAPDP = self.EntityFormularyDataFrame.loc[(self.EntityFormularyDataFrame['SubChannel'].isin(["Commercial",
                             "CVS FEP",
                             "Employer",
                             "Managed Medicaid",
                             "Medicare Other",
                             "PBM",
                             "State Medicaid",
                             "TRICARE",
                             "VA"])) & (self.EntityFormularyDataFrame['LISLives'].notnull() )]
       print(productLivesMAPDP['LISLives'])
       if(productLivesMAPDP.__len__() == 0):
           print("PASSED")

           mainExcel.Module = "EntityFormulary"
           mainExcel.TestCaseName = "Check  LIS Lives  and LIS %  column for other channels "
           mainExcel.ExpectedResult = "Null should be present"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("FAILED")
           mainExcel.Module = "EntityFormulary"
           mainExcel.TestCaseName = "Check  LIS Lives  and LIS %  column for other channels "
           mainExcel.ExpectedResult = "Null should be present"
           mainExcel.TestFailDescription = "LIS lives are  present for specified Entity's"+str(set(productLivesMAPDP['EntityID'].values.tolist()))
           mainExcel.TestFailSeverity = "Informational"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckPercentageLives(self,conn, mainExcel, wb):
      print("Check for percentage Lives")
      entityList = []
      for row in self.EntityFormularyDataFrame.iterrows():


          LisLivesValue = row[1]['LISLives']
          formularyRxLives = row[1]['FormularyRxLives']
          #print("LisLivesValue",LisLivesValue)
          #print("formularyRxLives", formularyRxLives)
          if(str(LisLivesValue) != "nan"):
           if((str(formularyRxLives) != "nan") & (float(formularyRxLives) != 0.0)) :
               print("LisLivesValue",LisLivesValue)
               print("formularyRxLives", formularyRxLives)
               result = float(LisLivesValue)/float(formularyRxLives)
               print("result",round(result,2))
               percentageValue = row[1]['LISLivesPercentage']
               print("percentageValue",percentageValue)
               if(round(result,2) != percentageValue):
                   entityList.append(row[1]['EntityID'])

      if(entityList.__len__() ==0):
          print("PASSED")
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Calculation of  LISLivesPercentage=(LISLives/ProductLivesRx)*100  "
          mainExcel.ExpectedResult = "Value should match"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")


          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName = "Calculation of  LISLivesPercentage=(LISLives/ProductLivesRx)*100  "
          mainExcel.ExpectedResult = "Value should match"
          mainExcel.TestFailDescription = "Percentage is not matched for following entity's" +entityList.__str__()
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckMedicalAdministratorIDForEmployee(self,conn,mainExcel,wb):
       print("Validate Medical adminstator ID")

       medicalAdminDF = self.EntityFormularyDataFrame.loc[(self.EntityFormularyDataFrame['SubChannel'] == 'Employer') &(self.EntityFormularyDataFrame['MedicalAdministratorID']==0)]

       if(medicalAdminDF.__len__() ==0):
          print("PASSED")

          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName =  "Check the MedicalAdministratorID for Employer "
          mainExcel.ExpectedResult = "Blank should not be present"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

       else:
          print("FAILED")
          mainExcel.Module = "EntityFormulary"
          mainExcel.TestCaseName =  "Check the MedicalAdministratorID for Employer "
          mainExcel.ExpectedResult = "Blank should not be present"
          mainExcel.TestFailDescription = "Medical AdministratorID is not present" +pd.Series(medicalAdminDF['EntityID']).tolist().__str__()
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)



  def saveResultToDataBase(self,conn,mainExcel):
       print("Saving result to Database")

       cursor = conn.cursor()
       cursor.execute(
           'EXEC dbo.uspQCProcessLogDtl @QLID = ? ,@Module = ?,@TestCaseName = ?,@ExpectedResult = ?,@TestFailDescription = ?,@TestFailSeverity = ?,@TestCaseStatus = ?',mainExcel.QLID,mainExcel.Module,mainExcel.TestCaseName,mainExcel.ExpectedResult,mainExcel.TestFailDescription,mainExcel.TestFailSeverity,mainExcel.TestCaseStatus)

       conn.commit()