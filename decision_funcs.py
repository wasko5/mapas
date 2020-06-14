import raw_correlations
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

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats import multitest
import researchpy as rp
from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
import global_vars
import calculations_helper_functions_only as helper_funcs


def get_raw_data_df():
	if global_vars.input_path_and_filename.endswith(".xlsx"):
		try:
			raw_data_df = pd.read_excel(global_vars.input_path_and_filename)
		except:
			raise Exception("Oh-oh. For some reason we cannot read the provided file. Please try another file - make sure it's an excel spreadsheet.")

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
			non_numeric_cols = [global_vars.raw_indttest_groupvar] ###list(set(list(raw_data_df.columns)) - set(numeric_cols)) #this is fine because numeric_cols is a subset of df.columns; could be a problem only if numeric_cols could contain unique values - https://stackoverflow.com/questions/3462143/get-difference-between-two-lists

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
		mod_raw_data_df = helper_funcs.raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols, non_numeric_cols) #this function works but need to change name

	elif global_vars.input_type == "summ_indttest":
		numeric_cols = [global_vars.summ_indttest_meanOne, global_vars.summ_indttest_sdOne, global_vars.summ_indttest_nOne, global_vars.summ_indttest_meanTwo, global_vars.summ_indttest_sdTwo, global_vars.summ_indttest_nTwo]
		non_numeric_cols = [global_vars.summ_indttest_var]
		if global_vars.summ_indttest_equal_var != "":
			non_numeric_cols.append(global_vars.summ_indttest_equal_var)
		helper_funcs.error_on_input(df=raw_data_df, cols=numeric_cols, input_type="numeric")
		helper_funcs.error_on_input(df=raw_data_df, cols=non_numeric_cols, input_type="nan")
		mod_raw_data_df = summ_indttest.summ_inddtest_generate_mod_raw_data_df(raw_data_df, numeric_cols, non_numeric_cols)

	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "corr":
			mod_raw_data_df = spss_correlations.spss_corr_generate_mod_raw_data_df(raw_data_df)
		elif global_vars.spss_test == "mr":
			mod_raw_data_df = spss_mr.spss_mr_generate_mod_raw_data_df(raw_data_df) #might remove the function depending on whether I add logical checks
		elif global_vars.spss_test == "indttest":
			mod_raw_data_df = spss_indttest.spss_indttest_generate_mod_raw_data_df(raw_data_df) #might remove the function depending on whether I add logical checks
		elif global_vars.spss_test == "pairttest":
			mod_raw_data_df = spss_pairttest.spss_pairttest_generate_mod_raw_data_df(raw_data_df) #might remove the function depending on whether I add logical checks
	elif global_vars.input_type == "pvalues":
		mod_raw_data_df = pvalues.pvalues_generate_mod_raw_data_df(raw_data_df) #-------------------------------------------------------------------TO LET USER CHOOSE PVALUE COLUMN

	return mod_raw_data_df

def generate_output_df(mod_raw_data_df):
	if global_vars.input_type == "raw":
		if global_vars.raw_test =="corr":
			output_df = raw_correlations.raw_corr_generate_output_df(mod_raw_data_df)
		elif global_vars.raw_test == "mr":
			output_df = raw_mr.raw_mr_generate_output_df(mod_raw_data_df)
		elif global_vars.raw_test == "indttest":
			output_df = raw_indttest.raw_indttest_generate_output_df(mod_raw_data_df)
		elif global_vars.raw_test == "pairttest":
			output_df = raw_pairttest.raw_pairttest_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "summ_corr":
		output_df = summ_correlations.summ_corr_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "summ_indttest":
		output_df = summ_indttest.summ_indttest_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "corr":
			output_df = spss_correlations.spss_corr_generate_output_df(mod_raw_data_df)
		elif global_vars.spss_test == "mr":
			output_df = spss_mr.spss_mr_generate_output_df(mod_raw_data_df)
		elif global_vars.spss_test == "indttest":
			output_df = spss_indttest.spss_indttest_generate_output_df(mod_raw_data_df)
		elif global_vars.spss_test == "pairttest":
			output_df = spss_pairttest.spss_pairttest_generate_output_df(mod_raw_data_df)
	elif global_vars.input_type == "pvalues":
		output_df = pvalues.pvalues_generate_output_df(mod_raw_data_df)

	return output_df

def multitest_correction(output_df):
	if global_vars.input_type == "summ_corr":
		pvalues_col_label = global_vars.summ_corr_pvalues
	elif global_vars.input_type == "pvalues":
		pvalues_col_label = global_vars.pvalues_col
	else:
		pvalues_col_label = "pvalues"
	
	if output_df[pvalues_col_label].isnull().values.any():
		#the correction function cannot handle missing values very well; workaround exist but they do not make sense in the context of the software
		#see https://github.com/statsmodels/statsmodels/issues/2899
		raise Exception("The pvalues column contains blank cells. Please make sure that all data in the pvalues column is filled.")
	
	if global_vars.spss_test != "mr":
		if global_vars.correction_type != "none":    
			adjusted_pvalues = multitest.multipletests(output_df[pvalues_col_label], alpha=global_vars.alpha_threshold, method=global_vars.correction_type, is_sorted=False, returnsorted=False)[1]
		else:
			adjusted_pvalues = output_df[pvalues_col_label]
		
		output_df["adjusted_pvalues"] = adjusted_pvalues

	return output_df

def save_output(mod_raw_data_df, output_df):
	if global_vars.input_type == "raw":
		if global_vars.raw_test =="corr":
			raw_correlations.raw_corr_apa_table(mod_raw_data_df, output_df)
		elif global_vars.raw_test == "mr":
			raw_mr.raw_mr_apa_table(mod_raw_data_df, output_df)
		elif global_vars.raw_test == "indttest":
			raw_indttest.raw_indttest_apa_table(mod_raw_data_df, output_df)
			if global_vars.raw_ttest_output_descriptives == True:
				raw_indttest.raw_indttest_descriptives_table(mod_raw_data_df, output_df)
		elif global_vars.raw_test == "pairttest":
			raw_pairttest.raw_pairttest_apa_table(mod_raw_data_df, output_df)
			if global_vars.raw_ttest_output_descriptives == True:
				raw_pairttest.raw_pairttest_descriptives_table(mod_raw_data_df, output_df)
	elif global_vars.input_type == "summ_corr":
		summ_correlations.summ_corr_apa_table(mod_raw_data_df, output_df)
	elif global_vars.input_type == "summ_indttest":
		summ_indttest.summ_indttest_apa_table(mod_raw_data_df, output_df)
	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "corr":
			spss_correlations.spss_corr_apa_table(mod_raw_data_df, output_df)
		elif global_vars.spss_test == "mr":
			spss_mr.spss_mr_apa_table(mod_raw_data_df, output_df)
		elif global_vars.spss_test == "indttest":
			spss_indttest.spss_indttest_apa_table(mod_raw_data_df, output_df)
		elif global_vars.spss_test == "pairttest":
			spss_pairttest.spss_pairttest_apa_table(mod_raw_data_df, output_df)
	elif global_vars.input_type == "pvalues":
		pvalues.pvalues_table(mod_raw_data_df, output_df)

