library("readxl")
library("psych")
library("dplyr")
library("writexl")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "raw_indttest_tests_withNumbersForGroups.xlsx", sep=""))
data <- filter(data, !is.na(Group))

data$Group = as.factor(data$Group)
descr_stats_by_group <- describeBy(data[2:4], group=data$Group)
descr_stats_all <- describe(data[2:4])

CI_low_var1_all <- t.test(data$var1)$conf.int[1]
CI_high_var1_all <- t.test(data$var1)$conf.int[2]
CI_low_var1_g1 <- t.test(as.numeric(unlist(data[data$Group == "Group1","var1"])))$conf.int[1]
CI_high_var1_g1 <- t.test(as.numeric(unlist(data[data$Group == "Group1","var1"])))$conf.int[2]
CI_low_var1_g2 <- t.test(as.numeric(unlist(data[data$Group == "Group2","var1"])))$conf.int[1]
CI_high_var1_g2 <- t.test(as.numeric(unlist(data[data$Group == "Group2","var1"])))$conf.int[2]
CI_low_var2_all <- t.test(data$var2)$conf.int[1]
CI_high_var2_all <- t.test(data$var2)$conf.int[2]
CI_low_var2_g1 <- t.test(as.numeric(unlist(data[data$Group == "Group1","var2"])))$conf.int[1]
CI_high_var2_g1 <- t.test(as.numeric(unlist(data[data$Group == "Group1","var2"])))$conf.int[2]
CI_low_var2_g2 <- t.test(as.numeric(unlist(data[data$Group == "Group2","var2"])))$conf.int[1]
CI_high_var2_g2 <- t.test(as.numeric(unlist(data[data$Group == "Group2","var2"])))$conf.int[2]
CI_low_var3_all <- t.test(data$var3)$conf.int[1]
CI_high_var3_all <- t.test(data$var3)$conf.int[2]
CI_low_var3_g1 <- t.test(as.numeric(unlist(data[data$Group == "Group1","var3"])))$conf.int[1]
CI_high_var3_g1 <- t.test(as.numeric(unlist(data[data$Group == "Group1","var3"])))$conf.int[2]
CI_low_var3_g2 <- t.test(as.numeric(unlist(data[data$Group == "Group2","var3"])))$conf.int[1]
CI_high_var3_g2 <- t.test(as.numeric(unlist(data[data$Group == "Group2","var3"])))$conf.int[2]

equal_var_pval_var1 <- var.test(as.numeric(unlist(data[data$Group == "Group1","var1"])),
                           as.numeric(unlist(data[data$Group == "Group2","var1"])))$p.value
equal_var_pval_var2 <- var.test(as.numeric(unlist(data[data$Group == "Group1","var2"])),
                           as.numeric(unlist(data[data$Group == "Group2","var2"])))$p.value
equal_var_pval_var3 <- var.test(as.numeric(unlist(data[data$Group == "Group1","var3"])),
                           as.numeric(unlist(data[data$Group == "Group2","var3"])))$p.value

equal_var_arr <- c(equal_var_pval_var1 > 0.05, equal_var_pval_var2 > 0.05, equal_var_pval_var3 > 0.05)
equal_var_replaced <- replace(equal_var_arr, equal_var_arr == TRUE, "Yes")
equal_var_replaced <- replace(equal_var_replaced, equal_var_replaced == FALSE, "No")

t_test_var1 <- t.test(data$var1 ~ data$Group, var.equal = equal_var_pval_var1 > 0.05)
t_test_var2 <- t.test(data$var2 ~ data$Group, var.equal = equal_var_pval_var2 > 0.05)
t_test_var3 <- t.test(data$var3 ~ data$Group, var.equal = equal_var_pval_var3 > 0.05)

output_df <- data.frame(
  Variable = colnames(data)[2:4],
  All_N = descr_stats_all$n,
  All_Mean = descr_stats_all$mean,
  All_SD = descr_stats_all$sd,
  All_Std_Err = descr_stats_all$se,
  All_95_CI_Low = c(CI_low_var1_all, CI_low_var2_all, CI_low_var3_all),
  All_95_CI_High = c(CI_high_var1_all, CI_high_var2_all, CI_high_var3_all),
  Group1_N = descr_stats_by_group$Group1$n,
  Group1_Mean = descr_stats_by_group$Group1$mean,
  Group1_SD = descr_stats_by_group$Group1$sd,
  Group1_Std_Err = descr_stats_by_group$Group1$se,
  Group1_95_CI_Low = c(CI_low_var1_g1, CI_low_var2_g1, CI_low_var3_g1),
  Group1_95_CI_High = c(CI_high_var1_g1, CI_high_var2_g1, CI_high_var3_g1),
  Group2_N = descr_stats_by_group$Group2$n,
  Group2_Mean = descr_stats_by_group$Group2$mean,
  Group2_SD = descr_stats_by_group$Group2$sd,
  Group2_Std_Err = descr_stats_by_group$Group2$se,
  Group2_95_CI_Low = c(CI_low_var1_g2, CI_low_var2_g2, CI_low_var3_g2),
  Group2_95_CI_High = c(CI_high_var1_g2, CI_high_var2_g2, CI_high_var3_g2),
  Equal_Variances_Assumed = equal_var_replaced,
  Degrees_of_Freedom = c(t_test_var1$parameter, t_test_var2$parameter, t_test_var3$parameter),
  t = c(t_test_var1$statistic, t_test_var2$statistic, t_test_var3$statistic),
  Cohens_d = c(0, 0, 0), #0s for placeholder purpose
  #Hedges_g = c(0, 0, 0),
  #Glass_d = c(0, 0, 0),
  #None = c("", "", ""),
  pvalues = c(t_test_var1$p.value, t_test_var2$p.value, t_test_var3$p.value)
)

names(output_df)[names(output_df) == "All_95_CI_Low"] <- "All_95% CI_Low"
names(output_df)[names(output_df) == "All_95_CI_High"] <- "All_95% CI_High"
names(output_df)[names(output_df) == "Group1_95_CI_Low"] <- "Group1_95% CI_Low"
names(output_df)[names(output_df) == "Group1_95_CI_High"] <- "Group1_95% CI_High"
names(output_df)[names(output_df) == "Group2_95_CI_Low"] <- "Group2_95% CI_Low"
names(output_df)[names(output_df) == "Group2_95_CI_High"] <- "Group2_95% CI_High"


output_df$Cohens_d <- output_df$t * sqrt(1/output_df$Group1_N + 1/output_df$Group2_N)
names(output_df)[names(output_df) == "Cohens_d"] <- "Cohen's d"

#output_df$Hedges_g <- (output_df$t * sqrt(1/output_df$Group1_N + 1/output_df$Group2_N)) * (1 - (3/(4*(output_df$Group1_N + output_df$Group2_N - 9))))
#names(output_df)[names(output_df) == "Hedges_g"] <- "Hedge's g"

#output_df$Glass_d <- (output_df$Group1_Mean - output_df$Group2_Mean) / output_df$Group1_SD
#names(output_df)[names(output_df) == "Glass_d"] <- "Glass's delta"


write_xlsx(output_df, paste(OUTPUT_BASE_DIR, "raw_indttest_tests_withNumbersForGroups.xlsx", sep=""))



################################WITH NUMBERS AS GROUPS############################################################
library("readxl")
library("psych")
library("dplyr")
library("writexl")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "raw_indttest_tests_withNumbersForGroups.xlsx", sep=""))
data <- filter(data, !is.na(Group))

data$Group = as.factor(data$Group)
descr_stats_by_group <- describeBy(data[2:4], group=data$Group)
descr_stats_all <- describe(data[2:4])

CI_low_var1_all <- t.test(data$var1)$conf.int[1]
CI_high_var1_all <- t.test(data$var1)$conf.int[2]
CI_low_var1_g1 <- t.test(as.numeric(unlist(data[data$Group == "1","var1"])))$conf.int[1]
CI_high_var1_g1 <- t.test(as.numeric(unlist(data[data$Group == "1","var1"])))$conf.int[2]
CI_low_var1_g2 <- t.test(as.numeric(unlist(data[data$Group == "0","var1"])))$conf.int[1]
CI_high_var1_g2 <- t.test(as.numeric(unlist(data[data$Group == "0","var1"])))$conf.int[2]
CI_low_var2_all <- t.test(data$var2)$conf.int[1]
CI_high_var2_all <- t.test(data$var2)$conf.int[2]
CI_low_var2_g1 <- t.test(as.numeric(unlist(data[data$Group == "1","var2"])))$conf.int[1]
CI_high_var2_g1 <- t.test(as.numeric(unlist(data[data$Group == "1","var2"])))$conf.int[2]
CI_low_var2_g2 <- t.test(as.numeric(unlist(data[data$Group == "0","var2"])))$conf.int[1]
CI_high_var2_g2 <- t.test(as.numeric(unlist(data[data$Group == "0","var2"])))$conf.int[2]
CI_low_var3_all <- t.test(data$var3)$conf.int[1]
CI_high_var3_all <- t.test(data$var3)$conf.int[2]
CI_low_var3_g1 <- t.test(as.numeric(unlist(data[data$Group == "1","var3"])))$conf.int[1]
CI_high_var3_g1 <- t.test(as.numeric(unlist(data[data$Group == "1","var3"])))$conf.int[2]
CI_low_var3_g2 <- t.test(as.numeric(unlist(data[data$Group == "0","var3"])))$conf.int[1]
CI_high_var3_g2 <- t.test(as.numeric(unlist(data[data$Group == "0","var3"])))$conf.int[2]

equal_var_pval_var1 <- var.test(as.numeric(unlist(data[data$Group == "1","var1"])),
                                as.numeric(unlist(data[data$Group == "0","var1"])))$p.value
equal_var_pval_var2 <- var.test(as.numeric(unlist(data[data$Group == "1","var2"])),
                                as.numeric(unlist(data[data$Group == "0","var2"])))$p.value
equal_var_pval_var3 <- var.test(as.numeric(unlist(data[data$Group == "1","var3"])),
                                as.numeric(unlist(data[data$Group == "0","var3"])))$p.value

equal_var_arr <- c(equal_var_pval_var1 > 0.05, equal_var_pval_var2 > 0.05, equal_var_pval_var3 > 0.05)
equal_var_replaced <- replace(equal_var_arr, equal_var_arr == TRUE, "Yes")
equal_var_replaced <- replace(equal_var_replaced, equal_var_replaced == FALSE, "No")

t_test_var1 <- t.test(data$var1 ~ data$Group, var.equal = equal_var_pval_var1 > 0.05)
t_test_var2 <- t.test(data$var2 ~ data$Group, var.equal = equal_var_pval_var2 > 0.05)
t_test_var3 <- t.test(data$var3 ~ data$Group, var.equal = equal_var_pval_var3 > 0.05)

output_df <- data.frame(
  Variable = colnames(data)[2:4],
  All_N = descr_stats_all$n,
  All_Mean = descr_stats_all$mean,
  All_SD = descr_stats_all$sd,
  All_Std_Err = descr_stats_all$se,
  All_95_CI_Low = c(CI_low_var1_all, CI_low_var2_all, CI_low_var3_all),
  All_95_CI_High = c(CI_high_var1_all, CI_high_var2_all, CI_high_var3_all),
  Group1_N = descr_stats_by_group$"1"$n,
  Group1_Mean = descr_stats_by_group$"1"$mean,
  Group1_SD = descr_stats_by_group$"1"$sd,
  Group1_Std_Err = descr_stats_by_group$"1"$se,
  Group1_95_CI_Low = c(CI_low_var1_g1, CI_low_var2_g1, CI_low_var3_g1),
  Group1_95_CI_High = c(CI_high_var1_g1, CI_high_var2_g1, CI_high_var3_g1),
  Group2_N = descr_stats_by_group$"0"$n,
  Group2_Mean = descr_stats_by_group$"0"$mean,
  Group2_SD = descr_stats_by_group$"0"$sd,
  Group2_Std_Err = descr_stats_by_group$"0"$se,
  Group2_95_CI_Low = c(CI_low_var1_g2, CI_low_var2_g2, CI_low_var3_g2),
  Group2_95_CI_High = c(CI_high_var1_g2, CI_high_var2_g2, CI_high_var3_g2),
  Equal_Variances_Assumed = equal_var_replaced,
  Degrees_of_Freedom = c(t_test_var1$parameter, t_test_var2$parameter, t_test_var3$parameter),
  t = c(t_test_var1$statistic, t_test_var2$statistic, t_test_var3$statistic),
  Cohens_d = c(0, 0, 0), #0s for placeholder purpose
  #Hedges_g = c(0, 0, 0),
  #Glass_d = c(0, 0, 0),
  #None = c("", "", ""),
  pvalues = c(t_test_var1$p.value, t_test_var2$p.value, t_test_var3$p.value)
)

names(output_df)[names(output_df) == "All_95_CI_Low"] <- "All_95% CI_Low"
names(output_df)[names(output_df) == "All_95_CI_High"] <- "All_95% CI_High"
names(output_df)[names(output_df) == "Group1_95_CI_Low"] <- "Group1_95% CI_Low"
names(output_df)[names(output_df) == "Group1_95_CI_High"] <- "Group1_95% CI_High"
names(output_df)[names(output_df) == "Group2_95_CI_Low"] <- "Group2_95% CI_Low"
names(output_df)[names(output_df) == "Group2_95_CI_High"] <- "Group2_95% CI_High"


output_df$Cohens_d <- output_df$t * sqrt(1/output_df$Group1_N + 1/output_df$Group2_N)
names(output_df)[names(output_df) == "Cohens_d"] <- "Cohen's d"

#output_df$Hedges_g <- (output_df$t * sqrt(1/output_df$Group1_N + 1/output_df$Group2_N)) * (1 - (3/(4*(output_df$Group1_N + output_df$Group2_N - 9))))
#names(output_df)[names(output_df) == "Hedges_g"] <- "Hedge's g"

#output_df$Glass_d <- (output_df$Group1_Mean - output_df$Group2_Mean) / output_df$Group1_SD
#names(output_df)[names(output_df) == "Glass_d"] <- "Glass's delta"


write_xlsx(output_df, paste(OUTPUT_BASE_DIR, "raw_indttest_tests_withNumbersForGroups.xlsx", sep=""))












