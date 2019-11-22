import pandas as pd
import DatabaseConnection

class EntityProduct :
  EntityProductDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0;
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In EntityProduct",conn)
    #mainExcel.writeHeaderToSheet("EntityProduct", wb)
    self.readDataFrame(conn)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.checkForBalnkSpaces(conn,mainExcel,wb)
    self.CheckProductLivesForNotMAPDP(conn,mainExcel,wb)
    self.CheckProductLivesForPBM(conn,mainExcel,wb)
    self.checkCorporateEntity(conn,mainExcel,wb)
    self.CheckForSubChannels(conn,mainExcel,wb)
    self.CheckPercentageLives(conn,mainExcel,wb)
    self.checkForProductType(conn,mainExcel,wb)
    self.checkProductTypeForSupplimentOther(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.EntityProduct "
      self.EntityProductDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.EntityProductDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "EntityProduct"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntityProduct Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "EntityProduct"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntityProduct  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the EntityProduct table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.EntityProductDataFrame.__len__())
    expectedcolumnnames = {"ProductID","EntityID","SubChannel","ProductType","ProductLives","ProductLivesRx","MedicalAdministratorID","LISLives","LISLivesPercentage"}
    presentColumnList = self.EntityProductDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        mainExcel.Module = "EntityProduct"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")

        mainExcel.Module = "EntityProduct"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Informational"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")
      expectedList = ["ProductLives","ProductLivesRx","MedicalAdministratorID","LISLives","LISLivesPercentage"]
      null_columns = self.EntityProductDataFrame.columns[self.EntityProductDataFrame.isnull().any()].tolist()
      print(null_columns)
      result = set(null_columns).difference(set(expectedList))
      if(result.__len__() == 0):
          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns except ProductLives ProductLivesRx MedicalAdministratorID LISLives LISLivesPercentage"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:

          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult = "Blank space should not present any of the columns except ProductLives ProductLivesRx MedicalAdministratorID LISLives LISLivesPercentage"
          mainExcel.TestFailDescription = "Blanks are Present for other Coulmns"+str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.EntityProductDataFrame.__len__())
      subChannelsList = self.EntityProductDataFrame['SubChannel'].values.tolist()
      #expectedSubchannels = set(mainExcel.channelList)
      expectedSubchannels = set(mainExcel.EntityProductList)
      """expectedSubchannels = {"Commercial",
                            "CVS FEP",
                            "Employer",
                            "MA",
                            "MA-PD",
                            "Managed Medicaid",
                            "Medicare Other",
                            "PBM",
                            "PDP",
                            "SPP",
                            "State Medicaid",
                            "TRICARE",
                            "VA","HIX"}"""
      print("subChannelsList",subChannelsList)
      result = expectedSubchannels.difference(set(subChannelsList))
      if (result.__len__() == 0):

          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present" + expectedSubchannels.__str__()
          mainExcel.TestFailDescription =  "Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkCorporateEntity(self,conn,mainExcel,wb):
       print(self.EntityProductDataFrame.__len__())
       EntityIdFromFormularyList = self.EntityProductDataFrame['EntityID'].values.tolist()
       EntityFromEntity = self.EntityData[self.EntityData['IsParent'] == 'Y']
       entityList = EntityFromEntity['EntityID'].values.tolist()

       if(set(entityList).issubset(set(EntityIdFromFormularyList))):
           print("FAILED")
           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName = "Check for the Corporate Plans"
           mainExcel.ExpectedResult = "Corporate Plans should not appear"
           mainExcel.TestFailDescription = "CorporatePlans are present"
           mainExcel.TestFailSeverity = "Critical"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("PASSED")
           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName = "Check for the Corporate Plans"
           mainExcel.ExpectedResult = "Corporate Plans should not appear"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckProductLivesForPBM(self,conn,mainExcel,wb):
       print("Check For PRoduct Lives PBM")
       print(self.EntityProductDataFrame.__len__())
       productLivesPBM = self.EntityProductDataFrame.loc[(self.EntityProductDataFrame['SubChannel'] == 'PBM') & (self.EntityProductDataFrame['ProductLivesRx'] != 0 )]

       if(productLivesPBM.__len__() == 0):
           print("PASSED")

           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName =  "Check Product Lives for PBM"
           mainExcel.ExpectedResult = "Product Lives should be 0 for PBM channel"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("FAILED")
           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName = "Check Product Lives for PBM"
           mainExcel.ExpectedResult = "Product Lives should be 0 for PBM channel"
           mainExcel.TestFailDescription = "Specified entity ID's does not have product lives as 0"+str(set(productLivesPBM['EntityID'].values.tolist()))
           mainExcel.TestFailSeverity = "Critical"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)



  def CheckProductLivesForNotMAPDP(self,conn,mainExcel,wb):
       print("Check For PRoduct Lives PBM")
       print(self.EntityProductDataFrame.__len__())
       productLivesMAPDP = self.EntityProductDataFrame.loc[(self.EntityProductDataFrame['SubChannel'].isin(["Commercial",
                             "CVS FEP",
                             "Employer",
                             "Managed Medicaid",
                             "Medicare Other",
                             "PBM",
                             "State Medicaid",
                             "TRICARE",
                             "VA"])) & (self.EntityProductDataFrame['LISLives'].notnull() )]
       print(productLivesMAPDP['LISLives'])
       if(productLivesMAPDP.__len__() == 0):
           print("PASSED")

           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName =  "Check  LIS Lives  and LIS %  column for other channels "
           mainExcel.ExpectedResult =  "Null shoul be present"
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           print("FAILED")
           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName = "Check  LIS Lives  and LIS %  column for other channels "
           mainExcel.ExpectedResult = "Null shoul be present"
           mainExcel.TestFailDescription = "LIS lives are  present for specified Entity's"+str(set(productLivesMAPDP['EntityID'].values.tolist()))
           mainExcel.TestFailSeverity = "Critical"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckPercentageLives(self,conn, mainExcel, wb):
      print("Check for percentage Lives")
      entityList = []
      for row in self.EntityProductDataFrame.iterrows():


          LisLivesValue = row[1]['LISLives']
          formularyRxLives = row[1]['ProductLivesRx']
          #print("LisLivesValue",LisLivesValue)
          #print("formularyRxLives", formularyRxLives)
          if(str(LisLivesValue) != "nan"):
           if((str(formularyRxLives) != "nan") & (float(formularyRxLives) != 0.0)) :
               print("LisLivesValue",LisLivesValue)
               print("ProductLivesRx", formularyRxLives)
               result = float(LisLivesValue)/float(formularyRxLives)
               print("result",round(result,2))
               percentageValue = row[1]['LISLivesPercentage']
               print("percentageValue",percentageValue)
               if(round(result,2) != percentageValue):
                   entityList.append(row[1]['EntityID'])

      if(entityList.__len__() ==0):
          print("PASSED")
          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Calculation of  LISLivesPercentage=(LISLives/ProductLivesRx)*100  "
          mainExcel.ExpectedResult = "Value should match"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")

          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Calculation of  LISLivesPercentage=(LISLives/ProductLivesRx)*100  "
          mainExcel.ExpectedResult = "Value should match"
          mainExcel.TestFailDescription = "Percentage is not matched for following entity's" +entityList.__str__()
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkForProductType(self,conn,mainExcel,wb):
       print("Check For Product Type ")
       productTypeList = set(mainExcel.productList)
       """productTypeList = ['Self-Funded/ASO',
                            'Tricare',
                            'EPO',
                            'Medicaid',
                            'Unions',
                            'Supplemental Medicare',
                            'HMO',
                            'PPO',
                            'CHIP',
                            'Federal Employees',
                            'Medicare Other',
                            'Others',
                            'State Medicaid',
                            'Bronze',
                            'Gold',
                            'Point of Service',
                            'PDP',
                            'SPP',
                            'Medicare Advantage',
                            'MA-PD',
                            'Platinum',
                            'Indemnity',
                            'Silver',
                            'PBM',
                            'Catastrophic']"""
       productTypeListDF = self.EntityProductDataFrame['ProductType'].unique()
       print(productTypeList.difference(set(productTypeListDF)))
       result = productTypeList.difference(set(productTypeListDF))

       if (result.__len__() == 0):
           print("PASSED")
           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName = "Validate Product Type "
           mainExcel.ExpectedResult = "Given Product Type should be present:"+ productTypeList.__str__()
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

       else:
           print("FAILED")
           mainExcel.Module = "EntityProduct"
           mainExcel.TestCaseName = "Validate Product Type "
           mainExcel.ExpectedResult = "Given Product Type should be present:" + productTypeList.__str__()
           mainExcel.TestFailDescription = "The following Product types's are not present" + result.__str__()
           mainExcel.TestFailSeverity = "Informational"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkProductTypeForSupplimentOther(self,conn,mainExcel,wb):
      dataFrameForSuppliment = self.EntityProductDataFrame.loc[(self.EntityProductDataFrame['ProductType'] == 'Supplemental Medicare') & (self.EntityProductDataFrame['SubChannel'] != 'Commercial')]
      if (dataFrameForSuppliment.__len__() == 0):
          print("PASSED")
          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Check the Channel when Product Type is Supplemental Medicare"
          mainExcel.ExpectedResult = "Commercial should display"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "EntityProduct"
          mainExcel.TestCaseName = "Check the Channel when Product Type is Supplemental Medicare"
          mainExcel.ExpectedResult = "Commercial should display"
          mainExcel.TestFailDescription = "The Supplemental Medicare Persent for others channels" + dataFrameForSuppliment['SubChannel']
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)