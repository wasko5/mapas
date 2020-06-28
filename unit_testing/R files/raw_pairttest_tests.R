library("readxl")
library("psych")
library("dplyr")
library("writexl")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/unit_testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/unit_testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "raw_pairttest_tests_unevenGroups_withMissingData.xlsx", sep=""))
t.test(data$Bar1, data$Bar2, paired=TRUE)
t.test(data$Foo1, data$Foo2, paired=TRUE)










