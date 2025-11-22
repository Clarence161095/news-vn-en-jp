from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import json
from datetime import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-2024'

# Import thư viện tạo IPA và Furigana
try:
    from pykakasi import kakasi
    KAKASI_AVAILABLE = True
    kks = kakasi()
except ImportError:
    KAKASI_AVAILABLE = False
    print("Warning: pykakasi not installed. Furigana generation will be disabled.")

try:
    import eng_to_ipa as ipa
    IPA_AVAILABLE = True
except ImportError:
    IPA_AVAILABLE = False
    print("Warning: eng-to-ipa not installed. IPA generation will be disabled.")

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
    translator = GoogleTranslator(source='ja', target='en')
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("Warning: deep-translator not installed. Katakana translation will use fallback dictionary.")

# Katakana to English dictionary (fallback cho các từ phổ biến nếu không có internet)
KATAKANA_TO_ENGLISH_FALLBACK = {
    'コンピュータ': 'computer',
    'コンピューター': 'computer',
    'プログラミング': 'programming',
    'プログラム': 'program',
    'データベース': 'database',
    'データ': 'data',
    'クラウド': 'cloud',
    'サーバー': 'server',
    'サーバ': 'server',
    'ネットワーク': 'network',
    'インターネット': 'internet',
    'ソフトウェア': 'software',
    'ハードウェア': 'hardware',
    'アプリケーション': 'application',
    'アプリ': 'app',
    'システム': 'system',
    'ファイル': 'file',
    'フォルダ': 'folder',
    'ユーザー': 'user',
    'パスワード': 'password',
    'セキュリティ': 'security',
    'テクノロジー': 'technology',
    'デジタル': 'digital',
    'オンライン': 'online',
    'オフライン': 'offline',
    'ダウンロード': 'download',
    'アップロード': 'upload',
    'インストール': 'install',
    'アップデート': 'update',
    'バージョン': 'version',
    'エラー': 'error',
    'バグ': 'bug',
    'デバッグ': 'debug',
    'コード': 'code',
    'スクリプト': 'script',
    'フレームワーク': 'framework',
    'ライブラリ': 'library',
    'モジュール': 'module',
    'パッケージ': 'package',
    'インターフェース': 'interface',
    'グラフィック': 'graphic',
    'イメージ': 'image',
    'ビデオ': 'video',
    'オーディオ': 'audio',
    'メディア': 'media',
    'ブラウザ': 'browser',
    'ウィンドウ': 'window',
    'メニュー': 'menu',
    'ボタン': 'button',
    'リンク': 'link',
    'ページ': 'page',
    'サイト': 'site',
    'ホーム': 'home',
    'プロフィール': 'profile',
    'アカウント': 'account',
    'ログイン': 'login',
    'ログアウト': 'logout',
    'メール': 'email',
    'メッセージ': 'message',
    'チャット': 'chat',
    'フォーム': 'form',
    'サーチ': 'search',
    'フィルター': 'filter',
    'ソート': 'sort',
    'リスト': 'list',
    'テーブル': 'table',
    'グリッド': 'grid',
    'チャート': 'chart',
    'グラフ': 'graph',
    'レポート': 'report',
    'ドキュメント': 'document',
    'テキスト': 'text',
    'フォント': 'font',
    'カラー': 'color',
    'スタイル': 'style',
    'テンプレート': 'template',
    'テーマ': 'theme',
    'デザイン': 'design',
    'レイアウト': 'layout',
    'フォーマット': 'format',
    'コンテンツ': 'content',
    'メタデータ': 'metadata',
    'タグ': 'tag',
    'カテゴリ': 'category',
    'ステータス': 'status',
    'プロセス': 'process',
    'タスク': 'task',
    'プロジェクト': 'project',
    'マネージャー': 'manager',
    'アドミニストレーター': 'administrator',
    'アドミン': 'admin',
    'ゲスト': 'guest',
    'グループ': 'group',
    'チーム': 'team',
    'メンバー': 'member',
    'ロール': 'role',
    'パーミッション': 'permission',
    'アクセス': 'access',
    'コントロール': 'control',
    'セッティング': 'setting',
    'オプション': 'option',
    'コンフィグ': 'config',
    'パラメータ': 'parameter',
    'バリュー': 'value',
    'キー': 'key',
    'ストレージ': 'storage',
    'メモリ': 'memory',
    'キャッシュ': 'cache',
    'バッファ': 'buffer',
    'スタック': 'stack',
    'キュー': 'queue',
    'アルゴリズム': 'algorithm',
    'ロジック': 'logic',
    'メソッド': 'method',
    'ファンクション': 'function',
    'クラス': 'class',
    'オブジェクト': 'object',
    'インスタンス': 'instance',
    'プロパティ': 'property',
    'アトリビュート': 'attribute',
    'イベント': 'event',
    'リスナー': 'listener',
    'ハンドラー': 'handler',
    'コールバック': 'callback',
    'プロミス': 'promise',
    'アシンク': 'async',
    'シンク': 'sync',
    'スレッド': 'thread',
    'プロセッサー': 'processor',
    'サービス': 'service',
    'API': 'API',
    'エンドポイント': 'endpoint',
    'リクエスト': 'request',
    'レスポンス': 'response',
    'ステータスコード': 'status code',
    'ヘッダー': 'header',
    'ボディ': 'body',
    'JSON': 'JSON',
    'XML': 'XML',
    'HTML': 'HTML',
    'CSS': 'CSS',
    'JavaScript': 'JavaScript',
    'Python': 'Python',
    'Java': 'Java',
    'Ruby': 'Ruby',
    'PHP': 'PHP',
    'SQL': 'SQL',
    'NoSQL': 'NoSQL',
    'MySQL': 'MySQL',
    'PostgreSQL': 'PostgreSQL',
    'MongoDB': 'MongoDB',
    'Redis': 'Redis',
    'Docker': 'Docker',
    'Kubernetes': 'Kubernetes',
    'Git': 'Git',
    'GitHub': 'GitHub',
    'Linux': 'Linux',
    'Windows': 'Windows',
    'Mac': 'Mac',
    'Android': 'Android',
    'iOS': 'iOS',
    'Amazon': 'Amazon',
    'Google': 'Google',
    'Microsoft': 'Microsoft',
    'Apple': 'Apple',
    'AWS': 'AWS',
    'Azure': 'Azure',
    'スケーラブル': 'scalable',
    'コンピューティング': 'computing',
    'フルスタック': 'full stack',
    'フロントエンド': 'front-end',
    'バックエンド': 'back-end',
    'フレキシブル': 'flexible',
    'レスポンシブ': 'responsive',
    'モバイル': 'mobile',
    'デスクトップ': 'desktop',
    'タブレット': 'tablet',
    'デバイス': 'device',
    'プラットフォーム': 'platform',
    'エコシステム': 'ecosystem',
}

# Load Katakana cache from JSON file (2000+ words for instant lookup)
KATAKANA_CACHE_FILE = 'katakana_cache.json'
KATAKANA_CACHE = {}
try:
    with open(KATAKANA_CACHE_FILE, 'r', encoding='utf-8') as f:
        KATAKANA_CACHE = json.load(f)
    print(f"✓ Loaded {len(KATAKANA_CACHE)} Katakana translations from cache file")
except FileNotFoundError:
    print(f"⚠️  Cache file '{KATAKANA_CACHE_FILE}' not found. Run 'generate_cache.bat' to create it.")
    print(f"   Using fallback dictionary ({len(KATAKANA_TO_ENGLISH_FALLBACK)} words) + Google Translate")
except Exception as e:
    print(f"❌ Error loading cache file: {e}")
    print(f"   Using fallback dictionary ({len(KATAKANA_TO_ENGLISH_FALLBACK)} words) + Google Translate")

# In-memory cache for Katakana translations
_katakana_translation_cache = {}

def translate_katakana_to_english(katakana_text):
    """
    Dịch Katakana sang tiếng Anh với multi-tier caching
    - Tier 1: In-memory cache (instant, runtime only)
    - Tier 2: JSON file cache (fast, ~2000+ words, persistent)
    - Tier 3: Fallback dictionary (fast, ~200 common words)
    - Tier 4: Google Translate (slow, online, cached after first call)
    """
    if not katakana_text or len(katakana_text) <= 1:
        return None
    
    # Tier 1: Check in-memory cache first (fastest, runtime only)
    if katakana_text in _katakana_translation_cache:
        return _katakana_translation_cache[katakana_text]
    
    # Tier 2: Check JSON file cache (fast, persistent, 2000+ words)
    if katakana_text in KATAKANA_CACHE:
        result = KATAKANA_CACHE[katakana_text]
        _katakana_translation_cache[katakana_text] = result
        return result
    
    # Tier 3: Check fallback dictionary (fast, common words)
    if katakana_text in KATAKANA_TO_ENGLISH_FALLBACK:
        result = KATAKANA_TO_ENGLISH_FALLBACK[katakana_text]
        _katakana_translation_cache[katakana_text] = result
        return result
    
    # Tier 4: Use Google Translate (slow, will be cached)
    if TRANSLATOR_AVAILABLE:
        try:
            # Translate từ tiếng Nhật sang tiếng Anh
            result = translator.translate(katakana_text)
            if result and result.lower() != katakana_text.lower():
                # Cache the result for future use
                _katakana_translation_cache[katakana_text] = result
                return result
        except Exception as e:
            print(f"Translation error for '{katakana_text}': {e}")
    
    # Không dịch được → cache None để tránh retry
    _katakana_translation_cache[katakana_text] = None
    return None

# Database initialization - Chỉ lưu nội dung gốc, không lưu IPA và Furigana
def init_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    
    # Articles table - Đơn giản hơn, chỉ lưu nội dung gốc
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
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
        )
    ''')
    
    # Article cache table - Lưu processed content (IPA + Furigana) vào DB thay vì RAM
    c.execute('''
        CREATE TABLE IF NOT EXISTS article_cache (
            article_id INTEGER PRIMARY KEY,
            title_en_ipa TEXT,
            title_jp_furigana TEXT,
            content_en_ipa TEXT,
            content_jp_furigana TEXT,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# Get database connection
def get_db():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== TỰ ĐỘNG TẠO IPA ====================
def generate_ipa_html(text):
    """
    Tự động chuyển đổi văn bản tiếng Anh sang HTML với IPA trong ruby tags
    Example: "Hello world" -> "<ruby>Hello<rt>/həˈloʊ/</rt></ruby> <ruby>world<rt>/wɝld/</rt></ruby>"
    """
    if not IPA_AVAILABLE or not text:
        return text
    
    try:
        # Tách thành các đoạn HTML và text
        html_parts = re.split(r'(<[^>]+>)', text)
        result = []
        
        for part in html_parts:
            # Nếu là HTML tag, giữ nguyên
            if part.startswith('<'):
                result.append(part)
            else:
                # Xử lý text: tách thành từng từ
                words = re.findall(r'\b[\w\']+\b|[^\w\s]|\s+', part)
                for word in words:
                    # Nếu là từ (không phải dấu câu hoặc khoảng trắng)
                    if re.match(r'\b[\w\']+\b', word):
                        try:
                            ipa_text = ipa.convert(word)
                            # Chỉ thêm ruby tag nếu có IPA
                            if ipa_text and ipa_text != word:
                                result.append(f'<ruby>{word}<rt>/{ipa_text}/</rt></ruby>')
                            else:
                                result.append(word)
                        except:
                            result.append(word)
                    else:
                        result.append(word)
        
        return ''.join(result)
    except Exception as e:
        print(f"Error generating IPA: {e}")
        return text

# ==================== TỰ ĐỘNG TẠO FURIGANA ====================
def generate_furigana_html(text):
    """
    Tự động chuyển đổi văn bản tiếng Nhật sang HTML với Furigana trong ruby tags
    - Kanji: Hiện Furigana bằng Hiragana (日本語 → にほんご)
    - Katakana: Hiện bằng tiếng Anh nếu có trong dictionary (コンピュータ → computer)
              Nếu không có trong dictionary thì dùng Romanization
    """
    if not KAKASI_AVAILABLE or not text:
        return text
    
    try:
        # Tách thành các đoạn HTML và text
        html_parts = re.split(r'(<[^>]+>)', text)
        result = []
        
        for part in html_parts:
            # Nếu là HTML tag, giữ nguyên
            if part.startswith('<'):
                result.append(part)
            else:
                # Xử lý text tiếng Nhật
                converted = kks.convert(part)
                for item in converted:
                    orig = item['orig']
                    hira = item['hira']
                    hepburn = item.get('hepburn', hira)  # Romaji conversion
                    
                    # Kiểm tra nếu là Katakana (ア-ン)
                    is_katakana = bool(re.search(r'[\u30A0-\u30FF]+', orig))
                    
                    if is_katakana and len(orig) > 1:
                        # Katakana → Tìm tiếng Anh (dùng translator hoặc dictionary)
                        english = translate_katakana_to_english(orig)
                        if english:
                            # Nếu dịch được sang tiếng Anh
                            result.append(f'<ruby>{orig}<rt>{english}</rt></ruby>')
                        else:
                            # Nếu không dịch được, dùng Romanization như fallback
                            result.append(f'<ruby>{orig}<rt>{hepburn}</rt></ruby>')
                    elif orig != hira and re.search(r'[\u4e00-\u9fff]', orig):
                        # Kanji → Hiện Furigana bằng Hiragana
                        result.append(f'<ruby>{orig}<rt>{hira}</rt></ruby>')
                    else:
                        result.append(orig)
        
        return ''.join(result)
    except Exception as e:
        print(f"Error generating Furigana: {e}")
        return text

# ==================== XỬ LÝ BÀI VIẾT ====================
def process_article_content(article):
    """
    Xử lý bài viết: tạo IPA và Furigana tự động từ nội dung gốc
    Bao gồm cả TITLE và CONTENT
    Sử dụng DB cache để giảm RAM usage (thay vì in-memory cache)
    """
    # Convert sqlite3.Row to dict first
    article_dict = dict(article)
    article_id = article_dict.get('id')
    
    if not article_id:
        # Nếu không có ID, process trực tiếp không cache
        processed = dict(article_dict)
        processed['title_en_ipa'] = generate_ipa_html(article_dict.get('title_en', ''))
        processed['title_jp_furigana'] = generate_furigana_html(article_dict.get('title_jp', ''))
        processed['content_en_ipa'] = generate_ipa_html(article_dict.get('content_en', ''))
        processed['content_jp_furigana'] = generate_furigana_html(article_dict.get('content_jp', ''))
        return processed
    
    # Check DB cache first
    conn = get_db()
    cache_row = conn.execute(
        'SELECT title_en_ipa, title_jp_furigana, content_en_ipa, content_jp_furigana FROM article_cache WHERE article_id = ?',
        (article_id,)
    ).fetchone()
    
    if cache_row:
        # Cache hit - Lấy từ DB
        conn.close()
        processed = dict(article_dict)
        processed['title_en_ipa'] = cache_row['title_en_ipa']
        processed['title_jp_furigana'] = cache_row['title_jp_furigana']
        processed['content_en_ipa'] = cache_row['content_en_ipa']
        processed['content_jp_furigana'] = cache_row['content_jp_furigana']
        return processed
    
    # Cache miss - Generate IPA và Furigana
    processed = dict(article_dict)
    
    # Tạo IPA cho tiêu đề tiếng Anh
    if article_dict.get('title_en'):
        processed['title_en_ipa'] = generate_ipa_html(article_dict['title_en'])
    else:
        processed['title_en_ipa'] = ''
    
    # Tạo Furigana cho tiêu đề tiếng Nhật
    if article_dict.get('title_jp'):
        processed['title_jp_furigana'] = generate_furigana_html(article_dict['title_jp'])
    else:
        processed['title_jp_furigana'] = ''
    
    # Tạo IPA cho nội dung tiếng Anh
    if article_dict.get('content_en'):
        processed['content_en_ipa'] = generate_ipa_html(article_dict['content_en'])
    else:
        processed['content_en_ipa'] = ''
    
    # Tạo Furigana cho nội dung tiếng Nhật
    if article_dict.get('content_jp'):
        processed['content_jp_furigana'] = generate_furigana_html(article_dict['content_jp'])
    else:
        processed['content_jp_furigana'] = ''
    
    # Lưu vào DB cache để dùng lần sau
    try:
        conn.execute('''
            INSERT INTO article_cache (article_id, title_en_ipa, title_jp_furigana, content_en_ipa, content_jp_furigana)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            article_id,
            processed['title_en_ipa'],
            processed['title_jp_furigana'],
            processed['content_en_ipa'],
            processed['content_jp_furigana']
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        # Cache đã tồn tại, skip
        pass
    finally:
        conn.close()
    
    return processed
    return processed

# ==================== ROUTES ====================

# Home page - list all articles
@app.route('/')
def index():
    conn = get_db()
    articles = conn.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

# Article detail page - Tự động tạo IPA và Furigana khi hiển thị
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    lang = request.args.get('lang', 'vi')
    conn = get_db()
    article_raw = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()
    
    if article_raw is None:
        return "Article not found", 404
    
    # Xử lý bài viết: tạo IPA và Furigana
    article = process_article_content(article_raw)
    
    return render_template('article.html', article=article, lang=lang)

# Delete Article
@app.route('/article/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    # Cache will be auto-deleted via CASCADE constraint
    conn = get_db()
    conn.execute('DELETE FROM articles WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
    flash('Bài viết đã được xóa thành công!', 'success')
    return redirect(url_for('index'))

# Import articles from JSON - CHỈ IMPORT NỘI DUNG GỐC
@app.route('/import', methods=['GET', 'POST'])
def import_articles():
    if request.method == 'POST':
        json_data = request.form.get('json_data')
        
        try:
            data = json.loads(json_data)
            conn = get_db()
            
            # Handle both single article and array of articles
            articles_to_import = data if isinstance(data, list) else [data]
            
            imported_count = 0
            for article in articles_to_import:
                # CHỈ LƯU NỘI DUNG GỐC - KHÔNG LƯU IPA VÀ FURIGANA
                conn.execute('''
                    INSERT INTO articles 
                    (title_vi, title_en, title_jp, content_vi, content_en, content_jp, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article.get('title_vi', ''),
                    article.get('title_en', ''),
                    article.get('title_jp', ''),
                    article.get('content_vi', ''),
                    article.get('content_en', ''),
                    article.get('content_jp', ''),
                    article.get('category', 'general')
                ))
                imported_count += 1
            
            conn.commit()
            conn.close()
            
            # DB cache will be auto-populated on first view
            
            flash(f'Đã import thành công {imported_count} bài viết! IPA và Furigana sẽ được tạo tự động khi xem bài.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Lỗi khi import: {str(e)}', 'error')
            return redirect(url_for('import_articles'))
    
    # Thống kê thư viện
    status = {
        'ipa': 'Đã cài đặt ✓' if IPA_AVAILABLE else 'Chưa cài đặt ✗',
        'furigana': 'Đã cài đặt ✓' if KAKASI_AVAILABLE else 'Chưa cài đặt ✗'
    }
    
    return render_template('import.html', lib_status=status)

# API endpoint to get article data with auto-generated IPA and Furigana
@app.route('/api/article/<int:article_id>')
def api_article(article_id):
    conn = get_db()
    article_raw = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()
    
    if article_raw is None:
        return jsonify({'error': 'Article not found'}), 404
    
    # Xử lý và trả về JSON với IPA và Furigana
    article = process_article_content(article_raw)
    return jsonify(dict(article))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
