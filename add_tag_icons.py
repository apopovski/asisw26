#!/usr/bin/env python3
import re

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Icon mapping - tag name -> SVG
icons = {
    'Meal Tickets': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M3 3h18v7.5c0 1.1-.9 2-2 2h-2v2h2c1.1 0 2 .9 2 2V21H3v-4.5c0-1.1.9-2 2-2h2v-2H5c-1.1 0-2-.9-2-2V3z" fill="currentColor"/>
    </svg>''',
    
    'Dinner': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M11 9H9V3H7v6H5V3H3v14c0 2.12 1.66 3.84 3.75 3.97V23h2.5v-2.03C15.34 20.84 17 19.12 17 17V3h-2v6h-2V3h-2v6z" fill="currentColor"/>
    </svg>''',
    
    'Breakfast': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M11 9H9V3H7v6H5V3H3v14c0 2.12 1.66 3.84 3.75 3.97V23h2.5v-2.03C15.34 20.84 17 19.12 17 17V3h-2v6h-2V3h-2v6z" fill="currentColor"/>
    </svg>''',
    
    'Lunch': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M11 9H9V3H7v6H5V3H3v14c0 2.12 1.66 3.84 3.75 3.97V23h2.5v-2.03C15.34 20.84 17 19.12 17 17V3h-2v6h-2V3h-2v6z" fill="currentColor"/>
    </svg>''',
    
    'Exhibits Open': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M13 13h-2v-2h2v2zm0-6h-2V5h2v2zm6 0h-2V5h2v2zM7 13H5v-2h2v2zm12-7h-1V4c0-.55-.45-1-1-1h-4c-.55 0-1 .45-1 1v1H9V4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v1H2v2h2v10c0 .55.45 1 1 1h14c.55 0 1-.45 1-1V8h2V6zM4 8h16v10H4V8zm9 2h-2v2h2v-2z" fill="currentColor"/>
    </svg>''',
    
    'Prayer Time': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M7.5 5C5.57 5 4 6.57 4 8.5c0 2.03 1.34 3.78 3.14 4.32.47.54.83 1.15 1.04 1.82.21.65.33 1.33.33 2.04 0 .93-.16 1.83-.47 2.67.68.62 1.56 1 2.5 1s1.82-.38 2.5-1c-.31-.84-.47-1.74-.47-2.67 0-.71.12-1.38.33-2.04.22-.67.57-1.28 1.04-1.82 1.8-.54 3.14-2.29 3.14-4.32 0-1.93-1.57-3.5-3.5-3.5z" fill="currentColor"/>
    </svg>''',
    
    'Speaker': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z" fill="currentColor"/>
    </svg>''',
    
    'Seminar 1': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M5 13.18c0 .65.13 1.29.38 1.93L2.85 16.7c-.53-1.02-.99-2.11-1.33-3.26h.01c-.35-1.24-.52-2.54-.52-3.9 0-1.36.17-2.66.52-3.9H1.52c.34-1.15.8-2.24 1.33-3.26l2.53 1.59c-.25.64-.38 1.28-.38 1.93 0 2.13 1.26 3.96 3.06 4.77l-1.89 3.15c-.71-.41-1.33-.95-1.86-1.59z" fill="currentColor"/>
      <path d="M12.75 7.02c.29.27.56.56.79.87l2.6-1.5c.54 1.02 1 2.11 1.33 3.26h-.01c.35 1.24.52 2.54.52 3.9 0 1.36-.17 2.66-.52 3.9h.01c-.33 1.15-.79 2.24-1.33 3.26l-2.6-1.5c-.23.31-.5.6-.79.87l1.89 3.15c.71.41 1.33.95 1.86 1.59l2.53-1.59c.25.64.38 1.28.38 1.93 0-2.13-1.26-3.96-3.06-4.77l1.89-3.15z" fill="currentColor"/>
    </svg>''',
    
    'Seminar 2': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M5 13.18c0 .65.13 1.29.38 1.93L2.85 16.7c-.53-1.02-.99-2.11-1.33-3.26h.01c-.35-1.24-.52-2.54-.52-3.9 0-1.36.17-2.66.52-3.9H1.52c.34-1.15.8-2.24 1.33-3.26l2.53 1.59c-.25.64-.38 1.28-.38 1.93 0 2.13 1.26 3.96 3.06 4.77l-1.89 3.15c-.71-.41-1.33-.95-1.86-1.59z" fill="currentColor"/>
      <path d="M12.75 7.02c.29.27.56.56.79.87l2.6-1.5c.54 1.02 1 2.11 1.33 3.26h-.01c.35 1.24.52 2.54.52 3.9 0 1.36-.17 2.66-.52 3.9h.01c-.33 1.15-.79 2.24-1.33 3.26l-2.6-1.5c-.23.31-.5.6-.79.87l1.89 3.15c.71.41 1.33.95 1.86 1.59l2.53-1.59c.25.64.38 1.28.38 1.93 0-2.13-1.26-3.96-3.06-4.77l1.89-3.15z" fill="currentColor"/>
    </svg>''',
    
    'Seminar 3': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M5 13.18c0 .65.13 1.29.38 1.93L2.85 16.7c-.53-1.02-.99-2.11-1.33-3.26h.01c-.35-1.24-.52-2.54-.52-3.9 0-1.36.17-2.66.52-3.9H1.52c.34-1.15.8-2.24 1.33-3.26l2.53 1.59c-.25.64-.38 1.28-.38 1.93 0 2.13 1.26 3.96 3.06 4.77l-1.89 3.15c-.71-.41-1.33-.95-1.86-1.59z" fill="currentColor"/>
      <path d="M12.75 7.02c.29.27.56.56.79.87l2.6-1.5c.54 1.02 1 2.11 1.33 3.26h-.01c.35 1.24.52 2.54.52 3.9 0 1.36-.17 2.66-.52 3.9h.01c-.33 1.15-.79 2.24-1.33 3.26l-2.6-1.5c-.23.31-.5.6-.79.87l1.89 3.15c.71.41 1.33.95 1.86 1.59l2.53-1.59c.25.64.38 1.28.38 1.93 0-2.13-1.26-3.96-3.06-4.77l1.89-3.15z" fill="currentColor"/>
    </svg>''',
    
    'Seminar 4': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M5 13.18c0 .65.13 1.29.38 1.93L2.85 16.7c-.53-1.02-.99-2.11-1.33-3.26h.01c-.35-1.24-.52-2.54-.52-3.9 0-1.36.17-2.66.52-3.9H1.52c.34-1.15.8-2.24 1.33-3.26l2.53 1.59c-.25.64-.38 1.28-.38 1.93 0 2.13 1.26 3.96 3.06 4.77l-1.89 3.15c-.71-.41-1.33-.95-1.86-1.59z" fill="currentColor"/>
      <path d="M12.75 7.02c.29.27.56.56.79.87l2.6-1.5c.54 1.02 1 2.11 1.33 3.26h-.01c.35 1.24.52 2.54.52 3.9 0 1.36-.17 2.66-.52 3.9h.01c-.33 1.15-.79 2.24-1.33 3.26l-2.6-1.5c-.23.31-.5.6-.79.87l1.89 3.15c.71.41 1.33.95 1.86 1.59l2.53-1.59c.25.64.38 1.28.38 1.93 0-2.13-1.26-3.96-3.06-4.77l1.89-3.15z" fill="currentColor"/>
    </svg>''',
    
    'Seminar 5': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M5 13.18c0 .65.13 1.29.38 1.93L2.85 16.7c-.53-1.02-.99-2.11-1.33-3.26h.01c-.35-1.24-.52-2.54-.52-3.9 0-1.36.17-2.66.52-3.9H1.52c.34-1.15.8-2.24 1.33-3.26l2.53 1.59c-.25.64-.38 1.28-.38 1.93 0 2.13 1.26 3.96 3.06 4.77l-1.89 3.15c-.71-.41-1.33-.95-1.86-1.59z" fill="currentColor"/>
      <path d="M12.75 7.02c.29.27.56.56.79.87l2.6-1.5c.54 1.02 1 2.11 1.33 3.26h-.01c.35 1.24.52 2.54.52 3.9 0 1.36-.17 2.66-.52 3.9h.01c-.33 1.15-.79 2.24-1.33 3.26l-2.6-1.5c-.23.31-.5.6-.79.87l1.89 3.15c.71.41 1.33.95 1.86 1.59l2.53-1.59c.25.64.38 1.28.38 1.93 0-2.13-1.26-3.96-3.06-4.77l1.89-3.15z" fill="currentColor"/>
    </svg>''',
    
    'Break': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 5h-2V5h2v3zM4 19h16v2H4z" fill="currentColor"/>
    </svg>''',
    
    'Morning Program': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/>
      <polyline points="12 7 12 12 16 14" stroke="currentColor" stroke-width="2" fill="none"/>
    </svg>''',
    
    'Afternoon Seminars': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/>
      <polyline points="12 7 12 12 16 14" stroke="currentColor" stroke-width="2" fill="none"/>
    </svg>''',
    
    'Evening Program': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/>
      <polyline points="12 7 12 12 16 14" stroke="currentColor" stroke-width="2" fill="none"/>
    </svg>''',
    
    'Health Focus': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" fill="currentColor"/>
    </svg>''',
    
    'Non-Commercial Exhibits': '''<svg viewBox="0 0 24 24" width="16" height="16" style="margin-right: 4px;">
      <path d="M5 13.18c0 .65.13 1.29.38 1.93L2.85 16.7c-.53-1.02-.99-2.11-1.33-3.26h.01c-.35-1.24-.52-2.54-.52-3.9 0-1.36.17-2.66.52-3.9H1.52c.34-1.15.8-2.24 1.33-3.26l2.53 1.59c-.25.64-.38 1.28-.38 1.93 0 2.13 1.26 3.96 3.06 4.77l-1.89 3.15c-.71-.41-1.33-.95-1.86-1.59z" fill="currentColor"/>
    </svg>'''
}

def add_tag_icons(content):
    lines = content.split('\n')
    result_lines = []
    
    for i, line in enumerate(lines):
        # Check if this line contains a tag
        match = re.search(r'<span class="tag">([^<]+)</span>', line)
        if match:
            tag_text = match.group(1)
            if tag_text in icons:
                # Replace tag with icon + tag
                icon = icons[tag_text].strip()
                new_tag = f'<span class="tag">{icon}{tag_text}</span>'
                new_line = line.replace(f'<span class="tag">{tag_text}</span>', new_tag)
                result_lines.append(new_line)
            else:
                result_lines.append(line)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

# Apply the replacement
new_content = add_tag_icons(content)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Icons added to all event tags!")
print("   - Meal icons for Breakfast, Lunch, Dinner")
print("   - Exhibit icons for Exhibits Open")
print("   - Lecture icons for Seminars and Speakers")
print("   - Prayer icons for Prayer Time")
print("   - Time icons for all programs")
