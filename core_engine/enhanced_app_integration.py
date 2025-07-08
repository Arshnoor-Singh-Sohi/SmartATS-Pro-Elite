"""
Simplified integration layer for SmartATS Pro Elite advanced features
This module provides integration points for enhanced features when available
"""

import streamlit as st
from typing import Dict, Any, Optional
import json

class FeatureManager:
    """
    Manages optional enhanced features and graceful fallbacks
    """
    
    def __init__(self):
        self.features = {
            'market_intelligence': False,
            'career_simulator': False,
            'interview_prep': False,
            'personal_brand': False,
            'job_scanner': False,
            'enhanced_analytics': False
        }
        self._check_feature_availability()
    
    def _check_feature_availability(self):
        """Check which enhanced features are available"""
        try:
            from intelligence_modules.market_intelligence_engine import MarketIntelligenceEngine
            self.features['market_intelligence'] = True
        except ImportError:
            pass
        
        try:
            from intelligence_modules.career_simulator import CareerPathSimulator
            self.features['career_simulator'] = True
        except ImportError:
            pass
        
        try:
            from intelligence_modules.interview_preparation_engine import InterviewPreparationEngine
            self.features['interview_prep'] = True
        except ImportError:
            pass
        
        try:
            from smart_components.job_market_scanner import JobMarketScanner
            self.features['job_scanner'] = True
        except ImportError:
            pass
    
    def is_feature_available(self, feature_name: str) -> bool:
        """Check if a specific feature is available"""
        return self.features.get(feature_name, False)
    
    def get_available_features(self) -> Dict[str, bool]:
        """Get dictionary of all available features"""
        return self.features.copy()
    
    def create_feature_navigation(self):
        """Create navigation for available features"""
        st.markdown("### 🚀 Advanced Features")
        
        available_count = sum(self.features.values())
        
        if available_count == 0:
            st.info("🔧 Enhanced features are being loaded. Please check back soon!")
            return
        
        st.markdown(f"✅ {available_count} advanced features available")
        
        # Feature cards
        feature_descriptions = {
            'market_intelligence': {
                'title': '📊 Market Intelligence',
                'description': 'Real-time job market analysis and salary insights'
            },
            'career_simulator': {
                'title': '🔮 Career Simulator', 
                'description': 'AI-powered career path simulation and planning'
            },
            'interview_prep': {
                'title': '🎤 Interview Coach',
                'description': 'Personalized interview preparation and practice'
            },
            'job_scanner': {
                'title': '🌐 Job Scanner',
                'description': 'Automated job opportunity discovery and matching'
            }
        }
        
        cols = st.columns(2)
        col_index = 0
        
        for feature, available in self.features.items():
            if available and feature in feature_descriptions:
                with cols[col_index % 2]:
                    info = feature_descriptions[feature]
                    if st.button(info['title'], use_container_width=True):
                        st.info(f"🚧 {info['title']} - Opening soon!")
                    st.caption(info['description'])
                col_index += 1

class EnhancedAnalysisIntegration:
    """
    Integration layer for enhanced analysis features
    """
    
    def __init__(self):
        self.feature_manager = FeatureManager()
    
    def enhance_analysis_with_market_data(self, analysis: Dict[str, Any], 
                                        industry: str, skills: list) -> Dict[str, Any]:
        """
        Enhance analysis with market intelligence data if available
        """
        if not self.feature_manager.is_feature_available('market_intelligence'):
            return analysis
        
        try:
            from intelligence_modules.market_intelligence_engine import MarketIntelligenceEngine
            market_engine = MarketIntelligenceEngine()
            
            market_insights = market_engine.generate_market_insights(
                industry, 'Mid Level', skills, 'National'
            )
            
            analysis['market_intelligence'] = market_insights
            return analysis
            
        except Exception as e:
            st.warning(f"Market intelligence temporarily unavailable: {str(e)}")
            return analysis
    
    def generate_career_recommendations(self, analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate career recommendations if career simulator is available
        """
        if not self.feature_manager.is_feature_available('career_simulator'):
            return None
        
        try:
            from intelligence_modules.career_simulator import CareerPathSimulator
            career_sim = CareerPathSimulator()
            
            # Simplified career analysis
            recommendations = {
                'next_steps': [
                    'Focus on improving match score above 80%',
                    'Add missing keywords to technical skills',
                    'Quantify achievements with specific metrics'
                ],
                'timeline': '3-6 months for significant improvement',
                'focus_areas': ['Technical Skills', 'ATS Optimization', 'Industry Alignment']
            }
            
            return recommendations
            
        except Exception as e:
            return None
    
    def create_interview_prep_suggestions(self, analysis: Dict[str, Any], 
                                        job_description: str) -> Optional[Dict[str, Any]]:
        """
        Create interview preparation suggestions if available
        """
        if not self.feature_manager.is_feature_available('interview_prep'):
            return None
        
        try:
            # Simplified interview prep suggestions
            suggestions = {
                'key_topics': [
                    'Technical skills mentioned in job description',
                    'Project examples that demonstrate matched keywords',
                    'Questions about company culture and growth'
                ],
                'practice_questions': [
                    'Tell me about your experience with [top matched keyword]',
                    'How do you handle [common industry challenge]?',
                    'Describe a project where you used [relevant skill]'
                ],
                'preparation_tips': [
                    'Review job requirements and prepare specific examples',
                    'Research company recent news and developments',
                    'Practice explaining technical concepts clearly'
                ]
            }
            
            return suggestions
            
        except Exception as e:
            return None

# Global instance for use throughout the application
enhanced_integration = EnhancedAnalysisIntegration()