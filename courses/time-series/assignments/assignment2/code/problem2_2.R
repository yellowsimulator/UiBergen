options( warn = -1 )

library(astsa)
data(varve)

# plot data
plot_data <- function(data){
  plot(varve,col="blue")
  title(main="Logarithm of glacial varve timeseries", col.main="blue")
  title(xlab="Time", col.lab="blue")
  title(ylab="Varve", col.lab="blue")
}

#histogram plot

histogram <- function(sample){
  hist(sample,main="Histogram of logarithm of varve data", col="blue", prob=TRUE,ylim=c(0,1))

  lines(density(sample),lwd=2,col="green")
}

# compute variance of a sample
get_variance <- function(sample){
  sample_variance <- var(sample)
  return(sample_variance)
}

# compute the logarithm of a sample
get_log <- function(sample){
  log_sample <- log(sample)
  plot(log_sample,col="blue",xlab="Time",ylab="Log varve", col.lab="blue")
  title(main="Logarithm of glacial varve timeseries", col.main="blue")
}

plot_difference <- function(sample){
  difference <- diff(sample,lag=1, differences=1)
  plot(difference,col="blue")
  title(main="Difference of log of varve data", col.main="blue")
  #title(xlab="Time", col.lab="blue")
  #title(ylab="Varve", col.lab="blue")

}



Y <- log(varve)
U <- diff(Y,lag=1, differences=1)
#emp_auto_corr_rho <- acf(U,type = "correlation")
#emp_auo_variance_gamma <- acf(U, type = "covariance")
#print(emp_auo_variance_gamma[1])
#print(emp_auo_variance_gamma[0])

x1 <- var(U)/(1-2*0.49+0.49*0.47)
x2 <- var(U)/(1-2*2+2*2)

print(x1)

print(x2)

print(var(U))











#
