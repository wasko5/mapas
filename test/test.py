import pandas as pd
import numpy as np
import os
from pandas import ExcelWriter
from pandas import ExcelFile


def testStringValue(a, b):
    return a == b

def testNumericValue(a, b, delta):
    return abs(a - b) <= delta

def testDF(df, df_two, delta):
    for i in range(0, len(df.index)):
        for j in range(0, len(df.columns)):
            currentValue = df.values[i,j]
            outputValue = df_two.values[i,j]

            if(pd.isna(currentValue) and pd.isna(outputValue)) : continue
            
            elif not (pd.isna(currentValue)) and pd.isna(outputValue):
                    print("TEST FAILED HERE")
                    print(currentValue)
                    print(outputValue)
                    return False

            elif (pd.isna(currentValue)) and not pd.isna(outputValue):
                    print("TEST FAILED HERE")
                    print(currentValue)
                    print(outputValue)
                    return False

            elif(isinstance(currentValue, str)):
                if not (testStringValue(currentValue, outputValue)):
                    print("TEST FAILED HERE")
                    print(currentValue)
                    print(outputValue)
                    return False

            elif(isinstance(currentValue, (int, float, complex))):
                if not (testNumericValue(currentValue, outputValue, delta)):
                        print("TEST FAILED HERE")
                        print(currentValue)
                        print(outputValue)
                        return False


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'test.xlsx')
my_file_two = os.path.join(THIS_FOLDER, 'test_output.xlsx')

df = pd.read_excel(my_file, sheet_name='Sheet')
#call function to generate dataframe from df
df_two = pd.read_excel(my_file_two, sheet_name='Sheet')


if(testDF(df, df_two, 0.01) == False):
    print("TEST DID NOT PASS")
else:
    print("TEST PASSED")
