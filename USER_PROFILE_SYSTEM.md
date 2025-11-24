# 👤 User Profile System - Local Multi-User Support

## ✨ Tổng quan

Hệ thống cho phép nhiều người dùng chia sẻ chung app local, mỗi người có tên riêng (username). Khi Like bài viết, username tự động được thêm vào như category thứ 6 (ngoài 5 categories thường).

---

## 🎯 Tính năng chính

### 1️⃣ **User Profile Modal - Chọn/Nhập Username**
```
Lần đầu vào app → Modal hiện ra tự động
┌─────────────────────────────────────┐
│   👤 Đặt tên người dùng             │
│   Chọn từ danh sách hoặc nhập mới   │
├─────────────────────────────────────┤
│ 📁 Chọn từ danh sách:               │
│ [ Tuấn    ]                         │
│ [ Mai     ]                         │
│ [ Hùng    ]                         │
├─────────────────────────────────────┤
│ [Nhập tên của bạn...          ]    │
│ [✅ Lưu] [❌ Hủy]                   │
└─────────────────────────────────────┘
```

**Khi nào hiển thị:**
- ✅ Lần đầu vào app (không có username trong localStorage)
- ✅ Click vào "👤 Chưa đặt tên" ở header
- ✅ Bất kỳ lúc nào muốn đổi tên

**LocalStorage:**
```javascript
localStorage.setItem('username', 'Tuấn');
localStorage.getItem('username'); // 'Tuấn'
```

---

### 2️⃣ **Username Display ở Header**
```
Header Navigation:
[Trang Chủ] [Import JSON] [👤 Tuấn] ← Click để đổi tên
                           ↑
                           Màu tím gradient
```

**Màu sắc:**
- Background: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Border-radius: `20px` (pill shape)
- Cursor: `pointer`

---

### 3️⃣ **Auto-add Username Category khi Like**

**Flow:**
```
User click ❤️ (Like)
  ↓
Check: Có username trong localStorage?
  ├─ NO → Alert: "Vui lòng đặt tên người dùng trước!"
  │        Hướng dẫn: Click "👤 Chưa đặt tên" ở header
  │
  └─ YES → Toggle favorite API
            ↓
          Favorite = TRUE?
            ├─ YES → Auto-add username as category
            │         (Category thứ 6, ngoài 5 categories thường)
            │
            └─ NO → (Optional) Remove username category
```

**Code Implementation:**
```javascript
async function toggleFavorite(articleId, button) {
    // 1. Check username
    const username = getUsername();
    if (!username) {
        alert('⚠️ Vui lòng đặt tên người dùng trước!');
        return;
    }
    
    // 2. Toggle favorite
    const response = await fetch(`/api/article/${articleId}/favorite`, {
        method: 'POST'
    });
    
    // 3. If favorite = true → Add username category
    if (data.is_favorite) {
        await addUsernameCategoryToArticle(articleId, username);
    }
}
```

---

### 4️⃣ **Category System Update**

**Giới hạn mới:**
- ❌ **Bỏ giới hạn 100 categories** (user có thể tạo không giới hạn)
- ✅ **Giữ nguyên giới hạn 5 categories/bài viết** (cho categories thường)
- ✅ **Username là category thứ 6** (đặc biệt, ngoài 5 categories)

**Ví dụ:**
```
Bài viết có:
1. Technology      ← Category 1
2. Programming     ← Category 2
3. Python          ← Category 3
4. AI              ← Category 4
5. Tutorial        ← Category 5
6. Tuấn            ← Category 6 (Username - auto-add khi Like)
```

---

## 🔧 Technical Implementation

### **Files Changed:**

#### 1. `templates/base.html`
**Added:**
- User Profile Modal HTML
- Username display badge in header
- JavaScript functions:
  - `getUsername()` - Get from localStorage
  - `setUsername(name)` - Save to localStorage
  - `updateUsernameDisplay()` - Update header
  - `showUserProfileModal()` - Show modal
  - `hideUserProfileModal()` - Hide modal
  - `loadExistingUsernames()` - Load categories as suggestions
  - `saveUsername()` - Save and close modal

**Auto-show modal:**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    if (!getUsername()) {
        setTimeout(showUserProfileModal, 500);
    }
});
```

---

#### 2. `templates/index.html`
**Modified:**
- `toggleFavorite()` function:
  - Check username before allowing Like
  - Auto-add username category when favorite = true

**Added:**
- `addUsernameCategoryToArticle(articleId, username)` function
  - Get current categories
  - Add username if not exists
  - Update via API

---

#### 3. `templates/article.html`
**Removed:**
- `MAX_SYSTEM_CATEGORIES = 100` constant
- System category limit checks in:
  - `filterCategorySuggestions()`
  - `addCategoryToArticle()`

**Updated:**
- Tooltip: "Khi Like bài viết, tên bạn sẽ tự động được thêm vào"

---

## 🎯 Use Cases

### **Use Case 1: Người dùng mới lần đầu vào app**
```
1. Mở http://localhost:5000
2. Modal tự động hiện: "👤 Đặt tên người dùng"
3. Có 2 options:
   a. Chọn từ danh sách (nếu có categories)
   b. Nhập tên mới: "Tuấn"
4. Click "✅ Lưu"
5. Header hiển thị: "👤 Tuấn"
6. Username lưu vào localStorage
```

---

### **Use Case 2: Đổi tên người dùng**
```
1. Click "👤 Tuấn" ở header
2. Modal hiện ra
3. Chọn tên khác hoặc nhập tên mới: "Mai"
4. Click "✅ Lưu"
5. Header cập nhật: "👤 Mai"
6. Lần sau Like bài viết → Category là "Mai"
```

---

### **Use Case 3: Like bài viết (Happy path)**
```
1. User đã đặt tên: "Tuấn"
2. Click ❤️ (Like) trên bài viết
3. Bài viết được favorite
4. System tự động thêm category "Tuấn" (category thứ 6)
5. Notification: "✅ Đã thêm vào yêu thích"
6. Console log: "✅ Added username category: Tuấn"
```

---

### **Use Case 4: Like bài viết (Chưa có username)**
```
1. User chưa đặt tên (localStorage rỗng)
2. Click ❤️ (Like)
3. Alert hiển thị:
   "⚠️ Vui lòng đặt tên người dùng trước!
   
   Click vào '👤 Chưa đặt tên' ở header để đặt tên."
4. User click "OK"
5. Click "👤 Chưa đặt tên" → Modal hiện ra
6. Đặt tên và thử lại
```

---

### **Use Case 5: Filter bài viết theo username**
```
Scenario: Tìm tất cả bài viết mà "Tuấn" đã Like

1. Vào trang chủ
2. Click "📁 Chọn categories..."
3. Gõ "Tuấn" vào ô filter
4. Tick vào "📁 Tuấn"
5. Click "🔍 Tìm kiếm"
6. ✅ Kết quả: Tất cả bài viết có category "Tuấn"
   (= Tất cả bài viết mà Tuấn đã Like)
```

---

## 💡 Multi-User Scenarios

### **Scenario 1: Gia đình 3 người dùng chung**
```
Bố:  Username = "Bố"
Mẹ:  Username = "Mẹ"
Con: Username = "Con"

Mỗi người:
1. Lần đầu vào → Đặt tên riêng
2. Like bài viết → Username riêng được thêm vào
3. Filter theo username → Xem bài mình đã Like
```

**Categories tạo ra:**
```
- Technology (Category thường)
- Programming (Category thường)
- Bố (Username category - 15 bài viết)
- Mẹ (Username category - 8 bài viết)
- Con (Username category - 5 bài viết)
```

---

### **Scenario 2: Đổi username giữa chừng**
```
1. User A: Đặt tên "Tuấn"
2. Like 10 bài viết → 10 bài có category "Tuấn"
3. Sau đó đổi tên thành "Tuấn Anh"
4. Like thêm 5 bài → 5 bài mới có category "Tuấn Anh"

Kết quả:
- Category "Tuấn": 10 bài (cũ)
- Category "Tuấn Anh": 5 bài (mới)
- Tổng 2 categories riêng biệt
```

---

## 🚀 Workflow Khuyến nghị

### **Lần đầu sử dụng:**
```
1. Mở app → Modal hiện tự động
2. Nhập tên của bạn: "Tuấn"
3. Click "✅ Lưu"
4. Bắt đầu đọc và Like bài viết
```

### **Sử dụng hàng ngày:**
```
1. Mở app → Header hiển thị "👤 Tuấn"
2. Đọc bài viết
3. Like bài viết → Tự động tag "Tuấn"
4. Filter theo "Tuấn" → Xem bài đã Like
```

### **Đổi người dùng:**
```
1. Click "👤 Tuấn" ở header
2. Nhập tên mới: "Mai"
3. Click "✅ Lưu"
4. Từ giờ Like bài viết → Tag "Mai"
```

---

## 🔍 Debugging

### **Check localStorage:**
```javascript
// Open Console (F12)
localStorage.getItem('username'); // Get current username
localStorage.setItem('username', 'Test'); // Set test username
localStorage.removeItem('username'); // Clear username
```

### **Force show modal:**
```javascript
showUserProfileModal();
```

### **Check if username category was added:**
```javascript
// After Like, check article categories
fetch('/api/article/1/categories')
    .then(r => r.json())
    .then(d => console.log(d.categories));
```

---

## 📊 Database Impact

**Categories table:**
```sql
-- Before (với giới hạn 100):
SELECT COUNT(*) FROM categories; -- Max 100

-- After (không giới hạn):
SELECT COUNT(*) FROM categories; -- Có thể > 100
```

**Example data:**
```sql
id | name          | created_at
---+---------------+-------------------
1  | Technology    | 2025-11-24 ...
2  | Programming   | 2025-11-24 ...
3  | Tuấn          | 2025-11-24 ...
4  | Mai           | 2025-11-24 ...
5  | Hùng          | 2025-11-24 ...
...
```

---

## ✅ Summary of Changes

1. ✅ **Bỏ giới hạn 100 categories** - User có thể tạo không giới hạn
2. ✅ **User Profile Modal** - Chọn/nhập username lần đầu
3. ✅ **Username display** - Header badge với click để đổi tên
4. ✅ **Auto-add username category** - Khi Like → Category thứ 6
5. ✅ **LocalStorage persistence** - Username lưu local
6. ✅ **Multi-user support** - Nhiều người dùng chung app

---

## 🎉 Ready to Test!

**Bây giờ bạn có thể:**
1. ✅ Đặt tên người dùng (lần đầu hoặc bất kỳ lúc nào)
2. ✅ Like bài viết → Username tự động tag
3. ✅ Filter theo username → Xem bài đã Like
4. ✅ Đổi username → Like với tên mới
5. ✅ Tạo không giới hạn categories

**Truy cập:** http://localhost:5000

**Restart server để test!** 🚀
