

# Rcode from question 6
#Determine reading csv files in R: https://swcarpentry.github.io/r-novice-inflammation/11-supp-read-write-csv/
#Removing nan containing columns: https://www.statology.org/remove-columns-with-na-in-r/
#Creating a function in R: https://swcarpentry.github.io/r-novice-inflammation/02-func-R/
#Building box plots: https://www.statmethods.net/graphs/boxplot.html
#set seed: https://r-coder.com/set-seed-r/'
#if statements : https://bookdown.org/ndphillips/YaRrr/using-if-then-statements-in-functions.html

####Fuction that reads csv files and removes columns where all values are NAN####
read_clean <- function(filename, thresh, samplesize) { #file name = name of csv file or directory of csv file, thresh = threshold of number of rows in data fram, samplesize = size of desired sample to pull from dataframe
    file_data <- read.csv(filename) #read csv file
    df <- data.frame(file_data) #convert read data into data frame
    new_df <- df[ , colSums(is.na(df))==0] #remove columns where all values are nan
    if (nrow(df) > thresh) { #if statement that samples the index of desired number of rows from data frame and forms a new sampled data frame with the sampled indices
        sampled_rows <- sample(1:nrow(new_df), samplesize)
        sampled_df <- new_df[sampled_rows, ]
    }
}
#################################################################################

file <- '/anvil/projects/tdm/data/flights/subset/1991.csv'
threshold <- 1000
samples <- 200
set.seed(10) #random set to ensure data is reproducible
flights <- read_clean(file, threshold, samples)

head(flights) #checks on dataframe to make sure the proper columns are dropped

#box plot for visualizing distribution and outliers of CRS elasped times for each month
boxplot(CRSElapsedTime~Month, data = flights, main = "CRSElapsedTimes", xlab = "Month", ylab = "Elapsed Time", ylim = c(0 , 480)) 
