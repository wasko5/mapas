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
#from Calculations_only import *
import global_vars
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory

#-------------------------------------------------------------2. GUI----------------------------------------------------------------
master = tk.Tk()
master.title("Multi-test corrections & APA table Software (MAPAS)")
#master.resizable(False, False)
tk.Grid.rowconfigure(master, 0, weight=1)
tk.Grid.columnconfigure(master, 0, weight=1)

#-----------------2.1. Variable and Frame declaration
input_type_tk = tk.StringVar()

raw_test_tk = tk.StringVar()
raw_corr_type_tk = tk.StringVar()
raw_mr_outcomevar_tk = tk.StringVar()
raw_indttest_groupvar_tk = tk.StringVar()
raw_pairttest_pairOne_tk = tk.StringVar()
raw_pairttest_pairTwo_tk = tk.StringVar()
raw_pairttest_pairThree_tk = tk.StringVar()
raw_pairttest_pairFour_tk = tk.StringVar()
raw_pairttest_pairFive_tk = tk.StringVar()
raw_pairttest_pairSix_tk = tk.StringVar()
raw_pairttest_pairSeven_tk = tk.StringVar()

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

non_numeric_input_raise_errors_tk = tk.BooleanVar()
output_pvalues_type_tk = tk.StringVar()
raw_ttest_output_descriptives_tk = tk.BooleanVar()

input_filename_tk = tk.StringVar()
input_fileext_tk = tk.StringVar()
alpha_threshold_tk = tk.StringVar()
output_dir_tk = tk.StringVar()

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

input_filename_Frame = tk.LabelFrame(master, text="Choose input file", padx=5, pady=5, borderwidth=3)
input_filename_Frame.grid(row=1, column=0, columnspan=50, sticky="W", pady=15, padx=15)

input_type_Frame = tk.LabelFrame(master, text="Select input type:", padx=5, pady=5, borderwidth=3)
input_type_Frame.grid(row=2,column=0, rowspan=45, sticky="W", padx=15)

raw_test_Frame = tk.LabelFrame(master, text="Statistical test", padx=5, pady=5, borderwidth=3)
raw_test_Frame.grid(row=2, column=1, sticky="W")

raw_corr_Frame = tk.LabelFrame(master, text="Correlation type", padx=5, pady=5, borderwidth=3)
raw_corr_Frame.grid(row=3, column=1, sticky="W")


raw_mr_Frame = tk.Frame(master)
raw_indttest_Frame = tk.Frame(master)
raw_pairttest_Frame = tk.Frame(master)

summ_corr_varNames_Frame = tk.Frame(master)

summ_indttest_cols_Frame = tk.Frame(master)

spss_test_Frame = tk.LabelFrame(master, text="Statistical test", padx=5, pady=5, borderwidth=3)
spss_test_Frame.grid(row=8, column=1, sticky="W")
spss_indttest_Frame = tk.Frame(master)
spss_pairttest_Frame = tk.Frame(master)

effect_size_Frame = tk.LabelFrame(master, text="Effect size", padx=5, pady=5, borderwidth=3)
effect_size_Frame.grid(row=4, column=1, sticky="W")
correction_type_Frame = tk.LabelFrame(master, text="Correction type", padx=5, pady=5, borderwidth=3)
correction_type_Frame.grid(row=5, column=1, sticky="W")

raw_ttest_output_descriptives_Frame = tk.LabelFrame(master, text="Output descriptive statistics?", padx=5, pady=5, borderwidth=3)
raw_ttest_output_descriptives_Frame.grid(row=6, column=1, sticky="W")
non_numeric_input_raise_errors_Frame = tk.LabelFrame(master, text="How to handle non-numeric cases?", padx=5, pady=5, borderwidth=3)
non_numeric_input_raise_errors_Frame.grid(row=7, column=1, sticky="W")

#-----------------2.2. Layout control
def remove_frames(frames_list):
	for frame in frames_list:
		frame.grid_remove()

def input_type_frames_layout():
	pass

def raw_test_clear_vars():
	pass

def raw_test_frames_layout():
	pass

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
	elif filename != "":
		messagebox.showerror("Error!", "Please select a valid file - XLSX only.")

tk.Button(input_filename_Frame, text="Select input file (xlsx only)", command=select_file).grid(row=0, column=0, sticky="W", padx=(0, 10))
filename_label = tk.Label(input_filename_Frame, text="No file selected.")
filename_label.grid(row=0, column=1, columnspan=1, sticky="W")

#Input Type
input_type_Dict = {"Raw data" : "raw", "Correlations from\nsummary statistics" : "summ_corr", 
					"Independent t-test\nfrom summary statistics" : "summ_indttest", "SPSS table" : "spss",
					"P values" : "pvalues"}
i_input = 0 #used for rows in the grid
for (text, value) in input_type_Dict.items(): 
		tk.Radiobutton(input_type_Frame, text=text, variable=input_type_tk, value=value, command=input_type_frames_layout).grid(row=i_input,sticky="W")
		i_input += 1

#Raw data // test
raw_corr_options = ("Select a correlation...", "Pearson's r", "Spearman's rho", "Kendall's tau")
raw_corr_drop = ttk.Combobox(raw_corr_Frame, values=raw_corr_options, state="readonly", width=30, textvariable=raw_corr_type_tk)
raw_corr_drop.current(0)
raw_corr_drop.grid(row=0, column=0)

#Raw data // test // Correlations
raw_test_options = ("Select a test...", "Correlations", "(Multiple) Regression - Standard", "Independent Samples t-test", "Paired samples t-test")
raw_test_drop = ttk.Combobox(raw_test_Frame, values=raw_test_options, state="readonly", width=30, textvariable=raw_test_tk)
raw_test_drop.current(0)
raw_test_drop.grid(row=0, column=0)

#Raw data // test // Multiple Regression

#Raw data // test // Independent samples t-test

#Raw data // test // Paired samples t-test

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
effect_size_options = ("Select effect size...", "Cohen's d", "Hedge's g", "Glass's delta", "None")
effect_size_drop = ttk.Combobox(effect_size_Frame, values=effect_size_options, state="readonly", width=30, textvariable=effect_size_choice_tk)
effect_size_drop.current(0)
effect_size_drop.grid(row=0, column=0)

#Correction type choice
correction_type_options = ("Select correction...", "Bonferroni",  "Sidak", "Holm-Sidak", "Holm-Bonferroni", "Simes-Hochberg", "Hommel", 
						"Benjamini-Hochberg", "Benjamini-Yekutieli", "Benjamini-Hochberg (2-stage) ", 
						"Benjamini-Yekutieli (2-stage)", "None")
correction_type_drop = ttk.Combobox(correction_type_Frame, values=correction_type_options, state="readonly", width=30, textvariable=correction_type_tk)
correction_type_drop.current(0)
correction_type_drop.grid(row=0, column=0)

#Pvalues choice

#Raise errors on non-numeric input choice
non_numeric_errors_options = ("Select error handling...", "Raise errors", "Ignore case-wise")
non_numeric_errors_drop = ttk.Combobox(non_numeric_input_raise_errors_Frame, values=non_numeric_errors_options, state="readonly", width=30, textvariable=non_numeric_input_raise_errors_tk)
non_numeric_errors_drop.current(0)
non_numeric_errors_drop.grid(row=0, column=0)

#Output descriptives for Raw t-tests
raw_ttest_output_descriptives_drop = ttk.Combobox(raw_ttest_output_descriptives_Frame, values=["No", "Yes"], state="readonly", width=30, textvariable=raw_ttest_output_descriptives_tk)
raw_ttest_output_descriptives_drop.current(0)
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