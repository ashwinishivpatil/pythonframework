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
import ExcelReport
import CreatePDFReport
from  PredominantStatusForN import PredominantStatusForN
from  PredominantForCorporate import PredominantForCorporate
from PreDominantStatusForPBM import PreDominantStatusForPBM
total_passed = 0
total_failed = 0
listOfModuleName=[]
listOfFailTest = []
listOfPassTest = []
try:
    conn = DatabaseConnection.Connection.getConnection()
    configDictionary = DatabaseConnection.Connection.ConfigProperties()
    mainExcel = ExcelReport.ExcelReports()
    mainExcel.fileName = configDictionary.get("FileName")
    chartName = configDictionary.get("ChartName")
    pdfFileName = configDictionary.get("PdfName")
    wb = ""
    a =  PredominantStatusForN()
    a.executeScripts(conn, mainExcel, wb)
except Exception as e:
    print('Failed to upload to ftp: '+ str(e))
    print("Somthing went Wrong")
    #conn.close()
finally:
    conn.close()