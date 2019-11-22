import pandas as pd
import DatabaseConnection
class ChannelRollup:
    ChannelRollupDataFrame = pd.DataFrame()
    EntityData = pd.DataFrame()
    passed = 0
    failed = 0
    def __call__(self):
        print("somthing")

    def executeScripts(self, conn, mainExcel, wb):
        print("In AccountRollup", conn)
        #mainExcel.writeHeaderToSheet("ChannelRollup", wb)
        self.readDataFrame(conn)
        self.checkForBalnkSpaces(conn,mainExcel,wb)
        self.checksubchannelbasedChannel(conn,mainExcel,wb)
        self.checkForData(conn, mainExcel, wb)


    def readDataFrame(self, conn):
        print("Reading Data Frame")
        sqlst = "SELECT * FROM stg.ChannelRollup "
        self.ChannelRollupDataFrame = pd.read_sql(sqlst, conn)
        sqlst = "SELECT * FROM stg.Entity "
        self.EntityData = pd.read_sql(sqlst, conn)
        print(self.EntityData.head())

    def checkForData(self, conn, mainExcel, wb):
        print("Check for Data Exists or not ")
        if (self.ChannelRollupDataFrame.__len__() > 0):
            self.passed = self.passed + 1
            mainExcel.Module = "ChannelRollup"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Channel Rollup Table should contain data"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
            # mainExcel.writeToSheet("Entity", wb)

        else:
            print("FAILED")
            self.failed = self.failed + 1
            mainExcel.Module = "ChannelRollup"
            mainExcel.TestCaseName = "Check for the data avalaiblity in the table"
            mainExcel.ExpectedResult = "The Channel Rollup Table should contain data"
            mainExcel.TestFailDescription = "Data is not present in the Account Rollup table"
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def checkForBalnkSpaces(self,conn, mainExcel, wb):
        print("Check for Blank Spaces")
        expectedList = ['Channel', 'SubChannel']
        null_columns = self.ChannelRollupDataFrame.columns[self.ChannelRollupDataFrame.isnull().any()].tolist()
        print(null_columns)
        result = set(null_columns).difference(set(expectedList))
        print(result)
        if (result.__len__() == 0):
            self.passed = self.passed+1
            mainExcel.Module = "ChannelRollup"
            mainExcel.TestCaseName = "Check Blank space for columns"
            mainExcel.ExpectedResult = "Blank space should not present any of the columns given 'EntityID', 'SubChannel' column"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
        else:
            self.failed = self.failed + 1
            mainExcel.Module = "ChannelRollup"
            mainExcel.TestCaseName = "Check Blank space for columns"
            mainExcel.ExpectedResult = "Blank space should not present any of the columns given 'EntityID', 'SubChannel' column"
            mainExcel.TestFailDescription =  "Blanks are Present for other Coulmns" + str(result)
            mainExcel.TestFailSeverity = "Informational"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def checksubchannelbasedChannel(self,conn, mainExcel, wb):
        """expectedDic = {"Cash": "Cash",
                       "Commercial": "Commercial",
                       "Managed Medicaid": "Commercial",
                       "Employer": "Employer",
                       "CVS FEP": "Government",
                       "TRICARE": "Government",
                       "VA": "Government",
                       "MA": "Medicare",
                       "MA-PD": "Medicare",
                       "PDP": "Medicare",
                       "Medicare Other": "Medicare",
                       "Other Third Party": "Other Third Party",
                       "PBM": "PBM",
                       "SPP": "SPP",
                       "State Medicaid": "State Medicaid"}"""
        expectedDic = mainExcel.channelRollupDictionary
        sub_channel_dic = {}
        for row in self.ChannelRollupDataFrame.iterrows():
            SubChannel = row[1]['SubChannel']
            channel =  row[1]['Channel']
            sub_channel_dic.update({SubChannel: channel})
        result = expectedDic.items() - sub_channel_dic.items()

        if (result.__len__() == 0):
            self.passed = self.passed + 1
            mainExcel.Module = "ChannelRollup"
            mainExcel.TestCaseName = "Check SubChannels Based on Channels"
            mainExcel.ExpectedResult =  "Subchannel should appear according to Channel"
            mainExcel.TestFailDescription = "None"
            mainExcel.TestFailSeverity = "None"
            mainExcel.TestCaseStatus = "PASSED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)
        else:
            self.failed = self.failed + 1
            mainExcel.Module = "ChannelRollup"
            mainExcel.TestCaseName = "Check SubChannels Based on Channels"
            mainExcel.ExpectedResult =  "Subchannel should appear according to Channel"
            mainExcel.TestFailDescription = "Specified Subchannels's channels are not found" + result.__str__()
            mainExcel.TestFailSeverity = "Critical"
            mainExcel.TestCaseStatus = "FAILED"
            DatabaseConnection.Connection.saveResultToDataBase(conn, mainExcel)

    def saveResultToDataBase(self,conn,mainExcel):
       print("Saving result to Database")

       cursor = conn.cursor()
       cursor.execute(
           'EXEC dbo.uspQCProcessLogDtl @QLID = ? ,@Module = ?,@TestCaseName = ?,@ExpectedResult = ?,@TestFailDescription = ?,@TestFailSeverity = ?,@TestCaseStatus = ?',mainExcel.QLID,mainExcel.Module,mainExcel.TestCaseName,mainExcel.ExpectedResult,mainExcel.TestFailDescription,mainExcel.TestFailSeverity,mainExcel.TestCaseStatus)

       conn.commit()
