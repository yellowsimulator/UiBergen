


# Exercise 1
# ----------

# 1.1
# ---
# First we assess the accurcy of the coefficient of the
# multiple linear regression, and decide weither there
# is a relationship between the response expenditure and the
# the preictors income and country. For that
# We are testing the null hypothesis H0 versus the alternative
# hypothesis.

# H0: There is no relationship between the predictors income,
# country and the response expenditure.
# Ha: There is some relationship between the predictors income,
# country and the response expenditure.

# The linear model is then given by
# expenditure = beta0 + beta1*income + beta2*country
# and the hypothesis test is

# H0: beta1 = beta2 = 0
# H1 beta1 != beat2 != 0


abspath <- normalizePath("./gsa.csv")
# The following command gets the absolute path of the file
# "gsa.csv"

dat <- read.csv(abspath)
attach(dat)
model <- lm(expenditure ~ income + country)
summary(model)
#confint(model, level=0.95)
#anova(model)
# The F-statistic is 219.9 which is very large (higher than 1),
# the pvalue is very small (less than the significance leve of 0.05)
# this ptovide a compalling evidence that there is a relatioship
# between the response and the predictors. Thus the null hypothesis
# is rejected in favour of the alternative hypothesis.

# Next we assess the accuracy of the model
# The Multiple R-squared and the Adjusted R-squared are respectively
# 0.2861 and 0.2848, which are very small. This sugests
# that approximately 28 % of variability in expenditure can be
# explained by the model.

# Next we perform feature importance.
incomeModel <- lm(expenditure ~ income)
summary(incomeModel)
# The Adjusted R-square is aproximately 0.0786. This mean that 7.86 %
# of the variablity in the response can be explained by the income alone.

countryModel <- lm(expenditure ~ income)
summary(countryModel)
# The adjusted R-square is also 0.0786

# We can conclude that the model with income and country is better
# than the one with individual predictors income and country




# 1.2
# ----
fullModel <- lm(expenditure~income+country+accomodation+year)
summary(fullModel)
# With the full model, the adjusted R-square increase to 0.3842.
fullModelNoYear <- lm(expenditure~income+country+accomodation)
summary(fullModelNoYear)
# removing year does not affect the Adjusted R-square

fullModelNoAccomodation <- lm(expenditure~income+country+year)
summary(fullModelNoAccomodation)
# With this model the Adjusted R-square drop to 0.2883.

# in conclusion, the model with income, country and accomodation
# is the best model


# 1.3
# ---
# since the data has been collected over time probability a time series
# analysis will be appropriate?
detach(dat)


# Exercise 2
# ----------

# 2.1
# ----

absPathElisaRedStats <- normalizePath("./ELISA red stats.csv")
dat1 <- read.csv(absPathElisaRedStats)
attach(dat1)
vaccine1Day100 <- dat1[ which(Vaccine=="Past 1" & Day==100),]
vaccine1Day200 <- dat1[ which(Vaccine=="Past 1" & Day==200),]
vaccine1Day300 <- dat1[ which(Vaccine=="Past 1" & Day==300),]
vaccine1Day400 <- dat1[ which(Vaccine=="Past 1" & Day==400),]
vaccine1Day500 <- dat1[ which(Vaccine=="Past 1" & Day==500),]
vaccine1Day600 <- dat1[ which(Vaccine=="Past 1" & Day==600),]
# We get all Vaccine 1 data for each Day
png("Vaccine1.png")
par(mfrow=c(3,2))
plot(vaccine1Day100$Abs,main="Day 100")
plot(vaccine1Day200$Abs,main="Day 200")
plot(vaccine1Day300$Abs,main="Day 300")
plot(vaccine1Day400$Abs,main="Day 400")
plot(vaccine1Day500$Abs,main="Day 500")
plot(vaccine1Day600$Abs,main="Day 600")
# Then we plot that data


# We perform the same process for Vaccine 2
vaccine2Day100 <- dat1[ which(Vaccine=="Past 2" & Day==100),]
vaccine2Day200 <- dat1[ which(Vaccine=="Past 2" & Day==200),]
vaccine2Day300 <- dat1[ which(Vaccine=="Past 2" & Day==300),]
vaccine2Day400 <- dat1[ which(Vaccine=="Past 2" & Day==400),]
vaccine2Day500 <- dat1[ which(Vaccine=="Past 2" & Day==500),]
vaccine2Day600 <- dat1[ which(Vaccine=="Past 2" & Day==600),]
# We get all Vaccine 1 data for each Day
png("Vaccine2.png")
par(mfrow=c(3,2))
plot(vaccine2Day100$Abs,main="Day 100")
plot(vaccine2Day200$Abs,main="Day 200")
plot(vaccine2Day300$Abs,main="Day 300")
plot(vaccine2Day400$Abs,main="Day 400")
plot(vaccine2Day500$Abs,main="Day 500")
plot(vaccine2Day600$Abs,main="Day 600")


# 2.2
# ---
