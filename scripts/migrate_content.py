import os
import shutil
import re

def migrate_content():
    base_dir = os.getcwd() 
    source_dir = os.path.join(base_dir, "old")
    dest_dir = os.path.join(base_dir, "new", "html_old")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    slug_map = {}
    
    slug_map[""] = "index.html" 
    
    files_to_process = []

    print("Scanning directories...")
    for dirpath, dirnames, filenames in os.walk(source_dir):
        if "index.html" in filenames:
            rel_path = os.path.relpath(dirpath, source_dir)
            
            if rel_path == ".":
                continue

            slug = rel_path.replace(os.path.sep, "/")
            new_name = rel_path.replace(os.path.sep, "_") + ".html"
            
            slug_map[slug] = new_name
            files_to_process.append((os.path.join(dirpath, "index.html"), new_name))

    print(f"Found {len(files_to_process)} files to process.")

    domain_regex = re.compile(r'https?://www\.aurelsystems\.com/([^"\']*)')

    for src_path, new_name in files_to_process:
        dest_path = os.path.join(dest_dir, new_name)
        
        try:
            with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            def replace_link(match):
                path = match.group(1)

                clean_path = path.rstrip('/')
                
                if clean_path in slug_map:
                    return slug_map[clean_path]
                
                if clean_path == "":
                    return "../index.html"  
                
                return match.group(0) 

            new_content = domain_regex.sub(replace_link, content)
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
        except Exception as e:
            print(f"Error processing {src_path}: {e}")

    print("Migration complete.")

if __name__ == "__main__":
    migrate_content()
