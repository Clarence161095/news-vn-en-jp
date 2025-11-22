# Katakana Cache Generator

## 📚 Mục Đích

Tạo file JSON cache chứa ~2000+ từ Katakana phổ biến nhất với bản dịch tiếng Anh để:
- **Tăng tốc độ**: Load furigana NHANH HƠN (không cần gọi Google Translate mỗi lần)
- **Offline-ready**: Hoạt động tốt ngay cả khi mất kết nối internet
- **Tiết kiệm**: Giảm số lần gọi Google Translate API

## 🚀 Cách Sử Dụng

### Bước 1: Generate Cache File

Chạy batch file để tạo `katakana_cache.json`:

```bash
generate_cache.bat
```

Hoặc chạy trực tiếp bằng Python:

```bash
python generate_katakana_cache.py
```

### Bước 2: Đợi Hoàn Thành

- **Thời gian dự kiến**: 5-10 phút
- **Số từ**: ~2000+ từ Katakana
- Script sẽ:
  - Dịch từng từ qua Google Translate
  - Lưu progress mỗi 50 từ (để có thể resume nếu bị gián đoạn)
  - Pause giữa các batch để tránh rate limiting

### Bước 3: Kiểm Tra Kết Quả

Sau khi hoàn thành, file `katakana_cache.json` sẽ được tạo với format:

```json
{
  "コンピュータ": "computer",
  "プログラミング": "programming",
  "データベース": "database",
  ...
}
```

### Bước 4: Restart Flask App

Flask sẽ tự động load cache file khi khởi động:

```
✓ Loaded 2156 Katakana translations from cache file
```

## 📊 Performance Improvement

### Trước khi có cache:
```
コンピュータ → Google Translate (300ms) → "computer"
テクノロジー → Google Translate (250ms) → "technology"
データベース → Google Translate (280ms) → "database"
Total: ~830ms cho 3 từ
```

### Sau khi có cache:
```
コンピュータ → JSON cache (1ms) → "computer"
テクノロジー → JSON cache (1ms) → "technology"
データベース → JSON cache (1ms) → "database"
Total: ~3ms cho 3 từ (nhanh hơn ~275 lần!)
```

## 🔧 Cấu Trúc Caching (4 Tiers)

App sử dụng **4-tier caching strategy** để tối ưu performance:

```
Request: コンピュータ
    ↓
┌─────────────────────────────────────────┐
│ Tier 1: In-Memory Cache (Runtime)      │ ← FASTEST (~1ms)
│ _katakana_translation_cache = {}       │
└─────────────────────────────────────────┘
    ↓ (if not found)
┌─────────────────────────────────────────┐
│ Tier 2: JSON File Cache (Persistent)   │ ← FAST (~2ms)
│ katakana_cache.json (2000+ words)      │
└─────────────────────────────────────────┘
    ↓ (if not found)
┌─────────────────────────────────────────┐
│ Tier 3: Fallback Dictionary            │ ← FAST (~1ms)
│ KATAKANA_TO_ENGLISH_FALLBACK (~200)    │
└─────────────────────────────────────────┘
    ↓ (if not found)
┌─────────────────────────────────────────┐
│ Tier 4: Google Translate API (Online)  │ ← SLOW (~100-500ms)
│ translator.translate()                  │
│ + Cache result to Tier 1 & memory      │
└─────────────────────────────────────────┘
```

## 📝 Danh Sách Từ Trong Cache

Cache bao gồm các category:

- **Technology & Computing** (200+ từ): API, クラウド, サーバー, データベース...
- **Business & Office** (200+ từ): ビジネス, マネジメント, マーケティング...
- **Food & Drinks** (300+ từ): コーヒー, ピザ, レストラン...
- **Fashion & Shopping** (200+ từ): ファッション, ブランド, オンラインショッピング...
- **Transportation & Travel** (200+ từ): エアポート, ホテル, タクシー...
- **Entertainment & Media** (200+ từ): ゲーム, ムービー, アニメ...
- **Health & Medical** (200+ từ): ホスピタル, ドクター, ワクチン...
- **Education & Science** (200+ từ): ユニバーシティ, サイエンス, リサーチ...
- **Countries & Cities** (200+ từ): アメリカ, トウキョウ, ニューヨーク...
- **Brands & Companies** (200+ từ): グーグル, アップル, マイクロソフト...
- **Common Words** (500+ từ): タイム, ハッピー, グッド, ビッグ...

## ⚠️ Lưu Ý

1. **Rate Limiting**: Script có delay để tránh bị Google block
2. **Resume Support**: Nếu bị gián đoạn, chạy lại script sẽ skip các từ đã dịch
3. **Internet Required**: Cần kết nối internet để generate cache lần đầu
4. **One-time Setup**: Chỉ cần chạy 1 lần, sau đó app dùng cache offline

## 🔄 Update Cache

Nếu muốn thêm từ mới:

1. Edit `generate_katakana_cache.py` → thêm từ vào list `KATAKANA_WORDS`
2. Chạy lại `generate_cache.bat`
3. Restart Flask app

## 📈 Statistics

Sau khi generate xong, script sẽ hiển thị:

```
============================================================
TRANSLATION COMPLETE!
============================================================
✓ Successfully translated: 2156 words
✗ Failed: 12 words
📄 Output file: katakana_cache.json
📦 File size: 125847 bytes
```

## 🎯 Expected Results

- **Cache size**: ~120KB (2000+ words)
- **Load time**: ~10ms khi Flask start
- **Lookup time**: ~1-2ms per word
- **Hit rate**: ~90% cho nội dung tin tức tiếng Nhật thông thường
- **Fallback**: Từ không có trong cache → Google Translate → cache vào memory

---

**Happy Caching! 🚀**
