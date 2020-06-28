import pandas as pd
import global_vars
#import calculations_helper_functions_only as helper_funcs
import decision_funcs
import os

INPUT_DATAFRAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit_testing\\input dataframes\\")
OUTPUT_DATAFRAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit_testing\\output dataframes\\")

def spss_pairttests_tests():
	#global vars
	global_vars.input_type = "spss"
	global_vars.spss_test = "pairttest"
	global_vars.spss_pairttest_n = 190
	global_vars.effect_size_choice = "Cohen's d"
	

	#setup - actual
	input_df = pd.read_excel(INPUT_DATAFRAMES_FOLDER + "spss_pairttest_tests.xlsx")
	mod_input_df = decision_funcs.modify_raw_data_df(input_df)
	actual_df = decision_funcs.generate_output_df(mod_input_df)
	
	#setup - expected
	#given the few empty columns (reserved for means and sds), the keep_default_na forces the nan values to be interpreted as empty strings, rather than np.nan
	expected_df_r = pd.read_excel(OUTPUT_DATAFRAMES_FOLDER + "spss_pairttest_tests.xlsx", keep_default_na=False)

	#assert
	pd.testing.assert_frame_equal(actual_df, expected_df_r, check_less_precise=3)

def main():
	spss_pairttests_tests()
	print("SPSS pairttest tests passed!")

main()