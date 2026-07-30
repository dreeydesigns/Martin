with open('src/App.tsx', 'r') as f:
    content = f.read()

# 1. Add formPhone and formError states
state_old = "const [formMessage, setFormMessage] = useState('');"
state_new = """const [formMessage, setFormMessage] = useState('');
  const [formPhone, setFormPhone] = useState('');
  const [formError, setFormError] = useState('');"""
content = content.replace(state_old, state_new)

# 2. Update handleSendMessage
import re
send_old = r"const handleSendMessage = async \(e: React\.FormEvent\) => \{\s*e\.preventDefault\(\);\s*setIsSending\(true\);\s*setSendResult\(null\);"
send_new = """const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');
    
    if (formMessage.trim().length === 0) {
      setFormError('Message cannot be empty.');
      return;
    }
    
    const phoneRegex = /^\\+?[0-9\\s\\-\\(\\)]{7,15}$/;
    if (!phoneRegex.test(formPhone)) {
      setFormError('Please enter a valid phone number.');
      return;
    }

    setIsSending(true);
    setSendResult(null);"""
content = re.sub(send_old, lambda _: send_new, content)

# 3. Update the form inside return()
form_old = """<div>\n              <input \n                type="text" \n                value={formName}"""
form_new = """{formError && <p className="text-red-500 text-xs text-center font-medium mb-2">{formError}</p>}
            <div>
              <input 
                type="text" 
                value={formName}"""
content = content.replace('<div>\n              <input \n                type="text" \n                value={formName}', form_new)

# Also add the Phone input
input_old = """className={`w-full px-4 py-3 rounded-xl border text-sm transition-colors duration-300 ${t.inputBg} ${t.inputBorder} ${t.textPrimary} placeholder:text-zinc-500`}\n              />\n            </div>\n            <div>\n              <textarea"""
input_new = """className={`w-full px-4 py-3 rounded-xl border text-sm transition-colors duration-300 ${t.inputBg} ${t.inputBorder} ${t.textPrimary} placeholder:text-zinc-500`}
              />
            </div>
            <div>
              <input 
                type="tel" 
                value={formPhone}
                onChange={(e) => setFormPhone(e.target.value)}
                required
                placeholder="Your Phone Number"
                className={`w-full px-4 py-3 rounded-xl border text-sm transition-colors duration-300 ${t.inputBg} ${t.inputBorder} ${t.textPrimary} placeholder:text-zinc-500`}
              />
            </div>
            <div>
              <textarea"""
content = content.replace(input_old, input_new)

# 4. Include phone in the whatsapp template? The user's template is {name}, {message}. Maybe add it to the message text.
# Let's just append it to the text.
replace_text_old = "let text = config.whatsappTemplate.replace('{name}', formName).replace('{message}', formMessage);"
replace_text_new = "let text = config.whatsappTemplate.replace('{name}', formName).replace('{message}', formMessage) + `\\n\\nPhone: ${formPhone}`;"
content = content.replace(replace_text_old, replace_text_new)

# Clear formPhone on success
clear_old = "setFormName('');\n      setFormMessage('');"
clear_new = "setFormName('');\n      setFormMessage('');\n      setFormPhone('');"
content = content.replace(clear_old, clear_new)

# 5. Image placeholders. We can create an ImageWithPlaceholder component and use it.
img_comp = """
function ImageWithPlaceholder({ src, alt, className }: { src: string, alt: string, className: string }) {
  const [loaded, setLoaded] = useState(false);
  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Skeleton */}
      <motion.div 
        animate={{ opacity: loaded ? 0 : 1 }} 
        transition={{ duration: 0.5 }}
        className="absolute inset-0 bg-zinc-200 dark:bg-zinc-800 animate-pulse" 
      />
      
      {/* Actual Image */}
      <img 
        src={src} 
        alt={alt}
        className={`w-full h-full object-cover transition-opacity duration-700 ${loaded ? 'opacity-100' : 'opacity-0'}`}
        onLoad={() => setLoaded(true)}
      />
    </div>
  );
}
"""
content = content.replace("// Subcomponents", "// Subcomponents\n" + img_comp)

# Replace <img src={config.profileImage} with ImageWithPlaceholder
# Wait, let's find the profile image img tag
profile_img_old = """<img \n                  src={config.profileImage} \n                  alt={config.name} \n                  className="w-full h-full object-cover object-top"\n                />"""
profile_img_new = """<ImageWithPlaceholder src={config.profileImage} alt={config.name} className="w-full h-full" />"""
content = content.replace(profile_img_old, profile_img_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
