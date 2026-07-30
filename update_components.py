import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# Update ActionButton definition
btn_def = r"function ActionButton\(\{ href, icon, label, t, isDarkMode \}: \{ href: string, icon: ReactNode, label: string, t: any, isDarkMode: boolean \}\) \{"
btn_def_new = r"function ActionButton({ href, icon, label, t, isDarkMode, onClick }: { href: string, icon: ReactNode, label: string, t: any, isDarkMode: boolean, onClick?: () => void }) {"
content = re.sub(btn_def, btn_def_new, content)
content = re.sub(r"className={`flex flex-col items-center justify-center py-3 px-2", r"onClick={onClick}\n      className={`flex flex-col items-center justify-center py-3 px-2", content)

# Update SocialLink definition
soc_def = r"function SocialLink\(\{ href, icon, t, isDarkMode \}: \{ href: string, icon: ReactNode, t: any, isDarkMode: boolean \}\) \{"
soc_def_new = r"function SocialLink({ href, icon, t, isDarkMode, onClick }: { href: string, icon: ReactNode, t: any, isDarkMode: boolean, onClick?: () => void }) {"
content = re.sub(soc_def, soc_def_new, content)
content = re.sub(r"className={`w-12 h-12 rounded-full border flex", r"onClick={onClick}\n      className={`w-12 h-12 rounded-full border flex", content)

# Usage in App:
content = re.sub(r"<ActionButton \n                href=\{`tel:\$\{config\.phone\}`\} \n                icon=\{<Phone size=\{20\} />\} \n                label=\{content\.call\}\n                t=\{t\}\n                isDarkMode=\{isDarkMode\}\n              />",
r"<ActionButton \n                href={`tel:${config.phone}`} \n                icon={<Phone size={20} />} \n                label={content.call}\n                t={t}\n                isDarkMode={isDarkMode}\n                onClick={() => handleTrackClick('call')}\n              />", content)

content = re.sub(r"<ActionButton \n                href=\{`https://wa\.me/\$\{config\.whatsapp\.replace\('\+', ''\)\}`\} \n                icon=\{<MessageCircle size=\{20\} />\} \n                label=\{content\.whatsapp\}\n                t=\{t\}\n                isDarkMode=\{isDarkMode\}\n              />",
r"<ActionButton \n                href={`https://wa.me/${config.whatsapp.replace('+', '')}`} \n                icon={<MessageCircle size={20} />} \n                label={content.whatsapp}\n                t={t}\n                isDarkMode={isDarkMode}\n                onClick={() => handleTrackClick('whatsapp')}\n              />", content)

content = re.sub(r"<ActionButton \n                href=\{`mailto:\$\{config\.email\}`\} \n                icon=\{<Mail size=\{20\} />\} \n                label=\{content\.email\}\n                t=\{t\}\n                isDarkMode=\{isDarkMode\}\n              />",
r"<ActionButton \n                href={`mailto:${config.email}`} \n                icon={<Mail size={20} />} \n                label={content.email}\n                t={t}\n                isDarkMode={isDarkMode}\n                onClick={() => handleTrackClick('email')}\n              />", content)

content = re.sub(r"<SocialLink href=\{config\.facebook\} icon=\{<Facebook size=\{22\} />\} t=\{t\} isDarkMode=\{isDarkMode\} />",
r"<SocialLink href={config.facebook} icon={<Facebook size={22} />} t={t} isDarkMode={isDarkMode} onClick={() => handleTrackClick('facebook')} />", content)

content = re.sub(r"<SocialLink href=\{config\.instagram\} icon=\{<Instagram size=\{22\} />\} t=\{t\} isDarkMode=\{isDarkMode\} />",
r"<SocialLink href={config.instagram} icon={<Instagram size={22} />} t={t} isDarkMode={isDarkMode} onClick={() => handleTrackClick('instagram')} />", content)

# Pulse Animation on Save Contact Button
old_save_btn = r"""<motion\.button
              variants=\{fadeInUp\}
              whileHover=\{\{ scale: 1\.02 \}\}
              whileTap=\{\{ scale: 0\.95 \}\}
              onClick=\{handleSaveContact\}
              className=\{`flex items-center justify-center gap-2 py-3 px-4 rounded-xl border transition-all duration-300 text-sm font-medium tracking-wide \$\{t\.btnBg\} \$\{t\.btnBorder\} \$\{isDarkMode \? 'text-zinc-300' : 'text-zinc-700'\} \$\{t\.btnHover\}`\}
            >"""
new_save_btn = r"""<motion.div variants={fadeInUp}>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.95 }}
              animate={{ 
                boxShadow: ["0 0 0 0 rgba(197,160,89,0)", `0 0 0 8px ${config.primaryColor}30`, "0 0 0 0 rgba(197,160,89,0)"]
              }}
              transition={{ repeat: Infinity, duration: 2 }}
              onClick={handleSaveContact}
              className={`w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl border transition-all duration-300 text-sm font-medium tracking-wide ${t.btnBg} ${t.btnBorder} ${isDarkMode ? 'text-zinc-300' : 'text-zinc-700'} ${t.btnHover}`}
            >"""
content = re.sub(old_save_btn, new_save_btn, content)
content = re.sub(r"\{content\.saveContact\}\n            </motion\.button>", r"{content.saveContact}\n            </motion.button>\n            </motion.div>", content)

with open("src/App.tsx", "w") as f:
    f.write(content)
