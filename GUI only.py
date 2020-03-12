'''
- One current 'feature' is that when you move between tests (correlations-mr in raw test) the things you put in the listbox (e.g. for MR) stay there despite clicking away.
			Might leave it like that for listboxes but reset for everything else. Might add a parameter to the reset_defaults function such that it can also
			reset to default these listboxes upon successful run of the program (i.e. when someone clicks "more analysis" in the popup)
'''

import raw_indttest
import raw_correlations
import raw_mr
import raw_indttest
import raw_pairttest
import summ_correlations
import summ_indttest
import spss_correlations
import spss_mr
import spss_indttest
import spss_pairttest
import pvalues


import global_vars
import calculations_helper_functions_only as helper_funcs
import tkinter as tk
from ttkthemes import themed_tk as thk #not needed if theme is not used
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from webbrowser import open_new
import time #temporary for testing

#-------------------------------------------------------------2. GUI----------------------------------------------------------------
#master = thk.ThemedTk()
#master.get_themes()
#master.set_theme("clearlooks")
master = tk.Tk()
master.title("MAPAS Rework")
master.resizable(False, False)


#---------------------------------------STYLING ATTEMPTS
#master.bind_class(className="TCombobox", sequence="<<ComboboxSelected>>", func=lambda e: master.focus())
#master.bind("<Button-1>", func=lambda e: master.focus()) #seems like a good idea to get rid of the blue highlighting of comboboxes when clicked outside, but does not let me type into the Entry boxes...
s = ttk.Style()
s.configure("TLabelframe", padding=5, borderwidth=3)
#s.configure("TCombobox", width=30)
#s.map("TCombobox", width=[("readonly", 30)])
#s.map("TCombobox", selectbackground=[("readonly", "black")])

#------------------------------------------------------------------------------

#-----------------2.1. Variable and Frame declaration
input_path_and_filename_tk = tk.StringVar()
alpha_threshold_tk = tk.StringVar()
output_filename_tk = tk.StringVar()

input_type_tk = tk.StringVar()

raw_test_tk = tk.StringVar()

raw_corr_type_tk = tk.StringVar()
raw_corr_vars_tk = tk.StringVar()
raw_mr_outcomevar_tk = tk.StringVar()
raw_indttest_groupvar_tk = tk.StringVar()
raw_pairttest_var1_tk = tk.StringVar()
raw_pairttest_var2_tk = tk.StringVar()

summ_corr_varOne_tk = tk.StringVar()
summ_corr_varTwo_tk = tk.StringVar()
summ_corr_coeff_tk = tk.StringVar()
summ_corr_pvalues_tk = tk.StringVar()

summ_indttest_var_tk = tk.StringVar()
summ_indttest_meanOne_tk = tk.StringVar()
summ_indttest_sdOne_tk = tk.StringVar()
summ_indttest_nOne_tk = tk.StringVar()
summ_indttest_meanTwo_tk = tk.StringVar()
summ_indttest_sdTwo_tk = tk.StringVar()
summ_indttest_nTwo_tk = tk.StringVar()
summ_indttest_equal_var_tk = tk.StringVar()

spss_test_tk = tk.StringVar()
spss_indttest_nOne_tk = tk.StringVar() #sample sizes are tk.StringVar for optimal UI (leaves it blank on load); int() is later called
spss_indttest_nTwo_tk = tk.StringVar()
spss_indttest_groupOneLabel_tk = tk.StringVar()
spss_indttest_groupTwoLabel_tk = tk.StringVar()
spss_pairttest_nOne_tk = tk.StringVar()
spss_pairttest_nTwo_tk = tk.StringVar()

effect_size_choice_tk = tk.StringVar()
correction_type_tk = tk.StringVar()

non_numeric_input_raise_errors_tk = tk.StringVar()
raw_ttest_output_descriptives_tk = tk.StringVar()

#resets variables to default but does not include input variables or alpha as it is used in functions below
def set_variables_default():
	raw_test_tk.set(global_vars.tk_vars_defaults["raw_test_tk"])

	raw_corr_type_tk.set(global_vars.tk_vars_defaults["raw_corr_type_tk"])
	raw_mr_outcomevar_tk.set(global_vars.tk_vars_defaults["raw_mr_outcomevar_tk"])
	raw_indttest_groupvar_tk.set(global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"])
	raw_pairttest_var1_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var1_tk"])
	raw_pairttest_var2_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var2_tk"])

	summ_corr_varOne_tk.set(global_vars.tk_vars_defaults["summ_corr_varOne_tk"])
	summ_corr_varTwo_tk.set(global_vars.tk_vars_defaults["summ_corr_varTwo_tk"])
	summ_corr_coeff_tk.set(global_vars.tk_vars_defaults["summ_corr_coeff_tk"])
	summ_corr_pvalues_tk.set(global_vars.tk_vars_defaults["summ_corr_pvalues_tk"])

	summ_indttest_var_tk.set(global_vars.tk_vars_defaults["summ_indttest_var_tk"])
	summ_indttest_meanOne_tk.set(global_vars.tk_vars_defaults["summ_indttest_meanOne_tk"])
	summ_indttest_sdOne_tk.set(global_vars.tk_vars_defaults["summ_indttest_sdOne_tk"])
	summ_indttest_nOne_tk.set(global_vars.tk_vars_defaults["summ_indttest_nOne_tk"])
	summ_indttest_meanTwo_tk.set(global_vars.tk_vars_defaults["summ_indttest_meanTwo_tk"])
	summ_indttest_sdTwo_tk.set(global_vars.tk_vars_defaults["summ_indttest_sdTwo_tk"])
	summ_indttest_nTwo_tk.set(global_vars.tk_vars_defaults["summ_indttest_nTwo_tk"])
	summ_indttest_equal_var_tk.set(global_vars.tk_vars_defaults["summ_indttest_equal_var_tk"])

	spss_test_tk.set(global_vars.tk_vars_defaults["spss_test_tk"])

	spss_indttest_nOne_tk.set(global_vars.tk_vars_defaults["spss_indttest_nOne_tk"])
	spss_indttest_nTwo_tk.set(global_vars.tk_vars_defaults["spss_indttest_nTwo_tk"])
	spss_indttest_groupOneLabel_tk.set(global_vars.tk_vars_defaults["spss_indttest_groupOneLabel_tk"])
	spss_indttest_groupTwoLabel_tk.set(global_vars.tk_vars_defaults["spss_indttest_groupTwoLabel_tk"])
	spss_pairttest_nOne_tk.set(global_vars.tk_vars_defaults["spss_pairttest_nOne_tk"])
	spss_pairttest_nTwo_tk.set(global_vars.tk_vars_defaults["spss_pairttest_nTwo_tk"])

	effect_size_choice_tk.set(global_vars.tk_vars_defaults["effect_size_choice_tk"])
	correction_type_tk.set(global_vars.tk_vars_defaults["correction_type_tk"])

	raw_ttest_output_descriptives_tk.set(global_vars.tk_vars_defaults["raw_ttest_output_descriptives_tk"])
	non_numeric_input_raise_errors_tk.set(global_vars.tk_vars_defaults["non_numeric_input_raise_errors_tk"])

#set all variables to default at start
input_type_tk.set(global_vars.tk_vars_defaults["input_type_tk"])
input_path_and_filename_tk.set(global_vars.tk_vars_defaults["input_path_and_filename_tk"])
output_filename_tk.set(global_vars.tk_vars_defaults["output_filename_tk"])
alpha_threshold_tk.set(global_vars.tk_vars_defaults["alpha_threshold_tk"])
set_variables_default()

input_filename_Frame = ttk.LabelFrame(master, text="Choose input file")
input_filename_Frame.grid(row=1, column=0, columnspan=2, sticky="NW", padx=15, pady=5)

alpha_threshold_Frame = ttk.LabelFrame(master, text="Alpha criterion")
alpha_threshold_Frame.grid(row=1, column=2, sticky="E", padx=(0,15), pady=5)

output_filename_Frame = ttk.LabelFrame(master, text="Save output as...")
output_filename_Frame.grid(row=4, column=0, columnspan=2, sticky="NW", padx=15, pady=5)

input_type_Frame = ttk.LabelFrame(master, text="Select input type:")
input_type_Frame.grid(row=2, column=0, columnspan=3, sticky="NW", padx=15, pady=5)

test_specifications_master_Frame = tk.Frame(master)
test_specifications_master_Frame.grid(row=3, column=0, columnspan=3, sticky="NW", padx=15)

raw_test_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Statistical test")

raw_corr_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Correlation type")
raw_corr_vars_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Variables to correlate")

raw_mr_outcomevar_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Outcome variable")
raw_mr_predictors_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Predictors")

raw_indttest_groupvar_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Grouping variable")
raw_indttest_dv_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Dependent variables")

raw_pairttest_master_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Choose variable pairs")
raw_pairttest_pairs_Frame = tk.Frame(raw_pairttest_master_Frame)
raw_pairttest_pairs_Frame.grid(row=0, column=0, pady=(0, 10))
raw_pairttest_btn_list_Frame = tk.Frame(raw_pairttest_master_Frame)
raw_pairttest_btn_list_Frame.grid(row=1, column=0)

summ_corr_master_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Map columns")
summ_corr_varOne_Frame = ttk.LabelFrame(summ_corr_master_Frame, text="Variable 1 column")
summ_corr_varOne_Frame.grid(row=0, column=0, padx=(0, 5))
summ_corr_varTwo_Frame = ttk.LabelFrame(summ_corr_master_Frame, text="Variable 2 column")
summ_corr_varTwo_Frame.grid(row=1, column=0, pady=(5, 0), padx=(0, 5))
summ_corr_coeff_Frame = ttk.LabelFrame(summ_corr_master_Frame, text="Correlation coefficient column")
summ_corr_coeff_Frame.grid(row=0, column=1)
summ_corr_pvalues_Frame = ttk.LabelFrame(summ_corr_master_Frame, text="P-values column")
summ_corr_pvalues_Frame.grid(row=1, column=1, pady=(5, 0))

summ_indttest_master_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Map columns")
summ_indttest_var_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="Variables column")
summ_indttest_var_Frame.grid(row=0, column=0, padx=(0, 10), pady=0)
summ_indttest_equal_var_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="Equal variances column")
summ_indttest_equal_var_Frame.grid(row=0, column=1)
summ_indttest_meanOne_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="Mean of Group 1 column")
summ_indttest_meanOne_Frame.grid(row=1, column=0, padx=(0, 10), pady=5)
summ_indttest_sdOne_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="SD of Group 1 column")
summ_indttest_sdOne_Frame.grid(row=2, column=0, padx=(0, 10), pady=0)
summ_indttest_nOne_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="N of Group 1 column")
summ_indttest_nOne_Frame.grid(row=3, column=0, padx=(0, 10), pady=(5, 0))
summ_indttest_meanTwo_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="Mean of Group 2 column")
summ_indttest_meanTwo_Frame.grid(row=1, column=1, pady=5)
summ_indttest_sdTwo_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="SD of Group 2 column")
summ_indttest_sdTwo_Frame.grid(row=2, column=1)
summ_indttest_nTwo_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="N of Group 2 column")
summ_indttest_nTwo_Frame.grid(row=3, column=1, pady=(5,0))

spss_test_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Statistical test")
spss_indttest_sampleSize_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Sample size")
spss_indttest_groupLabels_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Group labels (optional)")
spss_pairttest_sampleSize_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Sample size")

col_names_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Your variables")

effect_size_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Effect size")
correction_type_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Correction type")

raw_ttest_output_descriptives_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Output descriptive statistics?")
non_numeric_input_raise_errors_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="How to handle non-numeric cases?")

#----------------------------------------X.X. Helper functions
def update_filename_label(filename, label, char_limit):
	filename_no_ext = filename[:filename.rfind(".")]

	if len(filename_no_ext) > char_limit:
		label_text = filename_no_ext[:char_limit] + "[...]" + filename[filename.rfind("."):]
	else:
		label_text = filename

	label.config(text=label_text)

def get_values_for_dropdown(dropdown):
	dropdown.configure(values=col_names_lb.get(0, tk.END))

def add_variables_to_listbox(listbox):
	col_names_selection = list(col_names_lb.curselection())

	#check for duplicates
	already_added_items = list(listbox.get(0, tk.END))
	already_added_indices = [col_names_lb.get(0, tk.END).index(item) for item in already_added_items]
	common_elements_indices = list(set(col_names_selection) & set(already_added_indices))
	if len(common_elements_indices) < 1:
		listbox.insert(tk.END, *[col_names_lb.get(s) for s in col_names_selection])
	else:
		common_elements_items = [col_names_lb.get(ind) for ind in common_elements_indices]
		messagebox.showerror("Error!", "You tried to add the following variable(s): {}\nHowever, you cannot add the same variable(s) twice.".format("; ".join(common_elements_items)))

def remove_variables_from_listbox(listbox):
	current_selection = list(listbox.curselection())
	for index in current_selection[::-1]: #have to start backwards as each deletion changes item indices
		listbox.delete(index)

#-----------------2.2. Layout control
def remove_frames(frames_list):
	for frame in frames_list:
		frame.grid_remove()

def input_type_frames_layout():
	#the only frames it does not include are master or input_type
	frames_list = [raw_test_Frame, raw_corr_Frame, raw_corr_vars_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame, raw_indttest_dv_Frame,
					raw_pairttest_master_Frame, summ_corr_master_Frame, summ_indttest_master_Frame, spss_test_Frame, spss_indttest_sampleSize_Frame,
					spss_indttest_groupLabels_Frame, spss_pairttest_sampleSize_Frame, col_names_Frame, effect_size_Frame, correction_type_Frame,
					raw_ttest_output_descriptives_Frame, non_numeric_input_raise_errors_Frame]

	set_variables_default()
	remove_frames(frames_list)
	test_specifications_master_Frame.grid_rowconfigure(index=1, weight=0)

	if input_type_tk.get() == "raw":
		raw_test_Frame.grid(row=0, column=0, sticky="NW")
	elif input_type_tk.get() == "summ_corr":
		correction_type_Frame.grid(row=0, column=0, sticky="NW", padx=0, pady=0)
		summ_corr_master_Frame.grid(row=0, column=1, columnspan=2, sticky="NW", padx=15, pady=0)
	elif input_type_tk.get() == "summ_indttest":
		test_specifications_master_Frame.grid_rowconfigure(index=1, weight=1)
		correction_type_Frame.grid(row=0, column=0, sticky="NW", padx=(0, 15), pady=0)
		effect_size_Frame.grid(row=1, column=0, sticky="NW", padx=(0, 15), pady=5)
		summ_indttest_master_Frame.grid(row=0, column=1, columnspan=2, rowspan=2, sticky="NW", padx=(0, 15), pady=0)
	elif input_type_tk.get() == "spss":
		spss_test_Frame.grid(row=0, column=0, sticky="NW")
	elif input_type_tk.get() == "pvalues":
		correction_type_Frame.grid(row=0, column=0, sticky="NW", padx=0, pady=0)

def raw_test_clear_vars():
	raw_corr_type_tk.set(global_vars.tk_vars_defaults["raw_corr_type_tk"])
	raw_mr_outcomevar_tk.set(global_vars.tk_vars_defaults["raw_mr_outcomevar_tk"])
	raw_indttest_groupvar_tk.set(global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"])
	raw_pairttest_var1_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var1_tk"])
	raw_pairttest_var2_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var2_tk"])
	effect_size_choice_tk.set(global_vars.tk_vars_defaults["effect_size_choice_tk"])
	raw_ttest_output_descriptives_tk.set(global_vars.tk_vars_defaults["raw_ttest_output_descriptives_tk"])
	non_numeric_input_raise_errors_tk.set(global_vars.tk_vars_defaults["non_numeric_input_raise_errors_tk"])



def raw_test_frames_layout(event):
	frames_list = [raw_corr_Frame, raw_corr_vars_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame, raw_indttest_dv_Frame, raw_pairttest_master_Frame,
					col_names_Frame, effect_size_Frame, correction_type_Frame, raw_ttest_output_descriptives_Frame, non_numeric_input_raise_errors_Frame]

	raw_test_clear_vars()
	remove_frames(frames_list)

	if global_vars.master_dict[raw_test_tk.get()] == "corr":
		raw_corr_Frame.grid(row=1, column=0, sticky="NW", padx=0, pady=(5, 0))
		correction_type_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=5)
		non_numeric_input_raise_errors_Frame.grid(row=3, column=0, sticky="NW", padx=0, pady=0)
		col_names_Frame.grid(row=0, column=1, rowspan=4, sticky="NW", padx=15, pady=0)
		raw_corr_vars_Frame.grid(row=0, column=2, rowspan=4, sticky="NW", padx=0, pady=0)
	elif global_vars.master_dict[raw_test_tk.get()] == "mr":
		non_numeric_input_raise_errors_Frame.grid(row=1, column=0, sticky="NW", padx=0, pady=5)
		col_names_Frame.grid(row=0, column=1, rowspan=2, sticky="NW", padx=15, pady=0)
		raw_mr_outcomevar_Frame.grid(row=0, column=2, sticky="NW", padx=(0, 15), pady=0)
		raw_mr_predictors_Frame.grid(row=1, column=2, sticky="NW", padx=(0, 15), pady=(5, 0))
	elif global_vars.master_dict[raw_test_tk.get()] == "indttest":
		correction_type_Frame.grid(row=1, column=0, sticky="NW", padx=0, pady=5)
		effect_size_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=0)
		non_numeric_input_raise_errors_Frame.grid(row=3, column=0, sticky="NW", padx=0, pady=5)
		raw_ttest_output_descriptives_Frame.grid(row=4, column=0, sticky="NW", padx=0, pady=0)
		col_names_Frame.grid(row=0, column=1, rowspan=5, sticky="NW", padx=(15, 0), pady=0)
		raw_indttest_groupvar_Frame.grid(row=0, column=2, sticky="NW", padx=15, pady=0)
		raw_indttest_dv_Frame.grid(row=1, column=2, rowspan=4, sticky="NW", padx=15, pady=(5, 0))
	elif global_vars.master_dict[raw_test_tk.get()] == "pairttest":
		correction_type_Frame.grid(row=1, column=0, sticky="NW", padx=0, pady=5)
		effect_size_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=0)
		non_numeric_input_raise_errors_Frame.grid(row=3, column=0, sticky="NW", padx=0, pady=5)
		raw_ttest_output_descriptives_Frame.grid(row=4, column=0, sticky="NW", padx=0, pady=0)
		raw_pairttest_master_Frame.grid(row=0, column=1, rowspan=5, sticky="NW", padx=15, pady=0)

def spss_test_clear_vars():
	spss_indttest_nOne_tk.set(global_vars.tk_vars_defaults["spss_indttest_nOne_tk"])
	spss_indttest_nTwo_tk.set(global_vars.tk_vars_defaults["spss_indttest_nTwo_tk"])
	spss_indttest_groupOneLabel_tk.set(global_vars.tk_vars_defaults["spss_indttest_groupOneLabel_tk"])
	spss_indttest_groupTwoLabel_tk.set(global_vars.tk_vars_defaults["spss_indttest_groupTwoLabel_tk"])
	spss_pairttest_nOne_tk.set(global_vars.tk_vars_defaults["spss_pairttest_nOne_tk"])
	spss_pairttest_nTwo_tk.set(global_vars.tk_vars_defaults["spss_pairttest_nTwo_tk"])

	correction_type_tk.set(global_vars.tk_vars_defaults["correction_type_tk"])
	effect_size_choice_tk.set(global_vars.tk_vars_defaults["effect_size_choice_tk"])

def spss_test_frames_layout(event):
	frames_list = [spss_indttest_sampleSize_Frame, spss_indttest_groupLabels_Frame, spss_pairttest_sampleSize_Frame, effect_size_Frame, correction_type_Frame]

	spss_test_clear_vars()
	remove_frames(frames_list)

	if global_vars.master_dict[spss_test_tk.get()] == "corr":
		correction_type_Frame.grid(row=1, column=0, sticky="NW", padx=0, pady=(5, 0))
	elif global_vars.master_dict[spss_test_tk.get()] == "mr":
		pass #i.e. nothing needs to be done
	elif global_vars.master_dict[spss_test_tk.get()] == "indttest":
		correction_type_Frame.grid(row=1, column=0, sticky="NW", padx=0, pady=5)
		effect_size_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=0)
		spss_indttest_sampleSize_Frame.grid(row=0, column=1, rowspan=3, sticky="NW", padx=15, pady=0)
		spss_indttest_groupLabels_Frame.grid(row=0, column=2, rowspan=3, sticky="NW", padx=0, pady=0)
	elif global_vars.master_dict[spss_test_tk.get()] == "pairttest":
		correction_type_Frame.grid(row=1, column=0, sticky="NW", padx=(0, 15), pady=5)
		effect_size_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=0)
		spss_pairttest_sampleSize_Frame.grid(row=0, column=1, rowspan=3, sticky="NW", padx=0, pady=0)

#-----------------2.3. GUI Content
#Instructions
instr_label = ttk.Label(master, text="Main instructions")
instr_label.grid(row=0, column=0, columnspan=3)

#Input file button & label
def select_file():
	path_and_filename = askopenfilename(initialdir = "D:\\Desktop_current\\NPSoftware\\GitHub", title="Select input file. Must be Excel file.", filetypes=(("Excel files","*.xlsx"),("All files","*.*")))
	
	if path_and_filename.endswith(".xlsx"): # or filename[ext_sep_idx:] == ".csv" - for later use when csv is integrated
		update_filename_label(filename = path_and_filename[path_and_filename.rfind("/")+1:], label = filename_label, char_limit=50)

		input_path_and_filename_tk.set(path_and_filename)

		df_cols = helper_funcs.get_df_columns(path_and_filename)
		col_names_lb.configure(state="normal")
		col_names_lb.delete(0, tk.END)
		col_names_lb.insert(tk.END, *df_cols)

	elif path_and_filename != "":
		messagebox.showerror("Error!", "Please select a valid file - XLSX only.")

ttk.Button(input_filename_Frame, text="Select input file (xlsx only)", command=select_file).grid(row=0, column=0, sticky="W", padx=(0, 10))
filename_label = ttk.Label(input_filename_Frame, text="No file selected.")
filename_label.grid(row=0, column=1, columnspan=1, sticky="W")

#Alpha threshold
ttk.Label(alpha_threshold_Frame, text="Alpha: ").grid(row=0, column=0, sticky="NW")
ttk.Entry(alpha_threshold_Frame, textvariable=alpha_threshold_tk, width=6).grid(row=0, column=1, sticky="NW")

#Column names listbox and scrollbar
col_names_lb = tk.Listbox(col_names_Frame, selectmode="extended", height=10, width=20)
col_names_scroll_y = ttk.Scrollbar(col_names_Frame, orient="vertical", command=col_names_lb.yview)
col_names_scroll_x = ttk.Scrollbar(col_names_Frame, orient="horizontal", command=col_names_lb.xview)
col_names_lb.configure(yscrollcommand=col_names_scroll_y.set, xscrollcommand=col_names_scroll_x.set)
col_names_lb.grid(row=0, column=0, sticky="W")
col_names_scroll_x.grid(row=1, column=0, sticky="EW")
col_names_scroll_y.grid(row=0, column=1, sticky="NS")
col_names_lb.insert(0, "Select input file first...")
col_names_lb.configure(state="disabled")

#Input Type
input_type_Dict = {"Raw data" : "raw", "Correlations from summary statistics" : "summ_corr", 
					"Independent t-test from summary statistics" : "summ_indttest", "SPSS table" : "spss",
					"P values" : "pvalues"}
i_input = 0 #used for rows in the grid
for (text, value) in input_type_Dict.items(): 
		ttk.Radiobutton(input_type_Frame, text=text, variable=input_type_tk, value=value, command=input_type_frames_layout).grid(row=0, column=i_input, sticky="W")
		i_input += 1

#Raw data // test
raw_test_options = ("Correlations", "(Multiple) Regression - Standard", "Independent Samples t-test", "Paired samples t-test")
raw_test_drop = ttk.Combobox(raw_test_Frame, values=raw_test_options, state="readonly", width=30, textvariable=raw_test_tk)
raw_test_drop.bind("<<ComboboxSelected>>", raw_test_frames_layout)
raw_test_drop.grid(row=0, column=0)

#Raw data // test // Correlations
raw_corr_options = ("Pearson's r", "Spearman's rho", "Kendall's tau")
raw_corr_drop = ttk.Combobox(raw_corr_Frame, values=raw_corr_options, state="readonly", width=30, textvariable=raw_corr_type_tk)
raw_corr_drop.grid(row=0, column=0)

#Raw data // test // Correlations // Variables
raw_corr_vars_lb = tk.Listbox(raw_corr_vars_Frame, selectmode="extended", height=7, width=23)
raw_corr_vars_scroll_y = ttk.Scrollbar(raw_corr_vars_Frame, orient="vertical", command=raw_corr_vars_lb.yview)
raw_corr_vars_lb.configure(yscrollcommand=raw_corr_vars_scroll_y.set)
raw_corr_vars_lb.grid(row=0, column=1, rowspan=2, sticky="W")
raw_corr_vars_scroll_y.grid(row=0, column=2, rowspan=2, sticky="NS")

raw_corr_vars_add_btn = ttk.Button(raw_corr_vars_Frame, text="--->", command=lambda listbox=raw_corr_vars_lb: add_variables_to_listbox(listbox)) 
raw_corr_vars_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))
raw_corr_vars_remove_btn = ttk.Button(raw_corr_vars_Frame, text="X", command=lambda listbox=raw_corr_vars_lb: remove_variables_from_listbox(listbox))
raw_corr_vars_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Multiple Regression // Outcome variable
raw_mr_outcomevar_drop = ttk.Combobox(raw_mr_outcomevar_Frame, state="readonly", width=30, textvariable=raw_mr_outcomevar_tk)
raw_mr_outcomevar_drop.configure(postcommand=lambda dropdown=raw_mr_outcomevar_drop: get_values_for_dropdown(dropdown))
raw_mr_outcomevar_drop.grid(row=0, column=0)

#Raw data // test // Multiple Regression // Predictors
raw_mr_predictors_lb = tk.Listbox(raw_mr_predictors_Frame, selectmode="extended", height=7, width=23)
raw_mr_predictors_scroll_y = ttk.Scrollbar(raw_mr_predictors_Frame, orient="vertical", command=raw_mr_predictors_lb.yview)
raw_mr_predictors_lb.configure(yscrollcommand=raw_mr_predictors_scroll_y.set)
raw_mr_predictors_lb.grid(row=0, column=1, rowspan=2, sticky="W")
raw_mr_predictors_scroll_y.grid(row=0, column=2, rowspan=2, sticky="NS")

raw_mr_predictors_add_btn = ttk.Button(raw_mr_predictors_Frame, text="--->", command=lambda listbox=raw_mr_predictors_lb: add_variables_to_listbox(listbox))
raw_mr_predictors_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))
raw_mr_predictors_remove_btn = ttk.Button(raw_mr_predictors_Frame, text="X", command=lambda listbox=raw_mr_predictors_lb: remove_variables_from_listbox(listbox))
raw_mr_predictors_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Independent samples t-test // Grouping variable
raw_indttest_groupvar_drop = ttk.Combobox(raw_indttest_groupvar_Frame, state="readonly", width=30, textvariable=raw_indttest_groupvar_tk)
raw_indttest_groupvar_drop.configure(postcommand=lambda dropdown=raw_indttest_groupvar_drop: get_values_for_dropdown(dropdown))
raw_indttest_groupvar_drop.grid(row=0, column=0)

#Raw data // test // Independent samples t-test // DVs
raw_indttest_dv_lb = tk.Listbox(raw_indttest_dv_Frame, selectmode="extended", height=7, width=23)
raw_indttest_dv_scroll_y = ttk.Scrollbar(raw_indttest_dv_Frame, orient="vertical", command=raw_indttest_dv_lb.yview)
raw_indttest_dv_lb.configure(yscrollcommand=raw_indttest_dv_scroll_y.set)
raw_indttest_dv_lb.grid(row=0, column=1, rowspan=2, sticky="W")
raw_indttest_dv_scroll_y.grid(row=0, column=2, rowspan=2, sticky="NS")

raw_indttest_dv_add_btn = ttk.Button(raw_indttest_dv_Frame, text="--->", command=lambda listbox=raw_indttest_dv_lb: add_variables_to_listbox(listbox)) 
raw_indttest_dv_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))
raw_indttest_dv_remove_btn = ttk.Button(raw_indttest_dv_Frame, text="X", command=lambda listbox=raw_indttest_dv_lb: remove_variables_from_listbox(listbox))
raw_indttest_dv_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Paired samples t-test // Pair choices
raw_pairttest_var1_label = ttk.Label(raw_pairttest_pairs_Frame, text="Select the first variable")
raw_pairttest_var1_label.grid(row=0, column=0, sticky="NW", padx=(0,15), pady=0)
raw_pairttest_var1_drop = ttk.Combobox(raw_pairttest_pairs_Frame, state="readonly", width=20, textvariable=raw_pairttest_var1_tk)
raw_pairttest_var1_drop.configure(postcommand=lambda dropdown=raw_pairttest_var1_drop: get_values_for_dropdown(dropdown))
raw_pairttest_var1_drop.grid(row=1, column=0, sticky="NW", padx=(0,15), pady=0)

raw_pairttest_var2_label = ttk.Label(raw_pairttest_pairs_Frame, text="Select the second variable")
raw_pairttest_var2_label.grid(row=0, column=1, sticky="NW")
raw_pairttest_var2_drop = ttk.Combobox(raw_pairttest_pairs_Frame, state="readonly", width=20, textvariable=raw_pairttest_var2_tk)
raw_pairttest_var2_drop.configure(postcommand=lambda dropdown=raw_pairttest_var2_drop: get_values_for_dropdown(dropdown))
raw_pairttest_var2_drop.grid(row=1, column=1, sticky="NW")

#Raw data // test // Paired samples t-test // Pairs - buttons and listbox
def raw_pairttest_add_pair():
	if filename_label["text"] == "No file selected.":
		messagebox.showerror("Error!", "Please select input file first.")
	elif raw_pairttest_var1_tk == "Select first variable..." or raw_pairttest_var2_tk.get() == "Select second variable...":
		messagebox.showerror("Error!", "Please select variable 1 and variable 2 to create a pair.")
	elif raw_pairttest_var1_tk.get() == raw_pairttest_var2_tk.get():
		messagebox.showerror("Error!", "Make sure your variable 1 choice and variable 2 choice are not the same.")
	else:
		already_added_vars = [item for sublist in list(raw_pairttest_pairs_lb.get(0, tk.END)) for item in sublist.split(" <---> ")] #works on magic a bit - https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
		if raw_pairttest_var1_tk.get() in already_added_vars or raw_pairttest_var2_tk.get() in already_added_vars:
			messagebox.showerror("Error!", "You tried to add the following pair: {p1} <---> {p2}.\nHowever, you cannot add the same variable twice.".format(p1=raw_pairttest_var1_tk.get(), p2=raw_pairttest_var2_tk.get()))
		else:
			raw_pairttest_pairs_lb.insert(tk.END, "{p1} <---> {p2}".format(p1=raw_pairttest_var1_tk.get(), p2=raw_pairttest_var2_tk.get()))

raw_pairttest_pairs_lb = tk.Listbox(raw_pairttest_btn_list_Frame, selectmode="extended", height=9, width=40)
raw_pairttest_pairs_scroll_y = ttk.Scrollbar(raw_pairttest_btn_list_Frame, orient="vertical", command=raw_pairttest_pairs_lb.yview)
raw_pairttest_pairs_lb.configure(yscrollcommand=raw_pairttest_pairs_scroll_y.set)
raw_pairttest_pairs_lb.grid(row=1, column=0, columnspan=2, sticky="NW", pady=(10,0))
raw_pairttest_pairs_scroll_y.grid(row=1, column=3, sticky="NS")

raw_pairttest_add_btn = ttk.Button(raw_pairttest_btn_list_Frame, text="Add pair", command=raw_pairttest_add_pair)
raw_pairttest_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(0,50))
raw_pairttest_remove_btn = ttk.Button(raw_pairttest_btn_list_Frame, text="Remove", command=lambda listbox=raw_pairttest_pairs_lb: remove_variables_from_listbox(listbox))
raw_pairttest_remove_btn.grid(row=0, column=1, sticky="EWNS")

#Summary statistics - Correlations
summ_corr_varOne_drop = ttk.Combobox(summ_corr_varOne_Frame, state="readonly", width=30, textvariable=summ_corr_varOne_tk)
summ_corr_varOne_drop.configure(postcommand=lambda dropdown=summ_corr_varOne_drop: get_values_for_dropdown(dropdown))
summ_corr_varOne_drop.grid(row=0, column=0)

summ_corr_varTwo_drop = ttk.Combobox(summ_corr_varTwo_Frame, state="readonly", width=30, textvariable=summ_corr_varTwo_tk)
summ_corr_varTwo_drop.configure(postcommand=lambda dropdown=summ_corr_varTwo_drop: get_values_for_dropdown(dropdown))
summ_corr_varTwo_drop.grid(row=0, column=0)

summ_corr_coeff_drop = ttk.Combobox(summ_corr_coeff_Frame, state="readonly", width=30, textvariable=summ_corr_coeff_tk)
summ_corr_coeff_drop.configure(postcommand=lambda dropdown=summ_corr_coeff_drop: get_values_for_dropdown(dropdown))
summ_corr_coeff_drop.grid(row=0, column=0)

summ_corr_pvalues_drop = ttk.Combobox(summ_corr_pvalues_Frame, state="readonly", width=30, textvariable=summ_corr_pvalues_tk)
summ_corr_pvalues_drop.configure(postcommand=lambda dropdown=summ_corr_pvalues_drop: get_values_for_dropdown(dropdown))
summ_corr_pvalues_drop.grid(row=0, column=0)

#Summary statistics - Independent samples t-test
summ_indttest_var_drop = ttk.Combobox(summ_indttest_var_Frame, state="readonly", width=30, textvariable=summ_indttest_var_tk)
summ_indttest_var_drop.configure(postcommand=lambda dropdown=summ_indttest_var_drop: get_values_for_dropdown(dropdown))
summ_indttest_var_drop.grid(row=0, column=0)

summ_indttest_equal_var_drop = ttk.Combobox(summ_indttest_equal_var_Frame, state="readonly", width=30, textvariable=summ_indttest_equal_var_tk)
summ_indttest_equal_var_drop.configure(postcommand=lambda dropdown=summ_indttest_equal_var_drop: get_values_for_dropdown(dropdown))
summ_indttest_equal_var_drop.grid(row=0, column=0)

summ_indttest_meanOne_drop = ttk.Combobox(summ_indttest_meanOne_Frame, state="readonly", width=30, textvariable=summ_indttest_meanOne_tk)
summ_indttest_meanOne_drop.configure(postcommand=lambda dropdown=summ_indttest_meanOne_drop: get_values_for_dropdown(dropdown))
summ_indttest_meanOne_drop.grid(row=0, column=0)

summ_indttest_sdOne_drop = ttk.Combobox(summ_indttest_sdOne_Frame, state="readonly", width=30, textvariable=summ_indttest_sdOne_tk)
summ_indttest_sdOne_drop.configure(postcommand=lambda dropdown=summ_indttest_sdOne_drop: get_values_for_dropdown(dropdown))
summ_indttest_sdOne_drop.grid(row=0, column=0)

summ_indttest_nOne_drop = ttk.Combobox(summ_indttest_nOne_Frame, state="readonly", width=30, textvariable=summ_indttest_nOne_tk)
summ_indttest_nOne_drop.configure(postcommand=lambda dropdown=summ_indttest_nOne_drop: get_values_for_dropdown(dropdown))
summ_indttest_nOne_drop.grid(row=0, column=0)

summ_indttest_meanTwo_drop = ttk.Combobox(summ_indttest_meanTwo_Frame, state="readonly", width=30, textvariable=summ_indttest_meanTwo_tk)
summ_indttest_meanTwo_drop.configure(postcommand=lambda dropdown=summ_indttest_meanTwo_drop: get_values_for_dropdown(dropdown))
summ_indttest_meanTwo_drop.grid(row=0, column=0)

summ_indttest_sdTwo_drop = ttk.Combobox(summ_indttest_sdTwo_Frame, state="readonly", width=30, textvariable=summ_indttest_sdTwo_tk)
summ_indttest_sdTwo_drop.configure(postcommand=lambda dropdown=summ_indttest_sdTwo_drop: get_values_for_dropdown(dropdown))
summ_indttest_sdTwo_drop.grid(row=0, column=0)

summ_indttest_nTwo_drop = ttk.Combobox(summ_indttest_nTwo_Frame, state="readonly", width=30, textvariable=summ_indttest_nTwo_tk)
summ_indttest_nTwo_drop.configure(postcommand=lambda dropdown=summ_indttest_nTwo_drop: get_values_for_dropdown(dropdown))
summ_indttest_nTwo_drop.grid(row=0, column=0)

#SPSS // test
spss_test_options = ("Correlations", "(Multiple) Regression - Standard", "Independent Samples t-test", "Paired samples t-test")
spss_test_drop = ttk.Combobox(spss_test_Frame, values=spss_test_options, state="readonly", width=30, textvariable=spss_test_tk)
spss_test_drop.bind("<<ComboboxSelected>>", spss_test_frames_layout)
spss_test_drop.grid(row=0, column=0)

#SPSS // test // Independent samples t-test // Sample Size
ttk.Label(spss_indttest_sampleSize_Frame, text="N, Group 1:").grid(row=0, column=0, sticky="NWES", padx=(0,5), pady=(0,5))
ttk.Entry(spss_indttest_sampleSize_Frame, textvariable=spss_indttest_nOne_tk, width=15).grid(row=0, column=1, sticky="NWES", pady=(0,5))
ttk.Label(spss_indttest_sampleSize_Frame, text="N, Group 2:").grid(row=1, column=0, sticky="NWES", padx=(0,5))
ttk.Entry(spss_indttest_sampleSize_Frame, textvariable=spss_indttest_nTwo_tk, width=15).grid(row=1, column=1, sticky="NWES")

#SPSS // test // Independent samples t-test // Group Labels
ttk.Label(spss_indttest_groupLabels_Frame, text="Label, Group 1:").grid(row=0, column=0, sticky="NWES", padx=(0,5), pady=(0,5))
ttk.Entry(spss_indttest_groupLabels_Frame, textvariable=spss_indttest_groupOneLabel_tk, width=25).grid(row=0, column=1, sticky="NWES", pady=(0,5))
ttk.Label(spss_indttest_groupLabels_Frame, text="Label, Group 2:").grid(row=1, column=0, sticky="NWES", padx=(0,5))
ttk.Entry(spss_indttest_groupLabels_Frame, textvariable=spss_indttest_groupTwoLabel_tk, width=25).grid(row=1, column=1, sticky="NWES")

#SPSS // test // Paired samples t-test // Sample Size
ttk.Label(spss_pairttest_sampleSize_Frame, text="N, Group 1:").grid(row=0, column=0, sticky="NWES", padx=(0,5), pady=(0,5))
ttk.Entry(spss_pairttest_sampleSize_Frame, textvariable=spss_pairttest_nOne_tk, width=15).grid(row=0, column=1, sticky="NWES", pady=(0,5))
ttk.Label(spss_pairttest_sampleSize_Frame, text="N, Group 2:").grid(row=1, column=0, sticky="NWES", padx=(0,5))
ttk.Entry(spss_pairttest_sampleSize_Frame, textvariable=spss_pairttest_nTwo_tk, width=15).grid(row=1, column=1, sticky="NWES")

#Effect size choice
effect_size_options = ("Cohen's d", "Hedge's g", "Glass's delta", "None")
effect_size_drop = ttk.Combobox(effect_size_Frame, values=effect_size_options, state="readonly", width=30, textvariable=effect_size_choice_tk)
effect_size_drop.grid(row=0, column=0)

#Correction type choice
correction_type_options = ("Bonferroni",  "Sidak", "Holm-Sidak", "Holm-Bonferroni", "Simes-Hochberg", "Hommel", 
						"Benjamini-Hochberg", "Benjamini-Yekutieli", "Benjamini-Hochberg (2-stage) ", 
						"Benjamini-Yekutieli (2-stage)", "None")
correction_type_drop = ttk.Combobox(correction_type_Frame, values=correction_type_options, state="readonly", width=30, textvariable=correction_type_tk)
correction_type_drop.grid(row=0, column=0)

#Raise errors on non-numeric input choice
non_numeric_errors_options = ("Raise errors", "Ignore case-wise")
non_numeric_errors_drop = ttk.Combobox(non_numeric_input_raise_errors_Frame, values=non_numeric_errors_options, state="readonly", width=30, textvariable=non_numeric_input_raise_errors_tk)
non_numeric_errors_drop.grid(row=0, column=0)

#Output descriptives for Raw t-tests
raw_ttest_output_descriptives_drop = ttk.Combobox(raw_ttest_output_descriptives_Frame, values=["No", "Yes"], state="readonly", width=30, textvariable=raw_ttest_output_descriptives_tk)
raw_ttest_output_descriptives_drop.grid(row=0, column=0)

#Output file button & label
def save_file():
	filename = asksaveasfilename(initialdir = "/", title = "Save output file...", filetypes = (("Excel files","*.xlsx"),("All files","*.*")))

	if filename != "":
		output_filename_tk.set(filename)
		update_filename_label(filename=filename + ".xlsx", label=output_file_label, char_limit=70)

ttk.Button(output_filename_Frame, text="Save output file...", command=save_file).grid(row=0, column=0, sticky="NW", padx=(0, 10))
output_file_label = ttk.Label(output_filename_Frame, text="Nothing selected yet.")
output_file_label.grid(row=0, column=1, sticky="W")

#-----------------2.4. On Submit functions
def set_global_variables():
	global_vars.input_path_and_filename = input_path_and_filename_tk.get()
	try:
		global_vars.alpha_threshold = float(alpha_threshold_tk.get())
	except:
		raise Exception("Could not set an alpha of \'{}\'. Please enter a valid number. Example: 0.05 or 0.01".format(alpha_threshold_tk.get()))
	global_vars.output_filename = output_filename_tk.get()

	global_vars.input_type = "" if input_type_tk.get() == global_vars.tk_vars_defaults["input_type_tk"] else input_type_tk.get()

	global_vars.raw_test = "" if raw_test_tk.get() == global_vars.tk_vars_defaults["raw_test_tk"] else global_vars.master_dict[raw_test_tk.get()]

	global_vars.raw_corr_type =  "" if raw_corr_type_tk.get() == global_vars.tk_vars_defaults["raw_corr_type_tk"] else global_vars.master_dict[raw_corr_type_tk.get()]
	global_vars.raw_corr_vars = list(raw_corr_vars_lb.get(0, tk.END))
	global_vars.raw_mr_outcomevar = "" if raw_mr_outcomevar_tk.get() == global_vars.tk_vars_defaults["raw_mr_outcomevar_tk"] else raw_mr_outcomevar_tk.get()
	global_vars.raw_mr_predictors = list(raw_mr_predictors_lb.get(0, tk.END))
	global_vars.raw_indttest_groupvar = "" if raw_indttest_groupvar_tk.get() == global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"] else raw_indttest_groupvar_tk.get()
	global_vars.raw_indttest_dv = list(raw_indttest_dv_lb.get(0, tk.END))
	global_vars.raw_pairttest_var_pairs = [pair.split(" <---> ") for pair in list(raw_pairttest_pairs_lb.get(0, tk.END))]

	global_vars.summ_corr_varOne = "" if summ_corr_varOne_tk.get() == global_vars.tk_vars_defaults["summ_corr_varOne_tk"] else summ_corr_varOne_tk.get()
	global_vars.summ_corr_varTwo = "" if summ_corr_varTwo_tk.get() == global_vars.tk_vars_defaults["summ_corr_varTwo_tk"] else summ_corr_varTwo_tk.get()
	global_vars.summ_corr_coeff = "" if summ_corr_coeff_tk.get() == global_vars.tk_vars_defaults["summ_corr_coeff_tk"] else summ_corr_coeff_tk.get()
	global_vars.summ_corr_pvalues = "" if summ_corr_pvalues_tk.get() == global_vars.tk_vars_defaults["summ_corr_pvalues_tk"] else summ_corr_pvalues_tk.get()

	global_vars.summ_indttest_var = summ_indttest_var_tk.get()
	global_vars.summ_indttest_meanOne = summ_indttest_meanOne_tk.get()
	global_vars.summ_indttest_sdOne = summ_indttest_sdOne_tk.get()
	global_vars.summ_indttest_nOne = summ_indttest_nOne_tk.get()
	global_vars.summ_indttest_meanTwo = summ_indttest_meanTwo_tk.get()
	global_vars.summ_indttest_sdTwo = summ_indttest_sdTwo_tk.get()
	global_vars.summ_indttest_nTwo = summ_indttest_nTwo_tk.get()
	global_vars.summ_indttest_equal_var = summ_indttest_equal_var_tk.get()

	global_vars.spss_test = "" if spss_test_tk.get() == global_vars.tk_vars_defaults["spss_test_tk"] else global_vars.master_dict[spss_test_tk.get()]
	try:
		global_vars.spss_indttest_nOne = -1 if spss_indttest_nOne_tk.get() == "Enter an integer" else int(spss_indttest_nOne_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_indttest_nOne_tk.get()))
	try:
		global_vars.spss_indttest_nTwo = -1 if spss_indttest_nTwo_tk.get() == "Enter an integer" else int(spss_indttest_nTwo_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_indttest_nTwo_tk.get()))
	global_vars.spss_indttest_groupOneLabel = spss_indttest_groupOneLabel_tk.get()
	global_vars.spss_indttest_groupTwoLabel = spss_indttest_groupTwoLabel_tk.get()
	try:
		global_vars.spss_pairttest_nOne = -1 if spss_pairttest_nOne_tk.get() == "Enter an integer" else int(spss_pairttest_nOne_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_pairttest_nOne_tk.get()))
	try:
		global_vars.spss_pairttest_nTwo = -1 if spss_pairttest_nTwo_tk.get() == "Enter an integer" else int(spss_pairttest_nTwo_tk.get())
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_pairttest_nTwo_tk.get()))

	global_vars.effect_size_choice = "none" if effect_size_choice_tk.get() == global_vars.tk_vars_defaults["effect_size_choice_tk"] else effect_size_choice_tk.get()
	global_vars.correction_type = "none" if correction_type_tk.get() == global_vars.tk_vars_defaults["correction_type_tk"] else global_vars.master_dict[correction_type_tk.get()]

	global_vars.non_numeric_input_raise_errors = "" if non_numeric_input_raise_errors_tk.get() == global_vars.tk_vars_defaults["non_numeric_input_raise_errors_tk"] else global_vars.master_dict[non_numeric_input_raise_errors_tk.get()]
	global_vars.raw_ttest_output_descriptives = True if raw_ttest_output_descriptives_tk.get() == "Yes" else False

	print("-------------------------------START PRINTING OUTPUT---------------------------")
	print("input_path_and_filename - ", global_vars.input_path_and_filename)
	print("alpha_threshold - ", global_vars.alpha_threshold)
	print("output_filename - ", global_vars.output_filename)

	print("input_type - ", global_vars.input_type)

	print("raw_test - ", global_vars.raw_test)

	print("raw_corr_type - ", global_vars.raw_corr_type)
	print("raw_mr_outcomevar - ", global_vars.raw_mr_outcomevar)
	print("raw_mr_predictors - ", global_vars.raw_mr_predictors)
	print("raw_indttest_groupvar - ", global_vars.raw_indttest_groupvar)
	print("raw_indttest_dv - ", global_vars.raw_indttest_dv)
	print("raw_pairttest_var_pairs - ", global_vars.raw_pairttest_var_pairs)

	print("summ_corr_varOne - ", global_vars.summ_corr_varOne)
	print("summ_corr_varTwo - ", global_vars.summ_corr_varTwo)
	print("summ_corr_coeff - ", global_vars.summ_corr_coeff)
	print("summ_corr_pvalues - ", global_vars.summ_corr_pvalues)

	print("summ_indttest_var - ", global_vars.summ_indttest_var)
	print("summ_indttest_meanOne - ", global_vars.summ_indttest_meanOne)
	print("summ_indttest_sdOne - ", global_vars.summ_indttest_sdOne)
	print("summ_indttest_nOne - ", global_vars.summ_indttest_nOne)
	print("summ_indttest_meanTwo - ", global_vars.summ_indttest_meanTwo)
	print("summ_indttest_sdTwo - ", global_vars.summ_indttest_sdTwo)
	print("summ_indttest_nTwo - ", global_vars.summ_indttest_nTwo)
	print("summ_indttest_equal_var - ", global_vars.summ_indttest_equal_var)

	print("spss_test - ", global_vars.spss_test)
	print("spss_indttest_nOne - ", global_vars.spss_indttest_nOne)
	print("spss_indttest_nTwo - ", global_vars.spss_indttest_nTwo)
	print("spss_indttest_groupOneLabel - ", global_vars.spss_indttest_groupOneLabel)
	print("spss_indttest_groupTwoLabel - ", global_vars.spss_indttest_groupTwoLabel)
	print("spss_pairttest_nOne - ", global_vars.spss_pairttest_nOne)
	print("spss_pairttest_nTwo - ", global_vars.spss_pairttest_nTwo)

	print("effect_size_choice - ", global_vars.effect_size_choice)
	print("correction_type - ", global_vars.correction_type)

	print("non_numeric_input_raise_errors - ", global_vars.non_numeric_input_raise_errors)
	print("raw_ttest_output_descriptives - ", global_vars.raw_ttest_output_descriptives)
	print("-------------------------------END PRINTING OUTPUT---------------------------")

def input_validation():
	#find a way to abstract out the common errors - corrections, effect sizes etc
	if global_vars.input_path_and_filename == "":
		raise Exception("In a bit of a rush, are we? Well, we've all been there! But in order for this to work, you need to give us some data to do stuff on.\n\nPlease select your input file.")
	if global_vars.input_type == "":
		raise Exception("Although we are currently working on a version of this software where we can read your mind, we are not there just yet! For now, you will need to let us know what type of data you are providing.")
	if global_vars.input_type == "raw":
		if global_vars.raw_test == "":
			raise Exception("DO YOU WANT US TO DELETE YOUR DATA?\n\nNaah, just kidding. But we are really not sure what to do with it.\n\nPlease tell us what want kind of statistical test you want us to perform.")
		if global_vars.raw_test == "corr":
			if global_vars.raw_corr_type == "":
				raise Exception("")
			if global_vars.correction_type == "":
				raise Exception("")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("")
		elif global_vars.raw_test == "mr":
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("")
			if global_vars.raw_mr_outcomevar == "":
				raise Exception("")
			if global_vars.raw_mr_predictors == ():
				raise Exception("")
		elif global_vars.raw_test == "indttest":
			if global_vars.correction_type == "":
				raise Exception("")
			if global_vars.effect_size_choice == "":
				raise Exception("")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("")
			if global_vars.raw_ttest_output_descriptives == "":
				raise Exception("")
			if global_vars.raw_indttest_groupvar == "":
				raise Exception("")
			if global_vars.raw_indttest_dv == []:
				raise Exception("")
		elif global_vars.raw_test == "pairttest":
			if global_vars.correction_type == "":
				raise Exception("")
			if global_vars.effect_size_choice == "":
				raise Exception("")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("")
			if global_vars.raw_ttest_output_descriptives == "":
				raise Exception("")
			if global_vars.raw_pairttest_var_pairs == ():
				raise Exception("")
	elif global_vars.input_type == "summ_corr":
		if global_vars.correction_type == "":
			raise Exception("")
		if global_vars.summ_corr_varOne == "":
			raise Exception("")
		if global_vars.summ_corr_varTwo == "":
			raise Exception("")
		if global_vars.summ_corr_coeff == "":
			raise Exception("")
		if global_vars.summ_corr_pvalues == "":
			raise Exception("")
	elif global_vars.input_type == "summ_indttest":
		if global_vars.correction_type == "":
			raise Exception("")
		if global_vars.effect_size_choice == "":
			raise Exception("")
		if global_vars.summ_indttest_var == "":
			raise Exception("")
		if global_vars.summ_indttest_meanOne == "":
			raise Exception("")
		if global_vars.summ_indttest_sdOne == "":
			raise Exception("")
		if global_vars.summ_indttest_nOne == "":
			raise Exception("")
		if global_vars.summ_indttest_meanTwo == "":
			raise Exception("")
		if global_vars.summ_indttest_sdTwo == "":
			raise Exception("")
		if global_vars.summ_indttest_nTwo == "":
			raise Exception("")
		if global_vars.summ_indttest_equal_var == "":
			raise Exception("")
	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "":
			raise Exception("")
		elif global_vars.spss_test == "corr":
			if global_vars.correction_type == "":
				raise Exception("")
		elif global_vars.spss_test == "mr":
			pass
		elif global_vars.spss_test == "indttest":
			if global_vars.correction_type == "":
				raise Exception("")
			if global_vars.effect_size_choice == "":
				raise Exception("")
			if global_vars.spss_indttest_nOne == -1 or global_vars.spss_indttest_nTwo == -1:
				raise Exception("")
		elif global_vars.spss_test == "pairttest":
			if global_vars.correction_type == "":
				raise Exception("")
			if global_vars.effect_size_choice == "":
				raise Exception("")
			if global_vars.spss_pairttest_nOne == -1 or global_vars.spss_pairttest_nTwo == -1:
				raise Exception("")
	elif global_vars.input_type == "pvalues":
		if global_vars.correction_type == "":
			raise Exception("")


	if global_vars.effect_size_choice == "Glass's delta" and (global_vars.input_type == "summindttest" or global_vars.spss_test == "indttest" or global_vars.spss_test == "pairttest"):
		raise Exception("Sorry! Glass's delta is not available for this time of test. Glass's delta can only be requested if raw data is provided. For more information, see the documentation.")
	
	if global_vars.output_filename == "":
		raise Exception("")
		
'''
	####THIS SHOULD BE FIXED!!!
	if effect_size_choice == "" and (raw_test == "indttest" or raw_test == "pairttest" or spss_test == "indttest" or spss_test == "pairttest" or input_type == "summ_indttest"):
		raise Exception("Unfortunately, as this software is still in beta version, you need to select an effect size to add to your APA table.\n\nFeel free to select any effect size and delete the column in the produced output if not needed.")

'''
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

def submit_window(show_buttons=0):
	#show_buttons is either 0 or 1 - if 0, then only shows the message

	top = tk.Toplevel()
	top.grab_set()
	top.title("Popup name")

	some_message = "ALL DONE NOW! (and some other msg)"
	tk.Label(top, text=some_message).grid(row=0, column=0, columnspan=3, sticky="NWES", padx=15, pady=(5, 0))

	if show_buttons == 1:
		def openfilelocation():
			directory = global_vars.output_filename[:global_vars.output_filename.rfind("/")]
			open_new(directory)

		ttk.Button(top, text="Open file location", command=openfilelocation).grid(row=1, column=0, padx=(15, 0), pady=5)
		ttk.Button(top, text="I want to do more analysis", command=top.destroy).grid(row=1, column=1, padx=15, pady=5)
		ttk.Button(top, text="Close the app", command=master.destroy).grid(row=1,column=2, padx=(0, 15), pady=5)

	center(top)



#--------------------Menu
menubar = tk.Menu(master)
master.config(menu=menubar)


file = tk.Menu(menubar, tearoff=0)
file.add_command(label="Exit", command=master.destroy)
menubar.add_cascade(label="File", menu=file)

about = tk.Menu(menubar, tearoff=0)
#about.add_command(label="Info", command=lambda show_buttons=0: submit_window(show_buttons))
about.add_command(label="Info", command=submit_window)
menubar.add_cascade(label="About", menu=about)

#------------------------
def run_individual_funcs():
	if global_vars.input_type == "raw":
		if global_vars.raw_test == "corr":
			raw_correlations.main()
		elif global_vars.raw_test == "mr":
			raw_mr.main()
		elif global_vars.raw_test == "indttest":
			raw_indttest.main()
		elif global_vars.raw_test == "pairttest":
			raw_pairttest.main()
	elif global_vars.input_type == "summ_corr":
		summ_correlations.main()
	elif global_vars.input_type == "summ_indttest":
		summ_indttest.main()
	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "corr":
			spss_correlations.main()
		elif global_vars.spss_test == "mr":
			spss_mr.main()
		elif global_vars.spss_test == "indttest":
			spss_indttest.main()
		elif global_vars.spss_test == "pairttest":
			spss_pairttest.main()
	elif global_vars.input_type == "pvalues":
		pvalues.main()

#------------------------------------------------------------------------------------
def submit():
	set_global_variables()
	input_validation()
	run_individual_funcs()
	print("Success")
	#another_window_test() #the progess bar stuff for later
	submit_window(show_buttons=1)
	#master.destroy()
	#make sure to catch exceptions and do stuff to reset all variables

ttk.Button(master, text="Submit", command=submit).grid(row=4, column=2, sticky="E", padx=(0,15), pady=5)

master.mainloop()


'''
-------------Progess bar for later implementation
def another_window_test():
	#https://docs.python.org/3/library/tkinter.ttk.html#progressbar
	top2 = tk.Toplevel()
	top2.geometry("100x100")
	top2.grab_set()
	top2.title("Loading")
	center(top2)
	
	mymsg = tk.Message(top2, text="Starting to load...")
	mymsg.grid(row=0, column=0)

	progress = ttk.Progressbar(top2, orient="horizontal", length=100, mode="determinate")
	progress.grid(row=1, column=0)		

	print("Func 1 executed")
	progress["value"] = 25
	mymsg.config(text="Getting there...")
	top2.update_idletasks()
	time.sleep(3)
	
	print("Func 2 executed")
	progress["value"] = 50
	mymsg.config(text="Still calculating...")
	top2.update_idletasks()
	time.sleep(3)
	
	print("Func 3 executed")
	progress["value"] = 75
	mymsg.config(text="Aaaaalmoooost...")
	top2.update_idletasks()
	time.sleep(3)

	print("Func 4 executed")
	progress["value"] = 100
	mymsg.config(text="There we go!")

	#submit_window()
'''