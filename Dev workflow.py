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

global_vars.input_path_and_filename = "D:/Desktop_current/MAPAS/GitHub/unit_testing/main_funcs/input dataframes/spss_mr_tests_allStats.xlsx"
global_vars.alpha_threshold = 0.05
global_vars.output_filename = "D:/Desktop_current/MAPAS/GitHub/a"
global_vars.output_filetype = "Word"
global_vars.input_type = "spss"
global_vars.raw_test = ""
global_vars.raw_corr_type = ""
global_vars.raw_corr_vars = []
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
global_vars.spss_test = "mr"
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


def raw_mr_apa_table_excel(mod_raw_data_df, output_df):
	mod_output_df = output_df[["Variable","B","95% CI B","beta","t","adjusted_pvalues"]]

	pd.options.mode.chained_assignment = None
	mod_output_df[["B", "beta", "t"]] = mod_output_df[["B", "beta", "t"]].applymap(lambda x: "{:.2f}".format(x))

	mod_output_df["adjusted_pvalues"] = mod_output_df["adjusted_pvalues"].map(helper_funcs.pvalue_formatting)

	mod_output_df.rename(columns = {"95% CI B": "95% CI", "adjusted_pvalues": "p"}, inplace=True)
	mod_output_df.loc[0, "beta"] = "" #removes the beta value for constant as it is always 0

	wb = Workbook()
	ws = wb.active

	ws.append(list(mod_output_df.columns))

	for row in dataframe_to_rows(mod_output_df, index=False, header=False):
		ws.append(row)

	for cell in ws[1]:
		cell.font = global_vars.font_header

	for cell in ws[1] + ws[len(mod_output_df)+1]:
		cell.border = Border(top=global_vars.border_APA, bottom=global_vars.border_APA)
	for cell in ws[len(mod_output_df)+1]:
		cell.border = Border(bottom=global_vars.border_APA)

	for row in range(1, len(mod_output_df)+2):
		for cell in ws[row]:
			cell.alignment = global_vars.alignment_center

	table_notes = ["R squared adjusted = {R}".format(R="{:.2f}".format(output_df["R2adj"][0])), "Dependent Variable: {DV}".format(DV=global_vars.raw_mr_outcomevar)]
	helper_funcs.add_table_notes(ws, table_notes)

	helper_funcs.savefile(wb=wb)

raw_data_df = decision_funcs.get_raw_data_df()
mod_raw_data_df = decision_funcs.modify_raw_data_df(raw_data_df)
output_df = decision_funcs.generate_output_df(mod_raw_data_df)
output_df = decision_funcs.multitest_correction(output_df)
# raw_mr_apa_table_excel(mod_raw_data_df, output_df)
decision_funcs.save_output(mod_raw_data_df, output_df)

