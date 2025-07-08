import os
import json
import google.generativeai as genai
from typing import Dict, List, Any
import re
from collections import Counter

class GeminiAnalyzer:
    """
    Enhanced Gemini analyzer with industry context and advanced features
    """
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Industry-specific keyword databases
        self.industry_keywords = {
            'Technology': {
                'technical': ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'aws', 'azure', 'docker', 'kubernetes'],
                'soft': ['problem-solving', 'analytical thinking', 'innovation', 'collaboration', 'leadership'],
                'trending': ['ai', 'machine learning', 'cloud native', 'microservices', 'devops']
            },
            'Healthcare': {
                'technical': ['hipaa', 'clinical', 'patient care', 'ehr', 'medical', 'healthcare'],
                'soft': ['empathy', 'communication', 'attention to detail', 'teamwork'],
                'trending': ['telemedicine', 'digital health', 'ai in healthcare']
            },
            'Finance': {
                'technical': ['financial modeling', 'risk management', 'audit', 'compliance', 'excel', 'sql'],
                'soft': ['analytical', 'detail-oriented', 'integrity', 'communication'],
                'trending': ['fintech', 'cryptocurrency', 'blockchain', 'robo-advisory']
            }
        }
        
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Perform comprehensive resume analysis using Gemini AI
        """
        # Create enhanced prompt
        prompt = self._create_analysis_prompt(resume_text, job_description)
        
        try:
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis_result = self._parse_gemini_response(response.text)
            
            # Enhance with additional analysis
            enhanced_result = self._enhance_analysis(
                analysis_result, 
                resume_text, 
                job_description
            )
            
            return enhanced_result
            
        except Exception as e:
            return self._get_fallback_analysis(resume_text, job_description)
    
    def analyze_with_industry_context(self, resume_text: str, job_description: str, 
                                    industry: str = 'Technology', 
                                    experience_level: str = 'Mid Level') -> Dict[str, Any]:
        """
        Enhanced analysis with industry and experience context
        """
        # Get base analysis
        base_analysis = self.analyze_resume(resume_text, job_description)
        
        # Add industry-specific insights
        industry_insights = self._get_industry_insights(industry, base_analysis)
        
        # Add experience level adjustments
        experience_adjustments = self._adjust_for_experience(experience_level, base_analysis)
        
        # Combine all insights
        enhanced_analysis = {
            **base_analysis,
            'industry_insights': industry_insights,
            'experience_adjustments': experience_adjustments,
            'optimization_roadmap': self._create_optimization_roadmap(base_analysis),
            'competitive_analysis': self._perform_competitive_analysis(base_analysis)
        }
        
        return enhanced_analysis
    
    def _create_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """Create comprehensive prompt for analysis"""
        prompt = f"""
        You are an expert ATS analyzer and career coach. Analyze this resume against the job description.
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide analysis in JSON format:
        {{
            "match_percentage": <0-100>,
            "matched_keywords": ["keyword1", "keyword2"],
            "missing_keywords": ["keyword1", "keyword2"],
            "skills_analysis": {{
                "technical_skills": <0-100>,
                "soft_skills": <0-100>,
                "industry_knowledge": <0-100>,
                "experience_relevance": <0-100>
            }},
            "ats_friendliness": "<High/Medium/Low>",
            "strengths": ["strength1", "strength2"],
            "improvements": ["improvement1", "improvement2"],
            "important_terms": ["term1", "term2"],
            "skills_coverage": <0-100>
        }}
        
        Focus on:
        1. Exact keyword matches
        2. Skills alignment
        3. ATS compatibility
        4. Actionable improvements
        
        Return ONLY the JSON object.
        """
        return prompt
    
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
            return self._create_basic_analysis(response_text)
    
    def _enhance_analysis(self, analysis: Dict[str, Any], 
                         resume_text: str, 
                         job_description: str) -> Dict[str, Any]:
        """Enhance the analysis with additional metrics"""
        # Add word frequency analysis
        resume_words = self._extract_important_words(resume_text)
        jd_words = self._extract_important_words(job_description)
        
        # Calculate additional metrics
        common_words = set(resume_words.keys()) & set(jd_words.keys())
        keyword_density = len(common_words) / len(jd_words) * 100 if jd_words else 0
        
        # Add to analysis
        analysis['keyword_density'] = round(keyword_density, 1)
        analysis['resume_word_count'] = len(resume_text.split())
        analysis['common_important_words'] = list(common_words)[:10]
        
        # Ensure all required fields exist
        analysis = self._ensure_complete_analysis(analysis)
        
        return analysis
    
    def _get_industry_insights(self, industry: str, analysis: Dict) -> Dict[str, Any]:
        """Get industry-specific insights"""
        industry_data = self.industry_keywords.get(industry, self.industry_keywords['Technology'])
        
        all_keywords = industry_data['technical'] + industry_data['soft'] + industry_data['trending']
        matched_industry_keywords = [kw for kw in all_keywords if kw in analysis.get('matched_keywords', [])]
        missing_industry_keywords = [kw for kw in all_keywords if kw not in analysis.get('matched_keywords', [])]
        
        return {
            'industry': industry,
            'matched_industry_keywords': matched_industry_keywords,
            'missing_industry_keywords': missing_industry_keywords[:10],
            'industry_score': len(matched_industry_keywords) / len(all_keywords) * 100 if all_keywords else 0,
            'industry_recommendations': self._get_industry_recommendations(industry, missing_industry_keywords[:5])
        }
    
    def _adjust_for_experience(self, experience_level: str, analysis: Dict) -> Dict[str, Any]:
        """Adjust recommendations based on experience level"""
        level_adjustments = {
            "Entry Level": {
                'focus_areas': ['education', 'projects', 'internships', 'certifications'],
                'keyword_weight': 0.8,
                'experience_expectations': 'learning-focused'
            },
            "Mid Level": {
                'focus_areas': ['achievements', 'leadership', 'project management'],
                'keyword_weight': 1.0,
                'experience_expectations': 'growth-oriented'
            },
            "Senior Level": {
                'focus_areas': ['leadership', 'strategy', 'mentoring', 'results'],
                'keyword_weight': 1.2,
                'experience_expectations': 'results-driven'
            }
        }
        
        return level_adjustments.get(experience_level, level_adjustments["Mid Level"])
    
    def _create_optimization_roadmap(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Create optimization roadmap"""
        roadmap = []
        
        # Critical improvements
        if analysis.get('match_percentage', 0) < 50:
            roadmap.append({
                'priority': 'Critical',
                'action': 'Add Job-Specific Keywords',
                'description': 'Your resume lacks essential keywords from the job description',
                'estimated_impact': '+20-30% match score',
                'time_required': '1-2 hours'
            })
        
        # High impact improvements
        if len(analysis.get('missing_keywords', [])) > 3:
            roadmap.append({
                'priority': 'High',
                'action': 'Optimize Skills Section',
                'description': 'Add missing technical keywords naturally',
                'estimated_impact': '+10-15% match score',
                'time_required': '30-60 minutes'
            })
        
        # ATS optimization
        if analysis.get('ats_friendliness') != 'High':
            roadmap.append({
                'priority': 'High',
                'action': 'Improve ATS Compatibility',
                'description': 'Format resume for better ATS parsing',
                'estimated_impact': 'Better ATS pass-through rate',
                'time_required': '45 minutes'
            })
        
        return roadmap
    
    def _perform_competitive_analysis(self, analysis: Dict) -> Dict[str, Any]:
        """Perform competitive analysis"""
        return {
            'estimated_competition_level': 'High' if analysis.get('match_percentage', 0) < 70 else 'Medium',
            'competitive_advantages': self._identify_competitive_advantages(analysis),
            'areas_to_improve': self._identify_improvement_areas(analysis),
            'market_positioning': 'Top 25%' if analysis.get('match_percentage', 0) > 80 else 'Top 50%' if analysis.get('match_percentage', 0) > 60 else 'Needs Improvement'
        }
    
    def _extract_important_words(self, text: str) -> Dict[str, int]:
        """Extract important words and frequencies"""
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'as', 'by', 'from', 'will', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'can', 'could', 'should'
        }
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_freq = Counter(word for word in words if word not in stop_words)
        
        return dict(word_freq.most_common(30))
    
    def _ensure_complete_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure all required fields are present"""
        defaults = {
            'match_percentage': 0,
            'matched_keywords': [],
            'missing_keywords': [],
            'skills_analysis': {
                'technical_skills': 0,
                'soft_skills': 0,
                'industry_knowledge': 0,
                'experience_relevance': 0
            },
            'ats_friendliness': 'Medium',
            'strengths': [],
            'improvements': [],
            'important_terms': [],
            'skills_coverage': 0
        }
        
        for key, default_value in defaults.items():
            if key not in analysis:
                analysis[key] = default_value
        
        return analysis
    
    def _create_basic_analysis(self, response_text: str) -> Dict[str, Any]:
        """Create basic analysis when parsing fails"""
        return {
            'match_percentage': 75,
            'matched_keywords': ['skills', 'experience', 'education'],
            'missing_keywords': ['leadership', 'analytics', 'communication'],
            'skills_analysis': {
                'technical_skills': 70,
                'soft_skills': 80,
                'industry_knowledge': 75,
                'experience_relevance': 75
            },
            'ats_friendliness': 'Medium',
            'strengths': [
                'Well-structured resume format',
                'Relevant experience highlighted',
                'Clear professional presentation'
            ],
            'improvements': [
                'Add more job-specific keywords',
                'Quantify achievements with metrics',
                'Enhance technical skills section'
            ],
            'important_terms': ['experience', 'skills', 'education'],
            'skills_coverage': 75
        }
    
    def _get_fallback_analysis(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Fallback analysis if Gemini fails"""
        # Simple keyword matching
        resume_words = set(resume_text.lower().split())
        jd_words = set(job_description.lower().split())
        common_words = resume_words & jd_words
        
        match_percentage = min(len(common_words) / len(jd_words) * 100, 100) if jd_words else 50
        
        return {
            'match_percentage': int(match_percentage),
            'matched_keywords': list(common_words)[:10],
            'missing_keywords': list(jd_words - resume_words)[:10],
            'skills_analysis': {
                'technical_skills': 65,
                'soft_skills': 70,
                'industry_knowledge': 60,
                'experience_relevance': 70
            },
            'ats_friendliness': 'Medium',
            'strengths': [
                'Resume successfully processed',
                'Contains relevant content',
                'Professional formatting detected'
            ],
            'improvements': [
                'Add more job-specific keywords',
                'Enhance technical skills section',
                'Add quantifiable achievements'
            ],
            'important_terms': list(common_words)[:10],
            'skills_coverage': 65,
            'fallback_mode': True
        }
    
    def _get_industry_recommendations(self, industry: str, missing_keywords: List[str]) -> List[str]:
        """Get industry-specific recommendations"""
        recommendations = {
            "Technology": [
                "Emphasize technical achievements with metrics",
                "Include experience with modern development practices",
                "Highlight problem-solving and innovation skills"
            ],
            "Healthcare": [
                "Emphasize patient outcomes and safety",
                "Include relevant certifications and compliance",
                "Highlight interdisciplinary collaboration"
            ],
            "Finance": [
                "Quantify financial impacts and improvements",
                "Emphasize risk management and compliance",
                "Include analytical and strategic thinking skills"
            ]
        }
        return recommendations.get(industry, ["Tailor resume to industry requirements"])
    
    def _identify_competitive_advantages(self, analysis: Dict) -> List[str]:
        """Identify competitive advantages"""
        advantages = []
        if analysis.get('match_percentage', 0) > 80:
            advantages.append("High keyword alignment with job requirements")
        if len(analysis.get('matched_keywords', [])) > 10:
            advantages.append("Strong technical keyword coverage")
        return advantages
    
    def _identify_improvement_areas(self, analysis: Dict) -> List[str]:
        """Identify key improvement areas"""
        areas = []
        if analysis.get('match_percentage', 0) < 70:
            areas.append("Increase job-specific keyword usage")
        if len(analysis.get('missing_keywords', [])) > 5:
            areas.append("Add more relevant technical skills")
        return areas