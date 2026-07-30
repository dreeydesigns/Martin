import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Match from `function ConfigModal` up to `function ConfigInput`
modal_pattern = r"function ConfigModal\(.*?\}\s*\}\s*(?=function ConfigInput)"
content = re.sub(modal_pattern, "", content, flags=re.DOTALL)

# Add import at the top
import_statement = "import ConfigModal from './ConfigModal';\n"
content = content.replace("import CropModal from './CropModal';", "import CropModal from './CropModal';\n" + import_statement)

with open('src/App.tsx', 'w') as f:
    f.write(content)
