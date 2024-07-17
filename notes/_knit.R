## Set the working directory as the location of the _knit.R file (default rmarkdown and Rmd configurations)

## knit ----
rmarkdown::render("./notes/notes.Rmd", 
                  output_dir = "./_knit")

md_filename <- "./_knit/notes.md"
md_txt <- readLines(md_filename)
md_txt <- gsub(paste0(getwd(), "/_knit/"), "./", md_txt)
cat(md_txt, file=md_filename, sep="\n")



rmarkdown::render("./notes/notes_pobox.Rmd", 
                  output_dir = "./_knit")

md_filename <- "./_knit/notes_pobox.md"
md_txt <- readLines(md_filename)
md_txt <- gsub(paste0(getwd(), "/_knit/"), "./", md_txt)
cat(md_txt, file=md_filename, sep="\n")

