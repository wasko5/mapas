'''
- One current 'feature' is that when you move between tests (correlations-mr in raw test) the things you put in the listbox (e.g. for MR) stay there despite clicking away.
			Might leave it like that for listboxes but reset for everything else. Might add a parameter to the reset_defaults function such that it can also
			reset to default these listboxes upon successful run of the program (i.e. when someone clicks "more analysis" in the popup)
- Fix the ability to end up with "Please elect input file first..." in the comboboxes.
- Consider adding more menu options
- selecting None to correction on ind ttest brings up an error
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
from PIL import Image, ImageTk
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
columns_current_indices_dict = {}
previous_combobox_vals_dict = {}

input_path_and_filename_tk = tk.StringVar()
alpha_threshold_tk = tk.StringVar()
output_filename_tk = tk.StringVar()

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
	current_sel_ind = list(col_names_lb.curselection())
	current_sel_items = [col_names_lb.get(ele) for ele in current_sel_ind]
	
	listbox.insert(tk.END, *[col_names_lb.get(ele) for ele in current_sel_ind])
	delete_lbitems(col_names_lb, ind=current_sel_ind)

def move_lbvars_to_master(listbox): #TO CHANGE NAME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

	if combobox_prev_val != "" and combobox_prev_val != "Select input file first...":
		move_back_to_master([combobox_prev_val])

	if combobox_id == ".!frame.!labelframe8.!frame.!combobox" or combobox_id == ".!frame.!labelframe8.!frame.!combobox2": #ids for the 2 pairttest dropdowns
		pairttest_remove_added_vars_from_master()

	previous_combobox_vals_dict[combobox_id] = combobox_current_val
	delete_lbitems(col_names_lb, values=[combobox_current_val])
	update_columns_current_indices_dict()

#-----------------2.2. Layout control
def remove_frames(frames_list):
	for frame in frames_list:
		frame.grid_remove()

def input_type_frames_layout():
	#the only frames it does not include are master or input_type
	frames_list = [raw_test_Frame, raw_corr_Frame, raw_corr_vars_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame,
					raw_indttest_grouplevels_Frame, raw_indttest_dv_Frame, raw_pairttest_master_Frame, summ_corr_master_Frame, summ_indttest_master_Frame,
					spss_get_table_info_Frame, spss_test_Frame, spss_indttest_sampleSize_Frame, spss_indttest_groupLabels_Frame, spss_pairttest_sampleSize_Frame,
					col_names_Frame, effect_size_Frame, correction_type_Frame, raw_ttest_output_descriptives_Frame, non_numeric_input_raise_errors_Frame]

	
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
		spss_get_table_info_Frame.grid(row=3, column=2, sticky="NE", padx=15, pady=0)
	elif input_type_tk.get() == "pvalues":
		correction_type_Frame.grid(row=0, column=0, rowspan=1, sticky="NW", padx=0, pady=0)

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
	frames_list = [raw_corr_Frame, raw_corr_vars_Frame, raw_mr_outcomevar_Frame, raw_mr_predictors_Frame, raw_indttest_groupvar_Frame, raw_indttest_grouplevels_Frame,
					raw_indttest_dv_Frame, raw_pairttest_master_Frame, col_names_Frame, effect_size_Frame, correction_type_Frame, raw_ttest_output_descriptives_Frame,
					non_numeric_input_raise_errors_Frame]

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
		raw_ttest_output_descriptives_Frame.grid(row=4, column=0, sticky="NW", padx=0, pady=0)
		col_names_Frame.grid(row=0, column=1, rowspan=5, sticky="NW", padx=(15, 0), pady=0)
		raw_indttest_groupvar_Frame.grid(row=0, column=2, sticky="NW", padx=15, pady=0)
		raw_indttest_grouplevels_Frame.grid(row=1, column=2, sticky="NW", padx=15, pady=5)
		raw_indttest_dv_Frame.grid(row=2, column=2, rowspan=3, sticky="NW", padx=15, pady=0)
	elif global_vars.master_dict[raw_test_tk.get()] == "pairttest":
		correction_type_Frame.grid(row=1, column=0, rowspan=1, sticky="NW", padx=0, pady=5)
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

#-----------------2.3. GUI Content
#Instructions
instr_label = ttk.Label(master, text="Main instructions")
instr_label.grid(row=0, column=0, columnspan=3)

#Input file button & label
def select_file():
	path_and_filename = askopenfilename(initialdir = "D:\\Desktop_current\\NPSoftware\\GitHub\\Input files\\raw data", title="Select input file. Must be Excel file.", filetypes=(("Excel files","*.xlsx"),("All files","*.*")))
	
	if path_and_filename.endswith(".xlsx"): # or filename[ext_sep_idx:] == ".csv" - for later use when csv is integrated
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

	elif path_and_filename != "":
		messagebox.showerror("Oh-oh!", "As we agreed, you will need to select a valid file - .xlsx files only.")

ttk.Button(input_filename_Frame, text="Select input file (.xlsx only)", command=select_file).grid(row=0, column=0, sticky="W", padx=(0, 10))
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
	if input_path_and_filename_tk != "" and raw_indttest_groupvar_tk.get() != global_vars.tk_vars_defaults["raw_indttest_groupvar_tk"] and raw_indttest_groupvar_tk.get() != "Select input file first...":
		dropdown.configure(values=helper_funcs.get_raw_indttest_grouplevels(input_path_and_filename_tk.get(), raw_indttest_groupvar_tk.get()))

def raw_indttest_dropdowns_validation(event):
	if raw_indttest_grouplevel1_tk.get() == raw_indttest_grouplevel2_tk.get():
		raise Exception("You can't select the same level for both groups.")

raw_indttest_grouplevels_drop1 = ttk.Combobox(raw_indttest_grouplevels_Frame, state="readonly", width=15, textvariable=raw_indttest_grouplevel1_tk)
raw_indttest_grouplevels_drop1.configure(postcommand=lambda dropdown=raw_indttest_grouplevels_drop1: get_values_for_raw_indttest_dropdowns(dropdown))
raw_indttest_grouplevels_drop1.bind("<<ComboboxSelected>>", raw_indttest_dropdowns_validation)
raw_indttest_grouplevels_drop1.grid(row=0, column=0, padx=(0, 10))

raw_indttest_grouplevels_drop2 = ttk.Combobox(raw_indttest_grouplevels_Frame, state="readonly", width=15, textvariable=raw_indttest_grouplevel2_tk)
raw_indttest_grouplevels_drop2.configure(postcommand=lambda dropdown=raw_indttest_grouplevels_drop2: get_values_for_raw_indttest_dropdowns(dropdown))
raw_indttest_grouplevels_drop2.bind("<<ComboboxSelected>>", raw_indttest_dropdowns_validation)
raw_indttest_grouplevels_drop2.grid(row=0, column=1)

#Raw data // test // Independent samples t-test // DVs
raw_indttest_dv_lb = tk.Listbox(raw_indttest_dv_Frame, selectmode="extended", height=7, width=23)
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
	if raw_pairttest_var1_tk.get() == global_vars.tk_vars_defaults["raw_pairttest_var1_tk"] or raw_pairttest_var2_tk.get() == global_vars.tk_vars_defaults["raw_pairttest_var2_tk"]:
		messagebox.showerror("Error!", "Please select both variable columns of your pair.")
	else:
		raw_pairttest_pairs_lb.insert(tk.END, "{p1} <---> {p2}".format(p1=raw_pairttest_var1_tk.get(), p2=raw_pairttest_var2_tk.get()))
		raw_pairttest_var1_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var1_tk"])
		raw_pairttest_var2_tk.set(global_vars.tk_vars_defaults["raw_pairttest_var2_tk"])

raw_pairttest_pairs_lb = tk.Listbox(raw_pairttest_btn_list_Frame, selectmode="extended", height=9, width=40)
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

	img_1 = tk.PhotoImage(file="D:\\Desktop_current\\NPSoftware\\GitHub\\Images\\spss_instr3.gif")
	img_1_label = tk.Label(canvas, image=img_1)
	img_1_label.image = img_1
	img_1_label.grid(row=0, column=0)

	center(top)

	'''
	#top.maxsize(height=450, width=0)
	#top.geometry("450x600")

	
	def onFrameConfigure(canvas):
	    #Reset the scroll region to encompass the inner frame
	    canvas.configure(scrollregion=canvas.bbox("all"))


	canvas = tk.Canvas(top)
	frame = tk.Frame(canvas)	
	top_scroll = ttk.Scrollbar(top, command=canvas.yview, orient=tk.VERTICAL)
	
	canvas.configure(yscrollcommand=top_scroll.set)

	top_scroll.grid(row=0, column=1, sticky="NS")
	canvas.grid(row=0, column=0)
	canvas.create_window((4,4), window=frame, anchor="nw")
	#frame.grid(row=0, column=0)

	frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

	img_loc_1 = Image.open("spss_table_1.png")
	img_loc_1 = img_loc_1.resize((370, 300), Image.ANTIALIAS)
	img_1 = ImageTk.PhotoImage(img_loc_1)

	img_loc_2 = Image.open("spss_table_2.png")
	img_loc_2 = img_loc_2.resize((389, 450), Image.ANTIALIAS)
	img_2 =ImageTk.PhotoImage(img_loc_2)
	print(img_loc_1, img_loc_2)

	spss_table_info_text1 = tk.Label(frame, text=text_1)
	spss_table_info_img1 = tk.Label(frame, image=img_1)
	spss_table_info_img1.image = img_1
	spss_table_info_text2 = tk.Label(frame, text=text_2)
	spss_table_info_img2 = tk.Label(frame, image=img_2)
	spss_table_info_img2.image = img_2
	spss_table_info_text1.grid(row=0, column=0, sticky="W", padx=15, pady=5)
	spss_table_info_img1.grid(row=1, column=0, sticky="EW", padx=15, pady=0)
	spss_table_info_text2.grid(row=2, column=0, sticky="W", padx=15, pady=5)
	spss_table_info_img2.grid(row=3, column=0, sticky="EW", padx=15, pady=(0, 5))

	text_1 = """
	To export any table from SPSS output, follow the steps below (Correlations
	table is used as an example but works with any table):
	
	First, right-click on the SPSS table in the SPSS output, then click Export:
	"""
	img_1 = tk.PhotoImage("spss_table_1.pgm")
	text_2 = """
	Then under Document, for Type, select “Excel 2007 and Higher (*.xlsx)”.
	Then click Browse to select where to export the table.

	Finally, hit OK:
	"""
	img_2 = tk.PhotoImage("spss_table_2.pgm")
	
	spss_table_info_textbox_1 = tk.Text(top, height=20, width=50)
	spss_table_info_textbox_2 = tk.Text(top, height=20, width=50)
	spss_table_info_textbox_3 = tk.Text(top, height=20, width=50)
	spss_table_info_textbox_4 = tk.Text(top, height=20, width=50)

	spss_table_info_scroll = ttk.Scrollbar(top, command=spss_table_info_textbox.yview)
	spss_table_info_textbox.configure(yscrollcommand=spss_table_info_scroll.set)

	spss_table_info_textbox.insert(tk.END, text_1)
	spss_table_info_textbox.image_create(tk.END, image=img_1)
	spss_table_info_textbox.insert(tk.END, text_2)
	spss_table_info_textbox.image_create(tk.END, image=img_2)

	spss_table_info_textbox.grid(row=0, column=0)
	spss_table_info_scroll.grid(row=0, column=1, sticky="NS")
	'''	

spss_table_info_label = ttk.Label(spss_get_table_info_Frame, text="How to import SPSS table?", foreground="blue", cursor="hand2")
spss_table_info_label.grid(row=0, column=0, sticky="NE", padx=0, pady=5)
spss_table_info_label.bind("<Button-1>", spss_table_info_popup)

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
	print("raw_corr_vars - ", global_vars.raw_corr_vars)
	print("raw_mr_outcomevar - ", global_vars.raw_mr_outcomevar)
	print("raw_mr_predictors - ", global_vars.raw_mr_predictors)
	print("raw_indttest_groupvar - ", global_vars.raw_indttest_groupvar)
	print("raw_indttest_grouplevel1 - ", global_vars.raw_indttest_grouplevel1)
	print("raw_indttest_grouplevel2 - ", global_vars.raw_indttest_grouplevel2)
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
				raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correlation (pearson, spearman, kendall) you want to perform.")
			if global_vars.correction_type == "none":
				raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("What happens if you have missing or invalid data? Well, we don't know either so you will need to tell us your preference.\n\nPlease select how to handle non-numeric data.")
		elif global_vars.raw_test == "mr":
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("What happens if you have missing or invalid data? Well, we don't know either so you will need to tell us your preference.\n\nPlease select how to handle non-numeric data.")
			if global_vars.raw_mr_outcomevar == "":
				raise Exception("We can certainly perform a multiple regression but what are we predicting?\n\nPlease select your outcome (dependent) variable.")
			if global_vars.raw_mr_predictors == ():
				raise Exception("Although we are currently working on it, we still can't predict your predictors (ha, get it? predict the predictors... please send help).\n\nSpeaking of help, you might as well help us by telling us what your predictors are.")
		elif global_vars.raw_test == "indttest":
			if global_vars.correction_type == "none":
				raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
			if global_vars.effect_size_choice == "none":
				raise Exception("Your t-test will be much better with an effect size estimate in there.\n\nPlease select what effect size, if any, you want.")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("What happens if you have missing or invalid data? Well, we don't know either so you will need to tell us your preference.\n\nPlease select how to handle non-numeric data.")
			if global_vars.raw_indttest_groupvar == "" or global_vars.raw_indttest_grouplevel1 == "" or global_vars.raw_indttest_grouplevel2 == "":
				raise Exception("So far so good - we will be comparing independent groups. But what are those groups?\n\nPlease select your grouping variables and the labels for the groups we are comparing.")
			if global_vars.raw_indttest_dv == []:
				raise Exception("Right, so we are comparing those two groups - but we are not sure what to comapre them on.\n\nPlease select your dependent variables.")
		elif global_vars.raw_test == "pairttest":
			if global_vars.correction_type == "none":
				raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
			if global_vars.effect_size_choice == "none":
				raise Exception("Your t-test will be much better with an effect size estimate in there.\n\nPlease select what effect size, if any, you want.")
			if global_vars.non_numeric_input_raise_errors == "":
				raise Exception("What happens if you have missing or invalid data? Well, we don't know either so you will need to tell us your preference.\n\nPlease select how to handle non-numeric data.")
			if global_vars.raw_pairttest_var_pairs == ():
				raise Exception("In order to run that paired sample t-test, we first need to know what your pair of varialbes are.\n\nPlease add your pairs to the box using the dropdown menus and the buttons.")
	elif global_vars.input_type == "summ_corr":
		if global_vars.correction_type == "none":
			raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
		if global_vars.summ_corr_varOne == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your variable one labels.")
		if global_vars.summ_corr_varTwo == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your variable two labels.")
		if global_vars.summ_corr_coeff == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your correlation coefficients.")
		if global_vars.summ_corr_pvalues == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your pvalues.")
	elif global_vars.input_type == "summ_indttest":
		if global_vars.correction_type == "none":
			raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
		if global_vars.effect_size_choice == "none":
			raise Exception("Your t-test will be much better with an effect size estimate in there.\n\nPlease select what effect size, if any, you want.")
		if global_vars.summ_indttest_var == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your variable labels.")
		if global_vars.summ_indttest_meanOne == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your mean values for group 1.")
		if global_vars.summ_indttest_sdOne == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your standard deviation values for group 1.")
		if global_vars.summ_indttest_nOne == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your sample size for group 1.")
		if global_vars.summ_indttest_meanTwo == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your mean values for group 2.")
		if global_vars.summ_indttest_sdTwo == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your standard deviation values for group 2.")
		if global_vars.summ_indttest_nTwo == "":
			raise Exception("Oops - you missed one!\n\nPlease select the column with your sample size for group 2.")
	elif global_vars.input_type == "spss":
		if global_vars.spss_test == "":
			raise Exception("Where's the rush? First you will need to tell us what kind of SPSS table you have there first.")
		elif global_vars.spss_test == "corr":
			if global_vars.correction_type == "none":
				raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
		elif global_vars.spss_test == "mr":
			pass
		elif global_vars.spss_test == "indttest":
			if global_vars.correction_type == "none":
				raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
			if global_vars.effect_size_choice == "none":
				raise Exception("Your t-test will be much better with an effect size estimate in there.\n\nPlease select what effect size, if any, you want.")
			if global_vars.spss_indttest_nOne == -1 or global_vars.spss_indttest_nTwo == -1:
				raise Exception("To run some of the statistics for the t-test you will need to tell us what your sample size is.")
		elif global_vars.spss_test == "pairttest":
			if global_vars.correction_type == "none":
				raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")
			if global_vars.effect_size_choice == "none":
				raise Exception("Your t-test will be much better with an effect size estimate in there.\n\nPlease select what effect size, if any, you want.")
			if global_vars.spss_pairttest_nOne == -1 or global_vars.spss_pairttest_nTwo == -1:
				raise Exception("To run some of the statistics for the t-test you will need to tell us what your sample size is.")
	elif global_vars.input_type == "pvalues":
		if global_vars.correction_type == "none":
			raise Exception("Oops - you missed one!\n\nPlease tell us what kind of correction, if any, you want us to apply to the data.")


	if global_vars.effect_size_choice == "Glass's delta" and (global_vars.input_type == "summindttest" or global_vars.spss_test == "indttest" or global_vars.spss_test == "pairttest"):
		raise Exception("Sorry! Glass's delta is not available for this time of test. Glass's delta can only be requested if raw data is provided. For more information, see the documentation.")
	
	if global_vars.output_filename == "":
		raise Exception("We're almost there... Your output file is ready and waiting for you. You will just need to tell it where to pop up.\n\nPlease select an output file.")

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

	some_message = '''Your file is ready and waiting for you.
	
	If you've found this software useful in your work, please cite us as:
	Petrov, N., Atanasov, V., & Thompson, T. (2020). Open-source Software for Apply Multiple-tests Corrections and Printing APA Tables (MAPAS)...'''
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
	#except Exception as error_msg:
	#	messagebox.showerror("Oopsie!", error_msg)

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