library('ggplot2')
library('forecast')
library('tseries')
library('ggfortify')

daily_data = read.csv("Bike-Sharing-Dataset/day.csv",
                             header=TRUE,stringsAsFactor=FALSE)

plot_data <- function(output_file){
  daily_data$Date = as.Date(daily_data$dteday)
  #columns <- names(daily_data)
  ggplot(daily_data, aes(Date, cnt)) + geom_line() + scale_x_date('month') + ylab('Daily bike checkouts') + xlab('')+
         ggsave(file=paste(output_file,".png",sep=""), width=20, height=5, dpi=500)
  }

cleaned_data <- function(input_data){
  input_data$Date = as.Date(input_data$dteday)
  count_ts = ts(input_data[, c('cnt')])
  input_data$clean_cnt = tsclean(count_ts)
  return(input_data)
  }

plot_clean_data <- function(input_data,output_file){
  ggplot()+
     geom_line(data=input_data,aes(x=Date,y=clean_cnt)) + ylab("cleaned bicycle count")+
     ggsave(file=paste(output_file,".png",sep=""), width=20, height=5, dpi=500)
  }

plot_moving_average_with_data <- function(input_data,output_file){
  input_data$weekly_moving_average = ma(input_data$clean_cnt,order=7)
  input_data$monthly_moving_average = ma(input_data$clean_cnt,order=30)

  ggplot()+
    geom_line(data=input_data,aes(x=Date,y=weekly_moving_average, colour="Weekly moving average"))+
    geom_line(data=input_data,aes(x=Date,y=monthly_moving_average, colour="Monthly moving average"))+
    geom_line(data=input_data,aes(x=Date,y=clean_cnt, colour="Cleaned data"))+
    ylab("Bicycle count")+
    ggsave(file=paste(output_file,".png",sep=""), width=20, height=5, dpi=500)
  }

plot_decompse <- function(input_data){
  input_data$weekly_moving_average = ma(input_data$clean_cnt,order=7)
  input_data$monthly_moving_average = ma(input_data$clean_cnt,order=30)
  count_ma = ts(na.omit(input_data$monthly_moving_average), frequency=30)
  decomp = stl(count_ma, s.window="periodic")
  d_cnt <- seasadj(decomp)
  plot(decomp)

}

augmented_dickey_fuller_test <- function(input_data){
  input_data$weekly_moving_average = ma(input_data$clean_cnt,order=7)
  input_data$monthly_moving_average = ma(input_data$clean_cnt,order=30)
  count_ma = ts(na.omit(input_data$monthly_moving_average), frequency=30)
  adf.test(count_ma, alternative="stationary")

}
data <- cleaned_data(daily_data)
augmented_dickey_fuller_test(data)
