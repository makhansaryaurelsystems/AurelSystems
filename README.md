
> This is temporary for Aurel Systems Inc.

# Workflow of the website content management

## Site Content 
- Any subdirectory of the **content** directory is a page.
- The **name** of the subdirectory is the **title** of that page.
- The content of the subdirectory are **markdown files**. 
- Each **markdown file** is treated as a **card** for **css styling**. 
- **Subdirectories** of that specific subdirectory are **subpages** with their own cards and content but the same rules apply.

## **Markdown filename convention** 
- Starts with date in **YYYY-MM-DD** format.
- Use **kebab-case**.
- End with **.md** extension.

> Example: 2026-01-28-about.md

## Markdown file content
- The highest level heading uses a **level 2 heading (##)** at the begining of the file.
- The rest of the content uses lower level headings as per need. 
- Must use **markdown-only** for styling.

## Python script: 
- Will use the **date part** of the filename to set the date of the post and the order of the posts appearing on the page, _**everywhere**_.
- Does **not** care what the rest of the filename is. Use that portion of the filename for your own reference.

## CSS dyanmic switch 
- Use a **which-css** file in each subdirectory to DIRECT **python** to switch between css files.
