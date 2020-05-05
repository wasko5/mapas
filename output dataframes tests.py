
import raw_correlations
'''
import raw_mr
import raw_indttest
import raw_pairttest
import summ_correlations
import summ_indttest
import spss_correlations
import spss_mr
import spss_indttest
import spss_pairttest
import pvalues
'''

import pandas as pd
#import tests_definition as test
import global_vars
import calculations_helper_functions_only as helper_funcs

def test_1():
	#global vars
	global_vars.input_path_and_filename = "D:/Desktop_current/NPSoftware/GitHub/df5.xlsx"
	global_vars.alpha_threshold = 0.05
	global_vars.output_filename = "D:/Desktop_current/NPSoftware/GitHub/df5_output_mapas"
	global_vars.input_type =  "raw"
	global_vars.raw_test =  "corr"
	global_vars.raw_corr_type =  "pearson"
	global_vars.raw_corr_vars = ["a", "b", "c", "d"]
	#global_vars.raw_mr_outcomevar =  
	global_vars.raw_mr_predictors = []
	#global_vars.raw_indttest_groupvar =  
	#global_vars.raw_indttest_grouplevel1 =  
	#global_vars.raw_indttest_grouplevel2 =  
	global_vars.raw_indttest_dv = []
	global_vars.raw_pairttest_var_pairs = []
	#global_vars.summ_corr_varOne =  
	#global_vars.summ_corr_varTwo =  
	#global_vars.summ_corr_coeff =  
	#global_vars.summ_corr_pvalues =  
	#global_vars.summ_indttest_var =  
	#global_vars.summ_indttest_meanOne =  
	#global_vars.summ_indttest_sdOne =  
	#global_vars.summ_indttest_nOne =  
	#global_vars.summ_indttest_meanTwo =  
	#global_vars.summ_indttest_sdTwo =  
	#global_vars.summ_indttest_nTwo =  
	#global_vars.summ_indttest_equal_var =  
	#global_vars.spss_test =  
	global_vars.spss_indttest_nOne = -1
	global_vars.spss_indttest_nTwo = -1
	#global_vars.spss_indttest_groupOneLabel =  
	#global_vars.spss_indttest_groupTwoLabel =  
	global_vars.spss_pairttest_nOne = -1
	global_vars.spss_pairttest_nTwo = -1
	global_vars.effect_size_choice = "none"
	global_vars.correction_type = "fdr_bh"
	global_vars.non_numeric_input_raise_errors = True
	global_vars.raw_ttest_output_descriptives = False

	raw_data_df = raw_correlations.get_raw_data_df()
	mod_raw_data_df = raw_correlations.modify_raw_data_df(raw_data_df)
	output_df = raw_correlations.generate_output_df(mod_raw_data_df)
	output_df = helper_funcs.multitest_correction(output_df)

	df1_from_mapas = output_df[["Variable1", "Variable2", "Correlation_Coefficient", "pvalues", "adjusted_pvalues"]]
	#df1_from_mapas.rename(columns={"Correlation Coefficient" : "Correlation.Coefficient"}, inplace=True)

	df2 = pd.read_excel("df5_r_output.xlsx")

	pd.testing.assert_frame_equal(df1_from_mapas, df2, check_less_precise=3)


test_1()
#test_2()
