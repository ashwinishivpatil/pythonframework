import pandas as pd
import DatabaseConnection

class DrugFormularyRestrictions :
  drugFormularyRestricitionDataFrame   = pd.DataFrame()
  EntityData = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In DrugFormularyRestricition",conn)
    #mainExcel.writeHeaderToSheet("DrugFormularyRestrictions", wb)
    self.readDataFrame(conn)
    self.validateColumns(conn,mainExcel,wb)
    self.checkCorporateEntity(conn,mainExcel,wb)
    self.validateDrugs(conn,mainExcel, wb)
    self.checkForData(conn, mainExcel, wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "select * from stg.DrugFormularyRestrictions "
      self.drugFormularyRestricitionDataFrame = pd.read_sql(sqlst, conn)
      sqlst = "SELECT * FROM stg.Entity "
      self.EntityData = pd.read_sql(sqlst, conn)
      print(self.EntityData.head())

  def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.drugFormularyRestricitionDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "DrugFormularyRestrictions"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The DrugFormularyRestrictions Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "DrugFormularyRestrictions"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The DrugFormularyRestrictions  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the DrugFormularyRestrictions table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def validateColumns(self,conn,mainExcel,wb):
      print(self.drugFormularyRestricitionDataFrame.__len__())
      expectedcolumnnames = {  "EntityID","FormularyID","DrugID","DrugName","RestrictionCode","RestrictionComment","MedicalAdministratorID"
                            }
      presentColumnList = self.drugFormularyRestricitionDataFrame.columns.tolist()
      result = set(expectedcolumnnames).difference(set(presentColumnList))
      if ((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
          mainExcel.Module = "DrugFormularyRestrictions"
          mainExcel.TestCaseName = "Validate Column Names"
          mainExcel.ExpectedResult =  "Given Coulmn name should be present" + str(expectedcolumnnames)
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          self.failed = self.failed + 1
          mainExcel.Module = "DrugFormularyRestrictions"
          mainExcel.TestCaseName = "Validate Column Names"
          mainExcel.ExpectedResult =  "Given Coulmn name should be present" + str(expectedcolumnnames)
          mainExcel.TestFailDescription = "Specified column names are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkCorporateEntity(self,conn,mainExcel,wb):
       print(self.drugFormularyRestricitionDataFrame.__len__())
       EntityIdFromFormularyList = self.drugFormularyRestricitionDataFrame['EntityID'].values.tolist()
       EntityFromEntity = self.EntityData[self.EntityData['IsParent'] == 'Y']
       entityList = EntityFromEntity['EntityID'].values.tolist()

       if(set(entityList).issubset(set(EntityIdFromFormularyList))):
           self.failed = self.failed + 1
           mainExcel.Module = "DrugFormularyRestrictions"
           mainExcel.TestCaseName = "Check for the Corporate Plans"
           mainExcel.ExpectedResult = "Corporate Plans should not appear"
           mainExcel.TestFailDescription =  "CorporatePlans are present"
           mainExcel.TestFailSeverity = "Critical"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

       else:
              print("PASSED")
              mainExcel.Module = "DrugFormularyRestrictions"
              mainExcel.TestCaseName = "Check for the Corporate Plans"
              mainExcel.ExpectedResult =  "Corporate Plans should not appear"
              mainExcel.TestFailDescription = "None"
              mainExcel.TestFailSeverity = "None"
              mainExcel.TestCaseStatus = "PASSED"
              DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def validateDrugs(self,conn,mainExcel,wb):
      print(self.drugFormularyRestricitionDataFrame.__len__())
      subDrugList = self.drugFormularyRestricitionDataFrame['DrugName'].values.tolist()
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
          mainExcel.Module = "DrugFormularyRestrictions"
          mainExcel.TestCaseName = "Check the Drugs"
          mainExcel.ExpectedResult = "Given Drugs name should be present"+expectedSDrugs.__str__()
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          print("FAILED")
          mainExcel.Module = "DrugFormularyRestrictions"
          mainExcel.TestCaseName = "Check the Drugs"
          mainExcel.ExpectedResult = "Given Drugs name should be present"+expectedSDrugs.__str__()
          mainExcel.TestFailDescription = "Specified Drugs are not present" + str(result)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)