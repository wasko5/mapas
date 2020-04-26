data <- input_raw_correlations
str(data)
round(cor(data, method="pearson"), 2)

install.packages("Hmisc")
library("Hmisc")
res2 <- 
res2
?rcorr
rcorr(as.matrix(data))

flattenCorrMatrix <- function(cormat, pmat) {
  ut <- upper.tri(cormat)
  data.frame(
    row = rownames(cormat)[row(cormat)[ut]],
    column = rownames(cormat)[col(cormat)[ut]],
    cor  = (cormat)[ut],
    p = pmat[ut]
  )
}

res2<-rcorr(as.matrix(data))
corr_matrix <- flattenCorrMatrix(res2$r, res2$P)

corr_matrix$adj_p = p.adjust(corr_matrix$p, method = "BH")
corr_matrix[,3:5] = round(corr_matrix[,3:5], 2)
corr_matrix




