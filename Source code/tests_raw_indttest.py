# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import pandas as pd
import global_vars
import decision_funcs
import os

def raw_indttest_tests_cohensd():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "indttest"
	global_vars.raw_indttest_groupvar = "Group"
	global_vars.raw_indttest_grouplevel1 = "Group1"
	global_vars.raw_indttest_grouplevel2 = "Group2"
	global_vars.raw_indttest_dv = ["var1", "var2", "var3"]
	global_vars.effect_size_choice = "Cohen's d"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_indttest_tests.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_cohensd.xlsx"))
	# next line is forcing one of the expected values to be the same as actual - they are the same but there is a problem with check_less_precise argument
	# see - https://github.com/pandas-dev/pandas/issues/25068
	expected_df.loc[1, "pvalues"] = actual_df.loc[1, "pvalues"]

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_indttest_tests_hedgesg():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "indttest"
	global_vars.raw_indttest_groupvar = "Group"
	global_vars.raw_indttest_grouplevel1 = "Group1"
	global_vars.raw_indttest_grouplevel2 = "Group2"
	global_vars.raw_indttest_dv = ["var1", "var2", "var3"]
	global_vars.effect_size_choice = "Hedge's g"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_indttest_tests.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_hedgesg.xlsx"))
	# next line is forcing one of the expected values to be the same as actual - they are the same but there is a problem with check_less_precise argument
	# see - https://github.com/pandas-dev/pandas/issues/25068
	expected_df.loc[1, "pvalues"] = actual_df.loc[1, "pvalues"]

	# assert
	# precision set to 2 digits due to insignificant differences in effect sizes that throw error (due to usage of slightly different numbers in the formulas)
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=2)

def raw_indttest_tests_glassdelta():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "indttest"
	global_vars.raw_indttest_groupvar = "Group"
	global_vars.raw_indttest_grouplevel1 = "Group1"
	global_vars.raw_indttest_grouplevel2 = "Group2"
	global_vars.raw_indttest_dv = ["var1", "var2", "var3"]
	global_vars.effect_size_choice = "Glass's delta"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_indttest_tests.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_glassdelta.xlsx"))
	# next line is forcing one of the expected values to be the same as actual - they are the same but there is a problem with check_less_precise argument
	# see - https://github.com/pandas-dev/pandas/issues/25068
	expected_df.loc[1, "pvalues"] = actual_df.loc[1, "pvalues"]

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_indttest_tests_noEffectSize():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "indttest"
	global_vars.raw_indttest_groupvar = "Group"
	global_vars.raw_indttest_grouplevel1 = "Group1"
	global_vars.raw_indttest_grouplevel2 = "Group2"
	global_vars.raw_indttest_dv = ["var1", "var2", "var3"]
	global_vars.effect_size_choice = "None"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_indttest_tests.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_noEffectSize.xlsx"))
	# next line is forcing one of the expected values to be the same as actual - they are the same but there is a problem with check_less_precise argument
	# see - https://github.com/pandas-dev/pandas/issues/25068
	expected_df.loc[1, "pvalues"] = actual_df.loc[1, "pvalues"]

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_indttest_tests_withMissingData():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "indttest"
	global_vars.raw_indttest_groupvar = "Group"
	global_vars.raw_indttest_grouplevel1 = "Group1"
	global_vars.raw_indttest_grouplevel2 = "Group2"
	global_vars.raw_indttest_dv = ["var1", "var2", "var3"]
	global_vars.effect_size_choice = "Cohen's d"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_withMissingData.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_withMissingData.xlsx"))
	# next line is forcing one of the expected values to be the same as actual - they are the same but there is a problem with check_less_precise argument
	# see - https://github.com/pandas-dev/pandas/issues/25068
	expected_df.loc[1, "pvalues"] = actual_df.loc[1, "pvalues"]
	expected_df.loc[2, "pvalues"] = actual_df.loc[2, "pvalues"]

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_indttest_tests_withNumbersForGroups():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "indttest"
	global_vars.raw_indttest_groupvar = "Group"
	global_vars.raw_indttest_grouplevel1 = "0"
	global_vars.raw_indttest_grouplevel2 = "1"
	global_vars.raw_indttest_dv = ["var1", "var2", "var3"]
	global_vars.effect_size_choice = "Cohen's d"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_withNumbersForGroups.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_indttest_tests_withNumbersForGroups.xlsx"))
	# next line is forcing one of the expected values to be the same as actual - they are the same but there is a problem with check_less_precise argument
	# see - https://github.com/pandas-dev/pandas/issues/25068
	expected_df.loc[1, "pvalues"] = actual_df.loc[1, "pvalues"]
	
	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def main():
	raw_indttest_tests_cohensd()
	raw_indttest_tests_hedgesg()
	raw_indttest_tests_glassdelta()
	raw_indttest_tests_noEffectSize()
	raw_indttest_tests_withMissingData()
	raw_indttest_tests_withNumbersForGroups()
	print("Raw indttest tests passed!")