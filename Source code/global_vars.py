# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
from openpyxl.styles import Border, Side, Alignment, Font
import os

version = "1.0"
apa_reference = "Petrov, N., Atanasov, V., & Thompson, T. (2020). ..."
article_link = "www.nikolaybpetrov.com/mufos"
github_repository = "https://github.com/nikbpetrov/mufos.git"
software_page = "www.nikolaybpetrov.com/mufos"
contact = "nikbpetrov@gmail.com"

master_dict = {
	#used for translating longer names to shorter ones
	"Correlations" : "corr",
	"(Multiple) Regression - Standard" : "mr",
	"Independent Samples t-test" : "indttest",
	"Paired samples t-test" : "pairttest",

	"Pearson's r" : "pearson",
	"Spearman's rho" : "spearman",
	"Kendall's tau" : "kendall",

	"Raise errors" : True,
	"Ignore pair-wise" : False,

	"Bonferroni" : "bonferroni",
	"Sidak" : "sidak",
	"Holm-Sidak" : "holm-sidak",
	"Holm-Bonferroni" : "holm",
	"Simes-Hochberg" : "simes-hochberg",
	"Hommel" : "hommel",
	"Benjamini-Hochberg" : "fdr_bh",
	"Benjamini-Yekutieli" : "fdr_by",
	"Benjamini-Hochberg (2-stage)" : "fdr_tsbh",
	"Benjamini-Yekutieli (2-stage)" : "fdr_tsbky",
	"None" : "None"
}

tk_vars_defaults = {
	"input_type_tk" : "0",
	"input_path_and_filename_tk" : "",
	"output_filename_tk" : "",
	"output_filetype_tk" : "Excel",
	"alpha_threshold_tk" : "0.05",

	"raw_test_tk" : "Select a test...",

	"raw_corr_type_tk" : "Select a correlation...",
	"raw_corr_include_CI_tk" : 1, #checkbutton; set to 1 for UI but comes out as True/False
	"raw_mr_outcomevar_tk" : "Select outcome variable...",
	"raw_indttest_groupvar_tk" : "Select grouping variable...",
	"raw_indttest_grouplevel1_tk" : "Select Group 1",
	"raw_indttest_grouplevel2_tk" : "Select Group 2",
	"raw_pairttest_var1_tk" : "Select first variable...",
	"raw_pairttest_var2_tk" : "Select second variable...",

	"summ_corr_varOne_tk" : "Select var 1 column",
	"summ_corr_varTwo_tk" : "Select var 2 column",
	"summ_corr_coeff_tk" : "Select correlation coeff column",
	"summ_corr_pvalues_tk" : "Select p-values column",

	"summ_indttest_var_tk" : "",
	"summ_indttest_meanOne_tk" : "",
	"summ_indttest_sdOne_tk" : "",
	"summ_indttest_nOne_tk" : "",
	"summ_indttest_meanTwo_tk" : "",
	"summ_indttest_sdTwo_tk" : "",
	"summ_indttest_nTwo_tk" : "",
	"summ_indttest_equal_var_tk" : "",

	"spss_test_tk" : "Select a test...",

	"spss_indttest_nOne_tk" : "Enter an integer",
	"spss_indttest_nTwo_tk" : "Enter an integer",
	"spss_indttest_groupOneLabel_tk" : "",
	"spss_indttest_groupTwoLabel_tk" : "",
	"spss_pairttest_n_tk" : "Enter an integer",

	"pvalues_col_tk" : "Select p-values column",

	"effect_size_choice_tk" : "Select effect size...",
	"correction_type_tk" : "Select correction...",

	"non_numeric_input_raise_errors_tk" : "Ignore pair-wise",

	"corr_table_triangle_tk" : "Lower triangle"
}

dropdown_unselected_file_msg = "Please select input file first..."

input_path_and_filename = ""
alpha_threshold = ""
output_filename = ""
output_filetype = ""

input_type = ""

raw_test = ""

raw_corr_type = ""
raw_corr_vars = ""
raw_corr_include_CI = None
raw_mr_outcomevar = ""
raw_mr_predictors = ""
raw_indttest_groupvar = ""
raw_indttest_grouplevel1 = ""
raw_indttest_grouplevel2 = ""
raw_indttest_dv = ""
raw_pairttest_var_pairs = ""

summ_corr_varOne = ""
summ_corr_varTwo = ""
summ_corr_coeff = ""
summ_corr_pvalues = ""

summ_indttest_var = ""
summ_indttest_meanOne = ""
summ_indttest_sdOne = ""
summ_indttest_nOne = ""
summ_indttest_meanTwo = ""
summ_indttest_sdTwo = ""
summ_indttest_nTwo = ""
summ_indttest_equal_var = ""

spss_test = ""
spss_indttest_nOne = ""
spss_indttest_nTwo = ""
spss_indttest_groupOneLabel = ""
spss_indttest_groupTwoLabel = ""
spss_pairttest_n = ""

pvalues_col = ""

effect_size_choice = ""
correction_type = ""

non_numeric_input_raise_errors = None

corr_table_triangle = ""

alignment_top = Alignment(horizontal="center", vertical="top")
alignment_center = Alignment(horizontal="center", vertical="center")
font_title = Font(size=20, bold=True)
font_header = Font(italic=True)
font_bold = Font(bold=True)
border_APA = Side(border_style="medium", color="000000")
border_APA_word = {"sz": 12, "color": "000000", "val": "single"}

unit_tests_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit_testing")
TESTS_MAIN_FUNCS_INPUT_DATAFRAMES_FOLDER = os.path.join(unit_tests_directory, "main_funcs", "input dataframes")
TESTS_MAIN_FUNCS_OUTPUT_DATAFRAMES_FOLDER = os.path.join(unit_tests_directory, "main_funcs", "output dataframes")