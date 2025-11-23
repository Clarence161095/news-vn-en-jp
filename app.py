#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass  # If fails, continue without UTF-8 fix

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import json
from datetime import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-2024'

# Import thư viện tạo IPA cho tiếng Anh
try:
    import eng_to_ipa as ipa
    IPA_AVAILABLE = True
except ImportError:
    IPA_AVAILABLE = False
    print("Warning: eng-to-ipa not installed. IPA generation will be disabled.")

# Database initialization - Chỉ lưu nội dung Việt-Anh
def init_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    
    # Articles table - Chỉ Việt và Anh
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_vi TEXT,
            title_en TEXT,
            content_vi TEXT,
            content_en TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Article cache table - Lưu processed content (IPA) vào DB
    c.execute('''
        CREATE TABLE IF NOT EXISTS article_cache (
            article_id INTEGER PRIMARY KEY,
            title_en_ipa TEXT,
            content_en_ipa TEXT,
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

# ==================== TỰ ĐỘNG TẠO IPA (OPTIMIZED) ====================
def generate_ipa_html(text):
    """
    Tự động chuyển đổi văn bản tiếng Anh sang HTML với IPA trong ruby tags
    OPTIMIZED: Cache IPA lookups, batch processing
    """
    if not IPA_AVAILABLE or not text:
        return text
    
    try:
        # Tách thành các đoạn HTML và text - optimize với compiled regex
        html_parts = re.split(r'(<[^>]+>)', text)
        result = []
        
        # Cache IPA trong scope của function để tránh lookup trùng lặp
        ipa_cache = {}
        
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
                        # Check cache trước
                        word_lower = word.lower()
                        if word_lower in ipa_cache:
                            ipa_text = ipa_cache[word_lower]
                        else:
                            try:
                                ipa_text = ipa.convert(word)
                                ipa_cache[word_lower] = ipa_text
                            except:
                                ipa_text = None
                        
                        # Chỉ thêm ruby tag nếu có IPA
                        if ipa_text and ipa_text != word:
                            result.append(f'<ruby>{word}<rt>{ipa_text}</rt></ruby>')
                        else:
                            result.append(word)
                    else:
                        result.append(word)
        
        return ''.join(result)
    except Exception as e:
        print(f"Error generating IPA: {e}")
        return text

# ==================== XỬ LÝ BÀI VIẾT ====================
def process_article_content(article):
    """
    Xử lý bài viết: tạo IPA tự động cho tiếng Anh
    Bao gồm cả TITLE và CONTENT
    Sử dụng DB cache để giảm RAM usage
    """
    # Convert sqlite3.Row to dict first
    article_dict = dict(article)
    article_id = article_dict.get('id')
    
    if not article_id:
        # Nếu không có ID, process trực tiếp không cache
        processed = dict(article_dict)
        processed['title_en_ipa'] = generate_ipa_html(article_dict.get('title_en', ''))
        processed['content_en_ipa'] = generate_ipa_html(article_dict.get('content_en', ''))
        return processed
    
    # Check DB cache first
    conn = get_db()
    cache_row = conn.execute(
        'SELECT title_en_ipa, content_en_ipa FROM article_cache WHERE article_id = ?',
        (article_id,)
    ).fetchone()
    
    if cache_row:
        # Cache hit - Lấy từ DB
        conn.close()
        processed = dict(article_dict)
        processed['title_en_ipa'] = cache_row['title_en_ipa']
        processed['content_en_ipa'] = cache_row['content_en_ipa']
        return processed
    
    # Cache miss - Generate IPA
    processed = dict(article_dict)
    
    # Tạo IPA cho tiêu đề tiếng Anh
    if article_dict.get('title_en'):
        processed['title_en_ipa'] = generate_ipa_html(article_dict['title_en'])
    else:
        processed['title_en_ipa'] = ''
    
    # Tạo IPA cho nội dung tiếng Anh
    if article_dict.get('content_en'):
        processed['content_en_ipa'] = generate_ipa_html(article_dict['content_en'])
    else:
        processed['content_en_ipa'] = ''
    
    # Lưu vào DB cache để dùng lần sau
    try:
        conn.execute('''
            INSERT INTO article_cache (article_id, title_en_ipa, content_en_ipa)
            VALUES (?, ?, ?)
        ''', (
            article_id,
            processed['title_en_ipa'],
            processed['content_en_ipa']
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        # Cache đã tồn tại, skip
        pass
    finally:
        conn.close()
    
    return processed

# ==================== ROUTES ====================

# Home page - list all articles
@app.route('/')
def index():
    conn = get_db()
    articles = conn.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

# Article detail page - Tự động tạo IPA khi hiển thị
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    lang = request.args.get('lang', 'vi')
    conn = get_db()
    article_raw = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()
    
    if article_raw is None:
        return "Article not found", 404
    
    # Xử lý bài viết: tạo IPA
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

# Import articles from JSON - CHỈ IMPORT NỘI DUNG GỐC VỚI VALIDATION
@app.route('/import', methods=['GET', 'POST'])
def import_articles():
    if request.method == 'POST':
        json_data = request.form.get('json_data')
        
        try:
            data = json.loads(json_data)
            
            # Handle both single article and array of articles
            articles_to_import = data if isinstance(data, list) else [data]
            
            # VALIDATE: Kiểm tra cấu trúc JSON trước khi import
            required_fields = ['title_vi', 'title_en', 'content_vi', 'content_en']
            for idx, article in enumerate(articles_to_import):
                if not isinstance(article, dict):
                    flash(f'Lỗi: Bài viết #{idx+1} không phải là object JSON hợp lệ!', 'error')
                    return redirect(url_for('import_articles'))
                
                # Kiểm tra có ít nhất 1 title và 1 content
                has_title = article.get('title_vi') or article.get('title_en')
                has_content = article.get('content_vi') or article.get('content_en')
                
                if not has_title:
                    flash(f'Lỗi: Bài viết #{idx+1} thiếu title_vi hoặc title_en!', 'error')
                    return redirect(url_for('import_articles'))
                
                if not has_content:
                    flash(f'Lỗi: Bài viết #{idx+1} thiếu content_vi hoặc content_en!', 'error')
                    return redirect(url_for('import_articles'))
                
                # Cảnh báo nếu có field tiếng Nhật (cũ)
                if article.get('title_jp') or article.get('content_jp'):
                    flash(f'Cảnh báo: Bài #{idx+1} có field tiếng Nhật (title_jp/content_jp) sẽ bị bỏ qua!', 'warning')
            
            conn = get_db()
            imported_count = 0
            for article in articles_to_import:
                # CHỈ LƯU NỘI DUNG GỐC - KHÔNG LƯU IPA
                conn.execute('''
                    INSERT INTO articles 
                    (title_vi, title_en, content_vi, content_en, category)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    article.get('title_vi', ''),
                    article.get('title_en', ''),
                    article.get('content_vi', ''),
                    article.get('content_en', ''),
                    article.get('category', 'general')
                ))
                imported_count += 1
            
            conn.commit()
            conn.close()
            
            flash(f'✅ Đã import thành công {imported_count} bài viết! IPA sẽ được tạo tự động khi xem bài.', 'success')
            return redirect(url_for('index'))
        except json.JSONDecodeError as e:
            flash(f'❌ Lỗi cú pháp JSON: {str(e)}', 'error')
            return redirect(url_for('import_articles'))
        except Exception as e:
            flash(f'❌ Lỗi khi import: {str(e)}', 'error')
            return redirect(url_for('import_articles'))
    
    # Thống kê thư viện
    status = {
        'ipa': 'Đã cài đặt ✓' if IPA_AVAILABLE else 'Chưa cài đặt ✗'
    }
    
    return render_template('import.html', lib_status=status)

# API endpoint to get article data with auto-generated IPA
@app.route('/api/article/<int:article_id>')
def api_article(article_id):
    conn = get_db()
    article_raw = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()
    
    if article_raw is None:
        return jsonify({'error': 'Article not found'}), 404
    
    # Xử lý và trả về JSON với IPA
    article = process_article_content(article_raw)
    return jsonify(dict(article))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
