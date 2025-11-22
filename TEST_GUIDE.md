# 🧪 Test Refactored App

## Kiểm tra App đang chạy

App đang chạy tại: http://127.0.0.1:5000

⚠️ **Có warning**: "pykakasi not installed" - Cần kiểm tra virtual environment

## Test Flow

### 1. Import bài viết mẫu đơn giản

```bash
# File mẫu: sample_simple.json (chỉ có nội dung gốc, KHÔNG có IPA/Furigana)
```

1. Vào http://127.0.0.1:5000/import
2. Copy nội dung từ `sample_simple.json`
3. Click "Import"
4. **Kết quả mong đợi**: Import thành công, thông báo "IPA và Furigana sẽ được tạo tự động"

### 2. Xem bài viết với IPA tự động

1. Click vào bài viết "AWS for Beginners"
2. Chọn mode 🇬🇧 **English (IPA)**
3. **Kết quả mong đợi**: 
   - Từ "Amazon" → `<ruby>Amazon<rt>/ˈæməˌzɑn/</rt></ruby>`
   - Từ "Services" → `<ruby>Services<rt>/ˈsɝvəsəz/</rt></ruby>`
   - Tất cả từ tiếng Anh đều có IPA

### 3. Xem bài viết với Furigana tự động

1. Click vào bài viết "初心者向けAWS"
2. Chọn mode 🇯🇵 **日本語 (Furigana)**
3. **Kết quả mong đợi**:
   - Kanji "初心者" → `<ruby>初心者<rt>しょしんしゃ</rt></ruby>`
   - Kanji "世界" → `<ruby>世界<rt>せかい</rt></ruby>`
   - Tất cả Kanji đều có Furigana

### 4. Test Toggle Furigana

1. Ở trang bài viết tiếng Nhật
2. Click nút 🎌 góc phải dưới
3. **Kết quả mong đợi**: Tất cả Furigana ẩn
4. Click lại → Hiện lại
5. Click vào 1 từ riêng lẻ → Chỉ từ đó hiện Furigana

### 5. Test Xóa bài viết

1. Trang chủ: Click nút 🗑️ **Xóa**
2. Confirm dialog xuất hiện
3. Click OK
4. **Kết quả mong đợi**: Bài viết bị xóa, quay về trang chủ

## Kiểm tra Database

```bash
sqlite3 articles.db
```

```sql
-- Xem cấu trúc bảng (không còn content_en_ipa và content_jp_furigana)
.schema articles

-- Kết quả mong đợi:
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_vi TEXT,
    title_en TEXT,
    title_jp TEXT,
    content_vi TEXT,
    content_en TEXT,
    content_jp TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Xem dữ liệu
SELECT id, title_vi, title_en, category FROM articles;
```

## Kiểm tra thư viện

```bash
cd d:/01.\ Project/news-vn-en-jp

# Test pykakasi
py -c "from pykakasi import kakasi; kks = kakasi(); result = kks.convert('日本語'); print(result)"

# Kết quả mong đợi:
[{'orig': '日本語', 'hira': 'にほんご', 'kana': 'ニホンゴ', 'kunrei': 'nihongo', 'hepburn': 'nihongo', 'passport': 'nihongo'}]

# Test eng-to-ipa
py -c "import eng_to_ipa as ipa; print(ipa.convert('hello'))"

# Kết quả mong đợi:
həˈloʊ
```

## Sửa lỗi pykakasi

Nếu có warning "pykakasi not installed":

```bash
# Kiểm tra Python đang dùng
py -c "import sys; print(sys.executable)"

# Cài lại pykakasi vào đúng Python
py -m pip install --force-reinstall pykakasi==2.2.1

# Restart Flask app
# Ctrl+C để dừng
py app.py
```

## API Test

```bash
# Test API endpoint (với IPA và Furigana tự động)
curl http://127.0.0.1:5000/api/article/3
```

**Kết quả mong đợi**: JSON có thêm fields `content_en_ipa` và `content_jp_furigana` được tạo tự động.

## Performance Test

```bash
# Test tốc độ tạo IPA/Furigana
py -c "
from app import generate_ipa_html, generate_furigana_html
import time

text_en = 'Amazon Web Services is the world most comprehensive cloud platform'
text_jp = '日本語の文章を自動的に変換します'

# Test IPA
start = time.time()
result = generate_ipa_html(text_en)
print(f'IPA generation: {time.time() - start:.4f}s')

# Test Furigana
start = time.time()
result = generate_furigana_html(text_jp)
print(f'Furigana generation: {time.time() - start:.4f}s')
"
```

## Checklist

- [ ] App khởi động không lỗi
- [ ] Import JSON đơn giản (không có IPA/Furigana)
- [ ] IPA được tạo tự động khi xem bài tiếng Anh
- [ ] Furigana được tạo tự động khi xem bài tiếng Nhật
- [ ] Toggle Furigana hoạt động
- [ ] Xóa bài viết hoạt động
- [ ] Database chỉ lưu nội dung gốc
- [ ] API trả về kèm IPA/Furigana tự động
- [ ] 7 language modes hoạt động
- [ ] Responsive trên mobile

## Troubleshooting

### 1. Warning: pykakasi not installed
**Nguyên nhân**: Cài vào virtual environment khác
**Giải pháp**: 
```bash
py -m pip install --force-reinstall pykakasi==2.2.1
```

### 2. IPA không hiển thị
**Nguyên nhân**: eng-to-ipa chưa cài
**Giải pháp**:
```bash
py -m pip install eng-to-ipa==0.0.2
```

### 3. Database lỗi schema
**Nguyên nhân**: Database cũ còn content_en_ipa, content_jp_furigana
**Giải pháp**:
```bash
rm articles.db
py app.py  # Tạo database mới
```

---

**Status**: ✅ App đang chạy, cần test các tính năng
**URL**: http://127.0.0.1:5000
