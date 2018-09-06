library(rvest)
library(dplyr)


half_scrape <- function(gender = "women", year = 2018, top = 100) {
  
  num_pages <- top / 100
  pages <- seq(num_pages)
  
  list_of_dfs <- list()
  
  for (page in seq_along(pages)) {
    url <- paste0("https://www.iaaf.org/records/toplists/road-running/half-marathon/outdoor/", gender, "/senior/", year, "?regionType=world&drop=regular&fiftyPercentRule=regular&page=", page, "&bestResultsOnly=false")
    
    seq(30, 35, by = 0.001) %>%
      sample(1) %>%
      Sys.sleep()
    
    tables <- read_html(url) %>%
      html_nodes("table")
    
    if (length(tables) > 2) {
      df <- tables %>% 
        .[[3]] %>% html_table(fill = TRUE)
    } else {
      break
    }
    
    list_of_dfs[[page]] <- df
  }
  
  results <- as.data.frame(bind_rows(list_of_dfs))
  
  results <- results[ , !duplicated(colnames(results))]
  
  results[7] <- NULL
  
  results <- results %>%
    select(Mark, Competitor, DOB, Nat, Venue, Date) %>%
    rename(c("Mark" = "Result"))
  
  return(results)
}