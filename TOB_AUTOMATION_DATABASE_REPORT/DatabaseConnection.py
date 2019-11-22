import pyodbc
import configparser
import os
import pandas as pd
class Connection:
  cnxn =""
  testString = ""

  @staticmethod
  def getConnection(configFileName):
      os.getcwd()
      config = configparser.ConfigParser()
      config.read(configFileName)
      dataBaseName = config.get('DataBaseSection', 'DATABASEName')
      userName = config.get('DataBaseSection', 'UserID')
      password = config.get('DataBaseSection', 'password')
      servername=  config.get('DataBaseSection', 'servername')
      conn = pyodbc.connect(
          'DRIVER={SQL Server Native Client 11.0};SERVER='+servername+';DATABASE='+dataBaseName+';UID='+userName+';PWD='+password+'')

      return conn

  @staticmethod
  def ConfigProperties(configName):
      configDictionary ={}
      channelRollupDictionary = {}
      os.getcwd()
      config = configparser.ConfigParser()
      config.read(configName)
      list1 = config.options("MODULES TOAUTOMATE")
      for each in range(list1.__len__()):
          configDictionary.update({list1[each]:config.get("MODULES TOAUTOMATE",list1[each])})

      configDictionary.update({"FileName":config.get("FileSection","ExcelPathName")})
      configDictionary.update({"ChartName": config.get("FileSection", "ChartName")})
      configDictionary.update({"PdfName": config.get("FileSection", "PdfName")})
      print(configDictionary)
      ChannelString =  config.get('DATA SECTION', 'Channels')
      DrugString= config.get('DATA SECTION', 'DRUGS')
      productString = config.get('DATA SECTION', 'producttype')
      channelList = str(ChannelString).split(",")
      drugList =  str(DrugString).split(",")
      productList = str(productString).split(",")
      configDictionary.update({"channelList":channelList})
      configDictionary.update({"DrugList": drugList})
      configDictionary.update({"productList": productList})

      # acountExpected SubChannels channelRollupMapping
      accountrollupExpectedSubChannelsList = str(config.get('DATA SECTION', 'AccountRollupExpectedSubChannel')).split(
          ",")
      configDictionary.update({"accountrollupExpectedSubChannelsList": accountrollupExpectedSubChannelsList})

      channelRollupMappingList = str(config.get('DATA SECTION', 'channelRollupMapping')).split(",")
      print(channelRollupMappingList)
      for each in range(channelRollupMappingList.__len__()):
          channelrollup = str(channelRollupMappingList[each]).split(":")
          print(channelrollup[0], channelrollup[1])
          channelRollupDictionary.update({channelrollup[0]: channelrollup[1]})

      configDictionary.update({"channelRollupDictionary": channelRollupDictionary})

      DrugFormularyStatusList = str(config.get('DATA SECTION', 'DrugFormularyStatus')).split(
          ",")
      configDictionary.update({"DrugFormularyStatusList": DrugFormularyStatusList})

      EntityFormularyList = str(config.get('DATA SECTION', 'EntityFormulary')).split(
          ",")
      configDictionary.update({"EntityFormularyList": EntityFormularyList})

      EntityProductList = str(config.get('DATA SECTION', 'EntityProduct')).split(
          ",")
      configDictionary.update({"EntityProductList": EntityProductList})  # EntityProduct

      EntityProductFormularyList = str(config.get('DATA SECTION', 'EntityProductFormulary')).split(
          ",")
      configDictionary.update({"EntityProductFormularyList": EntityProductFormularyList})  #

      EntitySubChannelList = str(config.get('DATA SECTION', 'EntitySubChannel')).split(
          ",")
      configDictionary.update({"EntitySubChannelList": EntitySubChannelList})  #

      IMSBridgeList = str(config.get('DATA SECTION', 'IMSBridge')).split(
          ",")
      configDictionary.update({"IMSBridgeList": IMSBridgeList})  #

      PBMServicesList = str(config.get('DATA SECTION', 'PBMServices')).split(
          ",")
      configDictionary.update({"PBMServicesList": PBMServicesList})  #


      return configDictionary

  @staticmethod
  def saveResultToDataBase(conn, mainExcel):
      print("Saving result to Database")

      cursor = conn.cursor()
      cursor.execute(
          'EXEC dbo.uspQCProcessLogDtl @QLID = ? ,@Module = ?,@TestCaseName = ?,@ExpectedResult = ?,@TestFailDescription = ?,@TestFailSeverity = ?,@TestCaseStatus = ?',
          mainExcel.QLID, mainExcel.Module, mainExcel.TestCaseName, mainExcel.ExpectedResult,
          mainExcel.TestFailDescription, mainExcel.TestFailSeverity, mainExcel.TestCaseStatus)

      conn.commit()


