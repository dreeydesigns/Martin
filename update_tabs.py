import re

with open("src/App.tsx", "r") as f:
    content = f.read()

analytics_content = r"""<div className="py-2 space-y-8">
                <div>
                  <h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Daily Profile Views (Last 7 Days)</h3>
                  <div className="w-full h-48">
                    {analyticsData.length > 0 ? (
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

content = re.sub(
    r'<div className="py-2">\s*<h3 className=\{`text-sm font-medium mb-4 \$\{t\.textPrimary\}`\}>Daily Profile Views.*?No analytics data available yet\.\s*</div>\s*\)\}\s*</div>\s*</div>',
    analytics_content,
    content,
    flags=re.DOTALL
)

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


# Fix Image inputs: Hide URL input, use file input as primary, keep functionality
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

content = re.sub(
    r'<div className="mb-4 border-t border-inherit pt-4">\s*<label className=\{`block text-xs font-medium mb-2 \$\{t\.textPrimary\} opacity-80`\}>Profile Image</label>.*?</div>\s*</div>',
    image_fix,
    content,
    flags=re.DOTALL
)

with open("src/App.tsx", "w") as f:
    f.write(content)
