#install.packages("ggplot2")
library('ggplot2')
library('forecast')
library('tseries')
set.seed(1234)
require(graphics)
x <- arima.sim(
  model = list(ar = 0.7),
  n = 1000,
  innov = rnorm(1000, sd = 2)
)
plot(x)
