from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-2024'

# Database initialization
def init_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    
    # Articles table
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_vi TEXT,
            title_en TEXT,
            title_jp TEXT,
            content_vi TEXT,
            content_en TEXT,
            content_jp TEXT,
            content_en_ipa TEXT,
            content_jp_furigana TEXT,
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

# Home page - list all articles
@app.route('/')
def index():
    conn = get_db()
    articles = conn.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

# Article detail page
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    lang = request.args.get('lang', 'vi')  # Default to Vietnamese
    conn = get_db()
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()
    
    if article is None:
        return "Article not found", 404
    
    return render_template('article.html', article=article, lang=lang)

# Delete Article - Không cần đăng nhập
@app.route('/article/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    conn = get_db()
    conn.execute('DELETE FROM articles WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
    flash('Bài viết đã được xóa thành công!', 'success')
    return redirect(url_for('index'))

# Import articles from JSON
@app.route('/import', methods=['GET', 'POST'])
def import_articles():
    if request.method == 'POST':
        json_data = request.form.get('json_data')
        
        try:
            data = json.loads(json_data)
            conn = get_db()
            
            # Handle both single article and array of articles
            articles_to_import = data if isinstance(data, list) else [data]
            
            for article in articles_to_import:
                conn.execute('''
                    INSERT INTO articles 
                    (title_vi, title_en, title_jp, content_vi, content_en, content_jp, 
                     content_en_ipa, content_jp_furigana, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article.get('title_vi', ''),
                    article.get('title_en', ''),
                    article.get('title_jp', ''),
                    article.get('content_vi', ''),
                    article.get('content_en', ''),
                    article.get('content_jp', ''),
                    article.get('content_en_ipa', ''),
                    article.get('content_jp_furigana', ''),
                    article.get('category', 'general')
                ))
            
            conn.commit()
            conn.close()
            
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error importing data: {str(e)}", 400
    
    return render_template('import.html')

# API endpoint to get article data
@app.route('/api/article/<int:article_id>')
def api_article(article_id):
    conn = get_db()
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()
    
    if article is None:
        return jsonify({'error': 'Article not found'}), 404
    
    return jsonify(dict(article))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
