import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'motion/react';
import { Upload, Download, Cloud, X, Lock, FileImage, User, Activity, Settings, MessageSquare, Clock, Eye } from 'lucide-react';
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer } from 'recharts';
import CropModal from './CropModal';
import { storage } from './firebase';
import { ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage';

const ConfigInput = ({ label, name, value, onChange, t }: any) => (
  <div className="mb-4">
    <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>{label}</label>
    <input 
      type="text" 
      name={name}
      value={value}
      onChange={onChange}
      className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
    />
  </div>
);

export default function ConfigModal({ currentConfig, rawViewsData, socialClicks, visitorLocations, onSave, onSync, onClose, isDarkMode }: any) {
  const [formData, setFormData] = useState(currentConfig);
  const [activeTab, setActiveTab] = useState<'profile' | 'theme' | 'analytics' | 'hours' | 'whatsapp'>('profile');
  
  const [cropTarget, setCropTarget] = useState<'profileImage' | 'bgImage' | null>(null);
  const [cropImageSrc, setCropImageSrc] = useState<string>('');

  const [dateRange, setDateRange] = useState<'7' | '30' | 'all'>('7');

// Storage upload state
  const [uploadingImage, setUploadingImage] = useState<string | null>(null);

  const t = {
    bg: isDarkMode ? "bg-zinc-900 border-zinc-800" : "bg-white border-stone-200",
    textPrimary: isDarkMode ? "text-white" : "text-zinc-900",
    textSecondary: isDarkMode ? "text-zinc-400" : "text-zinc-600",
    inputBg: isDarkMode ? "bg-zinc-950" : "bg-stone-50",
    inputBorder: isDarkMode ? "border-zinc-800" : "border-stone-200",
    tabBg: isDarkMode ? "bg-zinc-800" : "bg-stone-200",
    tabActive: isDarkMode ? "bg-zinc-700" : "bg-white shadow-sm",
  };

  const debounceTimer = useRef<NodeJS.Timeout | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const newConfig = { ...formData, [e.target.name]: e.target.value };
    setFormData(newConfig);
    
    if (debounceTimer.current) clearTimeout(debounceTimer.current);
    debounceTimer.current = setTimeout(() => {
      onSave(newConfig);
      onSync(newConfig);
    }, 1200);
  };
  
  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
    };
  }, []);

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
    if (e.target.files && e.target.files.length > 0) {
      const reader = new FileReader();
      reader.addEventListener('load', () => {
        setCropImageSrc(reader.result?.toString() || '');
        setCropTarget(target);
      });
      reader.readAsDataURL(e.target.files[0]);
    }
  };

  const uploadToStorage = async (base64Image: string, target: 'profileImage' | 'bgImage') => {
    setUploadingImage(target);
    try {
      // Convert base64 to blob
      const res = await fetch(base64Image);
      const blob = await res.blob();
      const ext = blob.type.split('/')[1] || 'jpeg';
      
      const fileRef = ref(storage, `images/${target}_${Date.now()}.${ext}`);
      await uploadBytesResumable(fileRef, blob);
      const downloadURL = await getDownloadURL(fileRef);
      
      setFormData((prev: any) => ({ ...prev, [target]: downloadURL }));
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Failed to upload image to Storage. Using base64 fallback.");
      // Fallback to base64 if storage fails (e.g. no permissions)
      setFormData((prev: any) => ({ ...prev, [target]: base64Image }));
    } finally {
      setUploadingImage(null);
    }
  };

  // Generate Analytics Data
  const getAnalyticsData = () => {
    if (!rawViewsData) return [];
    
    let days = 7;
    if (dateRange === '30') days = 30;
    if (dateRange === 'all') days = 365;

    const chartData = Object.keys(rawViewsData)
      .filter(k => k !== 'total')
      .sort()
      .slice(-days)
      .map(k => ({
        date: k.split('-').slice(1).join('/'),
        views: rawViewsData[k]
      }));
    return chartData;
  };
  const analyticsData = getAnalyticsData();

  return (
    <>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-[100] bg-black/80 flex items-center justify-center p-4 overflow-y-auto">
        <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }} className={`w-full max-w-2xl rounded-xl overflow-hidden shadow-2xl border flex flex-col max-h-[90vh] ${t.bg}`}>
          <div className="flex items-center justify-between p-4 border-b border-inherit bg-inherit z-10">
            <h2 className={`text-lg font-medium flex items-center gap-2 ${t.textPrimary}`}>
              <Settings size={20} /> Settings
            </h2>
            <div className="flex items-center gap-2">
              <label className="p-2 rounded-full hover:bg-zinc-500/20 text-emerald-500 transition-colors cursor-pointer" title="Import Config">
                <Upload size={20} />
                <input type="file" accept=".json" className="hidden" onChange={handleImport} />
              </label>
              <button onClick={handleExport} title="Export Config" className="p-2 rounded-full hover:bg-zinc-500/20 text-blue-500 transition-colors">
                <Download size={20} />
              </button>
              <button onClick={() => onSync(formData)} title="Sync to Cloud" className="p-2 rounded-full hover:bg-zinc-500/20 text-[#c5a059] transition-colors">
                <Cloud size={20} />
              </button>
              <button onClick={onClose} className="p-2 rounded-full hover:bg-black/10 transition-colors">
                <X size={20} className={t.textPrimary} />
              </button>
            </div>
          </div>
          
          <div className="flex flex-col md:flex-row flex-1 overflow-hidden">
            {/* Sidebar Tabs */}
            <div className={`md:w-48 border-r md:border-b-0 border-b border-inherit p-3 flex md:flex-col gap-2 overflow-x-auto md:overflow-y-auto ${isDarkMode ? 'bg-zinc-900' : 'bg-stone-50'}`}>
              <button onClick={() => setActiveTab('profile')} className={`shrink-0 md:w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'profile' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <User size={16} /> Profile Info
              </button>
              <button onClick={() => setActiveTab('theme')} className={`shrink-0 md:w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'theme' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <FileImage size={16} /> Theme & Media
              </button>
              <button onClick={() => setActiveTab('whatsapp')} className={`shrink-0 md:w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'whatsapp' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <MessageSquare size={16} /> WhatsApp
              </button>
              <button onClick={() => setActiveTab('hours')} className={`shrink-0 md:w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'hours' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <Clock size={16} /> Operating Hours
              </button>
              <button onClick={() => setActiveTab('analytics')} className={`shrink-0 md:w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'analytics' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <Activity size={16} /> Analytics
              </button>
            </div>

            {/* Content Area */}
            <div className="flex-1 p-6 overflow-y-auto">
              
              {activeTab === 'profile' && (
                <div className="space-y-4">
                  <div className="mb-4">
                    <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>Status Mode (statusOverride)</label>
                    <select 
                      name="statusOverride"
                      value={formData.statusOverride}
                      onChange={handleChange}
                      className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                    >
                      <option value="auto">Auto (Based on business hours)</option>
                      <option value="available">Always Available</option>
                      <option value="away">Always Away</option>
                    </select>
                  </div>
                  
                  <ConfigInput label="Full Name (name)" name="name" value={formData.name} onChange={handleChange} t={t} />
                  <ConfigInput label="Job Title (title)" name="title" value={formData.title} onChange={handleChange} t={t} />
                  <ConfigInput label="Company Name (company)" name="company" value={formData.company} onChange={handleChange} t={t} />
                  <ConfigInput label="Hero Tagline (heroTagline)" name="heroTagline" value={formData.heroTagline} onChange={handleChange} t={t} />
                  <ConfigInput label="Contact Phone (phone)" name="phone" value={formData.phone} onChange={handleChange} t={t} />
                  <ConfigInput label="Contact Email (email)" name="email" value={formData.email} onChange={handleChange} t={t} />
                  <ConfigInput label="Physical Address (address)" name="address" value={formData.address} onChange={handleChange} t={t} />
                  <ConfigInput label="Instagram Profile URL (instagram)" name="instagram" value={formData.instagram} onChange={handleChange} t={t} />
                  <ConfigInput label="Facebook Profile URL (facebook)" name="facebook" value={formData.facebook} onChange={handleChange} t={t} />
                  
                  <div>
                    <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 1 - aboutP1)</label>
                    <textarea 
                      name="aboutP1"
                      value={formData.aboutP1}
                      onChange={handleChange}
                      rows={3}
                      className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                    />
                  </div>
                  <div>
                    <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 2 - aboutP2)</label>
                    <textarea 
                      name="aboutP2"
                      value={formData.aboutP2}
                      onChange={handleChange}
                      rows={3}
                      className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                    />
                  </div>
                </div>
              )}

              {activeTab === 'theme' && (
                <div className="space-y-6">
                  <div>
                    <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Primary Accent Color (primaryColor)</label>
                    <div className="flex items-center gap-3">
                      <input 
                        type="color" 
                        name="primaryColor"
                        value={formData.primaryColor}
                        onChange={handleChange}
                        className="w-10 h-10 rounded cursor-pointer border-0 p-0 bg-transparent"
                      />
                      <span className={`text-sm font-mono uppercase ${t.textSecondary}`}>{formData.primaryColor}</span>
                    </div>
                  </div>
                  
                  <div className="border-t border-inherit pt-4">
                    <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Profile Image (profileImage)</label>
                    <div className="flex flex-col sm:flex-row items-center gap-4 mb-2">
                      {formData.profileImage ? (
                        <img src={formData.profileImage} alt="Profile preview" className="w-16 h-16 shrink-0 rounded-full object-cover border-2 border-inherit" />
                      ) : (
                        <div className={`w-16 h-16 shrink-0 rounded-full border-2 border-dashed flex items-center justify-center ${t.inputBorder} ${t.textSecondary}`}>No Img</div>
                      )}
                      <label className={`flex w-full sm:flex-1 items-center justify-center gap-2 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${t.inputBorder} ${t.inputBg} hover:opacity-80`}>
                        {uploadingImage === 'profileImage' ? (
                           <div className="w-4 h-4 border-2 border-zinc-400 border-t-zinc-800 rounded-full animate-spin" />
                        ) : (
                           <Upload size={16} className={t.textSecondary} />
                        )}
                        <span className={`text-sm font-medium ${t.textPrimary}`}>
                          {uploadingImage === 'profileImage' ? 'Uploading...' : 'Upload Profile Image'}
                        </span>
                        <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e, 'profileImage')} disabled={!!uploadingImage} />
                      </label>
                    </div>
                  </div>

                  <div className="border-t border-inherit pt-4">
                    <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Background Image (bgImage)</label>
                    <div className="flex flex-col gap-3 mb-2">
                      {formData.bgImage ? (
                        <img src={formData.bgImage} alt="Background preview" className="w-full h-24 rounded-lg object-cover border border-inherit" />
                      ) : (
                        <div className={`w-full h-24 rounded-lg border-2 border-dashed flex items-center justify-center ${t.inputBorder} ${t.textSecondary}`}>No Img</div>
                      )}
                      <label className={`flex w-full items-center justify-center gap-2 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${t.inputBorder} ${t.inputBg} hover:opacity-80`}>
                        {uploadingImage === 'bgImage' ? (
                           <div className="w-4 h-4 border-2 border-zinc-400 border-t-zinc-800 rounded-full animate-spin" />
                        ) : (
                           <Upload size={16} className={t.textSecondary} />
                        )}
                        <span className={`text-sm font-medium ${t.textPrimary}`}>
                          {uploadingImage === 'bgImage' ? 'Uploading...' : 'Upload Background Image'}
                        </span>
                        <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e, 'bgImage')} disabled={!!uploadingImage} />
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'whatsapp' && (
                <div className="space-y-6">
                  <ConfigInput label="WhatsApp Number (whatsapp)" name="whatsapp" value={formData.whatsapp} onChange={handleChange} t={t} />
                  
                  <div>
                    <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>WhatsApp Auto-Fill Template (whatsappTemplate)</label>
                    <p className={`text-[10px] mb-2 ${t.textSecondary}`}>Variables: {'{name}'}, {'{message}'}</p>
                    <textarea 
                      name="whatsappTemplate"
                      value={formData.whatsappTemplate}
                      onChange={handleChange}
                      rows={4}
                      className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                    />
                  </div>

                  <div className={`p-4 rounded-xl border ${t.inputBorder} ${isDarkMode ? 'bg-zinc-900/50' : 'bg-stone-100/50'}`}>
                    <h3 className={`text-xs font-medium mb-3 flex items-center gap-2 ${t.textPrimary}`}><Eye size={14}/> Message Preview</h3>
                    <div className="flex flex-col gap-2">
                      <div className={`p-3 rounded-lg rounded-tr-none max-w-[85%] self-end text-sm text-white shadow-sm`} style={{ backgroundColor: '#128C7E' }}>
                        <p className="whitespace-pre-wrap">{formData.whatsappTemplate.replace('{name}', 'John Doe').replace('{message}', 'I am interested in buying a Range Rover Vogue.')}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'hours' && (
                <div className="space-y-4">
                  <h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Operating Hours (operatingHours)</h3>
                  {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map((dayName, idx) => {
                    const dIdx = idx === 6 ? 0 : idx + 1;
                    const hours = formData.operatingHours?.[dIdx] || { enabled: false, start: '09:00', end: '17:00' };
                    
                    const handleHourChange = (field: string, value: any) => {
                      setFormData((prev: any) => ({
                        ...prev,
                        operatingHours: {
                          ...prev.operatingHours,
                          [dIdx]: { ...hours, [field]: value }
                        }
                      }));
                    };

                    return (
                      <div key={dayName} className={`flex items-center gap-3 p-3 rounded-lg border ${t.inputBorder} ${t.inputBg}`}>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" className="sr-only peer" checked={hours.enabled} onChange={(e) => handleHourChange('enabled', e.target.checked)} />
                          <div className={`w-9 h-5 bg-zinc-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-zinc-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all ${hours.enabled ? 'theme-bg' : isDarkMode ? 'bg-zinc-700' : 'bg-stone-300'}`}></div>
                        </label>
                        <span className={`w-24 text-sm font-medium ${t.textPrimary}`}>{dayName}</span>
                        
                        <div className={`flex items-center gap-2 ${!hours.enabled ? 'opacity-30 pointer-events-none' : ''}`}>
                          <input 
                            type="time" 
                            value={hours.start}
                            onChange={(e) => handleHourChange('start', e.target.value)}
                            className={`px-2 py-1 text-sm rounded border ${t.inputBorder} ${t.inputBg} ${t.textPrimary}`}
                          />
                          <span className={t.textSecondary}>to</span>
                          <input 
                            type="time" 
                            value={hours.end}
                            onChange={(e) => handleHourChange('end', e.target.value)}
                            className={`px-2 py-1 text-sm rounded border ${t.inputBorder} ${t.inputBg} ${t.textPrimary}`}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {activeTab === 'analytics' && (
                <div className="py-2 space-y-8">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className={`text-sm font-medium ${t.textPrimary}`}>Profile Views</h3>
                      <select 
                        value={dateRange}
                        onChange={(e) => setDateRange(e.target.value as any)}
                        className={`text-xs px-2 py-1 rounded border ${t.inputBg} ${t.inputBorder} ${t.textPrimary}`}
                      >
                        <option value="7">Last 7 Days</option>
                        <option value="30">Last 30 Days</option>
                        <option value="all">All Time</option>
                      </select>
                    </div>
                    
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

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                </div>
              )}

            </div>
          </div>
          
          <div className="p-4 border-t border-inherit bg-inherit flex justify-end gap-3 z-10">
            <button 
              onClick={onClose}
              className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${isDarkMode ? 'border-zinc-700 text-zinc-300 hover:bg-zinc-800' : 'border-stone-300 text-zinc-700 hover:bg-stone-100'}`}
            >
              Close
            </button>
            <button 
              onClick={() => onSave(formData)}
              className="px-4 py-2 rounded-lg text-sm font-medium theme-bg text-white hover:opacity-90 transition-opacity"
            >
              Save Changes
            </button>
          </div>
        </motion.div>
      </motion.div>

      {cropTarget && cropImageSrc && (
        <CropModal 
          imageSrc={cropImageSrc}
          aspectRatio={cropTarget === 'profileImage' ? 1 : 16/9}
          isDarkMode={isDarkMode}
          onClose={() => {
            setCropTarget(null);
            setCropImageSrc('');
          }}
          onCropComplete={async (croppedBase64) => {
            setCropTarget(null);
            setCropImageSrc('');
            await uploadToStorage(croppedBase64, cropTarget);
          }}
        />
      )}
    </>
  );
}
