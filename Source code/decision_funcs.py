# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import main_funcs_raw_correlations
import main_funcs_raw_mr
import main_funcs_raw_indttest
import main_funcs_raw_pairttest
import main_funcs_summ_correlations
import main_funcs_summ_indttest
import main_funcs_spss_correlations
import main_funcs_spss_mr
import main_funcs_spss_indttest
import main_funcs_spss_pairttest
import main_funcs_pvalues

import pandas as pd
import numpy as np
from statsmodels.stats import multitest
import global_vars
import helper_funcs

def get_raw_data_df():
	if global_vars.raw_test == "corr":
		cols = global_vars.raw_corr_vars
	elif global_vars.raw_test == "mr":
		cols = [global_vars.raw_mr_outcomevar] + global_vars.raw_mr_predictors
	elif global_vars.raw_test == "indttest":
		cols = [global_vars.raw_indttest_groupvar] + global_vars.raw_indttest_dv
	elif global_vars.raw_test == "pairttest":
		cols = [var for pair in global_vars.raw_pairttest_var_pairs for var in pair]
	elif global_vars.input_type == "summ_corr":
		cols = [global_vars.summ_corr_varOne, global_vars.summ_corr_varTwo, global_vars.summ_corr_coeff, global_vars.summ_corr_pvalues]
	elif global_vars.input_type == "summ_indttest":
		cols = [global_vars.summ_indttest_var, global_vars.summ_indttest_meanOne, global_vars.summ_indttest_sdOne, global_vars.summ_indttest_nOne,
				global_vars.summ_indttest_meanTwo, global_vars.summ_indttest_sdTwo, global_vars.summ_indttest_nTwo]
		if global_vars.summ_indttest_equal_var != "":
			cols.append(global_vars.summ_indttest_equal_var)
	else:
		cols = None #default to read all cols
	
	try:
		if global_vars.input_path_and_filename.endswith(".xlsx"):
			raw_data_df = pd.read_excel(global_vars.input_path_and_filename, usecols=cols)
		elif global_vars.input_path_and_filename.endswith(".csv"):
			raw_data_df = pd.read_csv(global_vars.input_path_and_filename, usecols=cols)
	except:
		raise Exception("Oh-oh. For some reason the provided file cannot be read. Please try another file - make sure it's either .xlsx or .csv file.")

	return raw_data_df

def modify_raw_data_df(raw_data_df):
	if global_vars.input_type == "raw":

		if global_vars.raw_test == "corr":
			numeric_cols = global_vars.raw_corr_vars
			non_numeric_cols = []

		elif global_vars.raw_test == "mr":
			numeric_cols = [global_vars.raw_mr_outcomevar] + global_vars.raw_mr_predictors
			non_numeric_cols = []

		elif global_vars.raw_test == "indttest":
			numeric_cols = global_vars.raw_indttest_dv
			non_numeric_cols = [global_vars.raw_indttest_groupvar]

		elif global_vars.raw_test == "pairttest":
			numeric_cols = list(np.array(global_vars.raw_pairttest_var_pairs).flatten())
			non_numeric_cols = []

		
		if global_vars.non_numeric_input_raise_errors == True:
			helper_funcs.error_on_input(df=raw_data_df, cols=numeric_cols, input_type="numeric")
		
		mod_raw_data_df = helper_funcs.raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols, non_numeric_cols)
	
	elif global_vars.input_type == "summ_corr":
		numeric_cols = [global_vars.summ_corr_coeff, global_vars.summ_corr_pvalues]
		non_numeric_cols = [global_vars.summ_corr_varOne, global_vars.summ_corr_varTwo]
		helper_funcs.error_on_input(df=raw_data_df, cols=numeric_cols, input_type="numeric")
		helper_funcs.error_on_input(df=raw_data_df, cols=non_numeric_cols, input_type="nan")
		mod_raw_data_df = helper_funcs.raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols, non_numeric_cols)

	elif global_vars.input_type == "summ_indttest":
		numeric_cols = [global_vars.summ_indttest_meanOne, global_vars.summ_indttest_sdOne, global_vars.summ_indttest_nOne, global_vars.summ_indttest_meanTwo, global_vars.summ_indttest_sdTwo, global_vars.summ_indttest_nTwo]
		non_numeric_cols = [global_vars.summ_indttest_var]
		if global_vars.summ_indttest_equal_var != "":
			non_numeric_cols.append(global_vars.summ_indttest_equal_var)
		helper_funcs.error_on_input(df=raw_data_df, cols=numeric_cols, input_type="numeric")
		helper_funcs.error_on_input(df=raw_data_df, cols=non_numeric_cols, input_type="nan")
		mod_raw_data_df = main_funcs_summ_indttest.summ_inddtest_generate_mod_raw_data_df(raw_data_df, numeric_cols, non_numeric_cols)

	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "corr":
			mod_raw_data_df = main_funcs_spss_correlations.spss_corr_generate_mod_raw_data_df(raw_data_df)
		elif global_vars.spss_test == "mr":
			mod_raw_data_df = main_funcs_spss_mr.spss_mr_generate_mod_raw_data_df(raw_data_df)
		elif global_vars.spss_test == "indttest":
			mod_raw_data_df = main_funcs_spss_indttest.spss_indttest_generate_mod_raw_data_df(raw_data_df)
		elif global_vars.spss_test == "pairttest":
			mod_raw_data_df = main_funcs_spss_pairttest.spss_pairttest_generate_mod_raw_data_df(raw_data_df)
	elif global_vars.input_type == "pvalues":
		helper_funcs.error_on_input(df=raw_data_df, cols=[global_vars.pvalues_col], input_type="numeric")
		mod_raw_data_df = main_funcs_pvalues.pvalues_generate_mod_raw_data_df(raw_data_df)

	return mod_raw_data_df

def generate_output_df(mod_raw_data_df):
	if global_vars.input_type == "raw":
		if global_vars.raw_test =="corr":
			output_df = main_funcs_raw_correlations.raw_corr_generate_output_df(mod_raw_data_df)
		elif global_vars.raw_test == "mr":
			output_df = main_funcs_raw_mr.raw_mr_generate_output_df(mod_raw_data_df)
		elif global_vars.raw_test == "indttest":
			output_df = main_funcs_raw_indttest.raw_indttest_generate_output_df(mod_raw_data_df)
		elif global_vars.raw_test == "pairttest":
			output_df = main_funcs_raw_pairttest.raw_pairttest_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "summ_corr":
		output_df = main_funcs_summ_correlations.summ_corr_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "summ_indttest":
		output_df = main_funcs_summ_indttest.summ_indttest_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "corr":
			output_df = main_funcs_spss_correlations.spss_corr_generate_output_df(mod_raw_data_df)
		elif global_vars.spss_test == "mr":
			output_df = main_funcs_spss_mr.spss_mr_generate_output_df(mod_raw_data_df)
		elif global_vars.spss_test == "indttest":
			output_df = main_funcs_spss_indttest.spss_indttest_generate_output_df(mod_raw_data_df)
		elif global_vars.spss_test == "pairttest":
			output_df = main_funcs_spss_pairttest.spss_pairttest_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "pvalues":
		output_df = main_funcs_pvalues.pvalues_generate_output_df(mod_raw_data_df)

	return output_df

def multitest_correction(output_df):
	if global_vars.input_type == "summ_corr":
		pvalues_col_label = global_vars.summ_corr_pvalues
	elif global_vars.input_type == "pvalues":
		pvalues_col_label = global_vars.pvalues_col
	else:
		pvalues_col_label = "pvalues"
	
	if global_vars.correction_type != "None":
		if output_df[pvalues_col_label].isnull().values.any():
			#the correction function cannot handle missing values very well; workarounds exist but they do not make sense in the context of the software
			#see https://github.com/statsmodels/statsmodels/issues/2899
			raise Exception("The pvalues column contains blank cells. Please make sure that all data in the pvalues column is filled.")
		
		adjusted_pvalues = multitest.multipletests(output_df[pvalues_col_label], alpha=global_vars.alpha_threshold, method=global_vars.correction_type, is_sorted=False, returnsorted=False)[1]
	else:
		adjusted_pvalues = output_df[pvalues_col_label]
	
	output_df["adjusted_pvalues"] = adjusted_pvalues

	return output_df

def save_output(mod_raw_data_df, output_df):
	if global_vars.input_type == "raw":
		if global_vars.raw_test =="corr":
			if global_vars.output_filetype == "Excel":
				if global_vars.raw_corr_include_CI:
					main_funcs_raw_correlations.raw_corr_apa_table_withCIs_excel(mod_raw_data_df, output_df)
				else:
					main_funcs_raw_correlations.raw_corr_apa_table_noCIs_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				if global_vars.raw_corr_include_CI:
					main_funcs_raw_correlations.raw_corr_apa_table_withCIs_word(mod_raw_data_df, output_df)
				else:
					main_funcs_raw_correlations.raw_corr_apa_table_noCIs_word(mod_raw_data_df, output_df)
		elif global_vars.raw_test == "mr":
			if global_vars.output_filetype == "Excel":
				main_funcs_raw_mr.raw_mr_apa_table_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				main_funcs_raw_mr.raw_mr_apa_table_word(mod_raw_data_df, output_df)
		elif global_vars.raw_test == "indttest":
			if global_vars.output_filetype == "Excel":
				main_funcs_raw_indttest.raw_indttest_apa_table_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				main_funcs_raw_indttest.raw_indttest_apa_table_word(mod_raw_data_df, output_df)
		elif global_vars.raw_test == "pairttest":
			if global_vars.output_filetype == "Excel":
				main_funcs_raw_pairttest.raw_pairttest_apa_table_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				main_funcs_raw_pairttest.raw_pairttest_apa_table_word(mod_raw_data_df, output_df)
	
	elif global_vars.input_type == "summ_corr":
		if global_vars.output_filetype == "Excel":
			main_funcs_summ_correlations.summ_corr_apa_table_excel(mod_raw_data_df, output_df)
		elif global_vars.output_filetype == "Word":
			main_funcs_summ_correlations.summ_corr_apa_table_word(mod_raw_data_df, output_df)
	
	elif global_vars.input_type == "summ_indttest":
		if global_vars.output_filetype == "Excel":
			main_funcs_summ_indttest.summ_indttest_apa_table_excel(mod_raw_data_df, output_df)
		elif global_vars.output_filetype == "Word":
			main_funcs_summ_indttest.summ_indttest_apa_table_word(mod_raw_data_df, output_df)
	
	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "corr":
			if global_vars.output_filetype == "Excel":
				main_funcs_spss_correlations.spss_corr_apa_table_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				main_funcs_spss_correlations.spss_corr_apa_table_word(mod_raw_data_df, output_df)
		elif global_vars.spss_test == "mr":
			if global_vars.output_filetype == "Excel":
				main_funcs_spss_mr.spss_mr_apa_table_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				main_funcs_spss_mr.spss_mr_apa_table_word(mod_raw_data_df, output_df)
		elif global_vars.spss_test == "indttest":
			if global_vars.output_filetype == "Excel":
				main_funcs_spss_indttest.spss_indttest_apa_table_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				main_funcs_spss_indttest.spss_indttest_apa_table_word(mod_raw_data_df, output_df)
		elif global_vars.spss_test == "pairttest":
			if global_vars.output_filetype == "Excel":
				main_funcs_spss_pairttest.spss_pairttest_apa_table_excel(mod_raw_data_df, output_df)
			elif global_vars.output_filetype == "Word":
				main_funcs_spss_pairttest.spss_pairttest_apa_table_word(mod_raw_data_df, output_df)
	
	elif global_vars.input_type == "pvalues":
		main_funcs_pvalues.pvalues_table(mod_raw_data_df, output_df)