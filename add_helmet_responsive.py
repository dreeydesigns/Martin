import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add Helmet import
if 'import { Helmet }' not in content:
    content = content.replace("import React, { useState, useEffect } from 'react';", "import React, { useState, useEffect } from 'react';\nimport { Helmet } from 'react-helmet-async';")

# Add Helmet tags inside App component
helmet_tags = """
      <Helmet>
        <title>{config.name} | {config.title}</title>
        <meta name="description" content={config.heroTagline} />
        
        {/* Open Graph / Facebook */}
        <meta property="og:type" content="profile" />
        <meta property="og:url" content={window.location.href} />
        <meta property="og:title" content={`${config.name} | ${config.title}`} />
        <meta property="og:description" content={config.heroTagline} />
        <meta property="og:image" content={config.profileImage} />

        {/* Twitter */}
        <meta property="twitter:card" content="summary_large_image" />
        <meta property="twitter:url" content={window.location.href} />
        <meta property="twitter:title" content={`${config.name} | ${config.title}`} />
        <meta property="twitter:description" content={config.heroTagline} />
        <meta property="twitter:image" content={config.profileImage} />
      </Helmet>
"""
return_div = r"(return \(\n\s*<div className=\{`min-h-screen[^>]+>\n)"
content = re.sub(return_div, r"\1" + helmet_tags, content, count=1)

# Modify main tag for responsiveness
main_old = r"<main className=\{`max-w-md mx-auto sm:shadow-2xl sm:border sm:rounded-2xl overflow-hidden relative transition-colors duration-500 \$\{t.cardBg\} \$\{t.border\}`\}>"
main_new = r"""<main className={`w-full max-w-md md:max-w-4xl lg:max-w-5xl mx-auto sm:shadow-2xl sm:border sm:rounded-2xl overflow-hidden relative transition-colors duration-500 ${t.cardBg} ${t.border}`}>
        <div className="flex flex-col md:flex-row w-full h-full">
          
          {/* Left Column / Top Mobile */}
          <div className="w-full md:w-2/5 lg:w-1/3 md:border-r border-inherit relative">"""
content = re.sub(main_old, main_new, content, count=1)

# We need to split the sections.
# Left side sections:
# - Header / Hero Section (starts with <!-- Header / Hero Section --> or <motion.section className="relative">)
# - Action Buttons (Share, Save) (starts with <motion.section className="px-6 pb-6 pt-2")
# - Social Links (starts with <motion.section className="px-6 py-10")

# So we insert the end of left column and start of right column before "<!-- Operating Hours -->" or the fourth <motion.section>
# Looking at grep output, the 4th motion.section is at line 787.
# Let's search for the "Operating Hours" section or the 4th section.
# Actually, looking at the app, the sections are:
# 1. Header (615)
# 2. Action Buttons (686)
# 3. Social Links (770)
# 4. Operating Hours / Quick Actions / About Me ...
# Let's see what is immediately after Social Links.
