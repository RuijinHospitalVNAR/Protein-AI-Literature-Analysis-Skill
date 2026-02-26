#!/usr/bin/env python3
"""
Utilities for Protein AI Literature Analysis

Common helper functions used across the literature analysis pipeline:
- Text processing utilities
- API rate limiting helpers
- File I/O operations
- Data validation functions
"""

import os
import json
import time
import re
from datetime import datetime

class RateLimiter:
    """Simple rate limiter to respect API limits"""
    def __init__(self, max_calls, period):
        """
        Initialize rate limiter
        
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def wait(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove calls outside the period
        self.calls = [call for call in self.calls if now - call < self.period]
        
        # Wait if we've reached the limit
        if len(self.calls) >= self.max_calls:
            wait_time = self.period - (now - self.calls[0])
            if wait_time > 0:
                time.sleep(wait_time)
        
        # Record this call
        self.calls.append(time.time())

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters at the beginning/end
    text = text.strip()
    
    return text

def save_json(data, file_path, indent=2):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def load_json(file_path):
    """Load data from JSON file"""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_authors(authors):
    """Format authors list for display"""
    if not authors:
        return ""
    
    if isinstance(authors, str):
        return authors
    
    if len(authors) <= 5:
        return ', '.join(authors)
    else:
        return f"{', '.join(authors[:5])} et al. ({len(authors)} total)"

def validate_paper_data(paper):
    """Validate paper data structure"""
    required_fields = ['title', 'authors', 'abstract']
    
    for field in required_fields:
        if field not in paper or not paper[field]:
            return False
    
    return True

def get_file_timestamp():
    """Get timestamp for file naming"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def ensure_directory(directory):
    """Ensure directory exists"""
    os.makedirs(directory, exist_ok=True)

def truncate_text(text, max_length=300):
    """Truncate text to max length with ellipsis"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + '...'

def extract_keywords(text, num_keywords=10):
    """Extract keywords from text (simple implementation)"""
    if not text:
        return []
    
    # Remove stopwords (simple list)
    stopwords = set([
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'shall', 'should', 'can', 'could', 'may', 'might', 'must'
    ])
    
    # Tokenize and count words
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = {}
    
    for word in words:
        if word not in stopwords and len(word) > 2:
            word_counts[word] = word_counts.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:num_keywords]]

def calculate_reading_time(text, words_per_minute=200):
    """Calculate estimated reading time in minutes"""
    if not text:
        return 0
    
    words = len(re.findall(r'\b\w+\b', text))
    return max(1, round(words / words_per_minute))
