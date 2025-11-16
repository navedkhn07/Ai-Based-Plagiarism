"""
Test script to verify web search is working
"""
import sys
import time

print("Testing web search functionality...")
print("=" * 50)

# Test 1: Check if googlesearch is installed
print("\n1. Checking googlesearch library...")
try:
    from googlesearch import search
    print("   ✓ googlesearch library is installed")
except ImportError:
    print("   ✗ googlesearch library NOT installed")
    print("   Install with: pip install googlesearch-python")
    sys.exit(1)

# Test 2: Test web search module
print("\n2. Testing web search module...")
try:
    from web_search import WebSearcher
    searcher = WebSearcher()
    print("   ✓ WebSearcher class loaded")
except Exception as e:
    print(f"   ✗ Error loading WebSearcher: {e}")
    sys.exit(1)

# Test 3: Test actual search
print("\n3. Testing actual Google search...")
print("   This may take 10-20 seconds...")
test_query = "pathophysiology of hypertension"
start_time = time.time()

try:
    results = searcher._search_google(test_query, max_results=2)
    elapsed = time.time() - start_time
    print(f"   ✓ Search completed in {elapsed:.2f} seconds")
    print(f"   ✓ Found {len(results)} results")
    
    if results:
        for i, result in enumerate(results, 1):
            print(f"\n   Result {i}:")
            print(f"     URL: {result['url']}")
            print(f"     Title: {result['title']}")
            print(f"     Content length: {len(result.get('content', ''))} chars")
    else:
        print("   ⚠ No results found (this might be due to rate limiting)")
        
except Exception as e:
    print(f"   ✗ Search failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test completed!")
print("\nIf search is working, you should see results above.")
print("If not, check:")
print("  1. Internet connection")
print("  2. Google rate limiting (wait a few minutes)")
print("  3. Firewall/proxy settings")

