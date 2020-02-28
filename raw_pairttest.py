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
#more temporary - to use raw_pairttest_var_pairs ASAP
raw_pairttest_inputVars_list = [('Bar1', 'Bar2'), ('Foo1', 'Foo2'), ('Baz1', 'Baz2')]

#-----------------------------------------------------------0. Input----------------------------------------------------
#Commented out variables would either not be used or are considered for removal
input_filename = "Input files\\raw data\\input_raw_pairedTtest.xlsx"
#input_fileext = ""
alpha_threshold = 0.05
output_filename = "Output files for testing\\raw_pairttest_" #this does not end in .xlsx just for testing; in real app it should end with .xlsx (reason: function will add random numbers to prevent overwriting)

input_type = "raw"

raw_test = "pairttest"

#raw_corr_type = ""
#raw_mr_outcomevar = ""
#raw_mr_predictors = ""
#raw_indttest_groupvar = ""
#raw_indttest_dv = ""
raw_pairttest_var_pairs = "" #currently not used but to be used ASAP

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

effect_size_choice = "Cohen's d" #could also be "Hedge's g", "Glass's delta" or blank/none (no idea which one it was)
correction_type = "bonferroni" #see global_vars.master_dict for other values

non_numeric_input_raise_errors = True #or False
#raw_ttest_output_descriptives = ""


#-----------------------------------------------------------1. Main flow----------------------------------------------------
#Note that the execution of the main flow is at the bottom
def get_raw_data_df():
	raw_data_df = pd.read_excel(input_filename, sheet_name=0)

	raw_data_df.to_excel("Progress dataframes\\raw_pairttest\\raw_data_df.xlsx")

	return raw_data_df

def modify_raw_data_df(raw_data_df):
	if raw_test == "pairttest":
		raw_input_pairttest_colNames_check(raw_data_df)
	numeric_cols = get_numeric_cols(raw_data_df)
	if non_numeric_input_raise_errors == True:
		error_on_non_numeric_input(raw_data_df, numeric_cols)
	
	mod_raw_data_df = raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols)

	mod_raw_data_df.to_excel("Progress dataframes\\raw_pairttest\\mod_raw_data_df.xlsx")

	return mod_raw_data_df

def generate_output_df(mod_raw_data_df):
	output_df = raw_pairttest_generate_output_df(mod_raw_data_df)

	output_df.to_excel("Progress dataframes\\raw_pairttest\\output_df.xlsx")

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

	output_df.to_excel("Progress dataframes\\raw_pairttest\\output_df_corrections.xlsx")

	return output_df

def save_output(mod_raw_data_df, output_df):
	raw_pairttest_apa_table(mod_raw_data_df, output_df)

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
def raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols):
	if raw_test == "pairttest":
		#Treaing paired ttest input separately (as separate dataframes based on pairs) as it's possible for 1 pair 
		#to have 200 entires and another one with 400 entries
		df_list = []
		for var_time1, var_time2 in raw_pairttest_inputVars_list:
			df = raw_data_df[[var_time1, var_time2]]
			df = df.apply(pd.to_numeric, errors="coerce").dropna().reset_index(drop=True)
			df_list.append(df)
		mod_raw_data_df = pd.concat(df_list, axis=1)
	else:  
		mod_raw_data_df = raw_data_df.copy()
		mod_raw_data_df[numeric_cols] = mod_raw_data_df[numeric_cols].apply(pd.to_numeric, errors="coerce")
		mod_raw_data_df = mod_raw_data_df.dropna().reset_index(drop=True)
	
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
def raw_pairttest_generate_output_df(mod_raw_data_df):
	time1_n_list = []
	time1_mean_list = []
	time1_sd_list = []
	time1_se_list = []
	time1_ci_low_list = []
	time1_ci_high_list = []
	time2_n_list = []
	time2_mean_list = []
	time2_sd_list = []
	time2_se_list = []
	time2_ci_low_list = []
	time2_ci_high_list = []
	equal_var_list = []
	deg_free_list = []
	t_stat_list = []
	effectsize_list = []
	pvalues_list = []

	if effect_size_choice == "Cohen's d":
		effect_size_dfrow = 6
	elif effect_size_choice == "Hedge's g":
		effect_size_dfrow = 7
	elif effect_size_choice == "Glass's delta":
		effect_size_dfrow = 8

	for var_time1, var_time2 in raw_pairttest_inputVars_list:
		df_time1 = mod_raw_data_df[var_time1].dropna()
		df_time2 = mod_raw_data_df[var_time2].dropna()

		ttest_stats_df1 = rp.ttest(df_time1, df_time2, group1_name=var_time1, group2_name=var_time2, 
			 equal_variances=stats.levene(df_time1, df_time2)[1]>0.05, paired=True)[0]
		ttest_stats_df2 = rp.ttest(df_time1, df_time2, group1_name=var_time1, group2_name=var_time2, 
			 equal_variances=stats.levene(df_time1, df_time2)[1]>0.05, paired=True)[1]

		time1_n_list.append(int(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time1, "N"].item()))
		time1_mean_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time1, "Mean"].item())
		time1_sd_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time1, "SD"].item())
		time1_se_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time1, "SE"].item())
		time1_ci_low_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time1, "95% Conf."].item())
		time1_ci_high_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time1, "Interval"].item())
		time2_n_list.append(int(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time2, "N"].item()))
		time2_mean_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time2, "Mean"].item())
		time2_sd_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time2, "SD"].item())
		time2_se_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time2, "SE"].item())
		time2_ci_low_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time2, "95% Conf."].item())
		time2_ci_high_list.append(ttest_stats_df1.loc[ttest_stats_df1["Variable"] == var_time2, "Interval"].item())
		equal_var_list.append(stats.levene(df_time1, df_time2)[1]>0.05)
		deg_free_list.append(ttest_stats_df2.at[1,ttest_stats_df2.columns[1]])
		t_stat_list.append(ttest_stats_df2.at[2,ttest_stats_df2.columns[1]])
		effectsize_list.append(ttest_stats_df2.at[effect_size_dfrow,ttest_stats_df2.columns[1]])
		pvalues_list.append(ttest_stats_df2.at[3,ttest_stats_df2.columns[1]])

	output_df = pd.DataFrame()
	output_df["Variable"] = ["{var1} - {var2}".format(var1=x, var2=y) for x,y in raw_pairttest_inputVars_list]
	output_df["Time1_N"] = time1_n_list
	output_df["Time1_Mean"] = time1_mean_list
	output_df["Time1_SD"] = time1_sd_list
	output_df["Time1_Std Err"] = time1_se_list
	output_df["Time1_95% CI_Low"] = time1_ci_low_list
	output_df["Time1_95% CI_High"] = time1_ci_high_list
	output_df["Time2_N"] = time2_n_list
	output_df["Time2_Mean"] = time2_mean_list
	output_df["Time2_SD"] = time2_sd_list
	output_df["Time2_Std Err"] = time2_se_list
	output_df["Time2_95% CI_Low"] = time2_ci_low_list
	output_df["Time2_95% CI_High"] = time2_ci_high_list
	output_df["Equal Variances Assumed"] = equal_var_list
	output_df["Degrees of Freedom"] = deg_free_list
	output_df["t"] = t_stat_list
	output_df[effect_size_choice] = effectsize_list
	output_df["pvalues"] = pvalues_list

	output_df["Equal Variances Assumed"] = output_df["Equal Variances Assumed"].replace(True,'Yes')
	output_df["Equal Variances Assumed"] = output_df["Equal Variances Assumed"].replace(False,'No')

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
def raw_pairttest_apa_table(mod_raw_data_df, output_df):
	sign_bool_label = list(output_df.columns)[-1]
	
	apa_output_df = output_df[["Variable", "Time1_Mean", "Time1_SD", "Time2_Mean", "Time2_SD"] + list(output_df.columns)[14:-1]]

	if output_pvalues_type == "adjusted":
		adjusted_pvalues_threshold = None
		apa_output_df["pvalues"] = apa_output_df["adjusted_pvalues"]
	else:
		adjusted_pvalues_threshold = sign_bool_label[sign_bool_label.find("=")+2:]
	apa_output_df.drop(columns = ["adjusted_pvalues"], inplace=True)

	apa_output_df[list(apa_output_df.columns)[1:-1]] = apa_output_df[list(apa_output_df.columns)[1:-1]].applymap(lambda x: "{:.2f}".format(x))
	apa_output_df["pvalues"] = apa_output_df["pvalues"].map(pvalue_formatting)

	wb = Workbook()
	ws = wb.active
	
	ws.cell(row=1, column=1).value = "Variable"
	ws.merge_cells('A1:A2')
	ws.cell(row=1, column=1).font = font_header
	
	ws.cell(row=1, column=2).value = "Time 1"
	ws.merge_cells('B1:C1')
	
	ws.cell(row=1, column=4).value = "Time 2"
	ws.merge_cells('D1:E1')
	
	ws.cell(row=1, column=6).value = "df"
	ws.merge_cells('F1:F2')
	ws.cell(row=1, column=6).font = font_header
	
	ws.cell(row=1, column=7).value = "t"
	ws.merge_cells('G1:G2')
	ws.cell(row=1, column=7).font = font_header
	
	ws.cell(row=1, column=8).value = effect_size_choice
	ws.merge_cells('H1:H2')
	ws.cell(row=1, column=8).font = font_header
	
	ws.cell(row=1, column=9).value = "p"
	ws.merge_cells('I1:I2')
	ws.cell(row=1, column=9).font = font_header
	
	for col in range(2,5,2):
		ws.cell(row=2, column=col).value = "M"
		ws.cell(row=2, column=col).font = font_header
		ws.cell(row=2, column=col+1).value = "SD"
		ws.cell(row=2, column=col+1).font = font_header
	
	for row in dataframe_to_rows(apa_output_df, index=False, header=False):
		ws.append(row)

	for row in range(1, len(apa_output_df)+3):
		for cell in ws[row]:
			cell.alignment = alignment_center
	
	for cell in ws[2] + ws[len(apa_output_df)+2]:
		cell.border = Border(bottom=border_APA)

	for cell in ws[1]:
		cell.border = Border(top=border_APA)

	add_table_notes(ws, [], adjusted_pvalues_threshold)

	save_file("raw_data_pairttest", wb)


raw_data_df = get_raw_data_df()
mod_raw_data_df = modify_raw_data_df(raw_data_df)
output_df = generate_output_df(mod_raw_data_df)
output_df = multitest_correction(output_df)
save_output(mod_raw_data_df, output_df)