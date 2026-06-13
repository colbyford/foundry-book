import re
import glob

## Get list of .adoc files in the current directory
adoc_files = glob.glob("../_book/book-asciidoc/*.adoc")

def fix_headers(file_path):
    print(f"Processing file: {file_path}")

    ## Open the file and read its contents
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    ## Add `[role="pagenumrestart"]` at the beginning of chapter 1
    if content.startswith("[[sec-chapter-1]]"):
        content = content.replace("[[sec-chapter-1]]", '[role="pagenumrestart"]\n\n[[sec-chapter-1]]')

    ## Add `:leveloffset: +1` to all files
    content = ":leveloffset: +1\n\n" + content

    ## Open the file in write mode to save changes
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Finished processing: {file_path}")


for adoc_file in adoc_files:
    fix_headers(adoc_file)