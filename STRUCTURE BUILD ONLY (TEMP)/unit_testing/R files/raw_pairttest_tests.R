library("readxl")
library("psych")
library("dplyr")
library("writexl")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "raw_pairttest_tests_unevenGroups.xlsx", sep=""))


write_xlsx(output_df, paste(OUTPUT_BASE_DIR, "raw_indttest_tests_cohensd.xlsx", sep=""))












