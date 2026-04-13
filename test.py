from pathlib import Path

filename = "file.txt.html.cpp.py"
path = Path(filename)

print(f"Filename: {path.stem}")
print(f"Extension: {path.suffix}")
print(f"All extensions: {path.suffixes}")