import re

with open("src/App.tsx", "r") as f:
    content = f.read()

funcs = r"""
  const handleExport = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(formData, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "business-card-config.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const importedConfig = JSON.parse(event.target?.result as string);
          setFormData({ ...formData, ...importedConfig });
        } catch (e) {
          alert("Invalid configuration file.");
        }
      };
      reader.readAsText(file);
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>, target: 'profileImage' | 'bgImage') => {
"""

content = re.sub(r"  const handleImageUpload = \(e: React.ChangeEvent<HTMLInputElement>, target: 'profileImage' \| 'bgImage'\) => \{", funcs, content)

buttons_html = r"""
            <div className="flex items-center gap-2">
              <label className="p-2 rounded-full hover:bg-zinc-500/20 text-emerald-500 transition-colors cursor-pointer" title="Import Config">
                <Download size={20} className="rotate-180" />
                <input type="file" accept=".json" className="hidden" onChange={handleImport} />
              </label>
              <button 
                onClick={handleExport}
                title="Export Config"
                className="p-2 rounded-full hover:bg-zinc-500/20 text-blue-500 transition-colors"
              >
                <Download size={20} />
              </button>
              <button 
                onClick={() => onSync(formData)}
                title="Sync to Cloud"
                className="p-2 rounded-full hover:bg-zinc-500/20 text-[#c5a059] transition-colors"
              >
                <Cloud size={20} />
              </button>
"""

content = re.sub(
    r'<div className="flex items-center gap-2">\s*<button \s*onClick=\{\(\) => onSync\(formData\)\}\s*title="Sync to Cloud"\s*className="p-2 rounded-full hover:bg-zinc-500/20 text-\[\#c5a059\] transition-colors"\s*>\s*<Cloud size=\{20\} />\s*</button>',
    buttons_html,
    content
)

with open("src/App.tsx", "w") as f:
    f.write(content)
