# Katakana Auto-Translation Feature

## Overview
Ứng dụng sử dụng **Google Translate API** (qua thư viện `deep-translator`) để tự động dịch từ Katakana sang tiếng Anh.

## How It Works

### 1. Automatic Translation Flow
```
Katakana Text → Check Fallback Dictionary → Google Translate → English Translation
                         ↓ (if found)              ↓ (if not found)
                    Return cached              Translate online
```

### 2. Implementation

#### Libraries Used
- **pykakasi**: Phát hiện và xử lý Katakana
- **deep-translator**: Dịch Katakana → English qua Google Translate

#### Function: `translate_katakana_to_english()`
```python
def translate_katakana_to_english(katakana_text):
    """
    Dịch Katakana sang tiếng Anh
    - Ưu tiên: Fallback dictionary (nhanh, offline)
    - Thứ 2: Google Translate (chậm hơn, cần internet)
    - Fallback: None (sẽ dùng romaji)
    """
    # 1. Check fallback dictionary
    if katakana_text in KATAKANA_TO_ENGLISH_FALLBACK:
        return KATAKANA_TO_ENGLISH_FALLBACK[katakana_text]
    
    # 2. Try Google Translate
    try:
        result = translator.translate(katakana_text)
        return result
    except:
        return None  # Fallback to romaji
```

### 3. Fallback Dictionary
Dictionary nhỏ chứa các từ cực kỳ phổ biến để tăng tốc:

```python
KATAKANA_TO_ENGLISH_FALLBACK = {
    'コンピュータ': 'computer',
    'データベース': 'database',
    'AWS': 'AWS',
    # ... thêm các từ thường dùng
}
```

**Lưu ý**: Dictionary này CHỈ chứa một số từ rất phổ biến. Phần lớn từ Katakana sẽ được dịch tự động qua Google Translate.

## Examples

### Example 1: Words in Fallback Dictionary
```
Input:  コンピュータ
Source: Fallback Dictionary (fast)
Output: computer
```

### Example 2: Words NOT in Dictionary (Auto-translated)
```
Input:  テクノロジー
Source: Google Translate (online)
Output: technology

Input:  スマートフォン
Source: Google Translate (online)
Output: smartphone

Input:  ソフトウェアエンジニア
Source: Google Translate (online)
Output: software engineer
```

### Example 3: Cannot Translate (Fallback to Romaji)
```
Input:  ゴジラ (proper noun, may not translate well)
Source: Google Translate failed
Output: gojira (romaji fallback)
```

## Benefits

### ✅ Advantages
1. **Unlimited Coverage**: Dịch được MỌI từ Katakana, không giới hạn bởi dictionary
2. **Always Up-to-date**: Từ mới, thuật ngữ mới → tự động dịch được
3. **Less Maintenance**: Không cần cập nhật dictionary thường xuyên
4. **Smart Fallback**: 
   - Có internet → Google Translate
   - Không internet + từ phổ biến → Fallback dictionary
   - Không dịch được → Romaji

### ⚠️ Limitations
1. **Requires Internet**: Google Translate cần kết nối internet
2. **Slower**: Gọi API mất thời gian (~100-500ms/từ)
3. **Rate Limit**: Google có thể giới hạn số request (hiếm khi xảy ra)

## Performance Optimization

### Caching Strategy
Để tăng hiệu suất, có thể implement caching:

```python
# In-memory cache
_translation_cache = {}

def translate_katakana_to_english(katakana_text):
    # Check cache first
    if katakana_text in _translation_cache:
        return _translation_cache[katakana_text]
    
    # Check fallback dictionary
    if katakana_text in KATAKANA_TO_ENGLISH_FALLBACK:
        return KATAKANA_TO_ENGLISH_FALLBACK[katakana_text]
    
    # Translate via Google
    try:
        result = translator.translate(katakana_text)
        _translation_cache[katakana_text] = result  # Cache result
        return result
    except:
        return None
```

### Batch Translation (Future Enhancement)
Có thể dịch nhiều từ cùng lúc để giảm số lần gọi API:

```python
# Collect all Katakana words first
katakana_words = ['テクノロジー', 'スマートフォン', 'ネットワーク']

# Translate in batch
results = translator.translate_batch(katakana_words)
```

## Testing

### Run Auto-Translation Test
```bash
py test_auto_translation.py
```

### Expected Output
```
テクノロジー → technology [AUTO] ✓ EN
スマートフォン → smartphone [AUTO] ✓ EN
ソフトウェアエンジニア → software engineer [AUTO] ✓ EN
```

## Troubleshooting

### Issue 1: Translation Fails (No Internet)
**Symptom**: Katakana shows romaji instead of English

**Solution**: 
- Check internet connection
- Words will fall back to romaji if translation fails
- Add frequently used words to `KATAKANA_TO_ENGLISH_FALLBACK`

### Issue 2: Slow Performance
**Symptom**: Page loads slowly when displaying Japanese articles

**Solution**:
- Implement caching (see Performance Optimization above)
- Add more words to fallback dictionary
- Consider pre-translating articles during import

### Issue 3: Incorrect Translation
**Symptom**: Google Translate returns wrong translation

**Solution**:
- Add correct translation to `KATAKANA_TO_ENGLISH_FALLBACK`
- Fallback dictionary takes priority over Google Translate

## Future Enhancements

### 1. Persistent Cache
Store translations in database to avoid re-translating:

```sql
CREATE TABLE katakana_translations (
    katakana TEXT PRIMARY KEY,
    english TEXT,
    created_at TIMESTAMP
);
```

### 2. Pre-translation on Import
Translate all Katakana when importing articles:

```python
def import_article(article_data):
    # Detect all Katakana in content
    # Pre-translate and cache
    # Store in database
```

### 3. Alternative Translation Services
Use multiple services for better accuracy:
- Google Translate (current)
- DeepL (better quality)
- Microsoft Translator
- Custom ML model

## Configuration

### Install Required Libraries
```bash
pip install deep-translator pykakasi
```

### Environment Variables (Optional)
```python
# For premium API keys (future)
GOOGLE_TRANSLATE_API_KEY = "your-api-key"
DEEPL_API_KEY = "your-deepl-key"
```

## Summary

✅ **Before**: Fixed dictionary with ~200 words
✅ **After**: Unlimited translation via Google Translate
✅ **Coverage**: Can translate ANY Katakana word
✅ **Fallback**: Smart fallback to dictionary → romaji
✅ **Maintenance**: Minimal - no need to update dictionary frequently

---

**Last Updated**: November 22, 2025
**Version**: 2.0 (Auto-Translation)
