import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# 1. State changes
content = re.sub(
    r"const \[analyticsData, setAnalyticsData\] = useState<{date: string, views: number}\[\]>\(\[\]\);",
    r"const [analyticsData, setAnalyticsData] = useState<{date: string, views: number}[]>([]);\n  const [socialClicks, setSocialClicks] = useState<Record<string, number>>({});\n  const [visitorLocations, setVisitorLocations] = useState<Record<string, number>>({});",
    content
)

# 2. Track View logic
track_view_new = """const trackView = async () => {
      // Basic local storage tracking + Firestore sync for analytics
      const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
      const localKey = `viewed_${today}`;
      
      try {
        const viewsRef = doc(db, 'configs', 'views');
        const viewsSnap = await getDoc(viewsRef);
        
        let viewsData: any = {};
        if (viewsSnap.exists()) {
          viewsData = viewsSnap.data();
        }
        
        if (!viewsData.locations) viewsData.locations = {};
        if (!viewsData.clicks) viewsData.clicks = { whatsapp: 0, facebook: 0, instagram: 0, call: 0, email: 0 };
        
        // If haven't viewed today in this session/browser, increment
        if (!sessionStorage.getItem(localKey)) {
          sessionStorage.setItem(localKey, 'true');
          viewsData[today] = (viewsData[today] || 0) + 1;
          viewsData.total = (viewsData.total || 0) + 1;
          
          try {
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            let locationRegion = timezone ? timezone.split('/')[1]?.replace('_', ' ') || timezone : 'Unknown';
            if (locationRegion) viewsData.locations[locationRegion] = (viewsData.locations[locationRegion] || 0) + 1;
          } catch(e) {}
          
          await setDoc(viewsRef, viewsData);
        }
        
        setPageViews(viewsData.total || 0);
        
        // Format for recharts
        const chartData = Object.keys(viewsData)
          .filter(k => k !== 'total' && k !== 'locations' && k !== 'clicks')
          .sort()
          .slice(-7) // Last 7 days
          .map(k => ({
            date: k.split('-').slice(1).join('/'), // MM/DD
            views: viewsData[k]
          }));
        
        setAnalyticsData(chartData);
        setVisitorLocations(viewsData.locations);
        setSocialClicks(viewsData.clicks);

      } catch (e) {
        console.error("Error tracking view", e);
      }
    };"""
content = re.sub(r"const trackView = async \(\) => \{.*?(?=  \}, \[\]\);)    \};\s*trackView\(\);", track_view_new + "\n    trackView();", content, flags=re.DOTALL)

# 3. Track Click logic
handle_track_click = """
  const handleTrackClick = async (platform: string) => {
    try {
      const viewsRef = doc(db, 'configs', 'views');
      const viewsSnap = await getDoc(viewsRef);
      if (viewsSnap.exists()) {
        const data = viewsSnap.data();
        const clicks = data.clicks || {};
        clicks[platform] = (clicks[platform] || 0) + 1;
        await updateDoc(viewsRef, { clicks });
        setSocialClicks(clicks);
      }
    } catch (e) {
      console.error("Error tracking click", e);
    }
  };
"""
content = re.sub(r"(const handleSaveConfig = async)", handle_track_click + r"\n  \1", content)


# 4. Default config override
content = re.sub(r"aboutP2: \"As the Sales.*?rewarding.\"", r'aboutP2: "As the Sales & Marketing Manager at Range Rover Centre Ltd, my approach is built on transparency, personalized service, and a deep passion for the heritage of the brand. Whether you are exploring our latest models or seeking a certified pre-owned vehicle, I am committed to making your ownership journey seamless and rewarding.",\n  statusOverride: "auto"', content)


# 5. Check status logic
check_status_new = """useEffect(() => {
    const checkStatus = () => {
      if (config.statusOverride === 'available') {
        setIsOnline(true);
        return;
      }
      if (config.statusOverride === 'away') {
        setIsOnline(false);
        return;
      }
      const now = new Date();
      const nairobiTime = new Date(now.toLocaleString("en-US", {timeZone: "Africa/Nairobi"}));
      const day = nairobiTime.getDay();
      const hour = nairobiTime.getHours();

      let online = false;
      if (day >= 1 && day <= 5) {
        if (hour >= 8 && hour < 17) online = true;
      } else if (day === 6) {
        if (hour >= 9 && hour < 13) online = true;
      }
      setIsOnline(online);
    };

    checkStatus();
    const interval = setInterval(checkStatus, 60000);
    return () => clearInterval(interval);
  }, [config.statusOverride]);"""
content = re.sub(r"useEffect\(\(\) => \{\n    const checkStatus = \(\) => \{.*?(?=  \}, \[\]\);)  \}, \[\]\);", check_status_new, content, flags=re.DOTALL)

# 6. Click tracking on buttons
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

# 7. Button and SocialLink definitions
btn_def = r"function ActionButton\(\{ href, icon, label, t, isDarkMode \}: \{ href: string, icon: ReactNode, label: string, t: any, isDarkMode: boolean \}\) \{"
btn_def_new = r"function ActionButton({ href, icon, label, t, isDarkMode, onClick }: { href: string, icon: ReactNode, label: string, t: any, isDarkMode: boolean, onClick?: () => void }) {"
content = re.sub(btn_def, btn_def_new, content)
content = re.sub(r"className=\{`flex flex-col items-center justify-center py-3 px-2", r"onClick={onClick}\n      className={`flex flex-col items-center justify-center py-3 px-2", content)

soc_def = r"function SocialLink\(\{ href, icon, t, isDarkMode \}: \{ href: string, icon: ReactNode, t: any, isDarkMode: boolean \}\) \{"
soc_def_new = r"function SocialLink({ href, icon, t, isDarkMode, onClick }: { href: string, icon: ReactNode, t: any, isDarkMode: boolean, onClick?: () => void }) {"
content = re.sub(soc_def, soc_def_new, content)
content = re.sub(r"className=\{`w-12 h-12 rounded-full border flex", r"onClick={onClick}\n      className={`w-12 h-12 rounded-full border flex", content)

# 8. Save Contact Pulse Animation
old_save_btn = r"""<motion\.button\s*variants=\{fadeInUp\}\s*whileHover=\{\{ scale: 1\.02 \}\}\s*whileTap=\{\{ scale: 0\.95 \}\}\s*onClick=\{handleSaveContact\}\s*className=\{`flex items-center justify-center gap-2 py-3 px-4 rounded-xl border transition-all duration-300 text-sm font-medium tracking-wide \$\{t\.btnBg\} \$\{t\.btnBorder\} \$\{isDarkMode \? 'text-zinc-300' : 'text-zinc-700'\} \$\{t\.btnHover\}`\}\s*>"""
new_save_btn = r"""<motion.div variants={fadeInUp} className="w-full">
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
content = re.sub(r"\{content\.saveContact\}\s*</motion\.button>", r"{content.saveContact}\n            </motion.button>\n            </motion.div>", content)

# 9. ConfigModal props
content = re.sub(
    r"<ConfigModal \n            currentConfig=\{config\} \n            analyticsData=\{analyticsData\}\n            onSave=\{handleSaveConfig\} \n            onSync=\{handleSyncCloud\}\n            onClose=\{\(\) => setIsEditing\(false\)\} \n            isDarkMode=\{isDarkMode\} \n          />",
    r"<ConfigModal \n            currentConfig={config} \n            analyticsData={analyticsData}\n            socialClicks={socialClicks}\n            visitorLocations={visitorLocations}\n            onSave={handleSaveConfig} \n            onSync={handleSyncCloud}\n            onClose={() => setIsEditing(false)} \n            isDarkMode={isDarkMode} \n          />",
    content
)

content = re.sub(
    r"function ConfigModal\(\{ currentConfig, analyticsData, onSave, onSync, onClose, isDarkMode \}: any\) \{",
    r"function ConfigModal({ currentConfig, analyticsData, socialClicks, visitorLocations, onSave, onSync, onClose, isDarkMode }: any) {",
    content
)

# 10. ConfigModal statusOverride and input Image replacing
profile_content = r"""<div className="mb-4">
                  <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>Status Mode</label>
                  <select 
                    name="statusOverride"
                    value={formData.statusOverride}
                    onChange={(e) => setFormData({...formData, statusOverride: e.target.value})}
                    className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                  >
                    <option value="auto">Auto (Based on business hours)</option>
                    <option value="available">Always Available</option>
                    <option value="away">Always Away</option>
                  </select>
                </div>
                
                <ConfigInput label="Name\""""
content = re.sub(r'<ConfigInput label="Name"', profile_content, content, count=1)


image_fix = r"""
                <div className="mb-4 border-t border-inherit pt-4">
                  <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Profile Image</label>
                  <div className="flex items-center gap-4 mb-2">
                    {formData.profileImage ? (
                      <img src={formData.profileImage} alt="Profile preview" className="w-16 h-16 rounded-full object-cover border-2 border-inherit" />
                    ) : (
                      <div className={`w-16 h-16 rounded-full border-2 border-dashed flex items-center justify-center ${t.inputBorder} ${t.textSecondary}`}>No Img</div>
                    )}
                    <label className={`flex flex-1 items-center justify-center gap-2 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${t.inputBorder} ${t.inputBg} hover:opacity-80`}>
                      <Upload size={16} className={t.textSecondary} />
                      <span className={`text-sm font-medium ${t.textPrimary}`}>Upload Profile Image</span>
                      <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e, 'profileImage')} />
                    </label>
                  </div>
                </div>

                <div className="mb-4 border-t border-inherit pt-4">
                  <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Background Image</label>
                  <div className="flex flex-col gap-3 mb-2">
                    {formData.bgImage ? (
                      <img src={formData.bgImage} alt="Background preview" className="w-full h-24 rounded-lg object-cover border border-inherit" />
                    ) : (
                      <div className={`w-full h-24 rounded-lg border-2 border-dashed flex items-center justify-center ${t.inputBorder} ${t.textSecondary}`}>No Img</div>
                    )}
                    <label className={`flex w-full items-center justify-center gap-2 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${t.inputBorder} ${t.inputBg} hover:opacity-80`}>
                      <Upload size={16} className={t.textSecondary} />
                      <span className={`text-sm font-medium ${t.textPrimary}`}>Upload Background Image</span>
                      <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e, 'bgImage')} />
                    </label>
                  </div>
                </div>
"""

old_image_section = r'<div className="mb-4 border-t border-inherit pt-4">\s*<label className=\{`block text-xs font-medium mb-2 \$\{t\.textPrimary\} opacity-80`\}>Profile Image</label>.*?(?=<div className="mb-4 border-t border-inherit pt-4">\s*<label className=\{`block text-xs font-medium mb-1 \$\{t\.textPrimary\} opacity-80`\}>WhatsApp)'
content = re.sub(old_image_section, image_fix, content, flags=re.DOTALL)


# 11. ConfigModal analytics update
analytics_content = r"""<div className="py-2 space-y-8">
                <div>
                  <h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Daily Profile Views (Last 7 Days)</h3>
                  <div className="w-full h-48">
                    {analyticsData && analyticsData.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={analyticsData}>
                          <XAxis 
                            dataKey="date" 
                            stroke={isDarkMode ? '#52525b' : '#a1a1aa'} 
                            fontSize={12} 
                            tickLine={false} 
                          />
                          <Tooltip 
                            cursor={{ fill: isDarkMode ? '#27272a' : '#f4f4f5' }}
                            contentStyle={{ 
                              backgroundColor: isDarkMode ? '#18181b' : '#ffffff',
                              border: 'none',
                              borderRadius: '8px',
                              color: isDarkMode ? '#ffffff' : '#000000',
                              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
                            }}
                          />
                          <Bar 
                            dataKey="views" 
                            fill={formData.primaryColor || '#c5a059'} 
                            radius={[4, 4, 0, 0]} 
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className={`w-full h-full flex items-center justify-center text-sm ${t.textSecondary}`}>
                        No analytics data available yet.
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Social Link Clicks</h3>
                  <div className="space-y-3">
                    {Object.entries(socialClicks || {}).length > 0 ? (
                      Object.entries(socialClicks).sort((a, b) => (b[1] as number) - (a[1] as number)).map(([platform, count]) => (
                        <div key={platform} className={`flex items-center justify-between p-3 rounded-lg border ${t.inputBorder} ${t.inputBg}`}>
                          <span className={`text-sm capitalize font-medium ${t.textPrimary}`}>{platform}</span>
                          <span className={`text-sm font-mono font-bold ${t.textPrimary}`}>{count as number}</span>
                        </div>
                      ))
                    ) : (
                      <div className={`text-sm ${t.textSecondary}`}>No social clicks yet.</div>
                    )}
                  </div>
                </div>

                <div>
                  <h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Visitor Locations (Estimated)</h3>
                  <div className="space-y-3">
                    {Object.entries(visitorLocations || {}).length > 0 ? (
                      Object.entries(visitorLocations).sort((a, b) => (b[1] as number) - (a[1] as number)).map(([location, count]) => (
                        <div key={location} className={`flex items-center justify-between p-3 rounded-lg border ${t.inputBorder} ${t.inputBg}`}>
                          <span className={`text-sm font-medium ${t.textPrimary}`}>{location}</span>
                          <span className={`text-sm font-mono font-bold ${t.textPrimary}`}>{count as number}</span>
                        </div>
                      ))
                    ) : (
                      <div className={`text-sm ${t.textSecondary}`}>No location data yet.</div>
                    )}
                  </div>
                </div>
              </div>"""

old_analytics = r'<div className="py-2">\s*<h3 className=\{`text-sm font-medium mb-4 \$\{t\.textPrimary\}`\}>Daily Profile Views \(Last 7 Days\)</h3>.*?(?=\s*</>\s*\)\}\s*</div>\s*<div className="p-4 border-t border-inherit bg-inherit flex justify-end gap-3 z-10">)'
content = re.sub(old_analytics, analytics_content, content, flags=re.DOTALL)


# 12. ConfigModal Import / Export buttons and handlers
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
        } catch (err) {
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
                <Upload size={20} />
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
