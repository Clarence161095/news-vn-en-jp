#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clear IPA cache from database
"""

import sqlite3
import sys

def clear_ipa_cache():
    """Clear all IPA cache entries"""
    try:
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        
        # Count before delete
        count = cursor.execute('SELECT COUNT(*) FROM article_cache').fetchone()[0]
        print(f"Found {count} cached articles")
        
        # Delete all cache
        cursor.execute('DELETE FROM article_cache')
        conn.commit()
        
        print(f"✅ Successfully cleared {count} IPA cache entries")
        print("IPA will be regenerated when you view articles")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("CLEAR IPA CACHE")
    print("=" * 60)
    
    if clear_ipa_cache():
        sys.exit(0)
    else:
        sys.exit(1)
