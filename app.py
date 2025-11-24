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
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-2024'

# Cache expiration settings
CACHE_EXPIRATION_DAYS = 30  # Auto-delete cache older than 30 days

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
            is_favorite INTEGER DEFAULT 0,
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
    
    # Categories table
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Article-Category relationship (many-to-many)
    c.execute('''
        CREATE TABLE IF NOT EXISTS article_categories (
            article_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (article_id, category_id),
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        )
    ''')
    
    # Migration: Add is_favorite column if not exists
    try:
        c.execute('ALTER TABLE articles ADD COLUMN is_favorite INTEGER DEFAULT 0')
        print("✅ Added is_favorite column to articles table")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()

# Get database connection
def get_db():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== TỰ ĐỘNG TẠO IPA (FIXED & OPTIMIZED) ====================
def generate_ipa_html(text):
    """
    Tự động chuyển đổi văn bản tiếng Anh sang HTML với IPA trong ruby tags
    FIXED: Process ALL words, not just some
    OPTIMIZED: Cache IPA lookups to improve performance
    """
    if not IPA_AVAILABLE or not text:
        return text
    
    try:
        result = []
        ipa_cache = {}  # Cache IPA conversions
        
        # Strategy: Process character by character, identifying HTML tags vs text
        i = 0
        while i < len(text):
            # Check if we're at an HTML tag
            if text[i] == '<':
                # Find the end of the tag
                tag_end = text.find('>', i)
                if tag_end == -1:
                    # Malformed HTML, treat as text
                    result.append(text[i])
                    i += 1
                    continue
                
                # Extract full tag
                tag = text[i:tag_end + 1]
                result.append(tag)
                i = tag_end + 1
            else:
                # We're in text content - extract until next tag
                next_tag = text.find('<', i)
                if next_tag == -1:
                    # No more tags, process rest of text
                    text_content = text[i:]
                    result.append(process_text_with_ipa(text_content, ipa_cache))
                    break
                else:
                    # Process text until next tag
                    text_content = text[i:next_tag]
                    result.append(process_text_with_ipa(text_content, ipa_cache))
                    i = next_tag
        
        return ''.join(result)
    except Exception as e:
        print(f"Error generating IPA: {e}")
        import traceback
        traceback.print_exc()
        return text


def process_text_with_ipa(text, ipa_cache):
    """
    Process plain text and wrap each word with IPA ruby tags
    """
    if not text or not text.strip():
        return text
    
    result = []
    # Split into words, punctuation, and whitespace
    tokens = re.findall(r'\b[\w\']+\b|[^\w\s]|\s+', text)
    
    for token in tokens:
        # Check if it's a word (not punctuation or whitespace)
        if re.match(r'\b[\w\']+\b', token):
            # Check cache first
            token_lower = token.lower()
            if token_lower in ipa_cache:
                ipa_text = ipa_cache[token_lower]
            else:
                try:
                    ipa_text = ipa.convert(token)
                    ipa_cache[token_lower] = ipa_text
                except:
                    ipa_text = None
            
            # Add ruby tag if IPA is available and different from original
            if ipa_text and ipa_text != token:
                result.append(f'<ruby>{token}<rt>{ipa_text}</rt></ruby>')
            else:
                result.append(token)
        else:
            # Punctuation or whitespace - keep as is
            result.append(token)
    
    return ''.join(result)


def process_html_block(html_block, ipa_cache):
    """
    DEPRECATED: No longer used - kept for compatibility
    """
    return html_block

# ==================== CACHE MANAGEMENT ====================
def clean_old_cache():
    """
    Xóa cache cũ hơn CACHE_EXPIRATION_DAYS (30 ngày)
    Chỉ xóa cache, KHÔNG xóa bài viết
    Returns: số lượng cache đã xóa
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=CACHE_EXPIRATION_DAYS)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')
        
        # Delete old cache entries
        cursor.execute('''
            DELETE FROM article_cache 
            WHERE cached_at < ?
        ''', (cutoff_str,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"🧹 Cleaned {deleted_count} old cache entries (older than {CACHE_EXPIRATION_DAYS} days)")
        
        return deleted_count
    except Exception as e:
        print(f"Error cleaning old cache: {e}")
        return 0

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

# Home page - list all articles with search & filter
@app.route('/')
def index():
    conn = get_db()
    
    # Get search parameters
    search_query = request.args.get('q', '').strip()
    use_regex = request.args.get('regex', 'false') == 'true'
    categories = request.args.getlist('categories')  # Multiple categories
    favorites_only = request.args.get('favorites', 'false') == 'true'
    
    # Base query
    query = 'SELECT DISTINCT a.* FROM articles a'
    params = []
    conditions = []
    
    # Join with categories if filtering by category
    if categories:
        query += ' LEFT JOIN article_categories ac ON a.id = ac.article_id'
        query += ' LEFT JOIN categories c ON ac.category_id = c.id'
        placeholders = ','.join('?' * len(categories))
        conditions.append(f'c.name IN ({placeholders})')
        params.extend(categories)
    
    # Search filter
    if search_query:
        if use_regex:
            # Regex search - More flexible but slower
            # Note: SQLite REGEXP requires loading extension, so we'll fetch all and filter in Python
            pass  # Will filter after fetching
        else:
            # Normal LIKE search
            search_condition = '(a.title_vi LIKE ? OR a.title_en LIKE ? OR a.content_vi LIKE ? OR a.content_en LIKE ?)'
            conditions.append(search_condition)
            search_pattern = f'%{search_query}%'
            params.extend([search_pattern] * 4)
    
    # Favorites filter
    if favorites_only:
        conditions.append('a.is_favorite = 1')
    
    # Combine conditions
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY a.created_at DESC'
    
    articles = conn.execute(query, params).fetchall()
    
    # Apply regex filter if needed (post-query)
    if search_query and use_regex:
        try:
            pattern = re.compile(search_query, re.IGNORECASE)
            articles = [
                a for a in articles 
                if pattern.search(a['title_vi'] or '') or 
                   pattern.search(a['title_en'] or '') or 
                   pattern.search(a['content_vi'] or '') or 
                   pattern.search(a['content_en'] or '')
            ]
        except re.error:
            flash('Invalid regex pattern', 'error')
    
    # Get all categories for filter UI
    all_categories = conn.execute('SELECT DISTINCT name FROM categories ORDER BY name').fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         articles=articles, 
                         all_categories=all_categories,
                         search_query=search_query,
                         use_regex=use_regex,
                         selected_categories=categories,
                         favorites_only=favorites_only)

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
            
            # Clean old cache after importing new articles
            deleted_cache = clean_old_cache()
            
            flash(f'✅ Đã import thành công {imported_count} bài viết! IPA sẽ được tạo tự động khi xem bài.', 'success')
            if deleted_cache > 0:
                flash(f'🧹 Đã xóa {deleted_cache} cache cũ (>30 ngày)', 'info')
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

# API endpoint to clear IPA cache for specific article
@app.route('/api/clear-ipa-cache/<int:article_id>', methods=['POST'])
def clear_ipa_cache(article_id):
    """Clear IPA cache for a specific article"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if article exists
        article = cursor.execute('SELECT id FROM articles WHERE id = ?', (article_id,)).fetchone()
        if not article:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Bài viết không tồn tại'
            }), 404
        
        # Delete cache for this article
        cursor.execute('DELETE FROM article_cache WHERE article_id = ?', (article_id,))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Đã xóa cache cho bài viết này. IPA sẽ được tạo lại ngay bây giờ.',
            'deleted': deleted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# API endpoint to toggle favorite
@app.route('/api/article/<int:article_id>/favorite', methods=['POST'])
def toggle_favorite(article_id):
    """Toggle favorite status of an article"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get current favorite status
        article = cursor.execute('SELECT is_favorite FROM articles WHERE id = ?', (article_id,)).fetchone()
        if not article:
            conn.close()
            return jsonify({'success': False, 'error': 'Article not found'}), 404
        
        # Toggle favorite
        new_status = 0 if article['is_favorite'] else 1
        cursor.execute('UPDATE articles SET is_favorite = ? WHERE id = ?', (new_status, article_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'is_favorite': new_status,
            'message': 'Đã thêm vào yêu thích' if new_status else 'Đã bỏ yêu thích'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API endpoint to get all categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        conn = get_db()
        categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'categories': [dict(c) for c in categories]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API endpoint to add/update article categories
@app.route('/api/article/<int:article_id>/categories', methods=['POST'])
def update_article_categories(article_id):
    """Update categories for an article"""
    try:
        data = request.get_json()
        category_names = data.get('categories', [])
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if article exists
        article = cursor.execute('SELECT id FROM articles WHERE id = ?', (article_id,)).fetchone()
        if not article:
            conn.close()
            return jsonify({'success': False, 'error': 'Article not found'}), 404
        
        # Clear existing categories for this article
        cursor.execute('DELETE FROM article_categories WHERE article_id = ?', (article_id,))
        
        # Add new categories
        for cat_name in category_names:
            cat_name = cat_name.strip()
            if not cat_name:
                continue
            
            # Insert category if not exists
            cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat_name,))
            
            # Get category ID
            cat_id = cursor.execute('SELECT id FROM categories WHERE name = ?', (cat_name,)).fetchone()['id']
            
            # Link article to category
            cursor.execute('INSERT INTO article_categories (article_id, category_id) VALUES (?, ?)', 
                         (article_id, cat_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Đã cập nhật {len(category_names)} categories'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API endpoint to get article categories
@app.route('/api/article/<int:article_id>/categories', methods=['GET'])
def get_article_categories(article_id):
    """Get categories for an article"""
    try:
        conn = get_db()
        categories = conn.execute('''
            SELECT c.* FROM categories c
            JOIN article_categories ac ON c.id = ac.category_id
            WHERE ac.article_id = ?
            ORDER BY c.name
        ''', (article_id,)).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'categories': [dict(c) for c in categories]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
