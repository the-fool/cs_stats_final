d <- read.csv('results.csv')

## Remove candidates who have dropped out
results.all <- d[-c(5,6,9,11:15)]

## Explore pair-wise plots
library(GGally)
ggpairs(results.all[-c(1:2)])

## look closely at Cinton & Trump
ggplot(data = results.all, aes(CLINTON, TRUMP)) + 
  geom_point(alpha=0.6)

ggplot(data = results.all, aes(CLINTON, TRUMP)) + 
  scale_y_sqrt() +
  geom_point(alpha=0.6)

ggplot(data = results.all, aes(CLINTON, TRUMP)) + 
  scale_y_sqrt() + 
  geom_point(aes(colour=CRUZ)) + 
  scale_colour_gradient(low="blue", high="red")

ggplot(data = results.all, aes(CLINTON, TRUMP)) + 
  scale_y_sqrt() + 
  geom_point(aes(colour=KASICH)) + 
  scale_colour_gradient(low="blue", high="red")

ggplot(data = results.all, aes(SANDERS, TRUMP)) + 
  scale_y_sqrt() + 
  geom_point(aes(colour=KASICH)) + 
  scale_colour_gradient(low="blue", high="red")

ggplot(data = results.all, aes(SANDERS, KASICH)) + 
  scale_y_sqrt() + 
  geom_point(alpha=0.9) +
  geom_smooth()

##### Now to plot correlations

## split into two tables
results.dem <- results.all[1:4]
results.rep <- results.all[c(1:2, 5:7)]

## get correlations by county
correlations.matrix <- cor(results.dem[-c(1:2)], results.rep[-c(1:2)])

## Display the matrix
str(correlations.matrix)

## melt the matrix into long format
library(reshape2)
correlations.long = melt(correlations.matrix)

## rename columns on new data-frame
library(dplyr)
correlations.long <- rename(correlations.long, Dem = Var1, Rep = Var2, Correlation = value)

## Plot grouped by Democrat
ggplot(data = correlations.long, aes(x=Dem, y=Correlation, fill=factor(Rep))) +
    geom_bar(width=.75, stat="identity", position="dodge") +
    scale_y_continuous(breaks=pretty_breaks(n=20))

## Plot grouped by Republican
ggplot(data = correlations.long, aes(x=Rep, y=Correlation, fill=factor(Dem))) +
  geom_bar(width=0.75, stat="identity", position="dodge") +
  scale_y_continuous(breaks=pretty_breaks(n=20))

