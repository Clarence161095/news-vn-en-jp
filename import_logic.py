"""
Import logic - Separated for better reload
"""

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
    
    # 1. Add username category if provided
    if username and username.strip():
        categories_to_add.append(username.strip())
    
    # 2. Add category from JSON if provided
    if json_category and json_category.strip():
        json_cat = json_category.strip()
        if json_cat not in categories_to_add:
            categories_to_add.append(json_cat)
    
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
                print(f"➕ Creating new category: '{category_name}'")
                cat_cursor = conn.execute(
                    'INSERT INTO categories (name) VALUES (?)', 
                    (category_name,)
                )
                cat_id = cat_cursor.lastrowid
            else:
                cat_id = cat_result['id']
                print(f"✓ Found existing category: '{category_name}' (ID: {cat_id})")
            
            # Link category to article
            conn.execute('''
                INSERT OR IGNORE INTO article_categories (article_id, category_id)
                VALUES (?, ?)
            ''', (article_id, cat_id))
            
            # Verify link was created
            verify = conn.execute('''
                SELECT * FROM article_categories 
                WHERE article_id = ? AND category_id = ?
            ''', (article_id, cat_id)).fetchone()
            
            if verify:
                print(f"✅ Added category '{category_name}' (ID: {cat_id}) to article {article_id}")
                added_categories.append(category_name)
            else:
                print(f"⚠️ Failed to verify category link for article {article_id}")
                
        except Exception as e:
            print(f"❌ Error adding category '{category_name}': {e}")
            import traceback
            traceback.print_exc()
    
    if added_categories:
        print(f"📂 Total categories added to article {article_id}: {', '.join(added_categories)}")
    
    return added_categories
