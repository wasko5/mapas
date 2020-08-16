# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import pandas as pd
import global_vars
import decision_funcs
import os

def correction_tests_fdrbh():
	# global vars
	global_vars.correction_type = "fdr_bh"
	global_vars.alpha_threshold = 0.05

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "corrections_tests.xlsx"))
	actual_df = decision_funcs.multitest_correction(input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "corrections_tests_fdrbh.xlsx"))
	expected_df[expected_df.columns] = expected_df[expected_df.columns].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def correction_tests_fdrby():
	# global vars
	global_vars.correction_type = "fdr_by"
	global_vars.alpha_threshold = 0.05

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "corrections_tests.xlsx"))
	actual_df = decision_funcs.multitest_correction(input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "corrections_tests_fdrby.xlsx"))
	expected_df[expected_df.columns] = expected_df[expected_df.columns].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def correction_tests_holm():
	# global vars
	global_vars.correction_type = "holm"
	global_vars.alpha_threshold = 0.05

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "corrections_tests.xlsx"))
	actual_df = decision_funcs.multitest_correction(input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "corrections_tests_holm.xlsx"))
	expected_df[expected_df.columns] = expected_df[expected_df.columns].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def correction_tests_bonferroni():
	# global vars
	global_vars.correction_type = "bonferroni"
	global_vars.alpha_threshold = 0.05

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "corrections_tests.xlsx"))
	actual_df = decision_funcs.multitest_correction(input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "corrections_tests_bonferroni.xlsx"))
	expected_df[expected_df.columns] = expected_df[expected_df.columns].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def correction_tests_hochberg():
	# global vars
	global_vars.correction_type = "simes-hochberg"
	global_vars.alpha_threshold = 0.05

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "corrections_tests.xlsx"))
	actual_df = decision_funcs.multitest_correction(input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "corrections_tests_hochberg.xlsx"))
	expected_df[expected_df.columns] = expected_df[expected_df.columns].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def correction_tests_hommel():
	# global vars
	global_vars.correction_type = "hommel"
	global_vars.alpha_threshold = 0.05

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "corrections_tests.xlsx"))
	actual_df = decision_funcs.multitest_correction(input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "corrections_tests_hommel.xlsx"))
	expected_df[expected_df.columns] = expected_df[expected_df.columns].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def correction_tests_none():
	# global vars
	global_vars.correction_type = "None"
	global_vars.alpha_threshold = 0.05

	# setup - actual
	input_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER, "corrections_tests.xlsx"))
	actual_df = decision_funcs.multitest_correction(input_df)
	
	# setup - expected
	expected_df = pd.read_excel(os.path.join(global_vars.TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER, "corrections_tests_none.xlsx"))
	expected_df[expected_df.columns] = expected_df[expected_df.columns].astype(float)

	# assert
	pd.testing.assert_frame_equal(actual_df, expected_df, check_less_precise=3)

def main():
	correction_tests_fdrbh()
	correction_tests_fdrby()
	correction_tests_holm()
	correction_tests_bonferroni()
	correction_tests_hochberg()
	correction_tests_hommel()
	correction_tests_none()
	print("Corrections tests passed!")