#!/usr/bin/env python3
"""
Script to add username category to old articles that don't have it
Usage: python migrate_old_articles.py <username>
Example: python migrate_old_articles.py Clarence
"""

import sqlite3
import sys

def migrate_articles(username):
    """Add username category to all articles that don't have it"""
    
    if not username or not username.strip():
        print("❌ Error: Username is required")
        print("Usage: python migrate_old_articles.py <username>")
        return
    
    username = username.strip()
    
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    
    print("=" * 80)
    print(f"MIGRATING OLD ARTICLES TO ADD CATEGORY: {username}")
    print("=" * 80)
    
    # Get or create username category
    cat_result = conn.execute('SELECT id FROM categories WHERE name = ?', (username,)).fetchone()
    if not cat_result:
        print(f"\n➕ Creating new category: '{username}'")
        cursor = conn.execute('INSERT INTO categories (name) VALUES (?)', (username,))
        cat_id = cursor.lastrowid
        print(f"✅ Created category ID: {cat_id}")
    else:
        cat_id = cat_result['id']
        print(f"\n✓ Found existing category: '{username}' (ID: {cat_id})")
    
    # Find articles without this category
    cursor = conn.execute('''
        SELECT a.id, a.title_vi, a.created_by
        FROM articles a
        WHERE a.id NOT IN (
            SELECT article_id 
            FROM article_categories 
            WHERE category_id = ?
        )
    ''', (cat_id,))
    
    articles_to_update = cursor.fetchall()
    
    if not articles_to_update:
        print(f"\n✅ No articles to migrate. All articles already have category '{username}'")
        conn.close()
        return
    
    print(f"\n📝 Found {len(articles_to_update)} articles to migrate:")
    for article in articles_to_update:
        print(f"  - Article {article['id']}: {article['title_vi'][:50]}...")
    
    # Ask for confirmation
    print(f"\n⚠️  This will add category '{username}' to {len(articles_to_update)} articles.")
    response = input("Continue? [y/N]: ")
    
    if response.lower() != 'y':
        print("❌ Migration cancelled")
        conn.close()
        return
    
    # Migrate articles
    migrated_count = 0
    for article in articles_to_update:
        try:
            conn.execute('''
                INSERT OR IGNORE INTO article_categories (article_id, category_id)
                VALUES (?, ?)
            ''', (article['id'], cat_id))
            
            # Also update created_by if it's NULL
            if not article['created_by']:
                conn.execute('''
                    UPDATE articles 
                    SET created_by = ? 
                    WHERE id = ?
                ''', (username, article['id']))
            
            migrated_count += 1
            print(f"✅ Migrated article {article['id']}")
            
        except Exception as e:
            print(f"❌ Failed to migrate article {article['id']}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"✅ MIGRATION COMPLETE: {migrated_count}/{len(articles_to_update)} articles migrated")
    print("=" * 80)
    
    # Show updated stats
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    
    cursor = conn.execute('''
        SELECT 
            COUNT(DISTINCT a.id) as total_articles,
            COUNT(DISTINCT ac.article_id) as articles_with_category
        FROM articles a
        LEFT JOIN article_categories ac ON a.id = ac.article_id AND ac.category_id = ?
    ''', (cat_id,))
    
    stats = cursor.fetchone()
    conn.close()
    
    print(f"\n📊 Statistics:")
    print(f"  Total articles: {stats['total_articles']}")
    print(f"  Articles with '{username}' category: {stats['articles_with_category']}")
    print(f"  Coverage: {stats['articles_with_category'] / stats['total_articles'] * 100:.1f}%")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Error: Username is required")
        print("Usage: python migrate_old_articles.py <username>")
        print("Example: python migrate_old_articles.py Clarence")
        sys.exit(1)
    
    username = sys.argv[1]
    migrate_articles(username)
