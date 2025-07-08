import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
import json
import re
from datetime import datetime
import google.generativeai as genai
import os

class IntelligentResumeBuilder:
    """
    AI-powered resume builder with smart optimization and template generation
    """
    
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Resume templates with different focuses
        self.templates = {
            'ats_optimized': {
                'name': 'ATS-Optimized Professional',
                'description': 'Clean, keyword-rich format designed for ATS systems',
                'structure': ['header', 'summary', 'skills', 'experience', 'education', 'certifications'],
                'ats_score': 95,
                'best_for': ['Corporate roles', 'Large companies', 'Traditional industries']
            },
            'tech_focused': {
                'name': 'Technology Professional',
                'description': 'Technical skills and project-focused layout',
                'structure': ['header', 'technical_summary', 'technical_skills', 'projects', 'experience', 'education'],
                'ats_score': 90,
                'best_for': ['Software development', 'Engineering', 'IT roles']
            },
            'executive': {
                'name': 'Executive Leadership',
                'description': 'Results-driven format for senior positions',
                'structure': ['header', 'executive_summary', 'core_competencies', 'professional_experience', 'education', 'board_positions'],
                'ats_score': 85,
                'best_for': ['C-level positions', 'Senior management', 'Director roles']
            },
            'creative': {
                'name': 'Creative Professional',
                'description': 'Balanced design with ATS compatibility',
                'structure': ['header', 'portfolio', 'summary', 'experience', 'skills', 'education'],
                'ats_score': 80,
                'best_for': ['Design', 'Marketing', 'Creative roles']
            },
            'academic': {
                'name': 'Academic & Research',
                'description': 'Research and publication focused',
                'structure': ['header', 'summary', 'education', 'research', 'publications', 'experience'],
                'ats_score': 75,
                'best_for': ['Academic positions', 'Research roles', 'PhD positions']
            }
        }
        
        # Industry-specific optimization rules
        self.industry_rules = {
            'Technology': {
                'mandatory_sections': ['technical_skills', 'projects'],
                'keyword_focus': ['programming languages', 'frameworks', 'tools', 'methodologies'],
                'achievement_style': 'quantified_technical',
                'preferred_format': 'reverse_chronological'
            },
            'Healthcare': {
                'mandatory_sections': ['certifications', 'clinical_experience'],
                'keyword_focus': ['clinical skills', 'patient care', 'regulations', 'procedures'],
                'achievement_style': 'patient_outcomes',
                'preferred_format': 'functional'
            },
            'Finance': {
                'mandatory_sections': ['certifications', 'financial_analysis'],
                'keyword_focus': ['financial modeling', 'compliance', 'regulations', 'analysis'],
                'achievement_style': 'quantified_financial',
                'preferred_format': 'reverse_chronological'
            }
        }
    
    def analyze_and_optimize_resume(self, resume_text: str, job_description: str, 
                                  target_industry: str, experience_level: str) -> Dict[str, Any]:
        """
        Analyze current resume and provide comprehensive optimization recommendations
        """
        # Parse current resume structure
        current_structure = self._parse_resume_structure(resume_text)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(
            resume_text, job_description, target_industry, experience_level
        )
        
        # Generate AI-powered suggestions
        ai_suggestions = self._generate_ai_suggestions(
            resume_text, job_description, target_industry
        )
        
        # Recommend best template
        template_recommendation = self._recommend_template(
            target_industry, experience_level, job_description
        )
        
        # Create optimized version
        optimized_resume = self._create_optimized_version(
            resume_text, job_description, optimization_opportunities, ai_suggestions
        )
        
        return {
            'current_structure': current_structure,
            'optimization_opportunities': optimization_opportunities,
            'ai_suggestions': ai_suggestions,
            'template_recommendation': template_recommendation,
            'optimized_resume': optimized_resume,
            'improvement_metrics': self._calculate_improvement_metrics(
                resume_text, optimized_resume, job_description
            )
        }
    
    def build_resume_from_scratch(self, user_info: Dict[str, Any], 
                                job_description: str, template_type: str) -> str:
        """
        Build a complete resume from user information using AI
        """
        template = self.templates.get(template_type, self.templates['ats_optimized'])
        
        # Create AI prompt for resume generation
        prompt = self._create_resume_generation_prompt(user_info, job_description, template)
        
        try:
            response = self.gemini_model.generate_content(prompt)
            generated_resume = response.text
            
            # Post-process and validate
            validated_resume = self._validate_and_enhance_resume(generated_resume, job_description)
            
            return validated_resume
            
        except Exception as e:
            return self._create_fallback_resume(user_info, template)
    
    def _parse_resume_structure(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse and analyze current resume structure
        """
        structure = {
            'sections_found': [],
            'missing_sections': [],
            'section_quality': {},
            'overall_structure_score': 0
        }
        
        # Define section patterns
        section_patterns = {
            'contact_info': r'(email|phone|address|linkedin)',
            'summary': r'(summary|profile|objective)',
            'experience': r'(experience|employment|work history)',
            'education': r'(education|academic|degree)',
            'skills': r'(skills|competencies|technical)',
            'certifications': r'(certifications|licenses)',
            'projects': r'(projects|portfolio)',
            'achievements': r'(achievements|awards|honors)'
        }
        
        text_lower = resume_text.lower()
        
        for section, pattern in section_patterns.items():
            if re.search(pattern, text_lower):
                structure['sections_found'].append(section)
                structure['section_quality'][section] = self._evaluate_section_quality(
                    resume_text, section
                )
        
        # Identify missing critical sections
        critical_sections = ['contact_info', 'experience', 'education', 'skills']
        structure['missing_sections'] = [
            section for section in critical_sections 
            if section not in structure['sections_found']
        ]
        
        # Calculate overall structure score
        structure['overall_structure_score'] = (
            len(structure['sections_found']) / len(section_patterns) * 100
        )
        
        return structure
    
    def _identify_optimization_opportunities(self, resume_text: str, job_description: str,
                                          target_industry: str, experience_level: str) -> List[Dict[str, Any]]:
        """
        Identify specific optimization opportunities
        """
        opportunities = []
        
        # Keyword optimization
        keyword_opportunities = self._identify_keyword_opportunities(resume_text, job_description)
        opportunities.extend(keyword_opportunities)
        
        # ATS formatting improvements
        ats_opportunities = self._identify_ats_improvements(resume_text)
        opportunities.extend(ats_opportunities)
        
        # Content enhancement opportunities
        content_opportunities = self._identify_content_improvements(resume_text, experience_level)
        opportunities.extend(content_opportunities)
        
        # Industry-specific opportunities
        industry_opportunities = self._identify_industry_improvements(resume_text, target_industry)
        opportunities.extend(industry_opportunities)
        
        # Sort by impact and effort
        opportunities = sorted(opportunities, key=lambda x: (x['impact'], -x['effort']))
        
        return opportunities
    
    def _identify_keyword_opportunities(self, resume_text: str, job_description: str) -> List[Dict[str, Any]]:
        """
        Identify keyword optimization opportunities
        """
        opportunities = []
        
        # Extract job description keywords
        jd_keywords = self._extract_keywords_from_text(job_description)
        resume_keywords = self._extract_keywords_from_text(resume_text)
        
        missing_keywords = [kw for kw in jd_keywords if kw not in resume_keywords]
        
        for keyword in missing_keywords[:10]:  # Top 10 missing keywords
            opportunities.append({
                'type': 'keyword_addition',
                'description': f"Add '{keyword}' to relevant sections",
                'keyword': keyword,
                'suggested_placement': self._suggest_keyword_placement(keyword, resume_text),
                'impact': 8,
                'effort': 2,
                'category': 'Keywords'
            })
        
        return opportunities
    
    def _identify_ats_improvements(self, resume_text: str) -> List[Dict[str, Any]]:
        """
        Identify ATS formatting improvements
        """
        opportunities = []
        
        # Check for ATS-unfriendly elements
        if re.search(r'[^\w\s\-.,;:()"\'/]', resume_text):
            opportunities.append({
                'type': 'formatting',
                'description': 'Remove special characters that may confuse ATS systems',
                'impact': 6,
                'effort': 3,
                'category': 'ATS Formatting'
            })
        
        # Check for inconsistent date formatting
        date_patterns = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}|\w+\s\d{4}', resume_text)
        if len(set(date_patterns)) > 2:
            opportunities.append({
                'type': 'date_formatting',
                'description': 'Standardize date formats (recommend MM/YYYY)',
                'impact': 5,
                'effort': 2,
                'category': 'ATS Formatting'
            })
        
        return opportunities
    
    def _identify_content_improvements(self, resume_text: str, experience_level: str) -> List[Dict[str, Any]]:
        """
        Identify content enhancement opportunities
        """
        opportunities = []
        
        # Check for quantification
        numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?(?:%|k|K|M|million|billion)?\b', resume_text)
        if len(numbers) < 5:
            opportunities.append({
                'type': 'quantification',
                'description': 'Add more quantified achievements (numbers, percentages, metrics)',
                'impact': 9,
                'effort': 4,
                'category': 'Content Enhancement'
            })
        
        # Check for action verbs
        weak_verbs = ['responsible for', 'duties included', 'worked on']
        for weak_verb in weak_verbs:
            if weak_verb in resume_text.lower():
                opportunities.append({
                    'type': 'action_verbs',
                    'description': f"Replace '{weak_verb}' with stronger action verbs",
                    'impact': 7,
                    'effort': 3,
                    'category': 'Content Enhancement'
                })
        
        # Experience level specific checks
        if 'Senior' in experience_level or 'Executive' in experience_level:
            if 'led' not in resume_text.lower() and 'managed' not in resume_text.lower():
                opportunities.append({
                    'type': 'leadership',
                    'description': 'Add more leadership and management achievements',
                    'impact': 8,
                    'effort': 5,
                    'category': 'Content Enhancement'
                })
        
        return opportunities
    
    def _identify_industry_improvements(self, resume_text: str, target_industry: str) -> List[Dict[str, Any]]:
        """
        Identify industry-specific improvements
        """
        opportunities = []
        
        industry_rules = self.industry_rules.get(target_industry, {})
        mandatory_sections = industry_rules.get('mandatory_sections', [])
        
        for section in mandatory_sections:
            if section not in resume_text.lower():
                opportunities.append({
                    'type': 'industry_section',
                    'description': f"Add {section.replace('_', ' ').title()} section for {target_industry}",
                    'impact': 8,
                    'effort': 6,
                    'category': 'Industry Alignment'
                })
        
        return opportunities
    
    def _generate_ai_suggestions(self, resume_text: str, job_description: str, 
                               target_industry: str) -> Dict[str, Any]:
        """
        Generate AI-powered suggestions for resume improvement
        """
        prompt = f"""
        As an expert resume consultant specializing in {target_industry}, analyze this resume 
        against the job description and provide specific, actionable improvement suggestions.
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide suggestions in JSON format:
        {{
            "summary_improvements": ["suggestion1", "suggestion2"],
            "experience_enhancements": ["enhancement1", "enhancement2"],
            "skills_additions": ["skill1", "skill2"],
            "achievement_rewrites": [
                {{"original": "original text", "improved": "improved version"}},
                {{"original": "original text", "improved": "improved version"}}
            ],
            "keyword_integration": [
                {{"keyword": "keyword", "suggested_context": "how to integrate naturally"}}
            ],
            "section_reorganization": ["reorganization suggestion1", "reorganization suggestion2"],
            "industry_specific_tips": ["tip1", "tip2"]
        }}
        
        Focus on specific, actionable improvements that will increase ATS compatibility and human appeal.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return self._get_fallback_suggestions()
    
    def _recommend_template(self, target_industry: str, experience_level: str, 
                          job_description: str) -> Dict[str, Any]:
        """
        Recommend the best template based on context
        """
        # Industry mapping
        industry_template_map = {
            'Technology': 'tech_focused',
            'Healthcare': 'ats_optimized',
            'Finance': 'ats_optimized',
            'Marketing': 'creative',
            'Education': 'academic'
        }
        
        # Experience level considerations
        if 'Executive' in experience_level:
            recommended_template = 'executive'
        elif 'Entry' in experience_level and target_industry == 'Technology':
            recommended_template = 'tech_focused'
        else:
            recommended_template = industry_template_map.get(target_industry, 'ats_optimized')
        
        template = self.templates[recommended_template]
        
        return {
            'recommended_template': recommended_template,
            'template_details': template,
            'reasoning': self._explain_template_choice(template, target_industry, experience_level),
            'alternatives': self._suggest_alternative_templates(recommended_template)
        }
    
    def _create_optimized_version(self, resume_text: str, job_description: str,
                                opportunities: List[Dict], ai_suggestions: Dict) -> str:
        """
        Create an optimized version of the resume
        """
        prompt = f"""
        Create an optimized version of this resume incorporating the following improvements:
        
        ORIGINAL RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        OPTIMIZATION OPPORTUNITIES:
        {json.dumps(opportunities[:10], indent=2)}
        
        AI SUGGESTIONS:
        {json.dumps(ai_suggestions, indent=2)}
        
        Guidelines:
        1. Maintain the original structure and content integrity
        2. Integrate keywords naturally
        3. Improve action verbs and quantification
        4. Enhance ATS compatibility
        5. Keep the tone professional and authentic
        6. Preserve all factual information
        
        Return the complete optimized resume text.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except:
            return self._create_basic_optimization(resume_text, opportunities)
    
    def _create_resume_generation_prompt(self, user_info: Dict[str, Any], 
                                       job_description: str, template: Dict) -> str:
        """
        Create a comprehensive prompt for resume generation
        """
        prompt = f"""
        Create a professional resume using the following information and job description.
        
        USER INFORMATION:
        {json.dumps(user_info, indent=2)}
        
        TARGET JOB DESCRIPTION:
        {job_description}
        
        TEMPLATE STRUCTURE:
        {template['structure']}
        
        TEMPLATE FOCUS:
        {template['description']}
        
        Requirements:
        1. Follow the specified template structure
        2. Optimize for ATS compatibility (target score: {template['ats_score']}%)
        3. Include relevant keywords from the job description
        4. Use strong action verbs and quantified achievements
        5. Maintain professional tone throughout
        6. Ensure all dates and information are consistent
        7. Keep each section focused and relevant
        
        Best practices:
        - Use reverse chronological order for experience
        - Include specific achievements with metrics
        - Tailor skills section to job requirements
        - Write compelling summary that matches job requirements
        - Use industry-standard terminology
        
        Return a complete, well-formatted resume.
        """
        
        return prompt
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """
        Extract relevant keywords from text
        """
        # Simple keyword extraction (in production, use more sophisticated NLP)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'as', 'by', 'from', 'will', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'can', 'could', 'should'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return most frequent keywords
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(30)]
    
    def _suggest_keyword_placement(self, keyword: str, resume_text: str) -> str:
        """
        Suggest where to place a keyword in the resume
        """
        keyword_lower = keyword.lower()
        
        # Technical keywords go in skills section
        tech_keywords = ['python', 'java', 'sql', 'aws', 'docker', 'kubernetes']
        if any(tech in keyword_lower for tech in tech_keywords):
            return "Technical Skills section"
        
        # Soft skills in summary or experience
        soft_keywords = ['leadership', 'communication', 'teamwork', 'management']
        if any(soft in keyword_lower for soft in soft_keywords):
            return "Professional Summary or Experience descriptions"
        
        # Industry terms in experience
        return "Experience section or Professional Summary"
    
    def _evaluate_section_quality(self, resume_text: str, section: str) -> int:
        """
        Evaluate the quality of a resume section
        """
        # Simple quality scoring (0-100)
        section_text = self._extract_section_text(resume_text, section)
        
        if not section_text:
            return 0
        
        score = 50  # Base score
        
        # Length check
        if len(section_text) > 100:
            score += 20
        
        # Quantification check
        if re.search(r'\d+(?:%|k|K|M|million|billion)', section_text):
            score += 15
        
        # Action verbs check
        action_verbs = ['achieved', 'improved', 'led', 'managed', 'developed']
        if any(verb in section_text.lower() for verb in action_verbs):
            score += 15
        
        return min(100, score)
    
    def _extract_section_text(self, resume_text: str, section: str) -> str:
        """
        Extract text from a specific resume section
        """
        # Simple section extraction (in production, use more sophisticated parsing)
        section_patterns = {
            'summary': r'(summary|profile|objective)[\s\S]*?(?=\n[A-Z]|\n\n|\Z)',
            'experience': r'(experience|employment)[\s\S]*?(?=\n[A-Z]|\n\n|\Z)',
            'skills': r'(skills|competencies)[\s\S]*?(?=\n[A-Z]|\n\n|\Z)'
        }
        
        pattern = section_patterns.get(section, '')
        if pattern:
            match = re.search(pattern, resume_text, re.IGNORECASE)
            return match.group(0) if match else ""
        
        return ""
    
    def _calculate_improvement_metrics(self, original_resume: str, 
                                     optimized_resume: str, job_description: str) -> Dict[str, Any]:
        """
        Calculate improvement metrics between original and optimized resume
        """
        # Simple metrics calculation
        original_keywords = self._extract_keywords_from_text(original_resume)
        optimized_keywords = self._extract_keywords_from_text(optimized_resume)
        jd_keywords = self._extract_keywords_from_text(job_description)
        
        original_match = len(set(original_keywords) & set(jd_keywords))
        optimized_match = len(set(optimized_keywords) & set(jd_keywords))
        
        return {
            'keyword_improvement': optimized_match - original_match,
            'keyword_match_rate_original': original_match / len(jd_keywords) * 100 if jd_keywords else 0,
            'keyword_match_rate_optimized': optimized_match / len(jd_keywords) * 100 if jd_keywords else 0,
            'estimated_score_improvement': min(25, (optimized_match - original_match) * 3),
            'content_length_change': len(optimized_resume) - len(original_resume)
        }
    
    def _explain_template_choice(self, template: Dict, industry: str, experience_level: str) -> str:
        """
        Explain why a specific template was recommended
        """
        reasoning = f"The {template['name']} template is recommended because:\n"
        reasoning += f"• It's optimized for {industry} industry with {template['ats_score']}% ATS compatibility\n"
        reasoning += f"• The structure ({', '.join(template['structure'])}) aligns with {experience_level} expectations\n"
        reasoning += f"• It's proven effective for: {', '.join(template['best_for'])}"
        
        return reasoning
    
    def _suggest_alternative_templates(self, recommended: str) -> List[Dict[str, Any]]:
        """
        Suggest alternative templates
        """
        alternatives = []
        for key, template in self.templates.items():
            if key != recommended:
                alternatives.append({
                    'template_id': key,
                    'name': template['name'],
                    'ats_score': template['ats_score'],
                    'best_for': template['best_for'][:2]  # First 2 use cases
                })
        
        return sorted(alternatives, key=lambda x: x['ats_score'], reverse=True)[:3]
    
    def _get_fallback_suggestions(self) -> Dict[str, Any]:
        """
        Provide fallback suggestions when AI fails
        """
        return {
            'summary_improvements': [
                "Add quantified achievements to professional summary",
                "Include 2-3 key skills that match job requirements"
            ],
            'experience_enhancements': [
                "Use stronger action verbs (achieved, implemented, optimized)",
                "Quantify results with specific numbers and percentages"
            ],
            'skills_additions': [
                "Add technical skills mentioned in job description",
                "Include relevant soft skills like leadership and communication"
            ],
            'achievement_rewrites': [
                {"original": "Responsible for managing team", "improved": "Led cross-functional team of 8 members, achieving 15% improvement in project delivery time"}
            ],
            'industry_specific_tips': [
                "Use industry-standard terminology and acronyms",
                "Highlight relevant certifications and training"
            ]
        }
    
    def _create_basic_optimization(self, resume_text: str, opportunities: List[Dict]) -> str:
        """
        Create basic optimization when AI fails
        """
        optimized = resume_text
        
        # Apply simple optimizations
        for opp in opportunities[:5]:  # Apply top 5 opportunities
            if opp['type'] == 'keyword_addition':
                # Simple keyword addition
                optimized += f"\n• {opp['keyword']}"
            elif opp['type'] == 'action_verbs':
                # Replace weak verbs
                optimized = optimized.replace("responsible for", "managed")
                optimized = optimized.replace("worked on", "developed")
        
        return optimized
    
    def _create_fallback_resume(self, user_info: Dict[str, Any], template: Dict) -> str:
        """
        Create a basic resume when AI generation fails
        """
        name = user_info.get('name', 'Your Name')
        email = user_info.get('email', 'your.email@example.com')
        phone = user_info.get('phone', '(555) 123-4567')
        
        resume = f"""
{name}
{email} | {phone}

PROFESSIONAL SUMMARY
Experienced professional with expertise in {user_info.get('industry', 'your field')}. 
Proven track record of delivering results and driving innovation.

CORE COMPETENCIES
• Leadership and Team Management
• Strategic Planning and Execution
• Process Improvement
• Cross-functional Collaboration

PROFESSIONAL EXPERIENCE
[Add your work experience here]

EDUCATION
[Add your education here]

CERTIFICATIONS
[Add relevant certifications here]
        """
        
        return resume.strip()

class ResumeOptimizationEngine:
    """
    Engine for continuous resume optimization and A/B testing
    """
    
    def __init__(self):
        self.builder = IntelligentResumeBuilder()
    
    def create_multiple_versions(self, resume_text: str, job_description: str, 
                               target_industry: str) -> List[Dict[str, Any]]:
        """
        Create multiple optimized versions for A/B testing
        """
        versions = []
        
        # Version 1: Keyword-focused optimization
        keyword_optimized = self._create_keyword_focused_version(resume_text, job_description)
        versions.append({
            'name': 'Keyword-Optimized',
            'focus': 'Maximum keyword density and ATS compatibility',
            'content': keyword_optimized,
            'estimated_improvement': '+15-20% match score'
        })
        
        # Version 2: Achievement-focused optimization
        achievement_optimized = self._create_achievement_focused_version(resume_text)
        versions.append({
            'name': 'Achievement-Focused',
            'focus': 'Quantified results and impact statements',
            'content': achievement_optimized,
            'estimated_improvement': '+10-15% recruiter appeal'
        })
        
        # Version 3: Industry-specific optimization
        industry_optimized = self._create_industry_focused_version(resume_text, target_industry)
        versions.append({
            'name': 'Industry-Specialized',
            'focus': 'Industry terminology and best practices',
            'content': industry_optimized,
            'estimated_improvement': '+12-18% industry relevance'
        })
        
        return versions
    
    def _create_keyword_focused_version(self, resume_text: str, job_description: str) -> str:
        """Create a version optimized for keyword matching"""
        # Extract top keywords from job description
        jd_keywords = self.builder._extract_keywords_from_text(job_description)
        
        # Integrate keywords naturally into resume
        optimized = resume_text
        
        # Add keywords to skills section
        if 'SKILLS' in optimized.upper():
            for keyword in jd_keywords[:10]:
                if keyword not in optimized.lower():
                    optimized = optimized.replace('SKILLS', f'SKILLS\n• {keyword.title()}', 1)
        
        return optimized
    
    def _create_achievement_focused_version(self, resume_text: str) -> str:
        """Create a version focused on quantified achievements"""
        optimized = resume_text
        
        # Replace weak phrases with strong action verbs
        replacements = {
            'responsible for': 'managed',
            'worked on': 'developed',
            'helped with': 'contributed to',
            'duties included': 'achieved'
        }
        
        for weak, strong in replacements.items():
            optimized = optimized.replace(weak, strong)
        
        return optimized
    
    def _create_industry_focused_version(self, resume_text: str, industry: str) -> str:
        """Create a version optimized for specific industry"""
        optimized = resume_text
        
        # Add industry-specific terminology
        industry_terms = {
            'Technology': ['agile', 'scrum', 'CI/CD', 'cloud computing', 'API'],
            'Healthcare': ['patient care', 'clinical', 'HIPAA', 'EHR', 'quality improvement'],
            'Finance': ['risk management', 'compliance', 'financial modeling', 'audit', 'regulatory']
        }
        
        terms = industry_terms.get(industry, [])
        for term in terms[:5]:
            if term not in optimized.lower():
                optimized += f"\n• {term}"
        
        return optimized