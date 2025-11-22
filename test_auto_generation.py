"""
Test script để kiểm tra tự động tạo IPA và Furigana
"""
import sys
sys.path.insert(0, 'd:\\01. Project\\news-vn-en-jp')

from app import generate_ipa_html, generate_furigana_html

print("=" * 60)
print("TEST TỰ ĐỘNG TẠO IPA VÀ FURIGANA")
print("=" * 60)

# Test 1: IPA cho tiếng Anh
print("\n📝 TEST 1: Tự động tạo IPA cho tiếng Anh")
print("-" * 60)
english_text = "Amazon Web Services is the world's most comprehensive cloud platform."
result_ipa = generate_ipa_html(english_text)
print(f"Input:  {english_text}")
print(f"Output: {result_ipa[:200]}...")
print(f"✅ IPA generated: {bool('<ruby>' in result_ipa and '<rt>' in result_ipa)}")

# Test 2: Furigana cho tiếng Nhật
print("\n📝 TEST 2: Tự động tạo Furigana cho tiếng Nhật")
print("-" * 60)
japanese_text = "世界で最も包括的なクラウドプラットフォーム"
result_furigana = generate_furigana_html(japanese_text)
print(f"Input:  {japanese_text}")
print(f"Output: {result_furigana}")
print(f"✅ Furigana generated: {bool('<ruby>' in result_furigana and '<rt>' in result_furigana)}")

# Test 3: HTML content với IPA
print("\n📝 TEST 3: HTML content với IPA")
print("-" * 60)
html_text = "<p><strong>EC2 (Elastic Compute Cloud):</strong> Provides scalable computing capacity.</p>"
result_html_ipa = generate_ipa_html(html_text)
print(f"Input:  {html_text}")
print(f"Output: {result_html_ipa[:150]}...")
print(f"✅ HTML preserved: {bool('<p>' in result_html_ipa and '<strong>' in result_html_ipa)}")
print(f"✅ IPA added: {bool('<ruby>' in result_html_ipa)}")

# Test 4: HTML content với Furigana
print("\n📝 TEST 4: HTML content với Furigana")
print("-" * 60)
html_jp = "<p><strong>EC2（Elastic Compute Cloud）：</strong>クラウド内でスケーラブルなコンピューティング容量を提供します。</p>"
result_html_furigana = generate_furigana_html(html_jp)
print(f"Input:  {html_jp}")
print(f"Output: {result_html_furigana[:150]}...")
print(f"✅ HTML preserved: {bool('<p>' in result_html_furigana and '<strong>' in result_html_furigana)}")
print(f"✅ Furigana added: {bool('<ruby>' in result_html_furigana)}")

print("\n" + "=" * 60)
print("✅ TẤT CẢ TEST HOÀN TẤT!")
print("=" * 60)
