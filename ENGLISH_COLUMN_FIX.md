# English Column Display Fix

## Ngày: 24/11/2025

## Vấn đề
Phần nội dung Tiếng Anh bị mất chữ và không tự xuống dòng, thanh scroll cũng mất.

## Nguyên nhân
1. **Word Wrap** không được set → text tràn ra ngoài
2. **Grid Column Width** có thể bị 0 hoặc quá nhỏ
3. **Overflow** settings không rõ ràng

## Giải pháp

### 1. Thêm Word Wrap cho `.bilingual-column`
```css
.bilingual-column {
    padding: 20px;
    overflow-y: auto;
    overflow-x: hidden;
    max-height: 80vh;
    min-width: 0; /* Prevent grid blowout */
    background-color: #fafafa;
    border-radius: 8px;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    word-wrap: break-word;        /* ✅ NEW */
    overflow-wrap: break-word;    /* ✅ NEW */
}
```

**Kết quả**: Text sẽ tự động xuống dòng thay vì tràn ra ngoài

---

### 2. Thêm Word Wrap cho `.bilingual-content`
```css
.bilingual-content {
    transition: font-size 0.3s ease;
    width: 100%;                  /* ✅ NEW */
    word-wrap: break-word;        /* ✅ NEW */
    overflow-wrap: break-word;    /* ✅ NEW */
    white-space: normal;          /* ✅ NEW */
}

.bilingual-content * {            /* ✅ NEW */
    max-width: 100%;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
```

**Kết quả**: Tất cả elements bên trong (p, div, span, table, etc.) đều wrap đúng

---

### 3. Focus Mode - Đảm bảo Scroll & Display
```css
body.focus-mode .bilingual-column {
    max-height: 100vh;
    height: 100vh;
    border-radius: 0;
    overflow-y: auto !important;     /* ✅ IMPORTANT */
    overflow-x: hidden;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

body.focus-mode .bilingual-vi,
body.focus-mode .bilingual-en {
    overflow-y: auto !important;     /* ✅ Explicit scroll */
    overflow-x: hidden;
}

body.focus-mode .bilingual-content {
    width: 100%;
    max-width: 100%;
}
```

**Kết quả**: Trong Focus Mode, cả 2 columns đều có scroll và hiển thị đúng

---

### 4. Grid Column Width Validation
```javascript
function applyColumnWidth() {
    const container = document.querySelector('.bilingual-sync-container');
    const display = document.getElementById('columnWidthValue');
    
    if (container && display) {
        const leftPercent = columnWidthPercent;
        const rightPercent = 100 - columnWidthPercent;
        
        // ✅ Ensure columns are visible
        if (leftPercent < 20) columnWidthPercent = 20;
        if (leftPercent > 80) columnWidthPercent = 80;
        
        const finalLeft = Math.max(20, Math.min(80, leftPercent));
        const finalRight = 100 - finalLeft;
        
        container.style.gridTemplateColumns = `${finalLeft}% 4px ${finalRight}%`;
        display.textContent = finalLeft + '%';
        
        // Update slider
        const slider = document.getElementById('columnWidthSlider');
        if (slider) {
            slider.value = columnWidthPercent;
        }
    }
}
```

**Kết quả**: Grid columns luôn có width hợp lệ (20%-80%), không bao giờ = 0

---

## CSS Properties Explained

### `word-wrap: break-word`
- Cho phép từ dài **break ở giữa** nếu không fit
- Cần thiết cho URLs, emails, code dài

### `overflow-wrap: break-word`
- Modern version của `word-wrap`
- Better browser support

### `white-space: normal`
- Cho phép text **wrap bình thường**
- Override any `white-space: nowrap` từ parent

### `min-width: 0`
- Fix cho **grid/flexbox blowout**
- Prevent children từ forcing parent grow beyond grid

### `overflow-y: auto !important`
- **Force scroll** khi cần
- `!important` để override mọi CSS khác

---

## Testing Checklist

- [x] English column hiển thị text đầy đủ
- [x] English column có scroll khi nội dung dài
- [x] Text tự động xuống dòng (word wrap)
- [x] Không có text tràn ra ngoài
- [x] Grid columns có width đúng (20-80%)
- [x] Focus Mode - cả 2 columns hiển thị OK
- [x] Focus Mode - có scroll cho cả 2 columns
- [x] Dark Mode - text vẫn visible
- [x] Mobile/iPad - text wrap đúng
- [x] Long words/URLs - break đúng

---

## Files Modified
- `templates/article.html`
  - CSS: `.bilingual-column`, `.bilingual-content`
  - CSS: Focus Mode styles
  - JavaScript: `applyColumnWidth()` validation

---

## Conclusion
Vấn đề phần Tiếng Anh mất chữ và scroll đã được fix bằng cách:
1. ✅ Thêm `word-wrap` và `overflow-wrap` 
2. ✅ Explicit `overflow-y: auto !important`
3. ✅ Grid width validation (20%-80%)
4. ✅ `min-width: 0` để prevent grid blowout

English column giờ hiển thị đầy đủ, scroll mượt mà, và text wrap đúng! 🎉
