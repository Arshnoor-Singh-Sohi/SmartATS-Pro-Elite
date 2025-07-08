import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import re

class MarketIntelligenceEngine:
    """
    Advanced market intelligence and career insights engine
    """
    
    def __init__(self):
        # Market data (in production, this would come from external APIs)
        self.market_data = {
            'salary_ranges': {
                'Technology': {
                    'Entry Level (0-2 years)': {'min': 65000, 'max': 85000, 'median': 75000},
                    'Mid Level (3-5 years)': {'min': 85000, 'max': 120000, 'median': 102000},
                    'Senior Level (6-10 years)': {'min': 120000, 'max': 180000, 'median': 150000},
                    'Executive (10+ years)': {'min': 180000, 'max': 300000, 'median': 240000}
                },
                'Healthcare': {
                    'Entry Level (0-2 years)': {'min': 55000, 'max': 70000, 'median': 62000},
                    'Mid Level (3-5 years)': {'min': 70000, 'max': 95000, 'median': 82000},
                    'Senior Level (6-10 years)': {'min': 95000, 'max': 140000, 'median': 117000},
                    'Executive (10+ years)': {'min': 140000, 'max': 250000, 'median': 195000}
                },
                'Finance': {
                    'Entry Level (0-2 years)': {'min': 60000, 'max': 80000, 'median': 70000},
                    'Mid Level (3-5 years)': {'min': 80000, 'max': 115000, 'median': 97000},
                    'Senior Level (6-10 years)': {'min': 115000, 'max': 170000, 'median': 142000},
                    'Executive (10+ years)': {'min': 170000, 'max': 350000, 'median': 260000}
                }
            },
            'job_market_trends': {
                'Technology': {
                    'growth_rate': 15.2,
                    'demand_level': 'Very High',
                    'competition_level': 'High',
                    'hot_skills': ['AI/ML', 'Cloud Computing', 'DevOps', 'Cybersecurity', 'Data Science'],
                    'emerging_roles': ['AI Engineer', 'DevOps Architect', 'Cloud Solutions Architect'],
                    'market_outlook': 'Excellent'
                },
                'Healthcare': {
                    'growth_rate': 8.1,
                    'demand_level': 'High',
                    'competition_level': 'Medium',
                    'hot_skills': ['Telemedicine', 'Health Informatics', 'Digital Health', 'Clinical Research'],
                    'emerging_roles': ['Digital Health Specialist', 'Health Data Analyst', 'Telehealth Coordinator'],
                    'market_outlook': 'Strong'
                },
                'Finance': {
                    'growth_rate': 6.5,
                    'demand_level': 'Medium-High',
                    'competition_level': 'High',
                    'hot_skills': ['Fintech', 'Blockchain', 'Risk Analytics', 'Regulatory Compliance'],
                    'emerging_roles': ['Fintech Analyst', 'Blockchain Developer', 'ESG Specialist'],
                    'market_outlook': 'Stable'
                }
            },
            'skill_demand': {
                'Technology': {
                    'python': {'demand_score': 95, 'growth': 12.5, 'salary_premium': 15},
                    'aws': {'demand_score': 92, 'growth': 18.2, 'salary_premium': 20},
                    'react': {'demand_score': 88, 'growth': 10.1, 'salary_premium': 12},
                    'kubernetes': {'demand_score': 85, 'growth': 25.3, 'salary_premium': 25},
                    'machine learning': {'demand_score': 90, 'growth': 22.1, 'salary_premium': 28}
                },
                'Healthcare': {
                    'ehr systems': {'demand_score': 85, 'growth': 8.5, 'salary_premium': 10},
                    'clinical research': {'demand_score': 82, 'growth': 12.2, 'salary_premium': 15},
                    'telehealth': {'demand_score': 88, 'growth': 35.5, 'salary_premium': 18},
                    'health informatics': {'demand_score': 80, 'growth': 15.8, 'salary_premium': 20}
                }
            },
            'geographic_insights': {
                'Technology': {
                    'top_cities': [
                        {'city': 'San Francisco', 'avg_salary': 145000, 'job_count': 12500, 'cost_of_living': 180},
                        {'city': 'Seattle', 'avg_salary': 125000, 'job_count': 8200, 'cost_of_living': 135},
                        {'city': 'New York', 'avg_salary': 120000, 'job_count': 15000, 'cost_of_living': 150},
                        {'city': 'Austin', 'avg_salary': 105000, 'job_count': 6800, 'cost_of_living': 110},
                        {'city': 'Remote', 'avg_salary': 115000, 'job_count': 25000, 'cost_of_living': 100}
                    ]
                }
            }
        }
        
        # Career transition data
        self.transition_data = {
            'common_transitions': {
                'Technology → Finance': {
                    'success_rate': 72,
                    'avg_transition_time': '6-12 months',
                    'key_skills_needed': ['Financial modeling', 'Risk analysis', 'Regulatory knowledge'],
                    'salary_change': '+15%'
                },
                'Finance → Technology': {
                    'success_rate': 68,
                    'avg_transition_time': '8-15 months',
                    'key_skills_needed': ['Programming', 'Data analysis', 'Cloud platforms'],
                    'salary_change': '+25%'
                },
                'Healthcare → Technology': {
                    'success_rate': 65,
                    'avg_transition_time': '10-18 months',
                    'key_skills_needed': ['Health informatics', 'Data analysis', 'Software development'],
                    'salary_change': '+20%'
                }
            }
        }
    
    def generate_market_insights(self, industry: str, experience_level: str, 
                               skills: List[str], location: str = 'National') -> Dict[str, Any]:
        """
        Generate comprehensive market insights for user's profile
        """
        insights = {
            'salary_analysis': self._analyze_salary_prospects(industry, experience_level, skills),
            'market_trends': self._analyze_market_trends(industry),
            'skill_analysis': self._analyze_skill_demand(industry, skills),
            'career_opportunities': self._identify_career_opportunities(industry, experience_level),
            'geographic_insights': self._analyze_geographic_opportunities(industry, location),
            'competitive_landscape': self._analyze_competitive_landscape(industry, experience_level),
            'future_outlook': self._generate_future_outlook(industry, skills)
        }
        
        return insights
    
    def _analyze_salary_prospects(self, industry: str, experience_level: str, 
                                skills: List[str]) -> Dict[str, Any]:
        """
        Analyze salary prospects based on profile
        """
        base_salary_data = self.market_data['salary_ranges'].get(industry, {}).get(experience_level, {})
        
        if not base_salary_data:
            return {'error': 'Insufficient salary data'}
        
        # Calculate skill premium
        skill_premium = 0
        skill_demand_data = self.market_data['skill_demand'].get(industry, {})
        
        for skill in skills:
            skill_lower = skill.lower()
            for market_skill, data in skill_demand_data.items():
                if market_skill in skill_lower or skill_lower in market_skill:
                    skill_premium += data.get('salary_premium', 0)
        
        # Apply premium to base salary
        adjusted_median = base_salary_data['median'] * (1 + skill_premium / 100)
        adjusted_max = base_salary_data['max'] * (1 + skill_premium / 100)
        
        return {
            'base_range': base_salary_data,
            'skill_premium_percentage': skill_premium,
            'adjusted_salary': {
                'min': base_salary_data['min'],
                'max': int(adjusted_max),
                'median': int(adjusted_median)
            },
            'percentile_analysis': self._calculate_salary_percentiles(industry, experience_level),
            'negotiation_insights': self._generate_negotiation_insights(skill_premium)
        }
    
    def _analyze_market_trends(self, industry: str) -> Dict[str, Any]:
        """
        Analyze current market trends for the industry
        """
        trend_data = self.market_data['job_market_trends'].get(industry, {})
        
        if not trend_data:
            return {'error': 'No trend data available'}
        
        # Generate trend predictions
        current_growth = trend_data.get('growth_rate', 5)
        
        return {
            'current_trends': trend_data,
            'growth_forecast': {
                '6_months': round(current_growth * 0.5, 1),
                '1_year': current_growth,
                '2_years': round(current_growth * 1.8, 1)
            },
            'market_signals': self._generate_market_signals(trend_data),
            'timing_recommendations': self._generate_timing_recommendations(trend_data)
        }
    
    def _analyze_skill_demand(self, industry: str, user_skills: List[str]) -> Dict[str, Any]:
        """
        Analyze demand for user's skills
        """
        skill_data = self.market_data['skill_demand'].get(industry, {})
        
        skill_analysis = {
            'high_demand_skills': [],
            'emerging_skills': [],
            'skill_gaps': [],
            'learning_recommendations': []
        }
        
        # Analyze user's current skills
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        for market_skill, data in skill_data.items():
            demand_score = data.get('demand_score', 0)
            growth_rate = data.get('growth', 0)
            
            # Check if user has this skill
            has_skill = any(market_skill in user_skill or user_skill in market_skill 
                          for user_skill in user_skills_lower)
            
            if has_skill:
                if demand_score >= 85:
                    skill_analysis['high_demand_skills'].append({
                        'skill': market_skill,
                        'demand_score': demand_score,
                        'growth': growth_rate,
                        'salary_premium': data.get('salary_premium', 0)
                    })
            else:
                if demand_score >= 80 and growth_rate >= 15:
                    skill_analysis['skill_gaps'].append({
                        'skill': market_skill,
                        'demand_score': demand_score,
                        'growth': growth_rate,
                        'priority': 'High' if demand_score >= 90 else 'Medium'
                    })
                elif growth_rate >= 20:
                    skill_analysis['emerging_skills'].append({
                        'skill': market_skill,
                        'growth': growth_rate,
                        'future_potential': 'High'
                    })
        
        # Generate learning recommendations
        skill_analysis['learning_recommendations'] = self._generate_learning_recommendations(
            skill_analysis['skill_gaps'], skill_analysis['emerging_skills']
        )
        
        return skill_analysis
    
    def _identify_career_opportunities(self, industry: str, experience_level: str) -> Dict[str, Any]:
        """
        Identify career advancement opportunities
        """
        opportunities = {
            'advancement_paths': [],
            'lateral_opportunities': [],
            'transition_possibilities': [],
            'timeline_projections': {}
        }
        
        # Advancement paths based on experience level
        if 'Entry' in experience_level:
            opportunities['advancement_paths'] = [
                {'role': 'Senior Analyst', 'timeline': '2-3 years', 'salary_increase': '25-35%'},
                {'role': 'Team Lead', 'timeline': '3-4 years', 'salary_increase': '35-45%'}
            ]
        elif 'Mid' in experience_level:
            opportunities['advancement_paths'] = [
                {'role': 'Senior Manager', 'timeline': '2-3 years', 'salary_increase': '20-30%'},
                {'role': 'Director', 'timeline': '4-5 years', 'salary_increase': '40-60%'}
            ]
        elif 'Senior' in experience_level:
            opportunities['advancement_paths'] = [
                {'role': 'VP/Executive', 'timeline': '3-5 years', 'salary_increase': '30-50%'},
                {'role': 'C-Level', 'timeline': '5-8 years', 'salary_increase': '60-100%'}
            ]
        
        # Industry transition opportunities
        for transition, data in self.transition_data['common_transitions'].items():
            if transition.startswith(industry):
                opportunities['transition_possibilities'].append({
                    'target_industry': transition.split(' → ')[1],
                    'success_rate': data['success_rate'],
                    'timeline': data['avg_transition_time'],
                    'salary_change': data['salary_change'],
                    'key_skills': data['key_skills_needed']
                })
        
        return opportunities
    
    def _analyze_geographic_opportunities(self, industry: str, current_location: str) -> Dict[str, Any]:
        """
        Analyze geographic opportunities and mobility
        """
        geo_data = self.market_data['geographic_insights'].get(industry, {})
        
        if not geo_data:
            return {'error': 'Limited geographic data'}
        
        top_cities = geo_data.get('top_cities', [])
        
        # Calculate value scores (salary adjusted for cost of living)
        for city in top_cities:
            salary = city['avg_salary']
            col_index = city['cost_of_living']
            city['value_score'] = round((salary / col_index) * 100, 0)
            city['real_salary'] = round(salary * (100 / col_index), 0)
        
        # Sort by value score
        top_cities.sort(key=lambda x: x['value_score'], reverse=True)
        
        return {
            'top_markets': top_cities,
            'remote_opportunities': self._analyze_remote_opportunities(industry),
            'relocation_analysis': self._generate_relocation_analysis(top_cities, current_location),
            'market_recommendations': self._generate_market_recommendations(top_cities)
        }
    
    def _analyze_competitive_landscape(self, industry: str, experience_level: str) -> Dict[str, Any]:
        """
        Analyze competitive landscape for job seekers
        """
        trend_data = self.market_data['job_market_trends'].get(industry, {})
        competition_level = trend_data.get('competition_level', 'Medium')
        
        # Generate competitive insights
        insights = {
            'competition_level': competition_level,
            'market_saturation': self._calculate_market_saturation(industry),
            'differentiation_strategies': self._generate_differentiation_strategies(industry, experience_level),
            'timing_strategies': self._generate_timing_strategies(competition_level),
            'positioning_recommendations': self._generate_positioning_recommendations(industry)
        }
        
        return insights
    
    def _generate_future_outlook(self, industry: str, skills: List[str]) -> Dict[str, Any]:
        """
        Generate future career outlook
        """
        trend_data = self.market_data['job_market_trends'].get(industry, {})
        
        outlook = {
            'industry_forecast': {
                'short_term': self._generate_short_term_forecast(trend_data),
                'medium_term': self._generate_medium_term_forecast(trend_data),
                'long_term': self._generate_long_term_forecast(trend_data)
            },
            'skill_evolution': self._predict_skill_evolution(industry, skills),
            'career_resilience': self._assess_career_resilience(skills),
            'preparation_recommendations': self._generate_preparation_recommendations(industry, skills)
        }
        
        return outlook
    
    def create_market_intelligence_dashboard(self, insights: Dict[str, Any]) -> List[go.Figure]:
        """
        Create comprehensive market intelligence dashboard
        """
        figures = []
        
        # 1. Salary Analysis Chart
        if 'salary_analysis' in insights and 'adjusted_salary' in insights['salary_analysis']:
            figures.append(self._create_salary_analysis_chart(insights['salary_analysis']))
        
        # 2. Market Trends Chart
        if 'market_trends' in insights:
            figures.append(self._create_market_trends_chart(insights['market_trends']))
        
        # 3. Skill Demand Analysis
        if 'skill_analysis' in insights:
            figures.append(self._create_skill_demand_chart(insights['skill_analysis']))
        
        # 4. Geographic Opportunities
        if 'geographic_insights' in insights and 'top_markets' in insights['geographic_insights']:
            figures.append(self._create_geographic_chart(insights['geographic_insights']['top_markets']))
        
        # 5. Career Progression Timeline
        if 'career_opportunities' in insights:
            figures.append(self._create_career_timeline_chart(insights['career_opportunities']))
        
        return figures
    
    def _create_salary_analysis_chart(self, salary_data: Dict[str, Any]) -> go.Figure:
        """
        Create salary analysis visualization
        """
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Salary Range Analysis', 'Skill Premium Impact'),
            specs=[[{"type": "bar"}, {"type": "indicator"}]]
        )
        
        # Salary ranges
        base_range = salary_data['base_range']
        adjusted_range = salary_data['adjusted_salary']
        
        fig.add_trace(
            go.Bar(
                name='Base Range',
                x=['Min', 'Median', 'Max'],
                y=[base_range['min'], base_range['median'], base_range['max']],
                marker_color='#3B82F6'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                name='With Skills Premium',
                x=['Min', 'Median', 'Max'],
                y=[adjusted_range['min'], adjusted_range['median'], adjusted_range['max']],
                marker_color='#10B981'
            ),
            row=1, col=1
        )
        
        # Skill premium indicator
        premium = salary_data.get('skill_premium_percentage', 0)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=premium,
                title={'text': "Skills Premium %"},
                gauge={'axis': {'range': [None, 50]},
                       'bar': {'color': "#F59E0B"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title='Salary Market Analysis',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def _create_market_trends_chart(self, trend_data: Dict[str, Any]) -> go.Figure:
        """
        Create market trends visualization
        """
        if 'growth_forecast' not in trend_data:
            return go.Figure().add_annotation(text="No trend data available")
        
        forecast = trend_data['growth_forecast']
        periods = list(forecast.keys())
        growth_rates = list(forecast.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=periods,
            y=growth_rates,
            mode='lines+markers+text',
            text=[f'{rate}%' for rate in growth_rates],
            textposition='top center',
            line=dict(color='#8B5CF6', width=4),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title='Industry Growth Forecast',
            xaxis_title='Time Period',
            yaxis_title='Growth Rate (%)',
            height=300
        )
        
        return fig
    
    def _create_skill_demand_chart(self, skill_data: Dict[str, Any]) -> go.Figure:
        """
        Create skill demand analysis chart
        """
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('High Demand Skills', 'Skill Gaps to Address')
        )
        
        # High demand skills
        high_demand = skill_data.get('high_demand_skills', [])
        if high_demand:
            skills = [item['skill'] for item in high_demand]
            scores = [item['demand_score'] for item in high_demand]
            
            fig.add_trace(
                go.Bar(x=skills, y=scores, marker_color='#10B981', name='Demand Score'),
                row=1, col=1
            )
        
        # Skill gaps
        gaps = skill_data.get('skill_gaps', [])
        if gaps:
            gap_skills = [item['skill'] for item in gaps]
            gap_scores = [item['demand_score'] for item in gaps]
            
            fig.add_trace(
                go.Bar(x=gap_skills, y=gap_scores, marker_color='#EF4444', name='Missing Skills'),
                row=1, col=2
            )
        
        fig.update_layout(
            title='Skill Demand Analysis',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def _create_geographic_chart(self, geo_data: List[Dict[str, Any]]) -> go.Figure:
        """
        Create geographic opportunities chart
        """
        cities = [item['city'] for item in geo_data]
        salaries = [item['avg_salary'] for item in geo_data]
        value_scores = [item['value_score'] for item in geo_data]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=salaries,
            y=value_scores,
            mode='markers+text',
            text=cities,
            textposition='top center',
            marker=dict(
                size=15,
                color=value_scores,
                colorscale='viridis',
                showscale=True,
                colorbar=dict(title="Value Score")
            )
        ))
        
        fig.update_layout(
            title='Geographic Opportunities Analysis',
            xaxis_title='Average Salary ($)',
            yaxis_title='Value Score (Salary/Cost of Living)',
            height=400
        )
        
        return fig
    
    def _create_career_timeline_chart(self, career_data: Dict[str, Any]) -> go.Figure:
        """
        Create career progression timeline
        """
        advancement_paths = career_data.get('advancement_paths', [])
        
        if not advancement_paths:
            return go.Figure().add_annotation(text="No career path data available")
        
        roles = [path['role'] for path in advancement_paths]
        timelines = [path['timeline'] for path in advancement_paths]
        increases = [path['salary_increase'] for path in advancement_paths]
        
        fig = go.Figure()
        
        # Convert timeline strings to numeric values for plotting
        timeline_values = []
        for timeline in timelines:
            # Extract first number from timeline string
            match = re.search(r'(\d+)', timeline)
            timeline_values.append(int(match.group(1)) if match else 2)
        
        fig.add_trace(go.Scatter(
            x=timeline_values,
            y=list(range(len(roles))),
            mode='markers+text',
            text=[f"{role}<br>{increase}" for role, increase in zip(roles, increases)],
            textposition='middle right',
            marker=dict(size=15, color='#3B82F6')
        ))
        
        fig.update_layout(
            title='Career Advancement Timeline',
            xaxis_title='Years',
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(len(roles))),
                ticktext=roles
            ),
            height=300
        )
        
        return fig
    
    # Helper methods for generating insights
    def _calculate_salary_percentiles(self, industry: str, experience_level: str) -> Dict[str, int]:
        """Calculate salary percentiles"""
        base_data = self.market_data['salary_ranges'].get(industry, {}).get(experience_level, {})
        if not base_data:
            return {}
        
        min_sal, max_sal, median = base_data['min'], base_data['max'], base_data['median']
        
        return {
            '25th_percentile': int(min_sal + (median - min_sal) * 0.5),
            '50th_percentile': median,
            '75th_percentile': int(median + (max_sal - median) * 0.5),
            '90th_percentile': int(max_sal * 0.9)
        }
    
    def _generate_negotiation_insights(self, skill_premium: float) -> List[str]:
        """Generate salary negotiation insights"""
        insights = []
        
        if skill_premium > 20:
            insights.append("Strong negotiating position due to high-demand skills")
            insights.append("Consider asking for top of range or above")
        elif skill_premium > 10:
            insights.append("Moderate leverage for salary negotiation")
            insights.append("Aim for 75th percentile of range")
        else:
            insights.append("Focus on other benefits and growth opportunities")
            insights.append("Build skills to improve negotiating position")
        
        return insights
    
    def _generate_market_signals(self, trend_data: Dict[str, Any]) -> List[str]:
        """Generate market signals and indicators"""
        signals = []
        
        growth_rate = trend_data.get('growth_rate', 0)
        demand_level = trend_data.get('demand_level', 'Medium')
        
        if growth_rate > 10:
            signals.append("🟢 High growth market - excellent timing for career moves")
        elif growth_rate > 5:
            signals.append("🟡 Moderate growth - stable opportunities available")
        else:
            signals.append("🔴 Low growth - focus on differentiation and skills")
        
        if demand_level == 'Very High':
            signals.append("🟢 Very high demand - candidates have strong leverage")
        elif demand_level == 'High':
            signals.append("🟡 High demand - good opportunities for qualified candidates")
        
        return signals
    
    def _generate_timing_recommendations(self, trend_data: Dict[str, Any]) -> List[str]:
        """Generate timing recommendations for job searching"""
        recommendations = []
        
        demand_level = trend_data.get('demand_level', 'Medium')
        competition_level = trend_data.get('competition_level', 'Medium')
        
        if demand_level == 'Very High' and competition_level != 'Very High':
            recommendations.append("Excellent time to make career moves")
            recommendations.append("Consider reaching for stretch positions")
        elif demand_level == 'High':
            recommendations.append("Good timing for job search")
            recommendations.append("Market conditions favor candidates")
        else:
            recommendations.append("Focus on skill building before major moves")
            recommendations.append("Consider internal advancement opportunities")
        
        return recommendations
    
    def _generate_learning_recommendations(self, skill_gaps: List[Dict], 
                                         emerging_skills: List[Dict]) -> List[Dict[str, Any]]:
        """Generate learning and development recommendations"""
        recommendations = []
        
        # Prioritize high-demand gaps
        for gap in skill_gaps[:3]:  # Top 3 gaps
            recommendations.append({
                'skill': gap['skill'],
                'priority': gap['priority'],
                'reason': f"High demand ({gap['demand_score']}/100) with {gap['growth']}% growth",
                'action': 'immediate_learning'
            })
        
        # Add emerging skills for future-proofing
        for skill in emerging_skills[:2]:  # Top 2 emerging
            recommendations.append({
                'skill': skill['skill'],
                'priority': 'Future-focused',
                'reason': f"Emerging skill with {skill['growth']}% growth",
                'action': 'strategic_learning'
            })
        
        return recommendations
    
    def _analyze_remote_opportunities(self, industry: str) -> Dict[str, Any]:
        """Analyze remote work opportunities"""
        # Simulated remote work data
        remote_data = {
            'Technology': {'availability': 85, 'salary_impact': '+5%', 'trend': 'Increasing'},
            'Healthcare': {'availability': 40, 'salary_impact': '0%', 'trend': 'Stable'},
            'Finance': {'availability': 65, 'salary_impact': '-5%', 'trend': 'Increasing'}
        }
        
        return remote_data.get(industry, {
            'availability': 50, 'salary_impact': '0%', 'trend': 'Unknown'
        })
    
    def _calculate_market_saturation(self, industry: str) -> str:
        """Calculate market saturation level"""
        # Simplified calculation based on growth and competition
        trend_data = self.market_data['job_market_trends'].get(industry, {})
        growth = trend_data.get('growth_rate', 5)
        competition = trend_data.get('competition_level', 'Medium')
        
        if growth > 15 and competition != 'Very High':
            return 'Low Saturation - High Opportunity'
        elif growth > 8:
            return 'Moderate Saturation - Good Opportunity'
        else:
            return 'High Saturation - Competitive Market'
    
    def _generate_short_term_forecast(self, trend_data: Dict) -> str:
        """Generate 6-month forecast"""
        growth = trend_data.get('growth_rate', 5)
        if growth > 10:
            return "Strong growth expected, excellent job market conditions"
        elif growth > 5:
            return "Steady growth, stable job opportunities"
        else:
            return "Slow growth, competitive market conditions"
    
    def _generate_medium_term_forecast(self, trend_data: Dict) -> str:
        """Generate 1-2 year forecast"""
        hot_skills = trend_data.get('hot_skills', [])
        if len(hot_skills) >= 4:
            return "Multiple growth areas emerging, diverse opportunities"
        else:
            return "Focused growth in specific skill areas"
    
    def _generate_long_term_forecast(self, trend_data: Dict) -> str:
        """Generate 3-5 year forecast"""
        outlook = trend_data.get('market_outlook', 'Stable')
        if outlook == 'Excellent':
            return "Sustained growth expected, strong long-term prospects"
        elif outlook == 'Strong':
            return "Positive outlook with good career advancement potential"
        else:
            return "Stable market with evolution in skill requirements"