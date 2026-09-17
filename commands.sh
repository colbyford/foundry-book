## Render PDF
quarto render --to pdf

## Render HTML
quarto render --to html

## Render Asciidoc
quarto render --to asciidoc

# Then add :leveloffset: +1 to the beginning of the generated .adoc files to adjust heading levels.
# Also add [role="pagenumrestart"] to the beginning of Chapter 1 to reset page numbering for the PDF export.
# In 6_workflows.adoc, change [width="100%",cols="22%,78%",options="header",] to [options="header",]
# Change link:data/ch02/properties.json[`data/ch02/properties.json`] to [`data/ch02/properties.json`] (also link:data/ch04/finance_docs/[data/ch04/finance++_++docs])

# Then add this under each chapter header
# .A Note for Early Release Readers
# ****
# With Early Release ebooks, you get books in their earliest form—the author's raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

# This will be the 5th chapter of the final book. Please note that the GitHub repo will be made active later on.

# If you'd like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at @oreilly.com.
# ****
