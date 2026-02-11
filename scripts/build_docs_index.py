from pathlib import Path
import urllib.parse

DOCS = Path("docs")

EXCLUDE = {
    ".keep",
    "index.html",
    "boc_terminal_dir_index.txt",
    "index.json",
}

def q(s: str) -> str:
    # Encode each path segment so spaces work
    return "/".join(urllib.parse.quote(p) for p in s.split("/"))

def write_index(folder: Path, title: str, entries_html: str):
    out = folder / "index.html"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="{('../' if folder != DOCS else '')}../style.css">
  <style>
    body {{
      background-color: #f6f6f0;
      font-family: 'Courier New', Courier, monospace;
      padding: 2em;
      color: #111;
    }}
    h1 {{ font-size: 1.5em; margin-bottom: 0.5em; }}
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
    .archive-entry a:hover {{ text-decoration: underline; }}
    .back {{ margin: 1.5em 0; display: inline-block; }}
    footer {{ font-size: 0.8em; margin-top: 4em; color: #777; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <a class="back" href="{ '/' if folder == DOCS else '../' }">← Back</a>

  {entries_html}

  <footer>
    Bureau of Ontological Consistency /docs/ archive – Station 7 Node Mirror
  </footer>
</body>
</html>
"""
    out.write_text(html, encoding="utf-8")

# -------- Build top-level index (folders + direct files) --------

folders = [p for p in DOCS.iterdir() if p.is_dir() and not p.name.startswith(".")]
folders.sort(key=lambda p: p.name.lower())

direct_files = [
    p for p in DOCS.iterdir()
    if p.is_file() and not p.name.startswith(".") and p.name not in EXCLUDE
]
direct_files.sort(key=lambda p: p.name.lower())

folder_rows = "\n".join(
    f'<div class="archive-entry"><a href="./{q(p.name)}/">{p.name}/</a></div>'
    for p in folders
) or "<div class='archive-entry'>(none)</div>"

file_rows = "\n".join(
    f'<div class="archive-entry"><a href="./{q(p.name)}">{p.name}</a></div>'
    for p in direct_files
) or "<div class='archive-entry'>(none)</div>"

top_entries = f"""
  <p>Auto-generated index. Folders listed first.</p>

  <h2>Report Folders</h2>
  {folder_rows}

  <h2>Direct Documents</h2>
  {file_rows}
"""

write_index(DOCS, "BOC Field Archive Access – /docs", top_entries)

# -------- Build an index inside each top-level folder --------

for folder in folders:
    # List files directly inside this folder (and optionally recurse if you want)
    entries = []
    for p in folder.iterdir():
        if p.name.startswith(".") or p.name in EXCLUDE:
            continue
        if p.is_file():
            entries.append(p)
        elif p.is_dir():
            # Link subfolders too (will 404 unless you also generate deeper indexes)
            # Keep it simple: show subfolders as links, but you can recurse later.
            entries.append(p)

    # Sort: folders first, then files
    entries.sort(key=lambda p: (0 if p.is_dir() else 1, p.name.lower()))

    rows = []
    for p in entries:
        if p.is_dir():
            rows.append(f'<div class="archive-entry"><a href="./{q(p.name)}/">{p.name}/</a></div>')
        else:
            rows.append(f'<div class="archive-entry"><a href="./{q(p.name)}">{p.name}</a></div>')

    entries_html = "\n".join(rows) or "<div class='archive-entry'>(empty)</div>"

    write_index(folder, f"BOC Archive – {folder.name}", entries_html)
