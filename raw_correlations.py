#df = pd.read_excel("Input files\\raw data\\input_raw_correlations.xlsx")
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

#Temporary
correction_type_Dict = {"Bonferroni" : "bonferroni",  "Sidak" : "sidak", "Holm-Sidak" : "holm-sidak", 
						"Holm-Bonferroni" : "holm", "Simes-\nHochberg" : "simes-hochberg", "Hommel" : "hommel", 
						"Benjamini-Hochberg" : "fdr_bh", "Benjamini-Yekutieli" : "fdr_by", 
						"Benjamini-Hochberg (2-stage\nnon-negative correction) " : "fdr_tsbh", 
						"Benjamini-Yekutieli (2-stage\nnon-negative correction)" : "fdr_tsbky", "None" : 0}

output_pvalues_type = ""

#-----------------------------------------------------------0. Input----------------------------------------------------
#Commented out variables would either not be used or are considered for removal
input_filename = "Input files\\raw data\\input_raw_correlations.xlsx"
#input_fileext = ""
alpha_threshold = 0.05
output_filename = "Output files for testing\\test" #this does not end in .xlsx just for testing; in real app it should end with .xlsx (reason: function will add random numbers to prevent overwriting)

input_type = "raw"

raw_test = "corr"

raw_corr_type = "pearson" #could be "spearman" or "kendall"
#raw_mr_outcomevar = ""
#raw_indttest_groupvar = ""
#raw_pairttest_var1 = ""
#raw_pairttest_var2 = ""

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

#effect_size_choice = ""
correction_type = "fdr_bh" #see global_vars.master_dict for other values

non_numeric_input_raise_errors = True #or False
#raw_ttest_output_descriptives = ""


#-----------------------------------------------------------1. Main flow----------------------------------------------------
#Note that the execution of the main flow is at the bottom
def get_raw_data_df():
	raw_data_df = pd.read_excel(input_filename, sheet_name=0)

	return raw_data_df

def modify_raw_data_df(raw_data_df):
	numeric_cols = get_numeric_cols(raw_data_df)
	if non_numeric_input_raise_errors == True:
		error_on_non_numeric_input(raw_data_df, numeric_cols)
	
	mod_raw_data_df = raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols)

	return mod_raw_data_df

def generate_output_df(mod_raw_data_df):
	output_df = raw_corr_generate_output_df(mod_raw_data_df)

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
	raw_corr_apa_table(mod_raw_data_df, output_df)

#-----------------------------------------------------------2. Modified raw data dataframe----------------------------------------------------
#2.1.  Helper functions fo generating modified raw data dataframes
def get_numeric_cols(raw_data_df):
	numeric_cols = list(raw_data_df.columns)

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

#2.1.  Main function for generating the modified raw data dataframe
def raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols):
	mod_raw_data_df = raw_data_df.copy()
	mod_raw_data_df[numeric_cols] = mod_raw_data_df[numeric_cols].apply(pd.to_numeric, errors="coerce")
	mod_raw_data_df = mod_raw_data_df.dropna().reset_index(drop=True)

	return mod_raw_data_df

#-----------------------------------------------------------3. Output dataframe----------------------------------------------------
#3.1. Helper functions for generating output dataframes
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

#3.2.  Main function for generating the output  data dataframe
def raw_corr_generate_output_df(mod_raw_data_df):
	data_list = []

	i=0
	for var1 in mod_raw_data_df.columns:
		for var2 in mod_raw_data_df.columns[i:]:
			if not var1 == var2:
				r, p = raw_input_corr_coeff(mod_raw_data_df[var1],mod_raw_data_df[var2])
				ci_low, ci_high = corr_coeff_ci(r, n=mod_raw_data_df[var1].count())
				data_list.append((var1, var2, r, ci_low, ci_high, p))
		i += 1
	output_df = pd.DataFrame(data_list, columns=["Variable1", "Variable2", "Correlation Coefficient", "CI_low", "CI_high", "pvalues"])

	return output_df

#-----------------------------------------------------------4. Saving data----------------------------------------------------
#4.1. Helper functions for saving data
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
		table_notes.append("Multiple tests correction applied to p values: {c}".format(c=list(correction_type_Dict.keys())[list(correction_type_Dict.values()).index(correction_type)]))
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
def raw_corr_apa_table(mod_raw_data_df, output_df):
	wb = Workbook()
	ws = wb.active
	
	variables_list = list(mod_raw_data_df.columns)
	
	ws.append([""] + variables_list[:-1] + ["Mean", "SD"])
	ws["A2"] = variables_list[0]
	for ind,var in enumerate(variables_list[1:]):
		ws.cell(row=(ind*2)+3, column=1).value = var
	
	start_row = 3
	for col in range(2, len(variables_list)+3):
		col_var = ws.cell(row=1, column=col).value
		for row in range(start_row, len(variables_list)*2, 2):
			row_var = ws.cell(row=row, column=1).value
			#query method is slightly slower for smaller datasets
			r = output_df[((output_df["Variable1"]==row_var) & (output_df["Variable2"]==col_var)) | ((output_df["Variable1"]==col_var) & (output_df["Variable2"]==row_var))]["Correlation Coefficient"].item()
			p = output_df[((output_df["Variable1"]==row_var) & (output_df["Variable2"]==col_var)) | ((output_df["Variable1"]==col_var) & (output_df["Variable2"]==row_var))]["adjusted_pvalues"].item()
			ci_low = output_df[((output_df["Variable1"]==row_var) & (output_df["Variable2"]==col_var)) | ((output_df["Variable1"]==col_var) & (output_df["Variable2"]==row_var))]["CI_low"].item()
			ci_high = output_df[((output_df["Variable1"]==row_var) & (output_df["Variable2"]==col_var)) | ((output_df["Variable1"]==col_var) & (output_df["Variable2"]==row_var))]["CI_high"].item()
			#r = output_df.query("(Variable1 == @row_var and Variable2==@col_var) or (Variable1 == @col_var and Variable2==@row_var)")["Correlation Coefficient"].item()
			#p = output_df.query("(Variable1 == @row_var and Variable2==@col_var) or (Variable1 == @col_var and Variable2==@row_var)")["adjusted_pvalues"].item()
			#ci_low = output_df.query("(Variable1 == @row_var and Variable2==@col_var) or (Variable1 == @col_var and Variable2==@row_var)")["CI_low"].item()
			#ci_high = output_df.query("(Variable1 == @row_var and Variable2==@col_var) or (Variable1 == @col_var and Variable2==@row_var)")["CI_high"].item()
			r, ci_low, ci_high = correlations_format_val(r, p), correlations_format_val(ci_low), correlations_format_val(ci_high)
			ws.cell(row=row, column=col).value = r
			ws.cell(row=row+1, column=col).value = "[" + ci_low + ", " + ci_high + "]"
		start_row += 2
	
	ws.cell(row=2, column=len(variables_list)+1).value = "{:.2f}".format(mod_raw_data_df[variables_list[0]].mean(skipna=True))
	ws.cell(row=2, column=len(variables_list)+2).value = "{:.2f}".format(mod_raw_data_df[variables_list[0]].std(skipna=True))
	for row in range(3, len(variables_list)*2, 2):
		ws.cell(row=row, column=len(variables_list)+1).value = "{:.2f}".format(mod_raw_data_df[variables_list[int((row-1)/2)]].mean(skipna=True))
		ws.cell(row=row, column=len(variables_list)+2).value = "{:.2f}".format(mod_raw_data_df[variables_list[int((row-1)/2)]].std(skipna=True))    
	
	for row in range(3, len(variables_list)*2, 2):
		ws.merge_cells(start_row=row, start_column=1, end_row=row+1, end_column=1)
		ws.merge_cells(start_row=row, start_column=len(variables_list)+1, end_row=row+1, end_column=len(variables_list)+1)
		ws.merge_cells(start_row=row, start_column=len(variables_list)+2, end_row=row+1, end_column=len(variables_list)+2)
		
	for row in ws[1:len(variables_list)*2]:
		for cell in row:
			if cell.row > 2 and (cell.column == 1 or cell.column == len(variables_list)+1 or cell.column == len(variables_list)+2):
				cell.alignment = alignment_top
			else:
				cell.alignment = alignment_center
				
	for cell in ws[1]:
		cell.font = font_header
	
	ci_font = Font(size=9)
	for row in range(4, len(variables_list)*2+1, 2):
		for cell in ws[row]:
			cell.font = ci_font
	
	for cell in ws[1]:
		cell.border = Border(top=border_APA, bottom=border_APA)
	for cell in ws[len(variables_list)*2]:
		cell.border = Border(bottom = border_APA)
	
	table_notes = ["Note. M and SD represent mean and standard deviation, respectively. Values in square brackets indicate 95% confidence interval for the correlation coefficient."]
	table_notes.append("Correlation coefficient used: {}".format(raw_corr_type))
	table_notes.append("**p < 0.01")
	table_notes.append("*p < {}".format(alpha_threshold))
	add_table_notes(ws, table_notes) 
	
	save_file("raw_data_correlations", wb)


raw_data_df = get_raw_data_df()
mod_raw_data_df = modify_raw_data_df(raw_data_df)
output_df = generate_output_df(mod_raw_data_df)
output_df = multitest_correction(output_df)
save_output(mod_raw_data_df, output_df)