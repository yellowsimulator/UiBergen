
#maq <- read.delim("ma_q.txt")
#png("../note/simulated-arma2_2_plus.png")
#simulated_ma <- maq$x
#pacf(simulated_ma)
#K <- seq(1,20)
#AIC = c()


#arma2_2 <- arima.sim(n = 50*500,list(ar = c(-0.7, 0.2),ma = c(0.3, -0.2)),sd = 4)
ar_2 <- arima.sim(n = 1000,list(ar = c(1.4, -0.8),sd = 1))
print(5 + 1i)
#png("../note/p94ar2.png")
#plot(ar_2)
#plot(arma2_2)
#fitted_MA5_model <- arima(x=arma2_2, order=c(0,0,5), method="ML")
#aic <- AIC(fitted_MA5_model)
#bic <- AIC(fitted_MA5_model,k = log(length(fitted_MA5_model)))
#print(aic)
#print(bic)
#frequency <- arma.spec(ar = 0, ma = 5, var.noise = 1, n.freq = 500)
#print(frequency)
#library(TSA)
#periodogram <- periodogram(fitted_MA5_model)
#frequency = periodogram$freq
#print(frequency)
#amplitude <- periodogram$spec
#plot(w,amplitude)
#frequency <- periodogram$freq
#for (k in K)
#{
  #print(k)
#png("../note/pacf-selected-ma.png")
#model <- arima(x=simulated_ma, order=c(0,0,5), method="ML")
#coefficients = coef(model)
##ma1 = coefficients["ma1"]
#ma2 = coefficients["ma2"]
#ma3 = coefficients["ma3"]
#ma4 = coefficients["ma4"]
#ma5 = coefficients["ma5"]

#selected_ma_order_5 <- arima.sim(n = length(simulated_ma), list(ma = c(ma1,ma2,ma3,ma4,ma5)))
#pacf(selected_ma_order_5)
  #aic <- AIC(model)
  #bic <- AIC(model,k = log(length(y)))
  #AIC = append(AIC, aic)
  #BIC = append(BIC, bic)
#}
#min_bic = min(BIC)
#index_min_bic = which(BIC == min_bic)
#max_bic = max(BIC)

#min_aic = min(AIC)
#index_min_aic = which(AIC == min_aic)
#max_aic = max(AIC)
