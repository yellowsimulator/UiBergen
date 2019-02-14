#2004.02.12.10.32.39
#2004.02.19.06.22.39
all_files <- list.files(path = "../data/2nd_test")
print(length(all_files))
path <- paste("../data/2nd_test",all_files[40],sep="/" )
print(path)
df <- read.table(path)
#df <- data.matrix(df1)

b1 <- data.matrix(df[c(1)])
b2 <- data.matrix(df[c(2)])
b3 <- data.matrix(df[c(3)])
b4 <- data.matrix(df[c(4)])

#acf(b1)
histogram <- function(sample){
  hist(sample,main="Histogram of logarithm of varve data", col="blue", prob=TRUE,ylim=c(0,10))

  lines(density(sample),lwd=2,col="green")
}
#print(class(b3))
acf(b1)

#fils <- list.files(path = "../data/2nd_test")
#print(fils)
#print(b1)
