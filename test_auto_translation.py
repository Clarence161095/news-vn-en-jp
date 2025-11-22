#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Automatic Katakana to English Translation using Google Translate
"""

import re
from pykakasi import kakasi
from deep_translator import GoogleTranslator

# Initialize
kks = kakasi()
translator = GoogleTranslator(source='ja', target='en')

# Fallback dictionary (sẽ ít hơn nhiều)
KATAKANA_TO_ENGLISH_FALLBACK = {
    'コンピュータ': 'computer',
    'データベース': 'database',
    'AWS': 'AWS',
}

def translate_katakana_to_english(katakana_text):
    """
    Dịch Katakana sang tiếng Anh
    """
    if not katakana_text or len(katakana_text) <= 1:
        return None
    
    # Kiểm tra fallback dictionary trước
    if katakana_text in KATAKANA_TO_ENGLISH_FALLBACK:
        return KATAKANA_TO_ENGLISH_FALLBACK[katakana_text]
    
    # Dùng Google Translate
    try:
        result = translator.translate(katakana_text)
        if result and result.lower() != katakana_text.lower():
            return result
    except Exception as e:
        print(f"Translation error: {e}")
    
    return None

def generate_furigana_html(text):
    """
    Tự động chuyển đổi văn bản tiếng Nhật sang HTML với Furigana
    """
    if not text:
        return text
    
    try:
        html_parts = re.split(r'(<[^>]+>)', text)
        result = []
        
        for part in html_parts:
            if part.startswith('<'):
                result.append(part)
            else:
                converted = kks.convert(part)
                for item in converted:
                    orig = item['orig']
                    hira = item['hira']
                    hepburn = item.get('hepburn', hira)
                    
                    is_katakana = bool(re.search(r'[\u30A0-\u30FF]+', orig))
                    
                    if is_katakana and len(orig) > 1:
                        # Dịch Katakana → English
                        english = translate_katakana_to_english(orig)
                        if english:
                            result.append(f'<ruby>{orig}<rt>{english}</rt></ruby>')
                        else:
                            result.append(f'<ruby>{orig}<rt>{hepburn}</rt></ruby>')
                    elif orig != hira and re.search(r'[\u4e00-\u9fff]', orig):
                        result.append(f'<ruby>{orig}<rt>{hira}</rt></ruby>')
                    else:
                        result.append(orig)
        
        return ''.join(result)
    except Exception as e:
        print(f"Error: {e}")
        return text

# Test với các từ KHÔNG CÓ trong fallback dictionary
test_texts = [
    "コンピュータの使い方",      # computer (có trong dictionary)
    "テクノロジー業界",          # Technology (KHÔNG có trong dictionary)
    "インターネット接続",        # Internet (KHÔNG có trong dictionary)  
    "スマートフォン開発",        # Smartphone (KHÔNG có trong dictionary)
    "ソフトウェアエンジニア",    # Software Engineer (KHÔNG có trong dictionary)
    "ネットワーク管理",          # Network (KHÔNG có trong dictionary)
    "セキュリティ対策",          # Security (KHÔNG có trong dictionary)
]

print("=" * 80)
print("Automatic Katakana → English Translation Test")
print("Testing with words NOT in fallback dictionary")
print("=" * 80)

for text in test_texts:
    print(f"\n{'='*80}")
    print(f"Original: {text}")
    html = generate_furigana_html(text)
    print(f"HTML:     {html}")
    
    # Extract ruby tags
    ruby_tags = re.findall(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>', html)
    if ruby_tags:
        print("\nRuby tags:")
        for orig, rt in ruby_tags:
            is_katakana = bool(re.search(r'[\u30A0-\u30FF]', orig))
            is_english = not bool(re.search(r'[ぁ-んァ-ン]', rt))
            
            if is_katakana:
                in_dict = orig in KATAKANA_TO_ENGLISH_FALLBACK
                source = "DICT" if in_dict else "AUTO"
                marker = "✓ EN" if is_english else "✗ romaji"
                print(f"  {orig} → {rt} [{source}] {marker}")
            else:
                print(f"  {orig} → {rt} [Kanji]")

print("\n" + "=" * 80)
print("✓ Test Complete!")
print("Check if Katakana words are translated to English automatically")
print("=" * 80)
