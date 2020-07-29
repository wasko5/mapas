import decision_funcs
import global_vars
import helper_funcs
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from webbrowser import open_new
import sys
import os
import traceback




def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'): 
         return os.path.join(sys._MEIPASS, relative_path) # pylint: disable=no-member
     return os.path.join(os.path.abspath("."), relative_path)

master = tk.Tk()
master.title("Multi-test corrections and APA tables Software (MAPAS)")
master.iconphoto(True, tk.PhotoImage(file=resource_path(os.path.join("Images", "MAPAS_logo_temp.png"))))
master.resizable(False, False)

s = ttk.Style()
s.configure("TLabelframe", padding=5, borderwidth=3)

#------------------------------------Variable and Frame declaration
columns_current_indices_dict = {}
previous_combobox_vals_dict = {}

input_path_and_filename_tk = tk.StringVar()
alpha_threshold_tk = tk.StringVar()
output_filename_tk = tk.StringVar()
output_filetype_tk = tk.StringVar()

input_type_tk = tk.StringVar()

raw_test_tk = tk.StringVar()

raw_corr_type_tk = tk.StringVar()
raw_corr_vars_tk = tk.StringVar()
raw_mr_outcomevar_tk = tk.StringVar()
raw_indttest_groupvar_tk = tk.StringVar()
raw_indttest_grouplevel1_tk = tk.StringVar()
raw_indttest_grouplevel2_tk = tk.StringVar()
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
spss_pairttest_n_tk = tk.StringVar()

pvalues_col_tk = tk.StringVar()

effect_size_choice_tk = tk.StringVar()
correction_type_tk = tk.StringVar()

non_numeric_input_raise_errors_tk = tk.StringVar()

#resets variables to default but does not include input variables or alpha as it is used in functions below
def set_variables_default():
	raw_test_tk.set(global_vars.tk_vars_defaults["raw_test_tk"])

	raw_corr_type_tk.set(global_vars.tk_vars_defaults["raw_corr_type_tk"])
	raw_mr_outcomevar_tk.set(global_vars.tk_vars_defaults["raw_mr_outcomevar_tk"])
	raw_indttest_groupvar_tk.set(global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"])
	raw_indttest_grouplevel1_tk.set(global_vars.tk_vars_defaults["raw_indttest_grouplevel1_tk"])
	raw_indttest_grouplevel2_tk.set(global_vars.tk_vars_defaults["raw_indttest_grouplevel2_tk"])
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
	spss_pairttest_n_tk.set(global_vars.tk_vars_defaults["spss_pairttest_n_tk"])

	pvalues_col_tk.set(global_vars.tk_vars_defaults["pvalues_col_tk"])

	effect_size_choice_tk.set(global_vars.tk_vars_defaults["effect_size_choice_tk"])
	correction_type_tk.set(global_vars.tk_vars_defaults["correction_type_tk"])

	non_numeric_input_raise_errors_tk.set(global_vars.tk_vars_defaults["non_numeric_input_raise_errors_tk"])

#set all variables to default at start
input_type_tk.set(global_vars.tk_vars_defaults["input_type_tk"])
input_path_and_filename_tk.set(global_vars.tk_vars_defaults["input_path_and_filename_tk"])
output_filename_tk.set(global_vars.tk_vars_defaults["output_filename_tk"])
output_filetype_tk.set(global_vars.tk_vars_defaults["output_filetype_tk"])
alpha_threshold_tk.set(global_vars.tk_vars_defaults["alpha_threshold_tk"])
set_variables_default()

#frames are structured so that input file and alpha threshold are on the first row of the master,
#the second row is the input type (mutliple choice)
#the third row is the entire tests_specifications_master_Frame, which is further broken down into the test-specific frames
#the fourth row is the output file button and the submit button
#Note: rows are 0-indexed
input_filename_Frame = ttk.LabelFrame(master, text="Choose input file")
input_filename_Frame.grid(row=0, column=0, columnspan=2, sticky="NW", padx=15, pady=5)

alpha_threshold_Frame = ttk.LabelFrame(master, text="Alpha criterion")
alpha_threshold_Frame.grid(row=0, column=2, sticky="E", padx=(0,15), pady=5)

output_filename_Frame = ttk.LabelFrame(master, text="Save output")
output_filename_Frame.grid(row=3, column=0, columnspan=2, sticky="NW", padx=15, pady=5)

input_type_Frame = ttk.LabelFrame(master, text="Select input type:")
input_type_Frame.grid(row=1, column=0, columnspan=3, sticky="NW", padx=15, pady=5)

test_specifications_master_Frame = tk.Frame(master)
test_specifications_master_Frame.grid(row=2, column=0, columnspan=3, sticky="NW", padx=15)

raw_test_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Statistical test")

raw_corr_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Correlation type")
raw_corr_vars_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Variables to correlate")

raw_mr_outcomevar_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Outcome variable")
raw_mr_predictors_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Predictors")

raw_indttest_groupvar_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Grouping variable")
raw_indttest_grouplevels_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Groups")
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
summ_indttest_equal_var_Frame = ttk.LabelFrame(summ_indttest_master_Frame, text="Equal variances column (optional)")
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

spss_get_table_info_Frame = tk.Frame(master)
spss_test_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Statistical test")
spss_indttest_sampleSize_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Sample size")
spss_indttest_groupLabels_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Group labels (optional)")
spss_pairttest_sampleSize_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Sample size")

pvalues_col_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="P-values column")

col_names_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Your variables")

effect_size_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Effect size")
correction_type_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="Correction type")

non_numeric_input_raise_errors_Frame = ttk.LabelFrame(test_specifications_master_Frame, text="How to handle non-numeric cases?")

#-----------------------------------------------Helper functions
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
	current_sel_ind = list(col_names_lb.curselection())
	current_sel_items = [col_names_lb.get(ele) for ele in current_sel_ind]
	
	listbox.insert(tk.END, *current_sel_items)
	delete_lbitems(col_names_lb, ind=current_sel_ind)

def move_lbvars_to_master(listbox): 
	current_sel_ind = list(listbox.curselection())
	current_sel_items = []
	if global_vars.master_dict[raw_test_tk.get()] == "pairttest":
		for ind in current_sel_ind:
			for item in listbox.get(ind).split(" <---> "):
				current_sel_items.append(item)
	else:
		current_sel_items = [listbox.get(ele) for ele in current_sel_ind]

	if not any(val in global_vars.tk_vars_defaults.values() for val in current_sel_items): #avoids adding default combobox values to listboxes
		move_back_to_master(current_sel_items)

	delete_lbitems(listbox, ind=current_sel_ind)

def move_back_to_master(items):
	for item in items:
		update_columns_current_indices_dict()
		if item not in col_names_lb.get(0, tk.END):
		#this if handles the following case: on pairttest select var1-var2 and add, then select var3-var4 and add, then select var5 and BEFORE
		#selecting anything else, select the added var3 <---> var4 pair and remove it; then as pair to the already selected var5, select anything but var4
		#the result will be 2 var4s in the master lb as the previous value coincides with an already existing value
			current_ind_arr = list(columns_current_indices_dict.values())
			index_to_start_search = list(columns_current_indices_dict.keys()).index(item)
			for loop_ind, ele_ind in enumerate(current_ind_arr[index_to_start_search:]):
				if loop_ind + index_to_start_search == len(current_ind_arr[index_to_start_search:]) + index_to_start_search - 1 and ele_ind == -1:
					#corner case - checks if the item to be moved back should be last
					insert_in_master_lb(tk.END, item)
				if ele_ind != -1:
					insert_in_master_lb(ele_ind, item)
					break

def insert_in_master_lb(ind, item):
	if item in columns_current_indices_dict.keys():
		col_names_lb.insert(ind, item)

def delete_lbitems(listbox, values=[], ind=[]):
	if values != []:
		lb_items = listbox.get(0, tk.END)
		ind = []
		for val in values:
			ind.append(lb_items.index(val))

	for i in ind[::-1]:
		listbox.delete(i)

def update_columns_current_indices_dict():
	col_names_lb_current = list(col_names_lb.get(0, tk.END))  
	for key in columns_current_indices_dict.keys():
		if key not in col_names_lb_current:
			columns_current_indices_dict[key] = -1
		else:
			columns_current_indices_dict[key] = col_names_lb_current.index(key)

def reset_columns_dict_and_lb():
	col_names_lb.delete(0, tk.END)
	col_names_lb.insert(tk.END, *list(columns_current_indices_dict.keys()))

	for ind, ele in enumerate(list(columns_current_indices_dict.keys())):
		columns_current_indices_dict[ele] = ind

def reset_all_lb():
	reset_columns_dict_and_lb()
	raw_corr_vars_lb.delete(0, tk.END)
	raw_mr_predictors_lb.delete(0, tk.END)
	raw_indttest_dv_lb.delete(0, tk.END)
	raw_pairttest_pairs_lb.delete(0, tk.END)


def pairttest_remove_added_vars_from_master():
	col_names_lb_vars = col_names_lb.get(0, tk.END)
	pairttest_added_vars = [var for pair in list(raw_pairttest_pairs_lb.get(0, tk.END)) for var in pair.split(" <---> ")]

	for var in pairttest_added_vars:
		if var in col_names_lb_vars:
			delete_lbitems(col_names_lb, values=[var])

def move_comboboboxvar_to_master(event):
	combobox_id = str(event.widget) #takes advantage of the fact that a combobox is linked to a single variable
	combobox_current_val = event.widget.getvar(event.widget.cget("textvariable"))
	if combobox_id in previous_combobox_vals_dict.keys():
		combobox_prev_val = previous_combobox_vals_dict[combobox_id]
	else:
		combobox_prev_val = ""

	if combobox_prev_val != "" and combobox_prev_val != global_vars.dropdown_unselected_file_msg:
		move_back_to_master([combobox_prev_val])

	if combobox_id == ".!frame.!labelframe9.!frame.!combobox" or combobox_id == ".!frame.!labelframe9.!frame.!combobox2": #ids for the 2 pairttest dropdowns
		pairttest_remove_added_vars_from_master()

	previous_combobox_vals_dict[combobox_id] = combobox_current_val
	delete_lbitems(col_names_lb, values=[combobox_current_val])
	update_columns_current_indices_dict()

#-----------------------------------------------------Layout control
def remove_frames(frames_list):
	for frame in frames_list:
		frame.grid_remove()

def input_type_frames_layout():
	#the only frames it does not include are master or input_type
	frames_list = [raw_test_Frame, raw_corr_Frame, raw_corr_vars_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame,
					raw_indttest_grouplevels_Frame, raw_indttest_dv_Frame, raw_pairttest_master_Frame, summ_corr_master_Frame, summ_indttest_master_Frame,
					spss_get_table_info_Frame, spss_test_Frame, spss_indttest_sampleSize_Frame, spss_indttest_groupLabels_Frame, spss_pairttest_sampleSize_Frame,
					pvalues_col_Frame, col_names_Frame, effect_size_Frame, correction_type_Frame, non_numeric_input_raise_errors_Frame]

	
	set_variables_default()
	reset_all_lb()
	remove_frames(frames_list)
	test_specifications_master_Frame.grid_rowconfigure(index=1, weight=0)

	if input_type_tk.get() == "raw":
		raw_test_Frame.grid(row=0, column=0, sticky="NW")
	elif input_type_tk.get() == "summ_corr":
		correction_type_Frame.grid(row=0, column=0, rowspan=1, sticky="NW", padx=0, pady=0)
		summ_corr_master_Frame.grid(row=0, column=1, columnspan=2, sticky="NW", padx=(15, 0), pady=0)
	elif input_type_tk.get() == "summ_indttest":
		test_specifications_master_Frame.grid_rowconfigure(index=1, weight=1)
		correction_type_Frame.grid(row=0, column=0, rowspan=1, sticky="NW", padx=(0, 15), pady=0)
		effect_size_Frame.grid(row=1, column=0, sticky="NW", padx=(0, 15), pady=5)
		summ_indttest_master_Frame.grid(row=0, column=1, columnspan=2, rowspan=2, sticky="NW", padx=0, pady=0)
	elif input_type_tk.get() == "spss":
		spss_test_Frame.grid(row=0, column=0, sticky="NW")
		spss_get_table_info_Frame.grid(row=2, column=2, sticky="NE", padx=15, pady=0)
	elif input_type_tk.get() == "pvalues":
		correction_type_Frame.grid(row=0, column=0, rowspan=1, sticky="NW", padx=0, pady=0)
		pvalues_col_Frame.grid(row=0, column=1, rowspan=1, sticky="NW", padx=15, pady=0)

def raw_test_clear_vars():
	raw_corr_type_tk.set(global_vars.tk_vars_defaults["raw_corr_type_tk"])
	raw_mr_outcomevar_tk.set(global_vars.tk_vars_defaults["raw_mr_outcomevar_tk"])
	raw_indttest_groupvar_tk.set(global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"])
	raw_pairttest_var1_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var1_tk"])
	raw_pairttest_var2_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var2_tk"])
	effect_size_choice_tk.set(global_vars.tk_vars_defaults["effect_size_choice_tk"])
	non_numeric_input_raise_errors_tk.set(global_vars.tk_vars_defaults["non_numeric_input_raise_errors_tk"])

def raw_test_frames_layout(event):
	frames_list = [raw_corr_Frame, raw_corr_vars_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame, raw_indttest_grouplevels_Frame,
					raw_indttest_dv_Frame, raw_pairttest_master_Frame, col_names_Frame, effect_size_Frame, correction_type_Frame, non_numeric_input_raise_errors_Frame]

	raw_test_clear_vars()
	reset_all_lb()
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
		correction_type_Frame.grid(row=1, column=0, rowspan=1, sticky="NW", padx=0, pady=5)
		effect_size_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=0)
		non_numeric_input_raise_errors_Frame.grid(row=3, column=0, sticky="NW", padx=0, pady=5)
		col_names_Frame.grid(row=0, column=1, rowspan=4, sticky="NW", padx=(15, 0), pady=0)
		raw_indttest_groupvar_Frame.grid(row=0, column=2, sticky="NW", padx=15, pady=0)
		raw_indttest_grouplevels_Frame.grid(row=1, column=2, sticky="NW", padx=15, pady=5)
		raw_indttest_dv_Frame.grid(row=2, column=2, rowspan=2, sticky="NW", padx=15, pady=0)
	elif global_vars.master_dict[raw_test_tk.get()] == "pairttest":
		correction_type_Frame.grid(row=1, column=0, rowspan=1, sticky="NW", padx=0, pady=5)
		effect_size_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=0)
		non_numeric_input_raise_errors_Frame.grid(row=3, column=0, sticky="NW", padx=0, pady=5)
		raw_pairttest_master_Frame.grid(row=0, column=1, rowspan=4, sticky="NW", padx=15, pady=0)

def spss_test_clear_vars():
	spss_indttest_nOne_tk.set(global_vars.tk_vars_defaults["spss_indttest_nOne_tk"])
	spss_indttest_nTwo_tk.set(global_vars.tk_vars_defaults["spss_indttest_nTwo_tk"])
	spss_indttest_groupOneLabel_tk.set(global_vars.tk_vars_defaults["spss_indttest_groupOneLabel_tk"])
	spss_indttest_groupTwoLabel_tk.set(global_vars.tk_vars_defaults["spss_indttest_groupTwoLabel_tk"])
	spss_pairttest_n_tk.set(global_vars.tk_vars_defaults["spss_pairttest_n_tk"])

	correction_type_tk.set(global_vars.tk_vars_defaults["correction_type_tk"])
	effect_size_choice_tk.set(global_vars.tk_vars_defaults["effect_size_choice_tk"])

def spss_test_frames_layout(event):
	frames_list = [spss_indttest_sampleSize_Frame, spss_indttest_groupLabels_Frame, spss_pairttest_sampleSize_Frame, effect_size_Frame, correction_type_Frame]

	spss_test_clear_vars()
	remove_frames(frames_list)

	if global_vars.master_dict[spss_test_tk.get()] == "corr":
		correction_type_Frame.grid(row=1, column=0, rowspan=1, sticky="NW", padx=0, pady=(5, 0))
	elif global_vars.master_dict[spss_test_tk.get()] == "mr":
		pass #i.e. nothing needs to be done
	elif global_vars.master_dict[spss_test_tk.get()] == "indttest":
		correction_type_Frame.grid(row=1, column=0, rowspan=4, sticky="NW", padx=0, pady=5)
		effect_size_Frame.grid(row=5, column=0, sticky="NW", padx=0, pady=0)
		spss_indttest_sampleSize_Frame.grid(row=0, column=1, rowspan=3, sticky="NW", padx=15, pady=(0, 5))
		spss_indttest_groupLabels_Frame.grid(row=3, column=1, rowspan=3, sticky="NW", padx=15, pady=0)
	elif global_vars.master_dict[spss_test_tk.get()] == "pairttest":
		correction_type_Frame.grid(row=1, column=0, rowspan=1, sticky="NW", padx=(0, 15), pady=5)
		effect_size_Frame.grid(row=2, column=0, sticky="NW", padx=0, pady=0)
		spss_pairttest_sampleSize_Frame.grid(row=0, column=1, rowspan=3, sticky="NW", padx=0, pady=0)

#---------------------------------------------------------------GUI Content
#Input file button & label
def select_file():
	path_and_filename = askopenfilename(initialdir = resource_path(""), title="Select file (.xlsx or .csv)", filetypes=(("Excel files",".xlsx .csv"),("All files","*.*")))
	
	if path_and_filename.endswith(".xlsx") or path_and_filename.endswith(".csv"):
		try:
			df_cols = helper_funcs.get_df_columns(path_and_filename)
			update_filename_label(filename = path_and_filename[path_and_filename.rfind("/")+1:], label = filename_label, char_limit=50)
			if input_path_and_filename_tk.get() != global_vars.tk_vars_defaults["input_path_and_filename_tk"]:
				columns_current_indices_dict.clear()
				reset_all_lb()
				set_variables_default()
				input_type_frames_layout()

			input_path_and_filename_tk.set(path_and_filename)

			df_cols = helper_funcs.get_df_columns(path_and_filename)
			col_names_lb.configure(state="normal")
			col_names_lb.delete(0, tk.END)
			col_names_lb.insert(tk.END, *df_cols)
			for ind, col in enumerate(df_cols):
				columns_current_indices_dict[col] = ind
		except Exception as error_msg:
			messagebox.showerror("Oh-oh!", error_msg)

	elif path_and_filename != "":
		messagebox.showerror("Oh-oh!", "Please select a valid .xlsx or .csv file.")

ttk.Button(input_filename_Frame, text="Select file (.xlsx or .csv)", command=select_file).grid(row=0, column=0, sticky="W", padx=(0, 10))
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
col_names_lb.insert(0, global_vars.dropdown_unselected_file_msg)
col_names_lb.configure(state="disabled")

#Input Type
input_type_Dict = {"Raw data" : "raw", "Correlations from summary statistics" : "summ_corr", 
					"Independent t-test from summary statistics" : "summ_indttest", "SPSS table" : "spss",
					"p values" : "pvalues"}
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
raw_corr_vars_remove_btn = ttk.Button(raw_corr_vars_Frame, text="X", command=lambda listbox=raw_corr_vars_lb: move_lbvars_to_master(listbox))
raw_corr_vars_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Multiple Regression // Outcome variable
raw_mr_outcomevar_drop = ttk.Combobox(raw_mr_outcomevar_Frame, state="readonly", width=30, textvariable=raw_mr_outcomevar_tk)
raw_mr_outcomevar_drop.configure(postcommand=lambda dropdown=raw_mr_outcomevar_drop: get_values_for_dropdown(dropdown))
raw_mr_outcomevar_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
raw_mr_outcomevar_drop.grid(row=0, column=0)

#Raw data // test // Multiple Regression // Predictors
raw_mr_predictors_lb = tk.Listbox(raw_mr_predictors_Frame, selectmode="extended", height=7, width=23)
raw_mr_predictors_scroll_y = ttk.Scrollbar(raw_mr_predictors_Frame, orient="vertical", command=raw_mr_predictors_lb.yview)
raw_mr_predictors_lb.configure(yscrollcommand=raw_mr_predictors_scroll_y.set)
raw_mr_predictors_lb.grid(row=0, column=1, rowspan=2, sticky="W")
raw_mr_predictors_scroll_y.grid(row=0, column=2, rowspan=2, sticky="NS")

raw_mr_predictors_add_btn = ttk.Button(raw_mr_predictors_Frame, text="--->", command=lambda listbox=raw_mr_predictors_lb: add_variables_to_listbox(listbox))
raw_mr_predictors_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))
raw_mr_predictors_remove_btn = ttk.Button(raw_mr_predictors_Frame, text="X", command=lambda listbox=raw_mr_predictors_lb: move_lbvars_to_master(listbox))
raw_mr_predictors_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Independent samples t-test // Grouping variable
raw_indttest_groupvar_drop = ttk.Combobox(raw_indttest_groupvar_Frame, state="readonly", width=30, textvariable=raw_indttest_groupvar_tk)
raw_indttest_groupvar_drop.configure(postcommand=lambda dropdown=raw_indttest_groupvar_drop: get_values_for_dropdown(dropdown))
raw_indttest_groupvar_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
raw_indttest_groupvar_drop.grid(row=0, column=0)


#Raw data // test // Independent samples t-test // Grouping variable
def get_values_for_raw_indttest_dropdowns(dropdown):
	if input_path_and_filename_tk != "" and raw_indttest_groupvar_tk.get() != global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"] and raw_indttest_groupvar_tk.get() != global_vars.dropdown_unselected_file_msg:
		try:
			dropdown.configure(values=helper_funcs.get_raw_indttest_grouplevels(input_path_and_filename_tk.get(), raw_indttest_groupvar_tk.get()))
		except Exception as error_msg:
			messagebox.showerror("Oh-oh!", error_msg)

def raw_indttest_dropdowns_validation(event):
	if raw_indttest_grouplevel1_tk.get() == raw_indttest_grouplevel2_tk.get():
		messagebox.showerror("Oh-oh!", "You can't select the same level for both groups. Please choose different levels of your grouping variable.")

raw_indttest_grouplevels_drop1 = ttk.Combobox(raw_indttest_grouplevels_Frame, state="readonly", width=15, textvariable=raw_indttest_grouplevel1_tk)
raw_indttest_grouplevels_drop1.configure(postcommand=lambda dropdown=raw_indttest_grouplevels_drop1: get_values_for_raw_indttest_dropdowns(dropdown))
raw_indttest_grouplevels_drop1.bind("<<ComboboxSelected>>", raw_indttest_dropdowns_validation)
raw_indttest_grouplevels_drop1.grid(row=0, column=0, padx=(0, 10))

raw_indttest_grouplevels_drop2 = ttk.Combobox(raw_indttest_grouplevels_Frame, state="readonly", width=15, textvariable=raw_indttest_grouplevel2_tk)
raw_indttest_grouplevels_drop2.configure(postcommand=lambda dropdown=raw_indttest_grouplevels_drop2: get_values_for_raw_indttest_dropdowns(dropdown))
raw_indttest_grouplevels_drop2.bind("<<ComboboxSelected>>", raw_indttest_dropdowns_validation)
raw_indttest_grouplevels_drop2.grid(row=0, column=1)

#Raw data // test // Independent samples t-test // DVs
raw_indttest_dv_lb = tk.Listbox(raw_indttest_dv_Frame, selectmode="extended", height=5, width=23)
raw_indttest_dv_scroll_y = ttk.Scrollbar(raw_indttest_dv_Frame, orient="vertical", command=raw_indttest_dv_lb.yview)
raw_indttest_dv_lb.configure(yscrollcommand=raw_indttest_dv_scroll_y.set)
raw_indttest_dv_lb.grid(row=0, column=1, rowspan=2, sticky="W")
raw_indttest_dv_scroll_y.grid(row=0, column=2, rowspan=2, sticky="NS")

raw_indttest_dv_add_btn = ttk.Button(raw_indttest_dv_Frame, text="--->", command=lambda listbox=raw_indttest_dv_lb: add_variables_to_listbox(listbox)) 
raw_indttest_dv_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))
raw_indttest_dv_remove_btn = ttk.Button(raw_indttest_dv_Frame, text="X", command=lambda listbox=raw_indttest_dv_lb: move_lbvars_to_master(listbox))
raw_indttest_dv_remove_btn.grid(row=1, column=0, sticky="EWNS", padx=(5, 5), pady=(5, 5))

#Raw data // test // Paired samples t-test // Pair choices
raw_pairttest_var1_label = ttk.Label(raw_pairttest_pairs_Frame, text="Select the first variable")
raw_pairttest_var1_label.grid(row=0, column=0, sticky="NW", padx=(0,15), pady=0)
raw_pairttest_var1_drop = ttk.Combobox(raw_pairttest_pairs_Frame, state="readonly", width=20, textvariable=raw_pairttest_var1_tk)
raw_pairttest_var1_drop.configure(postcommand=lambda dropdown=raw_pairttest_var1_drop: get_values_for_dropdown(dropdown))
raw_pairttest_var1_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
raw_pairttest_var1_drop.grid(row=1, column=0, sticky="NW", padx=(0,15), pady=0)

raw_pairttest_var2_label = ttk.Label(raw_pairttest_pairs_Frame, text="Select the second variable")
raw_pairttest_var2_label.grid(row=0, column=1, sticky="NW")
raw_pairttest_var2_drop = ttk.Combobox(raw_pairttest_pairs_Frame, state="readonly", width=20, textvariable=raw_pairttest_var2_tk)
raw_pairttest_var2_drop.configure(postcommand=lambda dropdown=raw_pairttest_var2_drop: get_values_for_dropdown(dropdown))
raw_pairttest_var2_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
raw_pairttest_var2_drop.grid(row=1, column=1, sticky="NW")

#Raw data // test // Paired samples t-test // Pairs - buttons and listbox
def raw_pairttest_add_pair():
	if (raw_pairttest_var1_tk.get() == global_vars.tk_vars_defaults["raw_pairttest_var1_tk"] or raw_pairttest_var2_tk.get() == global_vars.tk_vars_defaults["raw_pairttest_var2_tk"] 
		or raw_pairttest_var1_tk.get() == global_vars.dropdown_unselected_file_msg or raw_pairttest_var2_tk.get() == global_vars.dropdown_unselected_file_msg):
		messagebox.showerror("Error!", "Please select both variable columns of your pair.")
	else:
		raw_pairttest_pairs_lb.insert(tk.END, "{p1} <---> {p2}".format(p1=raw_pairttest_var1_tk.get(), p2=raw_pairttest_var2_tk.get()))
		raw_pairttest_var1_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var1_tk"])
		raw_pairttest_var2_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var2_tk"])

raw_pairttest_pairs_lb = tk.Listbox(raw_pairttest_btn_list_Frame, selectmode="extended", height=8, width=40)
raw_pairttest_pairs_scroll_y = ttk.Scrollbar(raw_pairttest_btn_list_Frame, orient="vertical", command=raw_pairttest_pairs_lb.yview)
raw_pairttest_pairs_lb.configure(yscrollcommand=raw_pairttest_pairs_scroll_y.set)
raw_pairttest_pairs_lb.grid(row=1, column=0, columnspan=2, sticky="NW", pady=(10,0))
raw_pairttest_pairs_scroll_y.grid(row=1, column=3, sticky="NS")

raw_pairttest_add_btn = ttk.Button(raw_pairttest_btn_list_Frame, text="Add pair", command=raw_pairttest_add_pair)
raw_pairttest_add_btn.grid(row=0, column=0, sticky="EWNS", padx=(0,50))
raw_pairttest_remove_btn = ttk.Button(raw_pairttest_btn_list_Frame, text="Remove", command=lambda listbox=raw_pairttest_pairs_lb: move_lbvars_to_master(listbox))
raw_pairttest_remove_btn.grid(row=0, column=1, sticky="EWNS")

#Summary statistics - Correlations
summ_corr_varOne_drop = ttk.Combobox(summ_corr_varOne_Frame, state="readonly", width=30, textvariable=summ_corr_varOne_tk)
summ_corr_varOne_drop.configure(postcommand=lambda dropdown=summ_corr_varOne_drop: get_values_for_dropdown(dropdown))
summ_corr_varOne_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_corr_varOne_drop.grid(row=0, column=0)

summ_corr_varTwo_drop = ttk.Combobox(summ_corr_varTwo_Frame, state="readonly", width=30, textvariable=summ_corr_varTwo_tk)
summ_corr_varTwo_drop.configure(postcommand=lambda dropdown=summ_corr_varTwo_drop: get_values_for_dropdown(dropdown))
summ_corr_varTwo_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_corr_varTwo_drop.grid(row=0, column=0)

summ_corr_coeff_drop = ttk.Combobox(summ_corr_coeff_Frame, state="readonly", width=30, textvariable=summ_corr_coeff_tk)
summ_corr_coeff_drop.configure(postcommand=lambda dropdown=summ_corr_coeff_drop: get_values_for_dropdown(dropdown))
summ_corr_coeff_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_corr_coeff_drop.grid(row=0, column=0)

summ_corr_pvalues_drop = ttk.Combobox(summ_corr_pvalues_Frame, state="readonly", width=30, textvariable=summ_corr_pvalues_tk)
summ_corr_pvalues_drop.configure(postcommand=lambda dropdown=summ_corr_pvalues_drop: get_values_for_dropdown(dropdown))
summ_corr_pvalues_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_corr_pvalues_drop.grid(row=0, column=0)

#Summary statistics - Independent samples t-test
summ_indttest_var_drop = ttk.Combobox(summ_indttest_var_Frame, state="readonly", width=30, textvariable=summ_indttest_var_tk)
summ_indttest_var_drop.configure(postcommand=lambda dropdown=summ_indttest_var_drop: get_values_for_dropdown(dropdown))
summ_indttest_var_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_var_drop.grid(row=0, column=0)

summ_indttest_equal_var_drop = ttk.Combobox(summ_indttest_equal_var_Frame, state="readonly", width=30, textvariable=summ_indttest_equal_var_tk)
summ_indttest_equal_var_drop.configure(postcommand=lambda dropdown=summ_indttest_equal_var_drop: get_values_for_dropdown(dropdown))
summ_indttest_equal_var_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_equal_var_drop.grid(row=0, column=0)

summ_indttest_meanOne_drop = ttk.Combobox(summ_indttest_meanOne_Frame, state="readonly", width=30, textvariable=summ_indttest_meanOne_tk)
summ_indttest_meanOne_drop.configure(postcommand=lambda dropdown=summ_indttest_meanOne_drop: get_values_for_dropdown(dropdown))
summ_indttest_meanOne_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_meanOne_drop.grid(row=0, column=0)

summ_indttest_sdOne_drop = ttk.Combobox(summ_indttest_sdOne_Frame, state="readonly", width=30, textvariable=summ_indttest_sdOne_tk)
summ_indttest_sdOne_drop.configure(postcommand=lambda dropdown=summ_indttest_sdOne_drop: get_values_for_dropdown(dropdown))
summ_indttest_sdOne_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_sdOne_drop.grid(row=0, column=0)

summ_indttest_nOne_drop = ttk.Combobox(summ_indttest_nOne_Frame, state="readonly", width=30, textvariable=summ_indttest_nOne_tk)
summ_indttest_nOne_drop.configure(postcommand=lambda dropdown=summ_indttest_nOne_drop: get_values_for_dropdown(dropdown))
summ_indttest_nOne_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_nOne_drop.grid(row=0, column=0)

summ_indttest_meanTwo_drop = ttk.Combobox(summ_indttest_meanTwo_Frame, state="readonly", width=30, textvariable=summ_indttest_meanTwo_tk)
summ_indttest_meanTwo_drop.configure(postcommand=lambda dropdown=summ_indttest_meanTwo_drop: get_values_for_dropdown(dropdown))
summ_indttest_meanTwo_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_meanTwo_drop.grid(row=0, column=0)

summ_indttest_sdTwo_drop = ttk.Combobox(summ_indttest_sdTwo_Frame, state="readonly", width=30, textvariable=summ_indttest_sdTwo_tk)
summ_indttest_sdTwo_drop.configure(postcommand=lambda dropdown=summ_indttest_sdTwo_drop: get_values_for_dropdown(dropdown))
summ_indttest_sdTwo_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_sdTwo_drop.grid(row=0, column=0)

summ_indttest_nTwo_drop = ttk.Combobox(summ_indttest_nTwo_Frame, state="readonly", width=30, textvariable=summ_indttest_nTwo_tk)
summ_indttest_nTwo_drop.configure(postcommand=lambda dropdown=summ_indttest_nTwo_drop: get_values_for_dropdown(dropdown))
summ_indttest_nTwo_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
summ_indttest_nTwo_drop.grid(row=0, column=0)

#SPSS // SPSS table additional info
def spss_table_info_popup(event):
	#good enough.........
	top = tk.Toplevel()
	top.grab_set()
	top.title("Exporting SPSS table")
	def exit(event):
		top.destroy()
	top.bind("<Escape>", exit)

	frame = tk.Frame(top)
	frame.grid(row=0, column=0)

	canvas = tk.Canvas(frame)
	canvas.grid(row=0, column=0)

	img_1 = tk.PhotoImage(file=resource_path(os.path.join("Images", "spss_instr3.gif")))
	img_1_label = tk.Label(canvas, image=img_1)
	img_1_label.image = img_1
	img_1_label.grid(row=0, column=0)

	center(top)

spss_table_info_label = ttk.Label(spss_get_table_info_Frame, text="How to export an SPSS table?", foreground="blue", cursor="hand2")
spss_table_info_label.grid(row=0, column=0, sticky="NE", padx=0, pady=5)
spss_table_info_label.bind("<Button-1>", spss_table_info_popup)

#SPSS // test
spss_test_options = ("Correlations", "(Multiple) Regression - Standard", "Independent Samples t-test", "Paired samples t-test")
spss_test_drop = ttk.Combobox(spss_test_Frame, values=spss_test_options, state="readonly", width=30, textvariable=spss_test_tk)
spss_test_drop.bind("<<ComboboxSelected>>", spss_test_frames_layout)
spss_test_drop.grid(row=0, column=0)

#SPSS // test // Independent samples t-test // Sample Size
ttk.Label(spss_indttest_sampleSize_Frame, text="Used for calculating effect size (if selected)").grid(row=0, column=0, columnspan=2, sticky="NWES", padx=5, pady=(0,5))
ttk.Label(spss_indttest_sampleSize_Frame, text="Sample size of Group 1:").grid(row=1, column=0, sticky="NWES", padx=(0,5), pady=(0,5))
ttk.Entry(spss_indttest_sampleSize_Frame, textvariable=spss_indttest_nOne_tk, width=15).grid(row=1, column=1, sticky="NWES", pady=(0,5))
ttk.Label(spss_indttest_sampleSize_Frame, text="Sample size of Group 2:").grid(row=2, column=0, sticky="NWES", padx=(0,5))
ttk.Entry(spss_indttest_sampleSize_Frame, textvariable=spss_indttest_nTwo_tk, width=15).grid(row=2, column=1, sticky="NWES")

#SPSS // test // Independent samples t-test // Group Labels
ttk.Label(spss_indttest_groupLabels_Frame, text="Group 1:").grid(row=0, column=0, sticky="NWES", padx=(0,5))
ttk.Entry(spss_indttest_groupLabels_Frame, textvariable=spss_indttest_groupOneLabel_tk, width=20).grid(row=0, column=1, sticky="NWES", padx=(0,5))
ttk.Label(spss_indttest_groupLabels_Frame, text="Group 2:").grid(row=0, column=2, sticky="NWES", padx=(0,5))
ttk.Entry(spss_indttest_groupLabels_Frame, textvariable=spss_indttest_groupTwoLabel_tk, width=20).grid(row=0, column=3, sticky="NWES")

#SPSS // test // Paired samples t-test // Sample Size
ttk.Label(spss_pairttest_sampleSize_Frame, text="Used for calculating effect size (if selected)").grid(row=0, column=0, columnspan=2, sticky="NWES", padx=5, pady=(0,5))
ttk.Label(spss_pairttest_sampleSize_Frame, text="Number of valid pairs:").grid(row=1, column=0, sticky="NWES", padx=(0,5), pady=(0,5))
ttk.Entry(spss_pairttest_sampleSize_Frame, textvariable=spss_pairttest_n_tk, width=15).grid(row=1, column=1, sticky="NWES", pady=(0,5))

#Pvalues choice column
pvalues_col_drop = ttk.Combobox(pvalues_col_Frame, state="readonly", width=30, textvariable=pvalues_col_tk)
pvalues_col_drop.configure(postcommand=lambda dropdown=pvalues_col_drop: get_values_for_dropdown(dropdown))
pvalues_col_drop.bind("<<ComboboxSelected>>", move_comboboboxvar_to_master)
pvalues_col_drop.grid(row=0, column=0)

#Effect size choice
effect_size_options = ("Cohen's d", "Hedge's g", "Glass's delta", "None")
effect_size_drop = ttk.Combobox(effect_size_Frame, values=effect_size_options, state="readonly", width=30, textvariable=effect_size_choice_tk)
effect_size_drop.grid(row=0, column=0)

#Correction type choice
correction_type_options = ("Bonferroni",  "Sidak", "Holm-Sidak", "Holm-Bonferroni", "Simes-Hochberg", "Hommel", 
						"Benjamini-Hochberg", "Benjamini-Yekutieli", "Benjamini-Hochberg (2-stage)", 
						"Benjamini-Yekutieli (2-stage)", "None")
correction_type_drop = ttk.Combobox(correction_type_Frame, values=correction_type_options, state="readonly", width=30, textvariable=correction_type_tk)
correction_type_drop.grid(row=0, column=0)

#Raise errors on non-numeric input choice
non_numeric_errors_options = ("Raise errors", "Ignore pair-wise")
non_numeric_errors_drop = ttk.Combobox(non_numeric_input_raise_errors_Frame, values=non_numeric_errors_options, state="readonly", width=30, textvariable=non_numeric_input_raise_errors_tk)
non_numeric_errors_drop.grid(row=0, column=0)

#Output file button & label
def save_file():
	filename = asksaveasfilename(initialdir = resource_path(""), title = "Save output file...", filetypes = (("All files","*.*"), ("Excel files","*.xlsx"), ("Word files", "*.docx")))

	if filename != "":
		output_filename_tk.set(filename)
		update_filename_label(filename=filename, label=output_file_label, char_limit=70)

ttk.Button(output_filename_Frame, text="Save output file...", command=save_file).grid(row=0, column=0, sticky="NW", padx=(0, 10), pady=(0, 5))
output_file_label = ttk.Label(output_filename_Frame, text="Nothing selected yet.")
output_file_label.grid(row=0, column=1, sticky="W", pady=(0,5))
ttk.Label(output_filename_Frame, text="Save APA table in:").grid(row=1, column=0, sticky="NW", padx=(0, 10))
output_filetype_drop = ttk.Combobox(output_filename_Frame, values=("Excel",  "Word"), state="readonly", width=10, textvariable=output_filetype_tk)
output_filetype_drop.grid(row=1, column=1, sticky="W")

#----------------------------------------------------On Submit-related functions
def set_global_variables():
	global_vars.input_path_and_filename = input_path_and_filename_tk.get()
	try:
		global_vars.alpha_threshold = float(alpha_threshold_tk.get())
	except:
		raise Exception("Could not set an alpha of \'{}\'. Please enter a valid number. Example: 0.05 or 0.01".format(alpha_threshold_tk.get()))
	global_vars.output_filename = output_filename_tk.get()
	global_vars.output_filetype = output_filetype_tk.get()

	global_vars.input_type = "" if input_type_tk.get() == global_vars.tk_vars_defaults["input_type_tk"] else input_type_tk.get()

	global_vars.raw_test = "" if raw_test_tk.get() == global_vars.tk_vars_defaults["raw_test_tk"] else global_vars.master_dict[raw_test_tk.get()]

	global_vars.raw_corr_type =  "" if raw_corr_type_tk.get() == global_vars.tk_vars_defaults["raw_corr_type_tk"] else global_vars.master_dict[raw_corr_type_tk.get()]
	global_vars.raw_corr_vars = list(raw_corr_vars_lb.get(0, tk.END))
	global_vars.raw_mr_outcomevar = "" if raw_mr_outcomevar_tk.get() == global_vars.tk_vars_defaults["raw_mr_outcomevar_tk"] else raw_mr_outcomevar_tk.get()
	global_vars.raw_mr_predictors = list(raw_mr_predictors_lb.get(0, tk.END))
	global_vars.raw_indttest_groupvar = "" if raw_indttest_groupvar_tk.get() == global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"] else raw_indttest_groupvar_tk.get()
	global_vars.raw_indttest_grouplevel1 = "" if raw_indttest_grouplevel1_tk.get() == global_vars.tk_vars_defaults["raw_indttest_grouplevel1_tk"] else raw_indttest_grouplevel1_tk.get()
	global_vars.raw_indttest_grouplevel2 = "" if raw_indttest_grouplevel2_tk.get() == global_vars.tk_vars_defaults["raw_indttest_grouplevel2_tk"] else raw_indttest_grouplevel2_tk.get()
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
		if spss_indttest_nOne_tk.get() == "Enter an integer" or spss_indttest_nOne_tk.get() == "" or effect_size_choice_tk.get() == "None":
			global_vars.spss_indttest_nOne = -1
		else:
			global_vars.spss_indttest_nOne = int(spss_indttest_nOne_tk.get())
			if global_vars.spss_indttest_nOne <= 0:
				raise ValueError
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_indttest_nOne_tk.get()))
	try:
		if spss_indttest_nTwo_tk.get() == "Enter an integer" or spss_indttest_nTwo_tk.get() == "" or effect_size_choice_tk.get() == "None":
			global_vars.spss_indttest_nTwo = -1
		else:
			global_vars.spss_indttest_nTwo = int(spss_indttest_nTwo_tk.get())
			if global_vars.spss_indttest_nTwo <= 0:
				raise ValueError
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_indttest_nTwo_tk.get()))
	global_vars.spss_indttest_groupOneLabel = "Group1" if spss_indttest_groupOneLabel_tk.get() == "" else spss_indttest_groupOneLabel_tk.get()
	global_vars.spss_indttest_groupTwoLabel = "Group2" if spss_indttest_groupTwoLabel_tk.get() == "" else spss_indttest_groupTwoLabel_tk.get()
	try:
		if spss_pairttest_n_tk.get() == "Enter an integer" or spss_pairttest_n_tk.get() == "" or effect_size_choice_tk.get() == "None":
			global_vars.spss_pairttest_n = -1
		else:
			global_vars.spss_pairttest_n = int(spss_pairttest_n_tk.get())
			if global_vars.spss_pairttest_n <= 0:
				raise ValueError
	except ValueError:
		raise Exception("Could not set a sample size of {}. The number must be a positive integer. Example: 123 or 1021.".format(spss_pairttest_n_tk.get()))

	global_vars.pvalues_col = "" if pvalues_col_tk.get() == global_vars.tk_vars_defaults["pvalues_col_tk"] else pvalues_col_tk.get()

	global_vars.effect_size_choice = "no selection" if effect_size_choice_tk.get() == global_vars.tk_vars_defaults["effect_size_choice_tk"] else effect_size_choice_tk.get()
	if correction_type_tk.get() == global_vars.tk_vars_defaults["correction_type_tk"]:
		global_vars.correction_type = "no selection"
	elif global_vars.raw_test == "mr" or global_vars.spss_test == "mr":
		global_vars.correction_type = "None"
	else:
		global_vars.correction_type = global_vars.master_dict[correction_type_tk.get()]

	global_vars.correction_type = "no selection" if correction_type_tk.get() == global_vars.tk_vars_defaults["correction_type_tk"] else global_vars.master_dict[correction_type_tk.get()]

	global_vars.non_numeric_input_raise_errors = "" if non_numeric_input_raise_errors_tk.get() == global_vars.tk_vars_defaults["non_numeric_input_raise_errors_tk"] else global_vars.master_dict[non_numeric_input_raise_errors_tk.get()]

def input_validation():
	if global_vars.input_path_and_filename == "":
		raise Exception("Please select your input file.")
	if global_vars.input_type == "":
		raise Exception("Please first select the type of input data you are providing.")
	if global_vars.input_type == "raw":
		if global_vars.raw_test == "":
			raise Exception("Please select the statistical test you want to perform.")
		if global_vars.raw_test == "corr":
			if global_vars.raw_corr_type == "":
				raise Exception("Please select the kind of correlation (pearson, spearman, kendall) you want to perform.")
			if global_vars.correction_type == "no selection":
				raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("Please select how to handle non-numeric data.")
			if len(global_vars.raw_corr_vars) < 2:
				raise Exception("Please select 2 or more variables to correlation. You can do so by selected your variables from  the \"Your variables\" pane\nand move them across using the arrow button.")
		elif global_vars.raw_test == "mr":
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("Please select how to handle non-numeric data.")
			if global_vars.raw_mr_outcomevar == "" or global_vars.raw_mr_outcomevar == global_vars.dropdown_unselected_file_msg:
				raise Exception("Please select your outcome (dependent) variable.")
			if global_vars.raw_mr_predictors == ():
				raise Exception("Please select your at least 1 predictor (independent) variable. You can do so by selected your variables from  the \"Your variables\" pane\nand move them across using the arrow button.")
		elif global_vars.raw_test == "indttest":
			if global_vars.correction_type == "no selection":
				raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
			if global_vars.effect_size_choice == "no selection":
				raise Exception("Please select what effect size, if any, you want.")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("Please select how to handle non-numeric data.")
			if global_vars.raw_indttest_groupvar == "" or global_vars.raw_indttest_grouplevel1 == "" or global_vars.raw_indttest_grouplevel2 == "":
				raise Exception("Please select your grouping variables and the labels for the groups we are comparing.")
			if global_vars.raw_indttest_grouplevel1 == global_vars.raw_indttest_grouplevel2:
				raise Exception("You can't select the same level for both groups. Please choose different levels of your grouping variable.")
			if global_vars.raw_indttest_dv == []:
				raise Exception("Please select your dependent variables. You can do so by selected your variables from  the \"Your variables\" pane\nand move them across using the arrow button.")
		elif global_vars.raw_test == "pairttest":
			if global_vars.correction_type == "no selection":
				raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
			if global_vars.effect_size_choice == "no selection":
				raise Exception("Please select what effect size, if any, you want.")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("Please select how to handle non-numeric data.")
			if global_vars.raw_pairttest_var_pairs == ():
				raise Exception("Please add your pairs to the box using the dropdown menus and the buttons.")
	elif global_vars.input_type == "summ_corr":
		if global_vars.correction_type == "no selection":
			raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
		if global_vars.summ_corr_varOne == "" or global_vars.summ_corr_varOne == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your variable one labels.")
		if global_vars.summ_corr_varTwo == "" or global_vars.summ_corr_varTwo == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your variable two labels.")
		if global_vars.summ_corr_coeff == "" or global_vars.summ_corr_coeff == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your correlation coefficients.")
		if global_vars.summ_corr_pvalues == "" or global_vars.summ_corr_pvalues == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your pvalues.")
	elif global_vars.input_type == "summ_indttest":
		if global_vars.correction_type == "no selection":
			raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
		if global_vars.effect_size_choice == "no selection":
			raise Exception("Please select what effect size, if any, you want.")
		if global_vars.summ_indttest_var == "" or global_vars.summ_indttest_var == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your variable labels.")
		if global_vars.summ_indttest_meanOne == "" or global_vars.summ_indttest_meanOne == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your mean values for group 1.")
		if global_vars.summ_indttest_sdOne == "" or global_vars.summ_indttest_sdOne == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your standard deviation values for group 1.")
		if global_vars.summ_indttest_nOne == "" or global_vars.summ_indttest_nOne == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your sample size for group 1.")
		if global_vars.summ_indttest_meanTwo == "" or global_vars.summ_indttest_meanTwo == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your mean values for group 2.")
		if global_vars.summ_indttest_sdTwo == "" or global_vars.summ_indttest_sdTwo == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your standard deviation values for group 2.")
		if global_vars.summ_indttest_nTwo == "" or global_vars.summ_indttest_nTwo == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your sample size for group 2.")
	elif global_vars.input_type == "spss":
		if not global_vars.input_path_and_filename.endswith(".xlsx"):
			raise Exception("When SPSS table is provided, only .xlsx are allowed as input. Please click on the \"How to export an SPSS table?\" button or see the documentation at {}.".format(global_vars.software_page))
		if global_vars.spss_test == "":
			raise Exception("Please select what kind of SPSS table you are providing.")
		elif global_vars.spss_test == "corr":
			if global_vars.correction_type == "no selection":
				raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
		elif global_vars.spss_test == "mr":
			pass
		elif global_vars.spss_test == "indttest":
			if global_vars.correction_type == "no selection":
				raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
			if global_vars.effect_size_choice == "no selection":
				raise Exception("Please select what effect size, if any, you want.")
			if (global_vars.spss_indttest_nOne == -1 or global_vars.spss_indttest_nTwo == -1) and global_vars.effect_size_choice != "None":
				raise Exception("In order to add a {} effect size estimate, you will need provide your sample size.".format(global_vars.effect_size_choice))
		elif global_vars.spss_test == "pairttest":
			if global_vars.correction_type == "no selection":
				raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
			if global_vars.effect_size_choice == "no selection":
				raise Exception("Please select what effect size, if any, you want.")
			if global_vars.spss_pairttest_n == -1 and global_vars.effect_size_choice != "None":
				raise Exception("In order to add a {} effect size estimate, you will need provide your sample size.".format(global_vars.effect_size_choice))
	elif global_vars.input_type == "pvalues":
		if global_vars.correction_type == "no selection":
			raise Exception("Please select what kind of correction, if any, you want to apply to the data.")
		if global_vars.pvalues_col == "" or global_vars.pvalues_col == global_vars.dropdown_unselected_file_msg:
			raise Exception("Please select the column with your pvalues.")
		if global_vars.output_filetype == "Word":
			raise Exception("You can only export to Word if the output is an APA table. For a list of p values, please export to Excel.")

	if global_vars.effect_size_choice == "Glass's delta" and (global_vars.input_type == "summindttest" or global_vars.spss_test == "indttest" or global_vars.spss_test == "pairttest"):
		raise Exception("Oops - sorry! Glass's delta is not available for this type of test. Glass's delta can only be requested if raw data are provided. For more information, see the documentation.")
	
	if global_vars.output_filename == "":
		raise Exception("Please select where to save your output file.")

def clear_output_filename():
	output_filename_tk.set(global_vars.tk_vars_defaults["output_filename_tk"])
	output_file_label.config(text="Nothing selected yet.")
	
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

def submit_window():

	top = tk.Toplevel()
	top.grab_set()
	top.title("Thanks for using MAPAS!")
	def exit(event):
		top.destroy()
	top.bind("<Escape>", exit)

	some_message = '''Your file is ready and waiting for you.
	
	If you've found this software useful in your work, please cite us as:
	{}'''.format(global_vars.apa_reference)
	tk.Label(top, text=some_message).grid(row=0, column=0, columnspan=3, sticky="NWES", padx=15, pady=(5, 0))

	def openfilelocation():
		directory = global_vars.output_filename[:global_vars.output_filename.rfind("/")]
		open_new("file://" + directory)

	ttk.Button(top, text="Open file location", command=openfilelocation).grid(row=1, column=0, padx=(15, 0), pady=5)
	ttk.Button(top, text="I want to do more analysis", command=top.destroy).grid(row=1, column=1, padx=15, pady=5)
	ttk.Button(top, text="Close the app", command=master.destroy).grid(row=1,column=2, padx=(0, 15), pady=5)

	center(top)

def about_mapas_window():

	top = tk.Toplevel()
	top.grab_set()
	top.title("About MAPAS")
	def exit(event):
		top.destroy()
	top.bind("<Escape>", exit)

	some_message = '''This is MAPAS version: {v}.

	To learn more about the software, see:
	{a}'''.format(v=global_vars.version, a=global_vars.apa_reference)
	tk.Label(top, text=some_message).grid(row=0, column=0, columnspan=3, sticky="NWES", padx=15, pady=5)
	ttk.Button(top, text="Article page", command=lambda url=global_vars.article_link: open_new(url)).grid(row=1, column=0, padx=(15, 0), pady=(0, 5))
	ttk.Button(top, text="Software page", command=lambda url=global_vars.software_page: open_new(url)).grid(row=1, column=1, padx=15, pady=(0, 5))
	ttk.Button(top, text="Github repository", command=lambda url=global_vars.github_repository: open_new(url)).grid(row=1, column=2, padx=(0, 15), pady=(0, 5))

	center(top)

def log_error(traceback=None):
	log_filepath = asksaveasfilename(initialdir = resource_path(""), title = "Save log file as...", filetypes = (("Text files","*.txt"),("All files","*.*")))

	log_file = open(log_filepath + ".txt","w") 
	L = [
		"------------------------------Traceback details-----------------------",
		"{}".format(traceback),
		"--------------------------------Meta info-----------------------------",
		"OS: {}".format(sys.platform),
		"Software version: {}".format(global_vars.version),
		"--------------------------------Runtime specs-------------------------",
		"input_path_and_filename = \"{}\"".format(global_vars.input_path_and_filename),
		"alpha_threshold = {}".format(global_vars.alpha_threshold),
		"output_filename = \"{}\"".format(global_vars.output_filename),
		"output_filetype = \"{}\"".format(global_vars.output_filetype),

		"input_type = \"{}\"".format(global_vars.input_type),

		"raw_test = \"{}\"".format(global_vars.raw_test),

		"raw_corr_type = \"{}\"".format(global_vars.raw_corr_type),
		"raw_corr_vars = {}".format(global_vars.raw_corr_vars),
		"raw_mr_outcomevar = \"{}\"".format(global_vars.raw_mr_outcomevar),
		"raw_mr_predictors = {}".format(global_vars.raw_mr_predictors),
		"raw_indttest_groupvar = \"{}\"".format(global_vars.raw_indttest_groupvar),
		"raw_indttest_grouplevel1 = \"{}\"".format(global_vars.raw_indttest_grouplevel1),
		"raw_indttest_grouplevel2 = \"{}\"".format(global_vars.raw_indttest_grouplevel2),
		"raw_indttest_dv = {}".format(global_vars.raw_indttest_dv),
		"raw_pairttest_var_pairs = {}".format(global_vars.raw_pairttest_var_pairs),

		"summ_corr_varOne = \"{}\"".format(global_vars.summ_corr_varOne),
		"summ_corr_varTwo = \"{}\"".format(global_vars.summ_corr_varTwo),
		"summ_corr_coeff = \"{}\"".format(global_vars.summ_corr_coeff),
		"summ_corr_pvalues = \"{}\"".format(global_vars.summ_corr_pvalues),

		"summ_indttest_var = \"{}\"".format(global_vars.summ_indttest_var),
		"summ_indttest_meanOne = \"{}\"".format(global_vars.summ_indttest_meanOne),
		"summ_indttest_sdOne = \"{}\"".format(global_vars.summ_indttest_sdOne),
		"summ_indttest_nOne = \"{}\"".format(global_vars.summ_indttest_nOne),
		"summ_indttest_meanTwo = \"{}\"".format(global_vars.summ_indttest_meanTwo),
		"summ_indttest_sdTwo = \"{}\"".format(global_vars.summ_indttest_sdTwo),
		"summ_indttest_nTwo = \"{}\"".format(global_vars.summ_indttest_nTwo),
		"summ_indttest_equal_var = \"{}\"".format(global_vars.summ_indttest_equal_var),

		"spss_test = \"{}\"".format(global_vars.spss_test),
		"spss_indttest_nOne = {}".format(global_vars.spss_indttest_nOne),
		"spss_indttest_nTwo = {}".format(global_vars.spss_indttest_nTwo),
		"spss_indttest_groupOneLabel = \"{}\"".format(global_vars.spss_indttest_groupOneLabel),
		"spss_indttest_groupTwoLabel = \"{}\"".format(global_vars.spss_indttest_groupTwoLabel),
		"spss_pairttest_n = {}".format(global_vars.spss_pairttest_n),

		"pvalues_col = \"{}\"".format(global_vars.pvalues_col),

		"effect_size_choice = \"{}\"".format(global_vars.effect_size_choice),
		"correction_type = \"{}\"".format(global_vars.correction_type),

		"non_numeric_input_raise_errors = \"{}\"".format(global_vars.non_numeric_input_raise_errors),
		"------------------------------Input File Dataframe-----------------------"]  
	 
	log_file.writelines("\n".join(L) + "\n") 
	log_file.close()

	try:
		raw_data_df = decision_funcs.get_raw_data_df(debug=True)
	except:
		messagebox.showerror(title="Oopsie! Something has gone astray!", message="Unfortunately, the input file provided could not be read correctly which makes logging error details impossible.")
	raw_data_df.to_csv(log_filepath + ".txt", sep="\t", line_terminator="\n", mode="a+")

def log_window(traceback):
	top = tk.Toplevel()
	top.grab_set()
	top.title("Saving error details...")
	def exit(event):
		top.destroy()
	top.bind("<Escape>", exit)

	def save_log_file(traceback):
		top.destroy()
		log_error(traceback)
		log_file_saved_msg = "The details of your error message have been saved!\n\nPlease send us this file at {c} and we will try to get to you as soon as possible.\n\nYour help is greatly appreciated!".format(c=global_vars.contact, e=global_vars.contact)
		messagebox.showinfo(title = "File saved!", message=log_file_saved_msg)

	message = '''You will now be able to download a text file that contains some debugging information. We would be grateful if you could send us this information so we can improve the software.

	IMPORTANT NOTE: The text file will NOT contain any identifiable information. The only data from your input file that will be saved will be the columns you wanted
	to perform operations on. If your file contains any other columns, they will NOT be saved.

	Please feel free to open the text file after you've saved it and check the \"Input File Dataframe\" section for what data are saved.
	'''
	tk.Label(top, text=message).grid(row=0, column=0, columnspan=2, sticky="NWES", padx=15, pady=(5, 0))
	ttk.Button(top, text="Close", command=top.destroy).grid(row=1, column=0, padx=15, pady=5)
	ttk.Button(top, text="Save log file...", command=lambda traceback=traceback: save_log_file(traceback)).grid(row=1,column=1, padx=(0, 15), pady=5)

	center(top)

def error_window(error_msg, traceback=None):

	def open_log_window(traceback):
		top.destroy()
		log_window(traceback)

	top = tk.Toplevel()
	top.grab_set()
	top.title("Oopsie! Something has gone astray!")
	def exit(event):
		top.destroy()
	top.bind("<Escape>", exit)

	message = '''Oh no! Something appears to have gone wrong!

	Error Message: {}
	
	If you believe that we have made a mistake, please click on the \"Error Details\" button below.'''.format(error_msg)
	tk.Label(top, text=message).grid(row=0, column=0, columnspan=2, sticky="NWES", padx=15, pady=(5, 0))
	ttk.Button(top, text="Close", command=top.destroy).grid(row=1, column=0, padx=15, pady=5)
	ttk.Button(top, text="Error Details", command=lambda traceback=traceback: open_log_window(traceback)).grid(row=1,column=1, padx=(0, 15), pady=5)

	center(top)

#---------------------------------------------------------Menu
menubar = tk.Menu(master)
master.config(menu=menubar)

file = tk.Menu(menubar, tearoff=0)
file.add_command(label="Exit", command=master.destroy)
menubar.add_cascade(label="File", menu=file)

about = tk.Menu(menubar, tearoff=0)
about.add_command(label="About MAPAS", command=about_mapas_window)
menubar.add_cascade(label="Help", menu=about)

#------------------------
def run_main():
	raw_data_df = decision_funcs.get_raw_data_df()
	mod_raw_data_df = decision_funcs.modify_raw_data_df(raw_data_df)
	output_df = decision_funcs.generate_output_df(mod_raw_data_df)
	output_df = decision_funcs.multitest_correction(output_df)
	decision_funcs.save_output(mod_raw_data_df, output_df)

#------------------------------------------------------------------------------------Submit
def submit():
	try:
		set_global_variables()
		input_validation()
		run_main()
		clear_output_filename()
		submit_window()
	except Exception as error_msg:
		error_window(error_msg, traceback.format_exc())

ttk.Button(master, text="Submit", command=submit).grid(row=3, column=2, rowspan=2, sticky="E", padx=(0,15), pady=5)

master.mainloop()

#potentially useful function to raise errors in GUI at runtime; currente way of handling runtime GUI errros is suboptimal but given that there is little need for better handling, it suffices
#def report_callback_exception(self, exc, val, tb):
	#messagebox.showerror("Error", message=str(val))
#tk.Tk.report_callback_exception = report_callback_exception
