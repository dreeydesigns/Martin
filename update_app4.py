import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

default_config_old = r"""const defaultConfig = \{
  bgImage: "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a\?q=80&w=1000&auto=format&fit=crop",
  profileImage: "https://storage.googleapis.com/aistudio-dev-uploads/e0fb3af3-2e0f-4886-acbc-992a5435e165.jpeg",
  primaryColor: "#c5a059",
  name: "Martin Mwihoti",
  title: "Sales & Marketing Manager",
  company: "Range Rover Centre Ltd",
  phone: "\+254704183358",
  whatsapp: "\+254704183358",
  whatsappTemplate: "Hi Martin, I'm \{name\}\\n\\n\{message\}",
  email: "mmwihoti@gmail.com",
  address: "Kiambu Road, 00100, Nairobi, Kenya",
  instagram: "https://www.instagram.com/m.mwihoti_/",
  facebook: "https://www.facebook.com/p/Range-Rover-Centre-Motors-61574959497030/",
  hoursMonFri: "Mon-Fri: 8:00 AM - 5:00 PM",
  hoursSat: "Saturday: 9:00 AM - 1:00 PM",
  hoursSun: "Sunday: Closed",
  heroTagline: "\\"Dealer in Landrover, Range Rover and Discovery. Imports, Insurance, Local Re-sale, Parts and Repairs.\\"",
  aboutP1: "With over a decade of experience in automotive sales, I specialize in matching clients with the perfect Land Rover or Range Rover to suit their lifestyle.",
  aboutP2: "As the Sales & Marketing Manager at Range Rover Centre Ltd, my approach is built on transparency, personalized service, and a deep passion for the heritage of the brand. Whether you are exploring our latest models or seeking a certified pre-owned vehicle, I am committed to making your ownership journey seamless and rewarding.",
  statusOverride: "auto"
\};"""

default_config_new = r"""const defaultConfig = {
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
  heroTagline: "\"Dealer in Landrover, Range Rover and Discovery. Imports, Insurance, Local Re-sale, Parts and Repairs.\"",
  aboutP1: "With over a decade of experience in automotive sales, I specialize in matching clients with the perfect Land Rover or Range Rover to suit their lifestyle.",
  aboutP2: "As the Sales & Marketing Manager at Range Rover Centre Ltd, my approach is built on transparency, personalized service, and a deep passion for the heritage of the brand. Whether you are exploring our latest models or seeking a certified pre-owned vehicle, I am committed to making your ownership journey seamless and rewarding.",
  statusOverride: "auto",
  operatingHours: {
    1: { enabled: true, start: "08:00", end: "17:00" }, // Mon
    2: { enabled: true, start: "08:00", end: "17:00" }, // Tue
    3: { enabled: true, start: "08:00", end: "17:00" }, // Wed
    4: { enabled: true, start: "08:00", end: "17:00" }, // Thu
    5: { enabled: true, start: "08:00", end: "17:00" }, // Fri
    6: { enabled: true, start: "09:00", end: "13:00" }, // Sat
    0: { enabled: false, start: "09:00", end: "17:00" }, // Sun
  }
};"""
content = re.sub(default_config_old, default_config_new, content, flags=re.DOTALL)

# Update checkStatus function
check_status_old = r"""const checkStatus = \(\) => \{
      if \(config.statusOverride === 'available'\) \{
        setIsOnline\(true\);
        return;
      \}
      if \(config.statusOverride === 'away'\) \{
        setIsOnline\(false\);
        return;
      \}
      const now = new Date\(\);
      const nairobiTime = new Date\(now.toLocaleString\("en-US", \{timeZone: "Africa/Nairobi"\}\)\);
      const day = nairobiTime.getDay\(\);
      const hour = nairobiTime.getHours\(\);

      let online = false;
      if \(day >= 1 && day <= 5\) \{
        if \(hour >= 8 && hour < 17\) online = true;
      \} else if \(day === 6\) \{
        if \(hour >= 9 && hour < 13\) online = true;
      \}
      setIsOnline\(online\);
    \};"""

check_status_new = r"""const checkStatus = () => {
      if (config.statusOverride === 'available') {
        setIsOnline(true);
        return;
      }
      if (config.statusOverride === 'away') {
        setIsOnline(false);
        return;
      }
      const now = new Date();
      const nairobiTime = new Date(now.toLocaleString("en-US", {timeZone: "Africa/Nairobi"}));
      const day = nairobiTime.getDay();
      const hour = nairobiTime.getHours();
      const minutes = nairobiTime.getMinutes();
      const currentMinutes = hour * 60 + minutes;

      let online = false;
      const todayHours = config.operatingHours?.[day];
      if (todayHours && todayHours.enabled) {
        const [startH, startM] = todayHours.start.split(':').map(Number);
        const [endH, endM] = todayHours.end.split(':').map(Number);
        const startTotal = startH * 60 + startM;
        const endTotal = endH * 60 + endM;
        if (currentMinutes >= startTotal && currentMinutes < endTotal) {
          online = true;
        }
      }
      setIsOnline(online);
    };"""
content = re.sub(check_status_old, check_status_new, content, flags=re.DOTALL)

with open('src/App.tsx', 'w') as f:
    f.write(content)
