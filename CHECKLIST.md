# 📦 Checklist triển khai EC2

## ✅ Files cần thiết cho deployment

### Core Files
- [x] `app.py` - Flask application chính
- [x] `requirements.txt` - Python dependencies
- [x] `README.md` - Hướng dẫn sử dụng
- [x] `DEPLOY.md` - Hướng dẫn deploy lên EC2
- [x] `.gitignore` - Git ignore config

### Data Files
- [x] `katakana_cache.json` - Pre-cached 2,088 từ Katakana
- [x] `articles.db` - SQLite database (sẽ tạo mới trên server)

### Templates
- [x] `templates/base.html`
- [x] `templates/index.html`
- [x] `templates/article.html`
- [x] `templates/import.html`
- [x] `templates/admin_*.html` (admin templates)

## 🗑️ Files đã xóa (không cần thiết)

### Documentation Files (merged vào README.md)
- ❌ `README_REFACTORED.md`
- ❌ `BUG_FIX.md`
- ❌ `BUG_FIX_SUMMARY.md`
- ❌ `CACHE_MIGRATION_SUMMARY.md`
- ❌ `CENTERING_FINAL.md`
- ❌ `FEATURES.md`
- ❌ `FIX_ALIGNMENT.md`
- ❌ `FURIGANA_IMPROVEMENTS.md`
- ❌ `IMPLEMENTATION_COMPLETE.md`
- ❌ `IMPROVEMENTS.md`
- ❌ `KATAKANA_AUTO_TRANSLATION.md`
- ❌ `KATAKANA_CACHE_README.md`
- ❌ `KATAKANA_CACHE_SUMMARY.md`
- ❌ `QUICK_REFERENCE.md`
- ❌ `REFACTORING_SUMMARY.md`
- ❌ `SUMMARY_VI.md`
- ❌ `TEST_GUIDE.md`
- ❌ `TITLE_FURIGANA_COMPLETE.md`
- ❌ `UPDATE_SUMMARY_VI.md`
- ❌ `CHANGES.rst`
- ❌ `README.rst`

### Test Files
- ❌ `test_alignment.html`
- ❌ `test_auto_generation.py`
- ❌ `test_auto_translation.py`
- ❌ `test_cache.py`
- ❌ `test_katakana.py`
- ❌ `test_katakana_centering.html`
- ❌ `test_katakana_english.py`
- ❌ `debug_centering.html`
- ❌ `demo_furigana.html`
- ❌ `final_test.html`
- ❌ `visual_test.html`

### Backup Files
- ❌ `app_backup.py`
- ❌ `app_old.py`
- ❌ `app_refactored.py`

### Script Files
- ❌ `generate_10k_cache.py`
- ❌ `generate_cache.bat`
- ❌ `generate_katakana_cache.py`

### Sample Data
- ❌ `sample_simple.json`

## 📁 Cấu trúc cuối cùng

```text
news-vn-en-jp/
├── .git/                   # Git repository
├── .gitignore              # Git ignore config
├── app.py                  # Flask app chính ⭐
├── requirements.txt        # Dependencies ⭐
├── katakana_cache.json     # Katakana cache (2,088 words) ⭐
├── articles.db             # Database (sẽ tạo mới)
├── README.md               # Hướng dẫn đầy đủ ⭐
├── DEPLOY.md               # Hướng dẫn deploy EC2 ⭐
└── templates/              # HTML templates ⭐
    ├── base.html
    ├── index.html
    ├── article.html
    ├── import.html
    └── admin_*.html
```

## 🚀 Các bước deploy

1. **Trên EC2**:
   ```bash
   git clone https://github.com/Clarence161095/news-vn-en-jp.git
   cd news-vn-en-jp
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Chạy với Gunicorn**:
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
   ```

3. **Cấu hình systemd service** (xem DEPLOY.md)

4. **Cấu hình Nginx reverse proxy** (xem DEPLOY.md)

5. **Cài SSL với Let's Encrypt** (xem DEPLOY.md)

## 📊 Kích thước repository

| Item | Size | Note |
|------|------|------|
| `app.py` | ~23KB | Main application |
| `katakana_cache.json` | ~70KB | 2,088 cached words |
| `templates/` | ~50KB | HTML templates |
| `articles.db` | ~400KB | Sample data |
| **Total** | **~550KB** | Very lightweight! |

## ✨ Tính năng production-ready

- [x] Auto-generation IPA/Furigana
- [x] Multi-tier caching (RAM + JSON + DB + Google Translate)
- [x] SQLite database (low RAM usage)
- [x] Persistent cache (CASCADE delete)
- [x] REST API endpoints
- [x] Admin panel (with MFA)
- [x] Error handling
- [x] Logging support
- [x] Gunicorn ready
- [x] Nginx ready
- [x] SSL ready

## 🔒 Bảo mật

- [x] `.gitignore` configured (không commit sensitive data)
- [x] Virtual environment isolated
- [x] Database not committed to git
- [x] Admin MFA enabled
- [x] Password hashing
- [x] CSRF protection (Flask built-in)

## 📝 Next Steps

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Clean up and prepare for deployment"
   git push origin main  # hoặc develop
   ```

2. **Deploy to EC2**: Follow DEPLOY.md

3. **Configure domain**: Point DNS to EC2 IP

4. **Setup SSL**: Use Let's Encrypt (free)

5. **Monitor**: Setup logging and monitoring

---

**Repository is ready for deployment! 🎉**
