
library(TSA)
set.seed(10)
#,sep="",header=TRUE,row.names=TRUE,col.names=TRUE
yearlySunsplts <- na.omit(read.table(file="data/yearly_sunspots.txt",header=TRUE))
X <- yearlySunsplts$sunspots
Y <- X-mean(X)
m <- length(Y)
ar2 <- ar(Y,order.max=2)
#ar <- arima(model=list(ar=c(1.3666, -0.6792),order=c(2,0,0)),n=m,sd=sqrt(704.1))
ar<-arima(Y, order=c(2,0,0))
png("note/residualSpec.png")
residu <- ar$residuals
spevtrum <- spectrum(residu)
plot(spevtrum,col="blue",type="b")
