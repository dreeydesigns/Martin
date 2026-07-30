import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

hours_old = r"""<li>\{config.hoursMonFri\}</li>\s*<li>\{config.hoursSat\}</li>\s*<li>\{config.hoursSun\}</li>"""
hours_new = r"""{['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map((dayName, idx) => {
                      const dIdx = idx === 6 ? 0 : idx + 1;
                      const h = config.operatingHours?.[dIdx];
                      if (!h) return null;
                      return (
                        <li key={dayName} className="flex justify-between gap-4">
                          <span>{dayName}</span>
                          <span>{h.enabled ? `${h.start} - ${h.end}` : 'Closed'}</span>
                        </li>
                      );
                    })}"""
content = re.sub(hours_old, hours_new, content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
