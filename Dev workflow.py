import decision_funcs
import global_vars
import helper_funcs

global_vars.input_path_and_filename = "D:/Desktop_current/MAPAS/GitHub/old/Input files/spss/input_spss_pairedTtest.xlsx"
global_vars.alpha_threshold = 0.05
global_vars.output_filename = "D:/Desktop_current/MAPAS/GitHub/a"
global_vars.output_filetype = "Word"
global_vars.input_type = "spss"
global_vars.raw_test = ""
global_vars.raw_corr_type = ""
global_vars.raw_corr_vars = []
global_vars.raw_mr_outcomevar = ""
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
global_vars.spss_test = "pairttest"
global_vars.spss_indttest_nOne = -1
global_vars.spss_indttest_nTwo = -1
global_vars.spss_indttest_groupOneLabel = "Group1"
global_vars.spss_indttest_groupTwoLabel = "Group2"
global_vars.spss_pairttest_n = 25
global_vars.pvalues_col = ""
global_vars.effect_size_choice = "None"
global_vars.correction_type = "bonferroni"
global_vars.non_numeric_input_raise_errors = ""


raw_data_df = decision_funcs.get_raw_data_df()
mod_raw_data_df = decision_funcs.modify_raw_data_df(raw_data_df)
output_df = decision_funcs.generate_output_df(mod_raw_data_df)
output_df = decision_funcs.multitest_correction(output_df)
decision_funcs.save_output(mod_raw_data_df, output_df)