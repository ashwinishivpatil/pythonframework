import pandas as pd
import DatabaseConnection

class EntityProductFormulary :
  EntityProductFormularyDataFrame   = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In EntityProductFormulary",conn)
    #mainExcel.writeHeaderToSheet("EntityProductFormulary", wb)
    self.readDataFrame(conn)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.CheckForSubChannels(conn,mainExcel,wb)
    self.checkForProductType(conn,mainExcel,wb)
    self.checkForData(conn, mainExcel, wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.entityproductformulary "
      self.EntityProductFormularyDataFrame = pd.read_sql(sqlst, conn)

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.EntityProductFormularyDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "EntityProductFormulary"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The EntityProductFormulary Table should contain data"
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
            mainExcel.ExpectedResult = "The EntityProductFormulary  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the EntityProductFormulary table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.EntityProductFormularyDataFrame.__len__())
    expectedcolumnnames = {"ProductID","EntityID","SubChannel","ProductType","ProductID","FormularyID","BenefitDesign","MedicalAdministratorID"}
    presentColumnList = self.EntityProductFormularyDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        self.passed = self.passed + 1

        mainExcel.Module = "EntityProductFormulary"
        mainExcel.TestCaseName ="Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    else:
        print("FAILED")
        mainExcel.Module = "EntityProductFormulary"
        mainExcel.TestCaseName ="Validate Column Names"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription =  "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def CheckForSubChannels(self,conn,mainExcel,wb):
      print(self.EntityProductFormularyDataFrame.__len__())
      subChannelsList = self.EntityProductFormularyDataFrame['SubChannel'].values.tolist()
      #expectedSubchannels = set(mainExcel.channelList)
      expectedSubchannels = set(mainExcel.EntityProductFormularyList)
      """expectedSubchannels = {"Commercial",
                                "CVS FEP",
                                "Employer",
                                "Managed Medicaid",
                                "MA-PD",
                                "Medicare Other",
                                "PBM",
                                "PDP",
                                "State Medicaid",
                                "TRICARE",
                                "VA"}"""
      print("subChannelsList",subChannelsList)
      result = expectedSubchannels.difference(set(subChannelsList))
      if (result.__len__() == 0):

          mainExcel.Module = "EntityProductFormulary"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "EntityProductFormulary"
          mainExcel.TestCaseName = "Validate SubChannels Names"
          mainExcel.ExpectedResult = "Given SubChannels name should be present"+expectedSubchannels.__str__()
          mainExcel.TestFailDescription ="Specified SubChannels are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "PASSED"
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
       productTypeListDF = self.EntityProductFormularyDataFrame['ProductType'].unique()
       print(productTypeList.difference(set(productTypeListDF)))
       result = productTypeList.difference(set(productTypeListDF))

       if (result.__len__() == 0):
           print("PASSED")
           mainExcel.Module = "EntityProductFormulary"
           mainExcel.TestCaseName = "Validate Product Type "
           mainExcel.ExpectedResult = "Given Product Type should be present:"+ productTypeList.__str__()
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

       else:
           print("FAILED")

           mainExcel.Module = "EntityProductFormulary"
           mainExcel.TestCaseName = "Validate Product Type "
           mainExcel.ExpectedResult = "Given Product Type should be present:"+ productTypeList.__str__()
           mainExcel.TestFailDescription = "The following Product types's are not present" + result.__str__()
           mainExcel.TestFailSeverity = "Informational"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
