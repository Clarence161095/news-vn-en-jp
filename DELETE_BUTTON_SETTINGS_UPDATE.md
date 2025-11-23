# Delete Button & Ruby Display Fixes

## Ngày cập nhật: 24/11/2025

## Các thay đổi / Changes

### 1. ✅ Di chuyển nút Xóa bài viết vào Settings Panel

**Vấn đề**: Nút xóa bài viết ở ngay đầu trang dễ bấm nhầm.

**Giải pháp**:
- Di chuyển nút xóa từ đầu trang vào cuối Settings Panel
- Thêm phần "Vùng nguy hiểm" (Danger Zone) với border màu đỏ
- Đặt ở cuối cùng trong danh sách cài đặt để tránh bấm nhầm
- Thêm confirm dialog khi bấm xóa với thông báo rõ ràng hơn

**Code**:
```html
<!-- Delete Article Button -->
<div class="settings-section" style="border-top: 2px solid #e74c3c; padding-top: 15px; margin-top: 10px;">
    <span class="settings-label" style="color: #e74c3c;">⚠️ Vùng nguy hiểm</span>
    <form action="{{ url_for('delete_article', article_id=article['id']) }}" method="POST" 
          onsubmit="return confirm('Bạn có chắc chắn muốn xóa bài viết này? Hành động này không thể hoàn tác!');">
        <button type="submit" style="...">
            🗑️ Xóa bài viết
        </button>
    </form>
</div>
```

**CSS**:
```css
.settings-panel {
    max-height: calc(100vh - 120px);
    overflow-y: auto; /* Cho phép scroll nếu quá dài */
}

.settings-panel form button[type="submit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}
```

### 2. ✅ Fix Ruby/Furigana display (IPA phonetics)

**Vấn đề**: Sau khi thay đổi `display: inline`, furigana/IPA bị vỡ layout.

**Giải pháp**:
- Khôi phục `display: inline-flex` cho ruby elements
- Giữ `flex-direction: column` để IPA hiển thị đúng vị trí
- Đặt `line-height: 1.6` cho ruby, `line-height: 1` cho rt
- Giữ nguyên cơ chế click/hover để hiện IPA popup

**Code**:
```css
ruby {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    line-height: 1.6;
}

ruby > rb {
    line-height: inherit; /* Text chính */
}

ruby > rt {
    line-height: 1; /* IPA/furigana */
}
```

### 3. ✅ Đảm bảo cột EN giống cột VN

**Đã kiểm tra**:
```css
.bilingual-vi {
    background: #ffffff;
    border-right: 1px solid #e0e0e0;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}

.bilingual-en {
    background: #ffffff;
    border-left: 1px solid #e0e0e0;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}
```

✅ **Cả 2 cột đều giống nhau về:**
- Background color
- Word wrapping
- Text overflow handling
- White space behavior

## Thứ tự trong Settings Panel

1. **IPA (Phiên âm)** - Toggle switch
2. **🌙 Dark Mode** - Toggle switch
3. **🎯 Focus Mode** - Toggle switch
4. **📝 Kích thước chữ** - A- / A / A+ buttons
5. **📏 Độ rộng cột VN** - Slider (chỉ hiện khi ở mode Song Ngữ)
6. **⚠️ Vùng nguy hiểm** - Delete button (cuối cùng)

## Tính năng an toàn

✅ Nút xóa ở cuối cùng - khó bấm nhầm  
✅ Border đỏ cảnh báo "Vùng nguy hiểm"  
✅ Confirm dialog với thông báo rõ ràng  
✅ Nút màu đỏ nổi bật với gradient  
✅ Hover effect với shadow để người dùng nhận biết  

## Cách sử dụng

1. Mở bài viết
2. Nhấn nút ⚙️ Settings (góc dưới bên phải)
3. Scroll xuống cuối Settings Panel
4. Thấy phần "⚠️ Vùng nguy hiểm"
5. Nhấn "🗑️ Xóa bài viết"
6. Confirm trong dialog

---

**Files đã sửa**: `templates/article.html`
