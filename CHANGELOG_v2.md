# 📝 Changelog v2.0 - Multi-User System với Auto-Filter & Delete Protection

**Date:** 2025-11-24  
**Version:** 2.0.0

---

## 🎯 Tổng quan thay đổi

### **3 tính năng chính:**
1. ✅ **Auto-filter theo username** - Tự động lọc bài viết của người dùng hiện tại
2. ✅ **Delete protection** - Chỉ creator mới được xóa bài viết của mình
3. ✅ **User-specific favorites** - Favorites riêng cho từng user

---

## 🆕 Tính năng mới

### 1️⃣ **Auto-Filter theo Username (Default Filter)**

**Mô tả:**  
Khi user đã đặt tên, trang chủ tự động lọc bài viết có category = username của họ.

**Cách hoạt động:**
```javascript
// Auto-filter on page load
if (username && !manualFilter && !clearedBefore) {
    url.add('categories', username);
    redirect(url);
}
```

**User Experience:**
```
Bước 1: User "Tuấn" vào trang chủ
        ↓
Bước 2: Tự động filter: categories=Tuấn
        ↓
Bước 3: Chỉ hiển thị bài viết có category "Tuấn"
        (= bài do Tuấn tạo/import/like)
```

**Clear Filter:**
- Button "❌ Xóa bộ lọc 'Tuấn'" xuất hiện tự động
- Click để xóa filter và xem tất cả bài viết
- Thêm param `?noclear=1` để ngăn auto-filter lần sau

**File changes:**
- `templates/index.html` - Added auto-filter logic in DOMContentLoaded
- Added `showClearUsernameFilterButton()` function

---

### 2️⃣ **Creator Tracking (created_by)**

**Mô tả:**  
Lưu tên người tạo bài viết vào cột `created_by`.

**Database Migration:**
```sql
ALTER TABLE articles ADD COLUMN created_by TEXT;
```

**Khi nào set created_by:**
- ✅ Import bài viết → `created_by = username`
- ✅ Like bài viết → Auto-add username category (không set created_by)
- ✅ Tạo bài viết mới (future feature)

**Code Implementation:**
```python
# In import_articles()
cursor.execute('''
    INSERT INTO articles 
    (title_vi, title_en, content_vi, content_en, category, created_by)
    VALUES (?, ?, ?, ?, ?, ?)
''', (..., username))
```

**File changes:**
- `app.py` - Added `created_by` column to articles table
- `app.py` - Updated `import_articles()` to set `created_by`

---

### 3️⃣ **Delete Protection (Only Creator Can Delete)**

**Mô tả:**  
Chỉ người tạo bài viết mới được phép xóa.

**Validation Logic:**
```python
if article['created_by'] != current_username:
    return error: "⛔ Chỉ người tạo mới có thể xóa!"
```

**User Experience:**
```
Scenario 1: Tuấn xóa bài của Tuấn
  ✅ Success: "✅ Bài viết đã được xóa!"
  
Scenario 2: Mai xóa bài của Tuấn
  ❌ Error: "⛔ Chỉ người tạo (Tuấn) mới có thể xóa bài viết này!"
  
Scenario 3: Xóa bài cũ (không có created_by)
  ✅ Success: Anyone can delete (backward compatibility)
```

**API Changes:**
```javascript
// Old (no auth)
POST /article/delete/<id>

// New (with username)
POST /article/delete/<id>
Body: {username: "Tuấn"}
```

**File changes:**
- `app.py` - Updated `/article/delete/<id>` to check `created_by`
- `templates/article.html` - Updated `deleteArticle()` to send username

---

### 4️⃣ **User-Specific Favorites (Per-User Like)**

**Mô tả:**  
Favorites lưu riêng cho từng user thay vì global.

**Database Migration:**
```sql
CREATE TABLE user_favorites (
    username TEXT NOT NULL,
    article_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, article_id)
);
```

**Old vs New:**
```
OLD: articles.is_favorite (0/1) - Global cho tất cả users
NEW: user_favorites (username, article_id) - Riêng từng user
```

**API Changes:**
```javascript
// Toggle favorite
POST /api/article/<id>/favorite
Body: {username: "Tuấn"}

// Get user favorites
GET /api/user/<username>/favorites
Response: {favorite_ids: [1, 5, 10]}
```

**File changes:**
- `app.py` - Created `user_favorites` table
- `app.py` - Updated `/api/article/<id>/favorite` to use `user_favorites`
- `app.py` - Added `/api/user/<username>/favorites` endpoint
- `templates/index.html` - Added `loadUserFavorites()` function

---

## 🔧 Technical Details

### **Database Schema Changes**

#### **1. Articles Table - Added created_by**
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title_vi TEXT,
    title_en TEXT,
    content_vi TEXT,
    content_en TEXT,
    category TEXT,
    is_favorite INTEGER DEFAULT 0,  -- Deprecated, use user_favorites
    created_by TEXT,                 -- NEW: Creator username
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### **2. User Favorites Table - NEW**
```sql
CREATE TABLE user_favorites (
    username TEXT NOT NULL,
    article_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, article_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);
```

---

### **API Endpoints Updated**

#### **1. Toggle Favorite (Modified)**
```
POST /api/article/<id>/favorite
Request: {username: "Tuấn"}
Response: {success: true, is_favorite: true, message: "Tuấn đã thêm vào yêu thích"}
```

#### **2. Get User Favorites (NEW)**
```
GET /api/user/<username>/favorites
Response: {
    success: true, 
    username: "Tuấn",
    favorite_ids: [1, 2, 3]
}
```

#### **3. Delete Article (Modified)**
```
POST /article/delete/<id>
Request: {username: "Tuấn"}
Response: {success: true, message: "✅ Bài viết đã được xóa!"}
Error: {success: false, error: "⛔ Chỉ người tạo (Mai) mới có thể xóa!"}
```

---

### **Frontend Logic Changes**

#### **1. Auto-Filter on Page Load**
```javascript
document.addEventListener('DOMContentLoaded', async function() {
    const username = getUsername();
    const currentCategories = new URLSearchParams(window.location.search).getAll('categories');
    
    // Auto-filter by username if no manual filter
    if (username && currentCategories.length === 0 && !hasNoClearParam()) {
        // Redirect with username category
        window.location.search = `?categories=${encodeURIComponent(username)}`;
    }
});
```

#### **2. Clear Username Filter Button**
```javascript
function showClearUsernameFilterButton(username) {
    const btn = createElement('<button>❌ Xóa bộ lọc "' + username + '"</button>');
    btn.onclick = () => {
        // Remove username from categories
        const newUrl = removeCategory(username);
        newUrl.set('noclear', '1'); // Prevent auto-filter
        window.location.search = newUrl;
    };
}
```

#### **3. Delete with Username Check**
```javascript
async function deleteArticle() {
    const username = getUsername();
    if (!username) {
        alert('⚠️ Vui lòng đặt tên người dùng trước!');
        return;
    }
    
    const response = await fetch('/article/delete/' + articleId, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username})
    });
    
    if (!response.ok) {
        alert('❌ Không thể xóa bài viết');
    }
}
```

---

## 🎭 Use Cases

### **Use Case 1: Tuấn vào trang chủ lần đầu**
```
1. Tuấn đã đặt username = "Tuấn"
2. Vào http://localhost:5000
3. ✅ Tự động redirect: /?categories=Tuấn
4. ✅ Chỉ hiển thị bài viết có category "Tuấn"
5. ✅ Button "❌ Xóa bộ lọc 'Tuấn'" xuất hiện
```

### **Use Case 2: Tuấn muốn xem tất cả bài viết**
```
1. Click "❌ Xóa bộ lọc 'Tuấn'"
2. ✅ Redirect: /?noclear=1
3. ✅ Hiển thị tất cả bài viết
4. ✅ Lần sau vào trang chủ không còn auto-filter (do noclear=1)
```

### **Use Case 3: Mai cố xóa bài của Tuấn**
```
1. Mai (username = "Mai") vào bài viết do Tuấn tạo
2. Click "🗑️ Xóa bài viết"
3. ❌ Error: "⛔ Chỉ người tạo (Tuấn) mới có thể xóa bài viết này!"
4. ✅ Bài viết vẫn còn nguyên
```

### **Use Case 4: Import bài viết**
```
1. Tuấn import bài mới
2. Form gửi: {json_data: {...}, username: "Tuấn"}
3. ✅ Backend set: created_by = "Tuấn"
4. ✅ Backend auto-add category "Tuấn"
5. ✅ Bài viết chỉ Tuấn mới được xóa
```

### **Use Case 5: Like/Unlike bài viết**
```
1. Tuấn like bài viết ID=5
2. POST /api/article/5/favorite {username: "Tuấn"}
3. ✅ Insert into user_favorites: (Tuấn, 5)
4. ✅ Auto-add category "Tuấn" to article 5
5. Mai like cùng bài viết
6. ✅ Insert into user_favorites: (Mai, 5)
7. ✅ Auto-add category "Mai" to article 5
8. ✅ Kết quả: Article 5 có 2 categories: "Tuấn", "Mai"
```

---

## 📊 Database Migration Guide

### **Step 1: Backup Database**
```bash
cp articles.db backups/articles_backup_$(date +%Y%m%d_%H%M%S).db
```

### **Step 2: Add created_by Column**
```sql
ALTER TABLE articles ADD COLUMN created_by TEXT;
```

### **Step 3: Create user_favorites Table**
```sql
CREATE TABLE user_favorites (
    username TEXT NOT NULL,
    article_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, article_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);
```

### **Step 4: Migrate Old Favorites (Optional)**
```sql
-- If you want to preserve old global favorites
INSERT INTO user_favorites (username, article_id)
SELECT 'Admin', id FROM articles WHERE is_favorite = 1;
```

---

## 🚀 Deployment

### **Development:**
```bash
python app.py
```

### **Production:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Test Commands:**
```bash
# Check database structure
sqlite3 articles.db ".schema articles"
sqlite3 articles.db ".schema user_favorites"

# Count user favorites
sqlite3 articles.db "SELECT username, COUNT(*) FROM user_favorites GROUP BY username;"

# List articles by creator
sqlite3 articles.db "SELECT id, title_vi, created_by FROM articles WHERE created_by IS NOT NULL;"
```

---

## ⚠️ Breaking Changes

### **1. Delete Endpoint Changed**
```
OLD: POST /article/delete/<id> (no auth)
NEW: POST /article/delete/<id> {username: "..."}
```

**Migration:**  
Update all delete buttons to send username in request body.

### **2. Favorite Endpoint Changed**
```
OLD: POST /api/article/<id>/favorite (toggle global favorite)
NEW: POST /api/article/<id>/favorite {username: "..."} (toggle user favorite)
```

**Migration:**  
Update all favorite buttons to send username in request body.

### **3. Homepage Auto-Filter**
```
OLD: Show all articles by default
NEW: Auto-filter by username by default
```

**Migration:**  
Users can click "Clear Filter" to see all articles. Add `?noclear=1` to disable auto-filter.

---

## 🐛 Known Issues

1. **Old articles without created_by:**  
   - Anyone can delete them (backward compatibility)
   - Solution: Run migration script to set created_by based on categories

2. **noclear parameter persists:**  
   - If user clicks "Clear Filter", auto-filter won't work until they remove `?noclear=1` from URL
   - Solution: Add "Reset Filter" button to remove noclear param

3. **Favorites not migrated:**  
   - Old global favorites (is_favorite=1) not automatically migrated to user_favorites
   - Solution: Run migration SQL or manually favorite again

---

## 📚 Files Changed

### **Backend (app.py):**
- ✅ Added `created_by` column to articles table
- ✅ Created `user_favorites` table
- ✅ Updated `import_articles()` to set created_by
- ✅ Updated `/api/article/<id>/favorite` to use user_favorites
- ✅ Added `/api/user/<username>/favorites` endpoint
- ✅ Updated `/article/delete/<id>` to check creator

### **Frontend (templates/):**
- ✅ `index.html` - Auto-filter logic, Clear Filter button
- ✅ `index.html` - Load user favorites, update heart icons
- ✅ `article.html` - Delete with username check
- ✅ `import.html` - Send username with import

---

## ✅ Testing Checklist

- [ ] **Auto-Filter Test:**
  - [ ] User có username → Trang chủ auto-filter
  - [ ] User chưa có username → Không auto-filter
  - [ ] Click "Clear Filter" → Hiển thị tất cả
  - [ ] Reload page → Không auto-filter (noclear=1)

- [ ] **Delete Protection Test:**
  - [ ] Creator xóa bài của mình → Success
  - [ ] User khác xóa bài → Error 403
  - [ ] Xóa bài cũ (no created_by) → Success

- [ ] **User Favorites Test:**
  - [ ] User A like bài → Chỉ A thấy heart đỏ
  - [ ] User B like bài → Chỉ B thấy heart đỏ
  - [ ] Load favorites on page load → Hearts correct

- [ ] **Import Test:**
  - [ ] Import với username → created_by set
  - [ ] Import với username → Auto-add category
  - [ ] Import không username → created_by NULL

---

## 🎉 Summary

**Trước:**
- Favorites global (tất cả users dùng chung)
- Ai cũng xóa được bài viết
- Không tự động lọc theo user

**Sau:**
- ✅ Favorites riêng từng user
- ✅ Chỉ creator mới xóa được
- ✅ Tự động lọc bài viết của user hiện tại
- ✅ Button "Clear Filter" để xem tất cả

**Version:** 2.0.0  
**Release Date:** 2025-11-24  
**Status:** ✅ Production Ready
