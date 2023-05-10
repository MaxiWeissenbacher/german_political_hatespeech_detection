library(stringi)
library(stringr)
library(igraph)
library(dplyr)
library(tm)
library(networkD3)
tweets <- read.csv("C:/Users/maxiw/OneDrive/Dokumente/InfoWi pdf/Master InfoWi/Web and Data Science/worksheets/tweets_merged_maxi.csv", encoding="UTF-8")
ds <- politicans_v2[1:10,]
head(ds)
df <- ds %>%
  select(Screen.name, mentions_chr)
df[10,]
df$Screen.name <- paste("@", df$Screen.name)
df$Screen.name <- stri_replace_all_fixed(df$Screen.name, " ", "")
df # df without party content yet


politicans <- tweets %>%
  group_by(Screen.name) %>%
  summarise(Text=paste(Text,collapse=''), .groups = 'drop', party = party)
nrow(politicans)
ncol(politicans)
head(politicans)
politicans <- unique(politicans)
test <- unique(politicans$party)
test
politicans = mutate(politicans, mentions = str_extract_all(politicans$Text, "@\\w+"))
politicans$mentions <- sapply(politicans$mentions, paste0, collapse = ' ')
politicans <- politicans %>%
  select(Screen.name,mentions, party)
# grosses Netzwerk erstellen
politicans$Screen.name <- paste("@", politicans$Screen.name)
politicans$Screen.name <- stri_replace_all_fixed(politicans$Screen.name, " ", "")
s <- strsplit(politicans$mentions, split = " ")
dataFrame <- data.frame(Screen.name = rep(politicans$Screen.name, sapply(s, length)),mentions = unlist(s))
tail(dataFrame)
graph1 <- graph.data.frame(dataFrame, directed = TRUE)
plot(graph1,
     vertex.label = NA,
     vertex.color = "red",
     edge.color = "skyblue",
     vertex.size = 2,
     edge.arrow.size = 0.1,
     vertex.label.cex = 0.8)
E(graph1)$weight <- seq(ecount(graph1))
sort(strength(graph1), decreasing = TRUE)[1:10]
sort(strength(graph1, mode="out"), decreasing = TRUE)[1:20]
sort(degree(graph1), decreasing = TRUE)[1:20]

assortativity_degree(graph1, directed = TRUE)

graph.data.frame(big_join, directed = TRUE) %>%
  set_edge_attr(name = "color", value = factor(big_join$party)) %>%
  plot(
    vertex.label = NA,
    vertex.size = 2,
    edge.arrow.size = 0.1,
    vertex.label.cex = 0.8,
  )

mygraph <- graph.data.frame(big_join, directed = TRUE) %>%
  set_edge_attr(name = "color", value = c("red", "green", "orange", "purple","yellow","black", "blue","coral","brown4","deeppink","khaki","seagreen1","thistle1")[match(big_join$party, c("SPD", "GRUENE","CDU","CSU","AfD","DIE LINKE","SPD","Piraten","Fraktionslos","Freien","Gruppe Liberal-Konservative Reformer","FDP DVP",""))]) 
plot(mygraph,
  vertex.label = NA,
  vertex.size = 2,
  edge.arrow.size = 0.1,
  vertex.label.cex = 0.8,
)


Encoding(big_join$party) <- "ISO-8859-1"


test#kleiens Test-Netzwerk
ds <- politicans[2:4,]
head(ds)
ds$Screen.name <- paste("@", ds$Screen.name) ####################### hier der Fehler im Markdown
ds$Screen.name <- stri_replace_all_fixed(ds$Screen.name, " ", "")
ds # df withouts party content yet

# Get the DataFrame in the right form
s1 <- strsplit(ds$mentions, split = " ")
df1 <- data.frame(Screen.name = rep(ds$Screen.name, sapply(s1, length)),mentions = unlist(s1))
tail(df1)
###################### joined graph approach
tail(joined_df)
joined_df[30:60,]
gj <- graph.data.frame(joined_df, directed = TRUE)
gj1 <- simplify(gj)
V(gj)$party
edge_attr(gj)
vertex_attr(gj)

graph.data.frame(joined_df, directed = TRUE) %>%
  set_edge_attr(name = "color", value = factor(joined_df$party)) %>%
  plot(
    vertex.label = NA,
    vertex.size = 2,
    edge.arrow.size = 0.1,
    vertex.label.cex = 0.8,
    layout = layout.fruchterman.reingold
  )

plot(gj,
     vertex.label = NA,
     vertex.size = 2,
     edge.arrow.size = 0.1,
     vertex.label.cex = 0.8,
     layout = layout.fruchterman.reingold)
######################
colrs <- c("red", "skyblue")
g <- graph.data.frame(df1, directed = TRUE)
plot(g)


######################
E(g)$weight <- seq(ecount(g))
sort(strength(g))
strength(g, mode="out")
sort(strength(g, mode="out"))

sort(page_rank(mygraph)$vector, decreasing = TRUE)[1:20]
pageRank <- page_rank(mygraph)$vector
df <- data.frame("pageRank" = pageRank)
write.csv(pageRank, file = "pageRank.csv", row.names = TRUE)
df <- read.csv("pageRank.csv")
head(df)
# interaktive Graph
gb <- simpleNetwork(df1)
gb
