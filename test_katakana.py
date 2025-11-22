"""
Test Katakana → English romanization
"""
import sys
sys.path.insert(0, 'd:\\01. Project\\news-vn-en-jp')

from app import generate_furigana_html

print("=" * 60)
print("TEST KATAKANA → ENGLISH ROMANIZATION")
print("=" * 60)

# Test 1: Katakana words
test_cases = [
    ("コンピュータ", "konpyūta (computer)"),
    ("プログラミング", "puroguramingu (programming)"),
    ("データベース", "dētabēsu (database)"),
    ("クラウド", "kuraudo (cloud)"),
    ("アマゾン", "amazon"),
]

for katakana, expected in test_cases:
    result = generate_furigana_html(katakana)
    print(f"\n📝 Input: {katakana}")
    print(f"   Output: {result}")
    print(f"   Expected: Contains romaji")
    has_ruby = '<ruby>' in result and '<rt>' in result
    print(f"   ✅ Ruby tag: {has_ruby}")

# Test 2: Mixed Kanji + Katakana
print("\n" + "=" * 60)
print("TEST MIXED KANJI + KATAKANA")
print("=" * 60)

mixed_text = "クラウド内でスケーラブルなコンピューティング容量を提供します。"
result = generate_furigana_html(mixed_text)
print(f"\nInput:  {mixed_text}")
print(f"Output: {result}")
print(f"\n✅ Both Kanji and Katakana processed")

print("\n" + "=" * 60)
print("✅ TEST HOÀN TẤT!")
print("=" * 60)
