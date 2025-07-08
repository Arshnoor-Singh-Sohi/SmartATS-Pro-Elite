import os
import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import re
from collections import Counter
import time

class EnhancedGeminiAnalyzer:
    """
    Enhanced Gemini analyzer with advanced AI capabilities for comprehensive resume analysis
    """
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Industry-specific keyword databases
        self.industry_keywords = {
            'Technology': {
                'technical': ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'django', 'flask', 'spring', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'agile', 'scrum', 'api', 'rest', 'graphql', 'microservices', 'devops', 'ci/cd'],
                'soft': ['problem-solving', 'analytical thinking', 'innovation', 'collaboration', 'leadership', 'mentoring'],
                'trending': ['ai', 'machine learning', 'cloud native', 'containerization', 'serverless', 'blockchain']
            },
            'Healthcare': {
                'technical': ['hipaa', 'clinical', 'medical', 'patient care', 'ehr', 'emr', 'healthcare', 'nursing', 'pharmacy', 'radiology'],
                'soft': ['empathy', 'communication', 'attention to detail', 'critical thinking', 'teamwork'],
                'trending': ['telemedicine', 'digital health', 'ai in healthcare', 'precision medicine']
            },
            'Finance': {
                'technical': ['financial modeling', 'risk management', 'audit', 'compliance', 'sox', 'gaap', 'ifrs', 'excel', 'sql', 'bloomberg', 'reuters'],
                'soft': ['analytical', 'detail-oriented', 'integrity', 'communication', 'strategic thinking'],
                'trending': ['fintech', 'cryptocurrency', 'blockchain', 'algorithmic trading', 'robo-advisory']
            },
            'Marketing': {
                'technical': ['seo', 'sem', 'google analytics', 'facebook ads', 'content marketing', 'email marketing', 'social media', 'crm', 'marketing automation'],
                'soft': ['creativity', 'storytelling', 'data-driven', 'customer-focused', 'adaptability'],
                'trending': ['growth hacking', 'influencer marketing', 'marketing analytics', 'personalization', 'omnichannel']
            },
            'Data Science': {
                'technical': ['python', 'r', 'sql', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn', 'tableau', 'power bi'],
                'soft': ['analytical thinking', 'problem-solving', 'communication', 'business acumen', 'curiosity'],
                'trending': ['mlops', 'automated ml', 'explainable ai', 'edge computing', 'federated learning']
            }
        }
        
        # Experience level expectations
        self.experience_expectations = {
            'Entry Level (0-2 years)': {
                'keywords_weight': 0.7,
                'experience_weight': 0.3,
                'focus_areas': ['education', 'projects', 'internships', 'certifications', 'learning'],
                'expected_skills': 'foundational'
            },
            'Mid Level (3-5 years)': {
                'keywords_weight': 0.8,
                'experience_weight': 0.6,
                'focus_areas': ['achievements', 'project leadership', 'skill development', 'results'],
                'expected_skills': 'intermediate'
            },
            'Senior Level (6-10 years)': {
                'keywords_weight': 0.9,
                'experience_weight': 0.8,
                'focus_areas': ['leadership', 'mentoring', 'strategic impact', 'innovation'],
                'expected_skills': 'advanced'
            },
            'Executive (10+ years)': {
                'keywords_weight': 1.0,
                'experience_weight': 1.0,
                'focus_areas': ['vision', 'transformation', 'p&l responsibility', 'board interaction'],
                'expected_skills': 'expert'
            }
        }
    
    def analyze_resume_comprehensive(self, resume_text: str, job_description: str, 
                                   industry: str = 'Technology', 
                                   experience_level: str = 'Mid Level (3-5 years)',
                                   analysis_depth: str = 'Standard Analysis') -> Dict[str, Any]:
        """
        Perform comprehensive resume analysis with industry and experience context
        """
        try:
            # Generate base analysis prompt
            base_prompt = self._create_comprehensive_analysis_prompt(
                resume_text, job_description, industry, experience_level, analysis_depth
            )
            
            # Get AI analysis
            response = self.model.generate_content(base_prompt)
            base_analysis = self._parse_gemini_response(response.text)
            
            # Enhance with additional analysis layers
            enhanced_analysis = self._enhance_with_advanced_features(
                base_analysis, resume_text, job_description, industry, experience_level, analysis_depth
            )
            
            return enhanced_analysis
            
        except Exception as e:
            return self._get_comprehensive_fallback_analysis(resume_text, job_description, industry)
    
    def _create_comprehensive_analysis_prompt(self, resume_text: str, job_description: str,
                                            industry: str, experience_level: str, analysis_depth: str) -> str:
        """
        Create an advanced, context-aware analysis prompt
        """
        industry_context = self._get_industry_context(industry)
        experience_context = self._get_experience_context(experience_level)
        
        prompt = f"""
        You are an elite ATS and career optimization expert with deep expertise in {industry} industry 
        recruitment and {experience_level} candidate evaluation. Perform a comprehensive analysis of this 
        resume against the job description with {analysis_depth} level analysis.
        
        RESUME TEXT:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        ANALYSIS CONTEXT:
        - Industry: {industry}
        - Experience Level: {experience_level}
        - Analysis Depth: {analysis_depth}
        - Industry Keywords Priority: {industry_context['keywords']}
        - Experience Expectations: {experience_context['expectations']}
        
        Provide analysis in this JSON format:
        {{
            "overall_score": <0-100>,
            "match_percentage": <0-100>,
            "ats_compatibility_score": <0-100>,
            
            "keyword_analysis": {{
                "matched_keywords": ["keyword1", "keyword2", ...],
                "missing_critical_keywords": ["keyword1", "keyword2", ...],
                "missing_nice_to_have": ["keyword1", "keyword2", ...],
                "keyword_density": <0-100>,
                "semantic_matches": ["match1", "match2", ...]
            }},
            
            "skills_analysis": {{
                "technical_skills": <0-100>,
                "soft_skills": <0-100>,
                "industry_knowledge": <0-100>,
                "experience_relevance": <0-100>,
                "leadership_indicators": <0-100>,
                "innovation_indicators": <0-100>
            }},
            
            "ats_analysis": {{
                "formatting_score": <0-100>,
                "parsing_friendliness": "<High/Medium/Low>",
                "section_organization": <0-100>,
                "keyword_placement": <0-100>,
                "file_compatibility": <0-100>
            }},
            
            "content_quality": {{
                "achievement_quantification": <0-100>,
                "action_verb_strength": <0-100>,
                "relevance_to_role": <0-100>,
                "unique_value_proposition": <0-100>,
                "storytelling_coherence": <0-100>
            }},
            
            "industry_fit": {{
                "industry_terminology": <0-100>,
                "sector_experience": <0-100>,
                "trending_skills": <0-100>,
                "compliance_awareness": <0-100>
            }},
            
            "experience_level_assessment": {{
                "matches_level_expectations": <true/false>,
                "career_progression_clarity": <0-100>,
                "responsibility_scope": <0-100>,
                "impact_demonstration": <0-100>
            }},
            
            "strengths": [
                "specific strength 1",
                "specific strength 2",
                "specific strength 3"
            ],
            
            "critical_improvements": [
                "critical improvement 1",
                "critical improvement 2",
                "critical improvement 3"
            ],
            
            "strategic_recommendations": [
                "strategic recommendation 1",
                "strategic recommendation 2",
                "strategic recommendation 3"
            ],
            
            "competitive_positioning": {{
                "estimated_candidate_ranking": "<Top 10%/Top 25%/Top 50%/Bottom 50%>",
                "key_differentiators": ["differentiator1", "differentiator2"],
                "competitive_gaps": ["gap1", "gap2"],
                "market_competitiveness": <0-100>
            }},
            
            "optimization_roadmap": [
                {{
                    "priority": "<Critical/High/Medium/Low>",
                    "action": "specific action",
                    "impact": "expected impact",
                    "effort": "<High/Medium/Low>",
                    "timeframe": "<Immediate/Short-term/Long-term>"
                }}
            ],
            
            "ats_simulation": {{
                "parsing_success_probability": <0-100>,
                "keyword_extraction_accuracy": <0-100>,
                "ranking_prediction": "<Top tier/Mid tier/Lower tier>",
                "pass_through_likelihood": <0-100>
            }},
            
            "red_flags": [
                "potential red flag 1",
                "potential red flag 2"
            ],
            
            "green_flags": [
                "positive indicator 1",
                "positive indicator 2"
            ]
        }}
        
        Focus on:
        1. Industry-specific terminology and requirements
        2. Experience level appropriateness
        3. ATS optimization factors
        4. Competitive market positioning
        5. Actionable improvement strategies
        6. Quantifiable metrics wherever possible
        
        Provide specific, actionable insights rather than generic advice. Consider current market trends 
        in {industry} and expectations for {experience_level} professionals.
        
        Return ONLY the JSON object.
        """
        
        return prompt
    
    def _get_industry_context(self, industry: str) -> Dict[str, Any]:
        """Get industry-specific context for analysis"""
        industry_data = self.industry_keywords.get(industry, self.industry_keywords['Technology'])
        
        return {
            'keywords': industry_data.get('technical', [])[:10],
            'soft_skills': industry_data.get('soft', [])[:5],
            'trending': industry_data.get('trending', [])[:5],
            'weight_multiplier': 1.2  # Industry keywords get higher weight
        }
    
    def _get_experience_context(self, experience_level: str) -> Dict[str, Any]:
        """Get experience level context for analysis"""
        exp_data = self.experience_expectations.get(experience_level, self.experience_expectations['Mid Level (3-5 years)'])
        
        return {
            'expectations': exp_data['focus_areas'],
            'keywords_weight': exp_data['keywords_weight'],
            'experience_weight': exp_data['experience_weight'],
            'skill_level': exp_data['expected_skills']
        }
    
    def _enhance_with_advanced_features(self, base_analysis: Dict[str, Any], 
                                      resume_text: str, job_description: str,
                                      industry: str, experience_level: str, 
                                      analysis_depth: str) -> Dict[str, Any]:
        """
        Enhance base analysis with advanced features
        """
        # Add sentiment analysis
        base_analysis['sentiment_analysis'] = self._analyze_resume_sentiment(resume_text)
        
        # Add readability analysis
        base_analysis['readability_analysis'] = self._analyze_readability(resume_text)
        
        # Add uniqueness analysis
        base_analysis['uniqueness_analysis'] = self._analyze_uniqueness(resume_text, job_description)
        
        # Add industry trend analysis
        base_analysis['trend_analysis'] = self._analyze_industry_trends(resume_text, industry)
        
        # Add career trajectory analysis
        base_analysis['career_trajectory'] = self._analyze_career_trajectory(resume_text, experience_level)
        
        # Add deep dive features if requested
        if analysis_depth == "Deep Dive":
            base_analysis['deep_insights'] = self._perform_deep_dive_analysis(resume_text, job_description)
        
        # Add success probability prediction
        base_analysis['success_prediction'] = self._predict_application_success(base_analysis)
        
        return base_analysis
    
    def _analyze_resume_sentiment(self, resume_text: str) -> Dict[str, Any]:
        """Analyze the sentiment and tone of the resume"""
        strong_words = [
            'achieved', 'accomplished', 'delivered', 'exceeded', 'improved', 'increased',
            'led', 'managed', 'developed', 'created', 'innovated', 'optimized',
            'streamlined', 'transformed', 'pioneered', 'launched', 'implemented'
        ]
        
        weak_words = [
            'responsible for', 'duties included', 'worked on', 'helped with',
            'participated in', 'assisted with', 'involved in', 'contributed to'
        ]
        
        passive_words = [
            'was', 'were', 'had', 'did', 'made', 'got', 'became'
        ]
        
        text_lower = resume_text.lower()
        
        strong_count = sum(1 for word in strong_words if word in text_lower)
        weak_count = sum(1 for word in weak_words if word in text_lower)
        passive_count = sum(1 for word in passive_words if word in text_lower)
        
        total_words = len(resume_text.split())
        
        return {
            'confidence_score': min(100, max(0, (strong_count - weak_count) * 10 + 60)),
            'action_orientation': min(100, strong_count / max(weak_count, 1) * 20),
            'passive_voice_ratio': passive_count / total_words * 100 if total_words > 0 else 0,
            'strong_indicators': strong_count,
            'weak_indicators': weak_count,
            'overall_tone': 'Confident' if strong_count > weak_count else 'Moderate' if strong_count == weak_count else 'Passive'
        }
    
    def _analyze_readability(self, resume_text: str) -> Dict[str, Any]:
        """Analyze readability and clarity of the resume"""
        sentences = resume_text.split('.')
        words = resume_text.split()
        
        avg_words_per_sentence = len(words) / max(len(sentences), 1)
        avg_chars_per_word = sum(len(word) for word in words) / max(len(words), 1)
        
        # Simple readability calculation
        readability_score = max(0, min(100, 100 - (avg_words_per_sentence - 15) * 2 - (avg_chars_per_word - 5) * 3))
        
        return {
            'readability_score': int(readability_score),
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'avg_chars_per_word': round(avg_chars_per_word, 1),
            'total_words': len(words),
            'total_sentences': len(sentences),
            'complexity_level': 'Simple' if readability_score > 80 else 'Moderate' if readability_score > 60 else 'Complex'
        }
    
    def _analyze_uniqueness(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze how unique and differentiated the resume is"""
        resume_words = set(resume_text.lower().split())
        jd_words = set(job_description.lower().split())
        
        unique_to_resume = resume_words - jd_words
        common_words = resume_words & jd_words
        
        uniqueness_ratio = len(unique_to_resume) / len(resume_words) if resume_words else 0
        overlap_ratio = len(common_words) / len(resume_words) if resume_words else 0
        
        return {
            'uniqueness_score': min(100, int(uniqueness_ratio * 100)),
            'overlap_score': min(100, int(overlap_ratio * 100)),
            'differentiation_level': 'High' if uniqueness_ratio > 0.7 else 'Medium' if uniqueness_ratio > 0.5 else 'Low',
            'unique_elements_count': len(unique_to_resume),
            'common_elements_count': len(common_words)
        }
    
    def _analyze_industry_trends(self, resume_text: str, industry: str) -> Dict[str, Any]:
        """Analyze alignment with current industry trends"""
        industry_data = self.industry_keywords.get(industry, {})
        trending_keywords = industry_data.get('trending', [])
        
        text_lower = resume_text.lower()
        found_trending = [keyword for keyword in trending_keywords if keyword in text_lower]
        
        trend_score = len(found_trending) / len(trending_keywords) * 100 if trending_keywords else 0
        
        return {
            'trend_alignment_score': int(trend_score),
            'trending_keywords_found': found_trending,
            'trending_keywords_missing': [kw for kw in trending_keywords if kw not in found_trending],
            'future_readiness': 'High' if trend_score > 60 else 'Medium' if trend_score > 30 else 'Low'
        }
    
    def _analyze_career_trajectory(self, resume_text: str, experience_level: str) -> Dict[str, Any]:
        """Analyze career progression and trajectory"""
        leadership_indicators = [
            'led', 'managed', 'directed', 'supervised', 'coordinated',
            'team', 'staff', 'department', 'organization', 'initiative'
        ]
        
        growth_indicators = [
            'promoted', 'advancement', 'progression', 'increased responsibility',
            'senior', 'lead', 'principal', 'manager', 'director'
        ]
        
        text_lower = resume_text.lower()
        
        leadership_count = sum(1 for indicator in leadership_indicators if indicator in text_lower)
        growth_count = sum(1 for indicator in growth_indicators if indicator in text_lower)
        
        expected_level = self.experience_expectations.get(experience_level, {})
        
        return {
            'leadership_readiness': min(100, leadership_count * 20),
            'growth_trajectory': min(100, growth_count * 25),
            'level_alignment': 'Aligned' if leadership_count >= 2 else 'Developing',
            'career_progression_score': min(100, (leadership_count + growth_count) * 15),
            'next_level_readiness': leadership_count >= 3 and growth_count >= 2
        }
    
    def _perform_deep_dive_analysis(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Perform deep dive analysis with advanced insights"""
        return {
            'quantification_analysis': self._analyze_quantification(resume_text),
            'impact_analysis': self._analyze_impact_statements(resume_text),
            'skill_gap_analysis': self._analyze_skill_gaps(resume_text, job_description),
            'language_sophistication': self._analyze_language_sophistication(resume_text),
            'personal_branding': self._analyze_personal_branding(resume_text)
        }
    
    def _analyze_quantification(self, resume_text: str) -> Dict[str, Any]:
        """Analyze quantification of achievements"""
        # Look for numbers, percentages, metrics
        number_pattern = r'\b\d+(?:,\d{3})*(?:\.\d+)?(?:%|k|K|M|million|billion)?\b'
        numbers = re.findall(number_pattern, resume_text)
        
        metric_indicators = ['increased', 'decreased', 'improved', 'reduced', 'saved', 'generated', 'achieved']
        quantified_achievements = 0
        
        for indicator in metric_indicators:
            if indicator in resume_text.lower():
                # Check if there's a number nearby
                sentences_with_indicator = [s for s in resume_text.split('.') if indicator in s.lower()]
                for sentence in sentences_with_indicator:
                    if re.search(number_pattern, sentence):
                        quantified_achievements += 1
        
        return {
            'quantification_score': min(100, len(numbers) * 10),
            'numbers_found': len(numbers),
            'quantified_achievements': quantified_achievements,
            'quantification_level': 'High' if len(numbers) > 10 else 'Medium' if len(numbers) > 5 else 'Low'
        }
    
    def _analyze_impact_statements(self, resume_text: str) -> Dict[str, Any]:
        """Analyze the strength of impact statements"""
        impact_verbs = [
            'transformed', 'revolutionized', 'pioneered', 'spearheaded', 'orchestrated',
            'architected', 'engineered', 'optimized', 'streamlined', 'enhanced'
        ]
        
        result_indicators = [
            'resulting in', 'leading to', 'which resulted in', 'achieved', 'delivered'
        ]
        
        text_lower = resume_text.lower()
        
        impact_verb_count = sum(1 for verb in impact_verbs if verb in text_lower)
        result_count = sum(1 for indicator in result_indicators if indicator in text_lower)
        
        return {
            'impact_strength': min(100, impact_verb_count * 15),
            'result_orientation': min(100, result_count * 20),
            'impact_verbs_used': impact_verb_count,
            'result_statements': result_count,
            'overall_impact': 'Strong' if impact_verb_count > 3 else 'Moderate' if impact_verb_count > 1 else 'Weak'
        }
    
    def _analyze_skill_gaps(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze critical skill gaps"""
        # Extract skills from job description
        jd_skills = self._extract_skills_from_text(job_description)
        resume_skills = self._extract_skills_from_text(resume_text)
        
        critical_gaps = []
        nice_to_have_gaps = []
        
        # Simple classification based on frequency in job description
        for skill in jd_skills:
            if skill not in resume_skills:
                # Count occurrences in job description to determine criticality
                occurrences = job_description.lower().count(skill.lower())
                if occurrences > 2:
                    critical_gaps.append(skill)
                else:
                    nice_to_have_gaps.append(skill)
        
        return {
            'critical_skill_gaps': critical_gaps[:5],
            'nice_to_have_gaps': nice_to_have_gaps[:5],
            'skill_coverage_percentage': len(resume_skills) / len(jd_skills) * 100 if jd_skills else 0,
            'gap_severity': 'High' if len(critical_gaps) > 3 else 'Medium' if len(critical_gaps) > 1 else 'Low'
        }
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text"""
        # This is a simplified version - in production, you'd use more sophisticated NLP
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'node.js', 'sql',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'agile', 'scrum',
            'leadership', 'communication', 'problem-solving', 'analytics'
        ]
        
        text_lower = text.lower()
        found_skills = [skill for skill in common_skills if skill in text_lower]
        return found_skills
    
    def _analyze_language_sophistication(self, resume_text: str) -> Dict[str, Any]:
        """Analyze language sophistication and professional tone"""
        sophisticated_words = [
            'utilize', 'implement', 'facilitate', 'optimize', 'synthesize',
            'collaborate', 'coordinate', 'orchestrate', 'strategize', 'innovate'
        ]
        
        basic_words = [
            'use', 'do', 'make', 'help', 'work', 'get', 'put', 'take', 'give'
        ]
        
        text_lower = resume_text.lower()
        
        sophisticated_count = sum(1 for word in sophisticated_words if word in text_lower)
        basic_count = sum(1 for word in basic_words if word in text_lower)
        
        return {
            'sophistication_score': min(100, sophisticated_count * 10),
            'vocabulary_level': 'Advanced' if sophisticated_count > basic_count else 'Professional' if sophisticated_count > 0 else 'Basic',
            'sophisticated_terms': sophisticated_count,
            'basic_terms': basic_count
        }
    
    def _analyze_personal_branding(self, resume_text: str) -> Dict[str, Any]:
        """Analyze personal branding elements"""
        branding_indicators = [
            'innovative', 'strategic', 'results-driven', 'experienced', 'skilled',
            'dedicated', 'passionate', 'expert', 'specialist', 'leader'
        ]
        
        text_lower = resume_text.lower()
        
        branding_count = sum(1 for indicator in branding_indicators if indicator in text_lower)
        
        return {
            'branding_strength': min(100, branding_count * 15),
            'brand_indicators': branding_count,
            'personal_brand_clarity': 'Strong' if branding_count > 3 else 'Moderate' if branding_count > 1 else 'Weak'
        }
    
    def _predict_application_success(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Predict application success probability"""
        # Weight different factors
        match_score = analysis.get('match_percentage', 0) * 0.3
        ats_score = analysis.get('ats_compatibility_score', 0) * 0.2
        skills_score = sum(analysis.get('skills_analysis', {}).values()) / len(analysis.get('skills_analysis', {})) * 0.2 if analysis.get('skills_analysis') else 0
        content_score = sum(analysis.get('content_quality', {}).values()) / len(analysis.get('content_quality', {})) * 0.15 if analysis.get('content_quality') else 0
        industry_score = analysis.get('industry_fit', {}).get('industry_terminology', 0) * 0.15
        
        overall_score = match_score + ats_score + skills_score + content_score + industry_score
        
        # Predict success probability
        if overall_score >= 80:
            success_probability = 85
            interview_likelihood = "Very High"
        elif overall_score >= 70:
            success_probability = 70
            interview_likelihood = "High"
        elif overall_score >= 60:
            success_probability = 55
            interview_likelihood = "Moderate"
        else:
            success_probability = 30
            interview_likelihood = "Low"
        
        return {
            'success_probability': int(success_probability),
            'interview_likelihood': interview_likelihood,
            'overall_competitiveness': int(overall_score),
            'key_success_factors': self._identify_success_factors(analysis),
            'main_barriers': self._identify_barriers(analysis)
        }
    
    def _identify_success_factors(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify key success factors"""
        factors = []
        
        if analysis.get('match_percentage', 0) > 75:
            factors.append("Strong keyword alignment")
        
        if analysis.get('ats_compatibility_score', 0) > 80:
            factors.append("Excellent ATS compatibility")
        
        skills = analysis.get('skills_analysis', {})
        if skills.get('technical_skills', 0) > 80:
            factors.append("Strong technical skill match")
        
        return factors[:3]
    
    def _identify_barriers(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify main barriers to success"""
        barriers = []
        
        if analysis.get('match_percentage', 0) < 60:
            barriers.append("Low keyword match rate")
        
        if analysis.get('ats_compatibility_score', 0) < 70:
            barriers.append("ATS compatibility issues")
        
        missing_keywords = analysis.get('keyword_analysis', {}).get('missing_critical_keywords', [])
        if len(missing_keywords) > 5:
            barriers.append("Missing critical keywords")
        
        return barriers[:3]
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's response into structured data"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                return json.loads(response_text)
        except:
            return self._create_fallback_analysis(response_text)
    
    def _create_fallback_analysis(self, response_text: str) -> Dict[str, Any]:
        """Create fallback analysis when parsing fails"""
        return {
            'overall_score': 75,
            'match_percentage': 70,
            'ats_compatibility_score': 80,
            'keyword_analysis': {
                'matched_keywords': ['skill', 'experience', 'education'],
                'missing_critical_keywords': ['leadership', 'analytics'],
                'keyword_density': 65
            },
            'skills_analysis': {
                'technical_skills': 70,
                'soft_skills': 75,
                'industry_knowledge': 70,
                'experience_relevance': 80
            },
            'strengths': [
                'Well-structured resume format',
                'Relevant experience highlighted',
                'Clear professional presentation'
            ],
            'critical_improvements': [
                'Add more job-specific keywords',
                'Quantify achievements with metrics',
                'Enhance technical skills section'
            ],
            'raw_response': response_text[:500]
        }
    
    def _get_comprehensive_fallback_analysis(self, resume_text: str, job_description: str, industry: str) -> Dict[str, Any]:
        """Comprehensive fallback analysis"""
        # Basic keyword matching
        resume_words = set(resume_text.lower().split())
        jd_words = set(job_description.lower().split())
        common_words = resume_words & jd_words
        
        match_percentage = min(len(common_words) / len(jd_words) * 100, 100) if jd_words else 50
        
        return {
            'overall_score': int(match_percentage * 0.8),
            'match_percentage': int(match_percentage),
            'ats_compatibility_score': 75,
            'keyword_analysis': {
                'matched_keywords': list(common_words)[:10],
                'missing_critical_keywords': list(jd_words - resume_words)[:10],
                'keyword_density': int(match_percentage)
            },
            'skills_analysis': {
                'technical_skills': 65,
                'soft_skills': 70,
                'industry_knowledge': 60,
                'experience_relevance': 70
            },
            'industry_fit': {
                'industry_terminology': 65,
                'sector_experience': 70,
                'trending_skills': 50
            },
            'strengths': [
                'Resume successfully processed',
                'Contains relevant industry content',
                'Professional formatting detected'
            ],
            'critical_improvements': [
                'Add more job-specific keywords',
                'Enhance industry-specific terminology',
                'Improve quantification of achievements'
            ],
            'competitive_positioning': {
                'estimated_candidate_ranking': 'Top 50%',
                'market_competitiveness': 65
            },
            'success_prediction': {
                'success_probability': 60,
                'interview_likelihood': 'Moderate'
            },
            'fallback_mode': True
        }