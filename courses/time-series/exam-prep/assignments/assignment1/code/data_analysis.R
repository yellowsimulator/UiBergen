
# load data
data <- read.table("deaths.txt", skip=9, header=FALSE)

# add columns names to data
names(data) <- c("month", "year", "deaths")

#rearange date as datetime ie. yyyy-mm-15
data$time <- as.Date(paste(data$year, data$month, "15", sep="-"))

#plot death vs time
attach(data)
png("time-vs-death.png")
plot(time,deaths/1000, type="l", xlab="", ylab="deaths in thousands")
png("acf.png")
acf(deaths, lag.max=24)
png("histogram.png")
hist(deaths, breaks=15)
#print(data)
