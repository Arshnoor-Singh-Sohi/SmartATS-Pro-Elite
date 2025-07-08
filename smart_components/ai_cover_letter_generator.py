import streamlit as st
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json
import re
from datetime import datetime
from dataclasses import dataclass

@dataclass
class CoverLetterRequest:
    """Data class for cover letter generation requests"""
    company_name: str
    position_title: str
    hiring_manager_name: str
    job_description: str
    resume_summary: str
    industry: str
    experience_level: str
    tone: str
    length: str
    special_requirements: List[str]

class AICoverLetterGenerator:
    """
    Advanced AI-powered cover letter generator that creates personalized,
    compelling cover letters based on resume analysis and job requirements
    """
    
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Cover letter templates and styles
        self.letter_templates = {
            'professional': {
                'tone': 'Professional and formal',
                'structure': ['header', 'opening', 'body_experience', 'body_value', 'closing'],
                'best_for': ['Corporate', 'Finance', 'Healthcare', 'Legal']
            },
            'creative': {
                'tone': 'Creative and engaging',
                'structure': ['header', 'hook_opening', 'story_body', 'value_proposition', 'creative_closing'],
                'best_for': ['Marketing', 'Design', 'Media', 'Startups']
            },
            'technical': {
                'tone': 'Technical and precise',
                'structure': ['header', 'technical_opening', 'skills_body', 'problem_solving', 'closing'],
                'best_for': ['Technology', 'Engineering', 'Research', 'Data Science']
            },
            'executive': {
                'tone': 'Executive and strategic',
                'structure': ['header', 'leadership_opening', 'strategic_body', 'vision_value', 'executive_closing'],
                'best_for': ['C-Level', 'Senior Management', 'Director', 'VP']
            }
        }
        
        # Industry-specific customizations
        self.industry_customizations = {
            'Technology': {
                'key_themes': ['innovation', 'problem-solving', 'scalability', 'user experience'],
                'avoid_terms': ['outdated technologies', 'manual processes'],
                'emphasize': ['technical leadership', 'agile methodologies', 'digital transformation']
            },
            'Healthcare': {
                'key_themes': ['patient care', 'safety', 'compliance', 'quality improvement'],
                'avoid_terms': ['cost-cutting', 'efficiency over safety'],
                'emphasize': ['patient outcomes', 'regulatory compliance', 'interdisciplinary collaboration']
            },
            'Finance': {
                'key_themes': ['risk management', 'regulatory compliance', 'financial analysis', 'strategic planning'],
                'avoid_terms': ['aggressive tactics', 'cutting corners'],
                'emphasize': ['fiduciary responsibility', 'analytical rigor', 'stakeholder value']
            }
        }
        
        # Experience level adjustments
        self.experience_adjustments = {
            'Entry Level (0-2 years)': {
                'focus_areas': ['education', 'internships', 'projects', 'potential', 'eagerness to learn'],
                'tone_modifiers': ['enthusiastic', 'eager', 'motivated', 'fresh perspective'],
                'avoid': ['extensive experience claims', 'leadership without context']
            },
            'Mid Level (3-5 years)': {
                'focus_areas': ['achievements', 'growth', 'specialization', 'collaboration'],
                'tone_modifiers': ['experienced', 'proven', 'collaborative', 'results-driven'],
                'avoid': ['junior language', 'overstatement of seniority']
            },
            'Senior Level (6-10 years)': {
                'focus_areas': ['leadership', 'mentoring', 'strategic impact', 'innovation'],
                'tone_modifiers': ['seasoned', 'strategic', 'leadership-focused', 'transformational'],
                'avoid': ['entry-level enthusiasm', 'tactical-only focus']
            },
            'Executive (10+ years)': {
                'focus_areas': ['vision', 'transformation', 'P&L responsibility', 'board interaction'],
                'tone_modifiers': ['visionary', 'transformational', 'strategic', 'executive presence'],
                'avoid': ['operational details', 'individual contributor language']
            }
        }
    
    def generate_cover_letter(self, request: CoverLetterRequest, 
                            resume_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a personalized cover letter based on request and resume analysis
        """
        # Determine best template
        template_type = self._select_template(request.industry, request.experience_level, request.tone)
        
        # Create comprehensive generation prompt
        prompt = self._create_generation_prompt(request, resume_analysis, template_type)
        
        try:
            # Generate cover letter
            response = self.gemini_model.generate_content(prompt)
            generated_letter = response.text
            
            # Post-process and enhance
            enhanced_letter = self._enhance_cover_letter(generated_letter, request)
            
            # Analyze the generated letter
            analysis = self._analyze_cover_letter(enhanced_letter, request.job_description)
            
            return {
                'cover_letter': enhanced_letter,
                'template_used': template_type,
                'analysis': analysis,
                'optimization_suggestions': self._generate_optimization_suggestions(enhanced_letter, request),
                'alternative_versions': self._generate_alternative_versions(request, resume_analysis)
            }
            
        except Exception as e:
            return self._create_fallback_cover_letter(request, resume_analysis)
    
    def _select_template(self, industry: str, experience_level: str, tone_preference: str) -> str:
        """
        Select the most appropriate template based on context
        """
        # Industry-based selection
        if industry == 'Technology':
            if 'Executive' in experience_level:
                return 'executive'
            else:
                return 'technical'
        elif industry in ['Marketing', 'Design', 'Media']:
            return 'creative'
        elif industry in ['Finance', 'Healthcare', 'Legal']:
            return 'professional'
        elif 'Executive' in experience_level:
            return 'executive'
        
        # Default based on tone preference
        tone_mapping = {
            'professional': 'professional',
            'creative': 'creative',
            'technical': 'technical',
            'executive': 'executive'
        }
        
        return tone_mapping.get(tone_preference.lower(), 'professional')
    
    def _create_generation_prompt(self, request: CoverLetterRequest, 
                                resume_analysis: Dict[str, Any], template_type: str) -> str:
        """
        Create comprehensive prompt for cover letter generation
        """
        template_info = self.letter_templates[template_type]
        industry_info = self.industry_customizations.get(request.industry, {})
        experience_info = self.experience_adjustments.get(request.experience_level, {})
        
        # Extract key information from resume analysis
        strengths = resume_analysis.get('strengths', [])
        matched_keywords = resume_analysis.get('matched_keywords', [])
        achievements = resume_analysis.get('key_achievements', [])
        
        prompt = f"""
        Create a compelling, personalized cover letter as an expert career strategist and professional writer.
        
        POSITION DETAILS:
        - Company: {request.company_name}
        - Position: {request.position_title}
        - Hiring Manager: {request.hiring_manager_name if request.hiring_manager_name else 'Hiring Manager'}
        - Industry: {request.industry}
        - Experience Level: {request.experience_level}
        
        JOB DESCRIPTION:
        {request.job_description}
        
        CANDIDATE PROFILE:
        - Resume Summary: {request.resume_summary}
        - Key Strengths: {', '.join(strengths[:5])}
        - Matched Keywords: {', '.join(matched_keywords[:10])}
        - Notable Achievements: {', '.join(achievements[:3]) if achievements else 'Will be derived from resume summary'}
        
        TEMPLATE REQUIREMENTS:
        - Template Type: {template_type}
        - Tone: {template_info['tone']}
        - Structure: {' → '.join(template_info['structure'])}
        - Length: {request.length}
        
        INDUSTRY CUSTOMIZATION:
        - Key Themes: {', '.join(industry_info.get('key_themes', []))}
        - Emphasize: {', '.join(industry_info.get('emphasize', []))}
        - Avoid: {', '.join(industry_info.get('avoid_terms', []))}
        
        EXPERIENCE LEVEL GUIDANCE:
        - Focus Areas: {', '.join(experience_info.get('focus_areas', []))}
        - Tone Modifiers: {', '.join(experience_info.get('tone_modifiers', []))}
        - Avoid: {', '.join(experience_info.get('avoid', []))}
        
        SPECIAL REQUIREMENTS:
        {chr(10).join(f"- {req}" for req in request.special_requirements) if request.special_requirements else "None"}
        
        WRITING GUIDELINES:
        1. Create a compelling narrative that connects the candidate's background to the role
        2. Use specific examples and achievements from the resume analysis
        3. Demonstrate clear understanding of the company and role requirements
        4. Show personality while maintaining professionalism
        5. Include a strong call to action
        6. Ensure ATS compatibility while being engaging for human readers
        7. Use industry-appropriate language and terminology
        8. Maintain consistent tone throughout
        9. Address potential concerns proactively
        10. Create a memorable impression that differentiates from generic letters
        
        STRUCTURE REQUIREMENTS:
        - Header: Professional header with contact information
        - Opening: Compelling hook that immediately shows fit
        - Body (2-3 paragraphs): 
          * Connect background to role requirements
          * Highlight 2-3 most relevant achievements with specifics
          * Demonstrate company knowledge and cultural fit
        - Closing: Strong call to action and professional sign-off
        
        OUTPUT FORMAT:
        Provide the complete cover letter in professional business format, ready to send.
        Use proper formatting, spacing, and structure.
        
        Write a cover letter that would make a hiring manager excited to interview this candidate.
        """
        
        return prompt
    
    def _enhance_cover_letter(self, generated_letter: str, request: CoverLetterRequest) -> str:
        """
        Post-process and enhance the generated cover letter
        """
        enhanced = generated_letter
        
        # Ensure proper formatting
        enhanced = self._ensure_proper_formatting(enhanced)
        
        # Add company-specific touches
        enhanced = self._add_company_personalization(enhanced, request)
        
        # Optimize for ATS
        enhanced = self._optimize_for_ats(enhanced, request.job_description)
        
        return enhanced
    
    def _ensure_proper_formatting(self, letter: str) -> str:
        """
        Ensure proper business letter formatting
        """
        # Add consistent spacing
        letter = re.sub(r'\n\s*\n\s*\n+', '\n\n', letter)
        
        # Ensure proper date format
        today = datetime.now().strftime("%B %d, %Y")
        if 'date' not in letter.lower() and not re.search(r'\b\d{1,2},?\s+\d{4}\b', letter):
            # Add date if not present
            lines = letter.split('\n')
            if lines and lines[0].strip():
                lines.insert(1, f"\n{today}\n")
                letter = '\n'.join(lines)
        
        return letter.strip()
    
    def _add_company_personalization(self, letter: str, request: CoverLetterRequest) -> str:
        """
        Add company-specific personalization touches
        """
        # This would typically involve company research
        # For now, ensure company name is properly used
        company_variations = [
            request.company_name,
            request.company_name.split()[0] if ' ' in request.company_name else request.company_name
        ]
        
        # Ensure company name appears appropriately
        if not any(var in letter for var in company_variations):
            # Add company mention if missing
            letter = letter.replace(
                "your company", 
                request.company_name, 
                1
            )
        
        return letter
    
    def _optimize_for_ats(self, letter: str, job_description: str) -> str:
        """
        Optimize cover letter for ATS systems
        """
        # Extract key terms from job description
        jd_keywords = self._extract_key_terms(job_description)
        
        # Ensure some key terms are naturally integrated
        # This is a simplified implementation
        letter_lower = letter.lower()
        missing_keywords = [kw for kw in jd_keywords[:5] if kw.lower() not in letter_lower]
        
        # Note: In a real implementation, this would use more sophisticated NLP
        # to naturally integrate keywords without making the letter sound robotic
        
        return letter
    
    def _extract_key_terms(self, job_description: str) -> List[str]:
        """
        Extract key terms from job description
        """
        # Simplified keyword extraction
        # In production, this would use more sophisticated NLP
        words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())
        
        # Filter out common words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'as', 'by', 'from', 'will', 'be', 'been', 'have', 'has', 'had'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return most frequent keywords
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(20)]
    
    def _analyze_cover_letter(self, cover_letter: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze the generated cover letter for quality and effectiveness
        """
        analysis = {
            'length_analysis': self._analyze_length(cover_letter),
            'keyword_alignment': self._analyze_keyword_alignment(cover_letter, job_description),
            'tone_analysis': self._analyze_tone(cover_letter),
            'structure_analysis': self._analyze_structure(cover_letter),
            'readability_score': self._calculate_readability(cover_letter),
            'ats_compatibility': self._assess_ats_compatibility(cover_letter),
            'overall_score': 0  # Will be calculated
        }
        
        # Calculate overall score
        analysis['overall_score'] = self._calculate_overall_score(analysis)
        
        return analysis
    
    def _analyze_length(self, cover_letter: str) -> Dict[str, Any]:
        """
        Analyze cover letter length and provide recommendations
        """
        word_count = len(cover_letter.split())
        char_count = len(cover_letter)
        paragraph_count = len([p for p in cover_letter.split('\n\n') if p.strip()])
        
        # Optimal ranges
        optimal_words = (200, 400)
        optimal_paragraphs = (3, 5)
        
        return {
            'word_count': word_count,
            'character_count': char_count,
            'paragraph_count': paragraph_count,
            'length_assessment': self._assess_length_appropriateness(word_count, optimal_words),
            'recommendations': self._get_length_recommendations(word_count, paragraph_count)
        }
    
    def _analyze_keyword_alignment(self, cover_letter: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze keyword alignment between cover letter and job description
        """
        cl_keywords = set(self._extract_key_terms(cover_letter))
        jd_keywords = set(self._extract_key_terms(job_description))
        
        matched_keywords = cl_keywords & jd_keywords
        coverage_percentage = len(matched_keywords) / len(jd_keywords) * 100 if jd_keywords else 0
        
        return {
            'matched_keywords': list(matched_keywords),
            'coverage_percentage': round(coverage_percentage, 1),
            'missing_keywords': list(jd_keywords - cl_keywords)[:10],
            'keyword_density': len(matched_keywords) / len(cl_keywords) * 100 if cl_keywords else 0
        }
    
    def _analyze_tone(self, cover_letter: str) -> Dict[str, Any]:
        """
        Analyze the tone and style of the cover letter
        """
        # Analyze tone indicators
        confident_words = ['achieve', 'lead', 'drive', 'excel', 'succeed', 'deliver']
        enthusiastic_words = ['excited', 'passionate', 'eager', 'thrilled', 'motivated']
        professional_words = ['experience', 'expertise', 'professional', 'accomplished']
        
        letter_lower = cover_letter.lower()
        
        confidence_score = sum(1 for word in confident_words if word in letter_lower)
        enthusiasm_score = sum(1 for word in enthusiastic_words if word in letter_lower)
        professionalism_score = sum(1 for word in professional_words if word in letter_lower)
        
        return {
            'confidence_level': min(100, confidence_score * 20),
            'enthusiasm_level': min(100, enthusiasm_score * 25),
            'professionalism_level': min(100, professionalism_score * 20),
            'tone_balance': 'Excellent' if all(score >= 2 for score in [confidence_score, enthusiasm_score, professionalism_score]) else 'Good'
        }
    
    def _analyze_structure(self, cover_letter: str) -> Dict[str, Any]:
        """
        Analyze the structure and organization of the cover letter
        """
        paragraphs = [p.strip() for p in cover_letter.split('\n\n') if p.strip()]
        
        # Check for key structural elements
        has_date = bool(re.search(r'\b\d{1,2},?\s+\d{4}\b', cover_letter))
        has_greeting = any(greeting in cover_letter.lower() for greeting in ['dear', 'hello', 'greetings'])
        has_closing = any(closing in cover_letter.lower() for closing in ['sincerely', 'best regards', 'thank you'])
        has_call_to_action = any(phrase in cover_letter.lower() for phrase in ['look forward', 'contact me', 'discuss further'])
        
        structure_score = sum([has_date, has_greeting, has_closing, has_call_to_action]) * 25
        
        return {
            'paragraph_count': len(paragraphs),
            'has_proper_greeting': has_greeting,
            'has_proper_closing': has_closing,
            'has_call_to_action': has_call_to_action,
            'structure_score': structure_score,
            'organization_quality': 'Excellent' if structure_score >= 75 else 'Good' if structure_score >= 50 else 'Needs Improvement'
        }
    
    def _calculate_readability(self, cover_letter: str) -> int:
        """
        Calculate readability score (simplified Flesch Reading Ease)
        """
        sentences = len(re.split(r'[.!?]+', cover_letter))
        words = len(cover_letter.split())
        syllables = sum(self._count_syllables(word) for word in cover_letter.split())
        
        if sentences == 0 or words == 0:
            return 50
        
        # Simplified Flesch Reading Ease calculation
        avg_sentence_length = words / sentences
        avg_syllables_per_word = syllables / words
        
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        return max(0, min(100, int(readability)))
    
    def _count_syllables(self, word: str) -> int:
        """
        Count syllables in a word (simplified)
        """
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_char_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    syllable_count += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False
        
        # Handle silent e
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def _assess_ats_compatibility(self, cover_letter: str) -> Dict[str, Any]:
        """
        Assess ATS compatibility of the cover letter
        """
        # Check for ATS-friendly elements
        has_simple_formatting = not bool(re.search(r'[^\w\s\-.,;:()"\'/\n]', cover_letter))
        reasonable_length = 200 <= len(cover_letter.split()) <= 500
        has_keywords = len(self._extract_key_terms(cover_letter)) >= 10
        
        ats_score = sum([has_simple_formatting, reasonable_length, has_keywords]) * 33.33
        
        return {
            'ats_score': round(ats_score, 1),
            'simple_formatting': has_simple_formatting,
            'appropriate_length': reasonable_length,
            'keyword_rich': has_keywords,
            'compatibility_level': 'High' if ats_score >= 75 else 'Medium' if ats_score >= 50 else 'Low'
        }
    
    def _calculate_overall_score(self, analysis: Dict[str, Any]) -> int:
        """
        Calculate overall cover letter score
        """
        # Weight different factors
        length_score = 100 if analysis['length_analysis']['length_assessment'] == 'Optimal' else 75
        keyword_score = min(100, analysis['keyword_alignment']['coverage_percentage'] * 2)
        structure_score = analysis['structure_analysis']['structure_score']
        readability_score = analysis['readability_score']
        ats_score = analysis['ats_compatibility']['ats_score']
        
        # Weighted average
        weights = {
            'length': 0.15,
            'keywords': 0.25,
            'structure': 0.20,
            'readability': 0.15,
            'ats': 0.25
        }
        
        overall = (
            length_score * weights['length'] +
            keyword_score * weights['keywords'] +
            structure_score * weights['structure'] +
            readability_score * weights['readability'] +
            ats_score * weights['ats']
        )
        
        return round(overall)
    
    def _generate_optimization_suggestions(self, cover_letter: str, 
                                         request: CoverLetterRequest) -> List[Dict[str, str]]:
        """
        Generate specific optimization suggestions
        """
        suggestions = []
        
        # Analyze current letter
        word_count = len(cover_letter.split())
        
        # Length suggestions
        if word_count < 200:
            suggestions.append({
                'category': 'Length',
                'suggestion': 'Expand the letter to include more specific examples and achievements',
                'priority': 'High'
            })
        elif word_count > 400:
            suggestions.append({
                'category': 'Length',
                'suggestion': 'Condense the letter to be more concise and impactful',
                'priority': 'Medium'
            })
        
        # Keyword suggestions
        jd_keywords = self._extract_key_terms(request.job_description)
        cl_keywords = self._extract_key_terms(cover_letter)
        missing_keywords = set(jd_keywords) - set(cl_keywords)
        
        if len(missing_keywords) > 5:
            suggestions.append({
                'category': 'Keywords',
                'suggestion': f'Integrate key terms: {", ".join(list(missing_keywords)[:3])}',
                'priority': 'High'
            })
        
        # Structure suggestions
        if 'sincerely' not in cover_letter.lower() and 'best regards' not in cover_letter.lower():
            suggestions.append({
                'category': 'Structure',
                'suggestion': 'Add a professional closing (e.g., "Sincerely" or "Best regards")',
                'priority': 'Medium'
            })
        
        return suggestions
    
    def _generate_alternative_versions(self, request: CoverLetterRequest, 
                                     resume_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate alternative versions focusing on different aspects
        """
        alternatives = []
        
        # Create variations focusing on different strengths
        focus_areas = [
            {'name': 'Achievement-Focused', 'emphasis': 'quantified results and accomplishments'},
            {'name': 'Skill-Focused', 'emphasis': 'technical skills and expertise'},
            {'name': 'Culture-Focused', 'emphasis': 'cultural fit and company alignment'},
            {'name': 'Leadership-Focused', 'emphasis': 'leadership experience and potential'}
        ]
        
        for focus in focus_areas:
            alternatives.append({
                'version_name': focus['name'],
                'description': f"Version emphasizing {focus['emphasis']}",
                'preview': f"This version would highlight your {focus['emphasis']} to create a compelling narrative..."
            })
        
        return alternatives
    
    def _assess_length_appropriateness(self, word_count: int, optimal_range: tuple) -> str:
        """
        Assess if the length is appropriate
        """
        min_words, max_words = optimal_range
        
        if min_words <= word_count <= max_words:
            return 'Optimal'
        elif word_count < min_words * 0.8:
            return 'Too Short'
        elif word_count > max_words * 1.2:
            return 'Too Long'
        else:
            return 'Acceptable'
    
    def _get_length_recommendations(self, word_count: int, paragraph_count: int) -> List[str]:
        """
        Get specific length recommendations
        """
        recommendations = []
        
        if word_count < 200:
            recommendations.append("Add more specific examples and achievements")
            recommendations.append("Elaborate on how your background fits the role")
        elif word_count > 400:
            recommendations.append("Remove redundant information")
            recommendations.append("Focus on the most relevant achievements")
        
        if paragraph_count < 3:
            recommendations.append("Break content into more paragraphs for better readability")
        elif paragraph_count > 5:
            recommendations.append("Combine related ideas into fewer, more focused paragraphs")
        
        return recommendations
    
    def _create_fallback_cover_letter(self, request: CoverLetterRequest, 
                                    resume_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a fallback cover letter when AI generation fails
        """
        fallback_letter = f"""
{datetime.now().strftime("%B %d, %Y")}

Dear {request.hiring_manager_name if request.hiring_manager_name else 'Hiring Manager'},

I am writing to express my strong interest in the {request.position_title} position at {request.company_name}. With my background in {request.industry} and experience in {request.experience_level.lower()}, I am excited about the opportunity to contribute to your team.

Throughout my career, I have developed expertise in areas that align well with your requirements. My experience has equipped me with the skills necessary to excel in this role and drive meaningful results for {request.company_name}.

I am particularly drawn to {request.company_name} because of your commitment to excellence and innovation. I would welcome the opportunity to discuss how my background and enthusiasm can contribute to your team's continued success.

Thank you for your consideration. I look forward to hearing from you.

Sincerely,
[Your Name]
        """
        
        analysis = {
            'length_analysis': {'word_count': len(fallback_letter.split())},
            'keyword_alignment': {'coverage_percentage': 50},
            'overall_score': 70
        }
        
        return {
            'cover_letter': fallback_letter.strip(),
            'template_used': 'fallback',
            'analysis': analysis,
            'optimization_suggestions': [
                {'category': 'Personalization', 'suggestion': 'Add more specific details about your experience', 'priority': 'High'}
            ],
            'alternative_versions': []
        }

class CoverLetterOptimizer:
    """
    Cover letter optimization and A/B testing engine
    """
    
    def __init__(self):
        self.generator = AICoverLetterGenerator()
    
    def create_multiple_versions(self, request: CoverLetterRequest, 
                               resume_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create multiple optimized versions for A/B testing
        """
        versions = []
        
        # Version 1: Achievement-focused
        achievement_request = self._modify_request_for_focus(request, 'achievements')
        version1 = self.generator.generate_cover_letter(achievement_request, resume_analysis)
        versions.append({
            'name': 'Achievement-Focused',
            'focus': 'Quantified results and measurable impact',
            'letter': version1['cover_letter'],
            'score': version1['analysis']['overall_score']
        })
        
        # Version 2: Skills-focused
        skills_request = self._modify_request_for_focus(request, 'skills')
        version2 = self.generator.generate_cover_letter(skills_request, resume_analysis)
        versions.append({
            'name': 'Skills-Focused',
            'focus': 'Technical expertise and core competencies',
            'letter': version2['cover_letter'],
            'score': version2['analysis']['overall_score']
        })
        
        # Version 3: Culture-focused
        culture_request = self._modify_request_for_focus(request, 'culture')
        version3 = self.generator.generate_cover_letter(culture_request, resume_analysis)
        versions.append({
            'name': 'Culture-Focused',
            'focus': 'Company alignment and cultural fit',
            'letter': version3['cover_letter'],
            'score': version3['analysis']['overall_score']
        })
        
        return sorted(versions, key=lambda x: x['score'], reverse=True)
    
    def _modify_request_for_focus(self, original_request: CoverLetterRequest, focus: str) -> CoverLetterRequest:
        """
        Modify the request to emphasize a specific focus area
        """
        # Create a copy and modify special requirements
        modified_request = CoverLetterRequest(
            company_name=original_request.company_name,
            position_title=original_request.position_title,
            hiring_manager_name=original_request.hiring_manager_name,
            job_description=original_request.job_description,
            resume_summary=original_request.resume_summary,
            industry=original_request.industry,
            experience_level=original_request.experience_level,
            tone=original_request.tone,
            length=original_request.length,
            special_requirements=original_request.special_requirements.copy()
        )
        
        # Add focus-specific requirements
        focus_requirements = {
            'achievements': 'Emphasize quantified achievements and measurable results',
            'skills': 'Focus on technical skills and core competencies',
            'culture': 'Highlight cultural fit and company alignment'
        }
        
        if focus in focus_requirements:
            modified_request.special_requirements.append(focus_requirements[focus])
        
        return modified_request