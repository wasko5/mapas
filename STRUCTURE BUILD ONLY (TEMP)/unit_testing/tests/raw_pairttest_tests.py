import pandas as pd
import global_vars
#import calculations_helper_functions_only as helper_funcs
import decision_funcs
import os

INPUT_DATAFRAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit_testing\\input dataframes\\")
OUTPUT_DATAFRAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit_testing\\output dataframes\\")

def raw_pairttest_tests_unevenGroups_cohensd():
	#global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "Cohen's d"

	#setup - actual
	input_df = pd.read_excel(INPUT_DATAFRAMES_FOLDER + "raw_pairttest_tests_unevenGroups_withMissingData.xlsx")
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	#setup - expected
	expected_df_r = pd.read_excel(OUTPUT_DATAFRAMES_FOLDER + "raw_indttest_tests_cohensd.xlsx")

	#assert
	pd.testing.assert_frame_equal(actual_df, expected_df_r, check_less_precise=3)

def main():
	raw_pairttest_tests_unevenGroups_cohensd()
	print("Raw pairttest tests passed!")