#!/usr/bin/env python3
"""
Test import logic directly without Flask
"""
import sqlite3
import json

def test_import():
    # Test data
    username = "Clarence"
    article_data = {
        "title_vi": "Test Direct Import",
        "title_en": "Test Direct Import",
        "content_vi": "Content VI",
        "content_en": "Content EN",
        "category": "gaming"
    }
    
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    
    # Insert article
    cursor = conn.execute('''
        INSERT INTO articles 
        (title_vi, title_en, content_vi, content_en, category, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        article_data.get('title_vi', ''),
        article_data.get('title_en', ''),
        article_data.get('content_vi', ''),
        article_data.get('content_en', ''),
        article_data.get('category', 'general'),
        username if username else None
    ))
    
    article_id = cursor.lastrowid
    print(f"✅ Inserted article ID: {article_id}")
    
    # Collect categories
    categories_to_add = []
    
    # 1. Username category
    if username:
        categories_to_add.append(username)
    
    # 2. JSON category
    json_category = article_data.get('category', '').strip()
    if json_category and json_category not in categories_to_add:
        categories_to_add.append(json_category)
    
    print(f"📂 Categories to add: {categories_to_add}")
    
    # Add categories
    for category_name in categories_to_add:
        # Get or create category
        cat_result = conn.execute('SELECT id FROM categories WHERE name = ?', (category_name,)).fetchone()
        if not cat_result:
            print(f"➕ Creating new category: '{category_name}'")
            cat_cursor = conn.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            cat_id = cat_cursor.lastrowid
        else:
            cat_id = cat_result['id']
            print(f"✓ Found existing category: '{category_name}' (ID: {cat_id})")
        
        # Link category to article
        conn.execute('''
            INSERT OR IGNORE INTO article_categories (article_id, category_id)
            VALUES (?, ?)
        ''', (article_id, cat_id))
        
        print(f"✅ Linked category '{category_name}' to article {article_id}")
    
    conn.commit()
    
    # Verify
    print("\n" + "="*60)
    print("VERIFICATION:")
    print("="*60)
    
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    print(f"Article ID: {article['id']}")
    print(f"  Title: {article['title_vi']}")
    print(f"  Category (old field): {article['category']}")
    print(f"  Created by: {article['created_by']}")
    
    cats = conn.execute('''
        SELECT c.name 
        FROM categories c 
        JOIN article_categories ac ON c.id = ac.category_id 
        WHERE ac.article_id = ?
    ''', (article_id,)).fetchall()
    
    print(f"  Categories (new system): {[c['name'] for c in cats]}")
    
    conn.close()

if __name__ == '__main__':
    test_import()
