# 👤 Checkbox "Bài viết của tôi" - Quick Filter

## ✨ Tính năng

Checkbox lọc nhanh bài viết của user hiện tại, nằm cạnh "Regex" và "Chỉ xem yêu thích"

---

## 🎯 UI Layout

```
Row 1: Keyword Search
┌─────────────────────────────────────────┐
│ [Nhập từ khóa...            ] [🔍 Tìm]  │
│                                          │
│ ☐ 🔧 Regex                              │
│ ☐ ❤️ Chỉ xem yêu thích                  │
│ ☑ 👤 Bài viết của Tuấn  ← NEW CHECKBOX  │
└─────────────────────────────────────────┘
```

---

## 🔧 Behavior

### **Auto-show khi user đăng nhập:**
```javascript
if (username) {
    // Show checkbox
    checkbox.style.display = 'flex';
    
    // Update label with username
    label.innerHTML = `👤 Bài viết của ${username}`;
}
```

### **Auto-check khi đang filter:**
```javascript
// If URL has ?categories=Tuấn
if (currentCategories.includes(username)) {
    checkbox.checked = true;
}
```

### **Khi tick checkbox:**
```javascript
// Checked → Add username to category filter
urlParams.append('categories', username);
window.location.search = urlParams.toString();
```

### **Khi untick checkbox:**
```javascript
// Unchecked → Remove username + add noclear
urlParams.delete('categories');
urlParams.set('noclear', '1');
window.location.search = urlParams.toString();
```

---

## 📊 Use Cases

### **Case 1: User mới vào trang chủ**
```
Given: User "Tuấn" đã đăng nhập
When: Load homepage
Then:
  ✅ Auto-filter by username
  ✅ Checkbox "Bài viết của Tuấn" hiện ra
  ✅ Checkbox auto-checked ☑
```

### **Case 2: Untick checkbox**
```
Given: Checkbox đang checked
When: User untick checkbox
Then:
  ✅ URL: /?noclear=1
  ✅ Hiển thị tất cả bài viết
  ✅ Checkbox unchecked ☐
```

### **Case 3: Tick lại checkbox**
```
Given: Checkbox đang unchecked
When: User tick checkbox
Then:
  ✅ URL: /?categories=Tuấn
  ✅ Chỉ hiển thị bài của Tuấn
  ✅ Checkbox checked ☑
```

### **Case 4: User chưa đăng nhập**
```
Given: Chưa có username
When: Load homepage
Then:
  ✅ Checkbox không hiện (display: none)
  ✅ Chỉ có 2 checkboxes: Regex & Favorites
```

---

## 🎨 Styling

```html
<label class="filter-checkbox" id="myArticlesCheckbox" style="display: none;">
    <input type="checkbox" name="my_articles" id="myArticlesInput" value="true">
    <span style="font-size: 13px;">👤 <strong>Bài viết của Tuấn</strong></span>
</label>
```

**CSS:**
- Font-size: 13px
- Bold username
- Icon: 👤
- Display: flex (when shown)

---

## 🔄 Integration với Auto-Filter

### **Flow:**
```
1. Page load
   ↓
2. Check username
   ├─ No username → Hide checkbox
   └─ Has username → Show checkbox
       ↓
3. Check URL params
   ├─ Has ?categories=Tuấn → Check checkbox ☑
   └─ No filter → Uncheck checkbox ☐
       ↓
4. Auto-filter (if no noclear)
   → Check checkbox ☑
   → Redirect to /?categories=Tuấn
```

---

## 🧪 Testing

### **Test 1: Checkbox visibility**
```
1. Clear localStorage
2. Load homepage
   → ✅ Checkbox hidden

3. Set username "Tuấn"
4. Reload
   → ✅ Checkbox visible
   → ✅ Label: "Bài viết của Tuấn"
```

### **Test 2: Checkbox state sync**
```
1. Auto-filter applies (?categories=Tuấn)
   → ✅ Checkbox checked

2. Untick checkbox
   → ✅ URL: /?noclear=1
   → ✅ Show all articles

3. Tick checkbox
   → ✅ URL: /?categories=Tuấn
   → ✅ Filter applied
```

### **Test 3: Multiple filters**
```
1. Tick "Bài viết của Tuấn"
2. Tick "Chỉ xem yêu thích"
3. Type search keyword
   → ✅ All 3 filters work together
   → ✅ URL: /?categories=Tuấn&favorites=true&q=test
```

---

## 🆚 So sánh với Category Dropdown

### **OLD: Category Dropdown**
```
Pros:
  ✅ Có thể chọn nhiều categories
  ✅ Filter input tìm nhanh
  ✅ Cleanup button 🔄

Cons:
  ❌ Phải mở dropdown
  ❌ 2-3 clicks để filter
  ❌ Không trực quan
```

### **NEW: Checkbox "Bài viết của tôi"**
```
Pros:
  ✅ 1-click toggle
  ✅ Hiển thị ngay trên UI
  ✅ Trực quan, dễ dùng
  ✅ Auto-check khi filter

Cons:
  ❌ Chỉ filter 1 user (nhưng đây là use case chính)
```

---

## 💡 Best Practices

### **1. Default State:**
```
First visit → Auto-filter → Checkbox checked ☑
Click untick → Show all → Checkbox unchecked ☐ + noclear=1
Next visit → No auto-filter (due to noclear)
```

### **2. Label Update:**
```javascript
// Always show current username in label
const label = checkbox.querySelector('span');
label.innerHTML = `👤 <strong>Bài viết của ${username}</strong>`;
```

### **3. Event Handler:**
```javascript
// Use optional chaining for safety
document.getElementById('myArticlesInput')?.addEventListener('change', ...)
```

---

## 🚀 Implementation Summary

**Files changed:**
- `templates/index.html` - Added checkbox HTML
- `templates/index.html` - Added show/hide logic
- `templates/index.html` - Added checkbox change handler

**New Elements:**
- `#myArticlesCheckbox` - Label container
- `#myArticlesInput` - Checkbox input

**JavaScript Functions:**
- Auto-show checkbox when username exists
- Auto-check when filtering by username
- Handle checkbox change → Update URL params

---

## ✅ Status

**Implemented:** ✅  
**Tested:** Pending  
**Server:** http://localhost:5000

**Quick Test:**
1. Set username "Tuấn"
2. Refresh homepage
3. ✅ See checkbox "👤 Bài viết của Tuấn" (checked)
4. Untick → See all articles
5. Tick → See only Tuấn's articles

**Perfect for:** Quick toggle giữa "My articles" và "All articles" chỉ với 1 click! 🎯
