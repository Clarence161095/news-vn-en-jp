#!/bin/bash

# Debug script để test cleanup categories

echo "🔍 Kiểm tra database categories..."
echo ""

cd "$(dirname "$0")"

# Check database
sqlite3 articles.db << EOF
.headers on
.mode column

-- Tổng số categories
SELECT 'Total categories:' as info, COUNT(*) as count FROM categories;

-- Categories có bài viết
SELECT 'Categories with articles:' as info, COUNT(DISTINCT category_id) as count 
FROM article_categories;

-- Categories KHÔNG có bài viết (unused)
SELECT 'Unused categories:' as info, COUNT(*) as count 
FROM categories 
WHERE id NOT IN (SELECT DISTINCT category_id FROM article_categories WHERE category_id IS NOT NULL);

-- Liệt kê chi tiết unused categories
SELECT '' as blank;
SELECT '=== UNUSED CATEGORIES ===' as header;
SELECT id, name, created_at 
FROM categories 
WHERE id NOT IN (SELECT DISTINCT category_id FROM article_categories WHERE category_id IS NOT NULL);

-- Liệt kê categories đang được sử dụng
SELECT '' as blank;
SELECT '=== USED CATEGORIES ===' as header;
SELECT c.id, c.name, COUNT(ac.article_id) as article_count
FROM categories c
JOIN article_categories ac ON c.id = ac.category_id
GROUP BY c.id, c.name
ORDER BY article_count DESC;

EOF

echo ""
echo "✅ Hoàn tất kiểm tra!"
