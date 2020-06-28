library("readxl")
library("lm.beta")

INPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/input dataframes/"
OUTPUT_BASE_DIR = "D:/Desktop_current/NPSoftware/GitHub/Unit testing/output dataframes/"

data <- read_excel(paste(INPUT_BASE_DIR, "raw_mr_tests_withMissingData.xlsx", sep=""))
data_z <- as.data.frame(scale(data, center = TRUE, scale = TRUE))

fit <- lm(var1 ~ var2 + var3, data=data)
fit.beta <- lm.beta(fit)
summary(fit.beta) # show results
confint(fit, level=0.95)

fit_z <- lm(var1 ~ var2 + var3, data=data_z)
fit_z.beta <- lm.beta(fit_z)
summary(fit_z.beta) # show results
confint(fit_z, level=0.95)
