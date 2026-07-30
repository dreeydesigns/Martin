with open('src/ConfigModal.tsx', 'r') as f:
    content = f.read()

auth_import_old = "import { signInWithEmailAndPassword, signOut } from 'firebase/auth';"
auth_import_new = "import { signInWithEmailAndPassword, signOut, sendPasswordResetEmail } from 'firebase/auth';"
content = content.replace(auth_import_old, auth_import_new)

# Add state for reset password
state_old = "const [isAuthenticating, setIsAuthenticating] = useState(false);"
state_new = """const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [resetMessage, setResetMessage] = useState('');
  const [isResetting, setIsResetting] = useState(false);"""
content = content.replace(state_old, state_new)

# Add handleResetPassword
login_fn_old = "const handleLogin = async (e: React.FormEvent) => {"
login_fn_new = """const handleResetPassword = async () => {
    if (!email) {
      setAuthError('Please enter your email to reset password.');
      return;
    }
    setIsResetting(true);
    setAuthError('');
    setResetMessage('');
    try {
      await sendPasswordResetEmail(auth, email);
      setResetMessage('Password reset email sent! Check your inbox.');
    } catch (err: any) {
      setAuthError('Failed to send reset email. Ensure the email is correct.');
    } finally {
      setIsResetting(false);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {"""
content = content.replace(login_fn_old, login_fn_new)

# Add Forgot Password button in the auth form
form_old = """{authError && <p className="text-red-500 text-xs">{authError}</p>}
            <button disabled={isAuthenticating} type="submit" className="w-full py-2 rounded-lg theme-bg text-white text-sm font-medium hover:opacity-90 transition-opacity">
              {isAuthenticating ? 'Authenticating...' : 'Login'}
            </button>
            <p className={`text-[10px] text-center mt-2 ${t.textSecondary}`}>
              You must enable Email/Password auth in Firebase Console.
            </p>"""

form_new = """{authError && <p className="text-red-500 text-xs">{authError}</p>}
            {resetMessage && <p className="text-emerald-500 text-xs">{resetMessage}</p>}
            
            <div className="flex flex-col gap-2">
              <button disabled={isAuthenticating} type="submit" className="w-full py-2 rounded-lg theme-bg text-white text-sm font-medium hover:opacity-90 transition-opacity">
                {isAuthenticating ? 'Authenticating...' : 'Login'}
              </button>
              <button 
                type="button" 
                onClick={handleResetPassword}
                disabled={isResetting || isAuthenticating}
                className={`w-full py-2 rounded-lg border text-sm font-medium transition-opacity ${t.inputBorder} ${t.textPrimary} hover:opacity-80`}
              >
                {isResetting ? 'Sending...' : 'Forgot Password?'}
              </button>
            </div>
            
            <p className={`text-[10px] text-center mt-2 ${t.textSecondary}`}>
              You must enable Email/Password auth in Firebase Console.
            </p>"""
content = content.replace(form_old, form_new)

with open('src/ConfigModal.tsx', 'w') as f:
    f.write(content)
