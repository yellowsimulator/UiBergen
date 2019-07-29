################
# Assignment 2 #
################


# Ex. 1
# -----

# 1.

# the t-test is appropriate, since the variance is unknown. Otherwise, the z-test would have been preferable

# 2.
# read data
dat <- read.csv("Barley.csv", header = TRUE)
attach(dat) # access colums of the data set "dat" by its names
head(dat)
barley[1 : 6]
summary(barley) # some basic stats
# experimental hypothesis is that the yield is greater than 150 grams.
# thus, the statistical hypotheses are
# H0: mu <= 150, H1: mu > 150, 
# because this allows us to control the error of type I (via alpha), i.e. the probability of concluding that the yield is greater than 150, although in reality it is not 
t.test(barley, mu = 150, alternative = "greater")
# H0 can be rejected at level 10%, but not at 5%. so, keep your land, or lower the price

# 3.
t.test(barley, mu = 147, alternative = "two.sided")
# the null hypothesis can be rejected for an alpha of 10%. it could also be rejected for a level of 5% or 1% - but not 0.1%

# 4.
# the confidence interval is mentioned in the output.
# the result of the test can be directly deduced from the
# confidence band. For example:
t.test(barley, mu = 147, alternative = "two.sided",
       conf.level = 0.99)
t.test(barley, mu = 147, alternative = "two.sided",
       conf.level = 0.999)
# note that only the conf. interval a 99.9% includes the value 147. thus,
# the hypothesis of mean equal to 147 cannot be rejected for a given level
# alpha of 0.1% (0.0001)
       
# note that the assumption of normality should be tested
shapiro.test(barley)
hist(barley, breaks = 20)
# as this example shows, the normality hypothesis is rejected here. hence, the t-test was not the best choice here
detach(dat)

# 5.
# reading the data and "attaching" it
dat <- read.table("Partners.dat", header = TRUE)
attach(dat)

# visualization
head(dat)
# looking at the data set, the number of partners is count data. thus, it seems in principle quite unlikely that the assumption of a Gaussian distribution is satisfied
par(mfrow = c(2, 1))
hist(partners[sex == "m"], main = "Male particip.")
hist(partners[sex == "f"], main = "Female particip.")
# in particular the female group does not look Gaussian at all

# testing
shapiro.test(partners[sex == "m"])
shapiro.test(partners[sex == "f"])
# normality is clearly rejected for the female group. note that this is not the case for the male group, although the data are also counts. the reason is that count data can be approximately normally distriuted, and this is sufficient for not rejecting the normality hypothesis. in general, this is only the case if the data take a large number of different count values and are approximately symmetric (not skewed), i.e. they should "look normal"

# what would you tell your colleage apart from this?
# 1. were covariates taken into account? e.g. females could be very young, and males older, thus a bad experimental setup.
# 2. "self-report bias": honesty reduces when it comes to topics considered sensitive, e.g. sexual behaviour or diseases, wealth, drug use,...

detach(dat)



# Ex. 2
# -----

# 1.
# Voters can (should) be considered being independent of each other. Under the
# null hypothesis, they vote each with probability 0.5 for Bush.
# Binomial distribution: sum of i.i.d. Bernoulli experiments
# P(X = x) = (9 x) * pi ^ x * (1 - pi) ^ (9 - x), 
# for x = 0,...,9, else 0,
# where (n k) corresponds to the binomial coefficient n! / (k! x (n - k)!)
x <- 0 : 9
par(mfrow = c(3, 1))
par(mgp = c(1.5, 0.5, 0), 
    mar = c(3, 2.5, 1.0, 1))
y <- dbinom(x, 9, prob = 0.5)
plot(x, y, type = "h", lwd = 3, xlab = "x", ylab = "P(x)",
     main = "pi = 0.5")
y <- dbinom(x, 9, prob = 0.1)
plot(x, y, type = "h", lwd = 3, xlab = "x", ylab = "P(x)",
     main = "pi = 0.1")
y <- dbinom(x, 9, prob = 0.9)
plot(x, y, type = "h", lwd = 3, xlab = "x", ylab = "P(x)",
     main = "pi = 0.9")
# output figure
    
# 2.
# First, recall the definition of a p-value. Several exist, e.g.:
#
# 1. In statistical significance testing, the p-value
# is the probability of obtaining a test statistic at
# least as extreme as the one that was actually
# observed, assuming that the null hypothesis is true.
#
# 2. For a statistical test, the p-value corresponds to the lowest possible 
# level of the test (the alpha) for which the null hypothesis can be rejected
# 
# The lower the p-value, the less likely the result is
# if the null hypothesis is true, and consequently
# the more "significant" the result is, in the
# sense of statistical significance.
# One often accepts the alternative hypothesis,
# (i.e. rejects a null hypothesis) if the p-value
# is less than 0.05 or 0.01, corresponding
# respectively to a 5% or 1% chance of rejecting
# the null hypothesis when it is true (type I error).

# a)
y <- dbinom(x, 9, prob = 0.5) # striclty, pi = 0.4999999999....same result
sum(y[8 : 10]) # zone of rejection 7, 8, 9 -> position 8 a 10 of the vector
# probability of error type I is thus ~0.09
# b)
par(mfrow = c(1, 1))
plot(x, y, type = "h", lwd = 3, xlab = "x", ylab = "P(x)",
     main = "Zone of rejection (red) / non-rejection (blue)")
#abline(v = 2.5, col = "blue")
lines(c(7, 9), c(0, 0), col = "red", lwd = 3)
lines(c(-0.02, 6.02), c(0, 0), col = "blue", lwd = 3)
# c)
round(cumsum(y[10 : 1]), 3)
# if 9 votes for Bush are observed, the corresponding p-value is 0.002,
# for 8 votes it the p-value equals 0.020 and so on... 
# note: [10 : 1] is not necessary here since the distibution is symmetric. however, this changes if pi changes

# 3.
# probability of not rejection H0 when H1 is "just" true (pi = 0.5)
sum(y[1 : 7])
# ~same as 1 - alpha from type I error for pi = 0.5. this is not the case for other values of pi:
sum(dbinom(x, 9, prob = 0.6)[1 : 7])
sum(dbinom(x, 9, prob = 0.8)[1 : 7])
# in practice, one would say something like: "we would like to detect a true value of pi greater than e.g. 0.6" with a certain probability, e.g. 80%. then, the necessary sample size would be determined 


# 4.
x <- 0 : 9
v.prob <- c(0.1, 0.2, 0.3, 0.4, 0.4999,
            0.5, 0.6, 0.7, 0.8, 0.9)
p.reject <- c()
p.not.reject <- c()
for (i in 1 : length(v.prob)) {
  p.reject[i] <- sum(dbinom(x, 9, prob = v.prob[i])[8 : 10])
  p.not.reject[i] <- 1 - p.reject[i]
}
round(cbind(p.reject, p.not.reject), 3)

# pi      H0 true/  P(reject H0)      P(not reject H0)
#         false 
# ------------------------------------------------
# 0.1     true      0.0000            1.0000                           
# 0.2     true      0.0003            0.9997
# 0.3     true      0.004             0.996
# 0.4     true      0.03              0.97
# 0.4999  true      0.09              0.91
# 0.5     false     0.09              0.91
# 0.6     false     0.23              0.77
# 0.7     false     0.46              0.54
# 0.8     false     0.74              0.26
# 0.9     false     0.95              0.05


# 5.
v.prob <- seq(0, 1, by = 0.01) # for getting a smooth curve
p.reject <- c()
p.not.reject <- c()
for (i in 1 : length(v.prob)) {
  p.reject[i] <- sum(dbinom(x, 9, prob = v.prob[i])[8 : 10])
  p.not.reject[i] <- 1 - p.reject[i]
}

plot(v.prob, p.reject, type = "l", lwd = 2.5,
     xlab = expression(paste("True value of  ", pi)),
     ylab = "Probability of (not) rejecting the Null",
     main = "Visualization of errors of type I/II")
lines(v.prob, p.not.reject, lwd = 2.5, col = grey(0.6))
abline(v = 0.5, col = "blue")
legend("topright",
       c(expression(paste("Prob. rejecting ", H[0])),
         expression(paste("Prob. not rejecting ", H[0]))),
       lwd = c(2.5, 2.5),
       col = c("black", grey(0.6)),
       bg = "white"
      )
# Remark: an alternative approach would be to use the function "curve()"



# Ex. 3
# -----

# 1.
# small plot first
x <- 0 : 356
y <- dbinom(x, size = 356, prob = 0.5)
plot(x, y, type = "h", lwd = 1, xlab = "x",
     ylab = "P(x)", xlim = c(160, 356))
# example: probability of 201 votes or more
pbinom(200, size = 356, prob = 0.5, lower.tail = FALSE)
?pbinom # attention to the upper tail definition!
sum(y[202 : 357])
# not very likely to observe 201 or more votes, only ~0.849%
# thus, one would reject the hypothesis at level 5% and 1%
# however, if we set alpha = 0.1%, the number of votes is not high enough for
# rejecting the hypothesis of a pi smaller than / equal to (for computational convenience) 0.5

# 2.
# Several possibilities exist: e.g., by manually playing with dbinom or qbinom
# Alternatively, qbinom is faster, recall the definition of a quantile function
# Case 0.1%
qbinom(0.001, size = 356, prob = 0.5, lower.tail = FALSE) # with 207 votes or more, the probability mass is just equal or above 0.1%. quick checks:
sum(y[208 : 357]) # probability of 207 or more votes
pbinom(207, size = 356, prob = 0.5, lower.tail = FALSE)  # 208 or more votes
sum(y[209 : 357]) # prob. of 208 or more votes
# conclusion: we need 208 or more votes for rejecting the hypothesis for
# a given alpha of 0.1%  

# Case 1%
qbinom(0.01, size = 356, prob = 0.5, lower.tail = FALSE) # with 200 votes or more, the probability mass is just equal or above 1%. checks:
sum(y[201 : 357]) # 200 or more votes
pbinom(200, size = 356, prob = 0.5, lower.tail = FALSE)  # 201 or more votes 
sum(y[202 : 357]) # 201 or more votes 

# Case 5%
qbinom(0.05, size = 356, prob = 0.5, lower.tail = FALSE) # with 194 votes or more, the probability mass is just equal or above 5%. checks:
sum(y[195 : 357]) # 194 or more votes
pbinom(194, size = 356, prob = 0.5, lower.tail = FALSE)  # 195 or more votes 
sum(y[196 : 357]) # 195 or more votes 

# 3.
# Again with the loop, curve() would be an alternative
v.prob <- seq(0, 1, by = 0.01)
p.reject <- c()
p.not.reject <- c()
for (i in 1 : length(v.prob)) {
  p.reject[i] <- sum(dbinom(x, 356, 
                            prob = v.prob[i])[196 : 357])
  p.not.reject[i] <- 1 - p.reject[i]
}
# plotting
plot(v.prob, p.reject, type = "l", lwd = 2.5,
     xlab = expression(paste("True value of  ", pi)),
     ylab = "Probability of (not) rejecting the null hypothesis",
     main = "Visualization of errors of type I/II")
lines(v.prob, p.not.reject, lwd = 2.5, col = grey(0.6))
abline(v = 0.5, col = "blue")
legend("topright",
       c(expression(paste("Prob. rejecting ", H[0])),
         expression(paste("Prob. not rejecting ", H[0]))),
       lwd = c(2.5, 2.5),
       col = c("black", grey(0.6)),
       bg = "white"
      )
# a larger sample size causes a faster reduction of errors of type II when the true pi moves to values above 0.5



