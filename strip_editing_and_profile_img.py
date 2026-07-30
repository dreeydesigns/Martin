import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# 1. Remove ConfigModal import
content = re.sub(r"import ConfigModal from '\./ConfigModal';\n", "", content)

# 2. Remove Edit Button
edit_btn_pattern = r"\s*\{\/\* Edit Button \*\/\}\s*<button\s*onClick=\{\(\) => setIsEditing\(true\)\}[\s\S]*?aria-label=\"Edit Profile\"\s*>\s*<Edit size=\{14\} />\s*</button>"
content = re.sub(edit_btn_pattern, "", content)

# 3. Remove ConfigModal rendering block
config_modal_pattern = r"\s*<AnimatePresence>\s*\{isEditing && \(\s*<ConfigModal[\s\S]*?/>\s*\)\}\s*</AnimatePresence>"
content = re.sub(config_modal_pattern, "", content)

# 4. Remove Profile Image from Hero Section
profile_image_pattern = r"\s*<motion\.div\s*initial=\{\{ scale: 0\.8, opacity: 0 \}\}[\s\S]*?<ImageWithPlaceholder src=\{config\.profileImage\}[\s\S]*?</motion\.div>"
content = re.sub(profile_image_pattern, "", content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
