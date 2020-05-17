library("readxl")
library("writexl")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "summ_indttest_tests.xlsx", sep=""))

# m1, m2: the sample means
# s1, s2: the sample standard deviations
# n1, n2: the same sizes
# m0: the null value for the difference in means to be tested for. Default is 0. 
# equal.variance: whether or not to assume equal variance. Default is FALSE. 
#Credit for function - https://stats.stackexchange.com/questions/30394/how-to-perform-two-sample-t-tests-in-r-by-inputting-sample-statistics-rather-tha
t.test2 <- function(m1,m2,s1,s2,n1,n2,m0=0,equal.variance=FALSE)
{
  if( equal.variance==FALSE ) 
  {
    se <- sqrt( (s1^2/n1) + (s2^2/n2) )
    # welch-satterthwaite df
    df <- ( (s1^2/n1 + s2^2/n2)^2 )/( (s1^2/n1)^2/(n1-1) + (s2^2/n2)^2/(n2-1) )
  } else
  {
    # pooled standard deviation, scaled by the sample sizes
    se <- sqrt( (1/n1 + 1/n2) * ((n1-1)*s1^2 + (n2-1)*s2^2)/(n1+n2-2) ) 
    df <- n1+n2-2
  }    
  
  t <- (m1-m2-m0)/se 
  pval <- 2*pt(-abs(t)[1,],df[1,])
  Cohens_d <- t * sqrt(1/n1 + 1/n2)
  Hedges_g <- (t * sqrt(1/n1 + 1/n2)) * (1 - (3/(4*(n1 + n2 - 9))))
  
  dat <- c(df, t, pval, Cohens_d, Hedges_g)    
  names(dat) <- c("df", "t", "p", "Cohens_d", "Hedges_g")
  return(dat) 
}

output_df = data.frame()

for (i in 1:3) {
  curr_t_test <- t.test2(m1 = data[i, "Mean1"], m2 = data[i, "Mean2"], s1 = data[i, "SD1"],
                        s2 = data[i, "SD2"], n1 = data[i, "N1"], n2 = data[i, "N2"],
                        equal.variance = TRUE)
                        #equal.variance = data[i, "Equal Variances"])
  output_df[i, "Variable"] <- data[i, "Variable"]
  output_df[i, "Mean1"] <- data[i, "Mean1"]
  output_df[i, "SD1"] <- data[i, "SD1"]
  output_df[i, "Mean2"] <- data[i, "Mean2"]
  output_df[i, "SD2"] <- data[i, "SD2"]
  output_df[i, "Degrees of Freedom"] <- curr_t_test$df
  output_df[i, "t"] <- curr_t_test$t
  #output_df[i, "Cohen's d"] <- curr_t_test$Cohens_d
  output_df[i, "Hedge's g"] <- curr_t_test$Hedges_g
  output_df[i, "pvalues"] <- curr_t_test$p
}

write_xlsx(output_df, paste(OUTPUT_BASE_DIR, "summ_indttest_tests_noEqualVarCol_hedgesg.xlsx", sep=""))






