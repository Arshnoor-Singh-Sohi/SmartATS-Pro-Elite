from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from datetime import datetime
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd

# Import from first project (reliable components)
try:
    from components.pdf_processor import PDFProcessor
    from components.gemini_analyzer import GeminiAnalyzer
    from components.visualizations import VisualizationEngine
    from components.report_generator import ReportGenerator
    from components.ui_components import load_custom_css, create_header, create_sidebar, display_metrics_cards, create_progress_ring
    from utils.session_manager import SessionManager
    from utils.keyword_extractor import KeywordExtractor
    CORE_COMPONENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Core components not available: {e}")
    CORE_COMPONENTS_AVAILABLE = False

# Import analytics tracking modules with correct paths
try:
    from analytics_tracking.performance_dashboard import PerformanceTracker, GoalSettingEngine
    PERFORMANCE_TRACKING_AVAILABLE = True
except ImportError:
    PERFORMANCE_TRACKING_AVAILABLE = False
    print("Performance tracking not available - create analytics_tracking/performance_dashboard.py")

try:
    from analytics_tracking.job_application_tracker import JobApplicationTracker, JobApplication, ApplicationStatus
    JOB_TRACKING_AVAILABLE = True
except ImportError:
    JOB_TRACKING_AVAILABLE = False
    print("Job application tracking not available - create analytics_tracking/job_application_tracker.py")

# Import enhanced core engine modules
try:
    from core_engine.enhanced_gemini_analyzer import EnhancedGeminiAnalyzer
    ENHANCED_ANALYZER_AVAILABLE = True
except ImportError:
    ENHANCED_ANALYZER_AVAILABLE = False
    print("Enhanced analyzer not available - using standard analyzer")

try:
    from core_engine.advanced_visualizations import AdvancedVisualizationEngine
    ADVANCED_VISUALIZATIONS_AVAILABLE = True
except ImportError:
    ADVANCED_VISUALIZATIONS_AVAILABLE = False
    print("Advanced visualizations not available - using standard charts")

try:
    from core_engine.enhanced_app_integration import FeatureManager, EnhancedAnalysisIntegration
    ENHANCED_INTEGRATION_AVAILABLE = True
except ImportError:
    ENHANCED_INTEGRATION_AVAILABLE = False
    print("Enhanced integration not available - using standard features")

# Import ONLY the functional modules (keeping original UI)
try:
    from smart_components.ai_cover_letter_generator import AICoverLetterGenerator, CoverLetterOptimizer, CoverLetterRequest
    from smart_components.intelligent_resume_builder import IntelligentResumeBuilder, ResumeOptimizationEngine
    from smart_components.job_market_scanner import JobMarketScanner, JobOpportunity, MarketTrend
    SMART_COMPONENTS_AVAILABLE = True
except ImportError:
    SMART_COMPONENTS_AVAILABLE = False
    print("Smart components not available")

# Import advanced intelligence modules
try:
    from intelligence_modules.career_simulator import CareerPathSimulator, SalaryNegotiationCoach
    from intelligence_modules.interview_preparation_engine import InterviewPreparationEngine, InterviewAnalytics
    from intelligence_modules.market_intelligence_engine import MarketIntelligenceEngine
    from intelligence_modules.personal_brand_builder import PersonalBrandBuilder
    INTELLIGENCE_MODULES_AVAILABLE = True
except ImportError:
    INTELLIGENCE_MODULES_AVAILABLE = False
    print("Intelligence modules not available")

# PersonalBrandBuilder wrapper to handle missing methods
class PersonalBrandBuilderWrapper:
    """Wrapper for PersonalBrandBuilder with fallback methods"""
    
    def __init__(self):
        if INTELLIGENCE_MODULES_AVAILABLE:
            try:
                self.builder = PersonalBrandBuilder()
            except Exception as e:
                st.warning(f"PersonalBrandBuilder initialization failed: {e}")
                self.builder = None
        else:
            self.builder = None
    
    def create_personal_brand_strategy(self, user_profile: Dict[str, Any], 
                                     career_goals: Dict[str, Any], 
                                     current_presence: Dict[str, Any]) -> Dict[str, Any]:
        """Create personal brand strategy with fallback implementation"""
        if self.builder:
            try:
                # Add missing methods to the builder if they don't exist
                self._patch_missing_methods()
                return self.builder.create_personal_brand_strategy(user_profile, career_goals, current_presence)
            except Exception as e:
                st.warning(f"Personal brand strategy creation failed: {e}")
                return self._create_fallback_brand_strategy(user_profile, career_goals, current_presence)
        else:
            return self._create_fallback_brand_strategy(user_profile, career_goals, current_presence)
    
    def _patch_missing_methods(self):
        """Add missing methods to PersonalBrandBuilder instance"""
        if not hasattr(self.builder, '_define_brand_personality'):
            self.builder._define_brand_personality = self._define_brand_personality.__get__(self.builder)
        
        if not hasattr(self.builder, '_create_messaging_framework'):
            self.builder._create_messaging_framework = self._create_messaging_framework.__get__(self.builder)
        
        if not hasattr(self.builder, '_identify_competitive_differentiation'):
            self.builder._identify_competitive_differentiation = self._identify_competitive_differentiation.__get__(self.builder)
        
        if not hasattr(self.builder, '_select_content_framework'):
            self.builder._select_content_framework = self._select_content_framework.__get__(self.builder)
        
        if not hasattr(self.builder, '_define_content_pillars'):
            self.builder._define_content_pillars = self._define_content_pillars.__get__(self.builder)
        
        if not hasattr(self.builder, '_create_content_calendar_template'):
            self.builder._create_content_calendar_template = self._create_content_calendar_template.__get__(self.builder)
        
        if not hasattr(self.builder, '_generate_content_ideas'):
            self.builder._generate_content_ideas = self._generate_content_ideas.__get__(self.builder)
        
        if not hasattr(self.builder, '_create_posting_strategy'):
            self.builder._create_posting_strategy = self._create_posting_strategy.__get__(self.builder)
        
        if not hasattr(self.builder, '_create_engagement_strategy'):
            self.builder._create_engagement_strategy = self._create_engagement_strategy.__get__(self.builder)
        
        if not hasattr(self.builder, '_create_implementation_roadmap'):
            self.builder._create_implementation_roadmap = self._create_implementation_roadmap.__get__(self.builder)
        
        if not hasattr(self.builder, '_create_brand_guidelines'):
            self.builder._create_brand_guidelines = self._create_brand_guidelines.__get__(self.builder)
        
        if not hasattr(self.builder, '_define_success_metrics'):
            self.builder._define_success_metrics = self._define_success_metrics.__get__(self.builder)
        
        if not hasattr(self.builder, '_analyze_competitive_landscape'):
            self.builder._analyze_competitive_landscape = self._analyze_competitive_landscape.__get__(self.builder)
    
    def _define_brand_personality(self, user_profile: Dict[str, Any], brand_archetype: str) -> Dict[str, Any]:
        """Define brand personality"""
        archetypes = {
            'expert': {
                'traits': ['authoritative', 'knowledgeable', 'reliable'],
                'tone': 'professional and informative',
                'content_style': 'data-driven insights and analysis'
            },
            'mentor': {
                'traits': ['helpful', 'experienced', 'supportive'],
                'tone': 'encouraging and educational',
                'content_style': 'guidance and knowledge sharing'
            },
            'innovator': {
                'traits': ['creative', 'forward-thinking', 'experimental'],
                'tone': 'exciting and visionary',
                'content_style': 'cutting-edge trends and possibilities'
            },
            'connector': {
                'traits': ['collaborative', 'sociable', 'generous'],
                'tone': 'warm and engaging',
                'content_style': 'community building and networking'
            }
        }
        
        personality = archetypes.get(brand_archetype, archetypes['expert'])
        
        # Customize based on user profile
        if user_profile.get('industry') == 'Technology':
            personality['traits'].append('tech-savvy')
        
        return personality
    
    def _create_messaging_framework(self, unique_value_prop: str, target_audience: List[str], brand_personality: Dict[str, Any]) -> Dict[str, Any]:
        """Create messaging framework"""
        return {
            'core_message': unique_value_prop,
            'key_themes': [
                'Professional excellence',
                'Industry expertise',
                'Value creation',
                'Innovation and growth'
            ],
            'tone_guidelines': brand_personality.get('tone', 'professional'),
            'communication_style': brand_personality.get('content_style', 'informative'),
            'target_messaging': {
                audience: f"Helping {audience.lower()} achieve their goals through expertise and innovation"
                for audience in target_audience[:3]
            }
        }
    
    def _identify_competitive_differentiation(self, user_profile: Dict[str, Any]) -> List[str]:
        """Identify competitive differentiation"""
        differentiators = []
        
        skills = user_profile.get('core_skills', [])
        if len(skills) > 3:
            differentiators.append(f"Diverse skill set spanning {', '.join(skills[:3])}")
        
        industry = user_profile.get('industry', 'Technology')
        differentiators.append(f"Deep {industry.lower()} industry expertise")
        
        differentiators.extend([
            "Proven track record of delivering results",
            "Strong analytical and problem-solving abilities",
            "Excellent communication and collaboration skills"
        ])
        
        return differentiators
    
    def _select_content_framework(self, brand_positioning: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Select content framework"""
        archetype = brand_positioning.get('brand_archetype', 'expert')
        
        frameworks = {
            'expert': {
                'focus': 'Industry insights and expertise',
                'content_types': ['analysis', 'predictions', 'best_practices', 'case_studies'],
                'posting_frequency': 'Weekly deep insights',
                'target_audience': 'Industry peers and decision makers'
            },
            'mentor': {
                'focus': 'Teaching and knowledge sharing',
                'content_types': ['tutorials', 'explainers', 'tips', 'resources'],
                'posting_frequency': 'Daily helpful content',
                'target_audience': 'Learners and junior professionals'
            },
            'innovator': {
                'focus': 'Cutting-edge developments and trends',
                'content_types': ['trend_analysis', 'new_technologies', 'experiments'],
                'posting_frequency': 'Bi-weekly innovation updates',
                'target_audience': 'Tech enthusiasts and early adopters'
            },
            'connector': {
                'focus': 'Building professional relationships',
                'content_types': ['introductions', 'collaborations', 'community_building'],
                'posting_frequency': 'Daily engagement',
                'target_audience': 'Broad professional network'
            }
        }
        
        return frameworks.get(archetype, frameworks['expert'])
    
    def _define_content_pillars(self, brand_positioning: Dict[str, Any], user_profile: Dict[str, Any]) -> List[str]:
        """Define content pillars"""
        industry = user_profile.get('industry', 'Technology')
        skills = user_profile.get('core_skills', [])
        
        pillars = [
            f"{industry} Industry Insights",
            "Professional Development",
            "Innovation and Trends"
        ]
        
        if skills:
            pillars.append(f"{skills[0]} Expertise" if skills else "Technical Skills")
        
        pillars.append("Career Growth and Leadership")
        
        return pillars
    
    def _create_content_calendar_template(self, content_framework: Dict[str, Any], content_pillars: List[str]) -> Dict[str, Any]:
        """Create content calendar template"""
        return {
            'weekly_schedule': {
                'Monday': f"Industry insights ({content_pillars[0]})",
                'Wednesday': f"Professional tips ({content_pillars[1]})",
                'Friday': f"Innovation updates ({content_pillars[2]})"
            },
            'monthly_themes': {
                'Week 1': content_pillars[0] if len(content_pillars) > 0 else 'Industry Focus',
                'Week 2': content_pillars[1] if len(content_pillars) > 1 else 'Skills Development',
                'Week 3': content_pillars[2] if len(content_pillars) > 2 else 'Innovation',
                'Week 4': content_pillars[3] if len(content_pillars) > 3 else 'Career Growth'
            },
            'content_types': content_framework.get('content_types', ['posts', 'articles', 'insights'])
        }
    
    def _generate_content_ideas(self, content_pillars: List[str], user_profile: Dict[str, Any]) -> List[str]:
        """Generate content ideas"""
        ideas = []
        
        for pillar in content_pillars:
            ideas.extend([
                f"Share insights about {pillar.lower()}",
                f"Write a case study on {pillar.lower()}",
                f"Create tips for {pillar.lower()}",
                f"Discuss trends in {pillar.lower()}"
            ])
        
        # Add general ideas
        ideas.extend([
            "Share a professional achievement",
            "Write about lessons learned",
            "Post about industry events",
            "Share valuable resources",
            "Engage with thought leaders"
        ])
        
        return ideas[:20]  # Return top 20 ideas
    
    def _create_posting_strategy(self, brand_positioning: Dict[str, Any]) -> Dict[str, Any]:
        """Create posting strategy"""
        return {
            'frequency': {
                'linkedin': '3-5 posts per week',
                'twitter': '1-2 posts per day',
                'blog': '1-2 posts per month'
            },
            'optimal_times': {
                'linkedin': 'Weekdays 8-10 AM, 12-2 PM',
                'twitter': 'Weekdays 9 AM, 1-3 PM',
                'blog': 'Tuesday-Thursday mornings'
            },
            'content_mix': {
                'original_content': '60%',
                'curated_content': '25%',
                'engagement_posts': '15%'
            }
        }
    
    def _create_engagement_strategy(self, brand_positioning: Dict[str, Any]) -> Dict[str, Any]:
        """Create engagement strategy"""
        return {
            'daily_activities': [
                'Respond to comments within 2 hours',
                'Engage with 5-10 posts from network',
                'Share valuable insights in comments'
            ],
            'weekly_activities': [
                'Connect with 10-15 new professionals',
                'Share or comment on industry news',
                'Participate in relevant discussions'
            ],
            'monthly_activities': [
                'Review and optimize content strategy',
                'Analyze engagement metrics',
                'Plan content for next month'
            ]
        }
    
    def _create_implementation_roadmap(self, brand_audit: Dict[str, Any], 
                                     brand_positioning: Dict[str, Any], 
                                     content_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation roadmap"""
        return {
            'phase_1': {
                'duration': '1-2 weeks',
                'objectives': ['Complete profile optimization', 'Define content strategy'],
                'tasks': [
                    'Update LinkedIn headline and summary',
                    'Optimize all social media profiles',
                    'Create content calendar',
                    'Set up monitoring tools'
                ]
            },
            'phase_2': {
                'duration': '2-4 weeks',
                'objectives': ['Launch content strategy', 'Build engagement'],
                'tasks': [
                    'Begin regular posting schedule',
                    'Engage with target audience',
                    'Monitor and adjust strategy',
                    'Track key metrics'
                ]
            },
            'phase_3': {
                'duration': 'Ongoing',
                'objectives': ['Optimize and scale', 'Measure success'],
                'tasks': [
                    'Analyze performance data',
                    'Refine content strategy',
                    'Expand platform presence',
                    'Build thought leadership'
                ]
            }
        }
    
    def _create_brand_guidelines(self, brand_positioning: Dict[str, Any]) -> Dict[str, Any]:
        """Create brand guidelines"""
        return {
            'voice_and_tone': {
                'voice': brand_positioning.get('brand_personality', {}).get('tone', 'Professional'),
                'tone_examples': {
                    'professional': 'Clear, authoritative, and informative',
                    'approachable': 'Friendly, helpful, and accessible',
                    'innovative': 'Forward-thinking, creative, and inspiring'
                }
            },
            'visual_guidelines': {
                'color_palette': ['#2563EB', '#059669', '#DC2626'],
                'typography': 'Clean, modern fonts',
                'imagery_style': 'Professional, high-quality images'
            },
            'content_guidelines': {
                'dos': [
                    'Share valuable insights',
                    'Use professional language',
                    'Include clear call-to-actions',
                    'Engage authentically with others'
                ],
                'donts': [
                    'Share controversial political views',
                    'Use unprofessional language',
                    'Over-promote products/services',
                    'Ignore comments and messages'
                ]
            }
        }
    
    def _define_success_metrics(self, career_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics"""
        return {
            'awareness_metrics': [
                'Profile views',
                'Search appearances',
                'Mention volume',
                'Brand recognition surveys'
            ],
            'engagement_metrics': [
                'Likes, comments, shares',
                'Connection requests',
                'Message volume',
                'Event attendance'
            ],
            'conversion_metrics': [
                'Job opportunities',
                'Speaking invitations',
                'Collaboration requests',
                'Business inquiries'
            ],
            'growth_metrics': [
                'Follower growth rate',
                'Network expansion',
                'Influence score',
                'Industry ranking'
            ]
        }
    
    def _analyze_competitive_landscape(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitive landscape"""
        industry = user_profile.get('industry', 'Technology')
        
        return {
            'key_competitors': [
                f"Senior professionals in {industry}",
                f"{industry} thought leaders",
                f"Consultants in {industry} space"
            ],
            'competitive_advantages': [
                "Unique combination of technical and business skills",
                "Strong track record of delivering results",
                "Excellent communication abilities"
            ],
            'opportunities': [
                f"Growing demand for {industry} expertise",
                "Digital transformation trends",
                "Remote work adoption"
            ],
            'threats': [
                "Increased competition",
                "Rapid technology changes",
                "Market saturation"
            ]
        }
    
    def _create_fallback_brand_strategy(self, user_profile: Dict[str, Any], 
                                      career_goals: Dict[str, Any], 
                                      current_presence: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback brand strategy when PersonalBrandBuilder is not available"""
        return {
            'brand_positioning': {
                'unique_value_proposition': f"Experienced {user_profile.get('professional_title', 'professional')} with expertise in {user_profile.get('industry', 'technology')}",
                'target_audience': career_goals.get('target_audience', ['Industry professionals', 'Hiring managers']),
                'brand_archetype': 'expert',
                'brand_personality': {
                    'traits': ['professional', 'knowledgeable', 'reliable'],
                    'tone': 'professional and informative'
                }
            },
            'content_strategy': {
                'content_pillars': [
                    f"{user_profile.get('industry', 'Technology')} Expertise",
                    "Professional Development",
                    "Industry Insights",
                    "Career Growth"
                ],
                'posting_strategy': {
                    'linkedin': '3-4 posts per week',
                    'focus': 'Industry insights and professional updates'
                }
            },
            'platform_optimizations': {
                'linkedin': {
                    'headline_optimization': f"🚀 {user_profile.get('professional_title', 'Professional')} | Helping organizations achieve their goals",
                    'summary_optimization': f"Experienced {user_profile.get('professional_title', 'professional')} with a passion for driving results and innovation.",
                    'content_strategy': 'Share industry insights and professional achievements regularly'
                }
            },
            'implementation_plan': {
                'week_1': 'Optimize all profile sections',
                'week_2': 'Begin content posting schedule',
                'week_3': 'Engage with target audience',
                'week_4': 'Analyze and adjust strategy'
            }
        }

# Page configuration
st.set_page_config(
    page_title="SmartATS Pro Elite - AI Resume Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check core components availability
if not CORE_COMPONENTS_AVAILABLE:
    st.error("❌ Core components are required but not available. Please ensure all required modules are installed.")
    st.stop()

# Initialize session manager
session = SessionManager()

# Load custom CSS (keeping your original theme)
try:
    load_custom_css()
except Exception as e:
    st.warning(f"Custom CSS loading failed: {e}")

# Initialize components
pdf_processor = PDFProcessor()
gemini_analyzer = GeminiAnalyzer()
viz_engine = VisualizationEngine()
report_gen = ReportGenerator()
keyword_extractor = KeywordExtractor()

# Initialize ONLY the functional components (keeping original UI)
if SMART_COMPONENTS_AVAILABLE:
    cover_letter_generator = AICoverLetterGenerator()
    cover_letter_optimizer = CoverLetterOptimizer()
    resume_builder = IntelligentResumeBuilder()
    resume_optimizer = ResumeOptimizationEngine()
    job_scanner = JobMarketScanner()

# Initialize advanced intelligence modules
if INTELLIGENCE_MODULES_AVAILABLE:
    career_simulator = CareerPathSimulator()
    salary_negotiation_coach = SalaryNegotiationCoach()
    interview_prep_engine = InterviewPreparationEngine()
    interview_analytics = InterviewAnalytics()
    market_intelligence = MarketIntelligenceEngine()

# CareerPathSimulator wrapper to handle missing methods
class CareerPathSimulatorWrapper:
    """Wrapper for CareerPathSimulator with fallback methods"""
    
    def __init__(self):
        if INTELLIGENCE_MODULES_AVAILABLE:
            try:
                self.simulator = CareerPathSimulator()
            except Exception as e:
                st.warning(f"CareerPathSimulator initialization failed: {e}")
                self.simulator = None
        else:
            self.simulator = None
    
    def simulate_career_paths(self, current_profile: Dict[str, Any], career_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate career paths with fallback implementation"""
        if self.simulator:
            try:
                # Add missing methods to the simulator if they don't exist
                self._patch_missing_methods()
                return self.simulator.simulate_career_paths(current_profile, career_goals)
            except Exception as e:
                st.warning(f"Career path simulation failed: {e}")
                return self._create_fallback_simulation(current_profile, career_goals)
        else:
            return self._create_fallback_simulation(current_profile, career_goals)
    
    def create_career_path_visualizations(self, simulation_results: Dict[str, Any]) -> List[go.Figure]:
        """Create career path visualizations with fallback"""
        if self.simulator:
            try:
                self._patch_missing_methods()
                return self.simulator.create_career_path_visualizations(simulation_results)
            except Exception as e:
                st.warning(f"Career visualization creation failed: {e}")
                return self._create_fallback_visualizations(simulation_results)
        else:
            return self._create_fallback_visualizations(simulation_results)
    
    def _patch_missing_methods(self):
        """Add missing methods to CareerPathSimulator instance"""
        if not hasattr(self.simulator, '_identify_success_factors'):
            self.simulator._identify_success_factors = self._identify_success_factors.__get__(self.simulator)
        
        if not hasattr(self.simulator, '_generate_risk_mitigation_strategies'):
            self.simulator._generate_risk_mitigation_strategies = self._generate_risk_mitigation_strategies.__get__(self.simulator)
        
        if not hasattr(self.simulator, '_create_skill_development_chart'):
            self.simulator._create_skill_development_chart = self._create_skill_development_chart.__get__(self.simulator)
        
        if not hasattr(self.simulator, '_create_milestone_timeline'):
            self.simulator._create_milestone_timeline = self._create_milestone_timeline.__get__(self.simulator)
    
    def _identify_success_factors(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Identify key success factors across scenarios"""
        success_factors = []
        
        # Analyze common factors in high-performing scenarios
        high_performing = [s for s in scenarios if s.get('total_salary_growth', 0) > 15]
        
        if high_performing:
            # Skills development factor
            if all(s.get('skill_portfolio_score', 0) > 70 for s in high_performing):
                success_factors.append({
                    'factor': 'Continuous Skill Development',
                    'description': 'Consistent investment in learning and skill building',
                    'impact': 'High',
                    'actionable_steps': 'Dedicate time weekly to learning new skills and technologies'
                })
            
            # Networking factor
            if all(s.get('networking_score', 0) > 70 for s in high_performing):
                success_factors.append({
                    'factor': 'Strategic Networking',
                    'description': 'Building meaningful professional relationships',
                    'impact': 'High',
                    'actionable_steps': 'Attend industry events and maintain active LinkedIn presence'
                })
            
            # Market positioning factor
            success_factors.append({
                'factor': 'Market Awareness',
                'description': 'Understanding industry trends and positioning accordingly',
                'impact': 'Medium',
                'actionable_steps': 'Stay informed about industry developments and emerging opportunities'
            })
        
        # Add general success factors
        success_factors.extend([
            {
                'factor': 'Performance Excellence',
                'description': 'Consistently delivering high-quality results',
                'impact': 'High',
                'actionable_steps': 'Set clear goals and track achievements regularly'
            },
            {
                'factor': 'Leadership Development',
                'description': 'Building leadership and management capabilities',
                'impact': 'Medium',
                'actionable_steps': 'Take on leadership opportunities and mentor others'
            },
            {
                'factor': 'Industry Expertise',
                'description': 'Developing deep knowledge in your field',
                'impact': 'Medium',
                'actionable_steps': 'Stay current with industry best practices and innovations'
            }
        ])
        
        return success_factors[:5]  # Return top 5 factors
    
    def _generate_risk_mitigation_strategies(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        # Analyze risks across scenarios
        high_risk_scenarios = [s for s in scenarios if s.get('scenario_details', {}).get('risk_level') == 'High']
        
        if high_risk_scenarios:
            strategies.append({
                'risk': 'Market Volatility',
                'mitigation': 'Diversify skills and maintain flexible career options',
                'action_plan': 'Develop transferable skills and build network across multiple companies',
                'timeline': 'Ongoing'
            })
            
            strategies.append({
                'risk': 'High Competition',
                'mitigation': 'Build unique value proposition and strong personal brand',
                'action_plan': 'Focus on developing rare skills and documenting achievements',
                'timeline': '6-12 months'
            })
        
        # General risk mitigation strategies
        strategies.extend([
            {
                'risk': 'Economic Downturn',
                'mitigation': 'Build emergency fund and maintain strong professional network',
                'action_plan': 'Save 6-12 months expenses and cultivate relationships across industries',
                'timeline': '12-24 months'
            },
            {
                'risk': 'Skill Obsolescence',
                'mitigation': 'Continuous learning and adaptation to new technologies',
                'action_plan': 'Allocate time weekly for learning and experimenting with new tools',
                'timeline': 'Ongoing'
            },
            {
                'risk': 'Limited Growth Opportunities',
                'mitigation': 'Consider lateral moves and cross-functional experiences',
                'action_plan': 'Explore opportunities in adjacent roles or departments',
                'timeline': '1-2 years'
            }
        ])
        
        return strategies[:4]  # Return top 4 strategies
    
    def _create_skill_development_chart(self, scenarios: List[Dict[str, Any]]) -> go.Figure:
        """Create skill development progression chart"""
        fig = go.Figure()
        
        # Create sample skill development data
        skills = ['Technical Skills', 'Leadership', 'Communication', 'Strategic Thinking', 'Industry Knowledge']
        colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        
        for i, scenario in enumerate(scenarios[:3]):  # Show top 3 scenarios
            scenario_name = scenario.get('scenario_name', f'Scenario {i+1}')
            timeline = scenario.get('scenario_details', {}).get('timeline', 5)
            
            # Generate skill progression data
            skill_values = []
            for j, skill in enumerate(skills):
                # Simulate skill development based on scenario intensity
                intensity = scenario.get('scenario_details', {}).get('skill_development_intensity', 'Moderate')
                base_value = 50 + j * 5  # Starting skill level
                
                if intensity == 'Intensive':
                    growth = 35
                elif intensity == 'Moderate':
                    growth = 25
                elif intensity == 'Focused':
                    growth = 30
                else:  # Gradual
                    growth = 15
                
                final_value = min(100, base_value + growth)
                skill_values.append(final_value)
            
            fig.add_trace(go.Scatterpolar(
                r=skill_values,
                theta=skills,
                fill='toself',
                name=scenario_name,
                line_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            title='Skill Development Progression by Career Path',
            height=500
        )
        
        return fig
    
    def _create_milestone_timeline(self, scenarios: List[Dict[str, Any]]) -> go.Figure:
        """Create career milestone timeline chart"""
        fig = go.Figure()
        
        # Use the optimal scenario for milestone timeline
        if scenarios:
            optimal_scenario = max(scenarios, key=lambda x: x.get('total_salary_growth', 0))
            milestones = optimal_scenario.get('key_milestones', [])
            
            if milestones:
                years = [m.get('year', 0) for m in milestones]
                milestone_texts = [m.get('milestone', f'Year {m.get("year", 0)} milestone') for m in milestones]
                focus_areas = [m.get('focus_area', 'General') for m in milestones]
                
                # Create colors for different focus areas
                focus_color_map = {
                    'Skill Building': '#3B82F6',
                    'Leadership Development': '#10B981',
                    'Strategic Positioning': '#F59E0B',
                    'General': '#6B7280'
                }
                
                colors = [focus_color_map.get(area, '#6B7280') for area in focus_areas]
                
                fig.add_trace(go.Scatter(
                    x=years,
                    y=[1] * len(years),  # All on same horizontal line
                    mode='markers+text',
                    marker=dict(
                        size=30,
                        color=colors,
                        symbol='circle'
                    ),
                    text=milestone_texts,
                    textposition='top center',
                    hovertemplate='<b>Year %{x}</b><br>%{text}<br>Focus: %{customdata}<extra></extra>',
                    customdata=focus_areas,
                    name='Career Milestones'
                ))
                
                # Add connecting line
                fig.add_trace(go.Scatter(
                    x=years,
                    y=[1] * len(years),
                    mode='lines',
                    line=dict(color='gray', width=2, dash='dash'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            fig.update_layout(
                title=f'Career Milestone Timeline - {optimal_scenario.get("scenario_name", "Optimal Path")}',
                xaxis_title='Years',
                yaxis=dict(
                    visible=False,
                    range=[0.5, 1.5]
                ),
                height=300,
                showlegend=True
            )
        else:
            # Empty chart if no scenarios
            fig.add_annotation(
                text="No milestone data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )
            fig.update_layout(title='Career Milestone Timeline', height=300)
        
        return fig
    
    def _create_fallback_simulation(self, current_profile: Dict[str, Any], career_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback career simulation when CareerPathSimulator is not available"""
        current_salary = current_profile.get('current_salary', 75000)
        timeline = career_goals.get('timeline_years', 5)
        industry = current_profile.get('industry', 'Technology')
        
        # Create simplified scenarios
        scenarios = [
            {
                'scenario_name': 'Steady Growth Path',
                'scenario_details': {
                    'timeline': timeline,
                    'risk_level': 'Medium',
                    'skill_development_intensity': 'Moderate',
                    'success_probability': 0.75
                },
                'final_salary': int(current_salary * 1.5),  # 50% growth over timeline
                'total_salary_growth': 50.0,
                'networking_score': 70,
                'skill_portfolio_score': 75,
                'market_positioning': 'Above average positioning',
                'key_milestones': [
                    {'year': 1, 'milestone': 'Complete skill assessment and development plan', 'focus_area': 'Skill Building'},
                    {'year': timeline//2, 'milestone': 'Achieve promotion or role expansion', 'focus_area': 'Leadership Development'},
                    {'year': timeline, 'milestone': 'Reach target career level', 'focus_area': 'Strategic Positioning'}
                ],
                'required_actions': [
                    'Maintain consistent learning schedule',
                    'Build professional network',
                    'Document achievements regularly'
                ],
                'potential_obstacles': [
                    'Market competition',
                    'Skill gap requirements',
                    'Economic uncertainties'
                ]
            },
            {
                'scenario_name': 'Accelerated Growth',
                'scenario_details': {
                    'timeline': max(timeline - 1, 2),
                    'risk_level': 'High',
                    'skill_development_intensity': 'Intensive',
                    'success_probability': 0.60
                },
                'final_salary': int(current_salary * 1.8),  # 80% growth
                'total_salary_growth': 80.0,
                'networking_score': 85,
                'skill_portfolio_score': 85,
                'market_positioning': 'Top 25% of professionals',
                'key_milestones': [
                    {'year': 1, 'milestone': 'Intensive skill development and networking', 'focus_area': 'Skill Building'},
                    {'year': max(timeline - 1, 2), 'milestone': 'Achieve senior-level position', 'focus_area': 'Strategic Positioning'}
                ],
                'required_actions': [
                    'Dedicate 10+ hours/week to skill development',
                    'Pursue advanced certifications',
                    'Build strategic relationships'
                ],
                'potential_obstacles': [
                    'High competition for positions',
                    'Intensive time commitment',
                    'Market volatility'
                ]
            }
        ]
        
        return {
            'scenarios': scenarios,
            'analysis': {
                'comparison': {
                    'salary_comparison': {s['scenario_name']: {'final_salary': s['final_salary'], 'growth_percentage': s['total_salary_growth']} for s in scenarios}
                },
                'rankings': {
                    'highest_salary': scenarios[1]['scenario_name'],
                    'best_risk_adjusted': scenarios[0]['scenario_name'],
                    'fastest_growth': scenarios[1]['scenario_name']
                },
                'optimal_scenario': scenarios[0]  # Default to steady growth
            },
            'recommendations': [
                {
                    'category': 'Recommended Path',
                    'recommendation': 'Focus on steady, sustainable growth with balanced risk',
                    'action': 'Maintain consistent skill development and networking efforts',
                    'timeline': f'{timeline} years'
                },
                {
                    'category': 'Skill Development',
                    'recommendation': f'Prioritize {industry.lower()} industry skills and leadership development',
                    'action': 'Create structured learning plan with quarterly milestones',
                    'timeline': 'Ongoing'
                }
            ],
            'success_factors': self._identify_success_factors(scenarios),
            'risk_mitigation': self._generate_risk_mitigation_strategies(scenarios)
        }
    
    def _create_fallback_visualizations(self, simulation_results: Dict[str, Any]) -> List[go.Figure]:
        """Create fallback visualizations when CareerPathSimulator is not available"""
        scenarios = simulation_results.get('scenarios', [])
        
        figures = []
        
        if scenarios:
            # Salary progression chart
            fig1 = go.Figure()
            for i, scenario in enumerate(scenarios):
                timeline = scenario.get('scenario_details', {}).get('timeline', 5)
                current_salary = 75000  # Default
                final_salary = scenario.get('final_salary', current_salary * 1.5)
                
                # Create progression points
                years = list(range(timeline + 1))
                growth_rate = (final_salary / current_salary) ** (1/timeline) - 1
                salaries = [current_salary * (1 + growth_rate) ** year for year in years]
                
                fig1.add_trace(go.Scatter(
                    x=years,
                    y=salaries,
                    mode='lines+markers',
                    name=scenario.get('scenario_name', f'Scenario {i+1}'),
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
            
            fig1.update_layout(
                title='Career Path Salary Progression',
                xaxis_title='Years',
                yaxis_title='Salary ($)',
                height=400
            )
            figures.append(fig1)
            
            # Risk vs reward chart
            fig2 = go.Figure()
            risk_map = {'Low': 1, 'Medium': 2, 'High': 3}
            
            for scenario in scenarios:
                risk_level = scenario.get('scenario_details', {}).get('risk_level', 'Medium')
                growth = scenario.get('total_salary_growth', 50)
                success_prob = scenario.get('scenario_details', {}).get('success_probability', 0.75)
                
                fig2.add_trace(go.Scatter(
                    x=[risk_map[risk_level]],
                    y=[growth],
                    mode='markers+text',
                    text=[scenario.get('scenario_name', 'Scenario')],
                    textposition='top center',
                    marker=dict(
                        size=success_prob * 100,
                        color=growth,
                        colorscale='viridis'
                    ),
                    name=scenario.get('scenario_name', 'Scenario')
                ))
            
            fig2.update_layout(
                title='Risk vs Reward Analysis',
                xaxis=dict(
                    title='Risk Level',
                    tickvals=[1, 2, 3],
                    ticktext=['Low', 'Medium', 'High']
                ),
                yaxis_title='Salary Growth (%)',
                height=400
            )
            figures.append(fig2)
        
        return figures

# Initialize career simulator with wrapper (always available)
career_simulator = CareerPathSimulatorWrapper()

# SalaryNegotiationCoach wrapper to handle missing methods  
class SalaryNegotiationCoachWrapper:
    """Wrapper for SalaryNegotiationCoach with fallback methods"""
    
    def __init__(self):
        if INTELLIGENCE_MODULES_AVAILABLE:
            try:
                self.coach = SalaryNegotiationCoach()
            except Exception as e:
                st.warning(f"SalaryNegotiationCoach initialization failed: {e}")
                self.coach = None
        else:
            self.coach = None
    
    def create_negotiation_strategy(self, negotiation_context: Dict[str, Any], 
                                  market_data: Dict[str, Any], 
                                  personal_factors: Dict[str, Any]) -> Dict[str, Any]:
        """Create negotiation strategy with fallback implementation"""
        if self.coach:
            try:
                return self.coach.create_negotiation_strategy(negotiation_context, market_data, personal_factors)
            except Exception as e:
                st.warning(f"Negotiation strategy creation failed: {e}")
                return self._create_fallback_strategy(negotiation_context, market_data, personal_factors)
        else:
            return self._create_fallback_strategy(negotiation_context, market_data, personal_factors)
    
    def _create_fallback_strategy(self, negotiation_context: Dict[str, Any], 
                                market_data: Dict[str, Any], 
                                personal_factors: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback negotiation strategy"""
        current_offer = negotiation_context.get('current_offer', 85000)
        target_salary = negotiation_context.get('target_salary', 100000)
        competing_offers = negotiation_context.get('competing_offers', 0)
        
        # Calculate leverage score
        leverage_score = 50  # Base score
        if competing_offers > 0:
            leverage_score += 30
        if target_salary > current_offer:
            leverage_score += 10
        
        leverage_score = min(100, leverage_score)
        
        return {
            'position_analysis': {
                'leverage_score': leverage_score,
                'leverage_factors': [
                    'Market rate analysis' if target_salary > current_offer else 'Competitive offer',
                    'Multiple offers' if competing_offers > 0 else 'Single offer situation',
                    'Professional experience'
                ],
                'market_position': 'Market Rate',
                'negotiation_readiness': 'Moderate',
                'recommended_approach': 'Collaborative and value-focused'
            },
            'recommended_strategy': {
                'primary_strategy': 'value_demonstration',
                'confidence_level': 'Moderate',
                'target_increase': target_salary,
                'negotiation_timeline': '1 week'
            },
            'negotiation_scripts': {
                'opening': f"""
                Thank you for the offer. I'm excited about the opportunity and believe I can make a significant impact in this role. 
                Based on my experience and the value I can bring, I was hoping we could discuss a salary of ${target_salary:,.0f}. 
                Can we explore how we might reach this target?
                """,
                'counter_offer': f"""
                I understand budget considerations. If we can reach ${int(target_salary * 0.95):,.0f}, 
                I'm prepared to accept immediately. This represents a fair compromise given my qualifications.
                """,
                'benefits_focus': """
                I appreciate the base salary offer. Could we explore other aspects of the compensation package 
                that might add value for both of us?
                """
            },
            'objection_handling': {
                'budget_constraints': """
                I understand budget considerations. Could we explore a performance-based increase after 6 months, 
                or perhaps adjust other aspects of the compensation package?
                """,
                'company_policy': """
                I respect company policies. Perhaps we could explore a signing bonus or accelerated review cycle?
                """,
                'experience_concerns': """
                I understand the concern. What I bring is [specific value]. I'm confident I can deliver results quickly 
                and would welcome a performance review after 90 days.
                """
            },
            'success_probability': min(95, max(20, leverage_score + 10))
        }

# Initialize salary negotiation coach with wrapper (always available)  
salary_negotiation_coach = SalaryNegotiationCoachWrapper()

# Initialize PersonalBrandBuilder with wrapper (always available)
personal_brand_builder = PersonalBrandBuilderWrapper()

# Initialize enhanced core engine modules
if ENHANCED_ANALYZER_AVAILABLE:
    enhanced_analyzer = EnhancedGeminiAnalyzer()

if ADVANCED_VISUALIZATIONS_AVAILABLE:
    advanced_viz_engine = AdvancedVisualizationEngine()

if ENHANCED_INTEGRATION_AVAILABLE:
    feature_manager = FeatureManager()
    enhanced_integration = EnhancedAnalysisIntegration()

# Initialize analytics tracking modules
if PERFORMANCE_TRACKING_AVAILABLE:
    performance_tracker = PerformanceTracker()
    goal_engine = GoalSettingEngine()

if JOB_TRACKING_AVAILABLE:
    job_tracker = JobApplicationTracker()

# Enhanced analyzer wrapper (from File 1)
class AnalyzerWrapper:
    """Wrapper to use enhanced analyzer when available, fallback to basic"""
    
    def __init__(self):
        self.basic_analyzer = gemini_analyzer
        self.enhanced_analyzer = enhanced_analyzer if ENHANCED_ANALYZER_AVAILABLE else None
        self.keyword_extractor = keyword_extractor
    
    def analyze_resume(self, resume_text: str, job_description: str, **kwargs) -> Dict[str, Any]:
        # First try enhanced analyzer if available and requested
        if self.enhanced_analyzer and kwargs.get('use_enhanced', False):
            try:
                result = self.enhanced_analyzer.analyze_resume_comprehensive(
                    resume_text, job_description,
                    kwargs.get('industry', 'Technology'),
                    kwargs.get('experience_level', 'Mid Level'),
                    kwargs.get('analysis_depth', 'Standard Analysis')
                )
                # Enhance with keyword analysis
                enhanced_result = self._enhance_with_keywords(result, resume_text, job_description)
                
                # Record analysis session for performance tracking
                if PERFORMANCE_TRACKING_AVAILABLE:
                    session_id = performance_tracker.record_analysis(
                        enhanced_result, resume_text, job_description,
                        kwargs.get('industry', 'Technology'),
                        kwargs.get('experience_level', 'Mid Level')
                    )
                    enhanced_result['session_id'] = session_id
                
                # Apply enhanced integration features if available
                if ENHANCED_INTEGRATION_AVAILABLE:
                    enhanced_result = enhanced_integration.enhance_analysis_with_market_data(
                        enhanced_result, 
                        kwargs.get('industry', 'Technology'),
                        enhanced_result.get('matched_keywords', [])
                    )
                
                return enhanced_result
            except Exception as e:
                st.warning(f"Enhanced analysis failed: {str(e)}, using standard analysis")
        
        # Use basic analyzer - check if it has industry context method
        try:
            # Check if your GeminiAnalyzer has analyze_with_industry_context method
            if hasattr(self.basic_analyzer, 'analyze_with_industry_context'):
                result = self.basic_analyzer.analyze_with_industry_context(
                    resume_text, 
                    job_description,
                    kwargs.get('industry', 'Technology'),
                    kwargs.get('experience_level', 'Mid Level')
                )
            else:
                # Fallback to basic analyze_resume
                result = self.basic_analyzer.analyze_resume(resume_text, job_description)
            
            enhanced_result = self._enhance_with_keywords(result, resume_text, job_description)
            
            # Record analysis session for performance tracking
            if PERFORMANCE_TRACKING_AVAILABLE:
                session_id = performance_tracker.record_analysis(
                    enhanced_result, resume_text, job_description,
                    kwargs.get('industry', 'Technology'),
                    kwargs.get('experience_level', 'Mid Level')
                )
                enhanced_result['session_id'] = session_id
            
            # Apply enhanced integration features if available
            if ENHANCED_INTEGRATION_AVAILABLE:
                enhanced_result = enhanced_integration.enhance_analysis_with_market_data(
                    enhanced_result, 
                    kwargs.get('industry', 'Technology'),
                    enhanced_result.get('matched_keywords', [])
                )
            
            return enhanced_result
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            # Return minimal fallback result
            return self._create_fallback_result(resume_text, job_description)
    
    def _enhance_with_keywords(self, base_result: Dict[str, Any], resume_text: str, job_description: str) -> Dict[str, Any]:
        """Enhance analysis result with keyword extraction"""
        try:
            # Extract keywords using your KeywordExtractor
            resume_keywords = self.keyword_extractor.extract_keywords(resume_text, top_n=30)
            job_keywords = self.keyword_extractor.extract_keywords(job_description, top_n=25)
            
            # Compare keywords
            keyword_comparison = self.keyword_extractor.compare_keywords(resume_keywords, job_keywords)
            
            # Calculate keyword score
            keyword_score, keyword_details = self.keyword_extractor.calculate_keyword_score(resume_text, job_description)
            
            # Extract skills taxonomy
            skills_taxonomy = self.keyword_extractor.extract_skills_taxonomy(resume_text)
            
            # Calculate skills coverage
            skills_coverage = self._calculate_skills_coverage(skills_taxonomy, job_description)
            
            # Enhance the base result
            base_result.update({
                'matched_keywords': keyword_comparison['matched'],
                'missing_keywords': keyword_comparison['missing'],
                'additional_keywords': keyword_comparison['additional'],
                'keyword_score': round(keyword_score, 1),  # Round to 1 decimal
                'keyword_details': keyword_details,
                'skills_taxonomy': skills_taxonomy,
                'skills_coverage': skills_coverage,  # Already rounded in the method
                'important_terms': resume_keywords[:15],  # For word cloud
                'skills_analysis': self._create_skills_analysis(skills_taxonomy)
            })
            
            # Update match percentage if keyword score is available (rounded)
            if keyword_score > 0:
                base_result['match_percentage'] = round(max(base_result.get('match_percentage', 0), keyword_score), 1)
            
            return base_result
            
        except Exception as e:
            st.warning(f"Keyword enhancement failed: {str(e)}")
            return base_result
    
    def _calculate_skills_coverage(self, skills_taxonomy: Dict[str, List[str]], job_description: str) -> float:
        """Calculate skills coverage percentage"""
        try:
            # Extract skills from job description
            job_skills = self.keyword_extractor.extract_skills_taxonomy(job_description)
            
            total_job_skills = sum(len(skills) for skills in job_skills.values())
            total_resume_skills = sum(len(skills) for skills in skills_taxonomy.values())
            
            if total_job_skills == 0:
                return 75.0  # Default if no skills found in job description
            
            # Calculate overlap
            matched_skills = 0
            for category in job_skills:
                job_skills_set = set(job_skills[category])
                resume_skills_set = set(skills_taxonomy.get(category, []))
                matched_skills += len(job_skills_set & resume_skills_set)
            
            coverage = (matched_skills / total_job_skills) * 100 if total_job_skills > 0 else 0
            # Round to 1 decimal place to fix the long decimal issue
            return round(min(100, max(0, coverage)), 1)
            
        except Exception:
            return 60.0  # Default fallback
    
    def _create_skills_analysis(self, skills_taxonomy: Dict[str, List[str]]) -> Dict[str, Any]:
        """Create skills analysis for radar chart"""
        return {
            'Technical Skills': len(skills_taxonomy.get('programming_languages', [])) + len(skills_taxonomy.get('frameworks_libraries', [])),
            'Tools & Technologies': len(skills_taxonomy.get('tools_technologies', [])),
            'Cloud & Databases': len(skills_taxonomy.get('cloud_platforms', [])) + len(skills_taxonomy.get('databases', [])),
            'Methodologies': len(skills_taxonomy.get('methodologies', [])),
            'Overall Score': sum(len(skills) for skills in skills_taxonomy.values())
        }
    
    def _create_fallback_result(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Create fallback result when analysis fails"""
        try:
            # At least extract keywords
            resume_keywords = self.keyword_extractor.extract_keywords(resume_text, top_n=20)
            job_keywords = self.keyword_extractor.extract_keywords(job_description, top_n=15)
            keyword_comparison = self.keyword_extractor.compare_keywords(resume_keywords, job_keywords)
            keyword_score = len(keyword_comparison['matched']) / len(job_keywords) * 100 if job_keywords else 0
            
            return {
                'match_percentage': round(max(30, keyword_score), 1),
                'matched_keywords': keyword_comparison['matched'],
                'missing_keywords': keyword_comparison['missing'],
                'keyword_score': round(keyword_score, 1),
                'skills_coverage': 50.0,
                'ats_friendliness': 'Medium',
                'strengths': ['Resume processed successfully', 'Basic keyword analysis completed'],
                'improvements': ['Add more job-specific keywords', 'Enhance technical skills section'],
                'important_terms': resume_keywords[:10],
                'skills_analysis': {'Technical Skills': 3, 'Experience': 3, 'Education': 2}
            }
        except Exception:
            return {
                'match_percentage': 30.0,
                'matched_keywords': [],
                'missing_keywords': [],
                'skills_coverage': 40.0,
                'ats_friendliness': 'Medium',
                'strengths': ['Resume uploaded successfully'],
                'improvements': ['Complete analysis requires job description'],
                'important_terms': [],
                'skills_analysis': {}
            }

analyzer_wrapper = AnalyzerWrapper()

# Helper function to create feature cards (was missing in original code)
def create_feature_cards():
    """Display feature status cards"""
    st.markdown("### 🚀 Feature Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "✅ Active" if ENHANCED_ANALYZER_AVAILABLE else "⚠️ Loading"
        st.info(f"🧠 **Enhanced AI**\n{status}")
    
    with col2:
        status = "✅ Active" if SMART_COMPONENTS_AVAILABLE else "⚠️ Loading"
        st.info(f"🔨 **Smart Tools**\n{status}")
    
    with col3:
        status = "✅ Active" if INTELLIGENCE_MODULES_AVAILABLE else "⚠️ Loading"
        st.info(f"🎯 **AI Intelligence**\n{status}")
    
    with col4:
        status = "✅ Active" if ADVANCED_VISUALIZATIONS_AVAILABLE else "⚠️ Loading"
        st.info(f"📊 **Advanced Charts**\n{status}")

# Main header (keeping your existing header)
try:
    create_header()
except Exception as e:
    st.title("🎯 SmartATS Pro Elite - AI Resume Optimizer")
    st.warning(f"Header creation failed: {e}")

# Sidebar - properly handle the tuple return from your create_sidebar function
try:
    sidebar_result = create_sidebar()
    if isinstance(sidebar_result, tuple) and len(sidebar_result) >= 4:
        job_description, industry, experience_level, analysis_depth = sidebar_result
    else:
        # Fallback sidebar
        st.sidebar.title("Configuration")
        job_description = st.sidebar.text_area("Job Description", height=200)
        industry = st.sidebar.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Marketing", "Other"])
        experience_level = st.sidebar.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Executive"])
        analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Standard Analysis", "Deep Dive"])
except Exception as e:
    st.sidebar.title("Configuration")
    job_description = st.sidebar.text_area("Job Description", height=200)
    industry = st.sidebar.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Marketing", "Other"])
    experience_level = st.sidebar.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Executive"])
    analysis_depth = st.sidebar.selectbox("Analysis Depth", ["Standard Analysis", "Deep Dive"])
    st.warning(f"Sidebar creation failed: {e}")

# Ensure job_description is a string
if not isinstance(job_description, str):
    job_description = str(job_description) if job_description else ""

# MAIN CONTENT AREA - Enhanced with new features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Resume Analysis", 
    "📝 AI Cover Letter", 
    "🔨 Resume Builder", 
    "📊 Job Market Intel",
    "🎯 Career Dashboard"
])

# TAB 1: RESUME ANALYSIS (Enhanced existing functionality)
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📄 Resume Analysis")
        
        # File upload tabs - combining both versions
        analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs(["📁 Upload PDF", "✏️ Edit Resume", "🔍 Advanced Analysis"])
        
        with analysis_tab1:
            uploaded_file = st.file_uploader(
                "Choose your resume PDF",
                type=['pdf'],
                help="Upload a PDF version of your resume for analysis"
            )
            
            if uploaded_file:
                # Store in session
                session.set('uploaded_file', uploaded_file)
                session.set('file_name', uploaded_file.name)
                
                # Process PDF
                with st.spinner("🔍 Extracting resume content..."):
                    try:
                        resume_text = pdf_processor.extract_text(uploaded_file)
                        
                        if resume_text:
                            session.set('resume_text', resume_text)
                            st.success(f"✅ Successfully processed: {uploaded_file.name}")
                            
                            # Display preview
                            with st.expander("📋 Resume Preview", expanded=False):
                                st.text_area(
                                    "Extracted Content",
                                    resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text,
                                    height=200,
                                    disabled=True
                                )
                        else:
                            st.error("❌ Failed to extract text from PDF")
                    except Exception as e:
                        st.error(f"❌ PDF processing failed: {e}")
        
        with analysis_tab2:
            # Editable resume text area
            resume_text_input = st.text_area(
                "Paste or edit your resume here",
                value=session.get('resume_text', ''),
                height=400,
                help="You can paste your resume text directly or edit the extracted content"
            )
            
            if resume_text_input:
                session.set('resume_text', resume_text_input)
                session.set('is_edited', True)
            
            # Real-time stats
            if resume_text_input:
                char_count = len(resume_text_input)
                word_count = len(resume_text_input.split())
                st.markdown(f"**Stats:** {word_count} words | {char_count} characters")
        
        with analysis_tab3:
            # Advanced resume analysis features
            st.markdown("#### 🔍 Advanced Analysis Tools")
            
            if session.get('resume_text') and job_description and SMART_COMPONENTS_AVAILABLE:
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔬 Deep Resume Analysis", use_container_width=True):
                        with st.spinner("🔬 Performing deep analysis..."):
                            try:
                                analysis_result = resume_builder.analyze_and_optimize_resume(
                                    session.get('resume_text'),
                                    job_description,
                                    industry,
                                    experience_level
                                )
                                
                                session.set('deep_analysis_result', analysis_result)
                                st.success("Deep analysis complete!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Deep analysis failed: {e}")
                
                with col2:
                    if st.button("🎯 A/B Test Versions", use_container_width=True):
                        with st.spinner("🎯 Creating optimized versions..."):
                            try:
                                ab_versions = resume_optimizer.create_multiple_versions(
                                    session.get('resume_text'),
                                    job_description,
                                    industry
                                )
                                
                                session.set('ab_test_versions', ab_versions)
                                st.success("A/B test versions created!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"A/B test creation failed: {e}")
                
                # Display deep analysis results
                if session.get('deep_analysis_result'):
                    st.markdown("#### 📊 Deep Analysis Results")
                    deep_result = session.get('deep_analysis_result')
                    
                    # Show optimization opportunities
                    opportunities = deep_result.get('optimization_opportunities', [])
                    if opportunities:
                        st.markdown("**🎯 Optimization Opportunities:**")
                        for opp in opportunities[:5]:
                            impact_color = "🟢" if opp.get('impact', 0) >= 8 else "🟡" if opp.get('impact', 0) >= 6 else "🔴"
                            st.markdown(f"{impact_color} **{opp.get('category', 'General')}**: {opp.get('description', 'No description')}")
                
                # Display A/B test versions
                if session.get('ab_test_versions'):
                    st.markdown("#### 🧪 A/B Test Versions")
                    versions = session.get('ab_test_versions')
                    
                    for i, version in enumerate(versions):
                        with st.expander(f"📋 {version.get('name', f'Version {i+1}')} - {version.get('focus', 'General')}", expanded=False):
                            st.markdown(f"**Estimated Improvement:** {version.get('estimated_improvement', 'N/A')}")
                            st.text_area(
                                f"Version {i+1} Content", 
                                version.get('content', '')[:500] + "...", 
                                height=200,
                                disabled=True,
                                key=f"version_{i}"
                            )
            elif not SMART_COMPONENTS_AVAILABLE:
                st.info("🔧 Advanced analysis tools are not available. Please install smart_components module.")
            else:
                st.info("💡 Please provide both resume text and job description to enable advanced analysis.")
    
    # RIGHT COLUMN - Action Center (Enhanced)
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        # Enhanced analysis toggle
        use_enhanced = st.checkbox(
            "🚀 Enhanced AI Analysis", 
            value=ENHANCED_ANALYZER_AVAILABLE,
            help="Use advanced AI analysis with comprehensive insights, sentiment analysis, and competitive benchmarking"
        )
        
        if ENHANCED_ANALYZER_AVAILABLE and use_enhanced:
            st.success("🧠 Advanced AI features enabled!")
            
            # Analysis depth selector for enhanced mode
            analysis_depth = st.selectbox(
                "Analysis Depth",
                ["Standard Analysis", "Deep Dive"],
                help="Deep Dive provides comprehensive insights including sentiment analysis, competitive positioning, and success prediction"
            )
        else:
            analysis_depth = "Standard Analysis"
        
        # THE MAIN ANALYZE BUTTON
        if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
            if session.get('resume_text') and job_description:
                with st.spinner("🤖 AI Analysis in Progress..."):
                    start_time = time.time()
                    
                    try:
                        analysis_result = analyzer_wrapper.analyze_resume(
                            session.get('resume_text'),
                            job_description,
                            use_enhanced=use_enhanced,
                            industry=industry,
                            experience_level=experience_level,
                            analysis_depth=analysis_depth
                        )
                        
                        session.set('analysis_result', analysis_result)
                        session.set('analysis_timestamp', datetime.now())
                        
                        analysis_time = time.time() - start_time
                        
                        st.success(f"✅ Analysis Complete! ({analysis_time:.1f}s)")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
            else:
                st.error("Please provide both resume and job description!")
        
        # Re-analyze button
        if st.button("🔄 Rescore Resume", use_container_width=True):
            if session.get('resume_text') and job_description:
                with st.spinner("♻️ Rescoring..."):
                    try:
                        analysis_result = analyzer_wrapper.analyze_resume(
                            session.get('resume_text'),
                            job_description,
                            use_enhanced=use_enhanced,
                            industry=industry,
                            experience_level=experience_level,
                            analysis_depth=analysis_depth
                        )
                        session.set('analysis_result', analysis_result)
                        session.set('rescore_count', session.get('rescore_count', 0) + 1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Rescoring failed: {e}")
        
        # Clear session button
        if st.button("🗑️ Clear Session", use_container_width=True):
            session.clear()
            st.rerun()
        
        # Quick stats
        if session.get('analysis_result'):
            st.markdown("### 📊 Quick Stats")
            analysis = session.get('analysis_result')
            st.metric("Match Score", f"{analysis.get('match_percentage', 0)}%")
            st.metric("Keywords Found", len(analysis.get('matched_keywords', [])))
            st.metric("ATS Rating", analysis.get('ats_friendliness', 'Medium'))
        
        # Enhanced features status
        if ENHANCED_INTEGRATION_AVAILABLE:
            st.markdown("### 🚀 Enhanced Features")
            try:
                feature_status = feature_manager.get_available_features()
                
                available_count = sum(feature_status.values())
                total_features = len(feature_status)
                
                st.metric("Features Active", f"{available_count}/{total_features}")
                
                if available_count > 0:
                    st.success("🎯 Advanced AI features enabled!")
                    
                    # Show feature recommendations if analysis is available
                    if session.get('analysis_result'):
                        try:
                            career_recs = enhanced_integration.generate_career_recommendations(
                                session.get('analysis_result')
                            )
                            
                            if career_recs:
                                with st.expander("💡 Smart Recommendations", expanded=False):
                                    for rec in career_recs.get('next_steps', [])[:3]:
                                        st.markdown(f"• {rec}")
                        except Exception as e:
                            st.warning(f"Career recommendations failed: {e}")
                else:
                    st.info("🔧 Enhanced features loading...")
            except Exception as e:
                st.warning(f"Enhanced features status check failed: {e}")
        
        # Analysis insights for enhanced results
        if session.get('analysis_result'):
            analysis = session.get('analysis_result')
            
            # Show enhanced insights if available
            if analysis.get('success_prediction'):
                st.markdown("### 🎯 Success Prediction")
                success_data = analysis['success_prediction']
                
                st.metric("Success Rate", f"{success_data.get('success_probability', 65)}%")
                st.metric("Interview Likelihood", success_data.get('interview_likelihood', 'Moderate'))
                
                # Key success factors
                factors = success_data.get('key_success_factors', [])
                if factors:
                    st.markdown("**🟢 Success Factors:**")
                    for factor in factors:
                        st.markdown(f"• {factor}")
                
                # Main barriers
                barriers = success_data.get('main_barriers', [])
                if barriers:
                    st.markdown("**🔴 Key Barriers:**")
                    for barrier in barriers:
                        st.markdown(f"• {barrier}")
            
            # Enhanced competitive insights
            if analysis.get('competitive_positioning'):
                comp_data = analysis['competitive_positioning']
                
                st.markdown("### 🏆 Market Position")
                st.metric("Ranking", comp_data.get('estimated_candidate_ranking', 'Top 50%'))
                
                differentiators = comp_data.get('key_differentiators', [])
                if differentiators:
                    st.markdown("**🎯 Key Differentiators:**")
                    for diff in differentiators[:3]:
                        st.markdown(f"• {diff}")
            
            # Show enhanced analysis insights
            if analysis.get('sentiment_analysis'):
                sentiment = analysis['sentiment_analysis']
                
                st.markdown("### 📝 Content Analysis")
                st.metric("Confidence Score", f"{sentiment.get('confidence_score', 75)}/100")
                st.metric("Tone", sentiment.get('overall_tone', 'Professional'))
            
            # Trend analysis insights
            if analysis.get('trend_analysis'):
                trend_data = analysis['trend_analysis']
                
                st.markdown("### 📈 Industry Trends")
                st.metric("Trend Alignment", f"{trend_data.get('trend_alignment_score', 60)}/100")
                
                found_trends = trend_data.get('trending_keywords_found', [])
                if found_trends:
                    st.markdown("**🔥 Trending Skills Found:**")
                    for trend in found_trends[:3]:
                        st.markdown(f"• {trend}")
        
        # Interview prep suggestions
        if ENHANCED_INTEGRATION_AVAILABLE and session.get('analysis_result') and job_description:
            try:
                interview_suggestions = enhanced_integration.create_interview_prep_suggestions(
                    session.get('analysis_result'), job_description
                )
                
                if interview_suggestions:
                    st.markdown("### 🎤 Interview Prep")
                    
                    key_topics = interview_suggestions.get('key_topics', [])
                    if key_topics:
                        st.markdown("**🎯 Key Topics:**")
                        for topic in key_topics[:3]:
                            st.markdown(f"• {topic}")
                    
                    if st.button("📋 Full Interview Prep", use_container_width=True):
                        st.info("💡 Complete interview preparation available in Career Dashboard → Interview Prep tab")
            except Exception as e:
                st.warning(f"Interview prep suggestions failed: {e}")

# TAB 2: AI COVER LETTER GENERATOR (NEW)
with tab2:
    st.markdown("### 📝 AI Cover Letter Generator")
    
    if not SMART_COMPONENTS_AVAILABLE:
        st.error("❌ Smart components are required for this feature. Please install the smart_components module.")
    else:
        if not session.get('analysis_result'):
            st.info("💡 **Tip:** Analyze your resume first to generate personalized cover letters!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Cover letter input form
            st.markdown("#### 📋 Job Information")
            
            cl_col1, cl_col2 = st.columns(2)
            with cl_col1:
                company_name = st.text_input("Company Name", placeholder="e.g., Google, Microsoft")
                position_title = st.text_input("Position Title", placeholder="e.g., Senior Software Engineer")
            
            with cl_col2:
                hiring_manager = st.text_input("Hiring Manager (Optional)", placeholder="e.g., John Smith")
                cover_letter_tone = st.selectbox("Tone", ["Professional", "Creative", "Technical", "Executive"])
            
            cover_letter_length = st.selectbox("Length", ["Concise (200-250 words)", "Standard (250-350 words)", "Detailed (350-450 words)"])
            
            special_requirements = st.text_area(
                "Special Requirements (Optional)",
                placeholder="Any specific points to highlight or requirements to address...",
                height=100
            )
        
        with col2:
            st.markdown("#### ⚡ Generate Cover Letter")
            
            if st.button("✨ Generate Cover Letter", use_container_width=True, type="primary"):
                if company_name and position_title and job_description:
                    if session.get('analysis_result'):
                        with st.spinner("✨ Crafting your cover letter..."):
                            try:
                                # Create cover letter request
                                cl_request = CoverLetterRequest(
                                    company_name=company_name,
                                    position_title=position_title,
                                    hiring_manager_name=hiring_manager,
                                    job_description=job_description,
                                    resume_summary=session.get('resume_text', '')[:500],
                                    industry=industry,
                                    experience_level=experience_level,
                                    tone=cover_letter_tone.lower(),
                                    length=cover_letter_length.split()[0].lower(),
                                    special_requirements=[special_requirements] if special_requirements else []
                                )
                                
                                # Generate cover letter
                                cl_result = cover_letter_generator.generate_cover_letter(
                                    cl_request,
                                    session.get('analysis_result')
                                )
                                
                                session.set('cover_letter_result', cl_result)
                                st.success("✅ Cover letter generated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Cover letter generation failed: {e}")
                    else:
                        st.error("Please analyze your resume first!")
                else:
                    st.error("Please fill in company name, position, and job description!")
            
            if st.button("🎭 Generate Multiple Versions", use_container_width=True):
                if company_name and position_title and session.get('analysis_result'):
                    with st.spinner("🎭 Creating multiple versions..."):
                        try:
                            cl_request = CoverLetterRequest(
                                company_name=company_name,
                                position_title=position_title,
                                hiring_manager_name=hiring_manager,
                                job_description=job_description,
                                resume_summary=session.get('resume_text', '')[:500],
                                industry=industry,
                                experience_level=experience_level,
                                tone=cover_letter_tone.lower(),
                                length=cover_letter_length.split()[0].lower(),
                                special_requirements=[special_requirements] if special_requirements else []
                            )
                            
                            multiple_versions = cover_letter_optimizer.create_multiple_versions(
                                cl_request,
                                session.get('analysis_result')
                            )
                            
                            session.set('cover_letter_versions', multiple_versions)
                            st.success("✅ Multiple versions created!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Multiple versions creation failed: {e}")
        
        # Display cover letter results
        if session.get('cover_letter_result'):
            st.markdown("---")
            st.markdown("### 📄 Generated Cover Letter")
            
            cl_result = session.get('cover_letter_result')
            
            cl_tab1, cl_tab2, cl_tab3 = st.tabs(["📝 Cover Letter", "📊 Analysis", "💡 Suggestions"])
            
            with cl_tab1:
                st.text_area(
                    "Your Generated Cover Letter",
                    cl_result.get('cover_letter', ''),
                    height=400
                )
                
                # Download button
                st.download_button(
                    "📥 Download Cover Letter",
                    cl_result.get('cover_letter', ''),
                    file_name=f"cover_letter_{company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with cl_tab2:
                analysis = cl_result.get('analysis', {})
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Overall Score", f"{analysis.get('overall_score', 0)}/100")
                with col2:
                    st.metric("Word Count", analysis.get('length_analysis', {}).get('word_count', 0))
                with col3:
                    st.metric("Keyword Match", f"{analysis.get('keyword_alignment', {}).get('coverage_percentage', 0)}%")
                with col4:
                    st.metric("ATS Score", f"{analysis.get('ats_compatibility', {}).get('ats_score', 0)}/100")
            
            with cl_tab3:
                suggestions = cl_result.get('optimization_suggestions', [])
                if suggestions:
                    st.markdown("**📈 Optimization Suggestions:**")
                    for suggestion in suggestions:
                        priority_emoji = "🔴" if suggestion.get('priority') == 'High' else "🟡" if suggestion.get('priority') == 'Medium' else "🟢"
                        st.markdown(f"{priority_emoji} **{suggestion.get('category', 'General')}**: {suggestion.get('suggestion', 'No suggestion')}")
        
        # Display multiple versions
        if session.get('cover_letter_versions'):
            st.markdown("---")
            st.markdown("### 🎭 Multiple Cover Letter Versions")
            
            versions = session.get('cover_letter_versions')
            
            for i, version in enumerate(versions):
                with st.expander(f"📋 {version.get('name', f'Version {i+1}')} (Score: {version.get('score', 'N/A')})", expanded=False):
                    st.markdown(f"**Focus:** {version.get('focus', 'General')}")
                    st.text_area(
                        "Cover Letter Content",
                        version.get('letter', ''),
                        height=300,
                        key=f"cl_version_{i}"
                    )

# TAB 3: RESUME BUILDER (NEW)
with tab3:
    st.markdown("### 🔨 Intelligent Resume Builder")
    
    if not SMART_COMPONENTS_AVAILABLE:
        st.error("❌ Smart components are required for this feature. Please install the smart_components module.")
    else:
        builder_tab1, builder_tab2, builder_tab3 = st.tabs(["🆕 Build from Scratch", "🔧 Optimize Existing", "📋 Templates"])
        
        with builder_tab1:
            st.markdown("#### 🆕 Build Resume from Scratch")
            
            # User information form
            col1, col2 = st.columns(2)
            
            with col1:
                user_name = st.text_input("Full Name")
                user_email = st.text_input("Email Address")
                user_phone = st.text_input("Phone Number")
                user_location = st.text_input("Location")
            
            with col2:
                user_linkedin = st.text_input("LinkedIn URL (Optional)")
                user_portfolio = st.text_input("Portfolio/Website (Optional)")
                years_experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=3)
                target_salary = st.text_input("Target Salary Range (Optional)", placeholder="e.g., $80,000 - $120,000")
            
            user_summary = st.text_area(
                "Professional Summary/Objective",
                placeholder="Brief overview of your professional background and career goals...",
                height=100
            )
            
            user_skills = st.text_area(
                "Skills (comma-separated)",
                placeholder="Python, JavaScript, React, AWS, Machine Learning, etc.",
                height=75
            )
            
            user_experience = st.text_area(
                "Work Experience (List your positions)",
                placeholder="Company | Position | Dates | Key achievements...",
                height=150
            )
            
            user_education = st.text_area(
                "Education",
                placeholder="Degree | Institution | Year | Relevant coursework...",
                height=100
            )
            
            template_choice = st.selectbox(
                "Choose Template",
                ["ATS-Optimized", "Tech-Focused", "Executive", "Creative", "Academic"]
            )
            
            if st.button("🔨 Build My Resume", use_container_width=True, type="primary"):
                if user_name and user_email and job_description:
                    with st.spinner("🔨 Building your resume..."):
                        try:
                            user_info = {
                                'name': user_name,
                                'email': user_email,
                                'phone': user_phone,
                                'location': user_location,
                                'linkedin': user_linkedin,
                                'portfolio': user_portfolio,
                                'years_experience': years_experience,
                                'target_salary': target_salary,
                                'summary': user_summary,
                                'skills': [skill.strip() for skill in user_skills.split(',') if skill.strip()],
                                'experience': user_experience,
                                'education': user_education,
                                'industry': industry
                            }
                            
                            built_resume = resume_builder.build_resume_from_scratch(
                                user_info,
                                job_description,
                                template_choice.lower().replace('-', '_')
                            )
                            
                            session.set('built_resume', built_resume)
                            st.success("✅ Resume built successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Resume building failed: {e}")
                else:
                    st.error("Please fill in name, email, and provide a job description!")
        
        with builder_tab2:
            st.markdown("#### 🔧 Optimize Existing Resume")
            
            if session.get('resume_text') and job_description:
                if st.button("🚀 Smart Optimization", use_container_width=True, type="primary"):
                    with st.spinner("🚀 Optimizing your resume..."):
                        try:
                            optimization_result = resume_builder.analyze_and_optimize_resume(
                                session.get('resume_text'),
                                job_description,
                                industry,
                                experience_level
                            )
                            
                            session.set('optimization_result', optimization_result)
                            st.success("✅ Optimization complete!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Resume optimization failed: {e}")
            else:
                st.info("💡 Upload your resume and provide a job description to enable optimization.")
        
        with builder_tab3:
            st.markdown("#### 📋 Resume Templates")
            
            # Display available templates
            templates = {
                'ATS-Optimized': 'Clean, keyword-rich format for corporate roles',
                'Tech-Focused': 'Technical skills and project highlights',
                'Executive': 'Leadership and strategic accomplishments',
                'Creative': 'Balanced design with personality',
                'Academic': 'Research and publication focused'
            }
            
            for template_name, description in templates.items():
                with st.expander(f"📄 {template_name}", expanded=False):
                    st.write(description)
                    if st.button(f"Use {template_name}", key=f"template_{template_name}"):
                        st.session_state['selected_template'] = template_name.lower().replace('-', '_')
                        st.success(f"✅ {template_name} template selected!")
        
        # Display built resume
        if session.get('built_resume'):
            st.markdown("---")
            st.markdown("### 📄 Your Built Resume")
            
            built_resume = session.get('built_resume')
            
            st.text_area(
                "Generated Resume",
                built_resume,
                height=500
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Resume",
                    built_resume,
                    file_name=f"resume_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("📊 Analyze Built Resume", use_container_width=True):
                    # Analyze the built resume
                    session.set('resume_text', built_resume)
                    st.rerun()

# TAB 4: JOB MARKET INTELLIGENCE (NEW)
with tab4:
    st.markdown("### 📊 Job Market Intelligence")
    
    if not SMART_COMPONENTS_AVAILABLE:
        st.error("❌ Smart components are required for this feature. Please install the smart_components module.")
    else:
        market_tab1, market_tab2, market_tab3 = st.tabs(["🔍 Market Scan", "📈 Trends Analysis", "🎯 Opportunities"])
        
        with market_tab1:
            st.markdown("#### 🔍 AI-Powered Market Scan")
            
            # Market scan configuration
            col1, col2 = st.columns(2)
            
            with col1:
                scan_role = st.text_input("Target Role", value="Software Engineer")
                scan_location = st.selectbox("Location", ["Remote", "San Francisco", "New York", "Seattle", "Austin", "Boston"])
                scan_experience = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead", "Executive"])
            
            with col2:
                salary_min = st.number_input("Minimum Salary", value=75000, step=5000)
                salary_max = st.number_input("Maximum Salary", value=150000, step=5000)
                job_type = st.multiselect("Job Type", ["Full-time", "Contract", "Part-time", "Remote"], default=["Full-time"])
            
            if st.button("🚀 Scan Job Market", use_container_width=True, type="primary"):
                with st.spinner("🚀 Scanning job market..."):
                    try:
                        # Create search criteria
                        search_criteria = {
                            'role': scan_role,
                            'location': scan_location,
                            'experience_level': scan_experience,
                            'salary_range': {'min': salary_min, 'max': salary_max},
                            'job_type': job_type,
                            'industry': industry
                        }
                        
                        # Create resume profile for matching
                        resume_profile = {
                            'skills': session.get('analysis_result', {}).get('matched_keywords', []),
                            'years_experience': 3 if 'Mid' in experience_level else 1 if 'Entry' in experience_level else 7,
                            'target_roles': [scan_role],
                            'preferred_locations': [scan_location],
                            'salary_range': {'min': salary_min, 'max': salary_max}
                        }
                        
                        # Perform market scan
                        market_results = job_scanner.scan_job_market(search_criteria, resume_profile)
                        session.set('market_scan_results', market_results)
                        st.success("✅ Market scan complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Market scan failed: {e}")
        
        with market_tab2:
            st.markdown("#### 📈 Market Trends Analysis")
            
            if session.get('market_scan_results'):
                market_results = session.get('market_scan_results')
                
                # Market health score
                market_health = market_results.get('insights', {}).get('market_health_score', 75)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Market Health", f"{market_health}/100")
                with col2:
                    st.metric("Total Opportunities", len(market_results.get('opportunities', [])))
                with col3:
                    high_match = len([o for o in market_results.get('opportunities', []) if o.get('match_score', 0) > 80])
                    st.metric("High Match", high_match)
                with col4:
                    remote_pct = market_results.get('market_trends', {}).get('remote_work_percentage', 0)
                    st.metric("Remote Work %", f"{remote_pct}%")
                
                # Create market visualizations
                try:
                    market_charts = job_scanner.create_market_dashboard_visualizations(market_results)
                    
                    for i, chart in enumerate(market_charts):
                        st.plotly_chart(chart, use_container_width=True)
                except Exception as e:
                    st.info("📊 Market visualizations will be displayed when data is available")
            else:
                st.info("💡 Run a market scan first to see trends analysis!")
        
        with market_tab3:
            st.markdown("#### 🎯 Top Opportunities")
            
            if session.get('market_scan_results'):
                opportunities = session.get('market_scan_results').get('opportunities', [])
                
                if opportunities:
                    # Display top opportunities
                    for i, opp in enumerate(opportunities[:10]):
                        with st.expander(f"🏢 {opp.get('title', 'N/A')} at {opp.get('company', 'N/A')} - {opp.get('match_score', 0)}% match", expanded=False):
                            opp_col1, opp_col2 = st.columns(2)
                            
                            with opp_col1:
                                st.write(f"**Location:** {opp.get('location', 'N/A')}")
                                st.write(f"**Salary:** {opp.get('salary_range', 'N/A')}")
                                st.write(f"**Type:** {opp.get('job_type', 'N/A')}")
                                st.write(f"**Company Size:** {opp.get('company_size', 'N/A')}")
                            
                            with opp_col2:
                                posted_date = opp.get('posted_date')
                                if hasattr(posted_date, 'strftime'):
                                    st.write(f"**Posted:** {posted_date.strftime('%Y-%m-%d')}")
                                else:
                                    st.write(f"**Posted:** {posted_date}")
                                st.write(f"**Source:** {opp.get('source', 'N/A')}")
                                st.write(f"**Competition:** {opp.get('estimated_competition', 'Medium')}")
                                
                                if st.button(f"📋 View Details", key=f"view_{i}"):
                                    st.info("Feature coming soon: Detailed job analysis")
                else:
                    st.info("No opportunities found. Try adjusting your search criteria.")
            else:
                st.info("💡 Run a market scan first to see opportunities!")

# TAB 5: CAREER DASHBOARD (NEW)
with tab5:
    st.markdown("### 🎯 Career Intelligence Dashboard")
    
    dashboard_tab1, dashboard_tab2, dashboard_tab3, dashboard_tab4, dashboard_tab5 = st.tabs([
        "📊 Performance", 
        "🚀 Career Simulation", 
        "🎤 Interview Prep",
        "💰 Salary Negotiation",
        "🌟 Personal Brand"
    ])
        
    with dashboard_tab1:
        # Performance tracking dashboard
        st.markdown("#### 📊 Analysis Performance")
        
        if PERFORMANCE_TRACKING_AVAILABLE and session.get('analysis_result'):
            try:
                # Display performance metrics
                st.info("📊 Performance tracking dashboard will be displayed here")
            except:
                st.info("Performance tracking temporarily unavailable")
        else:
            st.info("💡 Complete a resume analysis to enable performance tracking")
    
    with dashboard_tab2:
        # Career Path Simulation with AI
        st.markdown("#### 🚀 AI Career Path Simulation")
        
        if not INTELLIGENCE_MODULES_AVAILABLE:
            st.warning("⚠️ Career simulation requires intelligence modules. Showing basic career guidance.")
            st.info("💡 **Career Planning Tips:**\n- Set clear short and long-term goals\n- Identify skill gaps and development needs\n- Network within your target industry\n- Consider lateral moves for growth\n- Regularly update your skills")
        elif session.get('analysis_result'):
            # Career simulation input form
            sim_col1, sim_col2 = st.columns(2)
            
            with sim_col1:
                current_salary = st.number_input("Current Salary", value=75000, step=5000)
                target_role = st.text_input("Target Role", placeholder="e.g., Senior Manager, Director")
                timeline_years = st.slider("Timeline (Years)", 1, 10, 5)
            
            with sim_col2:
                risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
                career_focus = st.selectbox("Career Focus", ["Technical Growth", "Management Track", "Entrepreneurial"])
                geographic_mobility = st.selectbox("Geographic Mobility", ["Local Only", "Regional", "National", "International"])
            
            if st.button("🚀 Simulate Career Paths", use_container_width=True):
                with st.spinner("🚀 Simulating career trajectories..."):
                    try:
                        # Prepare career simulation data
                        current_profile = {
                            'industry': industry,
                            'experience_level': experience_level,
                            'current_salary': current_salary,
                            'skills': session.get('analysis_result', {}).get('matched_keywords', [])
                        }
                        
                        career_goals = {
                            'target_role': target_role,
                            'timeline_years': timeline_years,
                            'risk_tolerance': risk_tolerance.lower(),
                            'career_focus': career_focus
                        }
                        
                        # Run career path simulation using wrapper
                        simulation_results = career_simulator.simulate_career_paths(current_profile, career_goals)
                        session.set('career_simulation_results', simulation_results)
                        st.success("✅ Career path simulation complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Career simulation failed: {e}")
            
            # Display career simulation results
            if session.get('career_simulation_results'):
                st.markdown("#### 📈 Career Path Analysis")
                sim_results = session.get('career_simulation_results')
                
                # Show scenario comparison
                scenarios = sim_results.get('scenarios', [])
                if scenarios:
                    st.markdown("**🎯 Career Path Scenarios:**")
                    
                    for scenario in scenarios[:3]:  # Top 3 scenarios
                        with st.expander(f"📊 {scenario.get('scenario_name', 'Scenario')} - {scenario.get('total_salary_growth', 0)}% growth", expanded=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Final Salary", f"${scenario.get('final_salary', 0):,}")
                                st.metric("Total Growth", f"{scenario.get('total_salary_growth', 0)}%")
                                success_prob = scenario.get('scenario_details', {}).get('success_probability', 0.65)
                                st.metric("Success Probability", f"{success_prob*100:.0f}%")
                            
                            with col2:
                                st.markdown("**Key Milestones:**")
                                milestones = scenario.get('key_milestones', [])
                                for milestone in milestones[:3]:
                                    st.markdown(f"• Year {milestone.get('year', 'N/A')}: {milestone.get('milestone', 'N/A')}")
                
                # Career path visualizations
                try:
                    career_charts = career_simulator.create_career_path_visualizations(sim_results)
                    
                    st.markdown("#### 📊 Career Path Analytics")
                    for chart in career_charts:
                        st.plotly_chart(chart, use_container_width=True)
                except Exception as e:
                    st.info("📊 Career visualizations will be displayed when data is available")
                
                # Show recommendations
                recommendations = sim_results.get('recommendations', [])
                if recommendations:
                    st.markdown("#### 💡 Strategic Recommendations")
                    for rec in recommendations:
                        st.info(f"**{rec.get('category', 'General')}**: {rec.get('recommendation', 'N/A')}")
        else:
            st.info("💡 Complete a resume analysis first to enable career path simulation")
    
    with dashboard_tab3:
        # AI Interview Preparation
        st.markdown("#### 🎤 AI Interview Preparation Engine")
        
        if not INTELLIGENCE_MODULES_AVAILABLE:
            st.warning("⚠️ Interview preparation requires intelligence modules. Showing basic interview tips.")
            st.info("💡 **Interview Preparation Tips:**\n- Research the company thoroughly\n- Practice common interview questions\n- Prepare specific examples using STAR method\n- Have questions ready for the interviewer\n- Practice your elevator pitch")
        elif session.get('analysis_result') and job_description:
            if st.button("🎯 Generate Interview Prep Plan", use_container_width=True):
                with st.spinner("🎯 Creating personalized interview preparation..."):
                    try:
                        # Generate comprehensive interview preparation
                        prep_plan = interview_prep_engine.generate_interview_preparation_plan(
                            resume_analysis=session.get('analysis_result'),
                            job_description=job_description,
                            industry=industry,
                            experience_level=experience_level,
                            company_info=""
                        )
                        
                        session.set('interview_prep_plan', prep_plan)
                        st.success("✅ Interview preparation plan ready!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Interview prep plan generation failed: {e}")
            
            # Display interview preparation plan
            if session.get('interview_prep_plan'):
                prep_plan = session.get('interview_prep_plan')
                
                # Interview prep tabs
                prep_tab1, prep_tab2, prep_tab3 = st.tabs(["❓ Likely Questions", "📋 Preparation Strategy", "🎭 Mock Interview"])
                
                with prep_tab1:
                    personalized_questions = prep_plan.get('personalized_questions', {})
                    
                    for category, questions in personalized_questions.items():
                        if questions:
                            st.markdown(f"**{category.replace('_', ' ').title()}:**")
                            for i, q in enumerate(questions[:3]):  # Show top 3 per category
                                question_text = q.get('question', '') if isinstance(q, dict) else str(q)
                                with st.expander(f"Q{i+1}: {question_text[:80]}...", expanded=False):
                                    st.markdown(f"**Question:** {question_text}")
                                    if isinstance(q, dict):
                                        st.markdown(f"**Focus Area:** {q.get('focus_area', 'General')}")
                                        st.markdown(f"**Difficulty:** {q.get('difficulty', 'Medium')}")
                                        st.markdown(f"**Why Likely:** {q.get('why_likely', 'Based on role requirements')}")
                                        
                                        # Key points to address
                                        key_points = q.get('key_points_to_address', [])
                                        if key_points:
                                            st.markdown("**Key Points to Address:**")
                                            for point in key_points:
                                                st.markdown(f"• {point}")
                
                with prep_tab2:
                    strategies = prep_plan.get('preparation_strategies', {})
                    
                    for strategy_name, strategy_data in strategies.items():
                        st.markdown(f"**{strategy_name.replace('_', ' ').title()}:**")
                        st.markdown(strategy_data.get('description', ''))
                        
                        tactics = strategy_data.get('tactics', [])
                        for tactic in tactics:
                            if isinstance(tactic, dict):
                                st.markdown(f"• **{tactic.get('focus', '')}**: {tactic.get('approach', '')}")
                            else:
                                st.markdown(f"• {tactic}")
                
                with prep_tab3:
                    mock_plan = prep_plan.get('mock_interview_plan', {})
                    
                    st.markdown(f"**Duration:** {mock_plan.get('total_duration', '45-60 minutes')}")
                    
                    structure = mock_plan.get('structure', {})
                    for phase_name, phase_data in structure.items():
                        duration = phase_data.get('duration', 'N/A') if isinstance(phase_data, dict) else 'N/A'
                        with st.expander(f"📝 {phase_name.replace('_', ' ').title()} ({duration})", expanded=False):
                            if isinstance(phase_data, dict):
                                st.markdown(f"**Purpose:** {phase_data.get('purpose', '')}")
                                
                                questions = phase_data.get('questions', [])
                                if questions:
                                    st.markdown("**Sample Questions:**")
                                    for q in questions:
                                        if isinstance(q, dict):
                                            st.markdown(f"• {q.get('question', q)}")
                                        else:
                                            st.markdown(f"• {q}")
        else:
            st.info("💡 Complete a resume analysis and provide job description for interview preparation")
    
    with dashboard_tab4:
        # AI Salary Negotiation Coach
        st.markdown("#### 💰 AI Salary Negotiation Coach")
        
        if not INTELLIGENCE_MODULES_AVAILABLE:
            st.warning("⚠️ Salary negotiation coaching requires intelligence modules. Showing basic negotiation tips.")
            st.info("💡 **Salary Negotiation Tips:**\n- Research market rates for your role\n- Document your achievements and value\n- Consider the full compensation package\n- Practice your negotiation pitch\n- Be prepared to walk away if needed")
        else:
            # Negotiation scenario input
            neg_col1, neg_col2 = st.columns(2)
            
            with neg_col1:
                current_offer = st.number_input("Current Offer ($)", value=85000, step=1000)
                target_salary = st.number_input("Target Salary ($)", value=100000, step=1000)
                competing_offers = st.number_input("Competing Offers", value=0, min_value=0, max_value=5)
            
            with neg_col2:
                company_size = st.selectbox("Company Size", ["Startup", "Medium", "Large"])
                urgency_level = st.selectbox("Role Urgency", ["Low", "Medium", "High"])
                years_experience = st.number_input("Years Experience", value=5, min_value=0, max_value=30)
            
            if st.button("💡 Create Negotiation Strategy", use_container_width=True):
                with st.spinner("💡 Crafting negotiation strategy..."):
                    try:
                        # Prepare negotiation context
                        negotiation_context = {
                            'current_offer': current_offer,
                            'target_salary': target_salary,
                            'competing_offers': competing_offers,
                            'company_size': company_size.lower(),
                            'urgency_level': urgency_level.lower(),
                            'industry': industry
                        }
                        
                        # Market data (simplified)
                        market_data = {
                            'median_salary': target_salary * 0.9,
                            'market_range': {'min': target_salary * 0.8, 'max': target_salary * 1.2}
                        }
                        
                        # Personal factors
                        personal_factors = {
                            'years_experience': years_experience,
                            'rare_skills': session.get('analysis_result', {}).get('matched_keywords', [])[:3]
                        }
                        
                        # Generate negotiation strategy using wrapper
                        negotiation_strategy = salary_negotiation_coach.create_negotiation_strategy(
                            negotiation_context, market_data, personal_factors
                        )
                        
                        session.set('negotiation_strategy', negotiation_strategy)
                        st.success("✅ Negotiation strategy ready!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Negotiation strategy creation failed: {e}")
            
            # Display negotiation strategy
            if session.get('negotiation_strategy'):
                strategy = session.get('negotiation_strategy')
                
                # Strategy overview
                position_analysis = strategy.get('position_analysis', {})
                recommended_strategy = strategy.get('recommended_strategy', {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Leverage Score", f"{position_analysis.get('leverage_score', 0)}/100")
                with col2:
                    st.metric("Success Probability", f"{strategy.get('success_probability', 0)}%")
                with col3:
                    st.metric("Recommended Approach", recommended_strategy.get('confidence_level', 'Moderate'))
                
                # Negotiation scripts
                scripts = strategy.get('negotiation_scripts', {})
                if scripts:
                    st.markdown("#### 📝 Negotiation Scripts")
                    
                    for script_type, script_content in scripts.items():
                        with st.expander(f"💬 {script_type.replace('_', ' ').title()}", expanded=False):
                            st.text_area(
                                "Script:",
                                script_content,
                                height=150,
                                disabled=True,
                                key=f"script_{script_type}"
                            )
                
                # Objection handling
                objections = strategy.get('objection_handling', {})
                if objections:
                    st.markdown("#### 🛡️ Objection Responses")
                    
                    for objection, response in objections.items():
                        with st.expander(f"❓ {objection.replace('_', ' ').title()}", expanded=False):
                            st.markdown(f"**Response:** {response}")
    
    with dashboard_tab5:
        # Personal Brand Builder
        st.markdown("#### 🌟 Personal Brand & Professional Presence")
        
        if session.get('analysis_result'):
            # Brand profile input
            brand_col1, brand_col2 = st.columns(2)
            
            with brand_col1:
                professional_title = st.text_input("Professional Title", placeholder="e.g., Senior Software Engineer")
                target_audience = st.multiselect(
                    "Target Audience", 
                    ["Hiring Managers", "Industry Peers", "Potential Clients", "Thought Leaders", "Team Members"],
                    default=["Hiring Managers", "Industry Peers"]
                )
            
            with brand_col2:
                brand_personality = st.multiselect(
                    "Brand Personality",
                    ["Expert", "Mentor", "Innovator", "Connector", "Leader", "Problem Solver"],
                    default=["Expert"]
                )
                preferred_platforms = st.multiselect(
                    "Preferred Platforms",
                    ["LinkedIn", "GitHub", "Twitter", "Personal Website", "Medium"],
                    default=["LinkedIn"]
                )
            
            unique_value_prop = st.text_area(
                "Unique Value Proposition",
                placeholder="What makes you unique in your field?",
                height=100
            )
            
            if st.button("🌟 Build Personal Brand Strategy", use_container_width=True):
                with st.spinner("🌟 Creating personal brand strategy..."):
                    try:
                        # Prepare brand building data
                        user_profile = {
                            'professional_title': professional_title,
                            'industry': industry,
                            'core_skills': session.get('analysis_result', {}).get('matched_keywords', []),
                            'experience_level': experience_level,
                            'unique_value_proposition': unique_value_prop
                        }
                        
                        career_goals = {
                            'target_audience': target_audience,
                            'brand_personality': brand_personality,
                            'preferred_platforms': preferred_platforms
                        }
                        
                        # Current presence (simulated)
                        current_presence = {
                            platform.lower(): {
                                'profile_completeness': 60,
                                'posting_frequency': 2,
                                'engagement_rate': 15
                            } for platform in preferred_platforms
                        }
                        
                        # Generate brand strategy using wrapper
                        brand_strategy = personal_brand_builder.create_personal_brand_strategy(
                            user_profile, career_goals, current_presence
                        )
                        
                        session.set('brand_strategy', brand_strategy)
                        st.success("✅ Personal brand strategy created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Personal brand strategy creation failed: {e}")
            
            # Display brand strategy
            if session.get('brand_strategy'):
                brand_strategy = session.get('brand_strategy')
                
                # Brand strategy tabs
                brand_tab1, brand_tab2, brand_tab3 = st.tabs(["🎯 Brand Positioning", "📄 Content Strategy", "📊 Implementation"])
                
                with brand_tab1:
                    positioning = brand_strategy.get('brand_positioning', {})
                    
                    st.markdown("**🎯 Your Brand Positioning:**")
                    st.info(positioning.get('unique_value_proposition', 'Your unique value in the market'))
                    
                    st.markdown("**👥 Target Audience:**")
                    audience = positioning.get('target_audience', [])
                    for aud in audience:
                        st.markdown(f"• {aud}")
                    
                    st.markdown("**🎭 Brand Archetype:**")
                    archetype = positioning.get('brand_archetype', 'expert')
                    st.markdown(f"**{archetype.title()}** - Professional who demonstrates expertise and authority")
                
                with brand_tab2:
                    content_strategy = brand_strategy.get('content_strategy', {})
                    
                    # Content pillars
                    pillars = content_strategy.get('content_pillars', [])
                    if pillars:
                        st.markdown("**📚 Content Pillars:**")
                        for pillar in pillars:
                            st.markdown(f"• {pillar}")
                    
                    # Content ideas
                    ideas = content_strategy.get('content_ideas', [])
                    if ideas:
                        st.markdown("**💡 Content Ideas:**")
                        for idea in ideas[:5]:
                            st.markdown(f"• {idea}")
                
                with brand_tab3:
                    implementation = brand_strategy.get('implementation_plan', {})
                    
                    st.markdown("**📋 Implementation Roadmap:**")
                    if isinstance(implementation, dict):
                        for phase, details in implementation.items():
                            if isinstance(details, dict):
                                st.markdown(f"**{phase.replace('_', ' ').title()}** ({details.get('duration', 'TBD')})")
                                objectives = details.get('objectives', [])
                                for obj in objectives:
                                    st.markdown(f"  • {obj}")
                            else:
                                st.markdown(f"**{phase.replace('_', ' ').title()}**: {details}")
                    else:
                        st.info("1. Optimize profile completeness\n2. Develop content calendar\n3. Engage with target audience\n4. Monitor and adjust strategy")
                    
                    # Platform optimizations
                    optimizations = brand_strategy.get('platform_optimizations', {})
                    if optimizations:
                        st.markdown("**📱 Platform Optimizations:**")
                        for platform, opt_data in optimizations.items():
                            with st.expander(f"📱 {platform.title()} Optimization", expanded=False):
                                st.markdown("**Key Recommendations:**")
                                if isinstance(opt_data, dict):
                                    for key, value in opt_data.items():
                                        if isinstance(value, str):
                                            st.markdown(f"• **{key.replace('_', ' ').title()}**: {value}")
                                        elif isinstance(value, dict):
                                            st.markdown(f"• **{key.replace('_', ' ').title()}**:")
                                            for sub_key, sub_value in value.items():
                                                if isinstance(sub_value, str):
                                                    st.markdown(f"  - {sub_key}: {sub_value}")
        else:
            st.info("💡 Complete a resume analysis first to enable personal brand building")

# RESULTS SECTION - Enhanced with new metrics dashboard
if session.get('analysis_result'):
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    analysis = session.get('analysis_result')
    
    # Enhanced metrics or basic metrics
    try:
        display_metrics_cards(analysis)  # Use your existing function
    except Exception as e:
        # Fallback metrics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Match Score", f"{analysis.get('match_percentage', 0)}%")
        with col2:
            st.metric("Keywords Found", len(analysis.get('matched_keywords', [])))
        with col3:
            st.metric("ATS Rating", analysis.get('ats_friendliness', 'Medium'))
        with col4:
            st.metric("Skills Coverage", f"{analysis.get('skills_coverage', 0)}%")
    
    # Feature cards showcase
    create_feature_cards()
    
    # Visualizations - keeping the comprehensive version
    st.markdown("### 📈 Interactive Analytics")
    
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "🎯 Keyword Analysis",
        "💼 Skills Coverage",
        "☁️ Word Cloud",
        "📊 Detailed Breakdown"
    ])
    
    with viz_tab1:
        # Keyword matching visualization
        try:
            fig_keywords = viz_engine.create_keyword_chart(
                analysis.get('matched_keywords', []),
                analysis.get('missing_keywords', [])
            )
            st.plotly_chart(fig_keywords, use_container_width=True)
        except Exception as e:
            st.warning(f"Keyword chart creation failed: {e}")
        
        # Keyword suggestions
        st.markdown("#### 💡 Keyword Optimization Tips")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🟢 Strong Keywords Found:**")
            for kw in analysis.get('matched_keywords', [])[:5]:
                st.markdown(f"- ✓ {kw}")
        
        with col2:
            st.markdown("**🔴 Missing Keywords to Add:**")
            for kw in analysis.get('missing_keywords', [])[:5]:
                st.markdown(f"- ⚠️ {kw}")
    
    with viz_tab2:
        # Skills coverage radar chart
        try:
            fig_skills = viz_engine.create_skills_radar(
                analysis.get('skills_analysis', {})
            )
            st.plotly_chart(fig_skills, use_container_width=True)
        except Exception as e:
            st.warning(f"Skills radar chart creation failed: {e}")
    
    with viz_tab3:
        # Word cloud visualization
        try:
            wordcloud_img = viz_engine.create_word_cloud(
                session.get('resume_text', ''),
                analysis.get('important_terms', [])
            )
            st.image(wordcloud_img, use_column_width=True)
        except Exception as e:
            st.warning(f"Word cloud creation failed: {e}")
    
    with viz_tab4:
        # Detailed breakdown
        try:
            if hasattr(viz_engine, 'create_detailed_breakdown'):
                breakdown_fig = viz_engine.create_detailed_breakdown(analysis)
                st.plotly_chart(breakdown_fig, use_container_width=True)
            else:
                st.info("Detailed breakdown chart will be available when viz_engine.create_detailed_breakdown is implemented")
        except Exception as e:
            st.warning(f"Detailed breakdown chart creation failed: {e}")
    
    # Recommendations section
    st.markdown("### 🎯 AI-Powered Recommendations")
    
    st.markdown("#### ✅ Strengths")
    for strength in analysis.get('strengths', []):
        st.info(f"💪 {strength}")
    
    st.markdown("#### 📈 Areas for Improvement")
    for improvement in analysis.get('improvements', []):
        st.warning(f"💡 {improvement}")
    
    # Report generation
    st.markdown("### 📄 Generate Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download PDF Report", use_container_width=True):
            try:
                pdf_bytes = report_gen.generate_pdf_report(
                    analysis,
                    session.get('resume_text', ''),
                    job_description
                )
                st.download_button(
                    label="💾 Save PDF Report",
                    data=pdf_bytes,
                    file_name=f"ATS_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF report generation failed: {e}")
    
    with col2:
        if st.button("📊 Download CSV Data", use_container_width=True):
            try:
                csv_data = report_gen.generate_csv_report(analysis)
                st.download_button(
                    label="💾 Save CSV Data",
                    data=csv_data,
                    file_name=f"ATS_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"CSV report generation failed: {e}")
    
    with col3:
        if st.button("📋 Copy Analysis", use_container_width=True):
            try:
                analysis_text = report_gen.generate_text_summary(analysis)
                st.code(analysis_text, language="markdown")
                st.info("📋 Analysis copied to clipboard!")
            except Exception as e:
                st.error(f"Text summary generation failed: {e}")

# Enhanced Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🚀 SmartATS Pro Elite - Built with ❤️ using Streamlit & Google Gemini</p>
        <p style='font-size: 0.8em;'>Next-Generation AI Resume Optimization Platform</p>
        <p style='font-size: 0.7em; opacity: 0.7;'>
            🎯 Resume Analysis • 📝 AI Cover Letters • 🔨 Resume Builder • 📊 Job Market Intel • 🚀 Career Simulation • 🎤 Interview Prep • 💰 Salary Negotiation • 🌟 Personal Brand • 🧠 Enhanced AI • 📈 Advanced Analytics
        </p>
        <p style='font-size: 0.6em; opacity: 0.5; margin-top: 10px;'>
            🧠 Enhanced AI: {"✅ Active" if ENHANCED_ANALYZER_AVAILABLE else "⚠️ Loading"} • 
            📊 Advanced Charts: {"✅ Active" if ADVANCED_VISUALIZATIONS_AVAILABLE else "⚠️ Loading"} • 
            🔗 Smart Integration: {"✅ Active" if ENHANCED_INTEGRATION_AVAILABLE else "⚠️ Loading"}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)