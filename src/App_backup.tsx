import { 
  Phone, Mail, MessageCircle, MapPin, Clock, 
  Award, CheckCircle, Car, Edit,
  Facebook, Instagram, Navigation, Calendar, X,
  Share2, Download, QrCode, Sun, Moon, Map, ChevronUp, Quote,
  Send, ArrowUp, ChevronDown, Eye, BarChart2, Cloud, Upload
} from 'lucide-react';
import React, { ReactNode, useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import QRCode from 'react-qr-code';
import confetti from 'canvas-confetti';
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer } from 'recharts';
import CropModal from './CropModal';
import { db, doc, setDoc, getDoc, updateDoc } from './firebase';

const defaultConfig = {
  bgImage: "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?q=80&w=1000&auto=format&fit=crop",
  profileImage: "https://storage.googleapis.com/aistudio-dev-uploads/e0fb3af3-2e0f-4886-acbc-992a5435e165.jpeg",
  primaryColor: "#c5a059",
  name: "Martin Mwihoti",
  title: "Sales & Marketing Manager",
  company: "Range Rover Centre Ltd",
  phone: "+254704183358",
  whatsapp: "+254704183358",
  whatsappTemplate: "Hi Martin, I'm {name}.\n\n{message}",
  email: "mmwihoti@gmail.com",
  address: "Kiambu Road, 00100, Nairobi, Kenya",
  instagram: "https://www.instagram.com/m.mwihoti_/",
  facebook: "https://www.facebook.com/p/Range-Rover-Centre-Motors-61574959497030/",
  hoursMonFri: "Mon-Fri: 8:00 AM - 5:00 PM",
  hoursSat: "Saturday: 9:00 AM - 1:00 PM",
  hoursSun: "Sunday: Closed",
  heroTagline: "\"Dealer in Landrover, Range Rover and Discovery. Imports, Insurance, Local Re-sale, Parts and Repairs.\"",
  aboutP1: "With over a decade of experience in automotive sales, I specialize in matching clients with the perfect Land Rover or Range Rover to suit their lifestyle.",
  aboutP2: "As the Sales & Marketing Manager at Range Rover Centre Ltd, my approach is built on transparency, personalized service, and a deep passion for the heritage of the brand. Whether you are exploring our latest models or seeking a certified pre-owned vehicle, I am committed to making your ownership journey seamless and rewarding."
};

const contentData = {
  en: {
    shareProfile: "Share Profile",
    saveContact: "Save Contact",
    call: "Call",
    whatsapp: "WhatsApp",
    email: "Email",
    aboutTitle: "About Me",
    servicesTitle: "What I Help With",
    service1Title: "New & Pre-Owned Sales",
    service1Desc: "Latest Range Rover models & vetted pre-owned vehicles.",
    service2Title: "Imports & Local Re-sale",
    service2Desc: "Sourcing high-quality vehicles internationally and locally.",
    service3Title: "Parts & Repairs",
    service3Desc: "Genuine parts and trusted repair services.",
    service4Title: "Insurance Guidance",
    service4Desc: "Tailored insurance packages for your vehicle.",
    expTitle: "Experience & Credentials",
    exp1: "Extensive Experience in Luxury Automotive",
    exp2: "Land Rover & Range Rover Specialist",
    exp3: "Expertise in Vehicle Imports",
    testTitle: "Client Testimonials",
    visitTitle: "Visit the Showroom",
    directions: "Directions",
    viewMap: "View on Map",
    hideMap: "Hide Map",
    businessHours: "Business Hours",
    contactTitle: "Send a Message",
    contactName: "Your Name",
    contactMessage: "Your Message",
    contactSend: "Send Message",
    scanTitle: "Scan to Connect",
    scanDesc: "Share this digital card instantly.",
    available: "Available",
    away: "Away",
    faqTitle: "Frequently Asked Questions",
    addCalendar: "Add to Calendar"
  },
  sw: {
    shareProfile: "Shiriki Profaili",
    saveContact: "Hifadhi Anwani",
    call: "Piga Simu",
    whatsapp: "WhatsApp",
    email: "Barua Pepe",
    aboutTitle: "Kuhusu Mimi",
    servicesTitle: "Ninachosaidia",
    service1Title: "Uuzaji Mpya & Zilizotumika",
    service1Desc: "Miundo ya hivi karibuni ya Range Rover & magari yaliyotumika yaliyokaguliwa.",
    service2Title: "Uagizaji & Uuzaji Ndani",
    service2Desc: "Kutafuta magari yenye ubora wa hali ya juu kimataifa na ndani.",
    service3Title: "Vipuri & Matengenezo",
    service3Desc: "Vipuri halisi na huduma za kuaminika za matengenezo.",
    service4Title: "Mwongozo wa Bima",
    service4Desc: "Vifurushi vya bima vilivyoboreshwa kwa gari lako.",
    expTitle: "Uzoefu na Sifa",
    exp1: "Uzoefu Mkubwa katika Magari ya Kifahari",
    exp2: "Mtaalam wa Land Rover & Range Rover",
    exp3: "Utaalam katika Uagizaji wa Magari",
    testTitle: "Ushuhuda wa Wateja",
    visitTitle: "Tembelea Showroom",
    directions: "Maelekezo",
    viewMap: "Tazama Kwenye Ramani",
    hideMap: "Ficha Ramani",
    businessHours: "Saa za Kazi",
    contactTitle: "Tuma Ujumbe",
    contactName: "Jina Lako",
    contactMessage: "Ujumbe Wako",
    contactSend: "Tuma Ujumbe",
    scanTitle: "Skani Kuunganisha",
    scanDesc: "Shiriki kadi hii ya kidijitali mara moja.",
    available: "Inapatikana",
    away: "Hayupo",
    faqTitle: "Maswali Yanayoulizwa Mara kwa Mara",
    addCalendar: "Ongeza kwa Kalenda"
  }
};

const faqs = [
  {
    q: "How long does it take to import a vehicle?",
    a: "Depending on the origin country (usually UK, Japan, or Australia), importing typically takes 4-6 weeks from purchase to clearing at the Port of Mombasa."
  },
  {
    q: "Do you offer financing options?",
    a: "Yes, we partner with major local banks to offer asset financing for up to 80% for both new and locally used models."
  },
  {
    q: "What does your insurance guidance cover?",
    a: "We help you compare comprehensive motor insurance quotes from top underwriters, ensuring you get the best valuation and premium rates."
  },
  {
    q: "Can you source specific parts?",
    a: "Absolutely. If we don't have it in stock locally, we can air-freight genuine Land Rover/Range Rover parts within 5-7 working days."
  }
];

type Language = 'en' | 'sw';

export default function App() {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [lang, setLang] = useState<Language>('en');
  const [isOnline, setIsOnline] = useState(false);
  const [showMap, setShowMap] = useState(false);
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [showBackToTop, setShowBackToTop] = useState(false);
  
  const [pageViews, setPageViews] = useState(0);
  const [analyticsData, setAnalyticsData] = useState<{date: string, views: number}[]>([]);
  
  const [isEditing, setIsEditing] = useState(false);
  const [config, setConfig] = useState(defaultConfig);

  const [formName, setFormName] = useState('');
  const [formMessage, setFormMessage] = useState('');
  
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const content = contentData[lang];

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const configRef = doc(db, 'configs', 'main');
        const configSnap = await getDoc(configRef);
        if (configSnap.exists()) {
          setConfig({ ...defaultConfig, ...configSnap.data() as typeof defaultConfig });
        } else {
          // Check local storage fallback
          const savedConfig = localStorage.getItem('business_card_config');
          if (savedConfig) {
            setConfig({ ...defaultConfig, ...JSON.parse(savedConfig) });
          }
        }
      } catch (e) {
        console.error("Error fetching config", e);
        const savedConfig = localStorage.getItem('business_card_config');
        if (savedConfig) setConfig({ ...defaultConfig, ...JSON.parse(savedConfig) });
      }
    };
    fetchConfig();

    const trackView = async () => {
      // Basic local storage tracking + Firestore sync for analytics
      const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
      const localKey = `viewed_${today}`;
      
      try {
        const viewsRef = doc(db, 'configs', 'views');
        const viewsSnap = await getDoc(viewsRef);
        
        let viewsData: Record<string, number> = {};
        if (viewsSnap.exists()) {
          viewsData = viewsSnap.data() as Record<string, number>;
        }
        
        // If haven't viewed today in this session/browser, increment
        if (!sessionStorage.getItem(localKey)) {
          sessionStorage.setItem(localKey, 'true');
          viewsData[today] = (viewsData[today] || 0) + 1;
          viewsData.total = (viewsData.total || 0) + 1;
          await setDoc(viewsRef, viewsData);
        }
        
        setPageViews(viewsData.total || 0);
        
        // Format for recharts
        const chartData = Object.keys(viewsData)
          .filter(k => k !== 'total')
          .sort()
          .slice(-7) // Last 7 days
          .map(k => ({
            date: k.split('-').slice(1).join('/'), // MM/DD
            views: viewsData[k]
          }));
        
        setAnalyticsData(chartData);

      } catch (e) {
        console.error("Error tracking view", e);
      }
    };
    
    trackView();
  }, []);

  const handleSaveConfig = async (newConfig: typeof config) => {
    setConfig(newConfig);
    localStorage.setItem('business_card_config', JSON.stringify(newConfig));
    setIsEditing(false);
  };

  const handleSyncCloud = async (newConfig: typeof config) => {
    try {
      await setDoc(doc(db, 'configs', 'main'), newConfig);
      alert('Configuration successfully synced to cloud!');
    } catch (e) {
      console.error("Sync error", e);
      alert('Failed to sync. Please try again.');
    }
  };

  useEffect(() => {
    const checkStatus = () => {
      const now = new Date();
      const nairobiTime = new Date(now.toLocaleString("en-US", {timeZone: "Africa/Nairobi"}));
      const day = nairobiTime.getDay();
      const hour = nairobiTime.getHours();

      let online = false;
      if (day >= 1 && day <= 5) {
        if (hour >= 8 && hour < 17) online = true;
      } else if (day === 6) {
        if (hour >= 9 && hour < 13) online = true;
      }
      setIsOnline(online);
    };

    checkStatus();
    const interval = setInterval(checkStatus, 60000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 300) {
        setShowBackToTop(true);
      } else {
        setShowBackToTop(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${config.name} - ${config.title}`,
          text: `Check out ${config.name}'s digital business card.`,
          url: window.location.href,
        });
      } catch (error) {
        console.error('Error sharing', error);
      }
    } else {
      alert("Sharing is not supported on this browser. You can copy the URL.");
    }
  };

  const handleSaveContact = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: [config.primaryColor, '#ffffff', '#09090b']
    });

    const vcfData = `BEGIN:VCARD
VERSION:3.0
N:${config.name.split(' ').pop()};${config.name.split(' ')[0]};;;
FN:${config.name}
ORG:${config.company}
TITLE:${config.title}
TEL;TYPE=WORK,VOICE:${config.phone}
EMAIL;TYPE=PREF,INTERNET:${config.email}
URL:https://www.rangerovercentre.co.ke
ADR;TYPE=WORK:;;${config.address.split(',')[0]};${config.address.split(',')[1] || ''};;;Kenya
END:VCARD`;

    const blob = new Blob([vcfData], { type: 'text/vcard' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${config.name.replace(/\s+/g, '_')}.vcf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleAddToCalendar = () => {
    const event = {
        title: `Consultation with ${config.name}`,
        description: 'Discussing vehicle options and inquiries.',
        duration: 60
    };
    
    const now = new Date();
    const start = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    const end = new Date(start.getTime() + 60 * 60 * 1000);

    const formatICSDate = (date: Date) => {
        return date.toISOString().replace(/-|:/g, '').split('.')[0] + 'Z';
    };

    const icsContent = `BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:${event.title}
DESCRIPTION:${event.description}
DTSTART:${formatICSDate(start)}
DTEND:${formatICSDate(end)}
LOCATION:${config.company}
END:VEVENT
END:VCALENDAR`;

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'consultation.ics';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    let text = config.whatsappTemplate.replace('{name}', formName).replace('{message}', formMessage);
    const waUrl = `https://wa.me/${config.whatsapp.replace('+', '')}?text=${encodeURIComponent(text)}`;
    window.open(waUrl, '_blank');
  };

  const toggleLanguage = () => {
    setLang(prev => prev === 'en' ? 'sw' : 'en');
  };

  const testimonials = [
    { text: "Martin made finding my new Range Rover an absolute pleasure. Professional and transparent throughout the entire process.", author: "James K.", role: "Business Owner" },
    { text: "The best automotive purchasing experience I've ever had in Nairobi. His knowledge of the brand is truly unmatched.", author: "Sarah M.", role: "Corporate Executive" },
    { text: "Efficient, polite, and extremely helpful. He found exactly what I was looking for and handled the import seamlessly.", author: "David W.", role: "Architect" }
  ];

  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6, ease: "easeOut" }
  };

  const staggerContainer = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const t = {
    bg: isDarkMode ? "bg-zinc-950 text-zinc-300" : "bg-stone-100 text-zinc-800",
    cardBg: isDarkMode ? "bg-zinc-950 sm:bg-zinc-900/40" : "bg-stone-50 sm:bg-white",
    textPrimary: isDarkMode ? "text-white" : "text-zinc-900",
    textSecondary: isDarkMode ? "text-zinc-400" : "text-zinc-600",
    border: isDarkMode ? "border-zinc-800/50" : "border-stone-200",
    divider: isDarkMode ? "bg-zinc-800" : "bg-stone-200",
    sectionBg: isDarkMode ? "bg-zinc-900/30" : "bg-stone-100",
    btnBg: isDarkMode ? "bg-zinc-900" : "bg-white",
    btnBorder: isDarkMode ? "border-zinc-800" : "border-stone-200",
    btnHover: isDarkMode ? "hover:bg-zinc-800" : "hover:bg-stone-50",
    gradientTop: isDarkMode ? "from-[#1a1c1a] to-zinc-950" : "from-stone-300/50 to-stone-50",
    inputBg: isDarkMode ? "bg-zinc-950" : "bg-white",
    inputBorder: isDarkMode ? "border-zinc-800 theme-ring" : "border-stone-300 theme-ring",
  };

  return (
    <div className={`min-h-screen font-sans sm:py-8 selection-theme transition-colors duration-500 ${t.bg}`}>
      
      {/* Inject dynamic CSS variables for the theme */}
      <style>{`
        .theme-text { color: ${config.primaryColor}; }
        .theme-bg { background-color: ${config.primaryColor}; }
        .theme-border { border-color: ${config.primaryColor}; }
        .theme-ring:focus { outline: none; border-color: ${config.primaryColor}; box-shadow: 0 0 0 1px ${config.primaryColor}; }
        .theme-shadow { box-shadow: 0 0 15px ${config.primaryColor}20; }
        .theme-hover-bg:hover { background-color: ${config.primaryColor}; color: white; }
        .theme-hover-border:hover { border-color: ${config.primaryColor}80; }
        .theme-hover-text:hover { color: ${config.primaryColor}; }
        .selection-theme *::selection { background-color: ${config.primaryColor}; color: white; }
      `}</style>

      {/* Edit Mode Modal */}
      <AnimatePresence>
        {isEditing && (
          <ConfigModal 
            currentConfig={config} 
            analyticsData={analyticsData}
            onSave={handleSaveConfig} 
            onSync={handleSyncCloud}
            onClose={() => setIsEditing(false)} 
            isDarkMode={isDarkMode} 
          />
        )}
      </AnimatePresence>

      <main className={`max-w-md mx-auto sm:shadow-2xl sm:border sm:rounded-2xl overflow-hidden relative transition-colors duration-500 ${t.cardBg} ${t.border}`}>
        
        {/* Top Controls */}
        <div className="absolute top-4 right-4 z-20 flex items-center gap-2">
          {/* Edit Button */}
          <button 
            onClick={() => setIsEditing(true)} 
            className={`p-2 rounded-full backdrop-blur-md border transition-all duration-300 active:scale-95 flex items-center justify-center w-9 h-9 ${
              isDarkMode 
                ? 'bg-black/40 border-white/10 text-white/80 hover:text-white hover:bg-black/60' 
                : 'bg-white/60 border-black/10 text-zinc-700 hover:text-black hover:bg-white/80 shadow-sm'
            }`}
            aria-label="Edit Profile"
          >
            <Edit size={14} />
          </button>
          {/* Language Toggle */}
          <button 
            onClick={toggleLanguage} 
            className={`p-2 rounded-full backdrop-blur-md border transition-all duration-300 active:scale-95 flex items-center justify-center font-semibold text-xs w-9 h-9 ${
              isDarkMode 
                ? 'bg-black/40 border-white/10 text-white/80 hover:text-white hover:bg-black/60' 
                : 'bg-white/60 border-black/10 text-zinc-700 hover:text-black hover:bg-white/80 shadow-sm'
            }`}
            aria-label="Toggle language"
          >
            {lang.toUpperCase()}
          </button>

          {/* Theme Toggle */}
          <button 
            onClick={() => setIsDarkMode(!isDarkMode)} 
            className={`p-2 rounded-full backdrop-blur-md border transition-all duration-300 active:scale-95 flex items-center justify-center w-9 h-9 ${
              isDarkMode 
                ? 'bg-black/40 border-white/10 text-white/80 hover:text-white hover:bg-black/60' 
                : 'bg-white/60 border-black/10 text-zinc-700 hover:text-black hover:bg-white/80 shadow-sm'
            }`}
            aria-label="Toggle theme"
          >
            {isDarkMode ? <Sun size={16} /> : <Moon size={16} />}
          </button>
        </div>

        {/* Status Indicator */}
        <div className="absolute top-5 left-5 z-20 flex items-center gap-2">
          <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full backdrop-blur-md border text-xs font-medium tracking-wide ${
            isDarkMode 
              ? 'bg-black/40 border-white/10 text-white/90' 
              : 'bg-white/60 border-black/10 text-zinc-800 shadow-sm'
          }`}>
            <span className="relative flex h-2.5 w-2.5">
              {isOnline && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>}
              <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${isOnline ? 'bg-emerald-500' : 'bg-zinc-400'}`}></span>
            </span>
            {isOnline ? content.available : content.away}
          </div>
        </div>
        
        {/* Header / Hero Section */}
        <motion.section 
          className="relative"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className={`absolute inset-0 bg-gradient-to-b z-0 transition-colors duration-500 ${t.gradientTop}`}>
             <div className={`absolute inset-0 ${isDarkMode ? 'opacity-10' : 'opacity-5 mix-blend-multiply'}`}
                  style={{
                    backgroundImage: `url('${config.bgImage}')`, 
                    backgroundSize: 'cover', 
                    backgroundPosition: 'center'
                  }} />
          </div>
          
          <div className="relative z-10 pt-20 pb-8 px-6 flex flex-col items-center text-center">
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className={`w-32 h-32 rounded-full border-2 p-1 mb-6 shadow-xl theme-border ${isDarkMode ? 'bg-zinc-950' : 'bg-white'}`}
            >
              <div className="w-full h-full rounded-full overflow-hidden bg-zinc-800">
                <img 
                  src={config.profileImage} 
                  alt={config.name} 
                  className="w-full h-full object-cover object-top"
                />
              </div>
            </motion.div>
            
            <motion.h1 
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className={`text-3xl font-light tracking-wide mb-1 transition-colors duration-500 ${t.textPrimary}`}
            >
              {config.name}
            </motion.h1>
            <motion.p 
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="font-medium text-sm tracking-wider uppercase mb-1 theme-text"
            >
              {config.title}
            </motion.p>
            <motion.p 
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className={`text-sm mb-6 transition-colors duration-500 ${t.textSecondary}`}
            >
              {config.company}
            </motion.p>
            
            <motion.div 
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              className={`w-12 h-[1px] mb-6 origin-center transition-colors duration-500 ${t.divider}`}
            ></motion.div>
            
            <motion.p 
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.7 }}
              className={`text-lg font-light italic px-4 leading-relaxed transition-colors duration-500 ${isDarkMode ? 'text-zinc-100' : 'text-zinc-800'}`}
            >
              {config.heroTagline}
            </motion.p>
          </div>
        </motion.section>

        {/* Action Buttons (Share, Save, Calendar) */}
        <motion.section 
          className="px-6 pb-6 pt-2"
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
        >
          <div className="grid grid-cols-2 gap-3 mb-3">
            <motion.button
              variants={fadeInUp}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleShare}
              className={`flex items-center justify-center gap-2 py-3 px-4 rounded-xl border border-transparent theme-text theme-shadow theme-hover-bg transition-all duration-300 text-sm font-medium tracking-wide shadow-md ${isDarkMode ? 'bg-[#18181b]' : 'bg-white'}`}
            >
              <Share2 size={16} />
              {content.shareProfile}
            </motion.button>
            
            <motion.button
              variants={fadeInUp}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSaveContact}
              className={`flex items-center justify-center gap-2 py-3 px-4 rounded-xl border transition-all duration-300 text-sm font-medium tracking-wide ${t.btnBg} ${t.btnBorder} ${isDarkMode ? 'text-zinc-300' : 'text-zinc-700'} ${t.btnHover}`}
            >
              <Download size={16} />
              {content.saveContact}
            </motion.button>
          </div>

          <motion.button
              variants={fadeInUp}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.97 }}
              onClick={handleAddToCalendar}
              className={`w-full mb-4 flex items-center justify-center gap-2 py-3 px-4 rounded-xl border transition-all duration-300 text-sm font-medium tracking-wide ${t.btnBg} ${t.btnBorder} ${isDarkMode ? 'text-zinc-300' : 'text-zinc-700'} ${t.btnHover}`}
            >
              <Calendar size={16} className="theme-text" />
              {content.addCalendar}
          </motion.button>

          <div className="grid grid-cols-3 gap-3">
            <motion.div variants={fadeInUp}>
              <ActionButton 
                href={`tel:${config.phone}`} 
                icon={<Phone size={20} />} 
                label={content.call}
                t={t}
                isDarkMode={isDarkMode}
              />
            </motion.div>
            <motion.div variants={fadeInUp}>
              <ActionButton 
                href={`https://wa.me/${config.whatsapp.replace('+', '')}`} 
                icon={<MessageCircle size={20} />} 
                label={content.whatsapp}
                t={t}
                isDarkMode={isDarkMode}
              />
            </motion.div>
            <motion.div variants={fadeInUp}>
              <ActionButton 
                href={`mailto:${config.email}`} 
                icon={<Mail size={20} />} 
                label={content.email}
                t={t}
                isDarkMode={isDarkMode}
              />
            </motion.div>
          </div>
        </motion.section>

        <div className={`w-full h-[1px] transition-colors duration-500 ${isDarkMode ? 'bg-gradient-to-r from-zinc-950 via-zinc-800 to-zinc-950' : 'bg-gradient-to-r from-stone-50 via-stone-200 to-stone-50'}`}></div>

        {/* About Section */}
        <motion.section 
          className="px-6 py-10"
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <SectionTitle t={t}>{content.aboutTitle}</SectionTitle>
          <p className={`text-sm leading-relaxed mb-4 font-light transition-colors duration-500 ${t.textSecondary}`}>
            {config.aboutP1}
          </p>
          <p className={`text-sm leading-relaxed font-light transition-colors duration-500 ${t.textSecondary}`}>
            {config.aboutP2}
          </p>
        </motion.section>

        {/* Services Section */}
        <motion.section 
          className={`px-6 py-8 transition-colors duration-500 ${t.sectionBg}`}
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <SectionTitle t={t}>{content.servicesTitle}</SectionTitle>
          <ul className="space-y-4">
            <ServiceItem t={t} icon={<Car size={18} />} title={content.service1Title} desc={content.service1Desc} />
            <ServiceItem t={t} icon={<CheckCircle size={18} />} title={content.service2Title} desc={content.service2Desc} />
            <ServiceItem t={t} icon={<svg className="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>} title={content.service3Title} desc={content.service3Desc} />
            <ServiceItem t={t} icon={<svg className="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>} title={content.service4Title} desc={content.service4Desc} />
          </ul>
        </motion.section>

        {/* Experience Section */}
        <motion.section 
          className="px-6 py-10"
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <SectionTitle t={t}>{content.expTitle}</SectionTitle>
          <div className="grid grid-cols-1 gap-4">
            <CredentialBadge t={t} text={content.exp1} isDarkMode={isDarkMode} />
            <CredentialBadge t={t} text={content.exp2} isDarkMode={isDarkMode} />
            <CredentialBadge t={t} text={content.exp3} isDarkMode={isDarkMode} />
          </div>
        </motion.section>

        <div className={`w-full h-[1px] transition-colors duration-500 ${isDarkMode ? 'bg-gradient-to-r from-zinc-950 via-zinc-800 to-zinc-950' : 'bg-gradient-to-r from-stone-50 via-stone-200 to-stone-50'}`}></div>

        {/* Testimonials Carousel */}
        <motion.section 
          className={`px-6 py-10 transition-colors duration-500 ${t.sectionBg}`}
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <SectionTitle t={t}>{content.testTitle}</SectionTitle>
          <div className="relative">
            <div className="overflow-hidden">
              <AnimatePresence mode="wait">
                <motion.div
                  key={currentTestimonial}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className={`p-6 rounded-xl border transition-colors duration-500 ${t.btnBg} ${t.btnBorder}`}
                >
                  <div className="theme-text mb-3">
                    <Quote size={24} fill="currentColor" className="opacity-80" />
                  </div>
                  <p className={`text-sm italic mb-4 leading-relaxed transition-colors duration-500 ${isDarkMode ? 'text-zinc-300' : 'text-zinc-700'}`}>
                    "{testimonials[currentTestimonial].text}"
                  </p>
                  <div>
                    <p className={`text-sm font-medium transition-colors duration-500 ${t.textPrimary}`}>{testimonials[currentTestimonial].author}</p>
                    <p className="text-xs theme-text">{testimonials[currentTestimonial].role}</p>
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>
            
            <div className="flex justify-center gap-2 mt-5">
              {testimonials.map((_, idx) => (
                <button 
                  key={idx}
                  onClick={() => setCurrentTestimonial(idx)}
                  style={currentTestimonial === idx ? { backgroundColor: config.primaryColor, width: '16px' } : {}}
                  className={`w-2 h-2 rounded-full transition-all duration-300 ${currentTestimonial === idx ? '' : (isDarkMode ? 'bg-zinc-700 hover:bg-zinc-600' : 'bg-stone-300 hover:bg-stone-400')}`}
                  aria-label={`Go to testimonial ${idx + 1}`}
                />
              ))}
            </div>
          </div>
        </motion.section>

        <div className={`w-full h-[1px] transition-colors duration-500 ${isDarkMode ? 'bg-gradient-to-r from-zinc-950 via-zinc-800 to-zinc-950' : 'bg-gradient-to-r from-stone-50 via-stone-200 to-stone-50'}`}></div>

        {/* FAQ Section */}
        <motion.section 
          className="px-6 py-10"
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <SectionTitle t={t}>{content.faqTitle}</SectionTitle>
          <div className="space-y-3">
            {faqs.map((faq, idx) => (
              <div 
                key={idx} 
                className={`border rounded-xl overflow-hidden transition-colors duration-300 ${t.btnBorder} ${isDarkMode ? 'bg-zinc-900/50' : 'bg-white'}`}
              >
                <button
                  onClick={() => setOpenFaq(openFaq === idx ? null : idx)}
                  className="w-full px-4 py-4 flex items-center justify-between text-left focus:outline-none"
                >
                  <span className={`text-sm font-medium transition-colors duration-300 ${t.textPrimary}`}>
                    {faq.q}
                  </span>
                  <motion.div
                    animate={{ rotate: openFaq === idx ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                    className="theme-text shrink-0 ml-2"
                  >
                    <ChevronDown size={18} />
                  </motion.div>
                </button>
                <AnimatePresence>
                  {openFaq === idx && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className={`px-4 pb-4 pt-1 text-sm font-light leading-relaxed transition-colors duration-300 ${t.textSecondary}`}>
                        {faq.a}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </div>
        </motion.section>

        <div className={`w-full h-[1px] transition-colors duration-500 ${isDarkMode ? 'bg-gradient-to-r from-zinc-950 via-zinc-800 to-zinc-950' : 'bg-gradient-to-r from-stone-50 via-stone-200 to-stone-50'}`}></div>

        {/* Contact Form Section */}
        <motion.section 
          className={`px-6 py-10 transition-colors duration-500 ${t.sectionBg}`}
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <SectionTitle t={t}>{content.contactTitle}</SectionTitle>
          <form onSubmit={handleSendMessage} className="space-y-4">
            <div>
              <input 
                type="text" 
                value={formName}
                onChange={(e) => setFormName(e.target.value)}
                required
                placeholder={content.contactName}
                className={`w-full px-4 py-3 rounded-xl border text-sm transition-colors duration-300 ${t.inputBg} ${t.inputBorder} ${t.textPrimary} placeholder:text-zinc-500`}
              />
            </div>
            <div>
              <textarea 
                value={formMessage}
                onChange={(e) => setFormMessage(e.target.value)}
                required
                placeholder={content.contactMessage}
                rows={4}
                className={`w-full px-4 py-3 rounded-xl border text-sm transition-colors duration-300 resize-none ${t.inputBg} ${t.inputBorder} ${t.textPrimary} placeholder:text-zinc-500`}
              />
            </div>
            <motion.button 
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl theme-bg text-white hover:opacity-90 transition-all duration-300 text-sm font-medium tracking-wide shadow-md"
            >
              <Send size={16} />
              {content.contactSend}
            </motion.button>
          </form>
        </motion.section>

        <div className={`w-full h-[1px] transition-colors duration-500 ${isDarkMode ? 'bg-gradient-to-r from-zinc-950 via-zinc-800 to-zinc-950' : 'bg-gradient-to-r from-stone-50 via-stone-200 to-stone-50'}`}></div>

        {/* Location & Hours */}
        <motion.section 
          className="px-6 py-10"
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <SectionTitle t={t}>{content.visitTitle}</SectionTitle>
          
          <div className={`border rounded-xl p-5 mb-6 transition-colors duration-500 ${t.btnBg} ${t.btnBorder}`}>
            <div className="flex items-start gap-4 mb-4">
              <div className={`p-2 rounded-lg theme-text shrink-0 transition-colors duration-500 ${isDarkMode ? 'bg-zinc-800' : 'bg-stone-100'}`}>
                <MapPin size={20} />
              </div>
              <div className="flex-1">
                <h4 className={`font-medium text-sm mb-1 transition-colors duration-500 ${t.textPrimary}`}>{config.company}</h4>
                <p className={`text-sm font-light leading-relaxed transition-colors duration-500 ${t.textSecondary}`}>
                  {config.address}
                </p>
                <div className="flex items-center gap-4 mt-3">
                  <a 
                    href={`https://maps.google.com/?q=${encodeURIComponent(config.company + " " + config.address)}`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 theme-text theme-hover-text text-sm transition-colors"
                  >
                    <Navigation size={14} /> {content.directions}
                  </a>
                  <button 
                    onClick={() => setShowMap(!showMap)}
                    className="inline-flex items-center gap-1 theme-text theme-hover-text text-sm transition-colors"
                  >
                    {showMap ? <ChevronUp size={14} /> : <Map size={14} />} {showMap ? content.hideMap : content.viewMap}
                  </button>
                </div>
              </div>
            </div>
            
            <AnimatePresence>
              {showMap && (
                <motion.div 
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="pt-2 pb-4">
                    <div className="w-full h-48 rounded-lg overflow-hidden border theme-border shadow-inner">
                      <iframe 
                        src={`https://www.google.com/maps?q=${encodeURIComponent(config.company + " " + config.address)}&output=embed`}
                        width="100%" 
                        height="100%" 
                        style={{ border: 0 }} 
                        allowFullScreen={false}
                        loading="lazy"
                        title="Map Location"
                      ></iframe>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
            
            <div className={`w-full h-[1px] my-4 transition-colors duration-500 ${t.divider}`}></div>
            
            <div className="flex items-start gap-4">
              <div className={`p-2 rounded-lg theme-text shrink-0 transition-colors duration-500 ${isDarkMode ? 'bg-zinc-800' : 'bg-stone-100'}`}>
                <Clock size={20} />
              </div>
              <div>
                <h4 className={`font-medium text-sm mb-1 transition-colors duration-500 ${t.textPrimary}`}>{content.businessHours}</h4>
                <p className={`text-sm font-light leading-relaxed transition-colors duration-500 ${t.textSecondary}`}>
                  {config.hoursMonFri}<br />
                  {config.hoursSat}<br />
                  {config.hoursSun}
                </p>
              </div>
            </div>
          </div>
        </motion.section>

        {/* QR Code Section */}
        <motion.section 
          className={`px-6 py-8 flex flex-col items-center border-t transition-colors duration-500 ${isDarkMode ? 'bg-zinc-950 border-zinc-900' : 'bg-stone-50 border-stone-200'}`}
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, margin: "-50px" }}
        >
          <div className="mb-4 text-center">
            <h4 className={`font-medium text-sm mb-1 flex items-center justify-center gap-2 transition-colors duration-500 ${t.textPrimary}`}>
              <QrCode size={16} className="theme-text" /> {content.scanTitle}
            </h4>
            <p className={`text-xs font-light transition-colors duration-500 ${t.textSecondary}`}>{content.scanDesc}</p>
          </div>
          <div className="bg-white p-3 rounded-xl shadow-lg inline-block">
            <QRCode 
              value={typeof window !== 'undefined' ? window.location.href : 'https://www.rangerovercentre.co.ke'}
              size={120}
              level="M"
              fgColor="#09090b"
              bgColor="#ffffff"
            />
          </div>
        </motion.section>

        {/* Social Links */}
        <motion.section 
          className="px-6 pt-6 pb-10 flex justify-center gap-6"
          variants={fadeInUp}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
        >
          <SocialLink href={config.facebook} icon={<Facebook size={22} />} t={t} isDarkMode={isDarkMode} />
          <SocialLink href={config.instagram} icon={<Instagram size={22} />} t={t} isDarkMode={isDarkMode} />
        </motion.section>

        {/* Footer */}
        <footer className={`py-8 px-6 text-center border-t transition-colors duration-500 ${isDarkMode ? 'bg-zinc-950 border-zinc-900' : 'bg-stone-100 border-stone-200'}`}>
          <p className="text-zinc-500 text-xs font-light mb-2 uppercase tracking-wider hover:text-zinc-400 transition-colors">
            <a href="https://rangerovercentre.co.ke/" target="_blank" rel="noopener noreferrer">{config.company}</a>
          </p>
          <p className="text-zinc-500 text-xs font-light mb-4">
            &copy; {new Date().getFullYear()} {config.name}. All rights reserved.
          </p>
          
          <div className="flex items-center justify-center gap-1 text-zinc-600 text-[10px] uppercase tracking-widest mt-6">
            <Eye size={12} />
            <span>{pageViews.toLocaleString()} views</span>
          </div>
        </footer>

        {/* Back to Top Button */}
        <AnimatePresence>
          {showBackToTop && (
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              onClick={scrollToTop}
              className="fixed bottom-6 right-6 z-50 p-3 rounded-full theme-bg text-white shadow-lg transition-all active:scale-95 sm:absolute hover:opacity-90"
              aria-label="Back to top"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <ArrowUp size={20} />
            </motion.button>
          )}
        </AnimatePresence>

      </main>
    </div>
  );
}

// Subcomponents

function ConfigModal({ currentConfig, analyticsData, onSave, onSync, onClose, isDarkMode }: any) {
  const [formData, setFormData] = useState(currentConfig);
  const [activeTab, setActiveTab] = useState<'profile' | 'theme' | 'analytics'>('profile');
  
  const [cropTarget, setCropTarget] = useState<'profileImage' | 'bgImage' | null>(null);
  const [cropImageSrc, setCropImageSrc] = useState<string>('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
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

  const t = {
    bg: isDarkMode ? "bg-zinc-900 border-zinc-800" : "bg-white border-stone-200",
    textPrimary: isDarkMode ? "text-white" : "text-zinc-900",
    textSecondary: isDarkMode ? "text-zinc-400" : "text-zinc-600",
    inputBg: isDarkMode ? "bg-zinc-950" : "bg-stone-50",
    inputBorder: isDarkMode ? "border-zinc-800" : "border-stone-200",
    tabBg: isDarkMode ? "bg-zinc-800" : "bg-stone-200",
    tabActive: isDarkMode ? "bg-zinc-700" : "bg-white shadow-sm",
  };

  return (
    <>
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] bg-black/80 flex items-center justify-center p-4 overflow-y-auto"
      >
        <motion.div 
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.95, opacity: 0 }}
          className={`w-full max-w-lg rounded-xl overflow-hidden shadow-2xl border flex flex-col max-h-[90vh] ${t.bg}`}
        >
          <div className="flex items-center justify-between p-4 border-b border-inherit bg-inherit z-10">
            <h2 className={`text-lg font-medium ${t.textPrimary}`}>Settings</h2>
            <div className="flex items-center gap-2">
              <button 
                onClick={() => onSync(formData)}
                title="Sync to Cloud"
                className="p-2 rounded-full hover:bg-zinc-500/20 text-[#c5a059] transition-colors"
              >
                <Cloud size={20} />
              </button>
              <button onClick={onClose} className="p-2 rounded-full hover:bg-black/10 transition-colors">
                <X size={20} className={t.textPrimary} />
              </button>
            </div>
          </div>
          
          <div className="px-4 pt-4 pb-2 border-b border-inherit">
            <div className={`flex p-1 rounded-lg ${t.tabBg}`}>
              <button 
                onClick={() => setActiveTab('profile')}
                className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-all ${activeTab === 'profile' ? t.tabActive + ' ' + t.textPrimary : t.textSecondary}`}
              >
                Profile
              </button>
              <button 
                onClick={() => setActiveTab('theme')}
                className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-all ${activeTab === 'theme' ? t.tabActive + ' ' + t.textPrimary : t.textSecondary}`}
              >
                Theme
              </button>
              <button 
                onClick={() => setActiveTab('analytics')}
                className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-all ${activeTab === 'analytics' ? t.tabActive + ' ' + t.textPrimary : t.textSecondary}`}
              >
                Analytics
              </button>
            </div>
          </div>

          <div className="p-6 overflow-y-auto space-y-4">
            
            {activeTab === 'profile' && (
              <>
                <ConfigInput label="Name" name="name" value={formData.name} onChange={handleChange} t={t} />
                <ConfigInput label="Title" name="title" value={formData.title} onChange={handleChange} t={t} />
                <ConfigInput label="Company" name="company" value={formData.company} onChange={handleChange} t={t} />
                <ConfigInput label="Hero Tagline" name="heroTagline" value={formData.heroTagline} onChange={handleChange} t={t} />
                
                <ConfigInput label="Phone" name="phone" value={formData.phone} onChange={handleChange} t={t} />
                <ConfigInput label="WhatsApp" name="whatsapp" value={formData.whatsapp} onChange={handleChange} t={t} />
                <ConfigInput label="Email" name="email" value={formData.email} onChange={handleChange} t={t} />
                <ConfigInput label="Address" name="address" value={formData.address} onChange={handleChange} t={t} />
                <ConfigInput label="Instagram URL" name="instagram" value={formData.instagram} onChange={handleChange} t={t} />
                <ConfigInput label="Facebook URL" name="facebook" value={formData.facebook} onChange={handleChange} t={t} />
                
                <div>
                  <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 1)</label>
                  <textarea 
                    name="aboutP1"
                    value={formData.aboutP1}
                    onChange={handleChange}
                    rows={3}
                    className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                  />
                </div>
                <div>
                  <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>About Me (Paragraph 2)</label>
                  <textarea 
                    name="aboutP2"
                    value={formData.aboutP2}
                    onChange={handleChange}
                    rows={3}
                    className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                  />
                </div>
              </>
            )}

            {activeTab === 'theme' && (
              <>
                <div className="mb-4">
                  <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Primary Accent Color</label>
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

                <div className="mb-4 border-t border-inherit pt-4">
                  <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Profile Image</label>
                  <div className="flex gap-2 mb-2">
                    <input 
                      type="text" 
                      name="profileImage"
                      value={formData.profileImage}
                      onChange={handleChange}
                      placeholder="Image URL"
                      className={`flex-1 px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                    />
                    <label className={`flex items-center justify-center px-3 py-2 rounded-lg border cursor-pointer hover:opacity-80 ${t.inputBorder} ${t.inputBg}`}>
                      <Upload size={16} className={t.textSecondary} />
                      <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e, 'profileImage')} />
                    </label>
                  </div>
                  {formData.profileImage && (
                    <img src={formData.profileImage} alt="Profile preview" className="w-16 h-16 rounded-full object-cover border-2 border-inherit" />
                  )}
                </div>

                <div className="mb-4 border-t border-inherit pt-4">
                  <label className={`block text-xs font-medium mb-2 ${t.textPrimary} opacity-80`}>Background Image</label>
                  <div className="flex gap-2 mb-2">
                    <input 
                      type="text" 
                      name="bgImage"
                      value={formData.bgImage}
                      onChange={handleChange}
                      placeholder="Image URL"
                      className={`flex-1 px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                    />
                    <label className={`flex items-center justify-center px-3 py-2 rounded-lg border cursor-pointer hover:opacity-80 ${t.inputBorder} ${t.inputBg}`}>
                      <Upload size={16} className={t.textSecondary} />
                      <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e, 'bgImage')} />
                    </label>
                  </div>
                  {formData.bgImage && (
                    <img src={formData.bgImage} alt="Background preview" className="w-full h-20 rounded-lg object-cover border border-inherit" />
                  )}
                </div>

                <div className="mb-4 border-t border-inherit pt-4">
                  <label className={`block text-xs font-medium mb-1 ${t.textPrimary} opacity-80`}>WhatsApp Auto-Fill Template</label>
                  <p className={`text-[10px] mb-2 ${t.textSecondary}`}>Variables: {'{name}'}, {'{message}'}</p>
                  <textarea 
                    name="whatsappTemplate"
                    value={formData.whatsappTemplate}
                    onChange={handleChange}
                    rows={4}
                    className={`w-full px-3 py-2 rounded-lg border text-sm focus:outline-none transition-colors duration-300 ${t.inputBg} ${t.inputBorder} theme-ring ${t.textPrimary}`}
                  />
                </div>
              </>
            )}

            {activeTab === 'analytics' && (
              <div className="py-2">
                <h3 className={`text-sm font-medium mb-4 ${t.textPrimary}`}>Daily Profile Views (Last 7 Days)</h3>
                <div className="w-full h-48">
                  {analyticsData.length > 0 ? (
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
            )}
            
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

      {/* Crop Modal rendered on top if needed */}
      {cropTarget && cropImageSrc && (
        <CropModal 
          imageSrc={cropImageSrc}
          aspectRatio={cropTarget === 'profileImage' ? 1 : 16/9}
          isDarkMode={isDarkMode}
          onClose={() => {
            setCropTarget(null);
            setCropImageSrc('');
          }}
          onCropComplete={(croppedBase64) => {
            setFormData({ ...formData, [cropTarget]: croppedBase64 });
            setCropTarget(null);
            setCropImageSrc('');
          }}
        />
      )}
    </>
  );
}

function ConfigInput({ label, name, value, onChange, t }: any) {
  return (
    <div>
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
}

function SectionTitle({ children, t }: { children: ReactNode, t: any }) {
  return (
    <h3 className={`text-lg font-medium tracking-wide mb-6 flex items-center gap-3 transition-colors duration-500 ${t.textPrimary}`}>
      {children}
      <div className={`flex-1 h-[1px] transition-colors duration-500 ${t.divider}`}></div>
    </h3>
  );
}

function ActionButton({ href, icon, label, t, isDarkMode }: { href: string, icon: ReactNode, label: string, t: any, isDarkMode: boolean }) {
  return (
    <motion.a 
      href={href}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`flex flex-col items-center justify-center py-3 px-2 rounded-xl border transition-colors duration-300 ${t.btnBg} ${t.btnBorder} ${isDarkMode ? 'text-zinc-300' : 'text-zinc-700'} theme-hover-border`}
    >
      <div className="mb-2 theme-text">{icon}</div>
      <span className="text-xs font-medium tracking-wide">{label}</span>
    </motion.a>
  );
}

function ServiceItem({ icon, title, desc, t }: { icon: ReactNode, title: string, desc: string, t: any }) {
  return (
    <li className={`flex items-start gap-4 p-3 rounded-lg transition-colors duration-300 ${t.btnHover}`}>
      <div className="theme-text mt-0.5">{icon}</div>
      <div>
        <h4 className={`text-sm font-medium mb-1 transition-colors duration-500 ${t.textPrimary}`}>{title}</h4>
        <p className={`text-xs font-light leading-relaxed transition-colors duration-500 ${t.textSecondary}`}>{desc}</p>
      </div>
    </li>
  );
}

function CredentialBadge({ text, t, isDarkMode }: { text: string, t: any, isDarkMode: boolean }) {
  return (
    <div className={`flex items-center gap-3 border rounded-lg p-3 transition-colors duration-500 ${isDarkMode ? 'bg-zinc-900/50 border-zinc-800' : 'bg-white border-stone-200'}`}>
      <Award size={16} className="theme-text shrink-0" />
      <span className={`text-sm font-light transition-colors duration-500 ${isDarkMode ? 'text-zinc-300' : 'text-zinc-700'}`}>{text}</span>
    </div>
  );
}

function SocialLink({ href, icon, t, isDarkMode }: { href: string, icon: ReactNode, t: any, isDarkMode: boolean }) {
  return (
    <motion.a 
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      whileHover={{ scale: 1.15, rotate: 5 }}
      whileTap={{ scale: 0.9 }}
      className={`w-12 h-12 rounded-full border flex items-center justify-center transition-colors ${t.btnBg} ${t.btnBorder} ${isDarkMode ? 'text-zinc-400' : 'text-zinc-500'} theme-hover-border theme-hover-text`}
    >
      {icon}
    </motion.a>
  );
}
