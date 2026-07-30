import re

with open("src/App.tsx", "r") as f:
    content = f.read()

analytics_content = r"""{activeTab === 'analytics' && (
              <div className="py-2 space-y-8">
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
              </div>
            )}"""

old_analytics = r"\{activeTab === 'analytics' && \(\s*<div className=\"py-2\">\s*<h3 className=\{`text-sm font-medium mb-4 \$\{t\.textPrimary\}`\}>Daily Profile Views \(Last 7 Days\)</h3>.*?\s*\)\}\s*</div>\s*</div>\s*\)\}"
content = re.sub(old_analytics, analytics_content, content, flags=re.DOTALL)

with open("src/App.tsx", "w") as f:
    f.write(content)
