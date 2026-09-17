import re
import glob

## Get list of .adoc files in the current directory
adoc_files = glob.glob("../_book/book-asciidoc/*.adoc")

def fix_pluses(file_path):
    print(f"Processing file: {file_path}")

    ## Open the file and read its contents
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    ## Replace the specified text
    # pattern = r"\+\+([<>{}\[\]_|+])\+\+"
    # updated_content = re.sub(pattern, r'\1', content)

    # updated_content = updated_content.replace("++*_++", r"*\_").replace("++_{++", r"\_{")

    updated_content = content.replace("++", "")

    ## Open the file in write mode to save changes
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print(f"Finished processing: {file_path}")


for adoc_file in adoc_files:
    fix_pluses(adoc_file)