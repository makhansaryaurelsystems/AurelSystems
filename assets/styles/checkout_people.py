import os
import re

# Paths
STYLES_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(STYLES_DIR, 'checkout_people.txt')
SCSS_FILE = os.path.join(STYLES_DIR, 'main.scss')
OUTPUT_HTML = os.path.join(STYLES_DIR, 'checkout_people.html')

def extract_scss_keys(scss_content, map_name):
    """Extracts keys from a SCSS map."""
    pattern = r'\$' + re.escape(map_name) + r'\s*:\s*\((.*?)\);'
    match = re.search(pattern, scss_content, re.DOTALL)
    if not match: return []
    map_content = match.group(1)
    keys = re.findall(r"['\"]([\w-]+)['\"]\s*:", map_content)
    unique_keys = []
    for k in keys:
        if k not in unique_keys: unique_keys.append(k)
    return unique_keys

def parse_people_text(raw_text):
    """
    Parses text blocks separated by double newlines.
    Expected format per block:
    Line 1: Name
    Line 2: Role
    Line 3: Description
    Lines 4+: Links (e.g. LinkedIn, GitHub)
    """
    blocks = [b.strip() for b in raw_text.split('\n\n') if b.strip()]
    people = []
    
    for block in blocks:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if len(lines) < 3: continue 
        
        person = {
            'name': lines[0],
            'role': lines[1],
            'desc': lines[2],
            'links': lines[3:] if len(lines) > 3 else []
        }
        people.append(person)
    return people

def main():
    # 1. Read Text Content
    if not os.path.exists(TEXT_FILE):
        print(f"Error: {TEXT_FILE} not found.")
        return
    
    with open(TEXT_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    people_data = parse_people_text(raw_text)
    
    if not people_data:
        print("Error: No valid people data found.")
        return

    # 2. Extract Themes
    if not os.path.exists(SCSS_FILE):
        print(f"Error: {SCSS_FILE} not found.")
        return
    
    with open(SCSS_FILE, 'r', encoding='utf-8') as f:
        scss_content = f.read()
        
    themes = extract_scss_keys(scss_content, 'people-themes')
    
    # 3. Generate HTML
    theme_options = ""
    for theme in themes:
        display_name = theme.replace('-', ' ').title()
        theme_options += f'<option value="{theme}">{display_name}</option>\n'

    grid_content = ""
    
    # Helper for avatar placeholder
    avatars = [68, 12, 44, 32, 5] # Random IDs
    
    for i, p in enumerate(people_data):
        links_html = ""
        for link_text in p['links']:
            # Using generic icon logic based on platform name
            icon = "https://cdn-icons-png.flaticon.com/512/846/846551.png" # default web
            if "linkedin" in link_text.lower(): icon = "https://cdn-icons-png.flaticon.com/512/174/174857.png"
            elif "github" in link_text.lower(): icon = "https://cdn-icons-png.flaticon.com/512/25/25231.png"
            elif "twitter" in link_text.lower(): icon = "https://cdn-icons-png.flaticon.com/512/733/733579.png"
            elif "dribbble" in link_text.lower(): icon = "https://cdn-icons-png.flaticon.com/512/174/174881.png"
            
            links_html += f'<img src="{icon}" alt="{link_text}" title="{link_text}">'

        img_id = avatars[i % len(avatars)]
        
        card = f"""
                <div class="team-card">
                    <div class="avatar">
                        <img src="https://i.pravatar.cc/150?img={img_id}" alt="{p['name']}" style="width:100%;height:100%;object-fit:cover;">
                    </div>
                    <div class="info">
                        <h3>{p['name']}</h3>
                        <div class="role">{p['role']}</div>
                        <p style="margin-top:0.5rem; font-size:0.9rem; opacity:0.8">{p['desc']}</p>
                        <div class="links">
                            {links_html}
                        </div>
                    </div>
                </div>
        """
        grid_content += card

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>People Theme Tester</title>
    <link rel="stylesheet" href="main.css">
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            padding: 40px;
            padding-top: 100px;
            background-color: #f4f4f5;
        }}
        #controls {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
        }}
        select {{
            padding: 8px 12px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>

    <div id="controls">
        <label for="theme-select"><strong>Select Theme:</strong></label>
        <select id="theme-select">
            {theme_options}
        </select>
    </div>

    <div class="container">
        <div id="wrapper" class="theme-people-{themes[0] if themes else 'classic-corporate'}">
            <div class="team-grid">
                {grid_content}
            </div>
        </div>
    </div>

    <script>
        const themeSelect = document.getElementById('theme-select');
        const wrapper = document.getElementById('wrapper');
        const themes = {str(themes)};

        themeSelect.addEventListener('change', (e) => {{
            const selected = e.target.value;
            // Remove all known theme classes
            themes.forEach(t => wrapper.classList.remove('theme-people-' + t));
            // Add selected
            wrapper.classList.add('theme-people-' + selected);
        }});
    </script>
</body>
</html>"""

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {OUTPUT_HTML} successfully.")

if __name__ == "__main__":
    main()
