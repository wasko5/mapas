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

output_pvalues_type = "" #temporary to work until functionality is fixed

#-----------------------------------------------------------0. Input----------------------------------------------------
#Commented out variables would either not be used or are considered for removal
input_filename = "Input files\\input_p-values.xlsx"
#input_fileext = ""
alpha_threshold = 0.05
output_filename = "Output files for testing\\pvalues_" #this does not end in .xlsx just for testing; in real app it should end with .xlsx (reason: function will add random numbers to prevent overwriting)

input_type = "pvalues"

raw_test = ""

#raw_corr_type = ""
#raw_mr_outcomevar = ""
#raw_mr_predictors = ""
#raw_indttest_groupvar = ""
#raw_indttest_dv = ""
#raw_pairttest_var_pairs = ""

#summ_corr_varOne = ""
#summ_corr_varTwo = ""
#summ_corr_coeff = ""
#summ_corr_pvalues = ""

#summ_indttest_var = ""
#summ_indttest_meanOne = ""
#summ_indttest_sdOne = ""
#summ_indttest_nOne = ""
#summ_indttest_meanTwo = ""
#summ_indttest_sdTwo = ""
#summ_indttest_nTwo = ""
#summ_indttest_equal_var = ""

#spss_test = ""
#spss_indttest_nOne = ""
#spss_indttest_nTwo = ""
#spss_indttest_groupOneLabel = ""
#spss_indttest_groupTwoLabel = ""
#spss_pairttest_nOne = ""
#spss_pairttest_nTwo = ""

#effect_size_choice = "" #could also be "Hedge's g", "Glass's delta" or blank/none (no idea which one it was)
correction_type = "fdr_bh" #see global_vars.master_dict for other values

#non_numeric_input_raise_errors = True #defaults to True here
#raw_ttest_output_descriptives = ""


#-----------------------------------------------------------1. Main flow----------------------------------------------------
#Note that the execution of the main flow is at the bottom
def get_raw_data_df():
	raw_data_df = pd.read_excel(input_filename, sheet_name=0)

	return raw_data_df

def modify_raw_data_df(raw_data_df):
	if "pvalues" not in raw_data_df.columns:
		raise Exception("Column \'pvalues\' is not found in the provided file. Please make sure it is typed correctly.")
	error_on_non_numeric_input(raw_data_df, ["pvalues"])
	mod_raw_data_df = raw_data_df.copy()

	return mod_raw_data_df

def generate_output_df(mod_raw_data_df):
	output_df = pvalues_generate_output_df(mod_raw_data_df)

	return output_df

def multitest_correction(output_df):
	pvalues_list = output_df["pvalues"]
	sign_col_label = "Adjusted p value significant at alpha = {alpha}".format(alpha=alpha_threshold)

	if correction_type != "":    
		if correction_type == "sidak":
			sign_col_label = "Original p value significant at corrected alpha = {alpha}".format(alpha=round(multitest.multipletests(pvalues_list, alpha=alpha_threshold, method=correction_type, is_sorted=False, returnsorted=False)[2],5))
		elif correction_type == "bonferroni":
			sign_col_label = "Original p value significant at corrected alpha = {alpha}".format(alpha=round(multitest.multipletests(pvalues_list, alpha=alpha_threshold, method=correction_type, is_sorted=False, returnsorted=False)[3],5))

		adjusted_pvalues = multitest.multipletests(pvalues_list, alpha=alpha_threshold, method=correction_type, is_sorted=False, returnsorted=False)[1]
		sign_bools = multitest.multipletests(pvalues_list, alpha=alpha_threshold, method=correction_type, is_sorted=False, returnsorted=False)[0]
	else:
		adjusted_pvalues = pvalues_list
		sign_bools = [bool(x < alpha_threshold) for x in pvalues_list]
		
	output_df["adjusted_pvalues"] = adjusted_pvalues
	output_df[sign_col_label] = sign_bools

	output_df[sign_col_label] = output_df[sign_col_label].replace(True,"Significant")
	output_df[sign_col_label] = output_df[sign_col_label].replace(False,"Non-significant")

	return output_df

def save_output(mod_raw_data_df, output_df):
	pvalues_table(mod_raw_data_df, output_df)

#-----------------------------------------------------------2. Modified raw data dataframe----------------------------------------------------
#2.1.  Helper functions fo generating modified raw data dataframes - all not just function-specific ones
def get_numeric_cols(raw_data_df):
	numeric_cols = list(raw_data_df.columns)
	if raw_test == "indttest":
		try:
			numeric_cols.remove(raw_indttest_groupvar)
		except ValueError:
			raise Exception("The grouping variable \'{}\' is not found in the file. Please make sure it is type correctly.".format(raw_indttest_groupvar))
	elif input_type == "summ_corr":
		#no need for error handling as the summ_corr_colNames_check func has already taken care of that
		numeric_cols.remove(summ_corr_varOne)
		numeric_cols.remove(summ_corr_varTwo)
	elif input_type == "summ_indttest":
		numeric_cols.remove(summ_indttest_var)
		numeric_cols.remove(summ_indttest_equal_var)
		
	return numeric_cols

def error_on_non_numeric_input(raw_data_df, numeric_cols):
	bad_vals_dict = {}
	for var in numeric_cols:
		ind_list = list(pd.to_numeric(raw_data_df[var], errors='coerce').isnull().to_numpy().nonzero()[0])
		if ind_list != []:
			bad_vals_dict[var] = ind_list
	if bad_vals_dict != {}:
		error_msg = "Non-numerical or blank entries found in the data!\n"
		for col, ind_arr in bad_vals_dict.items():
			error_msg += "In column {c}, there are non-numerical/blank entries on the following rows: {i}\n".format(c=col, i=(", ").join([str(x+2) for x in ind_arr]))
		raise Exception(error_msg)

def raw_input_pairttest_colNames_check(raw_data_df):
	inputVars_unique = []
	for var_time1, var_time2 in raw_pairttest_inputVars_list:
		if var_time1 not in raw_data_df.columns:
			raise Exception("The entered column \'{}\' is not found in the provided file.".format(var_time1))
		elif var_time2 not in raw_data_df.columns:
			raise Exception("The entered column \'{}\' is not found in the provided file.".format(var_time2))
		else:
			inputVars_unique.append(var_time1)
			inputVars_unique.append(var_time2)
	inputVars_unique = list(set(inputVars_unique))
	if len(inputVars_unique) > len(list(raw_data_df.columns)):
		raise Exception("The provided number of unique variable columns is {i}, while the number of columns in the provided file is {f}".format(i=len(inputVars_unique), f=len(list(raw_data_df.columns))))

def summ_input_colNames_check(raw_data_df, provided_cols):
	for var in provided_cols:
		if var not in list(raw_data_df.columns):
			raise Exception("Column {} is not found in the provided file.\nPlease ensure that the column names are typed correctly.".format(var))
	if len(list(raw_data_df.columns)) > len(provided_cols):
		raise Exception("The provided file contains too many columns. Please provide only {}.".format(len(provided_cols)))

#2.1.  Main function for generating the modified raw data dataframe
#None - done directly in the "modify_raw_data_df" function

#-----------------------------------------------------------3. Output dataframe----------------------------------------------------
#3.1. Helper functions for generating output dataframes - all not just function-specific ones
def raw_input_corr_coeff(x, y):
	if raw_corr_type == "pearson":
		x = np.array(x)
		y = np.array(y)
		nas = ~np.logical_or(np.isnan(x), np.isnan(y))
		x = np.compress(nas, x)
		y = np.compress(nas, y)

		r, p = stats.pearsonr(x, y)
	elif raw_corr_type == "spearman":
		r, p = stats.spearmanr(x, y, nan_policy="omit")
	elif raw_corr_type == "kendall":
		r, p = stats.kendalltau(x, y, nan_policy="omit")

	return r, p

def corr_coeff_ci(r, n):
	if n < 4:
		raise Exception("Sample size is too low for correlations. Minimum of 4 observations per variable required.")

	r_z = np.arctanh(r)
	se = 1/np.sqrt(n-3)
	z = stats.norm.ppf(1-0.05/2)
	low_z = r_z - z*se 
	high_z = r_z + z*se
	low, high = np.tanh((low_z, high_z))
	
	return low, high

#3.2.  Main function for generating the output data dataframe
def pvalues_generate_output_df(mod_raw_data_df):
	output_df = mod_raw_data_df.copy()

	return output_df

#-----------------------------------------------------------4. Saving data----------------------------------------------------
#4.1. Helper functions for saving data - all not just function-specific ones
alignment_top = Alignment(horizontal="center", vertical="top")
alignment_center = Alignment(horizontal="center", vertical="center")
font_title = Font(size=20, bold=True)
font_header = Font(italic=True)
font_bold = Font(bold=True)
border_APA = Side(border_style="medium", color="000000")

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

def add_table_notes(ws, table_notes, adjusted_pvalues_threshold=None):
	if correction_type != "":
		table_notes.append("Multiple tests correction applied to p values: {c}".format(c=list(global_vars.master_dict.keys())[list(global_vars.master_dict.values()).index(correction_type)]))
		if output_pvalues_type == "adjusted":
			table_notes.append("Adjusted p values used; significant at {alpha}".format(alpha=alpha_threshold))
		elif output_pvalues_type == "original":
			table_notes.append("Original p values used; significant at {alpha}".format(alpha=adjusted_pvalues_threshold))
		
	for note in table_notes:
		ws.append([note])

def save_file(output_name, wb):
	time_now = datetime.now().strftime("%H%M%S-%Y%m%d")
	filename = output_filename + time_now + ".xlsx"
	wb.save(filename=filename)

#4.2.  Main function for saving data
def pvalues_table(mod_raw_data_df, output_df):
	wb = Workbook()
	ws = wb.active

	for row in dataframe_to_rows(output_df, index=False, header=True):
		ws.append(row)

	for row in range(1, len(output_df)+2):
		for cell in ws[row]:
			cell.alignment = alignment_center

	for cell in ws[1]:
		cell.font = font_bold

	for cell in ws[1] + ws[len(output_df)+1]:
		cell.border = Border(bottom=border_APA)

	add_table_notes(ws, [])

	save_file("pvalues", wb)


raw_data_df = get_raw_data_df()
mod_raw_data_df = modify_raw_data_df(raw_data_df)
output_df = generate_output_df(mod_raw_data_df)
output_df = multitest_correction(output_df)
save_output(mod_raw_data_df, output_df)