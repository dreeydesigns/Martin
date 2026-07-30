import { initializeApp } from 'firebase/app';
import { getFirestore, doc, setDoc, getDoc, updateDoc, collection, getDocs, onSnapshot, query, where, orderBy, limit } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { getStorage } from 'firebase/storage';
import firebaseConfig from '../firebase-applet-config.json';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app, firebaseConfig.firestoreDatabaseId);
const auth = getAuth(app);
const storage = getStorage(app);

export { app, db, auth, storage, doc, setDoc, getDoc, updateDoc, collection, getDocs, onSnapshot, query, where, orderBy, limit };
