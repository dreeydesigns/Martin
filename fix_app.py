import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Fix await fetchConfig()
fetch_repl = r"await fetchConfig\(\);\s+setIsLoading\(false\);"
fetch_new = r"fetchConfig().finally(() => setIsLoading(false));"
content = re.sub(fetch_repl, fetch_new, content)

# Remove function ConfigModal entirely
modal_pattern = r"function ConfigModal\(.*?\}\s*\}\s*(?=function ConfigInput)"
content = re.sub(modal_pattern, "", content, flags=re.DOTALL)

with open('src/App.tsx', 'w') as f:
    f.write(content)

with open('src/ConfigModal.tsx', 'r') as f:
    cm_content = f.read()

cm_content = cm_content.replace("import { Upload, Download, Cloud, X, Lock, FileImage, User, Activity, Settings, MessageSquare, Clock } from 'lucide-react';", 
"import { Upload, Download, Cloud, X, Lock, FileImage, User, Activity, Settings, MessageSquare, Clock, Eye } from 'lucide-react';")

with open('src/ConfigModal.tsx', 'w') as f:
    f.write(cm_content)
