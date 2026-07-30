import re

with open('src/ConfigModal.tsx', 'r') as f:
    content = f.read()

# Remove handleLogin function
content = re.sub(r"const handleLogin = async \(e: React.FormEvent\) => \{.*?\};\n\n", "", content, flags=re.DOTALL)

with open('src/ConfigModal.tsx', 'w') as f:
    f.write(content)
