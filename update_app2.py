import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Update ConfigModal call
config_modal_repl = r"analyticsData=\{analyticsData\}"
config_modal_new = r"analyticsData={analyticsData}\n            rawViewsData={rawViewsData}"
content = re.sub(config_modal_repl, config_modal_new, content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
