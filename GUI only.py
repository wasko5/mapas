from Calculations_only import *
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory

#-------------------------------------------------------------2. GUI----------------------------------------------------------------
master = Tk()
master.title("Multi-test corrections & APA table Software (MAPAS)")
master.resizable(False, False)

#-----------------2.1. Variable and Frame declaration
input_type_tk = StringVar()

raw_test_tk = StringVar()
raw_corr_type_tk = StringVar()
raw_mr_outcomevar_tk = StringVar()
raw_indttest_groupvar_tk = StringVar()
raw_pairttest_pairOne_tk = StringVar()
raw_pairttest_pairTwo_tk = StringVar()
raw_pairttest_pairThree_tk = StringVar()
raw_pairttest_pairFour_tk = StringVar()
raw_pairttest_pairFive_tk = StringVar()
raw_pairttest_pairSix_tk = StringVar()
raw_pairttest_pairSeven_tk = StringVar()

summ_corr_varOne_tk = StringVar()
summ_corr_varTwo_tk = StringVar()
summ_corr_coeff_tk = StringVar()
summ_indttest_var_tk = StringVar()
summ_indttest_meanOne_tk = StringVar()
summ_indttest_sdOne_tk = StringVar()
summ_indttest_nOne_tk = StringVar()
summ_indttest_meanTwo_tk = StringVar()
summ_indttest_sdTwo_tk = StringVar()
summ_indttest_nTwo_tk = StringVar()
summ_indttest_equal_var_tk = StringVar()

spss_test_tk = StringVar()
spss_indttest_nOne_tk = StringVar() #sample sizes are StringVar for optimal UI (leaves it blank on load); int() is later called
spss_indttest_nTwo_tk = StringVar()
spss_indttest_groupOneLabel_tk = StringVar()
spss_indttest_groupTwoLabel_tk = StringVar()
spss_pairttest_nOne_tk = StringVar()
spss_pairttest_nTwo_tk = StringVar()

effect_size_choice_tk = StringVar()
correction_type_tk = StringVar()

non_numeric_input_raise_errors_tk = BooleanVar()
output_pvalues_type_tk = StringVar()
raw_ttest_output_descriptives_tk = BooleanVar()

input_filename_tk = StringVar()
input_fileext_tk = StringVar()
alpha_threshold_tk = StringVar()
output_dir_tk = StringVar()

#resets variables to default but does not include input variables or alpha as it is used in functions below
def set_variables_default():
	raw_test_tk.set(0)
	raw_corr_type_tk.set(0)
	raw_mr_outcomevar_tk.set("")
	raw_indttest_groupvar_tk.set("")
	raw_pairttest_pairOne_tk.set("")
	raw_pairttest_pairTwo_tk.set("")
	raw_pairttest_pairThree_tk.set("")
	raw_pairttest_pairFour_tk.set("")
	raw_pairttest_pairFive_tk.set("")
	raw_pairttest_pairSix_tk.set("")
	raw_pairttest_pairSeven_tk.set("")

	summ_corr_varOne_tk.set("")
	summ_corr_varTwo_tk.set("")
	summ_corr_coeff_tk.set("")

	summ_indttest_var_tk.set("")
	summ_indttest_meanOne_tk.set("")
	summ_indttest_sdOne_tk.set("")
	summ_indttest_nOne_tk.set("")
	summ_indttest_meanTwo_tk.set("")
	summ_indttest_sdTwo_tk.set("")
	summ_indttest_nTwo_tk.set("")
	summ_indttest_equal_var_tk.set("")

	spss_test_tk.set(0)
	spss_indttest_nOne_tk.set("")
	spss_indttest_nTwo_tk.set("")
	spss_indttest_groupOneLabel_tk.set("")
	spss_indttest_groupTwoLabel_tk.set("")
	spss_pairttest_nOne_tk.set("")
	spss_pairttest_nTwo_tk.set("")

	effect_size_choice_tk.set(0)
	correction_type_tk.set(0)

	raw_ttest_output_descriptives_tk.set(False)
	non_numeric_input_raise_errors_tk.set(True)
	output_pvalues_type_tk.set("adjusted")

	output_dir_tk.set("")

#set all variables to default at start
input_type_tk.set(0)
input_filename_tk.set("")
input_fileext_tk.set("")
alpha_threshold_tk.set("0.05")
set_variables_default()

input_type_Frame = Frame(master)
input_type_Frame.grid(row=1,column=0,rowspan=13)

raw_test_Frame = Frame(master)
raw_corr_Frame = Frame(master)
raw_mr_Frame = Frame(master)
raw_indttest_Frame = Frame(master)
raw_pairttest_Frame = Frame(master)

summ_corr_varNames_Frame = Frame(master)

summ_indttest_cols_Frame = Frame(master)

spss_test_tk_Frame = Frame(master)
spss_indttest_Frame = Frame(master)
spss_pairttest_Frame = Frame(master)

effect_size_Frame = Frame(master)
correction_type_Frame = Frame(master)

raw_ttest_output_descriptives_Frame = Frame(master)
non_numeric_input_raise_errors_Frame = Frame(master)
pvalues_type_Frame = Frame(master)

#-----------------2.2. Layout control
def remove_frames(frames_list):
	for frame in frames_list:
		frame.grid_remove()

def input_type_frames_layout():

	#the only frames it does not include are master or input_type
	frames_list = [raw_test_Frame, raw_corr_Frame, raw_mr_Frame, raw_indttest_Frame, raw_pairttest_Frame,
					summ_corr_varNames_Frame, summ_indttest_cols_Frame, spss_test_tk_Frame, spss_indttest_Frame,
					spss_pairttest_Frame, effect_size_Frame, correction_type_Frame, raw_ttest_output_descriptives_Frame, 
					non_numeric_input_raise_errors_Frame, pvalues_type_Frame]

	set_variables_default()
	remove_frames(frames_list)

	if input_type_tk.get() == "pvalues":
		correction_type_Frame.grid(row=1, column=1, rowspan=13)
	else:
		if input_type_tk.get() == "raw":
			raw_test_Frame.grid(row=1, column=1, rowspan=5)
		elif input_type_tk.get() == "summ_corr":
			summ_corr_varNames_Frame.grid(row=1, column=1, rowspan=13)
		elif input_type_tk.get() == "summ_indttest":
			summ_indttest_cols_Frame.grid(row=1,column=1, rowspan=8)
			effect_size_Frame.grid(row=9, column=1, rowspan=5, sticky=W)
			pvalues_type_Frame.grid(row=1, column=3, rowspan=5, sticky=W)
		elif input_type_tk.get() == "spss":
			spss_test_tk_Frame.grid(row=1, column=1, rowspan=5)

		correction_type_Frame.grid(row=1, column=2, rowspan=13)

def raw_test_clear_vars():
	raw_corr_type_tk.set(0)
	raw_mr_outcomevar_tk.set("")
	raw_indttest_groupvar_tk.set("")
	raw_pairttest_pairOne_tk.set("")
	raw_pairttest_pairTwo_tk.set("")
	raw_pairttest_pairThree_tk.set("")
	raw_pairttest_pairFour_tk.set("")
	raw_pairttest_pairFive_tk.set("")
	raw_pairttest_pairSix_tk.set("")
	raw_pairttest_pairSeven_tk.set("")
	effect_size_choice_tk.set(0)
	raw_ttest_output_descriptives_tk.set(False)
	non_numeric_input_raise_errors_tk.set(True)
	output_pvalues_type_tk.set("adjusted")

def raw_test_frames_layout():
	frames_list = [raw_corr_Frame, raw_mr_Frame, raw_indttest_Frame, raw_pairttest_Frame, effect_size_Frame, 
					correction_type_Frame, raw_ttest_output_descriptives_Frame, non_numeric_input_raise_errors_Frame, 
					pvalues_type_Frame]

	raw_test_clear_vars()
	remove_frames(frames_list)

	if raw_test_tk.get() == "mr":
		correction_type_tk.set(0)
		raw_mr_Frame.grid(row=6, column=1, rowspan=2, sticky=W)
		non_numeric_input_raise_errors_Frame.grid(row=1, column=3, rowspan=3, sticky=W)
	else:
		if raw_test_tk.get() == "corr":
			raw_corr_Frame.grid(row=6, column=1, rowspan=4, sticky=W)
			non_numeric_input_raise_errors_Frame.grid(row=1, column=3, rowspan=3, sticky=W)
		elif raw_test_tk.get() == "indttest":
			raw_indttest_Frame.grid(row=6, column=1, rowspan=2, sticky=W)
			effect_size_Frame.grid(row=8, column=1, rowspan=5, sticky=W)
			pvalues_type_Frame.grid(row=1, column=3, rowspan=5, sticky=W)
			non_numeric_input_raise_errors_Frame.grid(row=6, column=3, rowspan=3, sticky=W)
			raw_ttest_output_descriptives_Frame.grid(row=9, column=3, rowspan=3, sticky=W)
		elif raw_test_tk.get() == "pairttest":
			raw_pairttest_Frame.grid(row=6, column=1, rowspan=8, sticky=W)
			effect_size_Frame.grid(row=14, column=1, rowspan=5, sticky=W)
			pvalues_type_Frame.grid(row=1, column=3, rowspan=5, sticky=W)
			non_numeric_input_raise_errors_Frame.grid(row=6, column=3, rowspan=3, sticky=W)
			raw_ttest_output_descriptives_Frame.grid(row=9, column=3, rowspan=3, sticky=W)
		correction_type_Frame.grid(row=1, column=2, rowspan=13, sticky=W)

def spss_test_tk_clear_vars():
	spss_indttest_nOne_tk.set("")
	spss_indttest_nTwo_tk.set("")
	spss_indttest_groupOneLabel_tk.set("")
	spss_indttest_groupTwoLabel_tk.set("")
	spss_pairttest_nOne_tk.set("")
	spss_pairttest_nTwo_tk.set("")
	output_pvalues_type_tk.set("adjusted")

def spss_test_tk_frames_layout():

	frames_list = [spss_indttest_Frame, spss_pairttest_Frame, effect_size_Frame, correction_type_Frame, pvalues_type_Frame]

	spss_test_tk_clear_vars()
	remove_frames(frames_list)

	if spss_test_tk.get() == "mr":
		correction_type_tk.set(0)
	else:
		if spss_test_tk.get() == "corr":
			pass
		elif spss_test_tk.get() == "indttest":
			spss_indttest_Frame.grid(row=6, column=1, rowspan=6, sticky=W)
			effect_size_Frame.grid(row=12, column=1, sticky=W)
			pvalues_type_Frame.grid(row=1, column=3, rowspan=13, sticky=W)
		elif spss_test_tk.get() == "pairttest":
			spss_pairttest_Frame.grid(row=6, column=1, rowspan=3, sticky=W)
			effect_size_Frame.grid(row=9, column=1, sticky=W)
			pvalues_type_Frame.grid(row=1, column=3, rowspan=13, stick=W)
		correction_type_Frame.grid(row=1, column=2, rowspan=13)


#-----------------2.3. GUI Content
#Instructions
instr_label = Label(master, text="Welcome to this software which allows you to apply\nmultiple tests corrections to various data inputs and produce beautiful APA tables.\n\nFor guidance on how to use the software, please see the documentation at:\nwww.nikolaybpetrov.com/software\n\nIf you need help, experience an error, or have feedback, please contact us at:\nnp5473j@greenwich.ac.uk\nI aim to reply within 48 hours.\n")
instr_label.grid(row=0, column=0, columnspan=4)

#Input Type
Label(input_type_Frame, text="First, please select the type of your input:").grid(row=0, sticky=W)
input_type_Dict = {"Raw data" : "raw", "Correlations from\nsummary statistics" : "summ_corr", 
					"Independent t-test\nfrom summary statistics" : "summ_indttest", "SPSS table" : "spss",
					"P values" : "pvalues"}
i_input = 1 #used for rows in the grid
for (text, value) in input_type_Dict.items(): 
		Radiobutton(input_type_Frame, text=text, variable=input_type_tk, value=value, command=input_type_frames_layout).grid(row=i_input,sticky=W)
		i_input += 1

#Raw data // test
Label(raw_test_Frame, text="Select the test you would like to perform:").grid(row=0, sticky=W)
raw_test_Dict = {"Correlations" : "corr", "(Multiple) Regression - Standard" : "mr",
					 "Independent Samples t-test" : "indttest", "Paired samples t-test" : "pairttest"}
i_raw_test = 1 #used for rows in the grid
for (text, value) in raw_test_Dict.items():
	Radiobutton(raw_test_Frame, text=text, variable=raw_test_tk, value=value, 
					command=raw_test_frames_layout).grid(row=i_raw_test,sticky=W)
	i_raw_test += 1 

#Raw data // test // correlations
Label(raw_corr_Frame, text="Select type of correlation").grid(row=0, sticky=W)
corr_type_Dict = {"Pearson's r" : "pearson", "Spearman's rho" : "spearman", "Kendall's tau": "kendall"}
i_corr = 1 #used for rows in the grid
for (text, value) in corr_type_Dict.items():
	Radiobutton(raw_corr_Frame, text=text, variable=raw_corr_type_tk, value=value).grid(row=i_corr,sticky=W)
	i_corr += 1

#Raw data // test // Multiple Regression
Label(raw_mr_Frame, text="Enter your outcome variable: ").grid(row=0, sticky=W)
Entry(raw_mr_Frame, textvariable=raw_mr_outcomevar_tk).grid(row=1,sticky=W)

#Raw data // test // Independent samples t-test
Label(raw_indttest_Frame, text="Enter your grouping variable: ").grid(row=0, sticky=W)
Entry(raw_indttest_Frame, textvariable=raw_indttest_groupvar_tk).grid(row=1,sticky=W)

#Raw data // test // Paired samples t-test
Label(raw_pairttest_Frame, text="Please enter your pair of variables.\nMust be COMMA separated.\nExample: foo1,foo2").grid(row=0, column=1, columnspan=2, sticky=W)
for ind, var in enumerate([raw_pairttest_pairOne_tk, raw_pairttest_pairTwo_tk, raw_pairttest_pairThree_tk,
							raw_pairttest_pairFour_tk, raw_pairttest_pairFive_tk, raw_pairttest_pairSix_tk,
							raw_pairttest_pairSeven_tk]):
	Label(raw_pairttest_Frame, text="Pair {}:".format(ind+1)).grid(row=ind+1, column=1, sticky=W)
	Entry(raw_pairttest_Frame, textvariable=var).grid(row=ind+1, column=2, sticky=W)

#Summary statistics - Correlations
Label(summ_corr_varNames_Frame, text="Enter column label of\nvariable 1:").grid(row=0, sticky=W)
Entry(summ_corr_varNames_Frame, textvariable=summ_corr_varOne_tk).grid(row=1,sticky=W)
Label(summ_corr_varNames_Frame, text="Enter column label of\nvariable 2:").grid(row=3, sticky=W)
Entry(summ_corr_varNames_Frame, textvariable=summ_corr_varTwo_tk).grid(row=4,sticky=W)
Label(summ_corr_varNames_Frame, text="Enter column label of\ncorrelation coefficient:").grid(row=5, sticky=W)
Entry(summ_corr_varNames_Frame, textvariable=summ_corr_coeff_tk).grid(row=6,sticky=W)
Label(summ_corr_varNames_Frame, text="Please remember that\nthe pvalues column\nmust be called \"pvalues\"").grid(row=7, sticky=W)

#Summary statistics - Independent samples t-test
Label(summ_indttest_cols_Frame, text="Please enter the column labels of your summary statistics.").grid(row=0, column=0, columnspan=2, sticky=W)
Label(summ_indttest_cols_Frame, text="Variable:").grid(row=1, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_var_tk).grid(row=1, column=1, sticky=W)
Label(summ_indttest_cols_Frame, text="Mean, Group 1").grid(row=2, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_meanOne_tk).grid(row=2, column=1, sticky=W)
Label(summ_indttest_cols_Frame, text="Std Div, Group 1").grid(row=3, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_sdOne_tk).grid(row=3, column=1, sticky=W)
Label(summ_indttest_cols_Frame, text="N, Group 1").grid(row=4, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_nOne_tk).grid(row=4, column=1, sticky=W)
Label(summ_indttest_cols_Frame, text="Mean, Group 2").grid(row=5, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_meanTwo_tk).grid(row=5, column=1, sticky=W)
Label(summ_indttest_cols_Frame, text="Std Div, Group 2").grid(row=6, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_sdTwo_tk).grid(row=6, column=1, sticky=W)
Label(summ_indttest_cols_Frame, text="N, Group 2").grid(row=7, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_nTwo_tk).grid(row=7, column=1, sticky=W)
Label(summ_indttest_cols_Frame, text="Equal Variances").grid(row=8, column=0, sticky=W)
Entry(summ_indttest_cols_Frame, textvariable=summ_indttest_equal_var_tk).grid(row=8, column=1, sticky=W)

#SPSS // test
Label(spss_test_tk_Frame, text="Select the type of your SPSS table").grid(row=0, sticky=W)
spss_test_tk_Dict = {"Correlations" : "corr", "(Multiple) Regression - Standard" : "mr",
					 "Independent Samples t-test" : "indttest", "Paired samples t-test" : "pairttest"}
i_spss_test_tk = 1 #used for rows in the grid
for (text, value) in spss_test_tk_Dict.items():
	Radiobutton(spss_test_tk_Frame, text=text, variable=spss_test_tk, value=value,
					command=spss_test_tk_frames_layout).grid(row=i_spss_test_tk, sticky=W)
	i_spss_test_tk += 1 

#SPSS // test // Independent samples t-test
Label(spss_indttest_Frame, text="Please enter your sample size:").grid(row=0, column=0, columnspan=2, sticky=W)
Label(spss_indttest_Frame, text="n, Group 1:").grid(row=1, column=0, sticky=W)
Entry(spss_indttest_Frame, textvariable=spss_indttest_nOne_tk).grid(row=1, column=1, sticky=W)
Label(spss_indttest_Frame, text="n, Group 2:").grid(row=2, column=0, sticky=W)
Entry(spss_indttest_Frame, textvariable=spss_indttest_nTwo_tk).grid(row=2, column=1, sticky=W)
Label(spss_indttest_Frame, text="Please enter group labels (optional):").grid(row=3, column=0, columnspan=2, sticky=W)
Label(spss_indttest_Frame, text="Group 1 label").grid(row=4, column=0, sticky=W)
Entry(spss_indttest_Frame, textvariable=spss_indttest_groupOneLabel_tk).grid(row=4, column=1, sticky=W)
Label(spss_indttest_Frame, text="Group 2 label").grid(row=5, column=0, sticky=W)
Entry(spss_indttest_Frame, textvariable=spss_indttest_groupTwoLabel_tk).grid(row=5, column=1, sticky=W)

#SPSS // test // Paired samples t-test
Label(spss_pairttest_Frame, text="Please enter your sample size:").grid(row=0, column=0, columnspan=2, sticky=W)
Label(spss_pairttest_Frame, text="n, Group 1:").grid(row=1, column=0, sticky=W)
Entry(spss_pairttest_Frame, textvariable=spss_pairttest_nOne_tk).grid(row=1, column=1, sticky=W)
Label(spss_pairttest_Frame, text="n, Group 2:").grid(row=2, column=0, sticky=W)
Entry(spss_pairttest_Frame, textvariable=spss_pairttest_nTwo_tk).grid(row=2, column=1, sticky=W)

#Effect size choice
Label(effect_size_Frame, text="Select effect size").grid(row=0, sticky=W)
effect_size_choice_Dict = {"Cohen's d" : "Cohen's d", "Hedge's g" : "Hedge's g", "Glass's delta" : "Glass's delta", "None" : 0}
i_effect = 1 #used for rows in the grid
for (text, value) in effect_size_choice_Dict.items():
	Radiobutton(effect_size_Frame, text=text, variable=effect_size_choice_tk, value=value).grid(row=i_effect, sticky=W)
	i_effect += 1

#Correction type choice
Label(correction_type_Frame, text="Select type of correction").grid(row=0, sticky=W)
correction_type_Dict = {"Bonferroni" : "bonferroni",  "Sidak" : "sidak", "Holm-Sidak" : "holm-sidak", 
						"Holm-Bonferroni" : "holm", "Simes-\nHochberg" : "simes-hochberg", "Hommel" : "hommel", 
						"Benjamini-Hochberg" : "fdr_bh", "Benjamini-Yekutieli" : "fdr_by", 
						"Benjamini-Hochberg (2-stage\nnon-negative correction) " : "fdr_tsbh", 
						"Benjamini-Yekutieli (2-stage\nnon-negative correction)" : "fdr_tsbky", "None" : 0}
i_correction = 1 #used for rows in the grid
for (text, value) in correction_type_Dict.items():
	Radiobutton(correction_type_Frame, text=text, variable=correction_type_tk, value=value).grid(row=i_correction, sticky=W)
	i_correction += 1

#Pvalues choice
Label(pvalues_type_Frame, text="Please select which pvalues to report.\nOriginal pvalues can only be reported for\nBonferroni and Sidak corrections.").grid(row=0, sticky=W)
Radiobutton(pvalues_type_Frame, text="original pvalues", variable=output_pvalues_type_tk, value="original").grid(row=1, sticky=W)
Radiobutton(pvalues_type_Frame, text="adjusted pvalues", variable=output_pvalues_type_tk, value="adjusted").grid(row=2, sticky=W)

#Raise errors on non-numeric input choice
Label(non_numeric_input_raise_errors_Frame, text="Please select how to handle non-numerical input.").grid(row=0, sticky=W)
Radiobutton(non_numeric_input_raise_errors_Frame, text="Raise errors if non-numerical input is found.", variable=non_numeric_input_raise_errors_tk, value=True).grid(row=1, sticky=W)
Radiobutton(non_numeric_input_raise_errors_Frame, text="Ignore non-numerical input case-wise.", variable=non_numeric_input_raise_errors_tk, value=False).grid(row=2, sticky=W)

#Output descriptives for Raw t-tests
Label(raw_ttest_output_descriptives_Frame, text="Would you like an additional spreadsheet with descriptive statistics?").grid(row=0, sticky=W)
Radiobutton(raw_ttest_output_descriptives_Frame, text="Yes", variable=raw_ttest_output_descriptives_tk, value=True).grid(row=1, sticky=W)
Radiobutton(raw_ttest_output_descriptives_Frame, text="No", variable=raw_ttest_output_descriptives_tk, value=False).grid(row=2, sticky=W)

#Input file button & label
def select_file():
	filename = askopenfilename(title="Select input file. Must be Excel file.", filetypes=(("Excel files","*.xlsx"),("All files","*.*")))
	sep_idx = filename.rfind(".")
	
	if filename[sep_idx:] == ".xlsx": # or filename[sep_idx:] == ".csv" - for later use when csv is integrated
		input_filename_tk.set(filename[:sep_idx])
		input_fileext_tk.set(filename[sep_idx:])
		filename_label.config(text=filename)
	elif filename != "":
		messagebox.showerror("Error!", "Please select a valid file - XLSX only.")

Button(master, text="Select input file (xlsx only)", command=select_file).grid(row=20, column=0, sticky=W)
filename_label = Label(master, text="No file selected.")
filename_label.grid(row=20, column=1, columnspan=3, sticky=W)

#Output directory button & label
def select_output_dir_tk():
	output_dir_tk.set(askdirectory(title="Select output directory. Filename will be generated  automatically."))

	if output_dir_tk.get() != "":
		output_dir_tk_label.config(text=output_dir_tk.get())

Button(master, text="Select output directory\n(filename generated automatically)", command=select_output_dir_tk).grid(row=21, column=0, sticky=W)
output_dir_tk_label = Label(master, text="No directory selected.")
output_dir_tk_label.grid(row=21, column=1, columnspan=3, sticky=W)

#Alpha threshold
Label(master, text="Enter Alpha threshold level: ").grid(row=22, column=0, sticky=W)
Entry(master, textvariable=alpha_threshold_tk).grid(row=22, column=1, sticky=W)

#-----------------2.4. On Submit functions
def set_global_variables():
	#the variables are duplicated (tkinter variables end in _tk) as otherwise if submit is clicked but an Exception is raised
	#(i.e. wrong input) then this modifies the state of the variables and confuses the UI. By splitting the variables,
	#I otimize UI by being able to control the behaviour of the tkinter variables separately to the variables in the data
	#trasnformation functions. Such split also allows me to work with more sensible values in the data transformation functions
	#see below comment.
	global input_type

	global raw_test
	global raw_corr_type
	global raw_mr_outcomevar
	global raw_indttest_groupvar
	global raw_pairttest_inputVars_list

	global summ_corr_varOne
	global summ_corr_varTwo
	global summ_corr_coeff
	global summ_indttest_var
	global summ_indttest_meanOne
	global summ_indttest_sdOne
	global summ_indttest_nOne
	global summ_indttest_meanTwo
	global summ_indttest_sdTwo
	global summ_indttest_nTwo
	global summ_indttest_equal_var

	global spss_test
	global spss_indttest_nOne
	global spss_indttest_nTwo
	global spss_indttest_groupOneLabel
	global spss_indttest_groupTwoLabel
	global spss_pairttest_nOne
	global spss_pairttest_nTwo

	global effect_size_choice
	global correction_type

	global raw_ttest_output_descriptives
	global non_numeric_input_raise_errors
	global output_pvalues_type
	
	global input_filename
	global input_fileext
	global alpha_threshold
	global output_dir

	#the if-else statements below solve the following problem: The default state of the _tk variables is set for optimal UI
	#(radiobuttons set to 0 despite encoding for string as otherwise they all appear selected on load OR numbers (sample sizes) 
	#set to "" so that the field is blank). When using them in code they are set to more sensible values ("" for str and -1 for missing int).
	input_type = input_type_tk.get()

	raw_test = "" if raw_test_tk.get() == "0" else raw_test_tk.get()
	raw_corr_type = "" if raw_corr_type_tk.get() == "0" else raw_corr_type_tk.get()
	raw_mr_outcomevar = raw_mr_outcomevar_tk.get()
	raw_indttest_groupvar = raw_indttest_groupvar_tk.get()
	if raw_test == "pairttest":
		def get_raw_pairttest_inputVars_list(*args):
			result_arr = []
			for ind, pair in enumerate(args):
				comma_ind_arr = [i for i, char in enumerate(pair) if char == ',']
				if len(comma_ind_arr) > 1:
					raise Exception("More than one comma found in Pair {ind}: {pair}.\nPlease enter the two variables as a pair with a single comma separating them.".format(ind=ind+1, pair=pair))
				if pair != "":
					pair_arr = [x.strip() for x in pair.split(',')]
					result_arr.append((pair_arr[0], pair_arr[1]))
			return result_arr
		raw_pairttest_inputVars_list = get_raw_pairttest_inputVars_list(raw_pairttest_pairOne_tk.get(), raw_pairttest_pairTwo_tk.get(), raw_pairttest_pairThree_tk.get(), raw_pairttest_pairFour_tk.get(), raw_pairttest_pairFive_tk.get(), raw_pairttest_pairSix_tk.get(), raw_pairttest_pairSeven_tk.get())
	else:
		raw_pairttest_inputVars_list = [""]

	summ_corr_varOne = summ_corr_varOne_tk.get()
	summ_corr_varTwo = summ_corr_varTwo_tk.get()
	summ_corr_coeff = summ_corr_coeff_tk.get()
	summ_indttest_var = summ_indttest_var_tk.get()
	summ_indttest_meanOne = summ_indttest_meanOne_tk.get()
	summ_indttest_sdOne = summ_indttest_sdOne_tk.get()
	summ_indttest_nOne = summ_indttest_nOne_tk.get()
	summ_indttest_meanTwo = summ_indttest_meanTwo_tk.get()
	summ_indttest_sdTwo = summ_indttest_sdTwo_tk.get()
	summ_indttest_nTwo = summ_indttest_nTwo_tk.get()
	summ_indttest_equal_var = summ_indttest_equal_var_tk.get()

	spss_test = "" if spss_test_tk.get() == "0" else spss_test_tk.get()
	spss_indttest_groupOneLabel = spss_indttest_groupOneLabel_tk.get()
	spss_indttest_groupTwoLabel = spss_indttest_groupTwoLabel_tk.get()
	if spss_test == "indttest":
		spss_indttest_groupOneLabel = "Group1" if spss_indttest_groupOneLabel == "" else spss_indttest_groupOneLabel
		spss_indttest_groupTwoLabel = "Group2" if spss_indttest_groupTwoLabel == "" else spss_indttest_groupTwoLabel
	try:
		spss_indttest_nOne = -1 if spss_indttest_nOne_tk.get() == "" else int(spss_indttest_nOne_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_indttest_nOne_tk.get()))
	try:
		spss_indttest_nTwo = -1 if spss_indttest_nTwo_tk.get() == "" else int(spss_indttest_nTwo_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_indttest_nTwo_tk.get()))
	try:
		spss_pairttest_nOne = -1 if spss_pairttest_nOne_tk.get() == "" else int(spss_pairttest_nOne_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_pairttest_nOne_tk.get()))
	try:
		spss_pairttest_nTwo = -1 if spss_pairttest_nTwo_tk.get() == "" else int(spss_pairttest_nTwo_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_pairttest_nTwo_tk.get()))
	
	effect_size_choice = "" if effect_size_choice_tk.get() == "0" else effect_size_choice_tk.get()
	correction_type = "" if correction_type_tk.get() == "0" else correction_type_tk.get()

	raw_ttest_output_descriptives = raw_ttest_output_descriptives_tk.get()
	non_numeric_input_raise_errors = non_numeric_input_raise_errors_tk.get()
	output_pvalues_type = "" if output_pvalues_type_tk.get() == "0" else output_pvalues_type_tk.get()

	input_filename = input_filename_tk.get()
	input_fileext = input_fileext_tk.get()
	try:
		alpha_threshold = float(alpha_threshold_tk.get())
	except:
		raise Exception("Could not set an alpha of \'{}\'. Please enter a valid number. Example: 0.05 or 0.01".format(alpha_threshold_tk.get()))
	output_dir = output_dir_tk.get()

	
	print("input_type", input_type)

	print("raw_test", raw_test)
	print("raw_corr_type", raw_corr_type)
	print("raw_mr_outcomevar", raw_mr_outcomevar)
	print("raw_indttest_groupvar", raw_indttest_groupvar)
	print("raw_pairttest_inputVars_list", raw_pairttest_inputVars_list)

	print("summ_corr_varOne", summ_corr_varOne)
	print("summ_corr_varTwo", summ_corr_varTwo)
	print("summ_corr_coeff", summ_corr_coeff)
	print("summ_indttest_var", summ_indttest_var)
	print("summ_indttest_meanOne", summ_indttest_meanOne)
	print("summ_indttest_sdOne", summ_indttest_sdOne)
	print("summ_indttest_nOne", summ_indttest_nOne)
	print("summ_indttest_meanTwo", summ_indttest_meanTwo)
	print("summ_indttest_sdTwo", summ_indttest_sdTwo)
	print("summ_indttest_nTwo", summ_indttest_nTwo)
	print("summ_indttest_equal_var", summ_indttest_equal_var)

	print("spss_test", spss_test)
	print("spss_indttest_nOne", spss_indttest_nOne)
	print("spss_indttest_nTwo", spss_indttest_nTwo)
	print("spss_indttest_groupOneLabel", spss_indttest_groupOneLabel)
	print("spss_indttest_groupTwoLabel", spss_indttest_groupTwoLabel)
	print("spss_pairttest_nOne", spss_pairttest_nOne)
	print("spss_pairttest_nTwo", spss_pairttest_nTwo)

	print("effect_size_choice", effect_size_choice)
	print("correction_type", correction_type)

	print("raw_ttest_output_descriptives", raw_ttest_output_descriptives)
	print("non_numeric_input_raise_errors", non_numeric_input_raise_errors)
	print("output_pvalues_type", output_pvalues_type)

	print("input_filename", input_filename)
	print("input_fileext", input_fileext)
	print("alpha_threshold", alpha_threshold)
	print("output_dir", output_dir)
	

def input_validation():
	if input_type == "":
		raise Exception("Please select the type of input of your data.")
	if input_type == "raw":
		if raw_test == "":
			raise Exception("Please select a statistical test you would like to perform on your data.")
		elif raw_test == "corr" and raw_corr_type == "":
			raise Exception("Please select the type of correlation you would like to perform.")
		elif raw_test == "mr" and raw_mr_outcomevar == "":
			raise Exception("Please enter the name of your outcome variable. This will be the at the bottom of your SPSS.")
		elif raw_test == "indttest" and raw_indttest_groupvar == "":
			raise Exception("Please enter the name of your grouping variable.")
		elif raw_test == "pairttest" and raw_pairttest_inputVars_list == [""]:
			raise Exception("Please enter your variable pairs.")
	elif input_type == "summ_corr":
		if summ_corr_varOne == "":
			raise Exception("Please enter the name of the column that contains the first set of variables.")
		if summ_corr_varTwo == "":
			raise Exception("Please enter the name of the column that contains the second set of variables.")
		if summ_corr_coeff == "":
			raise Exception("Please enter the name of the column that contains the correlation coefficient values.")
	elif input_type == "summ_indttest":
		if summ_indttest_var == "":
			raise Exception("Please enter the name of the column that contains the variable names.")
		if summ_indttest_meanOne == "":
			raise Exception("Please enter the name of the column that contains the values for the means of group 1.")
		if summ_indttest_sdOne == "":
			raise Exception("Please enter the name of the column that contains the values for the standard deviations for group 1.")
		if summ_indttest_nOne == "":
			raise Exception("Please enter the name of the column that contains the values for the sample size for group 1.")
		if summ_indttest_meanTwo == "":
			raise Exception("Please enter the name of the column that contains the values for the means for group 2.")
		if summ_indttest_sdTwo == "":
			raise Exception("Please enter the name of the column that contains the values for the standard deviations for group 2.")
		if summ_indttest_nTwo == "":
			raise Exception("Please enter the name of the column that contains the values for the sample size for group 2.")
		if summ_indttest_equal_var == "":
			raise Exception("Please enter the name of the column that contains the TRUE/FALSE values whether the equal variances assumption is met.")
	elif input_type == "spss":
		if spss_test == "":
			raise Exception("Please select the test you performed on your data.")
		if spss_test == "indttest" and (spss_indttest_nOne == -1 or spss_indttest_nTwo == -1):
			raise Exception("Please enter the sample sizes of your groups.")
		if spss_test == "pairttest" and (spss_pairttest_nOne == -1 or spss_pairttest_nTwo == -1):
			raise Exception("Please enter the sample sizes of your groups.")
	

	if effect_size_choice == "Glass's delta" and (input_type == "summindttest" or spss_test == "indttest" or spss_test == "pairttest"):
		raise Exception("Sorry! Glass's delta is not available for this time of test. Glass's delta can only be requested if raw data is provided. For more information, see the documentation.")
	if output_pvalues_type == "original" and (correction_type != "bonferroni" and correction_type != "sidak"):
		raise Exception("Original p values can only be requested if the multiple tests correction is either Boneforroni or Sidak. For more information, see the documentation.")
	if input_filename == "":
		raise Exception("Please provide an input file.")
	if output_dir == "":
		raise Exception("Please provide an output directory.")

	if effect_size_choice == "" and (raw_test == "indttest" or raw_test == "pairttest" or spss_test == "indttest" or spss_test == "pairttest" or input_type == "summ_indttest"):
		raise Exception("Unfortunately, as this software is still in beta version, you need to select an effect size to add to your APA table.\n\nFeel free to select any effect size and delete the column in the produced output if not needed.")

	if input_type == "pvalues" and correction_type == "":
		raise Exception("In order to use the p values input option, please select a correction type.")

def submit():
	#try:
	set_global_variables()
	input_validation()
	raw_data_df = get_raw_data_df()
	mod_raw_data_df = modify_raw_data_df(raw_data_df)
	output_df = generate_output_df(mod_raw_data_df)
	if spss_test != "mr":
		output_df = multitest_correction(output_df)
	save_output(mod_raw_data_df, output_df)
	#print("Success")
	master.destroy()
	final_message()
	#except Exception as error_msg:
		#messagebox.showerror("Oopsie!", error_msg)
	
Button(master, text="Submit", command=submit).grid(row=23, column=0, columnspan=4)

#---------GUI 2
def final_message():
	
	def center(win):
		"""
		centers a tkinter window
		:param win: the root or Toplevel window to center
		"""
		win.update_idletasks()
		width = win.winfo_width()
		frm_width = win.winfo_rootx() - win.winfo_x()
		win_width = width + 2 * frm_width
		height = win.winfo_height()
		titlebar_height = win.winfo_rooty() - win.winfo_y()
		win_height = height + titlebar_height + frm_width
		x = win.winfo_screenwidth() // 2 - win_width // 2
		y = win.winfo_screenheight() // 2 - win_height // 2
		win.geometry("{}x{}+{}+{}".format(width, height, x, y))
		win.deiconify()
	
	master2 = Tk()
	master2.title("Thanks!")
	final_message = "Thanks for using this software. If you have experienced any troubles using the software or have any feedback, please email us at np5473j@greenwich.ac.uk.\n\nPlease use the following reference for any of your work:\nPetrov, N., Thompson, T., & Atanasov, V. (2020). The Devil is in the Details: An Open‐source Software for Multiple Tests Corrections and APA tables. Manuscript in preparation."
	Label(master2, text=final_message).pack()
	center(master2)
	master2.mainloop()

master.mainloop()