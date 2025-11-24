# 🧪 Test Guide - Multi-User Features

**Date:** 2025-11-24  
**Version:** 2.0.0

---

## 🎯 Test Scenarios

### ✅ **Test 1: Auto-Filter by Username**

#### **Scenario 1.1: First-time user with username**
```
Given: User "Tuấn" đã đặt tên trong localStorage
When: Vào http://localhost:5000
Then:
  ✅ Auto-redirect to: /?categories=Tuấn
  ✅ Chỉ hiển thị bài viết có category "Tuấn"
  ✅ Button "❌ Xóa bộ lọc 'Tuấn'" xuất hiện
```

#### **Scenario 1.2: User without username**
```
Given: Chưa đặt username (localStorage empty)
When: Vào http://localhost:5000
Then:
  ✅ Không auto-filter
  ✅ Hiển thị tất cả bài viết
  ✅ Modal "👤 Đặt tên người dùng" hiện ra
```

#### **Scenario 1.3: Clear filter**
```
Given: Đang filter by username
When: Click "❌ Xóa bộ lọc 'Tuấn'"
Then:
  ✅ Redirect to: /?noclear=1
  ✅ Hiển thị tất cả bài viết
  ✅ Button "Clear Filter" biến mất
```

#### **Scenario 1.4: After clearing filter**
```
Given: URL has ?noclear=1
When: Reload trang (F5)
Then:
  ✅ Không auto-filter
  ✅ Vẫn hiển thị tất cả bài viết
```

---

### ✅ **Test 2: Delete Protection**

#### **Scenario 2.1: Creator deletes own article**
```
Given: 
  - User "Tuấn" logged in
  - Article ID=1 created_by="Tuấn"
When: Click "🗑️ Xóa bài viết"
Then:
  ✅ Confirm dialog: "Bạn có chắc chắn muốn xóa..."
  ✅ Click OK → Alert: "✅ Bài viết đã được xóa!"
  ✅ Redirect to homepage
  ✅ Article không còn trong danh sách
```

#### **Scenario 2.2: Non-creator tries to delete**
```
Given:
  - User "Mai" logged in
  - Article ID=1 created_by="Tuấn"
When: Click "🗑️ Xóa bài viết"
Then:
  ✅ Confirm dialog: "Bạn có chắc chắn muốn xóa..."
  ✅ Click OK → Alert: "⛔ Chỉ người tạo (Tuấn) mới có thể xóa bài viết này!"
  ✅ Vẫn ở trang bài viết
  ✅ Article vẫn còn
```

#### **Scenario 2.3: Delete old article (no creator)**
```
Given:
  - User "Mai" logged in
  - Article ID=5 created_by=NULL (old article)
When: Click "🗑️ Xóa bài viết"
Then:
  ✅ Confirm dialog: "Bạn có chắc chắn muốn xóa..."
  ✅ Click OK → Alert: "✅ Bài viết đã được xóa!"
  ✅ Article bị xóa (backward compatibility)
```

#### **Scenario 2.4: Delete without username**
```
Given: User chưa đặt tên (localStorage empty)
When: Click "🗑️ Xóa bài viết"
Then:
  ✅ Alert: "⚠️ Vui lòng đặt tên người dùng trước!"
  ✅ Không có confirm dialog
  ✅ Article vẫn còn
```

---

### ✅ **Test 3: User-Specific Favorites**

#### **Scenario 3.1: User A likes article**
```
Given: User "Tuấn" logged in
When: Click ❤️ (Like) on Article ID=1
Then:
  ✅ Heart icon: 🤍 → ❤️
  ✅ Notification: "Tuấn đã thêm vào yêu thích"
  ✅ Auto-add category "Tuấn" to article
```

#### **Scenario 3.2: User B views same article**
```
Given:
  - User "Mai" logged in
  - Article ID=1 liked by "Tuấn" only
When: View Article ID=1
Then:
  ✅ Heart icon: 🤍 (not ❤️)
  ✅ Mai chưa like bài này
```

#### **Scenario 3.3: User B also likes**
```
Given: User "Mai" logged in
When: Click ❤️ on Article ID=1
Then:
  ✅ Heart icon: 🤍 → ❤️
  ✅ Notification: "Mai đã thêm vào yêu thích"
  ✅ Auto-add category "Mai" to article
  ✅ Article now has 2 categories: "Tuấn", "Mai"
```

#### **Scenario 3.4: Unlike article**
```
Given: User "Tuấn" đã like Article ID=1
When: Click ❤️ (Unlike)
Then:
  ✅ Heart icon: ❤️ → 🤍
  ✅ Notification: "Tuấn đã bỏ yêu thích"
  ✅ Category "Tuấn" vẫn còn (intentional - không tự động xóa)
```

#### **Scenario 3.5: Filter by favorites**
```
Given: User "Tuấn" logged in
When: 
  - Tick checkbox "❤️ Chỉ xem yêu thích"
  - Click "🔍 Tìm kiếm"
Then:
  ✅ Chỉ hiển thị bài viết Tuấn đã like
  ✅ Không hiển thị bài viết Mai like
```

---

### ✅ **Test 4: Import with Auto-Category**

#### **Scenario 4.1: Import with username**
```
Given: User "Tuấn" logged in
When: 
  - Vào /import
  - Paste JSON: {"title_vi": "Test", ...}
  - Click "✅ Import Bài Viết"
Then:
  ✅ Success message: "Đã import thành công 1 bài viết!"
  ✅ Article created with created_by="Tuấn"
  ✅ Auto-add category "Tuấn"
  ✅ Console log: "✅ Auto-added category 'Tuấn' to imported article ID X"
```

#### **Scenario 4.2: Import without username**
```
Given: User chưa đặt tên
When: Import JSON
Then:
  ✅ Article created with created_by=NULL
  ✅ Không auto-add category
  ✅ Console log: "⚠️ No username set, importing without auto-category"
```

#### **Scenario 4.3: Import multiple articles**
```
Given: User "Mai" logged in
When: Import JSON array [article1, article2, article3]
Then:
  ✅ All 3 articles created with created_by="Mai"
  ✅ All 3 articles have category "Mai"
  ✅ Success message: "Đã import thành công 3 bài viết!"
```

---

### ✅ **Test 5: Category Cleanup**

#### **Scenario 5.1: Manual cleanup with used categories**
```
Given: 
  - Category "Tuấn" has 5 articles
  - Category "Mai" has 3 articles
When: Click 🔄 (Cleanup button)
Then:
  ✅ Alert: "🧹 Đã xóa 0 categories"
  ✅ Stats: "Categories trước: 2 | sau: 2 | Tổng liên kết: 8"
```

#### **Scenario 5.2: Cleanup with unused categories**
```
Given:
  - Category "OldTag" has 0 articles
  - Category "Tuấn" has 5 articles
When: Click 🔄
Then:
  ✅ Alert: "🧹 Đã xóa 1 categories"
  ✅ Stats: "Categories trước: 2 | sau: 1 | Tổng liên kết: 5"
  ✅ Page reload
  ✅ "OldTag" không còn trong dropdown
```

---

## 🔧 Manual Testing Steps

### **Setup:**
```bash
# 1. Make sure server is running
http://localhost:5000

# 2. Open browser console (F12)
# 3. Check localStorage
localStorage.getItem('username')

# 4. Clear localStorage (if needed)
localStorage.clear()
```

---

### **Test Flow 1: New User Experience**
```
Step 1: Clear localStorage
  > localStorage.clear()

Step 2: Open homepage
  > http://localhost:5000
  ✅ Modal "👤 Đặt tên người dùng" hiện ra

Step 3: Set username
  > Nhập "Tuấn" → Click "✅ Lưu"
  ✅ Header hiển thị "👤 Tuấn"
  ✅ localStorage.username = "Tuấn"

Step 4: Import test article
  > Vào /import
  > Paste JSON:
  {
    "title_vi": "Bài test của Tuấn",
    "title_en": "Tuan's Test Article",
    "content_vi": "Nội dung test",
    "content_en": "Test content"
  }
  > Click "✅ Import"
  ✅ Success: "Đã import thành công 1 bài viết!"

Step 5: Check homepage
  > Vào /
  ✅ Auto-filter: /?categories=Tuấn
  ✅ Chỉ hiển thị bài "Bài test của Tuấn"
  ✅ Button "❌ Xóa bộ lọc 'Tuấn'" xuất hiện

Step 6: Clear filter
  > Click "❌ Xóa bộ lọc 'Tuấn'"
  ✅ URL: /?noclear=1
  ✅ Hiển thị tất cả bài viết

Step 7: Try to like
  > Click ❤️ on any article
  ✅ Heart: 🤍 → ❤️
  ✅ Category "Tuấn" added

Step 8: Try to delete
  > Click vào bài "Bài test của Tuấn"
  > Click "🗑️ Xóa bài viết"
  ✅ Confirm dialog
  > Click OK
  ✅ Success: "✅ Bài viết đã được xóa!"
  ✅ Redirect to /
```

---

### **Test Flow 2: Multi-User**
```
Step 1: User A (Tuấn) creates article
  > localStorage.setItem('username', 'Tuấn')
  > Import article
  ✅ created_by = "Tuấn"

Step 2: User B (Mai) logs in
  > localStorage.setItem('username', 'Mai')
  > Reload page
  ✅ Auto-filter by "Mai" (empty results if Mai has no articles)

Step 3: Mai tries to delete Tuấn's article
  > Open Tuấn's article
  > Click "🗑️ Xóa bài viết"
  ✅ Error: "⛔ Chỉ người tạo (Tuấn) mới có thể xóa!"

Step 4: Mai likes Tuấn's article
  > Click ❤️
  ✅ Heart: 🤍 → ❤️
  ✅ Category "Mai" added

Step 5: Tuấn checks favorites
  > localStorage.setItem('username', 'Tuấn')
  > Reload homepage
  ✅ Auto-filter by "Tuấn"
  ✅ Tuấn's articles shown
  ✅ Article Mai liked NOT in Tuấn's favorites (separate favorites)
```

---

## 📊 Expected Results Summary

### **Homepage Behavior:**
| User State | URL | Result |
|------------|-----|--------|
| No username | `/` | Show all articles, no filter |
| Username="Tuấn" | `/` | Auto-redirect to `/?categories=Tuấn` |
| Username="Tuấn" | `/?noclear=1` | Show all articles, no auto-filter |
| Username="Tuấn" | `/?categories=Tuấn` | Show only Tuấn's articles, Clear button visible |

### **Delete Permissions:**
| User | Article Creator | Can Delete? | Error Message |
|------|----------------|-------------|---------------|
| Tuấn | Tuấn | ✅ Yes | - |
| Mai | Tuấn | ❌ No | "⛔ Chỉ người tạo (Tuấn)..." |
| Mai | NULL (old) | ✅ Yes | - |
| No username | Any | ❌ No | "⚠️ Vui lòng đặt tên..." |

### **Favorites Behavior:**
| Action | Result |
|--------|--------|
| Tuấn likes Article 1 | Heart ❤️ for Tuấn only |
| Mai views Article 1 | Heart 🤍 (not liked by Mai) |
| Mai likes Article 1 | Heart ❤️ for Mai, Article has 2 likes |
| Tuấn unlikes | Heart 🤍 for Tuấn, Mai's like remains |

---

## 🐛 Known Issues to Check

1. **Auto-filter infinite loop:**
   - Check if page keeps reloading
   - Check if noclear param is set correctly

2. **Delete button not responding:**
   - Check console for errors
   - Verify username in localStorage

3. **Favorites not loading:**
   - Check console: "✅ Loaded X favorites for USERNAME"
   - Verify API endpoint works: `/api/user/Tuấn/favorites`

4. **Clear filter button not showing:**
   - Check if filtering by username
   - Check `selectedCategories` container exists

---

## ✅ Success Criteria

All tests pass if:
- ✅ Auto-filter works on first visit
- ✅ Clear filter button works
- ✅ Only creator can delete
- ✅ Favorites are user-specific
- ✅ Import sets created_by
- ✅ No console errors
- ✅ No infinite redirects

**Status:** Ready for testing  
**Server:** http://localhost:5000  
**Documentation:** CHANGELOG_v2.md
