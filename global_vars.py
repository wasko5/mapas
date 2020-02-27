master_dict = {
	"Correlations" : "corr",
	"(Multiple) Regression - Standard" : "mr",
	"Independent Samples t-test" : "indttest",
	"Paired samples t-test" : "pairttest",

	"Raise errors" : True,
	"Ignore case-wise" : False,

	"Bonferroni" : "bonferroni",
	"Sidak" : "sidak",
	"Holm-Sidak" : "holm-sidak",
	"Holm-Bonferroni" : "holm",
	"Simes-\nHochberg" : "simes-hochberg",
	"Hommel" : "hommel",
	"Benjamini-Hochberg" : "fdr_bh",
	"Benjamini-Yekutieli" : "fdr_by",
	"Benjamini-Hochberg (2-stage\nnon-negative correction) " : "fdr_tsbh",
	"Benjamini-Yekutieli (2-stage\nnon-negative correction)" : "fdr_tsbky",
	"None" : ""
}

input_filename = ""
input_fileext = ""
alpha_threshold = ""
output_filename = ""

input_type = ""

raw_test = ""

raw_corr_type = ""
raw_mr_outcomevar = ""
raw_indttest_groupvar = ""
raw_pairttest_var1 = ""
raw_pairttest_var2 = ""

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
spss_pairttest_nOne = ""
spss_pairttest_nTwo = ""

effect_size_choice = ""
correction_type = ""

non_numeric_input_raise_errors = ""
raw_ttest_output_descriptives = ""