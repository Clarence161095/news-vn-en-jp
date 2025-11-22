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
    Example: "日本語" -> "<ruby>日本語<rt>にほんご</rt></ruby>"
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
                    
                    # Nếu có Kanji (orig != hira), thêm furigana
                    if orig != hira and re.search(r'[\u4e00-\u9fff]', orig):
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
    """
    processed = dict(article)
    
    # Tạo IPA cho tiếng Anh
    if article['content_en']:
        processed['content_en_ipa'] = generate_ipa_html(article['content_en'])
    else:
        processed['content_en_ipa'] = ''
    
    # Tạo Furigana cho tiếng Nhật
    if article['content_jp']:
        processed['content_jp_furigana'] = generate_furigana_html(article['content_jp'])
    else:
        processed['content_jp_furigana'] = ''
    
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
