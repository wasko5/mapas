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


#Helper functions for GUI
def get_df_columns(path_and_filename):
	try:
		if path_and_filename.endswith(".xlsx"):
			df_columns = list(pd.read_excel(path_and_filename, sheet_name=0).columns)
		elif path_and_filename.endsiwth(".csv"):
			df_columns = list(pd.read_csv(path_and_filename).columns)

		return df_columns
	except:
		raise Exception("There was a problem reading the columns from the file.")

def get_raw_indttest_grouplevels(path_and_filename, group_var):
	try:
		if path_and_filename.endswith(".xlsx"):
			df = pd.read_excel(path_and_filename, sheet_name=0)
		elif path_and_filename.endsiwth(".csv"):
			df = pd.read_csv(path_and_filename)
	except:
		raise Exception("There was a problem reading the columns from the file.")

	
	unique_groups = [x.strip() for x in df[group_var].astype(str).unique() if len(x.strip()) > 0]

	return unique_groups

#1.1.1. Helper functions fo generating modified raw data dataframes
def raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols, non_numeric_cols=[]):
	mod_raw_data_df = raw_data_df[numeric_cols + non_numeric_cols] #does NOT raise errors when array is blank (default arg)
	mod_raw_data_df[numeric_cols] = mod_raw_data_df[numeric_cols].apply(pd.to_numeric, errors="coerce") #non-numeric values will be np.nan
	try:
		mod_raw_data_df[non_numeric_cols] = mod_raw_data_df[non_numeric_cols].astype(str) #does NOT raise errors when array is blank (default arg)
	except:
		raise Exception("The data could not be processed. Please ensure that the non-numeric columns contain only strings.")
	#mod_raw_data_df = mod_raw_data_df.dropna().reset_index(drop=True) NEVER DOROP NA HERE - JUST COERCE TO KNOW WHERE NA VALUES ARE BUT DO NOT ALTER!!!!
	
	return mod_raw_data_df

def get_numeric_cols(raw_data_df):
	numeric_cols = list(raw_data_df.columns)
	if global_vars.input_type == "summ_indttest":
		numeric_cols.remove(global_vars.summ_indttest_var)
		numeric_cols.remove(global_vars.summ_indttest_equal_var)
		
	return numeric_cols

def error_on_input(df, cols, input_type):
	'''
	df - the dataframe to check
	cols - the cols to check
	input_type - the input type to check for - can be either 'numeric' or 'nan'
	'''
	bad_vals_dict = {}
	for var in cols:
		if input_type == "numeric":
			current_series = pd.to_numeric(df[var], errors="coerce")
		elif input_type == "nan":
			current_series = df[var]
		ind_list = list(current_series.isnull().to_numpy().nonzero()[0])
		if ind_list != []:
			bad_vals_dict[var] = ind_list
	if bad_vals_dict != {}:
		error_msg = "Non-numerical or blank entries found in the data!\n"
		for col, ind_arr in bad_vals_dict.items():
			error_msg += "In column {c}, there are non-numerical/blank entries on the following rows: {i}\n".format(c=col, i=(", ").join([str(x+2) for x in ind_arr]))
		raise Exception(error_msg)

def summ_input_colNames_check(raw_data_df, provided_cols):
	for var in provided_cols:
		if var not in list(raw_data_df.columns):
			raise Exception("Column {} is not found in the provided file.\nPlease ensure that the column names are typed correctly.".format(var))
	if len(list(raw_data_df.columns)) > len(provided_cols):
		raise Exception("The provided file contains too many columns. Please provide only {}.".format(len(provided_cols)))


#1.2.1. Helper functions for generating output dataframes
def raw_input_corr_coeff(x, y):
	if global_vars.raw_corr_type == "pearson":
		#although it's a clunky loop, there does not seem to be another way around:
				#https://stackoverflow.com/questions/38894488/dropping-nan-with-pearsons-r-in-scipy-pandas
		x = np.array(x)
		y = np.array(y)
		nas = ~np.logical_or(np.isnan(x), np.isnan(y))
		x = np.compress(nas, x)
		y = np.compress(nas, y)

		r, p = stats.pearsonr(x, y)
	elif global_vars.raw_corr_type == "spearman":
		r, p = stats.spearmanr(x, y, nan_policy="omit")
	elif global_vars.raw_corr_type == "kendall":
		r, p = stats.kendalltau(x, y, nan_policy="omit")

	return r, p

def corr_coeff_ci(r, n):
	'''
	Credits: https://zhiyzuo.github.io/Pearson-Correlation-CI-in-Python/
	'''
	if n < 4:
		raise Exception("Sample size is too low for correlations. Minimum of 4 observations per variable required.")

	r_z = np.arctanh(r)
	se = 1/np.sqrt(n-3)
	z = stats.norm.ppf(1-0.05/2)
	low_z = r_z - z*se 
	high_z = r_z + z*se
	low, high = np.tanh((low_z, high_z))
	
	return low, high

#1.3.1. Helper functions for saving data
def pvalue_formatting(x):
	if x<0.001:
		return "<.001"
	else:
		return "{:.3f}".format(x).replace("0", "", 1)

def correlations_format_val(x, p=None):
	try:
		if isinstance(x, str): #covers the case when the correlations come from SPSS input and are flagged significant
			x = "{:.2f}".format(float("".join([char for char in x if char!="*"]))).replace("0","",1)
		elif abs(x) == 1.0:
			x = "{:.2f}".format(val)
		else:
			x = "{:.2f}".format(x).replace("0","",1)
	except:
		raise Exception("Something went wrong with formatting the correlation coefficients. Please try again.")
	if p != None:
		if p < 0.001:
			x = x + "**"
		elif p < 0.05:
			x = x + "*"
	return x

def add_table_notes(ws, table_notes=[], adjusted_pvalues_threshold=None):
	if global_vars.correction_type != "none":
		#currently using the master_dict indexing for the correction lookup, but might separate the master_dict into different ones later
		#however, consider a helper lookup func for the long expression - see also raw_correlations
		table_notes.append("Multiple tests correction applied to p values: {c}".format(c=list(global_vars.master_dict.keys())[list(global_vars.master_dict.values()).index(global_vars.correction_type)]))
		'''
		##############################################################the function needs to work without the below
		if global_vars.output_pvalues_type == "adjusted":
			table_notes.append("Adjusted p values used; significant at {alpha}".format(alpha=global_vars.alpha_threshold))
		elif global_vars.output_pvalues_type == "original":
			table_notes.append("Original p values used; significant at {alpha}".format(alpha=adjusted_pvalues_threshold))
		'''
		
	for note in table_notes:
		ws.append([note])

def save_file(output_name, wb):
	time_now = datetime.now().strftime("%H%M%S-%Y%m%d")
	filename = global_vars.output_filename + "_" + time_now + ".xlsx"
	wb.save(filename=filename)




