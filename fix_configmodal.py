import re

with open('src/ConfigModal.tsx', 'r') as f:
    content = f.read()

# 1. Update imports
content = content.replace("import React, { useState } from 'react';", "import React, { useState, useRef, useEffect } from 'react';")

# 2. Add debounce functionality
handleChange_old = """const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };"""
handleChange_new = """const debounceTimer = useRef<NodeJS.Timeout | null>(null);

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
  }, []);"""
content = content.replace(handleChange_old, handleChange_new)

# 3. Fix responsive design for Sidebar Tabs
sidebar_old = """<div className={`md:w-48 border-r border-inherit p-3 space-y-1 ${isDarkMode ? 'bg-zinc-900' : 'bg-stone-50'} overflow-y-auto`}>
              <button onClick={() => setActiveTab('profile')} className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'profile' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <User size={16} /> Profile Info
              </button>
              <button onClick={() => setActiveTab('theme')} className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'theme' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <FileImage size={16} /> Theme & Media
              </button>
              <button onClick={() => setActiveTab('whatsapp')} className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'whatsapp' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <MessageSquare size={16} /> WhatsApp
              </button>
              <button onClick={() => setActiveTab('hours')} className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'hours' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <Clock size={16} /> Operating Hours
              </button>
              <button onClick={() => setActiveTab('analytics')} className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${activeTab === 'analytics' ? t.tabActive + ' ' + t.textPrimary + ' shadow-sm' : t.textSecondary + ' hover:bg-zinc-500/10'}`}>
                <Activity size={16} /> Analytics
              </button>
            </div>"""

sidebar_new = """<div className={`md:w-48 border-r md:border-b-0 border-b border-inherit p-3 flex md:flex-col gap-2 overflow-x-auto md:overflow-y-auto ${isDarkMode ? 'bg-zinc-900' : 'bg-stone-50'}`}>
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
            </div>"""
content = content.replace(sidebar_old, sidebar_new)

# 4. Descriptive labels in Profile Tab
profile_inputs_old = """<ConfigInput label="Name" name="name" value={formData.name} onChange={handleChange} t={t} />
                  <ConfigInput label="Title" name="title" value={formData.title} onChange={handleChange} t={t} />
                  <ConfigInput label="Company" name="company" value={formData.company} onChange={handleChange} t={t} />
                  <ConfigInput label="Hero Tagline" name="heroTagline" value={formData.heroTagline} onChange={handleChange} t={t} />
                  <ConfigInput label="Phone" name="phone" value={formData.phone} onChange={handleChange} t={t} />
                  <ConfigInput label="Email" name="email" value={formData.email} onChange={handleChange} t={t} />
                  <ConfigInput label="Address" name="address" value={formData.address} onChange={handleChange} t={t} />
                  <ConfigInput label="Instagram URL" name="instagram" value={formData.instagram} onChange={handleChange} t={t} />
                  <ConfigInput label="Facebook URL" name="facebook" value={formData.facebook} onChange={handleChange} t={t} />"""

profile_inputs_new = """<ConfigInput label="Full Name (name)" name="name" value={formData.name} onChange={handleChange} t={t} />
                  <ConfigInput label="Job Title (title)" name="title" value={formData.title} onChange={handleChange} t={t} />
                  <ConfigInput label="Company Name (company)" name="company" value={formData.company} onChange={handleChange} t={t} />
                  <ConfigInput label="Hero Tagline (heroTagline)" name="heroTagline" value={formData.heroTagline} onChange={handleChange} t={t} />
                  <ConfigInput label="Contact Phone (phone)" name="phone" value={formData.phone} onChange={handleChange} t={t} />
                  <ConfigInput label="Contact Email (email)" name="email" value={formData.email} onChange={handleChange} t={t} />
                  <ConfigInput label="Physical Address (address)" name="address" value={formData.address} onChange={handleChange} t={t} />
                  <ConfigInput label="Instagram Profile URL (instagram)" name="instagram" value={formData.instagram} onChange={handleChange} t={t} />
                  <ConfigInput label="Facebook Profile URL (facebook)" name="facebook" value={formData.facebook} onChange={handleChange} t={t} />"""
content = content.replace(profile_inputs_old, profile_inputs_new)

# About Me paragraphs
content = content.replace('label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 1)</label>', 'label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 1 - aboutP1)</label>')
content = content.replace('label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 2)</label>', 'label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 2 - aboutP2)</label>')
content = content.replace('label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>Status Mode</label>', 'label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>Status Mode (statusOverride)</label>')

# 5. Fix responsive design for image uploads
theme_inputs_old = """<div className="border-t border-inherit pt-4">
                    <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Profile Image</label>
                    <div className="flex items-center gap-4 mb-2">
                      {formData.profileImage ? (
                        <img src={formData.profileImage} alt="Profile preview" className="w-16 h-16 rounded-full object-cover border-2 border-inherit" />
                      ) : (
                        <div className={`w-16 h-16 rounded-full border-2 border-dashed flex items-center justify-center ${t.inputBorder} ${t.textSecondary}`}>No Img</div>
                      )}
                      <label className={`flex flex-1 items-center justify-center gap-2 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${t.inputBorder} ${t.inputBg} hover:opacity-80`}>"""

theme_inputs_new = """<div className="border-t border-inherit pt-4">
                    <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Profile Image (profileImage)</label>
                    <div className="flex flex-col sm:flex-row items-center gap-4 mb-2">
                      {formData.profileImage ? (
                        <img src={formData.profileImage} alt="Profile preview" className="w-16 h-16 shrink-0 rounded-full object-cover border-2 border-inherit" />
                      ) : (
                        <div className={`w-16 h-16 shrink-0 rounded-full border-2 border-dashed flex items-center justify-center ${t.inputBorder} ${t.textSecondary}`}>No Img</div>
                      )}
                      <label className={`flex w-full sm:flex-1 items-center justify-center gap-2 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${t.inputBorder} ${t.inputBg} hover:opacity-80`}>"""
content = content.replace(theme_inputs_old, theme_inputs_new)

bg_img_old = """<div className="border-t border-inherit pt-4">
                    <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Background Image</label>
                    <div className="flex flex-col gap-3 mb-2">"""
bg_img_new = """<div className="border-t border-inherit pt-4">
                    <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Background Image (bgImage)</label>
                    <div className="flex flex-col gap-3 mb-2">"""
content = content.replace(bg_img_old, bg_img_new)

color_old = "label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Primary Accent Color</label>"
color_new = "label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Primary Accent Color (primaryColor)</label>"
content = content.replace(color_old, color_new)

whatsapp_old = 'ConfigInput label="WhatsApp Number" name="whatsapp"'
whatsapp_new = 'ConfigInput label="WhatsApp Number (whatsapp)" name="whatsapp"'
content = content.replace(whatsapp_old, whatsapp_new)

whatsapp_tpl_old = 'label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>WhatsApp Auto-Fill Template</label>'
whatsapp_tpl_new = 'label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>WhatsApp Auto-Fill Template (whatsappTemplate)</label>'
content = content.replace(whatsapp_tpl_old, whatsapp_tpl_new)

hours_old = 'h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Operating Hours</h3>'
hours_new = 'h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Operating Hours (operatingHours)</h3>'
content = content.replace(hours_old, hours_new)

with open('src/ConfigModal.tsx', 'w') as f:
    f.write(content)
