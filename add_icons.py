#!/usr/bin/env python3
import re

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# SVG clock icon template
clock_svg = '''<span class="icon">
    <svg viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10"></circle>
      <polyline points="12 6 12 12 16 14"></polyline>
    </svg>
  </span>'''

# Replace all <span class="time">TEXT</span> with wrapped version
# Pattern: match opening span with class="time", capture content, match closing span
pattern = r'<span class="time">([^<]+)</span>'

def replace_time(match):
    time_text = match.group(1)
    return f'{clock_svg}\n  {time_text}\n</span>'

# Use a more careful replacement that preserves structure
def replace_with_wrapper(content):
    # Find all time spans
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        if '<span class="time">' in line and '</span>' in line:
            # Extract the time text
            match = re.search(r'<span class="time">([^<]+)</span>', line)
            if match:
                time_text = match.group(1)
                # Get the indentation
                indent = len(line) - len(line.lstrip())
                indent_str = ' ' * indent
                
                # Build the replacement with proper indentation
                replacement = (
                    f'{indent_str}<span class="time-with-icon">\n'
                    f'{indent_str}  {clock_svg}\n'
                    f'{indent_str}  {time_text}\n'
                    f'{indent_str}</span>'
                )
                result_lines.append(replacement)
            else:
                result_lines.append(line)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

# Apply the replacement
new_content = replace_with_wrapper(content)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Icons added to all time entries!")
