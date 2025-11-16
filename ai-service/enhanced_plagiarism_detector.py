"""
Enhanced plagiarism detector that works like plagiarismchecker.ai
Uses multiple search strategies and better matching algorithms
"""
import re
import time
from plagiarism_detector import PlagiarismDetector

class EnhancedPlagiarismDetector(PlagiarismDetector):
    """Enhanced version with better search and matching"""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        super().__init__(model_name)
        self.search_strategies = [
            'sentence_based',
            'phrase_based',
            'keyword_based'
        ]
    
    def detect_plagiarism(self, text):
        """
        Enhanced plagiarism detection with multiple search strategies
        """
        sentences = self.preprocess_text(text)
        ai_detection = self.detect_ai_generated(text)
        
        if not self.web_searcher or not self.text_matcher:
            print("Web search not available, using basic detection")
            return self._basic_detection(text, sentences, ai_detection)
        
        print("=" * 60)
        print("ENHANCED PLAGIARISM DETECTION")
        print("=" * 60)
        print(f"Text length: {len(text)} characters")
        print(f"Sentences: {len(sentences)}")
        print("=" * 60)
        
        # Strategy 0: Search specifically for Wikipedia pages (highest priority)
        print("\n[Strategy 0] Searching specifically for Wikipedia pages...")
        wikipedia_sources = self._search_wikipedia(text)
        sources = wikipedia_sources
        
        # Strategy 1: Search using key sentences
        print("\n[Strategy 1] Searching with key sentences...")
        sentence_sources = self._search_with_sentences(text, sentences)
        sources.extend(sentence_sources)
        
        # Strategy 2: Search using important phrases
        if len(sources) < 5:
            print("\n[Strategy 2] Searching with important phrases...")
            phrase_sources = self._search_with_phrases(text)
            sources.extend(phrase_sources)
        
        # Strategy 3: Search using keywords
        if len(sources) < 5:
            print("\n[Strategy 3] Searching with keywords...")
            keyword_sources = self._search_with_keywords(text)
            sources.extend(keyword_sources)
        
        # Remove duplicates and prioritize Wikipedia sources
        seen_urls = set()
        unique_sources = []
        wikipedia_sources = []
        other_sources = []
        
        for source in sources:
            url = source.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                # Ensure URL is always included
                if not source.get('url'):
                    source['url'] = url
                # Prioritize Wikipedia sources
                if 'wikipedia.org' in url.lower():
                    wikipedia_sources.append(source)
                else:
                    other_sources.append(source)
        
        # Put Wikipedia sources first
        unique_sources = wikipedia_sources + other_sources
        
        print(f"\nTotal unique sources found: {len(unique_sources)}")
        
        if unique_sources:
            print("\nAnalyzing matches against sources...")
            match_results = self.text_matcher.find_matches(text, unique_sources)
            
            exact_match_pct = match_results['exact_match_percentage']
            partial_match_pct = match_results['partial_match_percentage']
            total_plagiarism = match_results['total_plagiarism']
            unique_content = match_results['unique_content_percentage']
            matches = match_results['matches']
            
            # Format matches with URLs - ensure URLs are always included
            formatted_matches = []
            for i, match in enumerate(matches[:15], 1):  # Top 15 matches
                # Ensure URL is always present - if missing, try to find it from source
                match_url = match.get('url', '')
                if not match_url:
                    # Try to find URL from source title or source info
                    source_name = match.get('source', '')
                    # Look for Wikipedia URL in sources
                    for source in unique_sources:
                        if source.get('title', '') == source_name or source_name in source.get('title', ''):
                            match_url = source.get('url', '')
                            break
                
                formatted_matches.append({
                    'text': match['text'],
                    'similarity': match['similarity'],
                    'match_type': match['match_type'],
                    'source': match.get('source', 'Unknown Source'),
                    'url': match_url,  # Always include URL, even if empty
                    'match_number': i
                })
            
            similarity_score = total_plagiarism
            
            return self._format_results(
                similarity_score, exact_match_pct, partial_match_pct,
                unique_content, formatted_matches, ai_detection, text, sentences
            )
        else:
            print("\nNo sources found, using semantic analysis")
            return self._basic_detection(text, sentences, ai_detection)
    
    def _search_wikipedia(self, text):
        """Search specifically for Wikipedia pages"""
        sources = []
        
        # Extract the main topic/keyword from the text (usually first sentence or key terms)
        sentences = self.preprocess_text(text)
        if sentences:
            first_sentence = sentences[0] if sentences else ""
            
            # Extract potential Wikipedia article title (first few words, capitalized)
            words = first_sentence.split()
            # Look for proper nouns or capitalized words
            potential_titles = []
            for i in range(min(3, len(words))):
                if words[i] and words[i][0].isupper():
                    potential_titles.append(words[i])
            
            # Try searching with "site:wikipedia.org" for better Wikipedia results
            queries = []
            
            # Query 1: First sentence with Wikipedia site search
            if len(first_sentence) > 20:
                queries.append(f'site:wikipedia.org "{first_sentence[:100]}"')
            
            # Query 2: Key terms with Wikipedia
            if potential_titles:
                title_query = ' '.join(potential_titles[:3])
                queries.append(f'site:wikipedia.org {title_query}')
            
            # Query 3: Extract key phrase and search Wikipedia
            if len(words) >= 5:
                key_phrase = ' '.join(words[:5])
                queries.append(f'site:wikipedia.org "{key_phrase}"')
            
            # Also try without site: restriction but with "wikipedia" keyword
            if first_sentence:
                queries.append(f'wikipedia {first_sentence[:80]}')
            
            for query in queries[:3]:  # Limit to 3 queries
                try:
                    print(f"  Searching Wikipedia: '{query[:60]}...'")
                    results = self.web_searcher._search_google(query, max_results=3)
                    # Prioritize Wikipedia URLs
                    for result in results:
                        url = result.get('url', '')
                        if 'wikipedia.org' in url.lower():
                            sources.append(result)
                            print(f"    ✓ Found Wikipedia page: {url[:60]}...")
                    time.sleep(0.8)  # Rate limiting
                except Exception as e:
                    print(f"  Error searching Wikipedia: {str(e)}")
        
        return sources
    
    def _search_with_sentences(self, text, sentences):
        """Search using key sentences"""
        sources = []
        # Use first 3-5 most important sentences
        key_sentences = sentences[:5]
        
        for sentence in key_sentences:
            if len(sentence) > 20:
                try:
                    results = self.web_searcher._search_google(sentence[:200], max_results=2)
                    sources.extend(results)
                    time.sleep(0.5)  # Rate limiting
                except Exception as e:
                    print(f"  Error searching sentence: {str(e)}")
        
        return sources
    
    def _search_with_phrases(self, text):
        """Search using important phrases"""
        sources = []
        words = text.split()
        
        # Extract 4-6 word phrases
        phrases = []
        for length in range(4, 7):
            for i in range(len(words) - length + 1):
                phrase = ' '.join(words[i:i+length])
                if 30 <= len(phrase) <= 150:
                    phrases.append(phrase)
        
        # Use top 5 unique phrases
        unique_phrases = list(set(phrases))[:5]
        
        for phrase in unique_phrases:
            try:
                results = self.web_searcher._search_google(phrase, max_results=1)
                sources.extend(results)
                time.sleep(0.5)
            except Exception as e:
                print(f"  Error searching phrase: {str(e)}")
        
        return sources
    
    def _search_with_keywords(self, text):
        """Search using important keywords"""
        sources = []
        
        # Extract keywords (longer words, excluding common words)
        words = text.lower().split()
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        keywords = [w for w in words if len(w) > 4 and w not in common_words]
        # Get top 5 most frequent keywords
        from collections import Counter
        if keywords:
            keyword_counts = Counter(keywords)
            top_keywords = [word for word, count in keyword_counts.most_common(5)]
        else:
            top_keywords = []
        
        # Search with 2-3 keyword combinations
        if len(top_keywords) < 2:
            return sources
        
        for i in range(len(top_keywords) - 1):
            query = f"{top_keywords[i]} {top_keywords[i+1]}"
            try:
                results = self.web_searcher._search_google(query, max_results=1)
                sources.extend(results)
                time.sleep(0.5)
            except Exception as e:
                print(f"  Error searching keywords: {str(e)}")
        
        return sources
    
    def _basic_detection(self, text, sentences, ai_detection):
        """Basic detection when web search is not available"""
        similarity_score, matches = self._fallback_semantic_check(text, sentences)
        return self._format_results(
            similarity_score, 0, similarity_score,
            100 - similarity_score, matches, ai_detection, text, sentences
        )
    
    def _format_results(self, similarity_score, exact_match_pct, partial_match_pct,
                       unique_content, matches, ai_detection, text, sentences):
        """Format results consistently"""
        analysis = []
        
        if similarity_score >= 80:
            analysis.append({
                'type': 'High Plagiarism Detected',
                'description': 'The text shows high similarity to existing content. Significant portions may need rewriting.',
                'confidence': min(similarity_score, 100),
            })
        elif similarity_score >= 50:
            analysis.append({
                'type': 'Moderate Plagiarism',
                'description': 'Some plagiarism detected. Review and ensure proper citations are included.',
                'confidence': similarity_score,
            })
        elif similarity_score >= 20:
            analysis.append({
                'type': 'Low Plagiarism',
                'description': 'Minor similarities found. Text appears mostly original.',
                'confidence': similarity_score,
            })
        else:
            analysis.append({
                'type': 'Original Content',
                'description': 'Text appears to be original with minimal similarity to known sources.',
                'confidence': 100 - similarity_score,
            })
        
        if ai_detection.get('is_ai_generated'):
            analysis.append({
                'type': 'AI-Generated Content Detected',
                'description': f"The text shows characteristics of AI-generated content (confidence: {ai_detection.get('ai_confidence', 0):.1f}%).",
                'confidence': ai_detection.get('ai_confidence', 0),
            })
        
        if partial_match_pct > 10:
            analysis.append({
                'type': 'Possible Paraphrasing',
                'description': 'The text may contain paraphrased content. Ensure original sources are properly cited.',
                'confidence': partial_match_pct,
            })
        
        return {
            'similarity_score': float(similarity_score),
            'plagiarism_percentage': float(similarity_score),
            'exact_match_percentage': float(exact_match_pct),
            'partial_match_percentage': float(partial_match_pct),
            'unique_content_percentage': float(unique_content),
            'matches': matches,
            'analysis': analysis,
            'ai_detection': {
                'is_ai_generated': bool(ai_detection.get('is_ai_generated', False)),
                'ai_confidence': float(ai_detection.get('ai_confidence', 0)),
                'repetition_score': float(ai_detection.get('repetition_score', 0)),
                'uniformity_score': float(ai_detection.get('uniformity_score', 0)),
            },
            'text_length': int(len(text)),
            'sentence_count': int(len(sentences)),
        }

