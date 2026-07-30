import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# The block to move
loading_block_pattern = r"(\s*if \(isLoading\) \{.*?\}\n)"

match = re.search(loading_block_pattern, content, re.DOTALL)
if match:
    loading_block = match.group(1)
    # Remove from its current location
    content = content.replace(loading_block, "")
    
    # Place it before the return statement
    return_pattern = r"(\s*return \(\n\s*<div)"
    content = re.sub(return_pattern, loading_block + r"\1", content, count=1)

with open('src/App.tsx', 'w') as f:
    f.write(content)

