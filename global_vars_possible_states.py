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
import random
import string


input_path_and_filename_states = os.listdir(os.path.join(global_vars.unit_tests_directory, "APA_tables", "input dataframes"))
alpha_threshold_states = random.uniform(0.01, 0.1) 
output_filename_states = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
output_filetype_states = ["Excel", "Word"]
input_type_states = ["raw", "summ_corr", "summ_indttest", "spss", "pvalues"]
raw_test_states = ["corr", "mr", "indttest", "pairttest"]
raw_corr_type_states = ["pearson", "spearman", "kendall"]
raw_corr_vars_states = None
raw_corr_include_CI_states = [True, False]
raw_mr_outcomevar_states = None
raw_mr_predictors_states = None
raw_indttest_groupvar_states = None
raw_indttest_grouplevel1_states = None
raw_indttest_grouplevel2_states = None
raw_indttest_dv_states = None
raw_pairttest_var_pairs_states = None
summ_corr_varOne_states = None
summ_corr_varTwo_states = None
summ_corr_coeff_states = None
summ_corr_pvalues_states = None
summ_indttest_var_states = None
summ_indttest_meanOne_states = None
summ_indttest_sdOne_states = None
summ_indttest_nOne_states = None
summ_indttest_meanTwo_states = None
summ_indttest_sdTwo_states = None
summ_indttest_nTwo_states = None
summ_indttest_equal_var_states = None
spss_test_states = ["corr", "mr", "indttest", "pairttest"]
spss_indttest_nOne_states = random.uniform(1, 100)
spss_indttest_nTwo_states = random.uniform(1, 100)
spss_indttest_groupOneLabel_states = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
spss_indttest_groupTwoLabel_states = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
spss_pairttest_n_states = random.uniform(1, 100)
pvalues_col_states = None
effect_size_choice_states = ["Cohen's d", "Hedge's g", "Glass's delta", "None"]
correction_type_states = ["bonferroni",	"sidak", "holm-sidak", "holm", "simes-hochberg", "hommel", "fdr_bh", "fdr_by", "fdr_tsbh","fdr_tsbky", "None"]
non_numeric_input_raise_errors_states = [True, False]
corr_table_triangle_states = ["Upper triangle", "Lower triangle", "Both"]


'''
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
'''