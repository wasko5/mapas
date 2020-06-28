library("readxl")
library("writexl")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "raw_correlations_tests.xlsx", sep=""))

var1s <- c("var1","var1","var1","var1","var1","var1","var1","var2","var2","var2","var2","var2","var2","var3","var3","var3","var3","var3","var4","var4","var4","var4","var5","var5","var5","var6","var6","var7")
var2s <- c("var2","var3","var4","var5","var6","var7","var8","var3","var4","var5","var6","var7","var8","var4","var5","var6","var7","var8","var5","var6","var7","var8","var6","var7","var8","var7","var8","var8")
kendall_df <- data.frame(
  Variable1 = var1s,
  Variable2 = var2s
)


kendall_df$Variable1 = levels(kendall_df$Variable1)[kendall_df$Variable1]
kendall_df$Variable2 = levels(kendall_df$Variable2)[kendall_df$Variable2]
for (i in 1:length(var1s)) {
  curr_var1 = kendall_df[i, "Variable1"]
  curr_var2 = kendall_df[i, "Variable2"]
  kendall_test = cor.test(as.numeric(unlist(data[curr_var1])),
                          as.numeric(unlist(data[curr_var2])),
                          method="kendall")
  curr_n = min(sum(!is.na(data[curr_var1])),
               sum(!is.na(data[curr_var2])))
  
  kendall_df[i, "Correlation_Coefficient"] = kendall_test$estimate
  kendall_df[i, "CI_low"] = CIr(r = kendall_test$estimate, n = curr_n)[1]
  kendall_df[i, "CI_high"] = CIr(r = kendall_test$estimate, n = curr_n)[2]
  kendall_df[i, "pvalues"] = kendall_test$p.value
}

write_xlsx(kendall_df, paste(OUTPUT_BASE_DIR, "raw_correlations_tests_kendall.xlsx", sep=""))





