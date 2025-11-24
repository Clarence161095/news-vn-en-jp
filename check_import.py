import sqlite3

conn = sqlite3.connect('articles.db')
conn.row_factory = sqlite3.Row

# Check last 5 articles
print("=" * 80)
print("LAST 5 IMPORTED ARTICLES:")
print("=" * 80)

cursor = conn.execute('''
    SELECT 
        a.id,
        a.title_vi,
        a.title_en,
        a.created_by,
        GROUP_CONCAT(c.name) as categories
    FROM articles a
    LEFT JOIN article_categories ac ON a.id = ac.article_id
    LEFT JOIN categories c ON ac.category_id = c.id
    GROUP BY a.id
    ORDER BY a.id DESC
    LIMIT 5
''')

for row in cursor.fetchall():
    print(f"\nArticle ID: {row['id']}")
    print(f"  Title VI: {row['title_vi'][:50]}...")
    print(f"  Created By: {row['created_by']}")
    print(f"  Categories: {row['categories'] or '(none)'}")

print("\n" + "=" * 80)
print("ALL CATEGORIES:")
print("=" * 80)

cursor = conn.execute('SELECT * FROM categories')
for row in cursor.fetchall():
    print(f"  ID {row['id']}: {row['name']}")

conn.close()
