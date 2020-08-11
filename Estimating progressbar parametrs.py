import decision_funcs
import global_vars
import helper_funcs
import os

#temp for testing
from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Inches
import pandas as pd
import numpy as np

import time

iterations = 100

TESTS_APA_TABLES_INPUT_DATAFRAMES_FOLDER = os.path.join(global_vars.unit_tests_directory, "APA_tables", "input dataframes")

parameter_gather_global_vars_df = pd.read_csv("parameter gathering.csv", keep_default_na=False)

def str_to_arr(x, pairttest=False):
	x = x.replace("[","")
	x = x.replace("]", "")
	x = x.replace("'", "")
	x = x.replace(" ", "")
	x = x.split(",")
	if pairttest:
		x = [x[i:i+2] for i in range(0, len(x), 2)]
	return x

parameters_dict = {}

start_10_runs = time.time()
for row_ind in range(0, len(parameter_gather_global_vars_df)):
	row = parameter_gather_global_vars_df.loc[row_ind]
	
	global_vars.input_path_and_filename = os.path.join(TESTS_APA_TABLES_INPUT_DATAFRAMES_FOLDER, row[0])
	global_vars.alpha_threshold = row[1]
	global_vars.output_filename = "D:/Desktop_current/MUFOS/GitHub/a"
	global_vars.output_filetype = row[3]
	global_vars.input_type = row[4]
	global_vars.raw_test = row[5]
	global_vars.raw_corr_type = row[6]
	global_vars.raw_corr_vars = str_to_arr(row[7])
	global_vars.raw_corr_include_CI = row[8]
	global_vars.raw_mr_outcomevar = row[9]
	global_vars.raw_mr_predictors = str_to_arr(row[10])
	global_vars.raw_indttest_groupvar = row[11]
	global_vars.raw_indttest_grouplevel1 = row[12]
	global_vars.raw_indttest_grouplevel2 = row[13]
	global_vars.raw_indttest_dv = str_to_arr(row[14])
	global_vars.raw_pairttest_var_pairs = str_to_arr(row[15], pairttest=True)
	global_vars.summ_corr_varOne = row[16]
	global_vars.summ_corr_varTwo = row[17]
	global_vars.summ_corr_coeff = row[18]
	global_vars.summ_corr_pvalues = row[19]
	global_vars.summ_indttest_var = row[20]
	global_vars.summ_indttest_meanOne = row[21]
	global_vars.summ_indttest_sdOne = row[22]
	global_vars.summ_indttest_nOne = row[23]
	global_vars.summ_indttest_meanTwo = row[24]
	global_vars.summ_indttest_sdTwo = row[25]
	global_vars.summ_indttest_nTwo = row[26]
	global_vars.summ_indttest_equal_var = row[27]
	global_vars.spss_test = row[28]
	global_vars.spss_indttest_nOne = row[29]
	global_vars.spss_indttest_nTwo = row[30]
	global_vars.spss_indttest_groupOneLabel = row[31]
	global_vars.spss_indttest_groupTwoLabel = row[32]
	global_vars.spss_pairttest_n = row[33]
	global_vars.pvalues_col = row[34]
	global_vars.effect_size_choice = row[35]
	global_vars.correction_type = row[36]
	global_vars.non_numeric_input_raise_errors = row[37]
	global_vars.corr_table_triangle = row[38]

	curr_step_dict = {}
	curr_step_dict["Step 1"] = []
	curr_step_dict["Step 2"] = []
	curr_step_dict["Step 3"] = []
	curr_step_dict["Step 4"] = []
	curr_step_dict["Step 5"] = []

	for i in range(iterations):
		start_time = time.time()
		raw_data_df = decision_funcs.get_raw_data_df()
		raw_data_df_end_time = time.time()
		mod_raw_data_df = decision_funcs.modify_raw_data_df(raw_data_df)
		mod_raw_data_df_end_time = time.time()
		output_df = decision_funcs.generate_output_df(mod_raw_data_df)
		output_df_end_time = time.time()
		output_df = decision_funcs.multitest_correction(output_df)
		multitest_correction_end_time = time.time()
		decision_funcs.save_output(mod_raw_data_df, output_df)
		save_output_end_time = time.time()

		raw_data_df_duration = raw_data_df_end_time - start_time
		mod_raw_data_df_duration = mod_raw_data_df_end_time - raw_data_df_end_time
		output_df_duration = output_df_end_time - mod_raw_data_df_end_time
		multitest_correction_duration = multitest_correction_end_time - output_df_end_time
		save_output_duration = save_output_end_time - multitest_correction_end_time

		total_duration = save_output_end_time - start_time

		raw_data_df_prop = raw_data_df_duration / total_duration  * 100
		mod_raw_data_df_prop = mod_raw_data_df_duration / total_duration * 100
		output_df_prop = output_df_duration / total_duration * 100
		multitest_correction_prop = multitest_correction_duration / total_duration * 100
		save_output_prop = save_output_duration / total_duration * 100

		curr_step_dict["Step 1"].append(raw_data_df_prop)
		curr_step_dict["Step 2"].append(mod_raw_data_df_prop)
		curr_step_dict["Step 3"].append(output_df_prop)
		curr_step_dict["Step 4"].append(multitest_correction_prop)
		curr_step_dict["Step 5"].append(save_output_prop)

	key_lookup = "{it}_{rt}_{st}_{ot}".format(it=global_vars.input_type, rt=global_vars.raw_test, st=global_vars.spss_test, ot=global_vars.output_filetype)
	parameters_dict[key_lookup] = curr_step_dict

summary_estimates_df = pd.DataFrame(index=["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"])

for key, subdict in parameters_dict.items():
	for step, estimates in subdict.items():
		summary_estimates_df.loc[step, key] = np.mean(estimates)

summary_estimates_df.to_excel("summary_estaimtes_df_{} iterations.xlsx".format(iterations))
print("{} iterations for each variation took {:.2f} seconds to run".format(iterations, time.time() - start_10_runs))  



























'''
global_vars.input_path_and_filename = "D:/Desktop_current/MUFOS/GitHub/unit_testing/main_funcs/input dataframes/raw_correlations_tests.xlsx"
global_vars.alpha_threshold = 0.05
global_vars.output_filename = "D:/Desktop_current/MUFOS/GitHub/a"
global_vars.output_filetype = "Excel"
global_vars.input_type = "raw"
global_vars.raw_test = "corr"
global_vars.raw_corr_type = "pearson"
global_vars.raw_corr_vars = ["var1", "var2", "var3", "var4", "var5", "var6", "var7", "var8"]
global_vars.raw_corr_include_CI = True
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
global_vars.spss_test = ""
global_vars.spss_indttest_nOne = -1
global_vars.spss_indttest_nTwo = -1
global_vars.spss_indttest_groupOneLabel = "Group1"
global_vars.spss_indttest_groupTwoLabel = "Group2"
global_vars.spss_pairttest_n = -1
global_vars.pvalues_col = ""
global_vars.effect_size_choice = "no selection"
global_vars.correction_type = "fdr_bh"
global_vars.non_numeric_input_raise_errors = False
global_vars.corr_table_triangle = "Lower triangle"
'''