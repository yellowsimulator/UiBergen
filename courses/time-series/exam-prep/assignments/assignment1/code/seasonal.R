library('itsmr')

## Decpmposed data into trend and seasonality
## and plot
data <- read.table("deaths.txt", skip=9, header=FALSE)
# add columns names to data
names(data) <- c("month", "year", "deaths")
#rearange date as datetime ie. yyyy-mm-15
data$time <- as.Date(paste(data$year, data$month, "15", sep="-"))
attach(data)
#removing the seasonality
#from the autocorrolation function acf plot we know the period is 12
st <- season(deaths, 12)
dtr <- deaths - st # remove seasonality


#Plot deseasonal data
png("deseasonal.png")
plot(time,dtr/1000, type="b", xlab="",ylab="(thousands)")
#add trend line
lines(time,trend(dtr,2)/1000,col=2)# trand line
#plot seasonal components
png("seasonal.png")
plot(time, season(deaths, 12), type="b", xlab="",ylab="(thousands)")
abline(h=0) # add horizontal line at zero


#get noise
trend_data <- trend(deaths,2)
seasonal_data <- season(deaths,12)
noise <- deaths-trend_data-seasonal_data 
png("acf_noise.png")
acf(noise,lag.max=24)
#seasonal <- seasonal.component(x=deaths)
