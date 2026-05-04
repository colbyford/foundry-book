## Render PDF
quarto render --to pdf

## Render HTML
quarto render --to html

## Render Asciidoc
quarto render --to asciidoc

# Then add :leveloffset: +1 to the beginning of the generated .adoc file to adjust heading levels.
# Also add [role="pagenumrestart"] to the beginning of Chapter 1 to reset page numbering for the PDF export.