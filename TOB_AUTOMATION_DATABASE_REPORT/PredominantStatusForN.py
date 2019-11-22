import pandas as pd

import math
import DatabaseConnection

class PredominantStatusForN :
  AccountRollupDataFrame = pd.DataFrame
  EntityFormularyDataFrame = pd.DataFrame
  DrugFormularyRestrictionDataFrame = pd.DataFrame
  DrugFormularyStatusDataFrame = pd.DataFrame
  EntityDataFrame = pd.DataFrame
  PredominantFormularyDataDataFrame = pd.DataFrame
  entityList=[]
  predominantdatBasedonEntityList = pd.DataFrame
  predominantStatusDic = {}
  predominantRestricitionDic = {}
  predominantCopayDic = {}
  rankingDictionary = {}
  passed = 0
  failed = 0
  def executeScripts(self,  conn, mainExcel, wb):
    print("In AccountRollup",conn)
    self.readDataFrame(conn)
    self.getEntityISParentN()
    self.readPredominantStatusFile()
    self.Compare(conn, mainExcel, wb)

    #mainExcel.writeHeaderToSheet("AccountRollup", wb)

  def  readDataFrame(self,conn):
      print("Reading Data Frame")
      sqlst = "SELECT * FROM stg.AccountRollup "
      self.AccountRollupDataFrame = pd.read_sql(sqlst, conn)
      #print(self.AccountRollupDataFrame.head())

      sqlst = "SELECT * FROM stg.Entity "
      self.EntityDataFrame = pd.read_sql(sqlst, conn)
      #print(self.EntityDataFrame.head())

      sqlst = "SELECT * FROM stg.entityformulary"
      self.EntityFormularyDataFrame = pd.read_sql(sqlst, conn)
      #print(self.EntityFormularyDataFrame.head())

      sqlst = "SELECT * FROM stg.drugformularystatus  "
      self.DrugFormularyStatusDataFrame = pd.read_sql(sqlst, conn)
      #print(self.DrugFormularyStatusDataFrame.head())

      sqlst = "SELECT * FROM stg.DrugFormularyRestrictions  "
      self.DrugFormularyRestrictionDataFrame = pd.read_sql(sqlst, conn)
      #print(self.DrugFormularyStatusDataFrame.head())

      sqlst = "SELECT * FROM stg.PredominantFormularyData  "
      self.PredominantFormularyDataDataFrame = pd.read_sql(sqlst, conn)
      #print(self.PredominantFormularyDataDataFrame.__len__())


  def getEntityISParentN(self):
      entity = self.EntityDataFrame.loc[(self.EntityDataFrame['IsParent'] == "N") & (self.EntityDataFrame['EntityType'] != "PBM")]
      #self.entityList.append(pd.Series(entity['EntityID']).values[1])
      #self.entityList.append(pd.Series(entity['EntityID']).values[2])
      #self.entityList = list(pd.Series(entity['EntityID']).values)
      self.entityList.append(pd.Series(entity['EntityID']).values[1])
      #print(self.entityList)


  def readPredominantStatusFile(self):
      print("Reading predominant status")
      self.predominantdatBasedonEntityList = self.PredominantFormularyDataDataFrame.loc[(self.PredominantFormularyDataDataFrame['EntityID'].isin(self.entityList) )&(self.PredominantFormularyDataDataFrame['CalculationType'] == 'Granular')]
      #print("Reading predominant status",self.predominantdatBasedonEntityList.head())
      for row in self.predominantdatBasedonEntityList.iterrows():
          #print("reading each row",row)
          entityId= row[1]['EntityID']
          channel= row[1]['SubChannel']
          drugID = row[1]['DrugID']
          predominantStatus = row[1]['PredominantStatus']
          predominantRestricition =  row[1]['PredominantRestriction']
          copayMax = row[1]['CoPayMax']
          copayMin = row[1]['CoPayMin']
          key = str(entityId) + "|" + channel + "|" + str(drugID)
          restricition = str(predominantRestricition).replace(" ", "")
          if (restricition == ''):
              restricition = "None"
          value = predominantStatus
          self.predominantStatusDic.update({key: value})
          self.predominantRestricitionDic.update({key:restricition})
          self.predominantCopayDic.update({key:str(copayMax) + "|" + str(copayMin)})
      #print("len",self.predominantStatusDic.__len__())
      #print("self.predominantCopayDic",self.predominantCopayDic)


  def Compare(self,conn,mainExcel,wb):
      self.getRanking(conn)
      #self.getRanking(conn)
      copaycount = 0
      statuscount = 0
      restrictioncount = 0
      f = open("predominantStatusForIsParentN.txt", "w+")
      f1 = open("predominantCopayForIsParentN.txt", "w+")
      f2 = open("predominantRestricitionForIsParentN.txt", "w+")
      for each in self.predominantStatusDic.keys():

          print("Each Entity", each)
          keyValues = str(each).split("|")
          entityId = int(keyValues[0])
          subchannel = str(keyValues[1])
          drugId = int(keyValues[2])
          predominantValue = self.predominantStatusDic.get(each)
          accountFormularyIds = self.EntityFormularyDataFrame.loc[(self.EntityFormularyDataFrame['EntityID'] == entityId) &
                                                      (self.EntityFormularyDataFrame['SubChannel'] == subchannel)
                                                      ]
          listOfIDsset = set(list(pd.Series(accountFormularyIds['FormularyID']).values))
          listOfIDs = list(listOfIDsset)
          print("List Of Formulary ID",listOfIDs.__str__())
          #getDrugFormulary status Data
          drugFormularyBasedOnListofIDs = self.DrugFormularyStatusDataFrame.loc[(self.DrugFormularyStatusDataFrame['EntityID'] == entityId) &
                                                    (self.DrugFormularyStatusDataFrame['FormularyID'].isin(listOfIDs)) &
                                                     (self.DrugFormularyStatusDataFrame['SubChannel'] == subchannel) &
                                                     (self.DrugFormularyStatusDataFrame['DrugID'] == drugId)
                                                     ]

          """EntityFormularyOnListofIDs = self.EntityFormularyDataFrame.loc[(self.DrugFormularyStatusDataFrame['EntityID'] == entityId) &

              (self.EntityFormularyDataFrame['FormularyID'].isin(listOfIDs)) &
              (self.EntityFormularyDataFrame['SubChannel'] == subchannel)
              ]"""
          tempList = []
          #print("after reading status",type(drugFormularyBasedOnListofIDs))
          statusList = []
          rxValuesList = []
          for rowi in drugFormularyBasedOnListofIDs.iterrows():
              #print( rowi[1]['FormularyID'])
              formualryID =  rowi[1]['FormularyID']
              statusi = rowi[1]['DrugStatus']

              totalRxLives = 0
              if not(tempList.__contains__(statusi)):
                  tempFormularyID = 0
                  for rowj in drugFormularyBasedOnListofIDs.iterrows():
                      formualryIDj = rowj[1]['FormularyID']
                      statusj = rowj[1]['DrugStatus']

                      if((statusi == statusj)&(formualryIDj != tempFormularyID)):
                          tempFormularyID = formualryIDj
                          livesDF = accountFormularyIds.loc[accountFormularyIds['FormularyID'] == formualryIDj]
                          totalRxLives = totalRxLives + int(pd.Series(livesDF['FormularyRxLives']).sum())
                          #totalRxLives = totalRxLives + int(pd.Series(livesDF['FormularyRxLives']).drop_duplicates().sum())
                  tempList.append(statusi)
                  statusList.append(statusi)
                  rxValuesList.append(totalRxLives)
          print("status List",statusList)
          print("rx value List",rxValuesList)
          if not (rxValuesList.__len__() == 0):

              index = rxValuesList.index(max(rxValuesList))
              value = statusList[index]

          if(value == predominantValue):
              #count = count + 1
              print("-----Passed first scenario-----")
              drugFormularycopay =pd.DataFrame(drugFormularyBasedOnListofIDs.loc[drugFormularyBasedOnListofIDs['DrugStatus'] == value])
              maxcleanedList = [x for x in pd.Series(drugFormularycopay['MaxCoPay']).tolist() if (math.isnan(x) == False)]
              mincleanedList = [x for x in pd.Series(drugFormularycopay['MinCoPay']).tolist() if (math.isnan(x) == False)]
              maxval = ""
              minval = ""
              #print(drugFormularycopay['FormularyID'].tolist())
              print("mincleaned copayList",maxcleanedList)
              print("mincleaned copay List",maxcleanedList)
              if(maxcleanedList.__len__() == 0):
                  maxval = 'nan'
              else:
                  maxval = str(max(maxcleanedList))
              if(mincleanedList.__len__() == 0):
                  minval = 'nan'
              else:
                  minval =  str(min(mincleanedList))

              copayvalue = maxval + "|" + minval
              print("Evaluated Copay Value",copayvalue)
              #drugFormularycopay =  drugFormularycopay.dropna()

              predominantCopayValue = self.predominantCopayDic.get(each)

              #copayvalue = str(max(pd.Series(drugFormularycopay['MaxCoPay']).tolist()))+"|"+str(min(pd.Series(drugFormularycopay['MinCoPay']).tolist()))

              RestricitionData = self.DrugFormularyRestrictionDataFrame.loc[
                  (self.DrugFormularyRestrictionDataFrame['FormularyID'].isin(drugFormularycopay['FormularyID'].tolist())) &
                  (self.DrugFormularyRestrictionDataFrame['DrugID'] == drugId)]

              if(predominantCopayValue == copayvalue ):
                  print("Copay validation is Passed")
              else:
                  if (subchannel == 'HIX'):
                      print("subchannel is HIX", subchannel)
                      copayDFforHIX = drugFormularycopay.loc[drugFormularycopay['EntityID'] == entityId]
                      maxHixList = [x for x in pd.Series(copayDFforHIX['MaxCoPay']).tolist() if
                                    (math.isnan(x) == False)]
                      minhixList = [x for x in pd.Series(copayDFforHIX['MinCoPay']).tolist() if
                                    (math.isnan(x) == False)]
                      maxval = ""
                      minval = ""
                      # print(drugFormularycopay['FormularyID'].tolist())
                      print("mincleaned copayList", maxHixList)
                      print("mincleaned copay List", minhixList)
                      if (maxHixList.__len__() == 0):
                          maxval = 'nan'
                      else:
                          maxval = str(max(maxHixList))
                      if (minhixList.__len__() == 0):
                          minval = 'nan'
                      else:
                          minval = str(min(minhixList))

                      copayvalueforhix = maxval + "|" + minval
                      print("Evaluated Copay Value", copayvalueforhix)
                      if (copayvalueforhix == predominantCopayValue):
                          print("Passed")
                      else:
                          copaycount = copaycount + 1
                          f1.write("key failed for Copay" + each + "\n")
                          f1.write("accountFormularyId" + str(listOfIDs) + "\n")
                          f1.write("statusandRestricitionList" + str(statusList) + "\n")
                          f1.write("totalRxList" + str(rxValuesList) + "\n")
                          f1.write("Computed Value" + copayvalue + "\n")
                          f1.write(
                              "Computed Value" + pd.Series(
                                  drugFormularycopay['MaxCoPay']).tolist().__str__() + "\n")
                          f1.write("maxcleanedList Value" + maxcleanedList + "\n")
                          f1.write("mincleanedList Value" + mincleanedList + "\n")
                          f1.write(predominantCopayValue + "\n")
                  else:
                      copaycount = copaycount + 1
                      f1.write("key failed for Copay" + each + "\n")
                      f1.write("accountFormularyId" + str(listOfIDs) + "\n")
                      f1.write("statusandRestricitionList" + str(statusList) + "\n")
                      f1.write("totalRxList" + str(rxValuesList) + "\n")
                      f1.write("Computed Value" + copayvalue + "\n")
                      f1.write("maxcleanedList Value" + maxcleanedList + "\n")
                      f1.write("mincleanedList Value" + mincleanedList + "\n")
                      f1.write(
                          "Computed Value" + pd.Series(drugFormularycopay['MaxCoPay']).tolist().__str__() + "\n")
                      f1.write(predominantCopayValue + "\n")
              #check for Restriction
              print("restricition for formulary id", pd.Series(RestricitionData['RestrictionCode']).tolist())
              print("restriction from prdominant status", str(self.predominantRestricitionDic.get(each)).split(","))
              restrictionlist = pd.Series(RestricitionData['RestrictionCode']).tolist()
              preDominantRestritionlist = str(self.predominantRestricitionDic.get(each)).split(",")
              if (restrictionlist.__len__() == 0):
                  restrictionlist.append("None")

              if(set(restrictionlist).__eq__(set(preDominantRestritionlist))):
                  print("Restricition is Passed")
              else:
                  restrictioncount = restrictioncount + 1
                  f2.write("key failed for Restriction" + each + "\n")
                  f2.write("accountFormularyId" + str(listOfIDs) + "\n")
                  f2.write("statusandRestricitionList" + str(statusList) + "\n")
                  f2.write("totalRxList" + str(rxValuesList) + "\n")

                  f2.write("restrictionlist Value" + restrictionlist.__str__() + "\n")
                  f2.write("preDominantRestrition Value" + preDominantRestritionlist.__str__() + "\n")
                  f2.write(predominantCopayValue + "\n")

          else:
              print("Faile 1st Screnario")

              if all([v == 0 for v in rxValuesList]):
                  print("checking for all the Rx values are Zero based on ranking")

                  #print("statusandRestricitionList", statusList)
                  highestRank = 24
                  highestStatus = ""

                  for i in range(statusList.__len__()):
                      Status = statusList[i]
                      print(Status)
                      print(self.rankingDictionary)
                      tempRank = self.rankingDictionary.get(Status)
                      print(tempRank)
                      if(tempRank != None):
                          if (tempRank < highestRank):
                              highestRank = tempRank
                              highestStatus = Status
                  if (highestStatus == predominantValue):
                          #count = count + 1
                          print(" Validation status  against ranking passed")
                          drugFormularycopay = drugFormularyBasedOnListofIDs.loc[
                              drugFormularyBasedOnListofIDs['DrugStatus'] == highestStatus]
                          #drugFormularycopay = drugFormularycopay.dropna()
                          #cleanedList = [x for x in drugFormularycopay if (math.isnan(x) == False)]
                          maxcleanedList = [x for x in pd.Series(drugFormularycopay['MaxCoPay']).tolist() if (math.isnan(x) == False)]
                          mincleanedList = [x for x in pd.Series(drugFormularycopay['MinCoPay']).tolist() if (math.isnan(x) == False)]
                          print("mincleaned copayList", maxcleanedList)
                          print("mincleaned copay List", maxcleanedList)
                          maxval = ""
                          minval = ""
                          if (maxcleanedList.__len__() == 0):
                              maxval = 'nan'
                          else:
                              maxval = str(max(maxcleanedList))
                          if (mincleanedList.__len__() == 0):
                              minval = 'nan'
                          else:
                              minval = str(min(mincleanedList))

                          copayvalue = maxval + "|" + minval
                          #copayvalue = str(max(maxcleanedList)) + "|" + str(min(mincleanedList))
                          predominantCopayValue = self.predominantCopayDic.get(each)

                          RestricitionData = self.DrugFormularyRestrictionDataFrame.loc[
                              (self.DrugFormularyRestrictionDataFrame['FormularyID'].isin(drugFormularycopay['FormularyID'].tolist())) &
                              (self.DrugFormularyRestrictionDataFrame['DrugID'] == drugId)]

                          if (predominantCopayValue == copayvalue):
                              print("Copay Passed")

                          else:
                              if (subchannel == 'HIX'):
                                  print("subchannel is HIX", subchannel)
                                  copayDFforHIX = drugFormularycopay.loc[drugFormularycopay['EntityID'] == entityId]
                                  maxHixList = [x for x in pd.Series(copayDFforHIX['MaxCoPay']).tolist() if
                                                (math.isnan(x) == False)]
                                  minhixList = [x for x in pd.Series(copayDFforHIX['MinCoPay']).tolist() if
                                                (math.isnan(x) == False)]
                                  maxval = ""
                                  minval = ""
                                  # print(drugFormularycopay['FormularyID'].tolist())
                                  print("mincleaned copayList", maxHixList)
                                  print("mincleaned copay List", minhixList)
                                  if (maxHixList.__len__() == 0):
                                      maxval = 'nan'
                                  else:
                                      maxval = str(max(maxHixList))
                                  if (minhixList.__len__() == 0):
                                      minval = 'nan'
                                  else:
                                      minval = str(min(minhixList))

                                  copayvalueforhix = maxval + "|" + minval
                                  print("Evaluated Copay Value", copayvalueforhix)
                                  if (copayvalueforhix == predominantCopayValue):
                                      print("Passed")
                                  else:
                                      copaycount = copaycount + 1
                                      f1.write("key failed for Copay" + each + "\n")
                                      f1.write("accountFormularyId" + str(listOfIDs) + "\n")
                                      f1.write("statusandRestricitionList" + str(statusList) + "\n")
                                      f1.write("totalRxList" + str(rxValuesList) + "\n")
                                      f1.write("Computed Value" + copayvalue + "\n")
                                      f1.write(
                                          "Computed Value" + pd.Series(
                                              drugFormularycopay['MaxCoPay']).tolist().__str__() + "\n")
                                      f1.write("maxcleanedList Value" + maxcleanedList + "\n")
                                      f1.write("mincleanedList Value" + mincleanedList + "\n")
                                      f1.write(predominantCopayValue + "\n")
                              else:
                                  copaycount = copaycount + 1
                                  f1.write("key failed for Copay" + each + "\n")
                                  f1.write("accountFormularyId" + str(listOfIDs) + "\n")
                                  f1.write("statusandRestricitionList" + str(statusList) + "\n")
                                  f1.write("totalRxList" + str(rxValuesList) + "\n")
                                  f1.write("Computed Value" + copayvalue + "\n")
                                  f1.write("maxcleanedList Value" + maxcleanedList + "\n")
                                  f1.write("mincleanedList Value" + mincleanedList + "\n")
                                  f1.write(
                                      "Computed Value" + pd.Series(
                                          drugFormularycopay['MaxCoPay']).tolist().__str__() + "\n")
                                  f1.write(predominantCopayValue + "\n")
                          print("restricition for formulary id",pd.Series(RestricitionData['RestrictionCode']).tolist())
                          print("restriction from prdominant status", str(self.predominantRestricitionDic.get(each)).split(","))
                          restrictionlist = pd.Series(RestricitionData['RestrictionCode']).tolist()
                          preDominantRestritionlist = str(self.predominantRestricitionDic.get(each)).split(",")
                          if (restrictionlist.__len__() == 0):
                              restrictionlist.append("None")

                          if (set(restrictionlist).__eq__(set(preDominantRestritionlist))):
                              print("Restricition is Passed")
                          else:
                              restrictioncount = restrictioncount + 1
                              f2.write("key failed for Restriction" + each + "\n")
                              f2.write("accountFormularyId" + str(listOfIDs) + "\n")
                              f2.write("statusandRestricitionList" + str(statusList) + "\n")
                              f2.write("totalRxList" + str(rxValuesList) + "\n")

                              f2.write("restrictionlist Value" + restrictionlist.__str__() + "\n")
                              f2.write("preDominantRestrition Value" + preDominantRestritionlist.__str__() + "\n")
                              f2.write(predominantCopayValue + "\n")

                  else:
                          statuscount = statuscount +1
                          #print("stList", statusList.__str__())
                          #print("rxList", rxValuesList.__str__())
                          #print("predominantValue", predominantValue)
                          #print("value", value)
                          print("failed 2nd Scenario----------------")
                          f.write("key" + each + "\n")
                          f.write("accountFormularyId" + str(listOfIDs) + "\n")
                          f.write("statusandRestricitionList" + str(statusList) + "\n")
                          f.write("totalRxList" + str(rxValuesList) + "\n")
                          f.write("Computed Value" + value + "\n")
                          f.write(predominantValue + "\n")
              else:
                  m = max(rxValuesList)
                  list1 = [i for i, j in enumerate(rxValuesList) if j == m]
                  print("If all are not Zero Scenario")
                            # print("statusandRestricitionList", statusList)
                  highestRank = 24
                  highestStatus = ""

                  for i in range(list1.__len__()):
                          Status = statusList[i]
                          print(Status)
                          print(self.rankingDictionary)
                          tempRank = self.rankingDictionary.get(Status)
                          print(tempRank)
                          if (tempRank != None):
                              if (tempRank < highestRank):
                                  highestRank = tempRank
                                  highestStatus = Status
                  if (highestStatus == predominantValue):
                      print("passed")
                  else:
                      statuscount = statuscount +1
                      #print("stList", statusList.__str__())
                      #print("rxList", rxValuesList.__str__())
                      #print("predominantValue", predominantValue)
                      #print("value", value)
                      f.write("key" + each + "\n")
                      f.write("accountFormularyId" + str(listOfIDs) + "\n")
                      f.write("statusandRestricitionList" + str(statusList) + "\n")
                      f.write("totalRxList" + str(rxValuesList) + "\n")
                      f.write("Computed Value" + value + "\n")
                      f.write(predominantValue + "\n")


              #maxRxValue = max(rxValuesList)
              #countRxOcurance =  rxValuesList.count(maxRxValue)
              #if(countRxOcurance > 1):
                 # self.getRanking(conn)

              #check For Duplicate Rx Lives

          #totalRxLives = totalRxLives+ rowi[1]['DrugStatus']
      try:
          tempconn = DatabaseConnection.Connection.getConnection(mainExcel.configFileName)

          if(copaycount == 0):
              self.passed = self.passed + 1
              print("All copay are verified no issues found")
              mainExcel.Module = "PredominantFormularyData"
              mainExcel.TestCaseName = "Validate the Copay of each Corporate Entity"
              mainExcel.ExpectedResult = "Copay should match with DrugFormularyCopay"
              mainExcel.TestFailDescription = "None"
              mainExcel.TestFailSeverity = "None"
              mainExcel.TestCaseStatus = "PASSED"
              DatabaseConnection.Connection.saveResultToDataBase(tempconn, mainExcel)
          else:
              self.failed = self.failed + 1
              print("All copay are verified issues are specified in given text file")
              mainExcel.Module = "PredominantFormularyData"
              mainExcel.TestCaseName = "Validate the Copay of each Corporate Entity"
              mainExcel.ExpectedResult = "Copay should match with DrugFormularyCopay"
              mainExcel.TestFailDescription = "There are some copay is mismatched for entities,Detail Mentioned in predominantCopayForN.txt"
              mainExcel.TestFailSeverity = "Informational"
              mainExcel.TestCaseStatus = "FAILED"
              DatabaseConnection.Connection.saveResultToDataBase(tempconn, mainExcel)

          if(statuscount == 0):
              print("All copay are verified no issues found")
              mainExcel.Module = "PredominantFormularyData"
              mainExcel.TestCaseName = "Validate the Status of each Other Entity"
              mainExcel.ExpectedResult ="Status should match with DrugFormularyStatus"
              mainExcel.TestFailDescription = "None"
              mainExcel.TestFailSeverity = "None"
              mainExcel.TestCaseStatus = "PASSED"
              DatabaseConnection.Connection.saveResultToDataBase(tempconn, mainExcel)
          else:
              self.failed = self.failed + 1
              print("All copay are verified no issues found")
              mainExcel.Module = "PredominantFormularyData"
              mainExcel.TestCaseName = "Validate the Status of each Corporate Entity"
              mainExcel.ExpectedResult ="Status should match with DrugFormularyStatus"
              mainExcel.TestFailDescription = "There are some copay is mismatched for entities,Detail Mentioned in predominantStatusForN.txt"
              mainExcel.TestFailSeverity = "Informational"
              mainExcel.TestCaseStatus = "FAILED"
              DatabaseConnection.Connection.saveResultToDataBase(tempconn, mainExcel)

          if (restrictioncount == 0):
              self.passed = self.passed + 1
              mainExcel.Module = "PredominantFormularyData"
              mainExcel.TestCaseName ="Validate the Restriction of each Corporate Entity"
              mainExcel.ExpectedResult ="Restriction should match with DrugFormularyRestriction"
              mainExcel.TestFailDescription = "None"
              mainExcel.TestFailSeverity = "None"
              mainExcel.TestCaseStatus = "PASSED"
              DatabaseConnection.Connection.saveResultToDataBase(tempconn, mainExcel)
          else:
              self.failed = self.failed + 1
              mainExcel.Module = "PredominantFormularyData"
              mainExcel.TestCaseName ="Validate the Restriction of each Corporate Entity"
              mainExcel.ExpectedResult ="Restriction should match with DrugFormularyRestriction"
              mainExcel.TestFailDescription = "There are some restriction is mismatched for entities,Detail Mentioned in predominantrestrictionForN.txt"
              mainExcel.TestFailSeverity = "Informational"
              mainExcel.TestCaseStatus = "FAILED"
              DatabaseConnection.Connection.saveResultToDataBase(tempconn, mainExcel)
          tempconn.close()
      except Exception as e:
          print("Exception accoured")
          tempconn.close()

  def getRanking(self,conn):
      print("get Ranking Table")
      #cnxn = pyodbc.connect(
          #'DRIVER={SQL Server Native Client 10.0};SERVER=10.0.0.15;PORT=1433;DATABASE=MasterPb;UID=m1bqc;PWD=m1b0813')
      cursor = conn.cursor()
      SQLCommand = ("""select * from stg.PredominantStatusRanking where FormularyType = 'Granular'""")
      cursor.execute(SQLCommand)
      counter = 0
      presentList = []
      for row in cursor:
          counter = counter + 1
          #print("row = %r" % (row[1]))
          self.rankingDictionary.update({row[3]: row[2]})

      #cnxn.close()
