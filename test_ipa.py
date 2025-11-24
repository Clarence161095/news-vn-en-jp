#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test IPA generation to identify issues
"""

import re

try:
    import eng_to_ipa as ipa
    IPA_AVAILABLE = True
except ImportError:
    IPA_AVAILABLE = False
    print("Error: eng-to-ipa not installed!")
    exit(1)

def generate_ipa_html_fixed(text):
    """FIXED function - Process ALL words"""
    if not IPA_AVAILABLE or not text:
        return text
    
    try:
        result = []
        ipa_cache = {}
        
        # Process character by character
        i = 0
        while i < len(text):
            # Check if we're at an HTML tag
            if text[i] == '<':
                # Find the end of the tag
                tag_end = text.find('>', i)
                if tag_end == -1:
                    # Malformed HTML, treat as text
                    result.append(text[i])
                    i += 1
                    continue
                
                # Extract full tag
                tag = text[i:tag_end + 1]
                result.append(tag)
                i = tag_end + 1
            else:
                # We're in text content - extract until next tag
                next_tag = text.find('<', i)
                if next_tag == -1:
                    # No more tags, process rest of text
                    text_content = text[i:]
                    result.append(process_text_with_ipa(text_content, ipa_cache))
                    break
                else:
                    # Process text until next tag
                    text_content = text[i:next_tag]
                    result.append(process_text_with_ipa(text_content, ipa_cache))
                    i = next_tag
        
        return ''.join(result)
    except Exception as e:
        print(f"Error generating IPA: {e}")
        import traceback
        traceback.print_exc()
        return text

def process_text_with_ipa(text, ipa_cache):
    """Process plain text and wrap each word with IPA ruby tags"""
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

def test_simple_text():
    """Test 1: Simple text without HTML"""
    print("\n=== TEST 1: Simple Text ===")
    text = "Hello world this is a test of vibe coding"
    result = generate_ipa_html_fixed(text)
    
    # Count words in original
    original_words = re.findall(r'\b[\w\']+\b', text)
    # Count ruby tags in result
    ruby_count = result.count('<ruby>')
    
    print(f"Original: {text}")
    print(f"Original word count: {len(original_words)}")
    print(f"Ruby tags generated: {ruby_count}")
    print(f"Result preview: {result[:200]}...")
    
    if ruby_count == len(original_words):
        print("✅ PASS: All words processed")
    else:
        print(f"❌ FAIL: Expected {len(original_words)} ruby tags, got {ruby_count}")
        print(f"Missing: {len(original_words) - ruby_count} words")

def test_text_with_html():
    """Test 2: Text with HTML tags"""
    print("\n=== TEST 2: Text with HTML ===")
    text = "<p>Hello world</p><p>This is a test</p>"
    result = generate_ipa_html_fixed(text)
    
    # Extract text from HTML
    text_only = re.sub(r'<[^>]+>', '', text)
    original_words = re.findall(r'\b[\w\']+\b', text_only)
    ruby_count = result.count('<ruby>')
    
    print(f"Original: {text}")
    print(f"Original word count: {len(original_words)}")
    print(f"Ruby tags generated: {ruby_count}")
    print(f"Result preview: {result[:300]}...")
    
    if ruby_count == len(original_words):
        print("✅ PASS: All words processed")
    else:
        print(f"❌ FAIL: Expected {len(original_words)} ruby tags, got {ruby_count}")

def test_table():
    """Test 3: Text in table"""
    print("\n=== TEST 3: Table ===")
    text = "<table><tr><td>Hello world</td><td>This is test</td></tr></table>"
    result = generate_ipa_html_fixed(text)
    
    # Extract text from HTML
    text_only = re.sub(r'<[^>]+>', '', text)
    original_words = re.findall(r'\b[\w\']+\b', text_only)
    ruby_count = result.count('<ruby>')
    
    print(f"Original: {text}")
    print(f"Original word count: {len(original_words)}")
    print(f"Ruby tags generated: {ruby_count}")
    print(f"Result preview: {result[:300]}...")
    
    if ruby_count == len(original_words):
        print("✅ PASS: All words processed")
    else:
        print(f"❌ FAIL: Expected {len(original_words)} ruby tags, got {ruby_count}")

def test_list():
    """Test 4: Text in list"""
    print("\n=== TEST 4: List ===")
    text = "<ul><li>Hello world</li><li>This is test</li></ul>"
    result = generate_ipa_html_fixed(text)
    
    # Extract text from HTML
    text_only = re.sub(r'<[^>]+>', '', text)
    original_words = re.findall(r'\b[\w\']+\b', text_only)
    ruby_count = result.count('<ruby>')
    
    print(f"Original: {text}")
    print(f"Original word count: {len(original_words)}")
    print(f"Ruby tags generated: {ruby_count}")
    print(f"Result preview: {result[:300]}...")
    
    if ruby_count == len(original_words):
        print("✅ PASS: All words processed")
    else:
        print(f"❌ FAIL: Expected {len(original_words)} ruby tags, got {ruby_count}")

def test_mixed_content():
    """Test 5: Mixed content"""
    print("\n=== TEST 5: Mixed Content ===")
    text = """
    <h1>What is vibe coding?</h1>
    <p>Vibe coding is a way of programming where you mainly talk to the AI in natural language.</p>
    <ul>
        <li>Almost no reading or writing code</li>
        <li>Judge quality based on UI, trial runs, logs, tests</li>
    </ul>
    """
    result = generate_ipa_html_fixed(text)
    
    # Extract text from HTML
    text_only = re.sub(r'<[^>]+>', '', text)
    original_words = re.findall(r'\b[\w\']+\b', text_only)
    ruby_count = result.count('<ruby>')
    
    print(f"Original word count: {len(original_words)}")
    print(f"Ruby tags generated: {ruby_count}")
    
    if ruby_count == len(original_words):
        print("✅ PASS: All words processed")
    else:
        print(f"❌ FAIL: Expected {len(original_words)} ruby tags, got {ruby_count}")
        print(f"Missing: {len(original_words) - ruby_count} words")
        
        # Show which words are missing
        print("\n=== Debugging: Checking each word ===")
        for word in original_words:
            if f'<ruby>{word}' not in result and f'<ruby>{word.lower()}' not in result.lower():
                print(f"❌ Missing: {word}")

def test_actual_article():
    """Test 6: From actual database article"""
    print("\n=== TEST 6: Actual Article Content ===")
    
    # Simulate getting from database
    import sqlite3
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get first article
    row = cursor.execute('SELECT content_en FROM articles LIMIT 1').fetchone()
    
    if not row:
        print("❌ No articles found in database")
        return
    
    text = row['content_en']
    conn.close()
    
    # Test generation
    result = generate_ipa_html_fixed(text)
    
    # Extract text from HTML
    text_only = re.sub(r'<[^>]+>', '', text)
    original_words = re.findall(r'\b[\w\']+\b', text_only)
    ruby_count = result.count('<ruby>')
    
    print(f"Article preview: {text[:200]}...")
    print(f"Original word count: {len(original_words)}")
    print(f"Ruby tags generated: {ruby_count}")
    print(f"Coverage: {ruby_count}/{len(original_words)} = {(ruby_count/len(original_words)*100):.1f}%")
    
    if ruby_count >= len(original_words) * 0.95:  # 95% threshold
        print("✅ PASS: Most words processed")
    else:
        print(f"❌ FAIL: Only {(ruby_count/len(original_words)*100):.1f}% coverage")
        print(f"Missing approximately {len(original_words) - ruby_count} words")

if __name__ == '__main__':
    print("=" * 60)
    print("IPA GENERATION TEST SUITE")
    print("=" * 60)
    
    test_simple_text()
    test_text_with_html()
    test_table()
    test_list()
    test_mixed_content()
    test_actual_article()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
