#!/usr/bin/R

suppressMessages(library(pdftools))

args <- commandArgs(trailingOnly = TRUE)
print(Sys.Date())
if (length(args) == 0) {
  stop("At least one argument must be supplied (input file)", call. = FALSE)
} else if (length(args) >= 1) {
  print(args[1])
  print(args[2])
}
text_file <- args[1]
filename <- args[2]

tryCatch(
  {
    txt <- pdf_text(text_file)
    fileConn <- file(paste(filename, sep = ''))
    writeLines(txt, fileConn)
    close(fileConn)
  },
  error = function(e) {
    # Handle the error
    cat("An error occurred:", conditionMessage(e), "\n")
    # You can take appropriate actions, such as logging or displaying a specific message
  },
  finally = {
    # Clean up or perform any necessary actions regardless of whether an error occurred or not
  }
)