# How to Use

## 1. Include Base CSS (Required)
Always include the base CSS file first:
```html
<link rel="stylesheet" href="style-base.css">
```

## 2. Choose ONE Theme
Include one of the theme CSS files:
```html
<link rel="stylesheet" href="style-minimalist.css">
```

## 3. HTML Structure
Use this HTML structure for each post card:

```html
<div class="posts-container">
    <div class="post-card">
        <div class="post-thumbnail">
            <img src="thumbnail.jpg" alt="Post thumbnail">
            <!-- Or use placeholder text -->
            <span>IMAGE</span>
        </div>
        <div class="post-content">
            <div class="post-header">
                <h2 class="post-title">Your Post Title</h2>
                <div class="post-meta">January 15, 2026 • by Author Name</div>
            </div>
            <div class="post-excerpt">
                First 10 sentences of your post content go here...
            </div>
            <div class="post-full">
                The rest of your post content goes here...
            </div>
            <button class="read-more" onclick="toggleReadMore(this)">Read More</button>
        </div>
    </div>
</div>
```

## 4. JavaScript for Read More
Add this JavaScript function:

```javascript
function toggleReadMore(button) {
    const postContent = button.closest('.post-content');
    const fullContent = postContent.querySelector('.post-full');
    
    fullContent.classList.toggle('expanded');
    
    if (fullContent.classList.contains('expanded')) {
        button.textContent = 'Read Less';
    } else {
        button.textContent = 'Read More';
    }
}
```

## 5. Customization

### Changing Accent Colors
Each theme uses CSS variables implicitly. To customize:

**Example - Neon Accent (Purple → Blue):**
```css
/* Change from purple to blue */
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
color: #60a5fa;
box-shadow: 0 0 15px rgba(59, 130, 246, 0.8);
```

#### Adjusting Contrast
For even higher contrast:
```css
.post-excerpt,
.post-full {
    color: #ffffff; /* Pure white instead of light gray */
}
```

#### Thumbnail Sizes
Adjust thumbnail dimensions per theme:
```css
.post-thumbnail {
    width: 150px;  /* Increase from default */
    height: 150px;
}
```
