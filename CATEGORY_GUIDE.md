# 📁 Hướng dẫn sử dụng Category System

## ✨ Tính năng chính

### 1️⃣ **Tìm kiếm theo từ khóa**
- 🔍 Tìm kiếm trong **tiêu đề** và **nội dung** (cả Việt và Anh)
- 💡 Tìm kiếm **có chứa** từ khóa (không cần chính xác 100%)
- ✅ Ví dụ: Tìm "Tuấn" → Tìm thấy bài có "Tuấn Anh", "Văn Tuấn",...
- 🔧 Hỗ trợ **Regex** (checkbox "Sử dụng Regex")

### 2️⃣ **Lọc theo Categories**
- 📁 Chọn nhiều categories cùng lúc
- 🏷️ Hiển thị dạng tags màu tím
- ❌ Click nút "×" để bỏ chọn category

### 3️⃣ **Click vào tiêu đề**
- 📰 Click vào title bất kỳ → Mở bài viết ở chế độ **Song Ngữ**
- 🎨 Hover effect: title chuyển màu xanh

### 4️⃣ **Quản lý Categories trong bài viết**

#### 📍 Vị trí:
Mở bài viết → Settings (⚙️) → **📁 Quản lý Categories** (section màu tím)

#### ✏️ Thêm Category:
1. Click vào ô input "Chọn hoặc nhập category mới..."
2. Dropdown sẽ hiện ra với 2 phần:
   - **"Chọn từ danh sách"**: Categories đã có sẵn
   - **"✨ Tạo mới"**: Nếu nhập tên category chưa có

3. Chọn từ dropdown HOẶC nhập tên mới → Enter/Click "➕ Thêm Category"

#### 🚫 Giới hạn:
- **5 categories/bài viết** (tối đa)
- **100 categories toàn hệ thống** (tối đa)
- Counter hiển thị: `(2/5)` - đang có 2 categories, tối đa 5

#### 🗑️ Xóa Category:
Click vào nút **×** trên tag category

---

## 🎯 Use Cases

### Use Case 1: Tìm bài viết về "coding"
```
1. Vào trang chủ
2. Nhập "coding" vào ô "🔍 Tìm kiếm theo từ khóa"
3. Click "🔍 Tìm kiếm"
4. Kết quả: Tất cả bài có chứa "coding" trong title hoặc content
```

### Use Case 2: Lọc bài viết về "Technology"
```
1. Vào trang chủ
2. Click "📁 Chọn categories..."
3. Tick vào checkbox "Technology"
4. Click "🔍 Tìm kiếm"
5. Kết quả: Chỉ bài viết có category "Technology"
```

### Use Case 3: Thêm category cho bài viết
```
1. Mở bài viết bất kỳ
2. Click icon ⚙️ Settings
3. Tìm section "📁 Quản lý Categories" (màu tím)
4. Click "▼" để mở (nếu đang đóng)
5. Click vào ô input → Dropdown hiện ra
6. Chọn category có sẵn HOẶC nhập tên mới
7. Click "➕ Thêm Category"
8. ✅ Category được lưu tự động!
```

### Use Case 4: Tìm bài viết yêu thích về "Python"
```
1. Vào trang chủ
2. Nhập "Python" vào ô search
3. Tick checkbox "❤️ Chỉ xem yêu thích"
4. Click "🔍 Tìm kiếm"
5. Kết quả: Chỉ bài yêu thích có chứa "Python"
```

---

## 🔧 API Endpoints

### GET `/`
**Homepage với search & filter**
```
Query params:
- q: Từ khóa tìm kiếm
- regex: true/false (Sử dụng regex)
- categories[]: Danh sách category (multi-select)
- favorites: true/false (Chỉ xem yêu thích)
```

### GET `/api/categories`
**Lấy tất cả categories trong hệ thống**
```json
{
  "success": true,
  "categories": [
    {"id": 1, "name": "Technology"},
    {"id": 2, "name": "Python"}
  ]
}
```

### GET `/api/article/<id>/categories`
**Lấy categories của 1 bài viết**
```json
{
  "success": true,
  "categories": [
    {"id": 1, "name": "Technology"}
  ]
}
```

### POST `/api/article/<id>/categories`
**Cập nhật categories cho bài viết**
```json
Request:
{
  "categories": ["Technology", "Python", "AI"]
}

Response:
{
  "success": true,
  "message": "Đã cập nhật 3 categories"
}
```

---

## 🗄️ Database Schema

```sql
-- Categories table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Article-Category relationship (many-to-many)
CREATE TABLE article_categories (
    article_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Articles with favorite flag
ALTER TABLE articles ADD COLUMN is_favorite INTEGER DEFAULT 0;
```

---

## 💡 Tips & Tricks

1. **Autocomplete thông minh**: Dropdown tự động lọc theo từ nhập vào
2. **Enter để thêm nhanh**: Nhập category → Enter (không cần click button)
3. **Click outside để đóng**: Click ra ngoài dropdown → Tự động đóng
4. **Counter màu đỏ**: Khi đạt 5/5 categories → Counter chuyển đỏ, button disabled
5. **Tooltip hữu ích**: Hover vào button để xem hướng dẫn
6. **Lưu tự động**: Mọi thay đổi category đều được lưu ngay lập tức

---

## 🚀 Next Steps

Bây giờ bạn có thể:
1. ✅ Tìm kiếm bài viết theo từ khóa
2. ✅ Lọc theo categories
3. ✅ Thêm/xóa categories cho bài viết
4. ✅ Click vào title để đọc bài
5. ✅ Đánh dấu bài viết yêu thích

**Truy cập:** http://localhost:5000
