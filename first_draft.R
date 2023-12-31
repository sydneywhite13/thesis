# R script to run analyses of Discover Weekly experiments

# cna also be done rudimentarily in Excel (for now) 

'''
notes: 
t tests in R are t.test(var1, var2)
OR
t test (var1, mu = )
OR
t test(var ~ var2) 
OR
t test(var, conf.level = .8)
and conclude that "there is (not) evidence (p = ) that ...


tests that you want to run:
- t test for significantly different proportions by user gender (male/female)
- chi square test for significantly different proportions between mulitple user identity groups
- t test for different proportions between male and female user of the same genre
- chi square test for different proportions between all identities of the same input data
- confidence interval for the true mean proportion of women in discover weekly 
- t test if true proprtion == STATISTICAL CRITERA OF FAIRNESS

(theoretically you could determine multiple statistical critera of fairness
and run them all and discuss their outcomes and meanings and shortcomings)
- tests of all sorts of other things you will need to measure
'''

library("readxl")
file.choose()
sydw13 <- read.csv("C:\\Users\\16107\\OneDrive\\senior year\\thesis\\my_disc_weekly_tracks_wgender_sydw13.csv")
lucy <- read.csv("C:\\Users\\16107\\OneDrive\\senior year\\thesis\\my_disc_weekly_tracks_wgender_3lemann.csv")
aoi <- read.csv("C:\\Users\\16107\\OneDrive\\senior year\\thesis\\my_disc_weekly_tracks_wgender_aoi.csv")
libby <- read.csv("C:\\Users\\16107\\OneDrive\\senior year\\thesis\\my_disc_weekly_tracks_wgender_libbytuttle.csv")
kate <- read.csv("C:\\Users\\16107\\OneDrive\\senior year\\thesis\\my_disc_weekly_tracks_wgender_katewiesehunter.csv")

lucy$duration_s <- lucy$duration_ms*0.001
lucy$minutes <- floor(lucy$duration_s/60)
lucy$seconds <- (lucy$duration_s %% 60)

sydw13$duration_s <- sydw13$duration_ms*0.001
sydw13$minutes <- floor(sydw13$duration_s/60)
sydw13$seconds <- (sydw13$duration_s %% 60)

aoi$duration_s <- aoi$duration_ms*0.001
aoi$minutes <- floor(aoi$duration_s/60)
aoi$seconds <- (aoi$duration_s %% 60)

libby$duration_s <- libby$duration_ms*0.001
libby$minutes <- floor(libby$duration_s/60)
libby$seconds <- (libby$duration_s %% 60)

kate$duration_s <- kate$duration_ms*0.001
kate$minutes <- floor(kate$duration_s/60)
kate$seconds <- (kate$duration_s %% 60)

View(sydw13)
View(libby)

total <- rbind(sydw13, libby, aoi, kate)

View(total)

# get some preliminary diagnostics on the data

# the classification 
mean(total$flag)
sum(total$flag)
table(total$pronoun)

# with flags and unknowns = 11 + 63 = 74 poorly/un - classified entries 
library(ggplot2)

ggplot(total, aes(x=factor(pronoun))) + 
  geom_bar(position="dodge") + 
  labs(title="Pronoun Distribution") + 
  geom_text(aes(label=..count..), stat='count')

# other metrics 
mean(total$danceability)
mean(total$energy)
mean(total$loudness)
mean(total$duration_s)/60

# for every user who helped me out
# metrics they might like:
# - gender breakdown
table(sydw13$pronoun)
table(aoi$pronoun)

values = c(2, 1, 5, 4, 16, 2)
ls = c('male group', 'female group', 'men', 'nonbinary', 'unknown', 'women')
pie(values, labels = ls, main="Aoi's Gender Breakdown")


table(libby$pronoun)

values = c(1, 1, 4, 1, 18, 5)
ls = c('male group', 'female group', 'men', 'nonbinary', 'unknown', 'women')
pie(values, labels = ls, main="Libby's Gender Breakdown")


table(kate$pronoun)


values = c(2, 4, 6, 16, 2)
ls = c('male group', 'men', 'nonbinary', 'unknown', 'women')
pie(values, labels = ls, main="Kate's Gender Breakdown")


values = c(3, 1, 9, 13, 3)
ls = c('male group', 'men', 'nonbinary', 'unknown', 'women')

pie(values, labels = ls, main="Sydney's Gender Breakdown")

# - danceability 
mean(sydw13$danceability)
mean(aoi$danceability)
mean(libby$danceability)
mean(kate$danceability)

# - energy 
mean(sydw13$energy)
mean(aoi$energy)
mean(libby$energy)
mean(kate$energy)

# - liveness
mean(sydw13$liveness)
mean(aoi$liveness)
mean(libby$liveness)
mean(kate$liveness)

# out of everyone, how do we rank on...

# count on H and GH
# count on W and GW and divide 
library(tidyverse)
gender_pro <- c()
class <- c(sum(sydw13$flag), sum(aoi$flag), sum(libby$flag), sum(kate$flag))
danceability <- c(mean(sydw13$danceability), mean(aoi$danceability), mean(libby$danceability), mean(kate$danceability))
energy <- c(mean(sydw13$energy), mean(aoi$energy), mean(libby$energy), mean(kate$energy))
names <- c('sydney', 'aoi', 'libby', 'kate')
loudness <- c(mean(sydw13$loudness), mean(aoi$loudness), mean(libby$loudness), mean(kate$loudness))
duration_s <- c(mean(sydw13$duration_s), mean(aoi$duration_s), mean(libby$duration_s), mean(kate$duration_s))

users <- data.frame(class, danceability, energy, names, loudness, duration_s)

par(mfrow=c(2,2))

# gender proportion 
ggplot(users, aes(x=names, y=class))+
  geom_col(aes(fill=names)) +
  labs(title = 'Number of Artists Failed to Categorize (aka the hardest and worst)', x = '', y = 'Inconclusive Results')

# danceability 
ggplot(users, aes(x=names, y =danceability)) + 
  geom_col(aes(fill=names)) + ylim(0, 1) + 
  labs(title="Danceability", x = '', y ="Score")

ggplot(users, aes(x=names, y =energy)) + 
    geom_col(aes(fill=names)) + ylim(0, 1) + 
  labs(title="Energy", x= '', y= "Score")
  
# duration_s 
  ggplot(users, aes(x=names, y =duration_s)) + 
    geom_col(aes(fill=names)) + labs(title="Length (in seconds)")
  
  ggplot(users, aes(x=names, y =duration_s/60)) + 
    geom_col(aes(fill=names)) + labs(title="Length (in minutes)")

library(ggplot2)

ggplot(lucy, aes(x=factor(pronoun))) + 
  geom_bar(position="dodge") + 
  labs(title="Pronoun Distribution") + 
  geom_text(aes(label=..count..), stat='count')

summary(lucy)

mean(lucy$danceability)
mean(lucy$energy)
mode(lucy$key)
mean(lucy$loudness)
mean(lucy$speechiness)
mean(lucy$acoustiness)
mean(lucy$instrumentalness)
mean(lucy$liveness)
mean(lucy$duration_ms)
mean(lucy$flag)
