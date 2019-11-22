import pandas as pd
import DatabaseConnection

class Drug :
    DrugDataFrame = pd.DataFrame
    passed = 0
    failed = 0
    def __call__(self):
        print("somthing")

    def executeScripts(self, conn, mainExcel, wb):
        print("In Drug", conn)

    def executeScripts(self, conn, mainExcel, wb):
        print("In Drug", conn)
        #mainExcel.writeHeaderToSheet("Drug", wb)
        self.readDataFrame(conn)
        self.checkForValidColumns(conn,mainExcel,wb)
        self.CheckAdministeredByColumn(conn,mainExcel,wb)
        self.CheckDesignationColumn(conn,mainExcel,wb)
        self.check_for_Blank_Columns(conn,mainExcel,wb)


    def readDataFrame(self, conn):
        print("Reading Data Frame")
        sqlst = "SELECT * FROM stg.Drug "
        self.DrugDataFrame = pd.read_sql(sqlst, conn)
        sqlst = "SELECT * FROM stg.Entity "
        self.EntityData = pd.read_sql(sqlst, conn)
        print(self.EntityData.head())

    def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.DrugDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Drug Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Drug  Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the Drug table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def checkForValidColumns(self,conn, mainExcel, wb):
        print(self.DrugDataFrame.__len__())
        expectedcolumnnames = {"DrugID","DrugName","DrugStrength","DrugForm","IsGroup","GroupID","DrugType","IsSingleStrength","IsDiscontinued","DrugDesignation","AdministeredBy"}
        presentColumnList = self.DrugDataFrame.columns.tolist()
        result = set(expectedcolumnnames).difference(set(presentColumnList))
        if ((set(expectedcolumnnames).difference(set(presentColumnList)).__len__()) == 0):
            self.passed = self.passed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Validate Column Names"
            mainExcel.ExpectedResult = "Given Coulmn name should be present" + str(expectedcolumnnames)
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Validate Column Names"
            mainExcel.ExpectedResult = "Given Coulmn name should be present" + str(expectedcolumnnames)
            mainExcel.TestFailDescription =  "Specified column names are not present" + str(result)
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def validateDrugs(self,conn, mainExcel, wb):
        print(self.DrugDataFrame.__len__())
        subDrugList = self.DrugDataFrame['DrugName'].values.tolist()
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
        print("subChannelsList", subDrugList)
        result = expectedSDrugs.difference(set(subDrugList))
        if (result.__len__() == 0):

            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check the Drugs"
            mainExcel.ExpectedResult = "Given Drugs name should be present" + expectedSDrugs.__str__()
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

        else:
            print("FAILED")
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check the Drugs"
            mainExcel.ExpectedResult = "Given Drugs name should be present" + expectedSDrugs.__str__()
            mainExcel.TestFailDescription ="Specified Drugs are not present" + str(result)
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def CheckAdministeredByColumn(self,conn,mainExcel, wb):
        print(self.DrugDataFrame.__len__())
        expectedSet = {'Pharmacy'}
        adminstartorColumnList = pd.Series(self.DrugDataFrame['AdministeredBy']).values

        result = expectedSet.difference(set(adminstartorColumnList))
        if (result.__len__() == 0):
            self.passed = self.passed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check for the AdministeredByColumn for 'Pharmacy'"
            mainExcel.ExpectedResult =  "Expected values should be present" + expectedSet.__str__()
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

        else:
            print("FAILED")
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check for the AdministeredByColumn for 'Pharmacy'"
            mainExcel.ExpectedResult =  "Expected values should be present" + expectedSet.__str__()
            mainExcel.TestFailDescription = "We have other data in AdministeredByColumn" + result.__str__()
            mainExcel.TestFailSeverity = "Informational"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def  CheckDesignationColumn(self,conn,mainExcel, wb):
        print(self.DrugDataFrame.__len__())
        expectedSet = {'Generic', 'Single', 'Multi'}
        DesignatedColumnList = (pd.Series(self.DrugDataFrame['DrugDesignation'].dropna()).values)
        DesignatedColumnList = list(DesignatedColumnList)
        print("DesignatedColumnList",DesignatedColumnList)
        result = set(DesignatedColumnList).difference(expectedSet)

        if (result.__len__() == 0):

            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check for the DesignationColumn for Generic,Single,Multi"
            mainExcel.ExpectedResult =  "Designation should be Generic/Single/Multi"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check for the DesignationColumn for Generic,Single,Multi"
            mainExcel.ExpectedResult =  "Designation should be Generic/Single/Multi"
            mainExcel.TestFailDescription = "We have other data in Designated" + result.__str__()
            mainExcel.TestFailSeverity = "Informational"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def check_for_Blank_Columns(self,conn,mainExcel, wb):
        global passed, failed
        ExpectedList = {"DrugID", "DrugName", "DrugStrength", "DrugForm", "IsGroup", "GroupID", "DrugType",
                        "IsSingleStrength", "IsDiscontinued"}
        exceptList  = {"DrugDesignation", "AdministeredBy"}
        null_columns = self.DrugDataFrame.columns[self.DrugDataFrame.isnull().any()]
        columnNAme = pd.Index(null_columns).values
        print(columnNAme)
        result = set(null_columns).difference(exceptList)
        if(list(result).__len__() == 0):
            self.passed = self.passed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check blank space for columns"
            mainExcel.ExpectedResult =  "Balnk spaces should not be present for given columns" + str(ExpectedList)
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "Drug"
            mainExcel.TestCaseName = "Check blank space for columns"
            mainExcel.ExpectedResult =  "Balnk spaces should not be present for given columns" + str(ExpectedList)
            mainExcel.TestFailDescription = "Blanks are present for following columns" + str(result)
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

