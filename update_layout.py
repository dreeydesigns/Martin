import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add Helmet import
if 'import { Helmet }' not in content:
    content = content.replace("import React, { useState, useEffect } from 'react';", "import React, { useState, useEffect } from 'react';\nimport { Helmet } from 'react-helmet-async';")

# Add Helmet tags
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
content = re.sub(r"(return \(\n\s*<div className=\{`min-h-screen[^>]+>\n)", r"\1" + helmet_tags, content, count=1)

# Modify main tag
main_old = r"<main className=\{`max-w-md mx-auto sm:shadow-2xl sm:border sm:rounded-2xl overflow-hidden relative transition-colors duration-500 \$\{t.cardBg\} \$\{t.border\}`\}>"
main_new = r"""<main className={`w-full max-w-md md:max-w-4xl lg:max-w-5xl mx-auto md:my-8 sm:shadow-2xl sm:border sm:rounded-2xl overflow-hidden relative transition-colors duration-500 ${t.cardBg} ${t.border}`}>
        <div className="flex flex-col md:flex-row w-full relative">
          
          {/* Left Column */}
          <div className="w-full md:w-[45%] lg:w-[40%] md:border-r border-inherit relative">
            <div className="md:sticky md:top-0">"""
content = re.sub(main_old, main_new, content, count=1)

# Now we need to close the inner sticky div and left column div, and open the right column div.
# We do this right before {/* About Section */}
# The regex looks for `        {/* About Section */}`
about_section_pattern = r"(\s*\{\/\* About Section \*\/})"
split_new = r"""
            </div>
          </div>
          
          {/* Right Column */}
          <div className="w-full md:w-[55%] lg:w-[60%]">
\1"""
content = re.sub(about_section_pattern, split_new, content, count=1)

# Now we need to close the right column div and the flex div just before the end of main.
# It looks like:
#        {/* Back to Top Button */}
#        ...
#      </main>
end_main_pattern = r"(\s*</main>)"
end_main_new = r"""
          </div>
        </div>
\1"""
content = re.sub(end_main_pattern, end_main_new, content, count=1)

# Let's move {/* Social Links */} from the right column to the left column (after Action Buttons)
# Find the Social Links block
social_links_pattern = r"(\s*\{\/\* Social Links \*\/\}.*?</motion\.section>)"
match = re.search(social_links_pattern, content, flags=re.DOTALL)
if match:
    social_links_block = match.group(1)
    # Remove it from its current position
    content = content.replace(social_links_block, "")
    # Insert it right before the left column closes
    left_col_end_pattern = r"(\s*</div>\s*</div>\s*\{\/\* Right Column \*\/\})"
    content = re.sub(left_col_end_pattern, social_links_block + r"\1", content, count=1)

with open('src/App.tsx', 'w') as f:
    f.write(content)

