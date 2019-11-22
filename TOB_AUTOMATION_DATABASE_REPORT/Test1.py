import pandas as pd


class Test1 :
    passed = 0
    failed = 0
    def __call__(self):
        print("somthing")
    def executeScripts(self, conn, mainExcel, wb):
        print("In Test1", conn)