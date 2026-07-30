import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# 1. Imports
# Need to import auth and storage
import_firebase_repl = r"import { db, doc, setDoc, getDoc, updateDoc } from './firebase';"
import_firebase_new = r"""import { db, doc, setDoc, getDoc, updateDoc, auth, storage } from './firebase';
import { signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage';
"""
content = content.replace(import_firebase_repl, import_firebase_new)

# 2. Add isLoading and rawViewsData state
state_repl = r"const \[analyticsData, setAnalyticsData\] = useState<\{date: string, views: number\}\[\]>\(\[\]\);"
state_new = r"""const [isLoading, setIsLoading] = useState(true);
  const [rawViewsData, setRawViewsData] = useState<Record<string, number>>({});
  const [analyticsData, setAnalyticsData] = useState<{date: string, views: number}[]>([]);"""
content = re.sub(state_repl, state_new, content)

# 3. Update fetchConfig to handle isLoading
fetch_repl = r"fetchConfig\(\);"
fetch_new = r"""await fetchConfig();
    setIsLoading(false);"""
content = re.sub(fetch_repl, fetch_new, content)

# 4. Update trackView to save rawViewsData
track_view_repl = r"setAnalyticsData\(chartData\);"
track_view_new = r"""setAnalyticsData(chartData);
        setRawViewsData(viewsData);"""
content = re.sub(track_view_repl, track_view_new, content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
