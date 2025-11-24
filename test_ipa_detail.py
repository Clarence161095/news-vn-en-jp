#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detailed test to find missing words
"""

import re
import sqlite3

try:
    import eng_to_ipa as ipa
    IPA_AVAILABLE = True
except ImportError:
    IPA_AVAILABLE = False
    print("Error: eng-to-ipa not installed!")
    exit(1)

def generate_ipa_html_fixed(text):
    """FIXED function"""
    if not IPA_AVAILABLE or not text:
        return text
    
    try:
        result = []
        ipa_cache = {}
        
        i = 0
        while i < len(text):
            if text[i] == '<':
                tag_end = text.find('>', i)
                if tag_end == -1:
                    result.append(text[i])
                    i += 1
                    continue
                
                tag = text[i:tag_end + 1]
                result.append(tag)
                i = tag_end + 1
            else:
                next_tag = text.find('<', i)
                if next_tag == -1:
                    text_content = text[i:]
                    result.append(process_text_with_ipa(text_content, ipa_cache))
                    break
                else:
                    text_content = text[i:next_tag]
                    result.append(process_text_with_ipa(text_content, ipa_cache))
                    i = next_tag
        
        return ''.join(result)
    except Exception as e:
        print(f"Error: {e}")
        return text

def process_text_with_ipa(text, ipa_cache):
    """Process plain text"""
    if not text or not text.strip():
        return text
    
    result = []
    tokens = re.findall(r'\b[\w\']+\b|[^\w\s]|\s+', text)
    
    for token in tokens:
        if re.match(r'\b[\w\']+\b', token):
            token_lower = token.lower()
            if token_lower in ipa_cache:
                ipa_text = ipa_cache[token_lower]
            else:
                try:
                    ipa_text = ipa.convert(token)
                    ipa_cache[token_lower] = ipa_text
                except:
                    ipa_text = None
            
            if ipa_text and ipa_text != token:
                result.append(f'<ruby>{token}<rt>{ipa_text}</rt></ruby>')
            else:
                result.append(token)
        else:
            result.append(token)
    
    return ''.join(result)

def find_missing_words():
    """Find which words are missing IPA"""
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    row = cursor.execute('SELECT id, title_en, content_en FROM articles LIMIT 1').fetchone()
    
    if not row:
        print("No articles found")
        return
    
    text = row['content_en']
    conn.close()
    
    # Generate IPA
    result = generate_ipa_html_fixed(text)
    
    # Extract all words from original
    text_only = re.sub(r'<[^>]+>', '', text)
    original_words = re.findall(r'\b[\w\']+\b', text_only)
    
    # Find missing words
    missing_words = []
    for word in original_words:
        # Check if word appears in result with ruby tag
        if f'<ruby>{word}' not in result:
            # Maybe it's lowercase?
            word_variants = [word, word.lower(), word.upper(), word.capitalize()]
            found = False
            for variant in word_variants:
                if f'<ruby>{variant}' in result:
                    found = True
                    break
            
            if not found:
                missing_words.append(word)
    
    print(f"Total words: {len(original_words)}")
    print(f"Ruby tags: {result.count('<ruby>')}")
    print(f"Missing words: {len(missing_words)}")
    print(f"Coverage: {((len(original_words) - len(missing_words)) / len(original_words) * 100):.1f}%")
    
    if missing_words:
        print("\n=== Missing Words (first 50) ===")
        unique_missing = list(set(missing_words))[:50]
        for word in unique_missing:
            # Try to convert manually
            try:
                ipa_result = ipa.convert(word)
                print(f"  - {word} -> IPA: {ipa_result} (should work)")
            except Exception as e:
                print(f"  - {word} -> ERROR: {e}")

if __name__ == '__main__':
    find_missing_words()
