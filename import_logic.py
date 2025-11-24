"""
Import logic - Separated for better reload
Version: 2024-11-24-16:45-FIXED
"""
import sys
from datetime import datetime

# Force reload marker
IMPORT_LOGIC_VERSION = "2024-11-24-16:45-FIXED"
print(f"🔄 Loading import_logic.py version: {IMPORT_LOGIC_VERSION}", flush=True)

def add_categories_to_article(conn, article_id, username, json_category):
    """
    Add both username and JSON category to article
    
    Args:
        conn: Database connection
        article_id: ID of the article
        username: Username to add as category
        json_category: Category from JSON field
    
    Returns:
        list: Names of categories added
    """
    categories_to_add = []
    
    print(f"🔍 add_categories_to_article called:", flush=True)
    print(f"   article_id={article_id}", flush=True)
    print(f"   username='{username}'", flush=True)
    print(f"   json_category='{json_category}'", flush=True)
    
    # 1. Add username category if provided
    if username and username.strip():
        categories_to_add.append(username.strip())
        print(f"   ✅ Added username '{username.strip()}' to list", flush=True)
    
    # 2. Add category from JSON if provided
    if json_category and json_category.strip():
        json_cat = json_category.strip()
        if json_cat not in categories_to_add:
            categories_to_add.append(json_cat)
            print(f"   ✅ Added JSON category '{json_cat}' to list", flush=True)
        else:
            print(f"   ⚠️ JSON category '{json_cat}' already in list", flush=True)
    
    print(f"   📋 Categories to add: {categories_to_add}", flush=True)
    
    # Add all categories to article
    added_categories = []
    for category_name in categories_to_add:
        try:
            # Get or create category
            cat_result = conn.execute(
                'SELECT id FROM categories WHERE name = ?', 
                (category_name,)
            ).fetchone()
            
            if not cat_result:
                print(f"   ➕ Creating new category: '{category_name}'", flush=True)
                cat_cursor = conn.execute(
                    'INSERT INTO categories (name) VALUES (?)', 
                    (category_name,)
                )
                cat_id = cat_cursor.lastrowid
                print(f"   ✅ Created category ID: {cat_id}", flush=True)
            else:
                cat_id = cat_result['id']
                print(f"   ✓ Found existing category: '{category_name}' (ID: {cat_id})", flush=True)
            
            # Link category to article
            conn.execute('''
                INSERT OR IGNORE INTO article_categories (article_id, category_id)
                VALUES (?, ?)
            ''', (article_id, cat_id))
            print(f"   🔗 Linked article {article_id} → category {cat_id}", flush=True)
            
            # Verify link was created
            verify = conn.execute('''
                SELECT * FROM article_categories 
                WHERE article_id = ? AND category_id = ?
            ''', (article_id, cat_id)).fetchone()
            
            if verify:
                print(f"   ✅ VERIFIED: Category '{category_name}' linked to article {article_id}", flush=True)
                added_categories.append(category_name)
            else:
                print(f"   ❌ FAILED TO VERIFY: Category link for article {article_id}", flush=True)
                
        except Exception as e:
            print(f"   ❌ ERROR adding category '{category_name}': {e}", flush=True)
            import traceback
            traceback.print_exc()
    
    print(f"   📊 Final result: {len(added_categories)}/{len(categories_to_add)} categories added", flush=True)
    print(f"   📂 Added categories: {added_categories}", flush=True)
    
    return added_categories
