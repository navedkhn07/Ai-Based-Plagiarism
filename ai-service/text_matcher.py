"""
Text matching module for finding exact and partial matches
"""
import re
from difflib import SequenceMatcher
from collections import defaultdict

class TextMatcher:
    """Match text against sources to find exact and partial matches"""
    
    def __init__(self):
        self.exact_threshold = 0.95  # 95% similarity = exact match
        self.partial_threshold = 0.70  # 70% similarity = partial match
    
    def find_matches(self, text, sources):
        """
        Find exact and partial matches in text against sources
        
        Args:
            text: Input text to check
            sources: List of source dictionaries with 'content' and 'url'
            
        Returns:
            Dictionary with matches, exact_match_percentage, partial_match_percentage
        """
        if not sources:
            return {
                'matches': [],
                'exact_match_percentage': 0,
                'partial_match_percentage': 0,
                'total_plagiarism': 0,
                'unique_content_percentage': 100
            }
        
        # Split text into sentences and phrases
        sentences = self._split_into_sentences(text)
        phrases = self._extract_phrases(text)
        
        matches = []
        exact_match_chars = 0
        partial_match_chars = 0
        total_chars = len(text)
        
        print(f"Matching {len(sentences)} sentences and {len(phrases)} phrases against {len(sources)} sources")
        
        # Check each sentence/phrase against sources
        for source_idx, source in enumerate(sources, 1):
            source_content = source.get('content', '')
            source_url = source.get('url', '')
            source_title = source.get('title', 'Unknown')
            
            if not source_content:
                print(f"  Source {source_idx}: No content available, skipping")
                continue
            
            if not source_url:
                print(f"  Source {source_idx}: No URL available")
            
            source_content_lower = source_content.lower()
            print(f"  Source {source_idx}: {source_title[:50]}... ({len(source_content)} chars)")
            
            # Check sentences
            for sentence in sentences:
                if len(sentence) < 10:
                    continue
                
                similarity, match_type = self._check_similarity(sentence, source_content_lower)
                
                if match_type == 'exact':
                    exact_match_chars += len(sentence)
                    matches.append({
                        'text': sentence,
                        'similarity': similarity * 100,
                        'match_type': 'exact',
                        'source': source_title,
                        'url': source_url,
                        'position': text.find(sentence)
                    })
                elif match_type == 'partial':
                    partial_match_chars += len(sentence) * similarity
                    matches.append({
                        'text': sentence,
                        'similarity': similarity * 100,
                        'match_type': 'partial',
                        'source': source_title,
                        'url': source_url,
                        'position': text.find(sentence)
                    })
            
            # Check phrases (for more granular matching)
            for phrase in phrases:
                if len(phrase) < 15:
                    continue
                
                similarity, match_type = self._check_similarity(phrase, source_content_lower)
                
                if match_type in ['exact', 'partial']:
                    # Check if this phrase is already covered by a sentence match
                    is_covered = any(
                        phrase.lower() in match['text'].lower() 
                        for match in matches 
                        if match.get('position', -1) >= 0
                    )
                    
                    if not is_covered:
                        if match_type == 'exact':
                            exact_match_chars += len(phrase)
                        else:
                            partial_match_chars += len(phrase) * similarity
                        
                        matches.append({
                            'text': phrase,
                            'similarity': similarity * 100,
                            'match_type': match_type,
                            'source': source_title,
                            'url': source_url,
                            'position': text.find(phrase)
                        })
        
        # Remove overlapping matches (keep the one with higher similarity)
        matches = self._remove_overlaps(matches)
        
        # Calculate percentages based on actual matched characters
        # Only count each character once (avoid double counting)
        matched_positions = set()
        exact_positions = set()
        partial_positions = set()
        
        for match in matches:
            pos = match.get('position', -1)
            if pos >= 0:
                match_length = len(match['text'])
                for i in range(pos, min(pos + match_length, len(text))):
                    matched_positions.add(i)
                    if match['match_type'] == 'exact':
                        exact_positions.add(i)
                    else:
                        partial_positions.add(i)
        
        # Calculate percentages based on unique positions
        exact_match_percentage = (len(exact_positions) / total_chars * 100) if total_chars > 0 else 0
        # Partial matches that don't overlap with exact matches
        partial_only_positions = partial_positions - exact_positions
        partial_match_percentage = (len(partial_only_positions) / total_chars * 100) if total_chars > 0 else 0
        total_plagiarism = exact_match_percentage + partial_match_percentage
        
        # Ensure percentages are reasonable
        exact_match_percentage = min(exact_match_percentage, 100)
        partial_match_percentage = min(partial_match_percentage, 100)
        total_plagiarism = min(total_plagiarism, 100)
        
        return {
            'matches': matches,
            'exact_match_percentage': min(exact_match_percentage, 100),
            'partial_match_percentage': min(partial_match_percentage, 100),
            'total_plagiarism': min(total_plagiarism, 100),
            'unique_content_percentage': max(0, 100 - total_plagiarism)
        }
    
    def _split_into_sentences(self, text):
        """Split text into sentences"""
        # Split by sentence endings
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _extract_phrases(self, text, min_length=15, max_length=100):
        """Extract phrases of various lengths"""
        words = text.split()
        phrases = []
        
        # Extract 3-7 word phrases
        for length in range(3, min(8, len(words))):
            for i in range(len(words) - length + 1):
                phrase = ' '.join(words[i:i+length])
                if min_length <= len(phrase) <= max_length:
                    phrases.append(phrase)
        
        # Remove duplicates
        return list(set(phrases))
    
    def _check_similarity(self, text, source_content):
        """
        Check similarity between text and source content
        
        Returns:
            (similarity_score, match_type)
            match_type: 'exact', 'partial', or None
        """
        text_lower = text.lower().strip()
        source_lower = source_content.lower()
        
        # Check for exact substring match first (most common case)
        # This is the most reliable for Wikipedia content
        if text_lower in source_lower:
            return 1.0, 'exact'
        
        # Also check with normalized whitespace (Wikipedia might have different spacing)
        text_normalized = ' '.join(text_lower.split())
        source_normalized = ' '.join(source_lower.split())
        if text_normalized in source_normalized:
            return 1.0, 'exact'
        
        # Check for near-exact match (allowing minor differences)
        # Remove punctuation and extra spaces for comparison
        import string
        text_clean = ''.join(c for c in text_lower if c not in string.punctuation)
        source_clean = ''.join(c for c in source_lower if c not in string.punctuation)
        
        if text_clean in source_clean:
            return 0.98, 'exact'
        
        # Check for similar phrases using SequenceMatcher
        best_similarity = 0
        best_match = None
        
        # Try matching against sentences in source
        source_sentences = re.split(r'[.!?]+\s+', source_lower)
        for source_sentence in source_sentences:
            if len(source_sentence) < 10:
                continue
            
            similarity = SequenceMatcher(None, text_lower, source_sentence).ratio()
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = source_sentence
        
        # Also check word-by-word matching for partial matches
        text_words = set(text_lower.split())
        source_words = set(source_lower.split())
        
        if len(text_words) > 0:
            common_words = text_words.intersection(source_words)
            word_overlap = len(common_words) / len(text_words)
            
            # If significant word overlap, it's likely a match
            if word_overlap >= 0.6:  # 60% of words match
                # Use the higher similarity score
                best_similarity = max(best_similarity, word_overlap * 0.9)
        
        # Check for partial matches (substrings of 4+ words)
        words = text_lower.split()
        if len(words) >= 4:
            # Try matching 4-word combinations
            for i in range(len(words) - 3):
                phrase = ' '.join(words[i:i+4])
                if phrase in source_lower:
                    return 0.90, 'partial'
        
        # Determine match type based on similarity
        if best_similarity >= self.exact_threshold:
            return best_similarity, 'exact'
        elif best_similarity >= self.partial_threshold:
            return best_similarity, 'partial'
        else:
            return best_similarity, None
    
    def _remove_overlaps(self, matches):
        """Remove overlapping matches, keeping the one with higher similarity"""
        if not matches:
            return []
        
        # Sort by position
        matches.sort(key=lambda x: x.get('position', 0))
        
        filtered = []
        for match in matches:
            is_overlapping = False
            match_start = match.get('position', 0)
            match_end = match_start + len(match['text'])
            
            for existing in filtered:
                existing_start = existing.get('position', 0)
                existing_end = existing_start + len(existing['text'])
                
                # Check if overlaps
                if not (match_end <= existing_start or match_start >= existing_end):
                    is_overlapping = True
                    # Keep the one with higher similarity
                    if match['similarity'] > existing['similarity']:
                        filtered.remove(existing)
                        filtered.append(match)
                    break
            
            if not is_overlapping:
                filtered.append(match)
        
        return filtered

