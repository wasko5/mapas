# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import pandas as pd
import global_vars
import decision_funcs
import os

def spss_mr_tests_minimalStats():
	# global vars
	global_vars.input_type = "spss"
	global_vars.spss_test = "mr"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "spss_mr_tests_minimalStats.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	# forcing dtype to object as data formatting is done within the output_df func
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "spss_mr_tests_minimalStats.xlsx"), dtype = object)
	# forcing the interpreted nan value to be empty as in the actual_df
	expected_df.iloc[0, 3] = actual_df.iloc[0, 3]
	#  forcing pvalues as float as this was a later change; pvlaues are later updated in the multitest correction function and formatted in the tables functions
	expected_df["pvalues"] = expected_df["pvalues"].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def spss_mr_tests_allStats():
	# global vars
	global_vars.input_type = "spss"
	global_vars.spss_test = "mr"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "spss_mr_tests_allStats.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	# forcing dtype to object as data formatting is done within the output_df func
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "spss_mr_tests_allStats.xlsx"), dtype = object)
	# forcing the interpreted nan value to be empty as in the actual_df
	expected_df.iloc[0, 3] = actual_df.iloc[0, 3]
	#  forcing pvalues as float as this was a later change; pvlaues are later updated in the multitest correction function and formatted in the tables functions
	expected_df["pvalues"] = expected_df["pvalues"].astype(float)
	
	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def main():
	spss_mr_tests_minimalStats()
	spss_mr_tests_allStats()
	print("SPSS MR tests passed!")