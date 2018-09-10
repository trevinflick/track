library(rvest)
library(dplyr)
library(progress)


marathon_scrape <- function(gender = "women", year = 2018) {
  

# Grab last page number of results ----------------------------------------

  url <- paste0("https://www.iaaf.org/records/toplists/road-running/marathon/outdoor/", gender, "/senior/", year, "?regionType=world&drop=regular&fiftyPercentRule=regular&page=1&bestResultsOnly=false")
  
  page_one_info <- read_html(url)
  
  last_page <- page_one_info %>% 
    html_node(".pag--show") %>% 
    xml_attr("data-page") %>% 
    as.integer()
  
  if (is.na(last_page)) {
    last_page <- page_one_info %>% 
      html_nodes("a.btn--number") %>%
      xml_attr("data-page") %>%
      as.integer() %>%
      max()
  }
  
  pages <- seq(from = 1, to = last_page)
  
  pb <- progress_bar$new(
    format = "fetching [:bar] :percent eta: :eta",
    total = last_page, clear = FALSE, width = 60)
  
  list_of_dfs <- list()
  

# Download data -----------------------------------------------------------

  for (page in seq_along(pages)) {
    url <- paste0("https://www.iaaf.org/records/toplists/road-running/marathon/outdoor/", gender, "/senior/", year, "?regionType=world&drop=regular&fiftyPercentRule=regular&page=", page, "&bestResultsOnly=false")
    
    pb$tick()
    
    seq(from = 30, to = 35, by = 0.001) %>%
      sample(1) %>%
      Sys.sleep()
    
    tables <- read_html(url) %>%
      html_nodes("table")
    
    df <- tables %>% 
      .[[3]] %>% html_table(fill = TRUE)
    
    list_of_dfs[[page]] <- df
  }


# Save results as a data frame --------------------------------------------

  results <- do.call(rbind, list_of_dfs)
  
  results <- results[ , !duplicated(colnames(results))]
  
  results[7] <- NULL
  
  results <- results %>%
          select(Mark, Competitor, DOB, Nat, Venue, Date) %>%
          rename(c("Mark" = "Result"))
  
  return(results)
}



  
  
    
    

  

  
