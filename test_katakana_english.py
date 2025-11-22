#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Katakana to English conversion
"""

import re
from pykakasi import kakasi

# Katakana to English dictionary (from app.py)
KATAKANA_TO_ENGLISH = {
    'コンピュータ': 'computer',
    'コンピューター': 'computer',
    'プログラミング': 'programming',
    'プログラム': 'program',
    'データベース': 'database',
    'データ': 'data',
    'クラウド': 'cloud',
    'サーバー': 'server',
    'サーバ': 'server',
    'AWS': 'AWS',
}

# Initialize pykakasi
kks = kakasi()

def generate_furigana_html(text):
    """
    Tự động chuyển đổi văn bản tiếng Nhật sang HTML với Furigana trong ruby tags
    - Kanji: Hiện Furigana bằng Hiragana (日本語 → にほんご)
    - Katakana: Hiện bằng tiếng Anh nếu có trong dictionary (コンピュータ → computer)
    """
    if not text:
        return text
    
    try:
        # Tách thành các đoạn HTML và text
        html_parts = re.split(r'(<[^>]+>)', text)
        result = []
        
        for part in html_parts:
            # Nếu là HTML tag, giữ nguyên
            if part.startswith('<'):
                result.append(part)
            else:
                # Xử lý text tiếng Nhật
                converted = kks.convert(part)
                for item in converted:
                    orig = item['orig']
                    hira = item['hira']
                    hepburn = item.get('hepburn', hira)
                    
                    # Kiểm tra nếu là Katakana
                    is_katakana = bool(re.search(r'[\u30A0-\u30FF]+', orig))
                    
                    if is_katakana and len(orig) > 1:
                        # Katakana → Tìm tiếng Anh trong dictionary
                        english = KATAKANA_TO_ENGLISH.get(orig, None)
                        if english:
                            # Nếu tìm thấy trong dictionary, dùng tiếng Anh
                            result.append(f'<ruby>{orig}<rt>{english}</rt></ruby>')
                        else:
                            # Nếu không tìm thấy, dùng Romanization như fallback
                            result.append(f'<ruby>{orig}<rt>{hepburn}</rt></ruby>')
                    elif orig != hira and re.search(r'[\u4e00-\u9fff]', orig):
                        # Kanji → Hiện Furigana bằng Hiragana
                        result.append(f'<ruby>{orig}<rt>{hira}</rt></ruby>')
                    else:
                        result.append(orig)
        
        return ''.join(result)
    except Exception as e:
        print(f"Error: {e}")
        return text

# Test cases
test_texts = [
    "コンピュータの使い方",  # computer no tsukaikata
    "AWSクラウドサービス",   # AWS cloud service
    "データベース設計",      # database sekkei
    "プログラミング言語",    # programming gengo
    "サーバー管理",         # server kanri
]

print("=" * 60)
print("Katakana to English Test")
print("=" * 60)

for text in test_texts:
    html = generate_furigana_html(text)
    print(f"\nOriginal: {text}")
    print(f"HTML:     {html}")
    
    # Extract and show ruby tags
    ruby_tags = re.findall(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>', html)
    if ruby_tags:
        print("Ruby tags:")
        for orig, rt in ruby_tags:
            is_english = not bool(re.search(r'[ぁ-んァ-ン]', rt))  # Check if rt is English
            marker = "✓ ENGLISH" if is_english and re.search(r'[\u30A0-\u30FF]', orig) else "✗ romaji"
            print(f"  {orig} → {rt} {marker}")

print("\n" + "=" * 60)
