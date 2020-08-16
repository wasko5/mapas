# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import pandas as pd
import global_vars
import decision_funcs
import os

def raw_pairttest_tests_unevenGroups_cohensd():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "Cohen's d"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups_cohensd.xlsx"))
	# degrees of freedom is float in the actual_df as it's looking up from the researchpy output dataframe which defaults to float behaviour
	expected_df["Degrees of Freedom"] = expected_df["Degrees of Freedom"].astype("float")

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_pairttest_tests_unevenGroups_hedgesg():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "Hedge's g"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups_hedgesg.xlsx"))
	# degrees of freedom is float in the actual_df as it's looking up from the researchpy output dataframe which defaults to float behaviour
	expected_df["Degrees of Freedom"] = expected_df["Degrees of Freedom"].astype("float")

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_pairttest_tests_unevenGroups_glassdelta():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "Glass's delta"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups_glassdelta.xlsx"))
	# degrees of freedom is float in the actual_df as it's looking up from the researchpy output dataframe which defaults to float behaviour
	expected_df["Degrees of Freedom"] = expected_df["Degrees of Freedom"].astype("float")

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_pairttest_tests_unevenGroups_noEffectSize():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "None"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups_noEffectSize.xlsx"))
	# degrees of freedom is float in the actual_df as it's looking up from the researchpy output dataframe which defaults to float behaviour
	expected_df["Degrees of Freedom"] = expected_df["Degrees of Freedom"].astype("float")

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_pairttest_tests_evenGroups():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "None"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_evenGroups.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_evenGroups.xlsx"))
	# degrees of freedom is float in the actual_df as it's looking up from the researchpy output dataframe which defaults to float behaviour
	expected_df["Degrees of Freedom"] = expected_df["Degrees of Freedom"].astype("float")

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_pairttest_tests_unequalVariance():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "Cohen's d"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unequalVariance.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unequalVariance.xlsx"))
	# degrees of freedom is float in the actual_df as it's looking up from the researchpy output dataframe which defaults to float behaviour
	expected_df["Degrees of Freedom"] = expected_df["Degrees of Freedom"].astype("float")

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def raw_pairttest_tests_unevenGroups_withMissingData():
	# global vars
	global_vars.input_type = "raw"
	global_vars.raw_test = "pairttest"
	global_vars.raw_pairttest_var_pairs = [['Bar1', 'Bar2'], ['Foo1', 'Foo2']]
	global_vars.effect_size_choice = "None"

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups_withMissingData.xlsx"))
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)

	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "raw_pairttest_tests_unevenGroups_withMissingData.xlsx"))
	# degrees of freedom is float in the actual_df as it's looking up from the researchpy output dataframe which defaults to float behaviour
	expected_df["Degrees of Freedom"] = expected_df["Degrees of Freedom"].astype("float")

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def main():
	raw_pairttest_tests_unevenGroups_cohensd()
	raw_pairttest_tests_unevenGroups_hedgesg()
	raw_pairttest_tests_unevenGroups_glassdelta()
	raw_pairttest_tests_unevenGroups_noEffectSize()
	raw_pairttest_tests_evenGroups()
	raw_pairttest_tests_unequalVariance() # maybe not a useful test as you can't have unequal variances in paired ttest and equality is always set to True in the func
	raw_pairttest_tests_unevenGroups_withMissingData()
	print("Raw pairttest tests passed!")