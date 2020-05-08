import pandas as pd
import global_vars
#import calculations_helper_functions_only as helper_funcs
import decision_funcs




def raw_corr_pearson_fdrBH_raiseErrors():
	#global vars
	global_vars.input_path_and_filename = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/raw_corr_pearson_fdrBH_raiseErrors.xlsx"
	global_vars.alpha_threshold = 0.05
	global_vars.output_filename = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/raw_corr_pearson_fdrBH_raiseErrors_MAPAS"
	global_vars.input_type =  "raw"
	global_vars.raw_test =  "corr"
	global_vars.raw_corr_type =  "pearson"
	global_vars.raw_corr_vars = ["a", "b", "c", "d"]
	global_vars.raw_mr_outcomevar =  ""
	global_vars.raw_mr_predictors = []
	global_vars.raw_indttest_groupvar = ""
	global_vars.raw_indttest_grouplevel1 = ""
	global_vars.raw_indttest_grouplevel2 = ""
	global_vars.raw_indttest_dv = []
	global_vars.raw_pairttest_var_pairs = []
	global_vars.summ_corr_varOne = ""
	global_vars.summ_corr_varTwo = ""
	global_vars.summ_corr_coeff = ""
	global_vars.summ_corr_pvalues = ""
	global_vars.summ_indttest_var = ""
	global_vars.summ_indttest_meanOne = ""
	global_vars.summ_indttest_sdOne = ""
	global_vars.summ_indttest_nOne = ""
	global_vars.summ_indttest_meanTwo = ""
	global_vars.summ_indttest_sdTwo = ""
	global_vars.summ_indttest_nTwo = ""
	global_vars.summ_indttest_equal_var = ""
	global_vars.spss_test = ""
	global_vars.spss_indttest_nOne = -1
	global_vars.spss_indttest_nTwo = -1
	global_vars.spss_indttest_groupOneLabel = ""
	global_vars.spss_indttest_groupTwoLabel = ""
	global_vars.spss_pairttest_nOne = -1
	global_vars.spss_pairttest_nTwo = -1
	global_vars.effect_size_choice = "none"
	global_vars.correction_type = "fdr_bh"
	global_vars.non_numeric_input_raise_errors = True
	global_vars.raw_ttest_output_descriptives = False

	raw_data_df = decision_funcs.get_raw_data_df()
	mod_raw_data_df = decision_funcs.modify_raw_data_df(raw_data_df)
	output_df = decision_funcs.generate_output_df(mod_raw_data_df)
	output_df = decision_funcs.multitest_correction(output_df)

	df_from_mapas = output_df
	#df_from_mapas.to_excel("df_from_mapas.xlsx")

	#df_from_mapas = output_df[["Variable1", "Correlation_Coefficient", "Variable2", "pvalues", "adjusted_pvalues"]]

	#df_from_mapas = output_df[["Variable1", "Variable2", "Correlation_Coefficient", "pvalues", "adjusted_pvalues"]]
	#df1_from_mapas.rename(columns={"Correlation Coefficient" : "Correlation.Coefficient"}, inplace=True)

	df_from_r = pd.read_excel("D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/raw_corr_pearson_fdrBH_raiseErrors_R.xlsx")

	pd.testing.assert_frame_equal(df_from_mapas, df_from_r, check_less_precise=3)


raw_corr_pearson_fdrBH_raiseErrors()
#test_2()
