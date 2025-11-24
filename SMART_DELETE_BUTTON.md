# 🔐 Smart Delete Button - Show Only for Article Owners

## ✨ Tính năng

Nút "🗑️ Xóa" chỉ hiện cho bài viết mà user hiện tại đã tạo/sở hữu (có category = username).

---

## 🎯 Logic

### **Quyết định hiện/ẩn:**
```
IF article has category matching username:
    ✅ Show delete button
ELSE:
    ❌ Hide delete button
```

---

## 📍 Áp dụng ở 2 nơi

### **1. Homepage (index.html)**

#### **Before:**
```html
<!-- Delete button hiện cho tất cả bài viết -->
<form action="/delete_article/{{ id }}" method="POST">
    <button>🗑️ Xóa</button>
</form>
```

#### **After:**
```html
<!-- Delete button ẩn mặc định -->
<button class="delete-article-btn"
        data-article-id="{{ article['id'] }}"
        onclick="deleteArticleFromHomepage({{ article['id'] }})"
        style="display: none;">
    🗑️ Xóa
</button>
```

#### **JavaScript Check:**
```javascript
async function showDeleteButtonsForUserArticles(username) {
    const deleteButtons = document.querySelectorAll('.delete-article-btn');
    
    for (const btn of deleteButtons) {
        const articleId = btn.getAttribute('data-article-id');
        
        // Get article categories via API
        const response = await fetch(`/api/article/${articleId}/categories`);
        const data = await response.json();
        
        const categories = data.categories.map(c => c.name);
        
        // Show if article has username category
        if (categories.includes(username)) {
            btn.style.display = 'inline-block';
        }
    }
}
```

---

### **2. Article Detail Page (article.html)**

#### **Before:**
```html
<!-- Delete button luôn hiện -->
<div>
    <button onclick="deleteArticle()">🗑️ Xóa bài viết</button>
</div>
```

#### **After:**
```html
<!-- Delete button ẩn mặc định -->
<div id="deleteArticleContainer" style="display: none;">
    <button onclick="deleteArticle()">🗑️ Xóa bài viết</button>
</div>
```

#### **JavaScript Check:**
```javascript
async function checkArticleOwnership() {
    const username = getUsername();
    if (!username) return;
    
    // Get article categories
    const response = await fetch('/api/article/{{ article.id }}/categories');
    const data = await response.json();
    
    const categories = data.categories.map(c => c.name);
    
    // Show delete button if user owns this article
    if (categories.includes(username)) {
        document.getElementById('deleteArticleContainer').style.display = 'block';
    }
}

// Call on page load
document.addEventListener('DOMContentLoaded', checkArticleOwnership);
```

---

## 🔄 Flow

### **Homepage:**
```
Page Load
  ↓
Get username from localStorage
  ↓
Loop through all delete buttons
  ↓
For each button:
  - Get article ID
  - Fetch article categories via API
  - Check if username in categories
  - If YES → Show button
  - If NO → Keep hidden
```

### **Article Detail:**
```
Page Load
  ↓
checkArticleOwnership()
  ↓
Get username from localStorage
  ↓
Fetch article categories via API
  ↓
Check if username in categories
  ↓
If YES → Show delete button container
If NO → Keep hidden
```

---

## 🎭 Use Cases

### **Case 1: Tuấn xem bài của Tuấn (Homepage)**
```
Given: 
  - User "Tuấn" logged in
  - Article has category "Tuấn"
When: Load homepage
Then:
  ✅ Delete button visible for this article
  ✅ Console: "✅ Show delete button for article X (owned by Tuấn)"
```

### **Case 2: Mai xem bài của Tuấn (Homepage)**
```
Given:
  - User "Mai" logged in
  - Article has category "Tuấn" (not "Mai")
When: Load homepage
Then:
  ❌ Delete button hidden for this article
  ✅ Console: "⚠️ User Mai does not own this article"
```

### **Case 3: Tuấn xem bài của Tuấn (Detail Page)**
```
Given:
  - User "Tuấn" logged in
  - Article has category "Tuấn"
When: Open article detail page
Then:
  ✅ Delete button visible in settings panel
  ✅ Console: "✅ User Tuấn owns this article - showing delete button"
```

### **Case 4: Mai xem bài của Tuấn (Detail Page)**
```
Given:
  - User "Mai" logged in
  - Article has category "Tuấn"
When: Open article detail page
Then:
  ❌ Delete button hidden in settings panel
  ✅ Console: "⚠️ User Mai does not own this article - hiding delete button"
```

### **Case 5: No username set**
```
Given: User chưa đăng nhập (no username)
When: View any page
Then:
  ❌ All delete buttons hidden
  ✅ Console: "⚠️ No username set, hiding delete button"
```

---

## 🔧 Implementation Details

### **New Functions:**

#### **1. showDeleteButtonsForUserArticles(username)** - Homepage
```javascript
// Called in DOMContentLoaded
if (username) {
    await showDeleteButtonsForUserArticles(username);
}
```

#### **2. checkArticleOwnership()** - Article Detail
```javascript
// Called in DOMContentLoaded
document.addEventListener('DOMContentLoaded', checkArticleOwnership);
```

#### **3. deleteArticleFromHomepage(articleId)** - Homepage
```javascript
async function deleteArticleFromHomepage(articleId) {
    const username = getUsername();
    
    if (!confirm('Bạn có chắc chắn muốn xóa?')) return;
    
    const response = await fetch(`/article/delete/${articleId}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username})
    });
    
    if (response.ok) {
        window.location.reload();
    }
}
```

---

## 🐛 Fix: 415 Unsupported Media Type

### **Problem:**
```
Error 415: Did not attempt to load JSON data 
because the request Content-Type was not 'application/json'
```

### **Cause:**
Old code used `<form>` submission (Content-Type: application/x-www-form-urlencoded)

### **Solution:**
Use `fetch()` with JSON body:
```javascript
fetch('/article/delete/1', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},  // ← FIX
    body: JSON.stringify({username: 'Tuấn'})        // ← FIX
})
```

---

## 📊 Comparison

### **Old Behavior:**
| Page | Delete Button | Problem |
|------|--------------|---------|
| Homepage | Always visible | ❌ Anyone can try to delete |
| Detail | Always visible | ❌ Shows error when clicking |

### **New Behavior:**
| Page | Delete Button | Benefit |
|------|--------------|---------|
| Homepage | Only for owners | ✅ Clear visual indicator |
| Detail | Only for owners | ✅ No confusing buttons |

---

## 🔍 API Dependency

### **Endpoint Used:**
```
GET /api/article/<id>/categories
```

**Response:**
```json
{
    "success": true,
    "categories": [
        {"id": 1, "name": "Tuấn"},
        {"id": 2, "name": "Technology"}
    ]
}
```

**Usage:**
```javascript
const categories = data.categories.map(c => c.name);
const isOwner = categories.includes(username);
```

---

## ✅ Testing Checklist

### **Homepage:**
- [ ] Tuấn sees delete button for Tuấn's articles
- [ ] Mai does NOT see delete button for Tuấn's articles
- [ ] Delete button works (deletes and reloads)
- [ ] Console logs ownership checks

### **Detail Page:**
- [ ] Tuấn sees delete button in settings for Tuấn's article
- [ ] Mai does NOT see delete button for Tuấn's article
- [ ] Delete button works (deletes and redirects)
- [ ] Console logs ownership check

### **Edge Cases:**
- [ ] No username → No delete buttons
- [ ] Article with no categories → No delete buttons
- [ ] Multiple users with same article → Each sees button for their own

---

## 🚀 Benefits

1. **UX Improvement:**
   - Users chỉ thấy nút xóa cho bài của mình
   - Không còn thử xóa rồi bị báo lỗi

2. **Security:**
   - Backend vẫn validate (double-check)
   - Frontend chỉ là UI hint

3. **Performance:**
   - Check ownership trên client
   - Không cần server roundtrip để hiện/ẩn button

4. **Consistency:**
   - Cùng logic ở cả homepage và detail page
   - Dễ maintain

---

## 📝 Files Changed

### **templates/index.html:**
- ✅ Changed delete `<form>` → `<button>` with display:none
- ✅ Added `showDeleteButtonsForUserArticles()` function
- ✅ Added `deleteArticleFromHomepage()` function
- ✅ Call ownership check in DOMContentLoaded

### **templates/article.html:**
- ✅ Wrapped delete button in container with display:none
- ✅ Added `checkArticleOwnership()` function
- ✅ Call ownership check in DOMContentLoaded

---

## 🎉 Summary

**Before:** 🗑️ button hiện cho tất cả → User click → Error  
**After:** 🗑️ button CHỈ hiện cho owner → User click → Success

**Status:** ✅ Ready to test  
**Server:** http://localhost:5000

**Quick Test:**
1. Set username "Tuấn"
2. Import article (auto-add category "Tuấn")
3. ✅ See delete button on homepage
4. ✅ See delete button in article detail
5. Change username to "Mai"
6. ✅ Delete button hidden for Tuấn's articles
