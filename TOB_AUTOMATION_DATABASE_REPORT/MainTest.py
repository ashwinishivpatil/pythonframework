import matplotlib.pyplot as plt
import numpy as np
import DatabaseConnection
from Entity import Entity
from EntityFormulary import EntityFormulary
from Drug import Drug
from DrugFormularyStatus import DrugFormularyStatus
from DrugFormularyRestrictions import DrugFormularyRestrictions
from AccountRollup import AccountRollup
from ChannelRollup import ChannelRollup
from Drug import Drug
from PlanProduct import PlanProduct
from Person import Person
from PBMServices import PBMServices
from KeyContact import KeyContact
from IMSBridge import IMSBridge
from Formulary import Formulary
from EntityPerson import EntityPerson
from EntityProduct import EntityProduct
from EntityProductFormulary import EntityProductFormulary
from EntitySubChannel import EntitySubChannel
from Test1 import Test1
from PredominantForCorporate import PredominantForCorporate
from PredominantStatusForN import PredominantStatusForN
from PreDominantStatusForPBM import PreDominantStatusForPBM
from EntityBenifitDesign import EntityBenifitDesign
import ExcelReport
import CreatePDFReport
import pandas
import sys


total_passed = 0
total_failed = 0
listOfModuleName=[]
listOfFailTest = []
listOfPassTest = []
#print("system argument",sys.argv[0])
#print("system argument",sys.argv[1])
mainExcel = ExcelReport.ExcelReports()
mainExcel.configFileName = sys.argv[1]
connclose =DatabaseConnection.Connection
#mainExcel.configFileName = "Config.txt"
conn = DatabaseConnection.Connection.getConnection(mainExcel.configFileName)
configDictionary = DatabaseConnection.Connection.ConfigProperties(mainExcel.configFileName)
NumberOfModules = configDictionary.get("numberofmodules")
#mainExcel = ExcelReport.ExcelReports()
mainExcel.fileName = configDictionary.get("FileName")
chartName = configDictionary.get("ChartName")
pdfFileName =  configDictionary.get("PdfName")
#wb = mainExcel.createWorkBook(configDictionary.get("FileName"))
wb=""
try:
    cursor = conn.cursor()
    cursor.execute('EXEC dbo.uspQCProcessLogStart @PLID = ? ', 1003, )
    conn.commit()
    sqlst = "SELECT max(QLID) FROM dbo.QCProcessLog "
    getQLID = cursor.execute(sqlst)
    tupleValues = cursor.fetchone()
    print(tupleValues[0])
    print(NumberOfModules)
    mainExcel.QLID = tupleValues[0]
    mainExcel.channelList = configDictionary.get("channelList")
    mainExcel.DrugList = configDictionary.get("DrugList")
    mainExcel.productList = configDictionary.get("productList")
    mainExcel.accountrollupExpectedSubChannelsList = configDictionary.get("accountrollupExpectedSubChannelsList")
    mainExcel.channelRollupDictionary = configDictionary.get("channelRollupDictionary")
    mainExcel.DrugFormularyStatusList = configDictionary.get("DrugFormularyStatusList")
    mainExcel.EntityFormularyList = configDictionary.get("EntityFormularyList")
    mainExcel.EntityProductList = configDictionary.get("EntityProductList")
    mainExcel.EntityProductFormularyList = configDictionary.get("EntityProductFormularyList")
    mainExcel.EntitySubChannelList = configDictionary.get("EntitySubChannelList")
    mainExcel.IMSBridgeList = configDictionary.get("IMSBridgeList")
    mainExcel.PBMServicesList = configDictionary.get("PBMServicesList")
    for each in range(1,int(NumberOfModules)):
        key = "module"+str(each)
        moduleName = configDictionary.get(key)
        print(moduleName)
        #mainExcel.createSheet(moduleName,wb)

        clas = globals()[moduleName]

        #func = clas.__dict__["executeScripts"]
        #mainExcel.channelList = configDictionary.get("channelList")
        #mainExcel.DrugList = configDictionary.get("DrugList")
        #mainExcel.productList = configDictionary.get("productList")
        obj = clas()
        obj.executeScripts(conn, mainExcel, wb)
        print(obj.passed)
        print(obj.failed)
        total_passed= total_passed+obj.passed
        total_failed = total_failed + obj.failed

        listOfModuleName.append(moduleName)
        listOfFailTest.append(obj.failed)
        listOfPassTest.append(obj.passed)
        #A = type(moduleName, (), {})
        #x = A()
        #(moduleName.__class__).readEntityDataFrame(conn,mainExcel,wb)
        print(clas)

    connclose = DatabaseConnection.Connection.getConnection(mainExcel.configFileName)
    cursor1 = connclose.cursor()
    cursor1.execute('EXEC dbo.uspQCProcessLogEnd  @QLID = ? ', mainExcel.QLID, )
    connclose.commit()

except Exception as e:
    print('Failed to upload to ftp: '+ str(e))
    print("Somthing went Wrong")
    conn.close()
    connclose.close()
    #wb.close()
    #conn.close()
finally:
    #conn.close()
    conn.close()
    connclose.close()
    #wb.close()

"""index=np.arange(len(listOfModuleName))
plt.bar(index+0,listOfPassTest,color='b',width=.4,label="Passed Testcases -"+str(total_passed))
plt.bar(index+0.4,listOfFailTest,color='r',width=.4,label="Failed Testcases - "+str(total_failed))
#plt.bar(index+0,listOfPassTest,color='g',width=.4,label="Passed Testcases",zorder=2)
#plt.bar(index+0.4,listOfFailTest,color='r',width=.4,label="Failed Testcases",zorder=2)
plt.xlabel('File Names',fontsize=10)
plt.ylabel('No. of Testcases',fontsize=10)
plt.xticks(index+0.2, listOfModuleName, fontsize=8, rotation=90)
plt.title("TOB Payer Back Bone Testing Status")
plt.grid(axis='y')
plt.legend()
plt.savefig(chartName)"""


#CreatePDFReport.CreatePDF(mainExcel.fileName,chartName,pdfFileName)
#EntityFormulary.EntityFormulary.readEntityFormularyDataFrame(conn)





