import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# Update ConfigModal prop usage in App
content = re.sub(
    r"<ConfigModal \n            currentConfig=\{config\} \n            analyticsData=\{analyticsData\}\n            onSave=\{handleSaveConfig\} \n            onSync=\{handleSyncCloud\}\n            onClose=\{\(\) => setIsEditing\(false\)\} \n            isDarkMode=\{isDarkMode\} \n          />",
    r"<ConfigModal \n            currentConfig={config} \n            analyticsData={analyticsData}\n            socialClicks={socialClicks}\n            visitorLocations={visitorLocations}\n            onSave={handleSaveConfig} \n            onSync={handleSyncCloud}\n            onClose={() => setIsEditing(false)} \n            isDarkMode={isDarkMode} \n          />",
    content
)

# Update ConfigModal definition
content = re.sub(
    r"function ConfigModal\(\{ currentConfig, analyticsData, onSave, onSync, onClose, isDarkMode \}: any\) \{",
    r"function ConfigModal({ currentConfig, analyticsData, socialClicks, visitorLocations, onSave, onSync, onClose, isDarkMode }: any) {",
    content
)

with open("src/App.tsx", "w") as f:
    f.write(content)
