import os
import sys
import subprocess

ClientName = sys.argv[1]
ConfigFileName = sys.argv[2]
print("ClientName",ClientName)
print("ConfigFileName",ConfigFileName)
#os.startfile('MainTest.exe' ,'D:\RunPayerBackBone\Config.txt')
if (ClientName == 'TOB'):
    os.system(r'MainTest.exe ' + ConfigFileName)
if (ClientName == 'ACE'):
    os.system(r'MainTest.exe ' + ConfigFileName)

