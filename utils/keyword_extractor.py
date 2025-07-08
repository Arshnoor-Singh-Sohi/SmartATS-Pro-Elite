import re
import nltk
from collections import Counter
from typing import List, Dict, Tuple
import string

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class KeywordExtractor:
    """
    Extracts and analyzes keywords from resume and job descriptions
    """
    
    def __init__(self):
        # Get English stopwords
        self.stop_words = set(stopwords.words('english'))
        
        # Add custom stopwords common in resumes and job descriptions
        self.custom_stopwords = {
            'experience', 'work', 'working', 'worked', 'responsibilities',
            'responsible', 'duties', 'duty', 'including', 'include',
            'requires', 'required', 'requirements', 'skills', 'skill',
            'ability', 'able', 'years', 'year', 'etc', 'company',
            'position', 'role', 'job', 'candidate', 'candidates',
            'team', 'teams', 'will', 'must', 'should', 'new'
        }
        
        self.stop_words.update(self.custom_stopwords)
        
        # Technical terms that should be preserved
        self.technical_terms = {
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'nodejs', 'django', 'flask', 'spring', 'aws', 'azure',
            'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'agile',
            'scrum', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'machine learning', 'deep learning', 'ai', 'ml', 'nlp',
            'data science', 'data analysis', 'data engineering',
            'ci/cd', 'devops', 'api', 'rest', 'graphql', 'microservices'
        }
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """
        Extract top keywords from text
        
        Args:
            text: Input text
            top_n: Number of top keywords to return
            
        Returns:
            List of keywords
        """
        # Convert to lowercase
        text_lower = text.lower()
        
        # Extract technical bigrams and trigrams first
        technical_phrases = self._extract_technical_phrases(text_lower)
        
        # Tokenize
        tokens = word_tokenize(text_lower)
        
        # Remove punctuation and stopwords
        keywords = [
            token for token in tokens
            if token not in self.stop_words
            and token not in string.punctuation
            and len(token) > 2
            and not token.isdigit()
        ]
        
        # Count frequencies
        keyword_freq = Counter(keywords)
        
        # Add technical phrases with higher weight
        for phrase in technical_phrases:
            keyword_freq[phrase] = keyword_freq.get(phrase, 0) + 3
        
        # Get top keywords
        top_keywords = [word for word, _ in keyword_freq.most_common(top_n)]
        
        return top_keywords
    
    def _extract_technical_phrases(self, text: str) -> List[str]:
        """
        Extract technical multi-word phrases
        
        Args:
            text: Input text in lowercase
            
        Returns:
            List of technical phrases found
        """
        found_phrases = []
        
        # Check for known technical terms
        for term in self.technical_terms:
            if term in text:
                found_phrases.append(term)
        
        # Extract common patterns
        patterns = [
            r'\b(?:machine|deep)\s+learning\b',
            r'\b(?:data)\s+(?:science|analysis|engineering|analytics)\b',
            r'\b(?:software|web|mobile|full[\s-]?stack)\s+(?:development|developer|engineering|engineer)\b',
            r'\b(?:project|product|program)\s+(?:management|manager)\b',
            r'\b(?:business)\s+(?:analysis|analyst|intelligence)\b',
            r'\b[a-z]+\s+(?:framework|library|platform|language)\b',
            r'\b(?:version)\s+(?:control|management)\b',
            r'\b(?:continuous)\s+(?:integration|deployment|delivery)\b'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            found_phrases.extend(matches)
        
        return list(set(found_phrases))
    
    def compare_keywords(self, resume_keywords: List[str], 
                        job_keywords: List[str]) -> Dict[str, List[str]]:
        """
        Compare keywords between resume and job description
        
        Args:
            resume_keywords: Keywords from resume
            job_keywords: Keywords from job description
            
        Returns:
            Dictionary with matched and missing keywords
        """
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        
        matched = list(resume_set & job_set)
        missing = list(job_set - resume_set)
        additional = list(resume_set - job_set)
        
        return {
            'matched': matched,
            'missing': missing,
            'additional': additional
        }
    
    def calculate_keyword_score(self, resume_text: str, job_text: str) -> Tuple[float, Dict]:
        """
        Calculate keyword matching score
        
        Args:
            resume_text: Resume content
            job_text: Job description content
            
        Returns:
            Tuple of (score, details)
        """
        # Extract keywords from both texts
        resume_keywords = self.extract_keywords(resume_text, top_n=50)
        job_keywords = self.extract_keywords(job_text, top_n=30)
        
        # Compare keywords
        comparison = self.compare_keywords(resume_keywords, job_keywords)
        
        # Calculate score
        if job_keywords:
            score = len(comparison['matched']) / len(job_keywords) * 100
        else:
            score = 0
        
        # Prepare details
        details = {
            'score': round(score, 1),
            'matched_count': len(comparison['matched']),
            'missing_count': len(comparison['missing']),
            'job_keyword_count': len(job_keywords),
            'resume_keyword_count': len(resume_keywords),
            'comparison': comparison
        }
        
        return score, details
    
    def suggest_keyword_improvements(self, missing_keywords: List[str], 
                                   resume_text: str) -> List[Dict[str, str]]:
        """
        Suggest how to incorporate missing keywords
        
        Args:
            missing_keywords: List of missing keywords
            resume_text: Current resume text
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Categorize keywords
        technical_skills = []
        soft_skills = []
        other_keywords = []
        
        # Common soft skills
        soft_skill_terms = {
            'leadership', 'communication', 'teamwork', 'collaboration',
            'problem-solving', 'analytical', 'creative', 'innovative',
            'organized', 'detail-oriented', 'strategic', 'critical thinking'
        }
        
        for keyword in missing_keywords[:15]:  # Limit to top 15
            if keyword in self.technical_terms or self._is_technical_term(keyword):
                technical_skills.append(keyword)
            elif keyword in soft_skill_terms:
                soft_skills.append(keyword)
            else:
                other_keywords.append(keyword)
        
        # Generate suggestions
        if technical_skills:
            suggestions.append({
                'category': 'Technical Skills',
                'keywords': technical_skills,
                'suggestion': f"Add these technical skills to your skills section: {', '.join(technical_skills)}. If you have experience with these technologies, include specific projects or achievements that demonstrate your proficiency."
            })
        
        if soft_skills:
            suggestions.append({
                'category': 'Soft Skills',
                'keywords': soft_skills,
                'suggestion': f"Incorporate these soft skills throughout your experience descriptions: {', '.join(soft_skills)}. Use action verbs and specific examples that demonstrate these qualities."
            })
        
        if other_keywords:
            suggestions.append({
                'category': 'Other Important Terms',
                'keywords': other_keywords,
                'suggestion': f"Consider including these terms where relevant: {', '.join(other_keywords)}. Ensure they fit naturally within your experience and qualifications."
            })
        
        return suggestions
    
    def _is_technical_term(self, term: str) -> bool:
        """
        Check if a term is likely technical
        
        Args:
            term: The term to check
            
        Returns:
            True if likely technical, False otherwise
        """
        # Common patterns for technical terms
        technical_patterns = [
            r'^[A-Z]+$',  # Acronyms like API, SQL, AWS
            r'^[a-z]+\.js$',  # JavaScript libraries
            r'^[a-z]+\+\+$',  # C++, etc.
            r'^\d+[a-z]+$',  # es6, etc.
            r'^[a-z]+\d+$',  # python3, etc.
        ]
        
        for pattern in technical_patterns:
            if re.match(pattern, term):
                return True
        
        # Check for common technical suffixes
        tech_suffixes = ['js', 'py', 'db', 'sql', 'api', 'sdk', 'ide']
        for suffix in tech_suffixes:
            if term.endswith(suffix):
                return True
        
        return False
    
    def extract_skills_taxonomy(self, text: str) -> Dict[str, List[str]]:
        """
        Extract and categorize skills from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of categorized skills
        """
        text_lower = text.lower()
        
        skills_taxonomy = {
            'programming_languages': [],
            'frameworks_libraries': [],
            'databases': [],
            'cloud_platforms': [],
            'tools_technologies': [],
            'methodologies': [],
            'soft_skills': []
        }
        
        # Define patterns for each category
        patterns = {
            'programming_languages': [
                r'\b(?:python|java|javascript|typescript|c\+\+|c#|ruby|go|rust|swift|kotlin|php|r|scala|perl)\b'
            ],
            'frameworks_libraries': [
                r'\b(?:react|angular|vue|django|flask|spring|express|rails|laravel|\.net|tensorflow|pytorch|keras)\b'
            ],
            'databases': [
                r'\b(?:mysql|postgresql|mongodb|redis|elasticsearch|cassandra|oracle|sql server|dynamodb|sqlite)\b'
            ],
            'cloud_platforms': [
                r'\b(?:aws|amazon web services|azure|google cloud|gcp|heroku|digitalocean)\b'
            ],
            'tools_technologies': [
                r'\b(?:docker|kubernetes|jenkins|git|github|gitlab|jira|confluence|terraform|ansible|nginx|apache)\b'
            ],
            'methodologies': [
                r'\b(?:agile|scrum|kanban|waterfall|devops|ci/cd|tdd|bdd|microservices|rest|graphql|mvc|mvvm)\b'
            ]
        }
        
        # Extract skills for each category
        for category, category_patterns in patterns.items():
            for pattern in category_patterns:
                matches = re.findall(pattern, text_lower)
                skills_taxonomy[category].extend(matches)
        
        # Remove duplicates
        for category in skills_taxonomy:
            skills_taxonomy[category] = list(set(skills_taxonomy[category]))
        
        return skills_taxonomy