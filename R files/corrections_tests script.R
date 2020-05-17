library("readxl")
library("writexl")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "corrections_tests.xlsx", sep=""))

data$adjusted_pvalues = p.adjust(data$pvalues, method = "none")

write_xlsx(data, paste(OUTPUT_BASE_DIR, "corrections_tests_none.xlsx", sep=""))