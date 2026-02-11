from pathlib import Path
import urllib.parse

DOCS = Path("docs")
OUT = DOCS / "index.html"

EXCLUDE = {
    ".keep",
    "index.html",
    "boc_terminal_dir_index.txt",
}

folders = set()
files = []

for path in DOCS.rglob("*"):
    if path.name in EXCLUDE:
        continue

    if path.is_dir():
        # Collect top-level folders only
        rel = path.relative_to(DOCS)
        if len(rel.parts) == 1:
            folders.add(rel.as_posix())
    elif path.is_file():
        rel = path.relative_to(DOCS).as_posix()
        # Skip files inside excluded folders automatically
        files.append(rel)

folders = sorted(folders)
files = sorted(files)

def link(rel):
    return urllib.parse.quote(rel)

folder_rows = "\n".join(
    f'<div class="archive-entry"><a href="./{link(folder)}/">{folder}/</a></div>'
    for folder in folders
)

file_rows = "\n".join(
    f'<div class="archive-entry"><a href="./{link(file)}">{file}</a></div>'
    for file in files
    if "/" not in file  # only loose files in /docs root
)

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>BOC Field Archive – /docs</title>
<link rel="stylesheet" href="../style.css">
<style>
body {{
  background-color: #f6f6f0;
  font-family: 'Courier New', Courier, monospace;
  padding: 2em;
  color: #111;
}}
h1 {{
  font-size: 1.5em;
  margin-bottom: 0.5em;
}}
h2 {{
  margin-top: 2em;
  font-size: 1.2em;
}}
.archive-entry {{
  margin: 0.8em 0;
  padding-bottom: 0.4em;
  border-bottom: 1px dotted #aaa;
  word-break: break-word;
}}
.archive-entry a {{
  color: #003366;
  text-decoration: none;
  font-weight: bold;
}}
.archive-entry a:hover {{
  text-decoration: underline;
}}
footer {{
  font-size: 0.8em;
  margin-top: 4em;
  color: #777;
}}
</style>
</head>
<body>
<h1>BOC Field Archive Access – /docs</h1>
<p>Auto-generated index. Folders listed first.</p>

<h2>Report Folders</h2>
{folder_rows}

<h2>Direct Documents</h2>
{file_rows}

<footer>
Bureau of Ontological Consistency /docs/ archive – Station 7 Node Mirror<br>
Catalog compiled from repository contents [AutoIndex]
</footer>

</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print("Docs index generated.")
