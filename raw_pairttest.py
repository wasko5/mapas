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

#-----------------------------------------------------------0. Input----------------------------------------------------
#TESTING ONLY
'''
global_vars.input_path_and_filename = "Input files\\raw data\\input_raw_pairedTtest.xlsx"
#input_fileext = ""
global_vars.alpha_threshold = 0.05
global_vars.output_filename = "Test outputs\\output_raw_pairttest" #this does not end in .xlsx just for testing; in real app it should end with .xlsx (reason: function will add random numbers to prevent overwriting)

global_vars.input_type = "raw"

global_vars.raw_test = "pairttest"

#raw_corr_type = ""
#raw_mr_outcomevar = ""
#raw_mr_predictors = ""
#raw_indttest_groupvar = ""
#raw_indttest_dv = ""
global_vars.raw_pairttest_var_pairs = [["Bar1", "Bar2"], ["Foo1", "Foo2"], ["Baz1", "Baz2"]] #currently not used but to be used ASAP

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

global_vars.effect_size_choice = "Cohen's d" #could also be "Hedge's g", "Glass's delta" or blank/none (no idea which one it was)
global_vars.correction_type = "bonferroni" #see global_vars.master_dict for other values

global_vars.non_numeric_input_raise_errors = True #or False
global_vars.raw_ttest_output_descriptives = True
'''

#-----------------------------------------------------------1. Main flow----------------------------------------------------
#Note that the execution of the main flow is at the bottom
def get_raw_data_df():
	if global_vars.input_path_and_filename.endswith(".xlsx"):
		try:
			raw_data_df = pd.read_excel(global_vars.input_path_and_filename)
		except:
			raise Exception("Oh-oh. For some reason we cannot read the provided file. Please try another file - make sure it's an excel spreadsheet.")

	#raw_data_df.to_excel("Progress dataframes\\raw_indttest\\raw_data_df.xlsx")

	return raw_data_df

def modify_raw_data_df(raw_data_df):
	#if global_vars.raw_test == "pairttest":
	#	helper_funcs.raw_input_pairttest_colNames_check(raw_data_df)
	numeric_cols = list(np.array(global_vars.raw_pairttest_var_pairs).flatten())
	if global_vars.non_numeric_input_raise_errors == True:
		helper_funcs.error_on_input(df=raw_data_df, cols=numeric_cols, input_type="numeric")
	
	mod_raw_data_df = raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols)

	#mod_raw_data_df.to_excel("Progress dataframes\\raw_pairttest\\mod_raw_data_df.xlsx")

	return mod_raw_data_df

def generate_output_df(mod_raw_data_df):
	output_df = raw_pairttest_generate_output_df(mod_raw_data_df)

	#output_df.to_excel("Progress dataframes\\raw_pairttest\\output_df.xlsx")

	return output_df

def save_output(mod_raw_data_df, output_df):
	raw_pairttest_apa_table(mod_raw_data_df, output_df)
	if global_vars.raw_ttest_output_descriptives == True:
		raw_pairttest_descriptives_table(mod_raw_data_df, output_df)

#-----------------------------------------------------------2. Modified raw data dataframe----------------------------------------------------
#2.1.  Main function for generating the modified raw data dataframe
def raw_input_generate_mod_raw_data_df(raw_data_df, numeric_cols):
	#Treaing paired ttest input separately (as separate dataframes based on pairs) as it's possible for 1 pair 
	#to have 200 entires and another one with 400 entries
	df_list = []
	for pair in global_vars.raw_pairttest_var_pairs:
		df = raw_data_df[[pair[0], pair[1]]]
		df = df.apply(pd.to_numeric, errors="coerce").dropna().reset_index(drop=True) #dropna fine here as there is only 1 comparison between 2 vars
		df_list.append(df)
	mod_raw_data_df = pd.concat(df_list, axis=1)
	
	return mod_raw_data_df

#-----------------------------------------------------------3. Output dataframe----------------------------------------------------
#3.2.  Main function for generating the output data dataframe
def raw_pairttest_generate_output_df(mod_raw_data_df):
	effect_size_df_row_lookup = {"Cohen's d": 6, "Hedge's g": 7, "Glass's delta": 8}
	dictionaries_list=[]

	for pair in global_vars.raw_pairttest_var_pairs:
		series_time1 = mod_raw_data_df[pair[0]].dropna() #dropna needed here as the merging of 2 dataframes with 200 and 400 cols would have generated 200 np.nan rows
		series_time2 = mod_raw_data_df[pair[1]].dropna()

		#-----------------------------------------------------------!!!!!!Assumes equal var for now as not equal var outputs a single df w/o descriptives stats!!!!!
		result = rp.ttest(series_time1, series_time2, group1_name=pair[0], group2_name=pair[1], equal_variances=True, paired=True)
		ttest_stats_df1 = result[0]
		ttest_stats_df2 = result[1]

		current_dict={}
		current_dict["Variable"] = "{var1} - {var2}".format(var1=pair[0], var2=pair[1])
		current_dict["Time1_N"] = int(ttest_stats_df1[ttest_stats_df1["Variable"] == pair[0]].iloc[0]["N"])
		current_dict["Time1_Mean"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[0]].iloc[0]["Mean"]
		current_dict["Time1_SD"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[0]].iloc[0]["SD"]
		current_dict["Time1_Std Err"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[0]].iloc[0]["SE"]
		current_dict["Time1_95% CI_Low"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[0]].iloc[0]["95% Conf."]
		current_dict["Time1_95% CI_High"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[0]].iloc[0]["Interval"]
		current_dict["Time2_N"] = int(ttest_stats_df1[ttest_stats_df1["Variable"] == pair[1]].iloc[0]["N"])
		current_dict["Time2_Mean"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[1]].iloc[0]["Mean"]
		current_dict["Time2_SD"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[1]].iloc[0]["SD"]
		current_dict["Time2_Std Err"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[1]].iloc[0]["SE"]
		current_dict["Time2_95% CI_Low"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[1]].iloc[0]["95% Conf."]
		current_dict["Time2_95% CI_High"] = ttest_stats_df1[ttest_stats_df1["Variable"] == pair[1]].iloc[0]["Interval"]
		current_dict["Equal Variances Assumed"] = "Yes" if stats.levene(series_time1,series_time2)[1]>0.05 else "No"
		current_dict["Degrees of Freedom"] = ttest_stats_df2.iloc[1, 1]
		current_dict["t"] = ttest_stats_df2.iloc[2, 1]
		current_dict[global_vars.effect_size_choice] = np.nan if global_vars.effect_size_choice == "none" else ttest_stats_df2.iloc[effect_size_df_row_lookup[global_vars.effect_size_choice], 1]
		current_dict["pvalues"] = ttest_stats_df2.iloc[3, 1]
		dictionaries_list.append(current_dict)

	output_df = pd.DataFrame(dictionaries_list)

	return output_df
		

#-----------------------------------------------------------4. Saving data----------------------------------------------------
#4.2.  Main function for saving data
def raw_pairttest_apa_table(mod_raw_data_df, output_df):
	apa_output_df = output_df[["Variable", "Time1_Mean", "Time1_SD", "Time2_Mean", "Time2_SD", "Degrees of Freedom", "t", global_vars.effect_size_choice, "adjusted_pvalues"]]

	pd.options.mode.chained_assignment = None
	apa_output_df[list(apa_output_df.columns)[1:-1]] = apa_output_df[list(apa_output_df.columns)[1:-1]].applymap(lambda x: "{:.2f}".format(x))

	apa_output_df["adjusted_pvalues"] = apa_output_df["adjusted_pvalues"].map(helper_funcs.pvalue_formatting)
	pd.options.mode.chained_assignment = "warn"

	wb = Workbook()
	ws = wb.active
	
	ws.cell(row=1, column=1).value = "Variable"
	ws.merge_cells("A1:A2")
	ws.cell(row=1, column=1).font = global_vars.font_header
	
	ws.cell(row=1, column=2).value = "Time 1"
	ws.merge_cells("B1:C1")
	
	ws.cell(row=1, column=4).value = "Time 2"
	ws.merge_cells("D1:E1")
	
	ws.cell(row=1, column=6).value = "df"
	ws.merge_cells("F1:F2")
	ws.cell(row=1, column=6).font = global_vars.font_header
	
	ws.cell(row=1, column=7).value = "t"
	ws.merge_cells("G1:G2")
	ws.cell(row=1, column=7).font = global_vars.font_header
	
	ws.cell(row=1, column=8).value = global_vars.effect_size_choice
	ws.merge_cells("H1:H2")
	ws.cell(row=1, column=8).font = global_vars.font_header
	
	ws.cell(row=1, column=9).value = "p"
	ws.merge_cells("I1:I2")
	ws.cell(row=1, column=9).font = global_vars.font_header
	
	for col in range(2,5,2):
		ws.cell(row=2, column=col).value = "M"
		ws.cell(row=2, column=col).font = global_vars.font_header
		ws.cell(row=2, column=col+1).value = "SD"
		ws.cell(row=2, column=col+1).font = global_vars.font_header
	
	for row in dataframe_to_rows(apa_output_df, index=False, header=False):
		ws.append(row)

	for row in range(1, len(apa_output_df)+3):
		for cell in ws[row]:
			cell.alignment = global_vars.alignment_center
	
	for cell in ws[2] + ws[len(apa_output_df)+2]:
		cell.border = Border(bottom=global_vars.border_APA)

	for cell in ws[1]:
		cell.border = Border(top=global_vars.border_APA)

	if global_vars.effect_size_choice == "none":
		ws.delete_cols(8)

	helper_funcs.add_table_notes(ws, [])

	helper_funcs.save_file("raw_data_pairttest", wb)

def raw_pairttest_descriptives_table(mod_raw_data_df, output_df):
	if global_vars.correction_type == "none":
		output_df.drop(columns = ["adjusted_pvalues", list(output_df.columns)[-1]], inplace=True)

	descriptive_stats_df = output_df[list(output_df.columns)[0:13]]
	test_stats_df = output_df[list(output_df.columns)[0:1] + list(output_df.columns)[13:]]

	pd.options.mode.chained_assignment = None
	if global_vars.effect_size_choice == "none":
		test_stats_df.drop(columns = [global_vars.effect_size_choice], inplace=True)
	pd.options.mode.chained_assignment = "warn"

	wb = Workbook()
	ws = wb.active

	ws.cell(row=1, column=1).value = "Descriptives"
	ws.cell(row=1, column=1).font = global_vars.font_title
	ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(descriptive_stats_df.columns))

	for row in dataframe_to_rows(descriptive_stats_df, index=False, header=True):
		ws.append(row)

	ws.cell(row=len(descriptive_stats_df)+5,column=1).value = "Test Statistics"
	ws.cell(row=len(descriptive_stats_df)+5,column=1).font = global_vars.font_title
	ws.merge_cells(start_row=len(descriptive_stats_df)+5, start_column=1,
				   end_row=len(descriptive_stats_df)+5, end_column=len(test_stats_df.columns))
	
	for row in dataframe_to_rows(test_stats_df, index=False, header=True):
		ws.append(row)

	for cell in ws[2] + ws[len(test_stats_df)+6]:
		cell.font = global_vars.font_header
		
	for row in range(1, len(descriptive_stats_df) + len(test_stats_df) + 7):
		for cell in ws[row]:
			cell.alignment = global_vars.alignment_center

	helper_funcs.save_file("raw_data_pairttest_descriptives", wb)

def main():
	raw_data_df = get_raw_data_df()
	mod_raw_data_df = modify_raw_data_df(raw_data_df)
	output_df = generate_output_df(mod_raw_data_df)
	output_df = helper_funcs.multitest_correction(output_df)
	save_output(mod_raw_data_df, output_df)