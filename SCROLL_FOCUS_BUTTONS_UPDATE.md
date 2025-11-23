# Scroll Sync & Focus Mode Button Updates

## Ngày: 24/11/2025

## Tóm tắt các thay đổi

### 1. 🔄 Scroll Synchronization (Đảo chiều)
**Trước đây**: Cả Vietnamese và English đều có scroll listeners → xung đột → scroll khựng

**Bây giờ**: 
- ✅ **English scrolls naturally** (tự nhiên mượt mà)
- ✅ **Vietnamese follows** (chỉ follow theo)
- ✅ Không có xung đột, không có timeout/throttle
- ✅ Sử dụng `requestAnimationFrame` cho 60 FPS

```javascript
// ONLY English has scroll listener - Vietnamese just follows
enColumn.addEventListener('scroll', function() {
    if (isScrollSyncing) return;
    isScrollSyncing = true;
    
    // Calculate scroll percentage from English
    const scrollPercentage = enColumn.scrollTop / (enColumn.scrollHeight - enColumn.clientHeight);
    
    // Apply to Vietnamese column
    viColumn.scrollTop = scrollPercentage * (viColumn.scrollHeight - viColumn.clientHeight);
    
    // Release immediately for smooth scrolling
    requestAnimationFrame(() => {
        isScrollSyncing = false;
    });
}, { passive: true });
```

---

### 2. 🎯 Focus Mode Button (Quick Access)

**Vị trí**: Góc dưới bên trái (FIXED)

**Chức năng**:
- 🎯 Icon khi OFF
- ✅ Icon khi ON
- Click để bật/tắt nhanh Focus Mode
- Sync với toggle trong Settings panel
- Keyboard shortcut: `Ctrl+F`

**Màu sắc**:
- Normal: Tím gradient (#9b59b6 → #8e44ad)
- Active: Xanh lá gradient (#27ae60 → #229954)

**CSS**:
```css
.focus-mode-btn {
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
    /* ... */
}

.focus-mode-btn.active {
    background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
}
```

---

### 3. ⚙️ Settings Button (Fixed Position)

**Vị trí**: Góc dưới bên phải (FIXED)

**Không thay đổi vị trí** - luôn luôn ở góc dưới phải:
- Normal mode: Bottom 30px, Right 30px
- Focus mode: Top 20px, Right 20px (di chuyển lên trên để tránh che nội dung)

---

### 4. 🌙 Dark Mode Support

Cả 2 buttons đều có dark mode styling:

**Focus Mode Button**:
```css
body.dark-mode .focus-mode-btn {
    box-shadow: 0 4px 15px rgba(155, 89, 182, 0.6);
}

body.dark-mode .focus-mode-btn.active {
    background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
    box-shadow: 0 4px 15px rgba(39, 174, 96, 0.6);
}
```

---

### 5. 📱 Focus Mode Improvements

**CSS Updates**:
```css
body.focus-mode {
    overflow: hidden !important; /* Remove outer scroll */
    margin: 0;
    padding: 0;
}

body.focus-mode .card {
    height: 100vh;
    overflow: hidden;
}

body.focus-mode .bilingual-sync-container {
    height: 100vh;
    width: 100vw;
}
```

**Kết quả**:
- ✅ Ẩn hoàn toàn header/footer
- ✅ Ẩn title, back button, delete button
- ✅ Loại bỏ scroll ngoài (outer scroll)
- ✅ Chỉ còn nội dung song ngữ full screen
- ✅ Vừa vặn trong 1 màn hình (iPad ngang hoặc desktop)

---

### 6. 🎹 Keyboard Shortcuts

| Phím | Chức năng |
|------|-----------|
| `Ctrl+F` | Toggle Focus Mode |
| `Ctrl+D` | Toggle Dark Mode |
| `Ctrl+I` | Toggle IPA |
| `Ctrl+0` | Reset font size to 100% |
| `Ctrl++` | Increase font size |
| `Ctrl+-` | Decrease font size |

---

## Cách sử dụng

### Focus Mode Quick Access
1. **Click nút 🎯** ở góc dưới trái
2. Hoặc nhấn `Ctrl+F`
3. Hoặc bật trong Settings panel

### Settings Access
1. **Click nút ⚙️** ở góc dưới phải
2. Tất cả settings có sẵn trong panel

### Trong Focus Mode
- Buttons di chuyển lên góc trên cùng
- Settings button: Góc trên phải
- Focus Mode button: Góc trên trái
- Click Focus Mode button để thoát

---

## UI Layout

### Normal Mode
```
┌─────────────────────────────────────┐
│         Header                      │
│         Title, Back, Delete         │
├─────────────────────────────────────┤
│                                     │
│    Vietnamese    │    English       │
│    Content       │    Content       │
│                  │                  │
│                                     │
├─────────────────────────────────────┤
│  🎯              Footer          ⚙️  │
│  (bottom-left)             (bottom- │
│                             right)  │
└─────────────────────────────────────┘
```

### Focus Mode
```
┌─────────────────────────────────────┐
│ ✅ (top-left)            ⚙️ (top-   │
│                          right)     │
├─────────────────────────────────────┤
│                                     │
│    Vietnamese    │    English       │
│    Content       │    Content       │
│    (FULL         │    (FULL         │
│     SCREEN)      │     SCREEN)      │
│                  │                  │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

---

## Technical Details

### Files Modified
- `templates/article.html`
  - CSS: Settings button, Focus Mode button, Focus Mode styles
  - HTML: Added Focus Mode button
  - JavaScript: Updated `toggleFocusMode()`, `loadSettings()`

### Performance
- **Scroll Sync**: 60 FPS với `requestAnimationFrame`
- **No throttling/debouncing** - direct synchronization
- **Passive listeners** cho better performance

### Browser Compatibility
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (desktop & mobile)
- ✅ iPad/iPhone

---

## Testing Checklist

- [x] English scroll → Vietnamese follows smoothly
- [x] Focus Mode button click → activates focus mode
- [x] Focus Mode button shows ✅ when active
- [x] Settings button stays bottom-right in normal mode
- [x] Settings button moves to top-right in focus mode
- [x] Focus Mode button moves to top-left in focus mode
- [x] Dark mode styling works for both buttons
- [x] Keyboard shortcut Ctrl+F works
- [x] Focus mode hides all outer scroll
- [x] Focus mode fits content in one screen
- [x] Toggle from settings panel syncs with button
- [x] localStorage persistence works

---

## Known Behavior

1. **Focus Mode auto-closes Settings panel** - After enabling focus mode from settings panel, the panel auto-closes after 300ms to provide clean reading experience

2. **Focus Mode scrolls to top** - When entering focus mode, both columns scroll to top for consistent reading position

3. **Button positions change in Focus Mode** - Buttons move from bottom to top corners to avoid covering content and provide easy access

---

## Conclusion

Tất cả các yêu cầu đã được hoàn thành:
✅ Scroll mượt mà - English scroll, Vietnamese follows
✅ Focus Mode button góc dưới trái (fixed)
✅ Settings button góc dưới phải (fixed)
✅ Focus Mode ẩn tất cả, chỉ hiện nội dung
✅ Không còn scroll ngoài khi Focus Mode ON
✅ Quick access với 1 click
