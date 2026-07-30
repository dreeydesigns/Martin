import re

with open('src/ConfigModal.tsx', 'r') as f:
    content = f.read()

# Remove unused states and functions
patterns = [
    r"  // Auth state\s*const \[isAuthenticated, setIsAuthenticated\] = useState\([^)]+\);\s*const \[email, setEmail\] = useState\(''\);\s*const \[password, setPassword\] = useState\(''\);\s*const \[authError, setAuthError\] = useState\(''\);\s*const \[isAuthenticating, setIsAuthenticating\] = useState\(false\);\s*const \[resetMessage, setResetMessage\] = useState\(''\);\s*const \[isResetting, setIsResetting\] = useState\(false\);\s*",
    r"  const handleResetPassword = async \(\) => \{.*?\};\s*",
    r"  const handleLogin = async \(e: React.FormEvent\) => \{.*?\};\s*"
]

for p in patterns:
    content = re.sub(p, "", content, flags=re.DOTALL)

with open('src/ConfigModal.tsx', 'w') as f:
    f.write(content)
