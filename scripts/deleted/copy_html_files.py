import os
import shutil

def copy_html_files():

    root_dir = os.getcwd() 
    target_dir_name = "new"
    target_dir = os.path.join(root_dir, target_dir_name)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created directory: {target_dir}")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if target_dir_name in dirnames: # not the "new" iteself
            dirnames.remove(target_dir_name)

        if "index.html" in filenames:
            rel_path = os.path.relpath(dirpath, root_dir)

            if rel_path == ".":
                level = 0
                parts = []
                base_name = "root" # Special case for root
            else:
                parts = rel_path.split(os.sep)
                level = len(parts)
                base_name = "_".join(parts)

            if level == 0:
                 new_filename = f"{base_name}{level}.html"
            else:
                 new_filename = f"{base_name}{level}.html"

            source_file = os.path.join(dirpath, "index.html")
            dest_file = os.path.join(target_dir, new_filename)

            try:
                shutil.copy2(source_file, dest_file)
                print(f"Copied: {rel_path}/index.html -> new/{new_filename}")
            except Exception as e:
                print(f"Error copying {source_file}: {e}")

if __name__ == "__main__":
    copy_html_files()
