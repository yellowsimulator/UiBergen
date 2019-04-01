library(TSA)

sigma = 1
phi <- c(1.4, -0.9)

f <- function(w){
  phi1 <- 1.4
  phi2 <- -0.9
  phi <- 1-phi1*w-phi2*w**2
  sigma <- 1
  denominator <- abs(1-phi1*exp(-(0+1i)*w) - phi2*exp(-(0+2i)*w))**2
  factor <- (sigma*sigma)/(2*pi)
  value <- factor*(1./denominator)
  return(value)

}
g <- function(w){
  return(exp(-(0+1000000000000000i)*w))
}
set.seed(10)
w <- seq(from=-pi, to=pi)
plot(g(w),col="red")
#logb(x,base=exp(1))
#png("theoreticalDensity2.png")
#plot(f(w), col="blue",type="b",xlab="frequency")
#png("estimatedSpecralDensity1000.png")
#ar.sim <- arima.sim(model=list(ar=c(1.4, -0.9)), n=1000)
#ts.plot(ar.sim)
#periodogram <- periodogram(ar.sim)
#amplitude <- periodogram$spec
#plot(w,amplitude)
#frequency <- periodogram$freq
#plot(frequency,amplitude,type="b")
#print(length(w))
#print(length(amplitude))
#print(amplitude)
#print("-----------------")
#print(frequency)
#pick <- max(amplitude)
#pickIndex = match(pick, amplitude)
#freq <- frequency[pickIndex]
#print(pick)
#print(freq)
#smoothPeriodogram = filter(amplitude, filter = c(1/3,3), sides=2)
#plot(smoothPeriodogram)
#estimatedSpecralDensity <- spectrum(ar.sim,method="ar")
#png("EstimatedSpectralDensity.png")
#plot(frequency,periodogram, type= "b", main = "moving average")
#plot(estimatedSpecralDensity)
