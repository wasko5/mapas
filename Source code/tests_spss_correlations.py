# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import pandas as pd
import global_vars
import decision_funcs
import os

def spss_correlations_tests_pearson():
	# global vars
	global_vars.input_type = "spss"
	global_vars.spss_test = "corr"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "spss_correlations_tests_pearson.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "spss_correlations_tests_pearson.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def spss_correlations_tests_spearman():
	# global vars
	global_vars.input_type = "spss"
	global_vars.spss_test = "corr"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "spss_correlations_tests_spearman.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "spss_correlations_tests_spearman.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def spss_correlations_tests_kendal():
	# global vars
	global_vars.input_type = "spss"
	global_vars.spss_test = "corr"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "spss_correlations_tests_kendal.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "spss_correlations_tests_kendal.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)


def main():
	spss_correlations_tests_pearson()
	spss_correlations_tests_spearman()
	spss_correlations_tests_kendal()
	print("SPSS correlations tests passed!")