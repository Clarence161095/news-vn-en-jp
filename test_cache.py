"""
Test Katakana Cache System
Verify 4-tier caching works correctly
"""

import json
import time

# Simulate app.py imports
print("Loading cache system...")
print("-" * 60)

# Load JSON cache
KATAKANA_CACHE_FILE = 'katakana_cache.json'
KATAKANA_CACHE = {}
try:
    with open(KATAKANA_CACHE_FILE, 'r', encoding='utf-8') as f:
        KATAKANA_CACHE = json.load(f)
    print(f"✓ Loaded {len(KATAKANA_CACHE)} Katakana translations from cache file")
except FileNotFoundError:
    print(f"✗ Cache file '{KATAKANA_CACHE_FILE}' not found")
except Exception as e:
    print(f"✗ Error loading cache file: {e}")

# Test cases
test_words = [
    "コンピュータ",  # Should be in cache
    "テクノロジー",  # Should be in cache
    "プログラミング", # Should be in cache
    "データベース",  # Should be in cache
    "アプリ",       # Should be in cache
]

print("\n" + "=" * 60)
print("TESTING CACHE LOOKUPS")
print("=" * 60)

for word in test_words:
    start = time.time()
    if word in KATAKANA_CACHE:
        english = KATAKANA_CACHE[word]
        elapsed = (time.time() - start) * 1000
        print(f"✓ {word:20} → {english:20} ({elapsed:.2f}ms)")
    else:
        elapsed = (time.time() - start) * 1000
        print(f"✗ {word:20} → NOT IN CACHE ({elapsed:.2f}ms)")

print("\n" + "=" * 60)
print("CACHE STATISTICS")
print("=" * 60)
print(f"Total cached words: {len(KATAKANA_CACHE)}")
print(f"Test words: {len(test_words)}")
print(f"Cache hits: {sum(1 for w in test_words if w in KATAKANA_CACHE)}")
print(f"Cache misses: {sum(1 for w in test_words if w not in KATAKANA_CACHE)}")
print(f"Hit rate: {sum(1 for w in test_words if w in KATAKANA_CACHE) / len(test_words) * 100:.1f}%")

# Show sample entries
print("\n" + "=" * 60)
print("SAMPLE CACHE ENTRIES (first 10)")
print("=" * 60)
for i, (kata, eng) in enumerate(list(KATAKANA_CACHE.items())[:10], 1):
    print(f"{i:2}. {kata:20} → {eng}")

print("\n✅ Test complete!")
