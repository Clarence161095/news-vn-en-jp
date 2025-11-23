# Bilingual Reading Format Fixes

## Changes Made (23/11/2025)

### 1. ✅ Removed IPA Slashes (`//`)
**File:** `app.py` (line 113)
- **Before:** `result.append(f'<ruby>{word}<rt>/{ipa_text}/</rt></ruby>')`
- **After:** `result.append(f'<ruby>{word}<rt>{ipa_text}</rt></ruby>')`
- **Impact:** IPA phonetic transcriptions now display without surrounding slashes (e.g., `həˈloʊ` instead of `/həˈloʊ/`)

### 2. ✅ Fixed Mobile Touch Handling (iPad/iPhone)
**File:** `templates/article.html`
- Added proper touch event handlers with `preventDefault()` to fix click/touch offset issues
- Added `-webkit-tap-highlight-color: transparent` to prevent blue highlight on iOS
- Added `user-select: none` to prevent text selection conflicts
- Improved single ruby tag activation (closes previous ones when clicking new ones)
- Added both `click` and `touchstart` event listeners for better mobile support

**Key improvements:**
```javascript
// Touch handling for mobile devices
document.addEventListener('touchstart', function(e) {
    const ruby = e.target.closest('ruby');
    if (ruby && !ipaEnabled) {
        e.preventDefault();
        // Toggle IPA display
        ruby.classList.toggle('show-rt');
    }
}, { passive: false });
```

### 3. ✅ Synchronized Bilingual Content Alignment
**Files:** `templates/article.html`, `templates/base.html`

#### Major improvements:

**a) New Bilingual Layout:**
- Redesigned bilingual container with proper grid layout
- Added visual headers for Vietnamese (🇻🇳) and English (🇬🇧) columns
- Added draggable divider to resize columns on desktop

**b) Synchronized Scrolling:**
- Both columns scroll together proportionally
- Smooth scroll synchronization with debouncing (10ms)
- Prevents scroll fighting between columns

**c) Content Alignment Algorithm:**
- Automatically aligns paragraphs and headings between Vietnamese and English
- Matches heading tags (H1-H4) for perfect alignment
- Applies minimum heights to keep parallel content aligned
- Handles content length differences gracefully

**d) Responsive Design:**
- Desktop: Side-by-side columns with draggable divider
- Mobile/Tablet: Stacked layout (one column)
- Proper padding and spacing for readability

#### CSS Features Added:
```css
.bilingual-sync-container {
    display: grid;
    grid-template-columns: 1fr 4px 1fr; /* Left column, divider, right column */
    gap: 0;
    position: relative;
    min-height: 400px;
}

.bilingual-divider {
    background: linear-gradient(180deg, #3498db 0%, #2c3e50 100%);
    cursor: col-resize; /* Draggable cursor */
}
```

#### JavaScript Features Added:
1. **Synchronized Scrolling:**
   - Calculates scroll percentage in one column
   - Applies same percentage to other column
   - Prevents infinite loop with `isScrollSyncing` flag

2. **Draggable Divider:**
   - Mouse drag to resize columns
   - Constraints: 20%-80% range to prevent too narrow columns
   - Smooth cursor change during drag

3. **Content Alignment:**
   - Scans paragraphs and headings in both columns
   - Matches by tag name (H1, H2, P, etc.)
   - Applies minimum height to shorter elements

### 4. Additional Improvements

**Mobile Optimizations:**
- Reduced IPA toggle button size on mobile (50px vs 60px)
- Better touch target sizes
- Improved IPA popup positioning on small screens
- Responsive language selector (stacked on mobile)

**Visual Enhancements:**
- Gradient backgrounds for language columns
- Color-coded headers (blue for VN, red for EN)
- Smooth transitions and animations
- Better visual separation between columns

## Testing Recommendations

1. **Desktop Testing:**
   - ✓ Verify IPA displays without slashes
   - ✓ Test dragging the divider to resize columns
   - ✓ Scroll one column and verify the other follows
   - ✓ Click IPA toggle button to enable/disable

2. **Mobile Testing (iPad/iPhone):**
   - ✓ Tap individual words with IPA disabled - should show popup
   - ✓ Verify no offset/jumping when tapping
   - ✓ Check that columns stack vertically
   - ✓ Test language selector buttons

3. **Bilingual Alignment:**
   - ✓ Load article in bilingual mode
   - ✓ Verify headings align between VN and EN
   - ✓ Check paragraph alignment
   - ✓ Test with articles of different lengths

## Files Modified

1. `app.py` - Removed IPA slashes from generation
2. `templates/article.html` - Major redesign with sync scrolling
3. `templates/base.html` - Updated responsive styles

## Browser Compatibility

- ✅ Chrome/Edge (Desktop & Mobile)
- ✅ Safari (Desktop & iOS)
- ✅ Firefox
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Notes

- Cache needs to be cleared after update: Run `sh reset.sh`
- Old cached IPA data may still have slashes until articles are re-processed
- Synchronized scrolling only works in "Song Ngữ" (bilingual) mode
- Divider dragging is disabled on mobile (<768px width)
