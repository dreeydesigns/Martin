import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Remove isEditing
content = re.sub(r"\s*const \[isEditing, setIsEditing\] = useState\(false\);\n", "", content)

# Remove toast state
content = re.sub(r"\s*const \[toast, setToast\] = useState<\{message: string, type: 'success' \| 'error'\} \| null>\(null\);\n", "", content)

# Remove handleSaveConfig
content = re.sub(r"\s*const handleSaveConfig = async \(newConfig: typeof config\) => \{[\s\S]*?setTimeout\(\(\) => setToast\(null\), 3000\);\n\s*\};\n", "", content)

# Remove handleSyncCloud
content = re.sub(r"\s*const handleSyncCloud = async \(newConfig: typeof config\) => \{[\s\S]*?setTimeout\(\(\) => setToast\(null\), 3000\);\n\s*\}\n\s*\};\n", "", content)

# Remove toast render block
toast_render_pattern = r"\s*<AnimatePresence>\s*\{toast && \([\s\S]*?\}\s*</AnimatePresence>"
content = re.sub(toast_render_pattern, "", content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
