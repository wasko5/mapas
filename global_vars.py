from openpyxl.styles import Border, Side, Alignment, Font

version = "BETA"

master_dict = {
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
	"alpha_threshold_tk" : "0.05",

	"raw_test_tk" : "Select a test...",

	"raw_corr_type_tk" : "Select a correlation...",
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

	"raw_ttest_output_descriptives_tk" : "No",
	"non_numeric_input_raise_errors_tk" : "Select error handling..."
}

dropdown_unselected_file_msg = "Please select input file first..."

input_path_and_filename = ""
alpha_threshold = ""
output_filename = ""

input_type = ""

raw_test = ""

raw_corr_type = ""
raw_corr_vars = ""
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

non_numeric_input_raise_errors = ""

alignment_top = Alignment(horizontal="center", vertical="top")
alignment_center = Alignment(horizontal="center", vertical="center")
font_title = Font(size=20, bold=True)
font_header = Font(italic=True)
font_bold = Font(bold=True)
border_APA = Side(border_style="medium", color="000000")