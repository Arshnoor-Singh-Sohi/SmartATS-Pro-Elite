import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import re
import numpy as np
from dataclasses import dataclass, asdict
import hashlib
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import time

@dataclass
class JobOpportunity:
    """Job opportunity data model"""
    id: str
    title: str
    company: str
    location: str
    job_type: str  # full-time, part-time, contract, remote
    salary_range: str
    posted_date: datetime
    source: str
    job_url: str
    description: str
    requirements: List[str]
    benefits: List[str]
    match_score: float
    ai_insights: Dict[str, Any]
    application_deadline: Optional[datetime]
    company_size: str
    industry: str
    seniority_level: str

@dataclass
class MarketTrend:
    """Market trend data model"""
    keyword: str
    demand_score: int
    growth_rate: float
    salary_impact: float
    geographic_hotspots: List[str]
    trending_period: str
    related_skills: List[str]

class JobMarketScanner:
    """
    AI-powered job market scanning and opportunity matching system
    """
    
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        self.session_key = 'job_market_scanner'
        self._initialize_scanner()
        
        # Job board APIs and sources (simulated for demo)
        self.job_sources = {
            'linkedin': {
                'base_url': 'https://linkedin.com/jobs/search',
                'rate_limit': 100,  # requests per hour
                'supported_filters': ['location', 'experience', 'company', 'industry']
            },
            'indeed': {
                'base_url': 'https://indeed.com/jobs',
                'rate_limit': 1000,
                'supported_filters': ['location', 'salary', 'date_posted', 'job_type']
            },
            'glassdoor': {
                'base_url': 'https://glassdoor.com/Jobs',
                'rate_limit': 500,
                'supported_filters': ['company_rating', 'salary', 'location']
            },
            'company_websites': {
                'base_url': 'direct',
                'rate_limit': 50,
                'supported_filters': ['company_specific']
            }
        }
        
        # AI matching algorithms
        self.matching_weights = {
            'title_match': 0.25,
            'skills_match': 0.30,
            'experience_match': 0.20,
            'location_preference': 0.10,
            'salary_alignment': 0.10,
            'company_culture': 0.05
        }
        
        # Market intelligence factors
        self.market_factors = {
            'demand_indicators': ['job_postings_volume', 'application_ratios', 'time_to_fill'],
            'supply_indicators': ['candidate_pool_size', 'skill_availability', 'geographic_distribution'],
            'trend_indicators': ['emerging_technologies', 'industry_growth', 'remote_work_adoption']
        }
    
    def _initialize_scanner(self):
        """Initialize the scanner system"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                'scan_history': [],
                'saved_opportunities': {},
                'market_insights': {},
                'user_preferences': {
                    'preferred_sources': ['linkedin', 'indeed'],
                    'scan_frequency': 'daily',
                    'notification_threshold': 85,  # minimum match score for notifications
                    'auto_apply_threshold': 95,   # threshold for auto-application suggestions
                },
                'tracking_keywords': [],
                'market_alerts': []
            }
    
    def scan_job_market(self, search_criteria: Dict[str, Any], 
                       resume_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive job market scan
        """
        # Execute parallel scanning across sources
        scan_results = self._execute_parallel_scan(search_criteria)
        
        # AI-powered opportunity matching
        matched_opportunities = self._match_opportunities(scan_results, resume_profile)
        
        # Market trend analysis
        market_trends = self._analyze_market_trends(scan_results, search_criteria)
        
        # Generate insights and recommendations
        insights = self._generate_market_insights(matched_opportunities, market_trends)
        
        # Create opportunity pipeline
        pipeline = self._create_opportunity_pipeline(matched_opportunities)
        
        # Store scan results
        scan_record = {
            'timestamp': datetime.now(),
            'criteria': search_criteria,
            'total_opportunities': len(scan_results),
            'high_match_opportunities': len([o for o in matched_opportunities if o['match_score'] > 80]),
            'market_score': insights.get('market_health_score', 75)
        }
        st.session_state[self.session_key]['scan_history'].append(scan_record)
        
        return {
            'opportunities': matched_opportunities,
            'market_trends': market_trends,
            'insights': insights,
            'pipeline': pipeline,
            'scan_summary': scan_record,
            'recommendations': self._generate_action_recommendations(matched_opportunities, insights)
        }
    
    def _execute_parallel_scan(self, search_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute parallel scanning across multiple job sources
        """
        # Simulate API calls to different job boards
        # In production, this would make actual API calls
        
        all_opportunities = []
        
        # Simulated job data for demo
        simulated_jobs = self._generate_simulated_jobs(search_criteria)
        
        for job_source, opportunities in simulated_jobs.items():
            # Add source metadata
            for opp in opportunities:
                opp['source'] = job_source
                opp['scraped_at'] = datetime.now()
                opp['confidence_score'] = np.random.uniform(0.7, 0.98)
            
            all_opportunities.extend(opportunities)
        
        # Remove duplicates based on company + title similarity
        unique_opportunities = self._deduplicate_opportunities(all_opportunities)
        
        return unique_opportunities
    
    def _generate_simulated_jobs(self, criteria: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """
        Generate simulated job data for demonstration
        """
        # This would be replaced with actual API calls in production
        role = criteria.get('role', 'Software Engineer')
        location = criteria.get('location', 'Remote')
        industry = criteria.get('industry', 'Technology')
        
        companies = [
            'TechCorp', 'InnovateSoft', 'DataDriven Inc', 'CloudFirst', 'AI Solutions',
            'NextGen Systems', 'Digital Dynamics', 'ScaleTech', 'FutureWorks', 'CodeCraft'
        ]
        
        job_types = ['Full-time', 'Contract', 'Part-time', 'Remote']
        seniority_levels = ['Entry', 'Mid', 'Senior', 'Lead', 'Principal']
        
        simulated_data = {}
        
        for source in ['linkedin', 'indeed', 'glassdoor']:
            jobs = []
            
            for i in range(np.random.randint(15, 35)):
                company = np.random.choice(companies)
                seniority = np.random.choice(seniority_levels)
                
                job = {
                    'id': f"{source}_{i}_{hashlib.md5(f'{company}{role}'.encode()).hexdigest()[:8]}",
                    'title': f"{seniority} {role}",
                    'company': company,
                    'location': location if location != 'Remote' else np.random.choice(['Remote', 'San Francisco', 'New York', 'Seattle']),
                    'job_type': np.random.choice(job_types),
                    'salary_range': self._generate_salary_range(seniority, industry),
                    'posted_date': datetime.now() - timedelta(days=np.random.randint(1, 30)),
                    'job_url': f"https://{source}.com/jobs/{i}",
                    'description': self._generate_job_description(role, seniority, company),
                    'requirements': self._generate_requirements(role, seniority),
                    'benefits': self._generate_benefits(),
                    'company_size': np.random.choice(['Startup', 'Mid-size', 'Enterprise']),
                    'industry': industry,
                    'seniority_level': seniority
                }
                
                jobs.append(job)
            
            simulated_data[source] = jobs
        
        return simulated_data
    
    def _generate_salary_range(self, seniority: str, industry: str) -> str:
        """Generate realistic salary range"""
        base_salaries = {
            'Entry': (60000, 80000),
            'Mid': (80000, 120000),
            'Senior': (120000, 160000),
            'Lead': (150000, 200000),
            'Principal': (180000, 250000)
        }
        
        industry_multipliers = {
            'Technology': 1.2,
            'Finance': 1.1,
            'Healthcare': 0.9,
            'Education': 0.8
        }
        
        base_min, base_max = base_salaries.get(seniority, (75000, 100000))
        multiplier = industry_multipliers.get(industry, 1.0)
        
        min_salary = int(base_min * multiplier)
        max_salary = int(base_max * multiplier)
        
        return f"${min_salary:,} - ${max_salary:,}"
    
    def _generate_job_description(self, role: str, seniority: str, company: str) -> str:
        """Generate realistic job description"""
        templates = {
            'Software Engineer': f"""
            {company} is seeking a {seniority} Software Engineer to join our dynamic team. 
            You'll be responsible for developing scalable applications, collaborating with cross-functional teams, 
            and contributing to our technical architecture. We're looking for someone passionate about clean code, 
            innovation, and delivering exceptional user experiences.
            
            Key responsibilities include building robust software solutions, participating in code reviews, 
            and mentoring junior team members. You'll work with modern technologies and have opportunities 
            to influence technical decisions and product direction.
            """,
            'Data Scientist': f"""
            Join {company} as a {seniority} Data Scientist and help drive data-informed decisions across the organization. 
            You'll work with large datasets, build predictive models, and translate complex analytics into actionable insights. 
            
            This role involves collaborating with product teams, developing machine learning models, and presenting 
            findings to stakeholders. We're looking for someone with strong analytical skills and a passion for 
            turning data into business value.
            """,
            'Product Manager': f"""
            {company} is looking for a {seniority} Product Manager to lead product strategy and execution. 
            You'll define product roadmaps, work closely with engineering and design teams, and ensure we're 
            building products that delight our customers.
            
            Key responsibilities include conducting market research, gathering user feedback, prioritizing features, 
            and driving cross-functional alignment. We need someone who can think strategically while executing tactically.
            """
        }
        
        return templates.get(role, f"Exciting {seniority} {role} opportunity at {company}.")
    
    def _generate_requirements(self, role: str, seniority: str) -> List[str]:
        """Generate job requirements"""
        base_requirements = {
            'Software Engineer': [
                'Bachelor\'s degree in Computer Science or related field',
                'Proficiency in Python, Java, or JavaScript',
                'Experience with web frameworks and databases',
                'Understanding of software development lifecycle',
                'Strong problem-solving and communication skills'
            ],
            'Data Scientist': [
                'Advanced degree in Statistics, Mathematics, or related field',
                'Proficiency in Python/R and SQL',
                'Experience with machine learning libraries',
                'Strong statistical and analytical skills',
                'Ability to communicate complex findings clearly'
            ],
            'Product Manager': [
                'Bachelor\'s degree in Business, Engineering, or related field',
                'Experience with product management tools',
                'Strong analytical and strategic thinking skills',
                'Excellent communication and leadership abilities',
                'Understanding of user experience principles'
            ]
        }
        
        requirements = base_requirements.get(role, ['Relevant experience', 'Strong communication skills'])
        
        # Add seniority-specific requirements
        if seniority in ['Senior', 'Lead', 'Principal']:
            requirements.extend([
                f'{5 if seniority == "Senior" else 7 if seniority == "Lead" else 10}+ years of relevant experience',
                'Leadership and mentoring experience',
                'Track record of delivering complex projects'
            ])
        
        return requirements
    
    def _generate_benefits(self) -> List[str]:
        """Generate company benefits"""
        benefit_pool = [
            'Competitive salary and equity',
            'Comprehensive health insurance',
            'Flexible work arrangements',
            'Professional development budget',
            'Unlimited PTO',
            '401(k) matching',
            'Remote work options',
            'Gym membership reimbursement',
            'Catered meals',
            'Learning and development opportunities'
        ]
        
        return list(np.random.choice(benefit_pool, size=np.random.randint(4, 8), replace=False))
    
    def _match_opportunities(self, opportunities: List[Dict[str, Any]], 
                           resume_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        AI-powered matching of opportunities to resume profile
        """
        matched_opportunities = []
        
        user_skills = resume_profile.get('skills', [])
        user_experience = resume_profile.get('years_experience', 3)
        preferred_locations = resume_profile.get('preferred_locations', ['Remote'])
        salary_expectations = resume_profile.get('salary_range', {'min': 75000, 'max': 120000})
        
        for opp in opportunities:
            # Calculate individual match scores
            title_score = self._calculate_title_match(opp['title'], resume_profile.get('target_roles', []))
            skills_score = self._calculate_skills_match(opp['requirements'], user_skills)
            experience_score = self._calculate_experience_match(opp['seniority_level'], user_experience)
            location_score = self._calculate_location_match(opp['location'], preferred_locations)
            salary_score = self._calculate_salary_match(opp['salary_range'], salary_expectations)
            
            # Calculate weighted overall match score
            overall_score = (
                title_score * self.matching_weights['title_match'] +
                skills_score * self.matching_weights['skills_match'] +
                experience_score * self.matching_weights['experience_match'] +
                location_score * self.matching_weights['location_preference'] +
                salary_score * self.matching_weights['salary_alignment']
            ) * 100
            
            # Generate AI insights for this opportunity
            ai_insights = self._generate_opportunity_insights(opp, resume_profile, overall_score)
            
            matched_opp = {
                **opp,
                'match_score': round(overall_score, 1),
                'match_breakdown': {
                    'title_match': round(title_score * 100, 1),
                    'skills_match': round(skills_score * 100, 1),
                    'experience_match': round(experience_score * 100, 1),
                    'location_match': round(location_score * 100, 1),
                    'salary_match': round(salary_score * 100, 1)
                },
                'ai_insights': ai_insights,
                'application_priority': self._calculate_application_priority(overall_score, ai_insights),
                'estimated_competition': self._estimate_competition_level(opp),
                'application_deadline': self._estimate_application_deadline(opp['posted_date'])
            }
            
            matched_opportunities.append(matched_opp)
        
        # Sort by match score descending
        return sorted(matched_opportunities, key=lambda x: x['match_score'], reverse=True)
    
    def _calculate_title_match(self, job_title: str, target_roles: List[str]) -> float:
        """Calculate title match score"""
        if not target_roles:
            return 0.7  # Default moderate match
        
        job_title_lower = job_title.lower()
        max_match = 0
        
        for target in target_roles:
            target_lower = target.lower()
            
            # Exact match
            if target_lower in job_title_lower or job_title_lower in target_lower:
                max_match = max(max_match, 1.0)
            
            # Partial word match
            target_words = set(target_lower.split())
            job_words = set(job_title_lower.split())
            overlap = len(target_words & job_words)
            
            if overlap > 0:
                partial_match = overlap / max(len(target_words), len(job_words))
                max_match = max(max_match, partial_match)
        
        return max_match
    
    def _calculate_skills_match(self, job_requirements: List[str], user_skills: List[str]) -> float:
        """Calculate skills match score"""
        if not user_skills or not job_requirements:
            return 0.5
        
        user_skills_lower = [skill.lower() for skill in user_skills]
        requirements_text = ' '.join(job_requirements).lower()
        
        matched_skills = 0
        for skill in user_skills_lower:
            if skill in requirements_text:
                matched_skills += 1
        
        # Also check for common skill synonyms/variations
        skill_synonyms = {
            'javascript': ['js', 'node.js', 'react', 'angular'],
            'python': ['django', 'flask', 'pandas', 'numpy'],
            'machine learning': ['ml', 'ai', 'deep learning', 'neural networks']
        }
        
        for skill in user_skills_lower:
            if skill in skill_synonyms:
                for synonym in skill_synonyms[skill]:
                    if synonym in requirements_text:
                        matched_skills += 0.5  # Partial credit for related skills
        
        return min(1.0, matched_skills / max(len(user_skills), 5))  # Normalize
    
    def _calculate_experience_match(self, job_seniority: str, user_experience: int) -> float:
        """Calculate experience level match"""
        seniority_requirements = {
            'Entry': (0, 2),
            'Mid': (2, 5),
            'Senior': (5, 8),
            'Lead': (7, 12),
            'Principal': (10, 20)
        }
        
        min_exp, max_exp = seniority_requirements.get(job_seniority, (3, 7))
        
        if min_exp <= user_experience <= max_exp:
            return 1.0
        elif user_experience < min_exp:
            # Under-qualified
            gap = min_exp - user_experience
            return max(0.3, 1.0 - (gap * 0.2))
        else:
            # Over-qualified
            excess = user_experience - max_exp
            return max(0.7, 1.0 - (excess * 0.1))
    
    def _calculate_location_match(self, job_location: str, preferred_locations: List[str]) -> float:
        """Calculate location preference match"""
        if 'Remote' in preferred_locations and ('remote' in job_location.lower() or job_location == 'Remote'):
            return 1.0
        
        for pref_loc in preferred_locations:
            if pref_loc.lower() in job_location.lower():
                return 1.0
        
        # Check for same state/region
        for pref_loc in preferred_locations:
            if len(pref_loc.split(',')) > 1 and len(job_location.split(',')) > 1:
                pref_state = pref_loc.split(',')[-1].strip()
                job_state = job_location.split(',')[-1].strip()
                if pref_state.lower() == job_state.lower():
                    return 0.7
        
        return 0.3  # Different location
    
    def _calculate_salary_match(self, job_salary_range: str, salary_expectations: Dict[str, int]) -> float:
        """Calculate salary alignment score"""
        # Extract salary numbers from range string
        salary_numbers = re.findall(r'\$?(\d{1,3}(?:,\d{3})*)', job_salary_range)
        
        if len(salary_numbers) < 2:
            return 0.7  # Default if can't parse
        
        try:
            job_min = int(salary_numbers[0].replace(',', ''))
            job_max = int(salary_numbers[1].replace(',', ''))
            job_mid = (job_min + job_max) / 2
            
            user_min = salary_expectations.get('min', 75000)
            user_max = salary_expectations.get('max', 120000)
            user_mid = (user_min + user_max) / 2
            
            # Check for overlap
            if job_max >= user_min and job_min <= user_max:
                # Calculate overlap percentage
                overlap_start = max(job_min, user_min)
                overlap_end = min(job_max, user_max)
                overlap_size = overlap_end - overlap_start
                
                job_range_size = job_max - job_min
                user_range_size = user_max - user_min
                
                overlap_ratio = overlap_size / min(job_range_size, user_range_size)
                return min(1.0, overlap_ratio)
            else:
                # No overlap - calculate distance penalty
                if job_max < user_min:
                    gap = user_min - job_max
                    return max(0.2, 1.0 - (gap / user_mid * 2))
                else:
                    gap = job_min - user_max
                    return max(0.8, 1.0 - (gap / user_mid * 0.5))  # Less penalty for higher offers
        
        except:
            return 0.5
    
    def _generate_opportunity_insights(self, opportunity: Dict[str, Any], 
                                     resume_profile: Dict[str, Any], 
                                     match_score: float) -> Dict[str, Any]:
        """
        Generate AI-powered insights for each opportunity
        """
        insights = {
            'strengths': [],
            'concerns': [],
            'recommendations': [],
            'competition_level': 'Medium',
            'application_urgency': 'Normal',
            'career_growth_potential': 'Good'
        }
        
        # Analyze strengths
        if match_score > 85:
            insights['strengths'].append('Excellent overall fit for your profile')
        
        if opportunity['company_size'] == 'Startup':
            insights['strengths'].append('Startup environment offers rapid growth opportunities')
            insights['career_growth_potential'] = 'High'
        
        if 'remote' in opportunity['location'].lower():
            insights['strengths'].append('Remote work flexibility aligns with modern preferences')
        
        # Identify concerns
        posted_days_ago = (datetime.now() - opportunity['posted_date']).days
        if posted_days_ago > 14:
            insights['concerns'].append('Position has been open for a while - may indicate specific requirements')
            insights['application_urgency'] = 'High'
        
        if opportunity['seniority_level'] in ['Lead', 'Principal']:
            insights['concerns'].append('Senior role may require extensive leadership experience')
        
        # Generate recommendations
        if match_score > 80:
            insights['recommendations'].append('High priority application - prepare tailored resume immediately')
        elif match_score > 60:
            insights['recommendations'].append('Good opportunity - research company culture and recent news')
        else:
            insights['recommendations'].append('Consider as backup option or for skill development')
        
        # Estimate competition
        if opportunity['company'] in ['Google', 'Apple', 'Microsoft', 'Meta']:
            insights['competition_level'] = 'Very High'
        elif opportunity['company_size'] == 'Enterprise':
            insights['competition_level'] = 'High'
        elif opportunity['location'] == 'San Francisco' or 'Silicon Valley' in opportunity['location']:
            insights['competition_level'] = 'High'
        
        return insights
    
    def _analyze_market_trends(self, opportunities: List[Dict[str, Any]], 
                             search_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market trends from scraped job data
        """
        if not opportunities:
            return {'error': 'No data available for trend analysis'}
        
        df = pd.DataFrame(opportunities)
        
        # Company size distribution
        company_size_dist = df['company_size'].value_counts().to_dict()
        
        # Salary trend analysis
        salary_trends = self._analyze_salary_trends(df)
        
        # Skills demand analysis
        skills_demand = self._analyze_skills_demand(df)
        
        # Location trends
        location_trends = df['location'].value_counts().head(10).to_dict()
        
        # Remote work trends
        remote_percentage = len(df[df['location'].str.contains('Remote', case=False)]) / len(df) * 100
        
        # Posting velocity (how quickly jobs are being posted)
        posting_velocity = self._calculate_posting_velocity(df)
        
        return {
            'market_health_score': self._calculate_market_health_score(df),
            'company_size_distribution': company_size_dist,
            'salary_trends': salary_trends,
            'skills_demand': skills_demand,
            'location_trends': location_trends,
            'remote_work_percentage': round(remote_percentage, 1),
            'posting_velocity': posting_velocity,
            'market_insights': self._generate_market_insights_text(df, search_criteria)
        }
    
    def _analyze_salary_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze salary trends from job data"""
        salary_data = []
        
        for _, row in df.iterrows():
            salary_range = row.get('salary_range', '')
            if salary_range:
                # Extract salary numbers
                numbers = re.findall(r'\$?(\d{1,3}(?:,\d{3})*)', salary_range)
                if len(numbers) >= 2:
                    try:
                        min_sal = int(numbers[0].replace(',', ''))
                        max_sal = int(numbers[1].replace(',', ''))
                        avg_sal = (min_sal + max_sal) / 2
                        
                        salary_data.append({
                            'company_size': row.get('company_size'),
                            'seniority': row.get('seniority_level'),
                            'location': row.get('location'),
                            'avg_salary': avg_sal,
                            'min_salary': min_sal,
                            'max_salary': max_sal
                        })
                    except:
                        continue
        
        if not salary_data:
            return {'error': 'No salary data available'}
        
        salary_df = pd.DataFrame(salary_data)
        
        return {
            'overall_average': round(salary_df['avg_salary'].mean(), 0),
            'salary_range': {
                'min': round(salary_df['min_salary'].min(), 0),
                'max': round(salary_df['max_salary'].max(), 0)
            },
            'by_seniority': salary_df.groupby('seniority')['avg_salary'].mean().round(0).to_dict(),
            'by_company_size': salary_df.groupby('company_size')['avg_salary'].mean().round(0).to_dict(),
            'salary_distribution_percentiles': {
                '25th': round(salary_df['avg_salary'].quantile(0.25), 0),
                '50th': round(salary_df['avg_salary'].quantile(0.50), 0),
                '75th': round(salary_df['avg_salary'].quantile(0.75), 0),
                '90th': round(salary_df['avg_salary'].quantile(0.90), 0)
            }
        }
    
    def _analyze_skills_demand(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze skills demand from job requirements"""
        all_requirements = []
        for requirements_list in df['requirements']:
            all_requirements.extend(requirements_list)
        
        # Extract common technical skills
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'sql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker',
            'kubernetes', 'machine learning', 'ai', 'data science',
            'git', 'agile', 'scrum', 'rest api', 'microservices'
        ]
        
        skill_demand = {}
        all_text = ' '.join(all_requirements).lower()
        
        for skill in technical_skills:
            count = all_text.count(skill.lower())
            if count > 0:
                skill_demand[skill] = {
                    'mentions': count,
                    'percentage': round(count / len(df) * 100, 1)
                }
        
        # Sort by demand
        sorted_skills = sorted(skill_demand.items(), key=lambda x: x[1]['mentions'], reverse=True)
        
        return {
            'top_skills': dict(sorted_skills[:10]),
            'emerging_skills': self._identify_emerging_skills(all_text),
            'skill_combinations': self._analyze_skill_combinations(df)
        }
    
    def _identify_emerging_skills(self, requirements_text: str) -> List[str]:
        """Identify emerging skills from job requirements"""
        emerging_keywords = [
            'llm', 'gpt', 'langchain', 'vector database', 'mlops',
            'kubernetes', 'istio', 'terraform', 'pulumi', 'rust',
            'golang', 'webassembly', 'edge computing', 'quantum'
        ]
        
        found_emerging = []
        for keyword in emerging_keywords:
            if keyword in requirements_text:
                found_emerging.append(keyword)
        
        return found_emerging
    
    def _analyze_skill_combinations(self, df: pd.DataFrame) -> Dict[str, int]:
        """Analyze common skill combinations"""
        combinations = {}
        
        # Common combinations to look for
        combo_patterns = [
            ['python', 'machine learning'],
            ['react', 'javascript'],
            ['aws', 'docker'],
            ['sql', 'python'],
            ['kubernetes', 'docker']
        ]
        
        for combo in combo_patterns:
            count = 0
            for requirements_list in df['requirements']:
                req_text = ' '.join(requirements_list).lower()
                if all(skill in req_text for skill in combo):
                    count += 1
            
            if count > 0:
                combinations[' + '.join(combo)] = count
        
        return combinations
    
    def _calculate_posting_velocity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate job posting velocity"""
        df['posted_date'] = pd.to_datetime(df['posted_date'])
        
        # Group by day and count postings
        daily_postings = df.groupby(df['posted_date'].dt.date).size()
        
        return {
            'average_daily_postings': round(daily_postings.mean(), 1),
            'peak_posting_day': str(daily_postings.idxmax()) if not daily_postings.empty else 'N/A',
            'trend': 'Increasing' if len(daily_postings) > 1 and daily_postings.iloc[-1] > daily_postings.iloc[0] else 'Stable'
        }
    
    def _calculate_market_health_score(self, df: pd.DataFrame) -> int:
        """Calculate overall market health score"""
        factors = {
            'posting_volume': len(df),
            'recent_postings': len(df[df['posted_date'] >= (datetime.now() - timedelta(days=7))]),
            'salary_competitiveness': 1,  # Would compare against historical data
            'remote_opportunities': len(df[df['location'].str.contains('Remote', case=False)])
        }
        
        # Normalize and weight factors
        volume_score = min(100, factors['posting_volume'] * 2)  # 50+ postings = 100
        recency_score = min(100, factors['recent_postings'] * 10)  # 10+ recent = 100
        remote_score = min(100, factors['remote_opportunities'] * 5)  # 20+ remote = 100
        
        overall_score = (volume_score * 0.4 + recency_score * 0.3 + remote_score * 0.3)
        
        return int(overall_score)
    
    def _generate_market_insights_text(self, df: pd.DataFrame, criteria: Dict[str, Any]) -> List[str]:
        """Generate human-readable market insights"""
        insights = []
        
        # Market activity insight
        if len(df) > 30:
            insights.append(f"Strong job market activity with {len(df)} opportunities found")
        elif len(df) > 15:
            insights.append(f"Moderate job market activity with {len(df)} opportunities")
        else:
            insights.append(f"Limited opportunities found ({len(df)}) - consider broadening search criteria")
        
        # Remote work insight
        remote_pct = len(df[df['location'].str.contains('Remote', case=False)]) / len(df) * 100
        if remote_pct > 40:
            insights.append(f"High remote work availability ({remote_pct:.0f}% of positions)")
        elif remote_pct > 20:
            insights.append(f"Moderate remote work options ({remote_pct:.0f}% of positions)")
        
        # Company size insight
        startup_pct = len(df[df['company_size'] == 'Startup']) / len(df) * 100
        if startup_pct > 30:
            insights.append("Strong startup ecosystem with growth opportunities")
        
        return insights
    
    def create_market_dashboard_visualizations(self, scan_results: Dict[str, Any]) -> List[go.Figure]:
        """Create comprehensive market dashboard visualizations"""
        figures = []
        
        opportunities = scan_results.get('opportunities', [])
        market_trends = scan_results.get('market_trends', {})
        
        if not opportunities:
            return [go.Figure().add_annotation(text="No data available")]
        
        # 1. Opportunity Match Score Distribution
        figures.append(self._create_match_score_distribution(opportunities))
        
        # 2. Salary Analysis Chart
        figures.append(self._create_salary_analysis_chart(opportunities))
        
        # 3. Skills Demand Heatmap
        if 'skills_demand' in market_trends:
            figures.append(self._create_skills_demand_chart(market_trends['skills_demand']))
        
        # 4. Market Trends Timeline
        figures.append(self._create_market_trends_timeline(scan_results))
        
        # 5. Geographic Distribution
        figures.append(self._create_geographic_distribution(opportunities))
        
        return figures
    
    def _create_match_score_distribution(self, opportunities: List[Dict]) -> go.Figure:
        """Create match score distribution chart"""
        scores = [opp['match_score'] for opp in opportunities]
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=scores,
            nbinsx=20,
            marker_color='#3B82F6',
            opacity=0.7
        ))
        
        # Add average line
        avg_score = np.mean(scores)
        fig.add_vline(
            x=avg_score, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Average: {avg_score:.1f}%"
        )
        
        fig.update_layout(
            title='Job Opportunity Match Score Distribution',
            xaxis_title='Match Score (%)',
            yaxis_title='Number of Opportunities',
            height=400
        )
        
        return fig
    
    def _create_salary_analysis_chart(self, opportunities: List[Dict]) -> go.Figure:
        """Create salary analysis visualization"""
        salary_data = []
        
        for opp in opportunities:
            salary_range = opp.get('salary_range', '')
            numbers = re.findall(r'\$?(\d{1,3}(?:,\d{3})*)', salary_range)
            
            if len(numbers) >= 2:
                try:
                    min_sal = int(numbers[0].replace(',', ''))
                    max_sal = int(numbers[1].replace(',', ''))
                    avg_sal = (min_sal + max_sal) / 2
                    
                    salary_data.append({
                        'company_size': opp.get('company_size', 'Unknown'),
                        'seniority': opp.get('seniority_level', 'Unknown'),
                        'avg_salary': avg_sal,
                        'match_score': opp.get('match_score', 0)
                    })
                except:
                    continue
        
        if not salary_data:
            return go.Figure().add_annotation(text="No salary data available")
        
        df = pd.DataFrame(salary_data)
        
        fig = px.scatter(
            df, 
            x='match_score', 
            y='avg_salary',
            color='company_size',
            size='avg_salary',
            hover_data=['seniority'],
            title='Salary vs Match Score Analysis'
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def _create_skills_demand_chart(self, skills_demand: Dict[str, Any]) -> go.Figure:
        """Create skills demand visualization"""
        top_skills = skills_demand.get('top_skills', {})
        
        if not top_skills:
            return go.Figure().add_annotation(text="No skills data available")
        
        skills = list(top_skills.keys())
        percentages = [top_skills[skill]['percentage'] for skill in skills]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=skills,
            x=percentages,
            orientation='h',
            marker_color='#10B981'
        ))
        
        fig.update_layout(
            title='Top Skills in Demand',
            xaxis_title='Percentage of Job Postings (%)',
            yaxis_title='Skills',
            height=400
        )
        
        return fig
    
    def _create_market_trends_timeline(self, scan_results: Dict[str, Any]) -> go.Figure:
        """Create market trends timeline"""
        # Simulate trend data for demo
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        job_volumes = np.random.randint(50, 200, len(dates))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=job_volumes,
            mode='lines+markers',
            name='Job Postings Volume',
            line=dict(color='#8B5CF6', width=3)
        ))
        
        fig.update_layout(
            title='Job Market Activity Timeline',
            xaxis_title='Date',
            yaxis_title='Number of Job Postings',
            height=300
        )
        
        return fig
    
    def _create_geographic_distribution(self, opportunities: List[Dict]) -> go.Figure:
        """Create geographic distribution chart"""
        locations = [opp['location'] for opp in opportunities]
        location_counts = pd.Series(locations).value_counts().head(10)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation='h',
            marker_color='#F59E0B'
        ))
        
        fig.update_layout(
            title='Job Opportunities by Location',
            xaxis_title='Number of Opportunities',
            yaxis_title='Location',
            height=400
        )
        
        return fig
    
    # Additional helper methods
    def _deduplicate_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Remove duplicate opportunities"""
        seen = set()
        unique_opportunities = []
        
        for opp in opportunities:
            # Create unique identifier based on company + title
            identifier = f"{opp['company']}_{opp['title']}".lower()
            if identifier not in seen:
                seen.add(identifier)
                unique_opportunities.append(opp)
        
        return unique_opportunities
    
    def _calculate_application_priority(self, match_score: float, ai_insights: Dict) -> str:
        """Calculate application priority"""
        if match_score > 90:
            return 'Urgent'
        elif match_score > 80:
            return 'High'
        elif match_score > 60:
            return 'Medium'
        else:
            return 'Low'
    
    def _estimate_competition_level(self, opportunity: Dict) -> str:
        """Estimate competition level for opportunity"""
        factors = {
            'company_prestige': opportunity.get('company', '') in ['Google', 'Apple', 'Microsoft'],
            'location_competitiveness': 'San Francisco' in opportunity.get('location', ''),
            'recent_posting': (datetime.now() - opportunity['posted_date']).days < 7
        }
        
        score = sum(factors.values())
        if score >= 2:
            return 'Very High'
        elif score == 1:
            return 'High'
        else:
            return 'Medium'
    
    def _estimate_application_deadline(self, posted_date: datetime) -> Optional[datetime]:
        """Estimate application deadline"""
        # Most job postings are open for 30 days
        return posted_date + timedelta(days=30)
    
    def _create_opportunity_pipeline(self, opportunities: List[Dict]) -> Dict[str, List[Dict]]:
        """Create opportunity pipeline based on priority"""
        pipeline = {
            'urgent': [],
            'high_priority': [],
            'medium_priority': [],
            'research_later': []
        }
        
        for opp in opportunities:
            priority = opp.get('application_priority', 'Medium')
            
            if priority == 'Urgent':
                pipeline['urgent'].append(opp)
            elif priority == 'High':
                pipeline['high_priority'].append(opp)
            elif priority == 'Medium':
                pipeline['medium_priority'].append(opp)
            else:
                pipeline['research_later'].append(opp)
        
        return pipeline
    
    def _generate_action_recommendations(self, opportunities: List[Dict], 
                                       insights: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        high_match_count = len([o for o in opportunities if o['match_score'] > 80])
        
        if high_match_count > 5:
            recommendations.append({
                'category': 'Application Strategy',
                'recommendation': f'You have {high_match_count} high-match opportunities. Prioritize the top 3-5 for immediate application.',
                'action': 'Create tailored resumes for top opportunities within 48 hours',
                'priority': 'High'
            })
        
        market_health = insights.get('market_health_score', 75)
        if market_health > 80:
            recommendations.append({
                'category': 'Market Timing',
                'recommendation': 'Excellent market conditions detected. This is an optimal time for job searching.',
                'action': 'Increase application velocity and consider reaching for stretch positions',
                'priority': 'Medium'
            })
        
        return recommendations
    
    def _generate_market_insights(self, opportunities: List[Dict], 
                                market_trends: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive market insights"""
        return {
            'market_health_score': market_trends.get('market_health_score', 75),
            'opportunity_quality': 'High' if len([o for o in opportunities if o['match_score'] > 70]) > len(opportunities) * 0.3 else 'Medium',
            'competitive_landscape': self._assess_competitive_landscape(opportunities),
            'timing_recommendations': self._generate_timing_recommendations(market_trends),
            'skill_gap_insights': self._analyze_skill_gaps(opportunities, market_trends)
        }
    
    def _assess_competitive_landscape(self, opportunities: List[Dict]) -> str:
        """Assess overall competitive landscape"""
        high_competition_count = len([o for o in opportunities if o.get('estimated_competition') in ['High', 'Very High']])
        
        if high_competition_count > len(opportunities) * 0.6:
            return 'Highly Competitive'
        elif high_competition_count > len(opportunities) * 0.3:
            return 'Moderately Competitive'
        else:
            return 'Favorable'
    
    def _generate_timing_recommendations(self, market_trends: Dict[str, Any]) -> List[str]:
        """Generate timing-related recommendations"""
        recommendations = []
        
        posting_velocity = market_trends.get('posting_velocity', {})
        if posting_velocity.get('trend') == 'Increasing':
            recommendations.append('Market activity is increasing - good time to apply')
        
        remote_pct = market_trends.get('remote_work_percentage', 0)
        if remote_pct > 30:
            recommendations.append('Strong remote work market - leverage location flexibility')
        
        return recommendations
    
    def _analyze_skill_gaps(self, opportunities: List[Dict], 
                          market_trends: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skill gaps from market data"""
        top_skills = market_trends.get('skills_demand', {}).get('top_skills', {})
        
        # This would compare against user's skills in production
        return {
            'most_demanded_skills': list(top_skills.keys())[:5],
            'emerging_opportunities': market_trends.get('skills_demand', {}).get('emerging_skills', []),
            'skill_development_priority': 'High' if len(top_skills) > 10 else 'Medium'
        }