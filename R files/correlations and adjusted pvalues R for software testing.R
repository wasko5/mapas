library(readxl)
data <- read_excel("D:/Desktop_current/NPSoftware/GitHub/df5.xlsx")
str(data)
round(cor(data, method="pearson"), 2)

install.packages("Hmisc")
library("Hmisc")
res2 <- 
res2
?rcorr
rcorr(as.matrix(data))

flattenCorrMatrix <- function(cormat, pmat) {
  lt <- lower.tri(cormat)
  data.frame(
    Variable1 = rownames(cormat)[col(cormat)[lt]],
    Variable2 = rownames(cormat)[row(cormat)[lt]],
    Correlation.Coefficient = (cormat)[lt],
    pvalues = pmat[lt]
  )
}

res2<-rcorr(as.matrix(data))
print(res2$r)
corr_matrix <- flattenCorrMatrix(res2$r, res2$P)

corr_matrix$adjusted_pvalues = p.adjust(corr_matrix$p, method = "BH")
corr_matrix[,3:5] = round(corr_matrix[,3:5], 2)
corr_matrix

install.packages("writexl")
library("writexl")
write_xlsx(corr_matrix, "D:/Desktop_current/NPSoftware/GitHub/df5_r_output.xlsx")
?p.adjust


