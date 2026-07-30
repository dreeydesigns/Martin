import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add states for contact form
state_contact = r"const \[formMessage, setFormMessage\] = useState\(''\);"
state_contact_new = r"""const [formMessage, setFormMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [sendResult, setSendResult] = useState<'success' | 'error' | null>(null);"""
content = re.sub(state_contact, state_contact_new, content)

# Modify handleSendMessage
handle_send_repl = r"const handleSendMessage = \(e: React.FormEvent\) => \{\s+e.preventDefault\(\);\s+let text = config.whatsappTemplate.replace\('\{name\}', formName\).replace\('\{message\}', formMessage\);\s+const waUrl = `https://wa.me/\$\{config.whatsapp.replace\('\+', ''\)\}\?text=\$\{encodeURIComponent\(text\)\}`;\s+window.open\(waUrl, '_blank'\);\s+\};"
handle_send_new = r"""const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSending(true);
    setSendResult(null);
    try {
      // Simulate brief processing for UX
      await new Promise(res => setTimeout(res, 800));
      let text = config.whatsappTemplate.replace('{name}', formName).replace('{message}', formMessage);
      const waUrl = `https://wa.me/${config.whatsapp.replace('+', '')}?text=${encodeURIComponent(text)}`;
      window.open(waUrl, '_blank');
      setSendResult('success');
      setFormName('');
      setFormMessage('');
      setTimeout(() => setSendResult(null), 3000);
    } catch (err) {
      setSendResult('error');
      setTimeout(() => setSendResult(null), 3000);
    } finally {
      setIsSending(false);
    }
  };"""
content = re.sub(handle_send_repl, handle_send_new, content)

# Modify the form submit button
submit_btn_repl = r"<Send size=\{16\} />\s+\{content.contactSend\}\s+</motion.button>"
submit_btn_new = r"""{isSending ? (
                <span className="flex items-center gap-2">
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }} className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full" />
                  Sending...
                </span>
              ) : (
                <span className="flex items-center gap-2"><Send size={16} />{content.contactSend}</span>
              )}
            </motion.button>
            {sendResult === 'success' && (
              <p className="text-emerald-500 text-xs text-center font-medium mt-2">Message opened in WhatsApp!</p>
            )}
            {sendResult === 'error' && (
              <p className="text-red-500 text-xs text-center font-medium mt-2">Failed to process request.</p>
            )}"""
content = re.sub(submit_btn_repl, submit_btn_new, content)

# Modify early return to show loading skeleton
skeleton_code = r"""
  if (isLoading) {
    return (
      <div className={`min-h-screen ${isDarkMode ? 'bg-zinc-950' : 'bg-stone-50'} flex flex-col items-center justify-center p-4`}>
        <motion.div animate={{ opacity: [0.5, 1, 0.5] }} transition={{ repeat: Infinity, duration: 1.5 }} className="w-full max-w-xl space-y-6">
          <div className="h-64 w-full bg-zinc-800/20 rounded-3xl" />
          <div className="flex flex-col items-center -mt-16">
            <div className="w-32 h-32 rounded-full border-4 border-white bg-zinc-800/20" />
            <div className="h-6 w-48 bg-zinc-800/20 rounded-md mt-4" />
            <div className="h-4 w-32 bg-zinc-800/20 rounded-md mt-2" />
          </div>
          <div className="h-24 w-full bg-zinc-800/20 rounded-2xl" />
        </motion.div>
      </div>
    );
  }
"""
content = content.replace("const content = contentData[lang];", "const content = contentData[lang];\n" + skeleton_code)

with open('src/App.tsx', 'w') as f:
    f.write(content)
