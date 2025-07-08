import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import re

@dataclass
class CareerPath:
    """Career path simulation data model"""
    current_role: str
    current_level: str
    current_salary: int
    target_role: str
    target_timeline: int  # years
    industry: str
    skills_gap: List[str]
    certifications_needed: List[str]
    experience_requirements: Dict[str, int]
    growth_trajectory: List[Dict[str, Any]]

@dataclass
class NegotiationScenario:
    """Salary negotiation scenario model"""
    current_offer: int
    market_rate: int
    target_salary: int
    benefits_value: int
    negotiation_factors: List[str]
    leverage_points: List[str]
    risks: List[str]
    strategies: List[str]

class CareerPathSimulator:
    """
    AI-powered career path simulation and planning system
    """
    
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Career progression data
        self.career_ladders = {
            'Technology': {
                'Individual Contributor': [
                    'Junior Developer', 'Software Engineer', 'Senior Engineer',
                    'Staff Engineer', 'Principal Engineer', 'Distinguished Engineer'
                ],
                'Management': [
                    'Team Lead', 'Engineering Manager', 'Senior Manager',
                    'Director of Engineering', 'VP Engineering', 'CTO'
                ],
                'Product': [
                    'Associate PM', 'Product Manager', 'Senior PM',
                    'Principal PM', 'Director of Product', 'VP Product'
                ]
            },
            'Finance': {
                'Analyst Track': [
                    'Financial Analyst', 'Senior Analyst', 'Finance Manager',
                    'Senior Manager', 'Director', 'VP Finance'
                ],
                'Investment': [
                    'Investment Analyst', 'Associate', 'VP',
                    'Principal', 'Managing Director', 'Partner'
                ]
            },
            'Healthcare': {
                'Clinical': [
                    'Staff Nurse', 'Charge Nurse', 'Nurse Manager',
                    'Director of Nursing', 'Chief Nursing Officer'
                ],
                'Administration': [
                    'Healthcare Analyst', 'Manager', 'Director',
                    'VP Operations', 'Chief Operating Officer'
                ]
            }
        }
        
        # Skill evolution patterns
        self.skill_evolution = {
            'Technology': {
                'technical_skills': ['Programming', 'System Design', 'Architecture', 'AI/ML', 'Cloud Platforms'],
                'leadership_skills': ['Team Management', 'Strategy', 'Communication', 'Mentoring'],
                'business_skills': ['Product Strategy', 'Business Analysis', 'Stakeholder Management']
            },
            'Finance': {
                'technical_skills': ['Financial Modeling', 'Risk Analysis', 'Regulations', 'Fintech'],
                'leadership_skills': ['Team Leadership', 'Client Management', 'Negotiation'],
                'business_skills': ['Strategic Planning', 'Market Analysis', 'Corporate Development']
            }
        }
        
        # Market data for simulations
        self.market_growth_rates = {
            'Technology': 0.12,  # 12% annual growth
            'Finance': 0.06,     # 6% annual growth
            'Healthcare': 0.08   # 8% annual growth
        }

    def simulate_career_paths(self, current_profile: Dict[str, Any],
                             career_goals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate multiple career path scenarios
        """
        # Generate multiple path scenarios
        scenarios = self._generate_path_scenarios(current_profile, career_goals)
        
        # Simulate outcomes for each scenario
        simulated_scenarios = []
        for scenario in scenarios:
            simulation = self._simulate_path_outcome(scenario, current_profile)
            simulated_scenarios.append(simulation)
        
        # Analyze and rank scenarios
        analysis = self._analyze_scenarios(simulated_scenarios)
        
        # Generate recommendations
        recommendations = self._generate_path_recommendations(simulated_scenarios, analysis)
        
        return {
            'scenarios': simulated_scenarios,
            'analysis': analysis,
            'recommendations': recommendations,
            'success_factors': self._identify_success_factors(simulated_scenarios),
            'risk_mitigation': self._generate_risk_mitigation_strategies(simulated_scenarios)
        }
    
    def _generate_path_scenarios(self, current_profile: Dict[str, Any],
                                career_goals: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate different career path scenarios
        """
        industry = current_profile.get('industry', 'Technology')
        current_level = current_profile.get('experience_level', 'Mid Level')
        target_role = career_goals.get('target_role', '')
        timeline = career_goals.get('timeline_years', 5)
        
        scenarios = []
        
        # Scenario 1: Aggressive Growth Path
        scenarios.append({
            'name': 'Aggressive Growth',
            'description': 'Fast-track advancement with high risk/reward',
            'timeline': max(timeline - 1, 2),
            'risk_level': 'High',
            'skill_development_intensity': 'Intensive',
            'networking_requirement': 'High',
            'salary_growth_rate': 0.25,
            'success_probability': 0.65
        })
        
        # Scenario 2: Steady Professional Growth
        scenarios.append({
            'name': 'Steady Professional',
            'description': 'Consistent advancement with balanced approach',
            'timeline': timeline,
            'risk_level': 'Medium',
            'skill_development_intensity': 'Moderate',
            'networking_requirement': 'Medium',
            'salary_growth_rate': 0.15,
            'success_probability': 0.80
        })
        
        # Scenario 3: Conservative Progression
        scenarios.append({
            'name': 'Conservative Progression',
            'description': 'Lower risk with gradual advancement',
            'timeline': timeline + 1,
            'risk_level': 'Low',
            'skill_development_intensity': 'Gradual',
            'networking_requirement': 'Low',
            'salary_growth_rate': 0.10,
            'success_probability': 0.90
        })
        
        # Scenario 4: Lateral + Vertical Movement
        scenarios.append({
            'name': 'Strategic Lateral Move',
            'description': 'Lateral move first, then vertical advancement',
            'timeline': timeline + 1,
            'risk_level': 'Medium',
            'skill_development_intensity': 'Focused',
            'networking_requirement': 'High',
            'salary_growth_rate': 0.18,
            'success_probability': 0.75
        })
        
        return scenarios
    
    def _simulate_path_outcome(self, scenario: Dict[str, Any],
                              current_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate outcomes for a specific career path scenario
        """
        timeline = scenario['timeline']
        current_salary = current_profile.get('current_salary', 75000)
        industry = current_profile.get('industry', 'Technology')
        
        # Calculate salary progression
        salary_progression = []
        for year in range(timeline + 1):
            if year == 0:
                salary = current_salary
            else:
                growth_rate = scenario['salary_growth_rate'] * (1 + np.random.normal(0, 0.1))
                salary = salary_progression[-1]['salary'] * (1 + growth_rate)
            
            salary_progression.append({
                'year': year,
                'salary': int(salary),
                'role_level': self._calculate_role_level(year, timeline),
                'skills_acquired': self._calculate_skills_acquired(year, scenario)
            })
        
        # Calculate key outcomes
        final_salary = salary_progression[-1]['salary']
        total_growth = (final_salary - current_salary) / current_salary * 100
        
        # Simulate additional factors
        networking_score = self._simulate_networking_growth(scenario)
        skill_portfolio_score = self._simulate_skill_development(scenario, timeline)
        market_positioning = self._simulate_market_positioning(scenario, industry)
        
        return {
            'scenario_name': scenario['name'],
            'scenario_details': scenario,
            'salary_progression': salary_progression,
            'final_salary': final_salary,
            'total_salary_growth': round(total_growth, 1),
            'networking_score': networking_score,
            'skill_portfolio_score': skill_portfolio_score,
            'market_positioning': market_positioning,
            'key_milestones': self._generate_milestones(timeline, scenario),
            'required_actions': self._generate_required_actions(scenario),
            'potential_obstacles': self._identify_potential_obstacles(scenario)
        }
    
    def _analyze_scenarios(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze and compare career path scenarios
        """
        # Compare outcomes
        comparison = {
            'salary_comparison': {},
            'risk_reward_analysis': {},
            'timeline_efficiency': {},
            'skill_development_comparison': {}
        }
        
        for scenario in scenarios:
            name = scenario['scenario_name']
            
            comparison['salary_comparison'][name] = {
                'final_salary': scenario['final_salary'],
                'growth_percentage': scenario['total_salary_growth']
            }
            
            comparison['risk_reward_analysis'][name] = {
                'risk_level': scenario['scenario_details']['risk_level'],
                'success_probability': scenario['scenario_details']['success_probability'],
                'reward_score': scenario['total_salary_growth'] * scenario['scenario_details']['success_probability']
            }
            
            comparison['timeline_efficiency'][name] = {
                'years_to_goal': scenario['scenario_details']['timeline'],
                'growth_per_year': scenario['total_salary_growth'] / scenario['scenario_details']['timeline']
            }
        
        # Rank scenarios
        rankings = {
            'highest_salary': max(scenarios, key=lambda x: x['final_salary'])['scenario_name'],
            'best_risk_adjusted': max(scenarios, key=lambda x: x['total_salary_growth'] * x['scenario_details']['success_probability'])['scenario_name'],
            'fastest_growth': max(scenarios, key=lambda x: x['total_salary_growth'] / x['scenario_details']['timeline'])['scenario_name']
        }
        
        return {
            'comparison': comparison,
            'rankings': rankings,
            'optimal_scenario': self._determine_optimal_scenario(scenarios)
        }
    
    def _generate_path_recommendations(self, scenarios: List[Dict[str, Any]],
                                     analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate actionable career path recommendations
        """
        recommendations = []
        
        optimal_scenario = analysis['optimal_scenario']
        
        recommendations.append({
            'category': 'Recommended Path',
            'recommendation': f"Based on analysis, the '{optimal_scenario['scenario_name']}' path offers the best balance of growth, risk, and success probability.",
            'action': f"Focus on {optimal_scenario['scenario_details']['skill_development_intensity'].lower()} skill development and {optimal_scenario['scenario_details']['networking_requirement'].lower()} networking efforts.",
            'timeline': f"{optimal_scenario['scenario_details']['timeline']} years"
        })
        
        # Skills recommendations
        recommendations.append({
            'category': 'Skill Development',
            'recommendation': f"Prioritize {optimal_scenario['required_actions'][0] if optimal_scenario['required_actions'] else 'technical and leadership skills'} for maximum impact.",
            'action': "Create a structured learning plan with quarterly milestones",
            'timeline': "Ongoing"
        })
        
        # Networking recommendations
        if optimal_scenario['scenario_details']['networking_requirement'] == 'High':
            recommendations.append({
                'category': 'Professional Networking',
                'recommendation': "Build strategic relationships within your target companies and industry",
                'action': "Attend 2-3 industry events per quarter and maintain active LinkedIn presence",
                'timeline': "6 months"
            })
        
        return recommendations
    
    def create_career_path_visualizations(self, simulation_results: Dict[str, Any]) -> List[go.Figure]:
        """
        Create comprehensive career path visualizations
        """
        figures = []
        
        # 1. Salary Progression Comparison
        figures.append(self._create_salary_progression_chart(simulation_results['scenarios']))
        
        # 2. Risk-Reward Analysis
        figures.append(self._create_risk_reward_chart(simulation_results['scenarios']))
        
        # 3. Skill Development Timeline
        figures.append(self._create_skill_development_chart(simulation_results['scenarios']))
        
        # 4. Career Milestone Timeline
        figures.append(self._create_milestone_timeline(simulation_results['scenarios']))
        
        return figures
    
    def _create_salary_progression_chart(self, scenarios: List[Dict[str, Any]]) -> go.Figure:
        """
        Create salary progression comparison chart
        """
        fig = go.Figure()
        
        colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
        
        for i, scenario in enumerate(scenarios):
            progression = scenario['salary_progression']
            years = [p['year'] for p in progression]
            salaries = [p['salary'] for p in progression]
            
            fig.add_trace(go.Scatter(
                x=years,
                y=salaries,
                mode='lines+markers',
                name=scenario['scenario_name'],
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8),
                hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Salary: $%{y:,.0f}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Career Path Salary Progression Comparison',
            xaxis_title='Years',
            yaxis_title='Salary ($)',
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def _create_risk_reward_chart(self, scenarios: List[Dict[str, Any]]) -> go.Figure:
        """
        Create risk vs reward analysis chart
        """
        risk_levels = {'Low': 1, 'Medium': 2, 'High': 3}
        
        x_values = [risk_levels[s['scenario_details']['risk_level']] for s in scenarios]
        y_values = [s['total_salary_growth'] for s in scenarios]
        sizes = [s['scenario_details']['success_probability'] * 100 for s in scenarios]
        names = [s['scenario_name'] for s in scenarios]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='markers+text',
            marker=dict(
                size=sizes,
                color=y_values,
                colorscale='viridis',
                showscale=True,
                colorbar=dict(title="Salary Growth %")
            ),
            text=names,
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Risk Level: %{x}<br>Salary Growth: %{y:.1f}%<br>Success Probability: %{marker.size}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Risk vs Reward Analysis (Bubble size = Success Probability)',
            xaxis=dict(
                title='Risk Level',
                tickvals=[1, 2, 3],
                ticktext=['Low', 'Medium', 'High']
            ),
            yaxis_title='Salary Growth (%)',
            height=400
        )
        
        return fig
    
    # Helper methods for career simulation
    def _calculate_role_level(self, year: int, total_timeline: int) -> str:
        """Calculate role level progression"""
        progress = year / total_timeline
        if progress < 0.3:
            return 'Current Level'
        elif progress < 0.6:
            return 'Mid-progression'
        elif progress < 0.9:
            return 'Senior Level'
        else:
            return 'Target Level'
    
    def _calculate_skills_acquired(self, year: int, scenario: Dict[str, Any]) -> List[str]:
        """Calculate skills acquired by year"""
        intensity = scenario['skill_development_intensity']
        base_skills_per_year = {'Intensive': 4, 'Moderate': 2, 'Gradual': 1, 'Focused': 3}
        
        skills_count = base_skills_per_year.get(intensity, 2) * year
        
        # Sample skill progression
        all_skills = [
            'Advanced Technical Skills', 'Leadership', 'Strategic Thinking',
            'Communication', 'Project Management', 'Industry Expertise',
            'Data Analysis', 'Innovation', 'Mentoring', 'Business Acumen'
        ]
        
        return all_skills[:min(skills_count, len(all_skills))]
    
    def _simulate_networking_growth(self, scenario: Dict[str, Any]) -> int:
        """Simulate networking score development"""
        base_score = 50
        requirement_multiplier = {'Low': 1.1, 'Medium': 1.3, 'High': 1.6}
        multiplier = requirement_multiplier.get(scenario['networking_requirement'], 1.2)
        
        return min(100, int(base_score * multiplier))
    
    def _simulate_skill_development(self, scenario: Dict[str, Any], timeline: int) -> int:
        """Simulate skill portfolio development score"""
        base_score = 60
        intensity_multiplier = {'Intensive': 1.5, 'Moderate': 1.2, 'Gradual': 1.1, 'Focused': 1.3}
        multiplier = intensity_multiplier.get(scenario['skill_development_intensity'], 1.2)
        
        return min(100, int(base_score * multiplier * (timeline / 5)))
    
    def _simulate_market_positioning(self, scenario: Dict[str, Any], industry: str) -> str:
        """Simulate market positioning outcome"""
        success_prob = scenario['success_probability']
        if success_prob > 0.8:
            return 'Top 10% of professionals'
        elif success_prob > 0.6:
            return 'Top 25% of professionals'
        else:
            return 'Above average positioning'
    
    def _generate_milestones(self, timeline: int, scenario: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate key milestones for the career path"""
        milestones = []
        
        for year in range(1, timeline + 1):
            if year == 1:
                milestone = "Complete initial skill assessment and development plan"
            elif year == timeline // 2:
                milestone = "Achieve mid-level promotion or significant role expansion"
            elif year == timeline:
                milestone = "Reach target role with desired compensation"
            else:
                milestone = f"Continued professional development and networking (Year {year})"
            
            milestones.append({
                'year': year,
                'milestone': milestone,
                'focus_area': self._get_focus_area_for_year(year, timeline)
            })
        
        return milestones
    
    def _get_focus_area_for_year(self, year: int, timeline: int) -> str:
        """Get focus area for specific year"""
        progress = year / timeline
        if progress < 0.4:
            return 'Skill Building'
        elif progress < 0.7:
            return 'Leadership Development'
        else:
            return 'Strategic Positioning'
    
    def _generate_required_actions(self, scenario: Dict[str, Any]) -> List[str]:
        """Generate required actions for the scenario"""
        actions = []
        
        intensity = scenario['skill_development_intensity']
        if intensity == 'Intensive':
            actions.append('Dedicate 10+ hours/week to skill development')
            actions.append('Pursue advanced certifications or degree')
        elif intensity == 'Moderate':
            actions.append('Maintain 5-7 hours/week learning schedule')
            actions.append('Complete relevant professional courses')
        
        networking = scenario['networking_requirement']
        if networking == 'High':
            actions.append('Attend monthly industry events')
            actions.append('Build relationships with key decision makers')
        
        return actions
    
    def _identify_potential_obstacles(self, scenario: Dict[str, Any]) -> List[str]:
        """Identify potential obstacles for the scenario"""
        obstacles = []
        
        if scenario['risk_level'] == 'High':
            obstacles.append('Market volatility could impact opportunities')
            obstacles.append('High competition for target positions')
        
        if scenario['networking_requirement'] == 'High':
            obstacles.append('Requires significant time investment in relationships')
        
        if scenario['success_probability'] < 0.7:
            obstacles.append('Lower probability of achieving all goals')
        
        return obstacles
    
    def _determine_optimal_scenario(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Determine the optimal scenario based on multiple factors"""
        # Score each scenario based on multiple criteria
        scored_scenarios = []
        
        for scenario in scenarios:
            score = (
                scenario['total_salary_growth'] * 0.3 +  # 30% weight on salary growth
                scenario['scenario_details']['success_probability'] * 100 * 0.4 +  # 40% weight on success probability
                (100 - scenario['scenario_details']['timeline'] * 10) * 0.2 +  # 20% weight on timeline (faster is better)
                scenario['skill_portfolio_score'] * 0.1  # 10% weight on skill development
            )
            
            scored_scenarios.append((scenario, score))
        
        # Return scenario with highest score
        return max(scored_scenarios, key=lambda x: x[1])[0]

class SalaryNegotiationCoach:
    """
    AI-powered salary negotiation coaching system
    """
    
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Negotiation strategies and tactics
        self.negotiation_strategies = {
            'anchoring': {
                'description': 'Set the initial offer high to anchor expectations',
                'best_for': ['First-time negotiations', 'Strong market position'],
                'script_template': "Based on my research and the value I bring, I was expecting a salary in the range of ${anchor_amount}..."
            },
            'value_demonstration': {
                'description': 'Focus on demonstrating unique value and ROI',
                'best_for': ['Experienced professionals', 'Specialized skills'],
                'script_template': "In my previous role, I delivered ${specific_value}. I'm confident I can bring similar results here..."
            },
            'market_comparison': {
                'description': 'Use market data to justify salary expectations',
                'best_for': ['Data-driven discussions', 'Transparent cultures'],
                'script_template': "According to market research, professionals with my background typically earn ${market_rate}..."
            },
            'total_compensation': {
                'description': 'Negotiate total package including benefits',
                'best_for': ['Fixed salary budgets', 'Benefit-rich companies'],
                'script_template': "I appreciate the base salary offer. Can we discuss the total compensation package..."
            }
        }
        
        # Industry-specific negotiation factors
        self.industry_factors = {
            'Technology': {
                'high_leverage_factors': ['Technical expertise', 'Stock options', 'Remote work'],
                'negotiable_benefits': ['Equity', 'Learning budget', 'Flexible schedule'],
                'market_volatility': 'Medium',
                'typical_increase_range': '10-25%'
            },
            'Finance': {
                'high_leverage_factors': ['Quantified results', 'Client relationships', 'Certifications'],
                'negotiable_benefits': ['Bonus structure', 'Professional development', 'Title'],
                'market_volatility': 'Low',
                'typical_increase_range': '5-15%'
            },
            'Healthcare': {
                'high_leverage_factors': ['Patient outcomes', 'Certifications', 'Experience'],
                'negotiable_benefits': ['Continuing education', 'Schedule flexibility', 'Loan forgiveness'],
                'market_volatility': 'Low',
                'typical_increase_range': '5-12%'
            }
        }
    
    def create_negotiation_strategy(self, negotiation_context: Dict[str, Any],
                                  market_data: Dict[str, Any],
                                  personal_factors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive salary negotiation strategy
        """
        # Analyze negotiation position
        position_analysis = self._analyze_negotiation_position(
            negotiation_context, market_data, personal_factors
        )
        
        # Generate strategy recommendations
        strategy = self._select_optimal_strategy(position_analysis, negotiation_context)
        
        # Create negotiation scripts
        scripts = self._generate_negotiation_scripts(strategy, negotiation_context, market_data)
        
        # Identify potential objections and responses
        objection_handling = self._prepare_objection_responses(negotiation_context, strategy)
        
        # Create timeline and action plan
        action_plan = self._create_negotiation_timeline(strategy, negotiation_context)
        
        return {
            'position_analysis': position_analysis,
            'recommended_strategy': strategy,
            'negotiation_scripts': scripts,
            'objection_handling': objection_handling,
            'action_plan': action_plan,
            'risk_assessment': self._assess_negotiation_risks(negotiation_context, strategy),
            'success_probability': self._calculate_success_probability(position_analysis, strategy)
        }
    
    def _analyze_negotiation_position(self, context: Dict[str, Any],
                                    market_data: Dict[str, Any],
                                    personal_factors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the strength of negotiation position
        """
        # Calculate leverage factors
        leverage_score = 0
        leverage_factors = []
        
        # Market position
        current_offer = context.get('current_offer', 0)
        market_rate = market_data.get('median_salary', current_offer)
        
        if current_offer < market_rate * 0.9:
            leverage_score += 30
            leverage_factors.append('Offer below market rate')
        elif current_offer > market_rate * 1.1:
            leverage_score -= 10
            leverage_factors.append('Offer above market rate')
        
        # Personal factors
        experience_premium = personal_factors.get('years_experience', 5) - 3
        if experience_premium > 2:
            leverage_score += 20
            leverage_factors.append('Strong experience advantage')
        
        # Unique skills
        if personal_factors.get('rare_skills', []):
            leverage_score += 25
            leverage_factors.append('Rare/high-demand skills')
        
        # Multiple offers
        if context.get('competing_offers', 0) > 0:
            leverage_score += 40
            leverage_factors.append('Multiple competing offers')
        
        # Company need
        if context.get('urgency_level', 'medium') == 'high':
            leverage_score += 15
            leverage_factors.append('High company urgency to fill role')
        
        leverage_score = min(100, max(0, leverage_score))
        
        return {
            'leverage_score': leverage_score,
            'leverage_factors': leverage_factors,
            'market_position': self._categorize_market_position(current_offer, market_rate),
            'negotiation_readiness': 'Strong' if leverage_score > 70 else 'Moderate' if leverage_score > 40 else 'Weak',
            'recommended_approach': self._recommend_approach(leverage_score)
        }
    
    def _select_optimal_strategy(self, position_analysis: Dict[str, Any],
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select the optimal negotiation strategy
        """
        leverage_score = position_analysis['leverage_score']
        industry = context.get('industry', 'Technology')
        
        if leverage_score > 70:
            primary_strategy = 'anchoring'
            confidence_level = 'High'
        elif leverage_score > 40:
            primary_strategy = 'value_demonstration'
            confidence_level = 'Moderate'
        else:
            primary_strategy = 'total_compensation'
            confidence_level = 'Conservative'
        
        # Add industry-specific considerations
        industry_factors = self.industry_factors.get(industry, self.industry_factors['Technology'])
        
        return {
            'primary_strategy': primary_strategy,
            'secondary_strategies': self._select_secondary_strategies(primary_strategy, industry),
            'confidence_level': confidence_level,
            'industry_considerations': industry_factors,
            'target_increase': self._calculate_target_increase(context, position_analysis),
            'negotiation_timeline': self._estimate_negotiation_timeline(context)
        }
    
    def _generate_negotiation_scripts(self, strategy: Dict[str, Any],
                                    context: Dict[str, Any],
                                    market_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate personalized negotiation scripts
        """
        primary_strategy = strategy['primary_strategy']
        current_offer = context.get('current_offer', 0)
        target_salary = context.get('target_salary', current_offer * 1.15)
        
        scripts = {}
        
        # Opening script
        if primary_strategy == 'anchoring':
            scripts['opening'] = f"""
            Thank you for the offer. I'm excited about the opportunity and believe I can make a significant impact in this role. 
            Based on my experience and the market research I've conducted, I was expecting a salary in the range of ${target_salary:,.0f}. 
            Can we discuss how we might bridge this gap?
            """
        
        elif primary_strategy == 'value_demonstration':
            scripts['opening'] = f"""
            I appreciate the offer and I'm very interested in joining the team. 
            Given the specific value I can bring - including [specific achievement] which resulted in [quantified impact] - 
            I believe a salary of ${target_salary:,.0f} would better reflect the ROI I can deliver.
            """
        
        elif primary_strategy == 'market_comparison':
            market_rate = market_data.get('median_salary', target_salary)
            scripts['opening'] = f"""
            Thank you for the offer. I've done extensive market research, and professionals with my background and skills 
            typically earn between ${market_rate * 0.9:,.0f} and ${market_rate * 1.1:,.0f}. 
            Could we adjust the offer to align with market standards?
            """
        
        # Counter-offer script
        scripts['counter_offer'] = f"""
        I understand budget constraints, and I want to find a solution that works for both of us. 
        If we can reach ${target_salary * 0.95:,.0f}, I'm prepared to accept immediately. 
        This represents a fair compromise given my qualifications and the value I'll bring.
        """
        
        # Benefit negotiation script
        scripts['benefits_focus'] = """
        I appreciate that the base salary may be fixed. Could we explore other aspects of the compensation package? 
        I'm particularly interested in [specific benefit] which would add significant value for me.
        """
        
        return scripts
    
    def _prepare_objection_responses(self, context: Dict[str, Any],
                                   strategy: Dict[str, Any]) -> Dict[str, str]:
        """
        Prepare responses to common objections
        """
        responses = {}
        
        responses['budget_constraints'] = """
        I understand budget considerations are important. Could we explore a performance-based increase after 6 months, 
        or perhaps adjust other aspects of the compensation package to bridge the gap?
        """
        
        responses['company_policy'] = """
        I respect company policies, and I'm wondering if there's flexibility in how we structure the total compensation. 
        Perhaps we could explore a signing bonus or accelerated review cycle?
        """
        
        responses['experience_concerns'] = """
        I understand the concern about experience. What I lack in years, I make up for in [specific strengths]. 
        I'm confident I can deliver results quickly and would welcome a performance review after 90 days.
        """
        
        responses['market_rate_dispute'] = """
        I'd be happy to share my research sources. Perhaps we could agree on a third-party salary survey to ensure 
        we're both working with accurate market data?
        """
        
        return responses
    
    def _create_negotiation_timeline(self, strategy: Dict[str, Any],
                                   context: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Create a negotiation timeline and action plan
        """
        timeline = []
        
        timeline.append({
            'phase': 'Preparation',
            'timeframe': '1-2 days before negotiation',
            'actions': [
                'Research salary data and prepare supporting documents',
                'Practice negotiation scripts with trusted advisor',
                'Prepare list of achievements and value propositions'
            ]
        })
        
        timeline.append({
            'phase': 'Initial Negotiation',
            'timeframe': 'Day 1',
            'actions': [
                'Present counter-offer using chosen strategy',
                'Listen actively to employer response',
                'Take notes and ask for time to consider if needed'
            ]
        })
        
        timeline.append({
            'phase': 'Follow-up',
            'timeframe': '2-3 days after initial discussion',
            'actions': [
                'Send follow-up email summarizing discussion',
                'Provide any additional documentation requested',
                'Reiterate interest and value proposition'
            ]
        })
        
        timeline.append({
            'phase': 'Final Decision',
            'timeframe': '1 week from initial negotiation',
            'actions': [
                'Review final offer against your minimum acceptable terms',
                'Make decision and communicate clearly',
                'If accepting, express enthusiasm; if declining, maintain positive relationship'
            ]
        })
        
        return timeline
    
    def _assess_negotiation_risks(self, context: Dict[str, Any],
                                strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess risks associated with the negotiation strategy
        """
        risks = {
            'offer_withdrawal': 'Low',
            'relationship_damage': 'Low',
            'reputation_impact': 'Minimal'
        }
        
        # Assess risk factors
        if strategy['confidence_level'] == 'High' and context.get('competing_offers', 0) == 0:
            risks['offer_withdrawal'] = 'Medium'
        
        if context.get('company_culture', 'collaborative') == 'hierarchical':
            risks['relationship_damage'] = 'Medium'
        
        if context.get('industry_reputation_importance', 'medium') == 'high':
            risks['reputation_impact'] = 'Moderate'
        
        return risks
    
    def _calculate_success_probability(self, position_analysis: Dict[str, Any],
                                     strategy: Dict[str, Any]) -> int:
        """
        Calculate probability of negotiation success
        """
        base_probability = 60  # Base success rate
        
        # Adjust based on leverage
        leverage_score = position_analysis['leverage_score']
        leverage_adjustment = (leverage_score - 50) * 0.4  # Scale leverage impact
        
        # Adjust based on strategy confidence
        confidence_adjustments = {'High': 15, 'Moderate': 5, 'Conservative': -5}
        confidence_adjustment = confidence_adjustments.get(strategy['confidence_level'], 0)
        
        final_probability = base_probability + leverage_adjustment + confidence_adjustment
        
        return max(20, min(95, int(final_probability)))
    
    # Helper methods
    def _categorize_market_position(self, current_offer: int, market_rate: int) -> str:
        """Categorize market position of current offer"""
        ratio = current_offer / market_rate if market_rate > 0 else 1
        
        if ratio < 0.9:
            return 'Below Market'
        elif ratio < 1.1:
            return 'Market Rate'
        else:
            return 'Above Market'
    
    def _recommend_approach(self, leverage_score: int) -> str:
        """Recommend negotiation approach based on leverage"""
        if leverage_score > 70:
            return 'Confident and direct'
        elif leverage_score > 40:
            return 'Collaborative and value-focused'
        else:
            return 'Flexible and benefit-focused'
    
    def _select_secondary_strategies(self, primary: str, industry: str) -> List[str]:
        """Select complementary negotiation strategies"""
        strategy_combinations = {
            'anchoring': ['value_demonstration', 'market_comparison'],
            'value_demonstration': ['total_compensation', 'market_comparison'],
            'market_comparison': ['value_demonstration', 'total_compensation'],
            'total_compensation': ['value_demonstration', 'market_comparison']
        }
        
        return strategy_combinations.get(primary, ['value_demonstration'])
    
    def _calculate_target_increase(self, context: Dict[str, Any],
                                 position_analysis: Dict[str, Any]) -> float:
        """Calculate realistic target salary increase"""
        current_offer = context.get('current_offer', 75000)
        leverage_score = position_analysis['leverage_score']
        
        # Base increase percentage based on leverage
        if leverage_score > 70:
            increase_percentage = 0.15  # 15%
        elif leverage_score > 40:
            increase_percentage = 0.10  # 10%
        else:
            increase_percentage = 0.05  # 5%
        
        return current_offer * (1 + increase_percentage)
    
    def _estimate_negotiation_timeline(self, context: Dict[str, Any]) -> str:
        """Estimate negotiation timeline"""
        company_size = context.get('company_size', 'medium')
        
        if company_size == 'startup':
            return '2-3 days'
        elif company_size == 'large':
            return '1-2 weeks'
        else:
            return '1 week'