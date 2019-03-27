
Barley <- read.csv("../Barley.csv")

mean <- mean(Barley$barley)
alpha <- 0.1 # 10%
level <- 1-alpha
test <- t.test(Barley$barley, mu=147, alternative="two.sided", conf.level=level)
shapiro <- shapiro.test(Barley$barley)
print(shapiro)
#print(test)
