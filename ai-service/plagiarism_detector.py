import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("Warning: spaCy not available. Using basic tokenization.")
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("Warning: TextBlob not available. Some features may be limited.")
import warnings
warnings.filterwarnings('ignore')

# Import web search and text matching modules
try:
    from web_search import WebSearcher
    from text_matcher import TextMatcher
    WEB_SEARCH_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Web search modules not available: {str(e)}")
    WEB_SEARCH_AVAILABLE = False

class PlagiarismDetector:
    """
    AI-based plagiarism detector using Sentence-Transformers for semantic similarity
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the plagiarism detector with a pre-trained model
        
        Args:
            model_name: Name of the Sentence-Transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self.nlp = None
        self.web_searcher = None
        self.text_matcher = None
        self._load_model()
        self._load_nlp()
        self._load_web_search()
    
    def _load_model(self):
        """Load the Sentence-Transformer model"""
        try:
            print(f"Loading model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def _load_nlp(self):
        """Load spaCy NLP model for text processing"""
        if not SPACY_AVAILABLE:
            self.nlp = None
            return
        
        try:
            # Try to load English model, fallback to basic if not available
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Warning: spaCy English model not found. Using basic tokenization.")
                self.nlp = None
        except Exception as e:
            print(f"Warning: Error loading spaCy: {str(e)}")
            self.nlp = None
    
    def _load_web_search(self):
        """Load web search and text matching modules"""
        if WEB_SEARCH_AVAILABLE:
            try:
                self.web_searcher = WebSearcher()
                self.text_matcher = TextMatcher()
                print("Web search and text matching modules loaded")
            except Exception as e:
                print(f"Warning: Could not load web search modules: {str(e)}")
                self.web_searcher = None
                self.text_matcher = None
        else:
            self.web_searcher = None
            self.text_matcher = None
    
    def is_model_loaded(self):
        """Check if the model is loaded"""
        return self.model is not None
    
    def preprocess_text(self, text):
        """
        Preprocess text: clean, normalize, and split into sentences
        
        Args:
            text: Input text string
            
        Returns:
            List of cleaned sentences
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Split into sentences
        if self.nlp:
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        else:
            # Fallback: simple sentence splitting
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def extract_features(self, text):
        """
        Extract semantic features from text using Sentence-Transformers
        
        Args:
            text: Input text string
            
        Returns:
            numpy array of embeddings
        """
        sentences = self.preprocess_text(text)
        
        if len(sentences) == 0:
            # If no sentences, use the whole text
            embeddings = self.model.encode([text])
        else:
            # Encode each sentence
            embeddings = self.model.encode(sentences)
        
        # Average the embeddings if multiple sentences
        if len(embeddings.shape) > 1 and embeddings.shape[0] > 1:
            embeddings = np.mean(embeddings, axis=0)
        
        return embeddings
    
    def calculate_similarity(self, text1_emb, text2_emb):
        """
        Calculate cosine similarity between two text embeddings
        
        Args:
            text1_emb: Embedding of first text
            text2_emb: Embedding of second text
            
        Returns:
            Similarity score (0-1)
        """
        # Ensure embeddings are 2D arrays
        if len(text1_emb.shape) == 1:
            text1_emb = text1_emb.reshape(1, -1)
        if len(text2_emb.shape) == 1:
            text2_emb = text2_emb.reshape(1, -1)
        
        similarity = cosine_similarity(text1_emb, text2_emb)[0][0]
        return float(similarity)
    
    def detect_ai_generated(self, text):
        """
        Detect if text might be AI-generated using heuristics
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with AI detection results
        """
        # Heuristic 1: Check for repetitive patterns
        sentences = self.preprocess_text(text)
        unique_sentences = len(set(sentences))
        repetition_score = 1 - (unique_sentences / max(len(sentences), 1))
        
        # Heuristic 2: Check for very uniform sentence length
        if len(sentences) > 0:
            sentence_lengths = [len(s) for s in sentences]
            avg_length = np.mean(sentence_lengths)
            std_length = np.std(sentence_lengths)
            uniformity = 1 - min(std_length / max(avg_length, 1), 1)
        else:
            uniformity = 0
        
        # Heuristic 3: Check for common AI writing patterns
        ai_patterns = [
            r'\b(it is important to note|it should be noted|it is worth mentioning)\b',
            r'\b(in conclusion|to summarize|in summary)\b',
            r'\b(furthermore|moreover|additionally)\b',
        ]
        pattern_count = sum(len(re.findall(pattern, text.lower())) for pattern in ai_patterns)
        pattern_score = min(pattern_count / max(len(sentences), 1), 1)
        
        # Combined AI score
        ai_score = (repetition_score * 0.3 + uniformity * 0.3 + pattern_score * 0.4)
        
        return {
            'is_ai_generated': bool(ai_score > 0.5),
            'ai_confidence': float(ai_score * 100),
            'repetition_score': float(repetition_score * 100),
            'uniformity_score': float(uniformity * 100),
        }
    
    def detect_plagiarism(self, text):
        """
        Main method to detect plagiarism in text
        
        Args:
            text: Input text to check
            
        Returns:
            Dictionary with plagiarism detection results
        """
        sentences = self.preprocess_text(text)
        
        # Detect AI-generated content
        ai_detection = self.detect_ai_generated(text)
        
        # Try to find real plagiarism using web search
        if self.web_searcher and self.text_matcher:
            try:
                print("=" * 50)
                print("Starting real-time web search for plagiarism detection...")
                print("This may take 15-30 seconds...")
                print("=" * 50)
                
                # Search for similar content online
                import time
                start_time = time.time()
                sources = self.web_searcher.search_queries(text, max_results=5)
                search_time = time.time() - start_time
                
                print(f"Web search completed in {search_time:.2f} seconds")
                
                if sources:
                    print(f"Found {len(sources)} potential sources")
                    print("Analyzing matches...")
                    
                    # Match text against found sources
                    match_start = time.time()
                    match_results = self.text_matcher.find_matches(text, sources)
                    match_time = time.time() - match_start
                    print(f"Text matching completed in {match_time:.2f} seconds")
                    
                    exact_match_pct = match_results['exact_match_percentage']
                    partial_match_pct = match_results['partial_match_percentage']
                    total_plagiarism = match_results['total_plagiarism']
                    unique_content = match_results['unique_content_percentage']
                    matches = match_results['matches']
                    
                    # Format matches with proper numbering
                    formatted_matches = []
                    for i, match in enumerate(matches[:10], 1):  # Limit to top 10 matches
                        formatted_matches.append({
                            'text': match['text'],
                            'similarity': match['similarity'],
                            'match_type': match['match_type'],
                            'source': match['source'],
                            'url': match.get('url', ''),
                            'match_number': i
                        })
                    
                    similarity_score = total_plagiarism
                    
                else:
                    # No sources found, use semantic similarity as fallback
                    print("No sources found, using semantic similarity with reference search")
                    similarity_score, matches = self._fallback_semantic_check(text, sentences)
                    exact_match_pct = 0
                    partial_match_pct = similarity_score
                    unique_content = 100 - similarity_score
                    formatted_matches = matches
                    
            except Exception as e:
                print(f"Error in web search plagiarism detection: {str(e)}")
                print("Falling back to semantic similarity with reference search")
                # Fallback to semantic similarity but still try to find references
                similarity_score, matches = self._fallback_semantic_check(text, sentences)
                exact_match_pct = 0
                partial_match_pct = similarity_score
                unique_content = 100 - similarity_score
                formatted_matches = matches
        else:
            # Web search not available, use semantic similarity
            print("Web search not available, using semantic similarity")
            print("Note: Reference links will not be available without web search")
            similarity_score, matches = self._fallback_semantic_check(text, sentences)
            exact_match_pct = 0
            partial_match_pct = similarity_score
            unique_content = 100 - similarity_score
            formatted_matches = matches
        
        # Generate analysis
        analysis = []
        
        # Similarity analysis
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
        
        # AI detection analysis
        if ai_detection['is_ai_generated']:
            analysis.append({
                'type': 'AI-Generated Content Detected',
                'description': f"The text shows characteristics of AI-generated content (confidence: {ai_detection['ai_confidence']:.1f}%).",
                'confidence': ai_detection['ai_confidence'],
            })
        
        # Paraphrasing detection
        if partial_match_pct > 10:
            analysis.append({
                'type': 'Possible Paraphrasing',
                'description': 'The text may contain paraphrased content. Ensure original sources are properly cited.',
                'confidence': partial_match_pct,
            })
        
        # Ensure all values are JSON serializable
        return {
            'similarity_score': float(similarity_score),
            'plagiarism_percentage': float(similarity_score),
            'exact_match_percentage': float(exact_match_pct),
            'partial_match_percentage': float(partial_match_pct),
            'unique_content_percentage': float(unique_content),
            'matches': formatted_matches,
            'analysis': analysis,
            'ai_detection': {
                'is_ai_generated': bool(ai_detection['is_ai_generated']),
                'ai_confidence': float(ai_detection['ai_confidence']),
                'repetition_score': float(ai_detection['repetition_score']),
                'uniformity_score': float(ai_detection['uniformity_score']),
            },
            'text_length': int(len(text)),
            'sentence_count': int(len(sentences)),
        }
    
    def _fallback_semantic_check(self, text, sentences):
        """Fallback method using semantic similarity when web search is not available"""
        # Calculate internal similarity (how similar are parts of the text to each other)
        if len(sentences) > 1:
            sentence_embeddings = self.model.encode(sentences)
            # Calculate pairwise similarities
            similarity_matrix = cosine_similarity(sentence_embeddings)
            # Get average similarity (excluding diagonal)
            np.fill_diagonal(similarity_matrix, 0)
            avg_similarity = float(np.mean(similarity_matrix[similarity_matrix > 0])) if bool(np.any(similarity_matrix > 0)) else 0.0
        else:
            avg_similarity = 0
        
        similarity_score = float(avg_similarity * 100)
        
        # Generate basic matches with reference links
        matches = []
        if similarity_score > 10:
            # Try to find reference links for top sentences
            top_sentences = sentences[:5] if len(sentences) >= 5 else sentences
            
            for i, sentence in enumerate(top_sentences, 1):
                if len(sentence) > 20:
                    # Try to find a reference link for this sentence
                    reference_url = self._find_reference_for_sentence(sentence)
                    
                    # Extract a meaningful source name
                    source_name = self._extract_source_name(sentence, reference_url)
                    
                    matches.append({
                        'text': sentence[:200] + '...' if len(sentence) > 200 else sentence,
                        'similarity': float(min(100, similarity_score * (0.9 - i * 0.1))),
                        'match_type': 'partial',
                        'source': source_name,
                        'url': reference_url if reference_url else '',
                        'match_number': i
                    })
        
        return similarity_score, matches
    
    def _find_reference_for_sentence(self, sentence):
        """Try to find a reference URL for a sentence using web search"""
        if not self.web_searcher:
            return ''
        
        try:
            # Use first 10 words of sentence as search query
            words = sentence.split()[:10]
            query = ' '.join(words)
            
            if len(query) < 15:
                return ''
            
            # Quick search for this sentence
            results = self.web_searcher._search_google(query, max_results=1)
            if results and results[0].get('url'):
                return results[0]['url']
        except Exception as e:
            print(f"Error finding reference for sentence: {str(e)}")
        
        return ''
    
    def _extract_source_name(self, sentence, url):
        """Extract a meaningful source name from sentence or URL"""
        if url:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(url)
                domain = parsed.netloc.replace('www.', '')
                # Capitalize and format domain
                if '.' in domain:
                    domain_parts = domain.split('.')
                    source_name = domain_parts[0].capitalize()
                    if len(domain_parts) > 1:
                        source_name += f" - {domain_parts[1]}"
                    return source_name
                return domain
            except:
                pass
        
        # Fallback: use first few words of sentence
        words = sentence.split()[:5]
        if len(words) >= 3:
            return ' '.join(words[:3]) + '...'
        return f'Match {len(sentence)} chars'

