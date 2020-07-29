import pandas as pd
import global_vars
import decision_funcs
import os

#Initial software setup was based on .xlsx files provided as inputs. These tests ensure that the input files are interpreted in the same way by pandas
#all excel files are same as for input dataframees tests

def main():
	for file in set([x.split(".")[0] for x in os.listdir(global_vars.CSV_INPUT_DATAFRAMES_FOLDER)]): #taking advantage of repeating names
		#set - actual (excel)
		actual_df = pd.read_excel(os.path.join(global_vars.CSV_INPUT_DATAFRAMES_FOLDER, file + ".xlsx"))
		
		#setup - expected (csv)
		expected_df = pd.read_csv(os.path.join(global_vars.CSV_INPUT_DATAFRAMES_FOLDER, file + ".csv"))

		#assert
		pd.testing.assert_frame_equal(actual_df, expected_df)
	print("CSV tests passed!")