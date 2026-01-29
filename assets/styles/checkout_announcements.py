import os
import re

# Paths
STYLES_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(STYLES_DIR, 'checkout_announcements.txt')
SCSS_FILE = os.path.join(STYLES_DIR, 'main.scss')
OUTPUT_HTML = os.path.join(STYLES_DIR, 'checkout_announcements.html')

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

def main():
    # 1. Read Text Content
    if not os.path.exists(TEXT_FILE):
        print(f"Error: {TEXT_FILE} not found.")
        return
    
    with open(TEXT_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    # Process text into paragraphs
    paragraphs = [p.strip() for p in raw_text.split('\n') if p.strip()]
    
    if not paragraphs:
        print("Error: No content in text file.")
        return

    excerpt_html = f"<p>{paragraphs[0]}</p>"
    full_text_html = "\n".join([f"<p>{p}</p>" for p in paragraphs])

    # 2. Extract Themes
    if not os.path.exists(SCSS_FILE):
        print(f"Error: {SCSS_FILE} not found.")
        return
    
    with open(SCSS_FILE, 'r', encoding='utf-8') as f:
        scss_content = f.read()
        
    themes = extract_scss_keys(scss_content, 'announcement-themes')
    
    # 3. Generate HTML
    theme_options = ""
    for theme in themes:
        display_name = theme.replace('-', ' ').title()
        theme_options += f'<option value="{theme}">{display_name}</option>\n'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Announcement Theme Tester</title>
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
            max-width: 800px;
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
        <div id="wrapper" class="theme-announcement-{themes[0] if themes else 'colorful'}">
            <div class="posts-container">
                
                <div class="post-card">
                    <div class="post-thumbnail">
                        <span>TEST</span>
                    </div>
                    <div class="post-content">
                        <h3 class="post-title">Theme Test Article</h3>
                        <div class="post-meta">Generated from text2test.txt</div>
                        
                        <div class="post-excerpt">
                            {excerpt_html}
                        </div>
                        
                        <div class="post-text">
                            {full_text_html}
                        </div>
                        
                        <button class="read-more">Read Full Story</button>
                    </div>
                </div>

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
            themes.forEach(t => wrapper.classList.remove('theme-announcement-' + t));
            // Add selected
            wrapper.classList.add('theme-announcement-' + selected);
        }});

        // Read More Toggle Logic
        document.querySelectorAll('.read-more').forEach(button => {{
            button.addEventListener('click', function() {{
                const card = this.closest('.post-card');
                card.classList.toggle('expanded');
                
                if (card.classList.contains('expanded')) {{
                    this.textContent = 'Read Less';
                }} else {{
                    this.textContent = 'Read Full Story';
                }}
            }});
        }});
    </script>
</body>
</html>"""

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {OUTPUT_HTML} successfully.")

if __name__ == "__main__":
    main()
