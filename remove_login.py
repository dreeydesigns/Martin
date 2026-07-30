import re

with open('src/ConfigModal.tsx', 'r') as f:
    content = f.read()

# Remove the isAuthenticated block
auth_block = r"if \(!isAuthenticated\) \{.*?return \(\s*<>\s*<motion\.div"
content = re.sub(r"if \(!isAuthenticated\) \{.*?return \(\s*<>\s*<motion\.div", r"return (\n    <>\n      <motion.div", content, flags=re.DOTALL)

with open('src/ConfigModal.tsx', 'w') as f:
    f.write(content)
