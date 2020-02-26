'''
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
'''
import Calculations_only as calcs
import global_vars
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory

#-------------------------------------------------------------2. GUI----------------------------------------------------------------
master = tk.Tk()
master.title("MAPAS Rework")
master.resizable(False, False)
#master.geometry("900x400")
#tk.Grid.rowconfigure(master, 0, weight=1)
#tk.Grid.columnconfigure(master, 0, weight=1)

#-----------------2.1. Variable and Frame declaration
input_type_tk = tk.StringVar()

raw_test_tk = tk.StringVar()
raw_corr_type_tk = tk.StringVar()
raw_mr_outcomevar_tk = tk.StringVar()
raw_indttest_groupvar_tk = tk.StringVar()
raw_pairttest_var1_tk = tk.StringVar()
raw_pairttest_var2_tk = tk.StringVar()

summ_corr_varOne_tk = tk.StringVar()
summ_corr_varTwo_tk = tk.StringVar()
summ_corr_coeff_tk = tk.StringVar()
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

input_filename_tk = tk.StringVar()
input_fileext_tk = tk.StringVar()
alpha_threshold_tk = tk.StringVar()
output_dir_tk = tk.StringVar()

#resets variables to default but does not include input variables or alpha as it is used in functions below
def set_variables_default():
	raw_test_tk.set("Select a test...")
	raw_corr_type_tk.set("Select a correlation...")
	raw_mr_outcomevar_tk.set("Select outcome variable...")
	raw_indttest_groupvar_tk.set("Select grouping variable...")
	raw_pairttest_var1_tk.set("Select first variable...")
	raw_pairttest_var2_tk.set("Select second variable...")

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

	effect_size_choice_tk.set("Select effect size...")
	correction_type_tk.set("Select correction...")

	raw_ttest_output_descriptives_tk.set("No")
	non_numeric_input_raise_errors_tk.set("Select error handling...")

	output_dir_tk.set("")

#set all variables to default at start
input_type_tk.set(0)
input_filename_tk.set("")
input_fileext_tk.set("")
alpha_threshold_tk.set("0.05")
set_variables_default()

input_filename_Frame = tk.LabelFrame(master, text="Choose input file", padx=5, pady=5, borderwidth=3)
input_filename_Frame.grid(row=1, column=0, columnspan=50, sticky="NW", padx=15, pady=5)

input_type_Frame = tk.LabelFrame(master, text="Select input type:", padx=5, pady=5, borderwidth=3)
input_type_Frame.grid(row=2, column=0, columnspan=50, sticky="NW", padx=15, pady=5)

raw_test_Frame = tk.LabelFrame(master, text="Statistical test", padx=5, pady=5, borderwidth=3)

raw_corr_Frame = tk.LabelFrame(master, text="Correlation type", padx=5, pady=5, borderwidth=3)

raw_mr_outcomevar_Frame = tk.LabelFrame(master, text="Outcome variable", padx=5, pady=5, borderwidth=3)
raw_mr_predictors_Frame = tk.LabelFrame(master, text="Predictors", padx=5, pady=5, borderwidth=3)
raw_indttest_groupvar_Frame = tk.LabelFrame(master, text="Grouping variable", padx=5, pady=5, borderwidth=3)
raw_indttest_dv_Frame = tk.LabelFrame(master, text="Dependent variables", padx=5, pady=5, borderwidth=3)

raw_pairttest_master_Frame = tk.LabelFrame(master, text="Choose variable pairs", padx=5, pady=5, borderwidth=3)
raw_pairttest_pairs_Frame = tk.Frame(raw_pairttest_master_Frame)
raw_pairttest_pairs_Frame.grid(row=0, column=0, pady=(0, 10))
raw_pairttest_btn_list_Frame = tk.Frame(raw_pairttest_master_Frame)
raw_pairttest_btn_list_Frame.grid(row=1, column=0)

summ_corr_varNames_Frame = tk.Frame(master)

summ_indttest_cols_Frame = tk.Frame(master)

spss_test_Frame = tk.LabelFrame(master, text="Statistical test", padx=5, pady=5, borderwidth=3)
spss_indttest_Frame = tk.Frame(master)
spss_pairttest_Frame = tk.Frame(master)

col_names_Frame = tk.LabelFrame(master, text="Your variables", padx=5, pady=5, borderwidth=3)

effect_size_Frame = tk.LabelFrame(master, text="Effect size", padx=5, pady=5, borderwidth=3)
correction_type_Frame = tk.LabelFrame(master, text="Correction type", padx=5, pady=5, borderwidth=3)

raw_ttest_output_descriptives_Frame = tk.LabelFrame(master, text="Output descriptive statistics?", padx=5, pady=5, borderwidth=3)
non_numeric_input_raise_errors_Frame = tk.LabelFrame(master, text="How to handle non-numeric cases?", padx=5, pady=5, borderwidth=3)

#----------------------------------------X.X. Helper functions
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
	frames_list = [raw_test_Frame, raw_corr_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame, raw_indttest_dv_Frame,
					raw_pairttest_master_Frame, summ_corr_varNames_Frame, summ_indttest_cols_Frame, spss_test_Frame, spss_indttest_Frame,
					spss_pairttest_Frame, col_names_Frame, effect_size_Frame, correction_type_Frame, raw_ttest_output_descriptives_Frame, 
					non_numeric_input_raise_errors_Frame]

	set_variables_default()
	remove_frames(frames_list)

	if input_type_tk.get() == "raw":
		raw_test_Frame.grid(row=3, column=0, sticky="NW", padx=15, pady=0)
	elif input_type_tk.get() == "summ_corr":
		pass
	elif input_type_tk.get() == "summ_indttest":
		pass
	elif input_type_tk.get() == "spss":
		pass
	elif input_type_tk.get() == "pvalues":
		correction_type_Frame.grid(row=3, column=0, sticky="NW", padx=15, pady=0)

def raw_test_clear_vars():
	raw_corr_type_tk.set("Select a correlation...")
	raw_mr_outcomevar_tk.set("Select outcome variable...")
	raw_indttest_groupvar_tk.set("Select grouping variable...")
	raw_pairttest_var1_tk.set("Select first variable...")
	raw_pairttest_var2_tk.set("Select second variable...")
	effect_size_choice_tk.set("Select effect size...")
	raw_ttest_output_descriptives_tk.set("No")
	non_numeric_input_raise_errors_tk.set("Select error handling...")

def raw_test_frames_layout(event):
	frames_list = [raw_corr_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame, raw_indttest_dv_Frame, raw_pairttest_master_Frame,
					col_names_Frame, effect_size_Frame, correction_type_Frame, raw_ttest_output_descriptives_Frame, non_numeric_input_raise_errors_Frame]

	raw_test_clear_vars()
	remove_frames(frames_list)

	if global_vars.master_dict[raw_test_tk.get()] == "corr":
		raw_corr_Frame.grid(row=4, column=0, sticky="NW", padx=15, pady=5)
		correction_type_Frame.grid(row=3, column=1, sticky="NW", padx=0, pady=0)
		non_numeric_input_raise_errors_Frame.grid(row=4, column=1, sticky="NW", padx=0, pady=5)
	elif global_vars.master_dict[raw_test_tk.get()] == "mr":
		non_numeric_input_raise_errors_Frame.grid(row=4, column=0, sticky="NW", padx=15, pady=5)
		col_names_Frame.grid(row=3, column=1, rowspan=2, sticky="NW", padx=(0,15), pady=(0,5))
		raw_mr_outcomevar_Frame.grid(row=3, column=2, sticky="NW", padx=0, pady=0)
		raw_mr_predictors_Frame.grid(row=4, column=2, sticky="NW", padx=0, pady=5)
	elif global_vars.master_dict[raw_test_tk.get()] == "indttest":
		correction_type_Frame.grid(row=4, column=0, sticky="NW", padx=15, pady=5)
		effect_size_Frame.grid(row=5, column=0, sticky="NW", padx=15, pady=0)
		non_numeric_input_raise_errors_Frame.grid(row=6, column=0, sticky="NW", padx=15, pady=5)
		raw_ttest_output_descriptives_Frame.grid(row=7, column=0, sticky="NW", padx=15, pady=(0,5))
		col_names_Frame.grid(row=3, column=1, rowspan=6, sticky="NW", padx=0, pady=0)
		raw_indttest_groupvar_Frame.grid(row=3, column=2, sticky="NW", padx=15, pady=0)
		raw_indttest_dv_Frame.grid(row=4, column=2, rowspan=5, sticky="NW", padx=15, pady=5)
	elif global_vars.master_dict[raw_test_tk.get()] == "pairttest":
		correction_type_Frame.grid(row=4, column=0, sticky="NW", padx=15, pady=5)
		effect_size_Frame.grid(row=5, column=0, sticky="NW", padx=15, pady=0)
		non_numeric_input_raise_errors_Frame.grid(row=6, column=0, sticky="NW", padx=15, pady=5)
		raw_ttest_output_descriptives_Frame.grid(row=7, column=0, sticky="NW", padx=15, pady=(0,5))
		raw_pairttest_master_Frame.grid(row=3, column=1, rowspan=6, sticky="NW", padx=0, pady=0)

def spss_test_tk_clear_vars():
	pass

def spss_test_tk_frames_layout():
	pass

#-----------------2.3. GUI Content
#Instructions
instr_label = tk.Label(master, text="Main instructions")
instr_label.grid(row=0, column=0, columnspan=50)

#Input file button & label
def select_file():
	filename = askopenfilename(title="Select input file. Must be Excel file.", filetypes=(("Excel files","*.xlsx"),("All files","*.*")))
	ext_sep_idx = filename.rfind(".")
	filename_sep_idx = filename.rfind("/")
	
	if filename[ext_sep_idx:] == ".xlsx": # or filename[ext_sep_idx:] == ".csv" - for later use when csv is integrated
		input_filename_tk.set(filename[:ext_sep_idx])
		input_fileext_tk.set(filename[ext_sep_idx:])

		filename_label.config(text=filename[filename_sep_idx+1:])

		df_cols = calcs.get_df_columns(filename)
		col_names_lb.configure(state="normal")
		col_names_lb.delete(0, tk.END)
		col_names_lb.insert(tk.END, *df_cols)

	elif filename != "":
		messagebox.showerror("Error!", "Please select a valid file - XLSX only.")

tk.Button(input_filename_Frame, text="Select input file (xlsx only)", command=select_file).grid(row=0, column=0, sticky="W", padx=(0, 10))
filename_label = tk.Label(input_filename_Frame, text="No file selected.")
filename_label.grid(row=0, column=1, columnspan=1, sticky="W")

#Column names listbox and scrollbar
col_names_lb = tk.Listbox(col_names_Frame, selectmode="extended", height=10, width=20)
col_names_scroll_y = tk.Scrollbar(col_names_Frame, orient="vertical", command=col_names_lb.yview)
col_names_scroll_x = tk.Scrollbar(col_names_Frame, orient="horizontal", command=col_names_lb.xview)
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
		tk.Radiobutton(input_type_Frame, text=text, variable=input_type_tk, value=value, command=input_type_frames_layout).grid(row=0, column=i_input, sticky="W")
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

#Raw data // test // Multiple Regression // Outcome variable
raw_mr_outcomevar_drop = ttk.Combobox(raw_mr_outcomevar_Frame, state="readonly", width=30, textvariable=raw_mr_outcomevar_tk)
raw_mr_outcomevar_drop.configure(postcommand=lambda dropdown=raw_mr_outcomevar_drop: get_values_for_dropdown(dropdown))
raw_mr_outcomevar_drop.grid(row=0, column=0)

#Raw data // test // Multiple Regression // Predictors
raw_mr_predictors_lb = tk.Listbox(raw_mr_predictors_Frame, selectmode="extended", height=7, width=23)
raw_mr_predictors_scroll_y = tk.Scrollbar(raw_mr_predictors_Frame, orient="vertical", command=raw_mr_predictors_lb.yview)
raw_mr_predictors_lb.configure(yscrollcommand=raw_mr_predictors_scroll_y.set)
raw_mr_predictors_lb.grid(row=0, column=1, rowspan=2, sticky="W")
raw_mr_predictors_scroll_y.grid(row=0, column=2, rowspan=2, sticky="NS")

raw_mr_predictors_add_btn = tk.Button(raw_mr_predictors_Frame, text="--->", command=lambda listbox=raw_mr_predictors_lb: add_variables_to_listbox(listbox))
raw_mr_predictors_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))
raw_mr_predictors_remove_btn = tk.Button(raw_mr_predictors_Frame, text="X", command=lambda listbox=raw_mr_predictors_lb: remove_variables_from_listbox(listbox))
raw_mr_predictors_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Independent samples t-test // Grouping variable
raw_indttest_groupvar_drop = ttk.Combobox(raw_indttest_groupvar_Frame, state="readonly", width=30, textvariable=raw_indttest_groupvar_tk)
raw_indttest_groupvar_drop.configure(postcommand=lambda dropdown=raw_indttest_groupvar_drop: get_values_for_dropdown(dropdown))
raw_indttest_groupvar_drop.grid(row=0, column=0)

#Raw data // test // Independent samples t-test // DVs
raw_indttest_dv_lb = tk.Listbox(raw_indttest_dv_Frame, selectmode="extended", height=7, width=23)
raw_indttest_dv_scroll_y = tk.Scrollbar(raw_indttest_dv_Frame, orient="vertical", command=raw_indttest_dv_lb.yview)
raw_indttest_dv_lb.configure(yscrollcommand=raw_indttest_dv_scroll_y.set)
raw_indttest_dv_lb.grid(row=0, column=1, rowspan=2, sticky="W")
raw_indttest_dv_scroll_y.grid(row=0, column=2, rowspan=2, sticky="NS")

raw_indttest_dv_add_btn = tk.Button(raw_indttest_dv_Frame, text="--->", command=lambda listbox=raw_indttest_dv_lb: add_variables_to_listbox(listbox)) 
raw_indttest_dv_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))
raw_indttest_dv_remove_btn = tk.Button(raw_indttest_dv_Frame, text="X", command=lambda listbox=raw_indttest_dv_lb: remove_variables_from_listbox(listbox))
raw_indttest_dv_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Paired samples t-test // Pair choices
raw_pairttest_var1_label = tk.Label(raw_pairttest_pairs_Frame, text="Select the first variable")
raw_pairttest_var1_label.grid(row=0, column=0, sticky="NW", padx=(0,15), pady=0)
raw_pairttest_var1_drop = ttk.Combobox(raw_pairttest_pairs_Frame, state="readonly", width=20, textvariable=raw_pairttest_var1_tk)
raw_pairttest_var1_drop.configure(postcommand=lambda dropdown=raw_pairttest_var1_drop: get_values_for_dropdown(dropdown))
raw_pairttest_var1_drop.grid(row=1, column=0, sticky="NW", padx=(0,15), pady=0)

raw_pairttest_var2_label = tk.Label(raw_pairttest_pairs_Frame, text="Select the second variable")
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
raw_pairttest_pairs_scroll_y = tk.Scrollbar(raw_pairttest_btn_list_Frame, orient="vertical", command=raw_pairttest_pairs_lb.yview)
raw_pairttest_pairs_lb.configure(yscrollcommand=raw_pairttest_pairs_scroll_y.set)
raw_pairttest_pairs_lb.grid(row=1, column=0, columnspan=2, sticky="NW", pady=(10,0))
raw_pairttest_pairs_scroll_y.grid(row=1, column=3, sticky="NS")

raw_pairttest_add_btn = tk.Button(raw_pairttest_btn_list_Frame, text="Add pair", command=raw_pairttest_add_pair)
raw_pairttest_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(0,50))
raw_pairttest_remove_btn = tk.Button(raw_pairttest_btn_list_Frame, text="Remove", command=lambda listbox=raw_pairttest_pairs_lb: remove_variables_from_listbox(listbox))
raw_pairttest_remove_btn.grid(row=0, column=1, sticky="EWNS")

#Summary statistics - Correlations

#Summary statistics - Independent samples t-test

#SPSS // test
spss_test_options = ("Select a test...", "Correlations", "(Multiple) Regression - Standard", "Independent Samples t-test", "Paired samples t-test")
spss_test_drop = ttk.Combobox(spss_test_Frame, values=spss_test_options, state="readonly", width=30, textvariable=spss_test_tk)
spss_test_drop.current(0)
spss_test_drop.grid(row=0, column=0)

#SPSS // test // Independent samples t-test

#SPSS // test // Paired samples t-test

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

#Pvalues choice

#Raise errors on non-numeric input choice
non_numeric_errors_options = ("Raise errors", "Ignore case-wise")
non_numeric_errors_drop = ttk.Combobox(non_numeric_input_raise_errors_Frame, values=non_numeric_errors_options, state="readonly", width=30, textvariable=non_numeric_input_raise_errors_tk)
non_numeric_errors_drop.grid(row=0, column=0)

#Output descriptives for Raw t-tests
raw_ttest_output_descriptives_drop = ttk.Combobox(raw_ttest_output_descriptives_Frame, values=["No", "Yes"], state="readonly", width=30, textvariable=raw_ttest_output_descriptives_tk)
raw_ttest_output_descriptives_drop.grid(row=0, column=0)


#-----------------2.4. On Submit functions
def set_global_variables():
	pass
	

def input_validation():
	pass

def submit():
	set_global_variables()
	#input_validation()
	print("Success")
	#master.destroy()

tk.Button(master, text="Submit", command=submit).grid(row=50, column=0, columnspan=50)

master.mainloop()