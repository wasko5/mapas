import pandas as pd
import numpy as np
import os
from pandas import ExcelWriter
from pandas import ExcelFile


def testStringValue(a, b):
	return a == b

def testNumericValue(a, b, delta):
	return abs(a - b) <= delta

def testDF(df, df_two, delta=0.1):
	for i in range(0, len(df.index)):
		for j in range(0, len(df.columns)):
			currentValue = df.values[i,j]
			outputValue = df_two.values[i,j]
			print('asd', currentValue, outputValue, type(currentValue))

			if(pd.isna(currentValue) and pd.isna(outputValue)) : continue
			
			elif not (pd.isna(currentValue)) and pd.isna(outputValue):
					print("TEST FAILED HERE1")
					print(currentValue)
					print(outputValue)
					return False

			elif (pd.isna(currentValue)) and not pd.isna(outputValue):
					print("TEST FAILED HERE2")
					print(currentValue)
					print(outputValue)
					return False

			elif(isinstance(currentValue, str)):
				if not (testStringValue(currentValue, outputValue)):
					print("TEST FAILED HERE3")
					print(currentValue)
					print(outputValue)
					return False

			elif(isinstance(currentValue, (int, float, complex))):
				print('asd', currentValue, outputValue)
				if not (testNumericValue(currentValue, outputValue, delta)):
						print("TEST FAILED HERE4")
						print(currentValue)
						print(outputValue)
						return False
