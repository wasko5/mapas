library("readxl")
library("Hmisc")
library("writexl")
library("psychometric")
library("dplyr")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

flattenCorrMatrix <- function(cormat, pmat) {
  lt <- lower.tri(cormat)
  data.frame(
    Variable1 = rownames(cormat)[col(cormat)[lt]],
    Variable2 = rownames(cormat)[row(cormat)[lt]],
    Correlation_Coefficient = (cormat)[lt],
    pvalues = pmat[lt]
  )
}

data <- read_excel(paste(INPUT_BASE_DIR, "raw_corr_full data.xlsx", sep=""))

res <- rcorr(as.matrix(data), type="pearson")
corr_matrix <- flattenCorrMatrix(res$r, res$P)
corr_matrix$adjusted_pvalues = p.adjust(corr_matrix$p, method = "holm")

corr_matrix$Variable1 = levels(corr_matrix$Variable1)[corr_matrix$Variable1]
corr_matrix$Variable2 = levels(corr_matrix$Variable2)[corr_matrix$Variable2]
for (row in 1:length(rownames(corr_matrix))) {
  curr_r = corr_matrix[row, "Correlation_Coefficient"]
  curr_n = min(length(rownames(data[corr_matrix[row, "Variable1"]])),
               length(rownames(data[corr_matrix[row, "Variable2"]])))
  corr_matrix[row, "CI_low"] = CIr(r = curr_r, n = curr_n)[1]
  corr_matrix[row, "CI_high"] = CIr(r = curr_r, n = curr_n)[2]
}
corr_matrix <- corr_matrix[, c("Variable1", "Variable2", "Correlation_Coefficient",
                               "CI_low", "CI_high", "pvalues", "adjusted_pvalues")]

write_xlsx(corr_matrix, paste(OUTPUT_BASE_DIR, "raw_corr_pearson_holm_raiseErrors_R.xlsx", sep=""))
