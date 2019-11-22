import ExcelReport
import pandas as pd
import pandas.io.sql as psql
import DatabaseConnection



class Entity :
  EntityDataFrame   = pd.DataFrame()
  passed = 0
  failed = 0
  def __call__(self):
     print("somthing")

  def executeScripts(self,conn,mainExcel,wb):
   #mainExcel.writeHeaderToSheet("Entity",wb)
   self.readDataFrame(conn)
   self.checkForData(conn,mainExcel,wb)
   self.checkForValidColumns(conn,mainExcel,wb)

   self.CheckEntityLevelPBM(conn,mainExcel,wb)
   self.checkegwp(conn,mainExcel,wb)
   self.Check_for_len_zipCode(conn,mainExcel,wb)
   self.Check_ForIS_Parent(conn,mainExcel,wb)
   self.Check_ForISActive(conn,mainExcel,wb)
   self.Check_is_Parent_TRICARE(conn,mainExcel,wb)
   self.check_is_Active_Cash(conn,mainExcel,wb)
   self.check_is_Active_OtherThirdParty(conn,mainExcel,wb)
   self.check_Entity_Type(conn,mainExcel,wb)
   self.checkEntityLevelForCorporate(conn,mainExcel,wb)
   self.CheckForTricareEntityLevel(conn,mainExcel,wb)
   self.checkEntityLevelForCompany(conn,mainExcel,wb)
   self.checkEntityLevelForAffilates_Employees(conn,mainExcel,wb)


  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.entity "
      self.EntityDataFrame = pd.read_sql(sqlst, conn)
      print(self.EntityDataFrame.head())

  def checkForData(self, conn, mainExcel, wb):
      print("Check for Data Exists or not ")
      if (self.EntityDataFrame.__len__() > 0):
          self.passed = self.passed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
          mainExcel.ExpectedResult = "The Enitiy Table should contain data"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
          # mainExcel.writeToSheet("Entity", wb)

      else:
          print("FAILED")
          self.failed = self.failed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
          mainExcel.ExpectedResult = "The Enitiy Table should contain data"
          mainExcel.TestFailDescription = "Data is not present in the Entity table"
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def checkForValidColumns(self,conn,mainExcel,wb):
    print(self.EntityDataFrame.__len__())
    expectedcolumnnames = {"EntityID", "EntityType", "EntityLevel", "EntityName", "EntityState", "EntityAffiliationID",
                           "StreetAddress", "SuiteNum", "City", "State", "Zip", "Phone", "IsParent", "IsActive",
                           "IsChild", "NewDrugCoveragePolicy", "WaitingPeriod", "ExceptionDetails",
                           "UpdateScheduleP&TCommittee", "PlanWebSite"}
    presentColumnList = self.EntityDataFrame.columns.tolist()
    result =  set(expectedcolumnnames).difference(set(presentColumnList))
    if((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
        self.passed = self.passed +1
        mainExcel.Module = "Entity"
        mainExcel.TestCaseName = "Check for valid Columns"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "None"
        mainExcel.TestFailSeverity = "None"
        mainExcel.TestCaseStatus = "PASSED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
        #mainExcel.writeToSheet("Entity", wb)

    else:
        print("FAILED")
        self.failed = self.failed+ 1
        mainExcel.Module = "Entity"
        mainExcel.TestCaseName = "Check for valid Columns"
        mainExcel.ExpectedResult = "Given Coulmn name should be present"+str(expectedcolumnnames)
        mainExcel.TestFailDescription = "Specified column names are not present"+str(result)
        mainExcel.TestFailSeverity = "Critical"
        mainExcel.TestCaseStatus = "FAILED"
        DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
        #mainExcel.writeToSheet("Entity", wb)

  def CheckEntityLevelPBM(self,conn,mainExcel,wb):
      print(self.EntityDataFrame.__len__())
      entityLevelPBM = self.EntityDataFrame.loc[
          (self.EntityDataFrame['EntityType'] == 'PBM') & (self.EntityDataFrame['EntityLevel'] != 'National')]
      print(entityLevelPBM.__len__())
      if(entityLevelPBM.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for PBM"
          mainExcel.ExpectedResult = "National should display"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for PBM"
          mainExcel.ExpectedResult = "National should display"
          mainExcel.TestFailDescription = "National is not present for"+pd.DataFrame(entityLevelPBM).values
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkegwp(self,conn,mainExcel,wb):
      print(self.EntityDataFrame.__len__())
      entityForEGWP = self.EntityDataFrame.loc[self.EntityDataFrame['EntityType'] == 'EGWP']
      print(entityForEGWP.__len__())
      #"Entity", "Passed", "Check EGWP under EntityType column", "EGWP should be present", ""
      if(entityForEGWP.__len__ == 0):
          self.failed = self.failed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check EGWP under EntityType column"
          mainExcel.ExpectedResult = "EGWP should be present"
          mainExcel.TestFailDescription =  "EGWP entity type is not present"+pd.DataFrame(entityForEGWP).values
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check EGWP under EntityType column"
          mainExcel.ExpectedResult = "EGWP should be present"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def Check_for_len_zipCode(self,conn,mainExcel,wb):
      print(self.EntityDataFrame.__len__())
      ZipCodeDataFrame = self.EntityDataFrame.loc[(self.EntityDataFrame['Zip'].map(str).apply(len) > 5)].dropna()
      # ZipCodeDataFrame.dropna()
      print(ZipCodeDataFrame.__len__())
     #"Entity", "Failed", "Check the length of the ZIP code","Length should be minimum 5 digits","Length of zip code is wrong"
      if(ZipCodeDataFrame.__len__() == 0):
          self.passed = self.passed + 1


          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the length of the ZIP code"
          mainExcel.ExpectedResult = "Length should be minimum 5 digits"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


      else:
          self.failed = self.failed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the length of the ZIP code"
          mainExcel.ExpectedResult = "Length should be minimum 5 digits"
          mainExcel.TestFailDescription = "Length of zip code is wrong"+str(ZipCodeDataFrame['EntityID'].values)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)


  def Check_ForIS_Parent(self,conn,mainExcel,wb):
      print(self.EntityDataFrame.__len__())
      isParentDataFrame = self.EntityDataFrame.loc[(self.EntityDataFrame['EntityName'].str.contains('(Corporate)')) & (self.EntityDataFrame['IsParent'] != 'Y')]
      print("is parent",isParentDataFrame.__len__())
      isParentDataFrame = isParentDataFrame[~ isParentDataFrame['EntityName'].str.contains('(Closed)')]
      if(isParentDataFrame.__len__() == 0):
          self.passed = self.passed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check for the 'Is Parent' column"
          mainExcel.ExpectedResult =  "IsParent column should contain 'Y'/'N'.All Parent plans should fall under'Y'All child plans should fall under'N'"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          self.failed = self.failed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check for the 'Is Parent' column"
          mainExcel.ExpectedResult =  "IsParent column should contain 'Y'/'N'.All Parent plans should fall under'Y'All child plans should fall under'N'"
          mainExcel.TestFailDescription = "Is parent column does not conatins either Y or N  for given entites"+str(isParentDataFrame['EntityID'].values)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def Check_ForISActive(self,conn,mainExcel,wb):
      print(self.EntityDataFrame.__len__())
      isActiveDataFrame = self.EntityDataFrame.loc[(self.EntityDataFrame['EntityName'].str.contains('(Closed)')) & (self.EntityDataFrame['IsActive'] == 'Y')]
      print("is parent",isActiveDataFrame.__len__())

      if(isActiveDataFrame.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check for the 'Is Active' column"
          mainExcel.ExpectedResult =   "Is Active column should contain 'Y'/'N'.All actives plans should fall under 'Y'All closed plans should fall under 'N'"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          self.failed = self.failed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check for the 'Is Active' column"
          mainExcel.ExpectedResult =   "Is Active column should contain 'Y'/'N'.All actives plans should fall under 'Y'All closed plans should fall under 'N'"
          mainExcel.TestFailDescription = "Is active column conatins 'Y' for closed Entites"+str(isActiveDataFrame['EntityID'].values)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def Check_is_Parent_TRICARE(self,conn,mainExcel,wb):
      print(self.EntityDataFrame.__len__())
      isTriCareDataFrame = self.EntityDataFrame.loc[(self.EntityDataFrame['EntityName'] == 'TRICARE') & (self.EntityDataFrame['IsParent'] != 'Y')]
      print("is TRICARE",isTriCareDataFrame.__len__())

      if(isTriCareDataFrame.__len__() == 0):

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check 'Is Parent' column for TRICARE channel"
          mainExcel.ExpectedResult =   "Is Parent' Column should be 'Y'"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check 'Is Parent' column for TRICARE channel"
          mainExcel.ExpectedResult =   "Is Parent' Column should be 'Y'"
          mainExcel.TestFailDescription = "The Is parent coulmn is not Y for Entity ID"+str(isTriCareDataFrame['EntityID'].values)
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def check_is_Active_Cash(self,conn,mainExcel,wb):
      print(self.EntityDataFrame.__len__())
      isTriCareDataFrame = self.EntityDataFrame.loc[
          (self.EntityDataFrame['EntityType'] == 'Cash') & (self.EntityDataFrame['IsActive'] == 'Y')]

      print("is CASH",isTriCareDataFrame.__len__())

      if(isTriCareDataFrame.__len__() == 0):
          self.passed = self.passed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check 'Is Active' column for CASH"
          mainExcel.ExpectedResult =   "'Is Active' Column should be 'N'"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check 'Is Active' column for CASH"
          mainExcel.ExpectedResult = "'Is Active' Column should be 'N'"
          mainExcel.TestFailDescription ="The Is Active coulmn is not N for Entity ID"+str(isTriCareDataFrame['EntityID'].values)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def check_is_Active_OtherThirdParty(self,conn, mainExcel, wb):
      print(self.EntityDataFrame.__len__())
      isOtherThirdPartyDataFrame = self.EntityDataFrame.loc[
          (self.EntityDataFrame['EntityType'] == 'Other Third Party') & (self.EntityDataFrame['IsActive'] == 'Y')]

      print("is CASH", isOtherThirdPartyDataFrame.__len__())

      if (isOtherThirdPartyDataFrame.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check 'Is Active' column for Other Third Party"
          mainExcel.ExpectedResult =   "'Is Active' Column should be 'N'"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:
          self.failed = self.failed+1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check 'Is Active' column for Other Third Party"
          mainExcel.ExpectedResult =   "'Is Active' Column should be 'N'"
          mainExcel.TestFailDescription ="The Is Active coulmn is not N for Entity ID" + str(
              isOtherThirdPartyDataFrame['EntityID'].values)
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def check_Entity_Type(self,conn, mainExcel, wb):
       print("Check For Entity Type")
       entityTypeSet = {'TriCare',
                        'MCO',
                        'Specialty Provider',
                        'Other Third Party',
                        'State Medicaid',
                        'Employer',
                        'Stand Alone HIX',
                        'EGWP',
                        'Cash',
                        'Stand-Alone Medicare',
                        'PBM',
                        'VA'}
       entityTypeFromDF = self.EntityDataFrame['EntityType'].unique()
       result = entityTypeSet.difference(set(entityTypeFromDF))
       if (result.__len__() == 0):
           self.passed = self.passed + 1
           mainExcel.Module = "Entity"
           mainExcel.TestCaseName = "Check for Entity Type "
           mainExcel.ExpectedResult = "The Given Entity Type Should BE present"+entityTypeSet.__str__()
           mainExcel.TestFailDescription = "None"
           mainExcel.TestFailSeverity = "None"
           mainExcel.TestCaseStatus = "PASSED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
       else:
           self.failed = self.failed + 1

           mainExcel.Module = "Entity"
           mainExcel.TestCaseName = "Check for Entity Type "
           mainExcel.ExpectedResult = "The Given Entity Type Should BE present"+entityTypeSet.__str__()
           mainExcel.TestFailDescription ="The Specified Entity are not present"+result.__str__()
           mainExcel.TestFailSeverity = "Informational"
           mainExcel.TestCaseStatus = "FAILED"
           DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
  def checkEntityLevelForCorporate(self,conn, mainExcel, wb):
      print("Check for Entity Level for corporate")
      errormessage = ""
      entityLevelForCorporateDF = pd.DataFrame
      entityLevelForCorporate = ['Regional','National']
      entityLevelForCorporateDF = self.EntityDataFrame.loc[(self.EntityDataFrame['EntityName'].str.contains('(Corporate)')) &(self.EntityDataFrame['IsParent'] == 'Y') ]
      ##entityLevelFromDF = pd.Series(entityLevelForCorporateDF['EntityLevel']).unique()
      print(pd.Series(entityLevelForCorporateDF['EntityLevel']).unique())

      #print("Entity Level from corporate",entityLevelFromDF)
      result = entityLevelForCorporateDF.loc[~entityLevelForCorporateDF['EntityLevel'].isin(entityLevelForCorporate)]
      for row in result.iterrows():
           EntityID = row[1]['EntityID']
           EntityLevel = row[1]['EntityLevel']
           if (EntityLevel == 'Local'):
                count = pd.DataFrame(self.EntityDataFrame.loc[self.EntityDataFrame['EntityID'] == EntityID ]).__len__()
                if(count > 1):
                    errormessage = errormessage +","+str(EntityID)
           else:

               errormessage = errormessage + "," + str(EntityID)
      print("errormessage",errormessage)
      if (errormessage.__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Corporate "
          mainExcel.ExpectedResult = "National and Regional should display"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Corporate "
          mainExcel.ExpectedResult = "National and Regional should display"
          mainExcel.TestFailDescription = "The Entity is not at Regional and National level" + errormessage
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def CheckForTricareEntityLevel(self,conn, mainExcel, wb):
      print("Check For Entity Tricare")
      entityLevelForTricareDF = self.EntityDataFrame.loc[
          (self.EntityDataFrame['EntityName'] == 'Tricare') & (self.EntityDataFrame['EntityLevel'] != 'National')]

      print("result",entityLevelForTricareDF['EntityLevel'].unique())
      if (entityLevelForTricareDF.__len__() == 0):
          self.passed = self.passed + 1


          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Tricare "
          mainExcel.ExpectedResult ="National  should display"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Tricare "
          mainExcel.ExpectedResult = "National  should display"
          mainExcel.TestFailDescription =  "The Entity are present with other levels" + str(entityLevelForTricareDF['EntityLevel'].unique())
          mainExcel.TestFailSeverity = "Critical"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkEntityLevelForCompany(self,conn,mainExcel, wb):
      print("Check for Entity Level for corporate")
      errormessage = ""
      entityLevelForCorporateDF = pd.DataFrame
      entityLevelForCorporateDF = self.EntityDataFrame.loc[(self.EntityDataFrame['EntityName'].str.contains('\(Company\)')) &(self.EntityDataFrame['EntityLevel'] != 'Regional') ]
      ##entityLevelFromDF = pd.Series(entityLevelForCorporateDF['EntityLevel']).unique()
      print(pd.Series(entityLevelForCorporateDF['EntityLevel']).unique())
      #print("Entity Level from corporate",entityLevelFromDF)


      print("result rrrrrrrrrrrrrrr",entityLevelForCorporateDF['EntityLevel'].unique())
      for row in entityLevelForCorporateDF.iterrows():
           EntityID = row[1]['EntityID']
           EntityLevel = row[1]['EntityLevel']
           if (EntityLevel == 'Local'):
                count = pd.DataFrame(self.EntityDataFrame.loc[self.EntityDataFrame['EntityID'] == EntityID ]).__len__()
                if(count > 1):
                    errormessage = errormessage +","+str(EntityID)

      if (errormessage.__len__() == 0):
          self.passed = self.passed + 1

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Company  "
          mainExcel.ExpectedResult =" Regional should display"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
      else:
          self.failed = self.failed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Company  "
          mainExcel.ExpectedResult =" Regional should display"
          mainExcel.TestFailDescription = "The Entity is not at Regional  level" + errormessage
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def checkEntityLevelForAffilates_Employees(self,conn,mainExcel, wb):
      print("Check for  EntityLevelForAffilates_Employees")
      entityLevelForCorporateDF = pd.DataFrame
      entityLevelForCorporateDF = self.EntityDataFrame.loc[~((self.EntityDataFrame['EntityName'].str.contains('(Company)'))|(self.EntityDataFrame['EntityName'].str.contains('(Corporate)'))) &(self.EntityDataFrame['IsParent'] == 'N') &(self.EntityDataFrame['EntityLevel'] != 'Local')]

      ##entityLevelFromDF = pd.Series(entityLevelForCorporateDF['EntityLevel']).unique()
      print(entityLevelForCorporateDF['EntityType'])
      EntityTypeNotPBM = entityLevelForCorporateDF.loc[~ entityLevelForCorporateDF['EntityType'].isin(['PBM','Stand-Alone Medicare'])]
      print("Entity Level from Affilates",EntityTypeNotPBM['EntityLevel'].unique())
      if (pd.Series(EntityTypeNotPBM['EntityLevel']).tolist().__len__() == 0):
          self.passed = self.passed + 1
          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Affiliates, Employers (including EGWP) "
          mainExcel.ExpectedResult = " Regional should display"
          mainExcel.TestFailDescription = "None"
          mainExcel.TestFailSeverity = "None"
          mainExcel.TestCaseStatus = "PASSED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

      else:

          mainExcel.Module = "Entity"
          mainExcel.TestCaseName = "Check the EntityLevel for Affiliates, Employers (including EGWP) "
          mainExcel.ExpectedResult = " Regional should display"
          mainExcel.TestFailDescription ="The Entities are found given entity level" + str(EntityTypeNotPBM['EntityLevel'].unique())
          mainExcel.TestFailSeverity = "Informational"
          mainExcel.TestCaseStatus = "FAILED"
          DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

  def saveResultToDataBase(self,conn,mainExcel):
       print("Saving result to Database")

       cursor = conn.cursor()
       cursor.execute(
           'EXEC dbo.uspQCProcessLogDtl @QLID = ? ,@Module = ?,@TestCaseName = ?,@ExpectedResult = ?,@TestFailDescription = ?,@TestFailSeverity = ?,@TestCaseStatus = ?',mainExcel.QLID,mainExcel.Module,mainExcel.TestCaseName,mainExcel.ExpectedResult,mainExcel.TestFailDescription,mainExcel.TestFailSeverity,mainExcel.TestCaseStatus)

       conn.commit()
