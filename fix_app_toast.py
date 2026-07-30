import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

state_old = "const [sendResult, setSendResult] = useState<'success' | 'error' | null>(null);"
state_new = """const [sendResult, setSendResult] = useState<'success' | 'error' | null>(null);
  const [toast, setToast] = useState<{message: string, type: 'success' | 'error'} | null>(null);"""
content = content.replace(state_old, state_new)

handleSave_old = """const handleSaveConfig = async (newConfig: typeof config) => {
    setConfig(newConfig);
    localStorage.setItem('business_card_config', JSON.stringify(newConfig));
    setIsEditing(false);
  };"""
handleSave_new = """const handleSaveConfig = async (newConfig: typeof config) => {
    setConfig(newConfig);
    localStorage.setItem('business_card_config', JSON.stringify(newConfig));
    setIsEditing(false);
    setToast({ message: 'Configuration saved locally!', type: 'success' });
    setTimeout(() => setToast(null), 3000);
  };"""
content = content.replace(handleSave_old, handleSave_new)

sync_old = """const handleSyncCloud = async (newConfig: typeof config) => {
    try {
      await setDoc(doc(db, 'configs', 'main'), newConfig);
      alert('Configuration successfully synced to cloud!');
    } catch (e) {
      console.error("Sync error", e);
      alert('Failed to sync. Please try again.');
    }
  };"""
sync_new = """const handleSyncCloud = async (newConfig: typeof config) => {
    try {
      await setDoc(doc(db, 'configs', 'main'), newConfig);
      setToast({ message: 'Configuration successfully synced to cloud!', type: 'success' });
      setTimeout(() => setToast(null), 3000);
    } catch (e) {
      console.error("Sync error", e);
      setToast({ message: 'Failed to sync. Please try again.', type: 'error' });
      setTimeout(() => setToast(null), 3000);
    }
  };"""
content = content.replace(sync_old, sync_new)

# Insert the toast component just before the end of the main return
toast_comp = """
      <AnimatePresence>
        {toast && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            className={`fixed bottom-4 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-xl shadow-2xl flex items-center gap-3 ${
              toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'
            }`}
          >
            <span className="text-sm font-medium">{toast.message}</span>
            <button onClick={() => setToast(null)} className="p-1 hover:bg-white/20 rounded-full transition-colors">
              <X size={16} />
            </button>
          </motion.div>
        )}
      </AnimatePresence>
"""
content = content.replace("</AnimatePresence>\n\n      <main", "</AnimatePresence>\n" + toast_comp + "\n      <main")

with open('src/App.tsx', 'w') as f:
    f.write(content)
