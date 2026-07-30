with open('src/ConfigModal.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { auth, storage } from './firebase';", "import { storage } from './firebase';")
content = content.replace("import { signInWithEmailAndPassword, signOut, sendPasswordResetEmail } from 'firebase/auth';\n", "")

with open('src/ConfigModal.tsx', 'w') as f:
    f.write(content)
