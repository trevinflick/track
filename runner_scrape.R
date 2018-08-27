# Scrape results from runners
# limited to races 3km and above
# results only available through 2017
# library(xml2)
# library(rvest)
# library(dplyr)

runner_scrape <- function(id) {
  url <- paste0("https://more.arrs.run/runner/", id)
  data <- read_html(url) %>% html_nodes("table") %>%
    .[[2]] %>% html_table(fill = TRUE)
  df <- as.data.frame(data)
  return(df)
}

