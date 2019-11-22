import pandas as pd
import DatabaseConnection

class EntityBenifitDesign :
  EntityBenfitDesignDataFrame   = pd.DataFrame()
  passed = 0;
  failed = 0
  def __call__(self):
     print("somthing")
  def executeScripts(self, conn, mainExcel, wb):
    print("In EntityBenfitDesign",conn)
    #mainExcel.writeHeaderToSheet("EntityBenifitDesign", wb)
    self.readDataFrame(conn)
    self.checkForValidColumns(conn,mainExcel,wb)
    self.checkForBalnkSpaces(conn,mainExcel,wb)


  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.EntityBenefitDesign "
      self.EntityBenfitDesignDataFrame = pd.read_sql(sqlst, conn)

  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.EntityBenfitDesignDataFrame.__len__())
    expectedcolumnnames = {"EntityID","ProductID","FormularyID","MedicalAdministratorID","FormularyStatus","CoPay","TierPosition"}
    presentColumnList = self.EntityBenfitDesignDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        mainExcel.Module = "EntityBenifitDesign"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult =  "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


    else:
        print("FAILED")
        self.failed = self.failed + 1
        mainExcel.Module = "EntityBenifitDesign"
        mainExcel.TestCaseName = "Validate Column Names"
        mainExcel.ExpectedResult =  "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "The Specified Entity are not  present" + result.__str__()
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def checkForBalnkSpaces(self,conn, mainExcel, wb):
      print("Check for Blank Spaces")

      #"EntityID", "ProductID", "FormularyID", "MedicalAdministratorID", "FormularyStatus", "CoPay", "TierPosition"
      expectedList = ["TierPosition", "MedicalAdministratorID", "CoPay"]
      null_columns = self.EntityBenfitDesignDataFrame.columns[self.EntityBenfitDesignDataFrame.isnull().any()].tolist()
      print(expectedList)
      result = set(null_columns).difference(set(expectedList))
      print(result.__str__())
      if(result.__len__() == 0):
          self.passed = self.passed+1
          mainExcel.Module = "EntityBenifitDesign"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult =  "Blank space should not present any of the columns except FormularyLivesRx column"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          mainExcel.Module = "EntityBenifitDesign"
          mainExcel.TestCaseName = "Check Blank space for columns"
          mainExcel.ExpectedResult =  "Blank space should not present any of the columns except FormularyLivesRx column"
          mainExcel.TestFailDescription =  "Blanks are Present for other Coulmns"+str(result)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)