import pandas as pd
import global_vars
import decision_funcs
import os

INPUT_DATAFRAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit_testing\\input dataframes\\")
OUTPUT_DATAFRAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit_testing\\output dataframes\\")

def summ_indttest_tests_cohensd():
	#global vars
	global_vars.input_type = "summ_indttest"
	global_vars.summ_indttest_var = "Variable"
	global_vars.summ_indttest_meanOne = "Mean1"
	global_vars.summ_indttest_sdOne = "SD1"
	global_vars.summ_indttest_nOne = "N1"
	global_vars.summ_indttest_meanTwo = "Mean2"
	global_vars.summ_indttest_sdTwo = "SD2"
	global_vars.summ_indttest_nTwo = "N2"
	global_vars.summ_indttest_equal_var = "Equal Variances"
	global_vars.effect_size_choice = "Cohen's d"

	#setup - actual
	input_df = pd.read_excel(INPUT_DATAFRAMES_FOLDER + "summ_indttest_tests.xlsx")
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	#setup - expected
	expected_df_r = pd.read_excel(OUTPUT_DATAFRAMES_FOLDER + "summ_indttest_tests_cohensd.xlsx")

	#assert
	pd.testing.assert_frame_equal(actual_df, expected_df_r, check_less_precise=3)

def summ_indttest_tests_hedgesg():
	#global vars
	global_vars.input_type = "summ_indttest"
	global_vars.summ_indttest_var = "Variable"
	global_vars.summ_indttest_meanOne = "Mean1"
	global_vars.summ_indttest_sdOne = "SD1"
	global_vars.summ_indttest_nOne = "N1"
	global_vars.summ_indttest_meanTwo = "Mean2"
	global_vars.summ_indttest_sdTwo = "SD2"
	global_vars.summ_indttest_nTwo = "N2"
	global_vars.summ_indttest_equal_var = "Equal Variances"
	global_vars.effect_size_choice = "Hedge's g"

	#setup - actual
	input_df = pd.read_excel(INPUT_DATAFRAMES_FOLDER + "summ_indttest_tests.xlsx")
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	#setup - expected
	expected_df_r = pd.read_excel(OUTPUT_DATAFRAMES_FOLDER + "summ_indttest_tests_hedgesg.xlsx")

	#assert
	pd.testing.assert_frame_equal(actual_df, expected_df_r, check_less_precise=3)

def summ_indttest_tests_noEqualVarCol_cohensd():
	#global vars
	global_vars.input_type = "summ_indttest"
	global_vars.summ_indttest_var = "Variable"
	global_vars.summ_indttest_meanOne = "Mean1"
	global_vars.summ_indttest_sdOne = "SD1"
	global_vars.summ_indttest_nOne = "N1"
	global_vars.summ_indttest_meanTwo = "Mean2"
	global_vars.summ_indttest_sdTwo = "SD2"
	global_vars.summ_indttest_nTwo = "N2"
	global_vars.summ_indttest_equal_var = ""
	global_vars.effect_size_choice = "Cohen's d"

	#setup - actual
	input_df = pd.read_excel(INPUT_DATAFRAMES_FOLDER + "summ_indttest_tests_noEqualVarCol.xlsx")
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	#setup - expected
	expected_df_r = pd.read_excel(OUTPUT_DATAFRAMES_FOLDER + "summ_indttest_tests_noEqualVarCol_cohensd.xlsx")

	#assert
	pd.testing.assert_frame_equal(actual_df, expected_df_r, check_less_precise=3)

def summ_indttest_tests_noEqualVarCol_hedgesg():
	#global vars
	global_vars.input_type = "summ_indttest"
	global_vars.summ_indttest_var = "Variable"
	global_vars.summ_indttest_meanOne = "Mean1"
	global_vars.summ_indttest_sdOne = "SD1"
	global_vars.summ_indttest_nOne = "N1"
	global_vars.summ_indttest_meanTwo = "Mean2"
	global_vars.summ_indttest_sdTwo = "SD2"
	global_vars.summ_indttest_nTwo = "N2"
	global_vars.summ_indttest_equal_var = ""
	global_vars.effect_size_choice = "Hedge's g"

	#setup - actual
	input_df = pd.read_excel(INPUT_DATAFRAMES_FOLDER + "summ_indttest_tests_noEqualVarCol.xlsx")
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	#setup - expected
	expected_df_r = pd.read_excel(OUTPUT_DATAFRAMES_FOLDER + "summ_indttest_tests_noEqualVarCol_hedgesg.xlsx")

	#assert
	pd.testing.assert_frame_equal(actual_df, expected_df_r, check_less_precise=3)

def main():
	summ_indttest_tests_cohensd()
	summ_indttest_tests_hedgesg()
	summ_indttest_tests_noEqualVarCol_cohensd()
	summ_indttest_tests_noEqualVarCol_hedgesg()
	print("Summary indttest tests passed!")