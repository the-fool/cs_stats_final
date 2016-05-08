setwd("~/workspace/cs280_stats/final_proj")
demographics <- read.csv("./results_with_demograph.csv")
d <- read.csv('results.csv')



## Remove candidates who have dropped out
results.all <- d[-c(5,6,9,11:15)]

## Explore pair-wise plots
library(GGally)
ggpairs(results.all[-c(1:2)])

## look closely at Cinton & Trump
library(ggplot2)
library(scales)
ggplot(data = results.all, aes(CLINTON, TRUMP)) + 
  geom_point(alpha=0.6)

## Adjust y-axis to handle more precision at lower levels
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

## Now get correlations for various demographic stats
## The stats of interest are Average Income, Percent Black, Percent BA Degrees, Population Density, and Unemployed

cor.demographics.dem <- cor(demographics[c('SANDERS','CLINTON')], demographics[c('AvgInc', 'PcntBlack', 'BADeg', 'PopDens', 'Unemployed')], use="complete.obs")
cor.demographics.rep <- cor(demographics[c('TRUMP', 'CRUZ', 'KASICH')], demographics[c('AvgInc', 'PcntBlack', 'BADeg', 'PopDens', 'Unemployed')], use="complete.obs")
cor.demographics.dem.long <- rename(melt(cor.demographics.dem), Candidate = Var1, Demographic = Var2, Correlation = value)
cor.demographics.rep.long <- rename(melt(cor.demographics.rep), Candidate = Var1, Demographic = Var2, Correlation = value)

## Plot the correlations
ggplot(data = cor.demographics.dem.long, aes(x=Demographic, y=Correlation, fill=factor(Candidate))) +
  geom_bar(width=.75, stat="identity", position="dodge") +
  scale_y_continuous(breaks=pretty_breaks(n=20))

ggplot(data = cor.demographics.rep.long, aes(x=Demographic, y=Correlation, fill=factor(Candidate))) +
  geom_bar(width=0.75, stat="identity", position="dodge") +
  scale_y_continuous(breaks=pretty_breaks(n=20))

## Now get the differences of correlations for each candidate
cor.demographics.merged <- merge(
  cor.demographics.dem.long, 
  cor.demographics.rep.long, 
  by = 'Demographic'
)

cor.demographics.merged$Candidates <- paste(
    as.character(cor.demographics.merged$Candidate.x), 
    as.character(cor.demographics.merged$Candidate.y), 
    sep = " / "
)

cor.demographics.merged$CorrelationDifference <- abs(cor.demographics.merged$Correlation.x - cor.demographics.merged$Correlation.y)

## Plot these differences
ggplot(data = cor.demographics.merged, aes(x = Demographic, y = CorrelationDifference, fill=factor(Candidates))) +
  geom_bar(width=0.7, stat="identity", position="dodge") +
  scale_y_continuous(breaks=pretty_breaks(n=20))
