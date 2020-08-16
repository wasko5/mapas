# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import pandas as pd
import global_vars
import decision_funcs
import os

def raw_correlations_tests_pearson():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "corr"
	global_vars.raw_corr_type = "pearson"
	global_vars.raw_corr_vars = ["var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8"]

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_correlations_tests.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_pearson.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_correlations_tests_spearman():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "corr"
	global_vars.raw_corr_type = "spearman"
	global_vars.raw_corr_vars = ["var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8"]

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_correlations_tests.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_spearman.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)


def raw_correlations_tests_kendall():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "corr"
	global_vars.raw_corr_type = "kendall"
	global_vars.raw_corr_vars = ["var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8"]

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_correlations_tests.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_kendall.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)


def raw_correlations_tests_pearson_withMissingData():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "corr"
	global_vars.raw_corr_type = "pearson"
	global_vars.raw_corr_vars = ["var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8"]

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_withMissingData.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_pearson_withMissingData.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_correlations_tests_spearman_withMissingData():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "corr"
	global_vars.raw_corr_type = "spearman"
	global_vars.raw_corr_vars = ["var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8"]

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_withMissingData.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_spearman_withMissingData.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)


def raw_correlations_tests_kendall_withMissingData():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "corr"
	global_vars.raw_corr_type = "kendall"
	global_vars.raw_corr_vars = ["var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8"]

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_withMissingData.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_correlations_tests_kendall_withMissingData.xlsx"))

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def main():
	raw_correlations_tests_pearson()
	raw_correlations_tests_spearman()
	raw_correlations_tests_kendall()
	raw_correlations_tests_pearson_withMissingData()
	raw_correlations_tests_spearman_withMissingData()
	raw_correlations_tests_kendall_withMissingData()
	print("Raw correlations tests passed!")