"""
Web search module for finding similar content online
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import time

class WebSearcher:
    """Search for similar content on the web"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_queries(self, text, max_results=5):
        """
        Extract search queries from text and search for similar content
        
        Args:
            text: Input text to check
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with URLs and snippets
        """
        # Extract key phrases from text (sentences and important phrases)
        sentences = re.split(r'[.!?]+', text)
        queries = []
        
        # Use first few sentences and key phrases as search queries
        for sentence in sentences[:5]:  # Use first 5 sentences
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                queries.append(sentence)
        
        # Also extract key phrases (3-5 word combinations)
        words = text.split()
        for i in range(len(words) - 3):
            phrase = ' '.join(words[i:i+4])
            if len(phrase) > 15 and len(phrase) < 100:
                queries.append(phrase)
        
        # Remove duplicates and limit
        queries = list(set(queries))[:10]
        
        results = []
        print(f"Processing {len(queries)} search queries...")
        for i, query in enumerate(queries, 1):
            try:
                print(f"  [{i}/{len(queries)}] Searching: '{query[:50]}...'")
                search_results = self._search_google(query, max_results=2)
                if search_results:
                    print(f"    Found {len(search_results)} results")
                    results.extend(search_results)
                else:
                    print(f"    No results found")
                time.sleep(1)  # Rate limiting - increased to avoid blocking
            except Exception as e:
                print(f"    Search error: {str(e)}")
                continue
        
        # Remove duplicates by URL and ensure all have valid URLs
        seen_urls = set()
        valid_results = []
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                # Ensure URL is valid
                if url.startswith('http://') or url.startswith('https://'):
                    valid_results.append(result)
        
        print(f"Returning {len(valid_results)} unique results with URLs")
        return valid_results[:max_results]
    
    def _search_google(self, query, max_results=3):
        """
        Search Google for the query (using googlesearch library or direct search)
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            List of search results
        """
        try:
            from googlesearch import search
            results = []
            print(f"      Executing Google search...")
            search_iter = search(query, num_results=max_results, lang='en', sleep_interval=1)
            
            for url in search_iter:
                try:
                    print(f"      Fetching content from: {url[:60]}...")
                    # Try to get page content
                    content = self._fetch_page_content(url)
                    if content and len(content) > 100:
                        results.append({
                            'url': url,
                            'title': self._extract_title(url, content),
                            'snippet': content[:500] if content else query,
                            'content': content
                        })
                        print(f"        ✓ Content fetched ({len(content)} chars)")
                    else:
                        # If we can't fetch content, still include the URL
                        # Use query as content for basic matching
                        results.append({
                            'url': url,
                            'title': self._extract_title_from_url(url),
                            'snippet': query,
                            'content': query.lower()  # Use query as content for matching
                        })
                        print(f"        ⚠ Using URL only (content fetch failed)")
                except Exception as e:
                    # Always include URL even if content fetch fails
                    print(f"        ⚠ Error fetching content: {str(e)}")
                    results.append({
                        'url': url,
                        'title': self._extract_title_from_url(url),
                        'snippet': query,
                        'content': query.lower()  # Use query as content for basic matching
                    })
                if len(results) >= max_results:
                    break
            return results
        except ImportError:
            print(f"      ERROR: googlesearch library not installed!")
            print(f"      Install with: pip install googlesearch-python")
            # Fallback: return empty results to trigger fallback
            return []
        except Exception as e:
            print(f"      Google search error: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def _fetch_page_content(self, url, timeout=10):
        """Fetch content from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Special handling for Wikipedia pages
                if 'wikipedia.org' in url.lower():
                    # Wikipedia has main content in specific divs
                    content_div = soup.find('div', {'id': 'mw-content-text'}) or soup.find('div', {'class': 'mw-parser-output'})
                    if content_div:
                        # Remove unwanted elements
                        for element in content_div.find_all(['script', 'style', 'nav', 'footer', 'header', 'table', 'div', 'span'], 
                                                          class_=lambda x: x and ('navbox' in x.lower() or 'infobox' in x.lower() or 'reference' in x.lower())):
                            element.decompose()
                        # Get text from Wikipedia content area
                        text = content_div.get_text(separator=' ', strip=True)
                        # Clean up whitespace
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        if len(text) > 100:
                            return text[:10000]  # Wikipedia articles can be long, allow more content
                
                # For other sites, use general extraction
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                # Get text content
                text = soup.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                # Return meaningful content (at least 100 chars)
                if len(text) > 100:
                    return text[:5000]  # Limit to 5000 characters for non-Wikipedia
        except requests.exceptions.Timeout:
            print(f"        Timeout fetching {url}")
        except Exception as e:
            print(f"        Error fetching {url}: {str(e)}")
        return None
    
    def _extract_title(self, url, content):
        """Extract title from page content or URL"""
        if content:
            try:
                soup = BeautifulSoup(content, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    return title_tag.get_text().strip()
            except:
                pass
        return self._extract_title_from_url(url)
    
    def _extract_title_from_url(self, url):
        """Extract a title from URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        path = parsed.path.strip('/').replace('/', ' - ')
        if path:
            return f"{domain} - {path[:50]}"
        return domain

