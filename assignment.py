import sys
import re
import requests
from bs4 import BeautifulSoup

# Polynomial Rolling Hash (64-bit)
def polynomial_hash(word, p=53):
    m = 2**64
    hash_value = 0
    power = 1
    
    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % m
        power = (power * p) % m
        
    return hash_value % m


# Word Frequency Counter
def get_word_frequencies(text):
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    freq = {}
    
    for word in words:
        freq[word] = freq.get(word, 0) + 1
        
    return freq


# Compute SimHash
def compute_simhash(text):
    freq = get_word_frequencies(text)
    
    vector = [0] * 64
    
    for word, count in freq.items():
        h = polynomial_hash(word)
        
        for i in range(64):
            bitmask = 1 << i
            if h & bitmask:
                vector[i] += count
            else:
                vector[i] -= count
                
    simhash = 0
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)
            
    return simhash


# Fetch Webpage Text
def fetch_text_from_url(url):
    response = requests.get(url)
    sp = BeautifulSoup(response.text, "html.parser")
    if sp.body:
        return sp.body.get_text(separator="\n")
    else:
        return "No body found"


# Compare Two URLs
def compare_urls(url1, url2):
    text1 = fetch_text_from_url(url1)
    text2 = fetch_text_from_url(url2)
    
    simhash1 = compute_simhash(text1)
    simhash2 = compute_simhash(text2)
    
    xor = simhash1 ^ simhash2
    different_bits = bin(xor).count("1")
    common_bits = 64 - different_bits
    
    print("SimHash 1:", simhash1)
    print("SimHash 2:", simhash2)
    print("Common bits:", common_bits)


# Command Line Execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python simhash.py <url1> <url2>")
        sys.exit(1)
        
    url1 = sys.argv[1]
    url2 = sys.argv[2]
    
    compare_urls(url1, url2)