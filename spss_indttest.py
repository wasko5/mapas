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
input_filename = "Input files\\spss\\input_spss_independentTtest.xlsx"
#input_fileext = ""
alpha_threshold = 0.05
output_filename = "Output files for testing\\spss_indttest_" #this does not end in .xlsx just for testing; in real app it should end with .xlsx (reason: function will add random numbers to prevent overwriting)

input_type = "spss"

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

spss_test = "indttest"
spss_indttest_nOne = 135
spss_indttest_nTwo = 125
spss_indttest_groupOneLabel = "G1"
spss_indttest_groupTwoLabel = "G2"
#spss_pairttest_nOne = ""
#spss_pairttest_nTwo = ""

effect_size_choice = "Cohen's d"
correction_type = "bonferroni" #see global_vars.master_dict for other values

non_numeric_input_raise_errors = True #or False
#raw_ttest_output_descriptives = ""


#-----------------------------------------------------------1. Main flow----------------------------------------------------
#Note that the execution of the main flow is at the bottom
def get_raw_data_df():
	raw_data_df = pd.read_excel(input_filename, sheet_name=0)

	raw_data_df.to_excel("Progress dataframes\\spss_indttest\\raw_data_df.xlsx")

	return raw_data_df

def modify_raw_data_df(raw_data_df):
	mod_raw_data_df = spss_indttest_generate_mod_raw_data_df(raw_data_df) #might remove the function depending on whether I add logical checks

	mod_raw_data_df.to_excel("Progress dataframes\\spss_indttest\\mod_raw_data_df.xlsx")

	return mod_raw_data_df

def generate_output_df(mod_raw_data_df):
	output_df = spss_indttest_generate_output_df(mod_raw_data_df)

	output_df.to_excel("Progress dataframes\\spss_indttest\\output_df.xlsx")

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

	output_df.to_excel("Progress dataframes\\spss_indttest\\output_df_corrections.xlsx")

	return output_df

def save_output(mod_raw_data_df, output_df):
	spss_indttest_apa_table(mod_raw_data_df, output_df)

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
def spss_indttest_generate_mod_raw_data_df(raw_data_df):
	mod_raw_data_df = raw_data_df.copy()

	#renaming columns as the multi-level formatting of the spss table makes it difficult to work with
	renaming_dict = {}
	new_col_names = list(mod_raw_data_df.columns[:2]) + list(mod_raw_data_df.iloc[1][2:-1]) + [mod_raw_data_df.columns[-1]]
	for i in range(0, len(mod_raw_data_df.columns)):
		renaming_dict[mod_raw_data_df.columns[i]] = new_col_names[i]

	mod_raw_data_df = mod_raw_data_df.rename(columns=renaming_dict).drop([mod_raw_data_df.index[0], mod_raw_data_df.index[1]]).reset_index(drop=True)
	
	if mod_raw_data_df.columns[0] != "Independent Samples Test":
		raise Exception("The SPSS table provided does not seem to be one from Independent Samples t-test. Please try with another file or refer to the documentation for help.")
	#if "Confidence Interval of the Difference" not in mod_raw_data_df.columns[9]:
	#	raise Exception("Confidence Intervals could not be read from the table. Please try with another file or refer to the instructions...")
	fields_to_check = ["F", "Sig.", "t", "df", "Sig. (2-tailed)"]
	for field in fields_to_check:
		if field not in mod_raw_data_df.columns:
			raise Exception("The column \'{}\' was not found in the file. Please try entering a correct data file. Please see the documentation for help.".format(field))

	return mod_raw_data_df

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
def spss_indttest_generate_output_df(mod_raw_data_df):
	variables_list = []
	levene_sig_list = []
	t_stat_list = []
	pvalues_list = []
	deg_free_list = []
	#ci_low_list = []
	#ci_high_list = []
	effectsize_list = []

	for row in range(1, len(mod_raw_data_df), 2):
		variables_list.append(mod_raw_data_df["Independent Samples Test"][row])
		levene_p = mod_raw_data_df["Sig."][row]
		if levene_p > 0.05:
			row_to_read = row
		else:
			row_to_read = row+1
		t = mod_raw_data_df["t"][row_to_read]
		t_stat_list.append(t)
		pvalues_list.append(mod_raw_data_df["Sig. (2-tailed)"][row_to_read])
		deg_free_list.append(mod_raw_data_df["df"][row_to_read])
		#ci_low_list.append(mod_raw_data_df[mod_raw_data_df.columns[9]][row_to_read])
		#ci_high_list.append(mod_raw_data_df[mod_raw_data_df.columns[10]][row_to_read])

		if effect_size_choice == "Cohen's d":
			effect_size = t*np.sqrt(1/spss_indttest_nOne + 1/spss_indttest_nTwo)
		elif effect_size_choice == "Hedge's g":
			#calculated using cohens_d * (1 - (3/4(n1+n2-9))) where cohens d is t*sqrt(1/n1 + 1/n2)
			effect_size = (t*np.sqrt(1/spss_indttest_nOne + 1/spss_indttest_nTwo))*np.sqrt(1/spss_indttest_nOne + 1/spss_indttest_nTwo)
		effectsize_list.append(effect_size)

	output_df = pd.DataFrame()
	output_df["Variable"] = variables_list
	output_df["All_Mean"] = [""] * len(output_df)
	output_df["All_SD"] = [""] * len(output_df)
	output_df[spss_indttest_groupOneLabel+"_Mean"] = [""] * len(output_df)
	output_df[spss_indttest_groupOneLabel+"_SD"] = [""] * len(output_df)
	output_df[spss_indttest_groupTwoLabel+"_Mean"] = [""] * len(output_df)
	output_df[spss_indttest_groupTwoLabel+"_SD"] = [""] * len(output_df)
	output_df["Degrees of Freedom"] = ["{:.2f}".format(x) for x in deg_free_list]
	output_df["t"] = ["{:.2f}".format(x) for x in t_stat_list]
	output_df[effect_size_choice] = ["{:.2f}".format(x) for x in effectsize_list]
	output_df["pvalues"] = pvalues_list

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
def spss_indttest_apa_table(mod_raw_data_df, output_df):
	apa_output_df = output_df.copy()

	if output_pvalues_type == "adjusted":
		adjusted_pvalues_threshold = None
		apa_output_df["pvalues"] = apa_output_df["adjusted_pvalues"]
	else:
		adjusted_pvalues_threshold = apa_output_df.columns[-1][apa_output_df.columns[-1].find("=")+2:]

	apa_output_df.drop(columns=apa_output_df.columns[-2:], inplace=True)

	apa_output_df["pvalues"] = apa_output_df["pvalues"].map(pvalue_formatting)

	wb = Workbook()
	ws = wb.active
	
	ws.cell(row=1, column=1).value = "Variable"
	ws.merge_cells('A1:A2')
	ws.cell(row=1, column=1).font = font_header
	
	ws.cell(row=1, column=2).value = "All, n=?"
	ws.merge_cells('B1:C1')
	
	ws.cell(row=1, column=4).value = "{}, n=?".format(spss_indttest_groupOneLabel)
	ws.merge_cells('D1:E1')
	
	ws.cell(row=1, column=6).value = "{}, n=?".format(spss_indttest_groupTwoLabel)
	ws.merge_cells('F1:G1')
	
	ws.cell(row=1, column=8).value = "df"
	ws.merge_cells('H1:H2')
	ws.cell(row=1, column=8).font = font_header
	
	ws.cell(row=1, column=9).value = "t"
	ws.merge_cells('I1:I2')
	ws.cell(row=1, column=9).font = font_header
	
	ws.cell(row=1, column=10).value = effect_size_choice
	ws.merge_cells('J1:J2')
	ws.cell(row=1, column=10).font = font_header
	
	ws.cell(row=1, column=11).value = "p"
	ws.merge_cells('K1:K2')
	ws.cell(row=1, column=11).font = font_header

	for col in range(2,7,2):
		ws.cell(row=2, column=col).value = "M"
		ws.cell(row=2, column=col).font = font_header
		ws.cell(row=2, column=col+1).value = "SD"
		ws.cell(row=2, column=col+1).font = font_header

	for row in dataframe_to_rows(apa_output_df, index=False, header=False):
		ws.append(row)

	for row in range(1, len(apa_output_df)+3):
		for cell in ws[row]:
			cell.alignment = alignment_center

	for cell in ws[1]:
		cell.border = Border(top=border_APA)
	for cell in ws[2] + ws[len(apa_output_df)+2]:
		cell.border = Border(bottom=border_APA)

	table_notes = ["Means and Standard Deviations could not be read from the SPSS table. Please add them yourself or remove those columns if they are not needed."]
	add_table_notes(ws, table_notes, adjusted_pvalues_threshold)

	save_file("spss_data_indttest", wb)


raw_data_df = get_raw_data_df()
mod_raw_data_df = modify_raw_data_df(raw_data_df)
output_df = generate_output_df(mod_raw_data_df)
if spss_test != "mr":
	output_df = multitest_correction(output_df)
save_output(mod_raw_data_df, output_df)