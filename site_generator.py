import os
import shutil
import re
import sys
import markdown
import sass  # Requires: pip install libsass

# --- Configuration ---
ROOT_DIR = '.'
CONTENT_DIR = os.path.join(ROOT_DIR, 'content')
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
STYLES_DIR = os.path.join(ASSETS_DIR, 'styles')
LIVE_DIR = os.path.join(ROOT_DIR, 'live')

SCSS_FILE = os.path.join(STYLES_DIR, 'main.scss')
CSS_OUTPUT_DIR = os.path.join(LIVE_DIR, 'css')
CSS_OUTPUT_FILE = os.path.join(CSS_OUTPUT_DIR, 'style.css')

# Regex for parsing date-filename.md (e.g. 2026-01-01-MyPost.md)
DATE_FILE_REGEX = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$')

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def compile_sass():
    """Compiles main.scss to style.css"""
    print(f"Compiling SASS: {SCSS_FILE} -> {CSS_OUTPUT_FILE}")
    ensure_dir(CSS_OUTPUT_DIR)
    
    try:
        css_content = sass.compile(filename=SCSS_FILE)
        with open(CSS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("SASS compilation successful.")
    except Exception as e:
        print(f"Error compiling SASS: {e}")
        # Continue execution even if SASS fails (might verify logic without style)

def clean_and_prepare_live():
    """Cleans /live/ directory but keeps the root folder."""
    ensure_dir(LIVE_DIR)
    # Optional: Clear subdirs to avoid stale files
    # for item in os.listdir(LIVE_DIR):
    #     path = os.path.join(LIVE_DIR, item)
    #     if os.path.isdir(path): shutil.rmtree(path)
    #     else: os.remove(path)
    
    ensure_dir(CSS_OUTPUT_DIR)

def get_navigation_items():
    """Returns top-level directories in 'content' as navigation items."""
    items = []
    if os.path.exists(CONTENT_DIR):
        for entry in os.listdir(CONTENT_DIR):
            if os.path.isdir(os.path.join(CONTENT_DIR, entry)):
                items.append(entry)
    items.sort()
    return items

def generate_navbar_html(active_tab, nav_items):
    """Generates the HTML for the navigation tabs."""
    nav_html = '<nav class="navbar"><ul class="nav-links">'
    for item in nav_items:
        link = f"{item}.html"
        active_class = ' class="active"' if item == active_tab else ''
        nav_html += f'<li{active_class}><a href="{link}">{item}</a></li>'
    nav_html += '</ul></nav>'
    return nav_html

def parse_md_file(filepath):
    """Reads an MD file and returns metadata and content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Simple parsing: separate metadata headers if any
    # Assuming standard markdown for now, or the format used in previous steps
    # Just return raw html conversion for simplicity unless frontmatter parser is needed
    html = markdown.markdown(text)
    return html

def parse_config(dir_path):
    """Reads 'config' file in directory to determine theme/layout."""
    config = {}
    config_path = os.path.join(dir_path, 'config')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key, val = line.strip().split(':', 1)
                    config[key.strip()] = val.strip()
    return config

def generate_html_pages(nav_items):
    """Walks through content directory and generates HTML pages."""
    
    # We treat top-level folders as "Tabs" -> "Page.html"
    for item in nav_items:
        section_path = os.path.join(CONTENT_DIR, item)
        output_filename = f"{item}.html"
        output_path = os.path.join(LIVE_DIR, output_filename)
        
        print(f"Processing Section: {item} -> {output_filename}")
        
        # Parse config for theme
        config = parse_config(section_path)
        # Default themes if not specified
        theme_class = ""
        if 'base' in config: # e.g. base: base
            pass 
        if 'cards' in config: # e.g. cards: executive
            # Map simplified config names to our SCSS theme classes
            # Announcements use 'theme-announcement-X', People use 'theme-people-X'
            # Let's map generically:
            theme_val = config['cards']
            if theme_val.lower() != 'none':
                # We check context based on folder name
                if item in ['People', 'Contact']:
                    theme_class = f"theme-people-{theme_val}"
                else:
                     theme_class = f"theme-announcement-{theme_val}"
        
        # Collect content
        page_body = ""
        
        # Gather markdown files
        md_files = []
        for f in os.listdir(section_path):
            if DATE_FILE_REGEX.match(f):
                md_files.append(f)
            # handle non-dated MD files? e.g. Introduction.md
            elif f.endswith('.md') and f not in ['header.md', 'footer.md']:
                 md_files.append(f)

        md_files.sort() # sort by name (date)
        
        # If it's a "People" grid, we want a grid container
        if item == 'People':
            page_body += '<div class="team-grid">'
        elif item in ['Announcements', 'Solutions', 'About']:
             page_body += '<div class="posts-container">'
        
        for md_file in md_files:
            md_path = os.path.join(section_path, md_file)
            content_html = parse_md_file(md_path)
            
            # Wrap content in a card if needed based on theme
            # The SCSS expects .post-card or .team-card inside the theme wrapper
            
            # For simplicity, we wrap every MD file's content in a card div
            if item == 'People':
                 # People MDs usually contained keys like Name: Role: etc. 
                 # We might needs a specialized parser for "People" to make strict cards
                 # For now, just wrap the raw HTML
                 page_body += f'<div class="team-card"><div>{content_html}</div></div>'
            else:
                 page_body += f'<div class="post-card"><div class="post-content">{content_html}</div></div>'
                 
        if item == 'People':
            page_body += '</div>' # close team-grid
        elif item in ['Announcements', 'Solutions', 'About']:
             page_body += '</div>' # close posts-container

        # Assemble Full Page
        nav_html = generate_navbar_html(item, nav_items)
        
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{item} - Aurel Systems</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="{theme_class}">
    <header>
        {nav_html}
    </header>
    
    <main style="padding-top: 80px;">
        <div class="header-content" style="text-align:center; padding: 20px;">
            <!-- Optional Header Content -->
        </div>
        
        {page_body}
    </main>
    
    <footer>
        <p>&copy; {datetime.now().year} Aurel Systems Inc.</p>
    </footer>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

def main():
    print("Starting Site Generator...")
    clean_and_prepare_live()
    compile_sass()
    
    nav_items = get_navigation_items()
    generate_html_pages(nav_items)
    print("Done.")

if __name__ == "__main__":
    main()