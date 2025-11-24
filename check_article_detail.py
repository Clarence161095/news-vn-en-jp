import sqlite3

conn = sqlite3.connect('articles.db')
conn.row_factory = sqlite3.Row

print("=" * 80)
print("DETAILED ARTICLE 2 INFO:")
print("=" * 80)

# Get article 2
article = conn.execute('SELECT * FROM articles WHERE id = 2').fetchone()
if article:
    print(f"\nArticle ID: {article['id']}")
    print(f"Title VI: {article['title_vi']}")
    print(f"Title EN: {article['title_en']}")
    print(f"Category (old field): {article['category']}")
    print(f"Created By: {article['created_by']}")
    
    # Get categories from article_categories table
    categories = conn.execute('''
        SELECT c.id, c.name 
        FROM categories c
        JOIN article_categories ac ON c.id = ac.category_id
        WHERE ac.article_id = ?
    ''', (article['id'],)).fetchall()
    
    print(f"\nCategories (new system):")
    if categories:
        for cat in categories:
            print(f"  - {cat['name']} (ID: {cat['id']})")
    else:
        print("  (none)")

print("\n" + "=" * 80)
print("ALL CATEGORIES IN DATABASE:")
print("=" * 80)

all_cats = conn.execute('SELECT * FROM categories').fetchall()
for cat in all_cats:
    print(f"  ID {cat['id']}: {cat['name']}")

print("\n" + "=" * 80)
print("ARTICLE_CATEGORIES LINKS:")
print("=" * 80)

links = conn.execute('SELECT * FROM article_categories').fetchall()
for link in links:
    print(f"  Article {link['article_id']} → Category {link['category_id']}")

conn.close()
