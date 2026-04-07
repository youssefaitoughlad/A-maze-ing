
# Before strip
line = "   hello world   \n"
print(repr(line))  # '   hello world   \n'

# After strip
line = line.strip()
print(repr(line))  # 'hello world'

lines = [
    "sk;k;;lackldkldskds",
    "lkjdjlkdslj\n",
    "     ls;l';lsl\n;ds;'l;l    ",
]

cleaned = []

for line in lines:
    line = line.strip()  # Removes leading/trailing spaces, tabs, newlines
    
    if not line or line.startswith("#"):
        continue
    
    cleaned.append(line)

print(cleaned)
