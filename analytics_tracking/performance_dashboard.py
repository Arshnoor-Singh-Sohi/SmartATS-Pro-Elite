import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional
import numpy as np
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class AnalysisRecord:
    """Data class for storing analysis records"""
    timestamp: datetime
    resume_version: str
    job_description_hash: str
    industry: str
    experience_level: str
    match_percentage: float
    ats_score: float
    keyword_match_count: int
    skills_coverage: float
    optimization_suggestions: List[str]
    user_actions_taken: List[str]
    session_id: str

class PerformanceTracker:
    """
    Advanced performance tracking and analytics system
    """
    
    def __init__(self):
        self.session_key = 'performance_analytics'
        self._initialize_tracking()
    
    def _initialize_tracking(self):
        """Initialize tracking data structure"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                'analysis_history': [],
                'resume_versions': {},
                'optimization_goals': [],
                'benchmark_data': {},
                'user_preferences': {
                    'target_industries': [],
                    'career_goals': '',
                    'tracking_enabled': True
                }
            }
    
    def record_analysis(self, analysis_result: Dict[str, Any], 
                       resume_text: str, job_description: str,
                       industry: str, experience_level: str) -> str:
        """
        Record an analysis session for tracking
        """
        # Generate unique identifiers
        resume_hash = hashlib.md5(resume_text.encode()).hexdigest()[:8]
        jd_hash = hashlib.md5(job_description.encode()).hexdigest()[:8]
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{resume_hash}"
        
        # Create analysis record
        record = AnalysisRecord(
            timestamp=datetime.now(),
            resume_version=resume_hash,
            job_description_hash=jd_hash,
            industry=industry,
            experience_level=experience_level,
            match_percentage=analysis_result.get('match_percentage', 0),
            ats_score=analysis_result.get('ats_compatibility_score', 0),
            keyword_match_count=len(analysis_result.get('matched_keywords', [])),
            skills_coverage=analysis_result.get('skills_coverage', 0),
            optimization_suggestions=analysis_result.get('critical_improvements', []),
            user_actions_taken=[],
            session_id=session_id
        )
        
        # Store in session state
        tracking_data = st.session_state[self.session_key]
        tracking_data['analysis_history'].append(asdict(record))
        
        # Store resume version
        tracking_data['resume_versions'][resume_hash] = {
            'content': resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
            'first_analyzed': datetime.now().isoformat(),
            'version_name': f"Version {len(tracking_data['resume_versions']) + 1}",
            'analysis_count': 1
        }
        
        return session_id
    
    def record_user_action(self, session_id: str, action: str):
        """
        Record user actions taken after analysis
        """
        tracking_data = st.session_state[self.session_key]
        
        for record in tracking_data['analysis_history']:
            if record['session_id'] == session_id:
                record['user_actions_taken'].append({
                    'action': action,
                    'timestamp': datetime.now().isoformat()
                })
                break
    
    def get_performance_dashboard_data(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard data
        """
        tracking_data = st.session_state[self.session_key]
        history = tracking_data['analysis_history']
        
        if not history:
            return self._get_empty_dashboard_data()
        
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate key metrics
        dashboard_data = {
            'summary_metrics': self._calculate_summary_metrics(df),
            'trend_analysis': self._analyze_trends(df),
            'goal_progress': self._track_goal_progress(df),
            'comparison_analysis': self._analyze_version_comparisons(df),
            'industry_insights': self._analyze_industry_performance(df),
            'recommendation_effectiveness': self._analyze_recommendation_effectiveness(df),
            'optimization_roadmap': self._generate_optimization_roadmap(df)
        }
        
        return dashboard_data
    
    def create_performance_dashboard(self) -> List[go.Figure]:
        """
        Create comprehensive performance dashboard
        """
        dashboard_data = self.get_performance_dashboard_data()
        figures = []
        
        # 1. Performance Trends Over Time
        figures.append(self._create_performance_trends_chart(dashboard_data['trend_analysis']))
        
        # 2. Multi-metric Comparison
        figures.append(self._create_multi_metric_dashboard(dashboard_data['summary_metrics']))
        
        # 3. Goal Progress Tracking
        figures.append(self._create_goal_progress_chart(dashboard_data['goal_progress']))
        
        # 4. Resume Version Comparison
        figures.append(self._create_version_comparison_chart(dashboard_data['comparison_analysis']))
        
        # 5. Industry Performance Analysis
        figures.append(self._create_industry_analysis_chart(dashboard_data['industry_insights']))
        
        return figures
    
    def _calculate_summary_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate summary performance metrics
        """
        if df.empty:
            return {}
        
        latest_analysis = df.iloc[-1]
        first_analysis = df.iloc[0]
        
        # Calculate improvements
        match_improvement = latest_analysis['match_percentage'] - first_analysis['match_percentage']
        ats_improvement = latest_analysis['ats_score'] - first_analysis['ats_score']
        keyword_improvement = latest_analysis['keyword_match_count'] - first_analysis['keyword_match_count']
        
        return {
            'total_analyses': len(df),
            'current_match_score': latest_analysis['match_percentage'],
            'current_ats_score': latest_analysis['ats_score'],
            'match_improvement': match_improvement,
            'ats_improvement': ats_improvement,
            'keyword_improvement': keyword_improvement,
            'best_match_score': df['match_percentage'].max(),
            'avg_match_score': df['match_percentage'].mean(),
            'consistency_score': 100 - df['match_percentage'].std(),  # Lower std = higher consistency
            'optimization_velocity': self._calculate_optimization_velocity(df)
        }
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze performance trends over time
        """
        if len(df) < 2:
            return {'trend_direction': 'insufficient_data'}
        
        # Calculate trend slopes
        x = np.arange(len(df))
        match_slope = np.polyfit(x, df['match_percentage'], 1)[0]
        ats_slope = np.polyfit(x, df['ats_score'], 1)[0]
        keyword_slope = np.polyfit(x, df['keyword_match_count'], 1)[0]
        
        return {
            'match_trend': 'improving' if match_slope > 0 else 'declining' if match_slope < 0 else 'stable',
            'ats_trend': 'improving' if ats_slope > 0 else 'declining' if ats_slope < 0 else 'stable',
            'keyword_trend': 'improving' if keyword_slope > 0 else 'declining' if keyword_slope < 0 else 'stable',
            'match_slope': match_slope,
            'ats_slope': ats_slope,
            'keyword_slope': keyword_slope,
            'trend_data': df[['timestamp', 'match_percentage', 'ats_score', 'keyword_match_count']].to_dict('records')
        }
    
    def _track_goal_progress(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Track progress towards optimization goals
        """
        # Default goals (can be customized by user)
        goals = {
            'match_percentage': 85,
            'ats_score': 90,
            'keyword_match_count': 15,
            'skills_coverage': 80
        }
        
        if df.empty:
            return {'goals': goals, 'progress': {}}
        
        latest = df.iloc[-1]
        progress = {}
        
        for metric, target in goals.items():
            if metric in latest:
                current = latest[metric]
                progress[metric] = {
                    'current': current,
                    'target': target,
                    'progress_percentage': min(100, (current / target) * 100),
                    'achieved': current >= target
                }
        
        return {
            'goals': goals,
            'progress': progress,
            'overall_goal_achievement': sum(1 for p in progress.values() if p['achieved']) / len(progress) * 100
        }
    
    def _analyze_version_comparisons(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze performance across different resume versions
        """
        if df.empty:
            return {}
        
        version_stats = df.groupby('resume_version').agg({
            'match_percentage': ['mean', 'max', 'count'],
            'ats_score': 'mean',
            'keyword_match_count': 'mean',
            'timestamp': 'max'
        }).round(2)
        
        # Find best performing version
        best_version = version_stats['match_percentage']['mean'].idxmax()
        
        return {
            'version_stats': version_stats.to_dict(),
            'best_version': best_version,
            'version_count': len(version_stats),
            'version_comparison_data': df.groupby('resume_version')[
                ['match_percentage', 'ats_score', 'keyword_match_count']
            ].mean().to_dict('index')
        }
    
    def _analyze_industry_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze performance across different industries
        """
        if df.empty:
            return {}
        
        industry_stats = df.groupby('industry').agg({
            'match_percentage': 'mean',
            'ats_score': 'mean',
            'keyword_match_count': 'mean'
        }).round(2)
        
        return {
            'industry_performance': industry_stats.to_dict('index'),
            'best_industry': industry_stats['match_percentage'].idxmax() if not industry_stats.empty else None,
            'industry_insights': self._generate_industry_insights(industry_stats)
        }
    
    def _analyze_recommendation_effectiveness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze how effective optimization recommendations have been
        """
        if len(df) < 2:
            return {'effectiveness': 'insufficient_data'}
        
        # Track improvements after recommendations
        improvements = []
        for i in range(1, len(df)):
            prev_score = df.iloc[i-1]['match_percentage']
            curr_score = df.iloc[i]['match_percentage']
            improvement = curr_score - prev_score
            improvements.append(improvement)
        
        avg_improvement = np.mean(improvements) if improvements else 0
        
        return {
            'avg_improvement_per_iteration': avg_improvement,
            'total_improvements': sum(1 for imp in improvements if imp > 0),
            'recommendation_success_rate': (sum(1 for imp in improvements if imp > 0) / len(improvements)) * 100 if improvements else 0,
            'max_single_improvement': max(improvements) if improvements else 0
        }
    
    def _generate_optimization_roadmap(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate future optimization roadmap based on historical data
        """
        if df.empty:
            return {}
        
        latest = df.iloc[-1]
        
        # Identify areas needing improvement
        improvement_areas = []
        
        if latest['match_percentage'] < 80:
            improvement_areas.append({
                'area': 'Keyword Optimization',
                'current_score': latest['match_percentage'],
                'target_score': 85,
                'priority': 'High',
                'estimated_timeline': '1-2 weeks'
            })
        
        if latest['ats_score'] < 85:
            improvement_areas.append({
                'area': 'ATS Compatibility',
                'current_score': latest['ats_score'],
                'target_score': 90,
                'priority': 'High',
                'estimated_timeline': '1 week'
            })
        
        if latest['keyword_match_count'] < 12:
            improvement_areas.append({
                'area': 'Technical Skills',
                'current_score': latest['keyword_match_count'],
                'target_score': 15,
                'priority': 'Medium',
                'estimated_timeline': '2-3 weeks'
            })
        
        return {
            'improvement_areas': improvement_areas,
            'next_milestone': self._calculate_next_milestone(latest),
            'projected_timeline': self._calculate_projected_timeline(df)
        }
    
    def _create_performance_trends_chart(self, trend_data: Dict[str, Any]) -> go.Figure:
        """
        Create performance trends chart
        """
        if 'trend_data' not in trend_data:
            return self._create_empty_chart("Performance Trends", "No data available")
        
        data = trend_data['trend_data']
        df = pd.DataFrame(data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Match Percentage Over Time', 'ATS Score Over Time', 
                          'Keyword Matches Over Time', 'Overall Progress'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Match percentage trend
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['match_percentage'],
                      mode='lines+markers', name='Match %',
                      line=dict(color='#3B82F6', width=3)),
            row=1, col=1
        )
        
        # ATS score trend
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['ats_score'],
                      mode='lines+markers', name='ATS Score',
                      line=dict(color='#10B981', width=3)),
            row=1, col=2
        )
        
        # Keyword matches trend
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['keyword_match_count'],
                      mode='lines+markers', name='Keywords',
                      line=dict(color='#F59E0B', width=3)),
            row=2, col=1
        )
        
        # Overall progress (combined metric)
        overall_score = (df['match_percentage'] + df['ats_score']) / 2
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=overall_score,
                      mode='lines+markers', name='Overall',
                      line=dict(color='#8B5CF6', width=3)),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            title_text="Performance Trends Analysis",
            showlegend=False
        )
        
        return fig
    
    def _create_multi_metric_dashboard(self, summary_metrics: Dict[str, Any]) -> go.Figure:
        """
        Create multi-metric dashboard
        """
        if not summary_metrics:
            return self._create_empty_chart("Performance Metrics", "No data available")
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Current Scores', 'Improvements', 'Consistency', 
                          'Analysis Count', 'Best Scores', 'Optimization Velocity'),
            specs=[[{"type": "indicator"}, {"type": "bar"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "bar"}, {"type": "indicator"}]]
        )
        
        # Current match score
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=summary_metrics.get('current_match_score', 0),
                title={'text': "Match Score"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "#3B82F6"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=1
        )
        
        # Improvements bar chart
        improvements = [
            summary_metrics.get('match_improvement', 0),
            summary_metrics.get('ats_improvement', 0),
            summary_metrics.get('keyword_improvement', 0)
        ]
        fig.add_trace(
            go.Bar(x=['Match', 'ATS', 'Keywords'], y=improvements,
                   marker_color=['#10B981' if x > 0 else '#EF4444' for x in improvements]),
            row=1, col=2
        )
        
        # Consistency score
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=summary_metrics.get('consistency_score', 0),
                title={'text': "Consistency"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "#8B5CF6"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=3
        )
        
        # Analysis count
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=summary_metrics.get('total_analyses', 0),
                title={'text': "Total Analyses"},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=2, col=1
        )
        
        # Best scores
        best_scores = [
            summary_metrics.get('best_match_score', 0),
            summary_metrics.get('current_ats_score', 0)
        ]
        fig.add_trace(
            go.Bar(x=['Best Match', 'Current ATS'], y=best_scores,
                   marker_color=['#F59E0B', '#06B6D4']),
            row=2, col=2
        )
        
        # Optimization velocity
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=summary_metrics.get('optimization_velocity', 0),
                title={'text': "Velocity (pts/week)"},
                number={'suffix': " pts"},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=2, col=3
        )
        
        fig.update_layout(
            height=500,
            title_text="Performance Metrics Dashboard",
            showlegend=False
        )
        
        return fig
    
    def _create_goal_progress_chart(self, goal_data: Dict[str, Any]) -> go.Figure:
        """
        Create goal progress tracking chart
        """
        if not goal_data.get('progress'):
            return self._create_empty_chart("Goal Progress", "Set goals to track progress")
        
        progress = goal_data['progress']
        
        metrics = list(progress.keys())
        current_values = [progress[m]['current'] for m in metrics]
        target_values = [progress[m]['target'] for m in metrics]
        progress_percentages = [progress[m]['progress_percentage'] for m in metrics]
        
        fig = go.Figure()
        
        # Current values
        fig.add_trace(go.Bar(
            name='Current',
            x=metrics,
            y=current_values,
            marker_color='#3B82F6'
        ))
        
        # Target values
        fig.add_trace(go.Bar(
            name='Target',
            x=metrics,
            y=target_values,
            marker_color='#10B981',
            opacity=0.6
        ))
        
        fig.update_layout(
            title='Goal Progress Tracking',
            xaxis_title='Metrics',
            yaxis_title='Scores',
            barmode='group',
            height=400
        )
        
        return fig
    
    def _create_version_comparison_chart(self, comparison_data: Dict[str, Any]) -> go.Figure:
        """
        Create resume version comparison chart
        """
        if not comparison_data.get('version_comparison_data'):
            return self._create_empty_chart("Version Comparison", "Multiple versions needed")
        
        data = comparison_data['version_comparison_data']
        versions = list(data.keys())
        
        match_scores = [data[v]['match_percentage'] for v in versions]
        ats_scores = [data[v]['ats_score'] for v in versions]
        keyword_counts = [data[v]['keyword_match_count'] for v in versions]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Match %',
            x=versions,
            y=match_scores,
            marker_color='#3B82F6'
        ))
        
        fig.add_trace(go.Bar(
            name='ATS Score',
            x=versions,
            y=ats_scores,
            marker_color='#10B981'
        ))
        
        fig.add_trace(go.Bar(
            name='Keywords',
            x=versions,
            y=keyword_counts,
            marker_color='#F59E0B'
        ))
        
        fig.update_layout(
            title='Resume Version Comparison',
            xaxis_title='Resume Versions',
            yaxis_title='Scores',
            barmode='group',
            height=400
        )
        
        return fig
    
    def _create_industry_analysis_chart(self, industry_data: Dict[str, Any]) -> go.Figure:
        """
        Create industry performance analysis chart
        """
        if not industry_data.get('industry_performance'):
            return self._create_empty_chart("Industry Analysis", "Multiple industries needed")
        
        data = industry_data['industry_performance']
        industries = list(data.keys())
        
        match_scores = [data[ind]['match_percentage'] for ind in industries]
        ats_scores = [data[ind]['ats_score'] for ind in industries]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=match_scores,
            y=ats_scores,
            mode='markers+text',
            text=industries,
            textposition='top center',
            marker=dict(size=12, color='#3B82F6'),
            name='Industries'
        ))
        
        fig.update_layout(
            title='Industry Performance Analysis',
            xaxis_title='Match Percentage',
            yaxis_title='ATS Score',
            height=400
        )
        
        return fig
    
    def _create_empty_chart(self, title: str, message: str) -> go.Figure:
        """
        Create empty chart with message
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=title,
            height=300,
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig
    
    def _calculate_optimization_velocity(self, df: pd.DataFrame) -> float:
        """
        Calculate optimization velocity (improvement per time period)
        """
        if len(df) < 2:
            return 0
        
        time_diff = (df.iloc[-1]['timestamp'] - df.iloc[0]['timestamp']).days
        score_diff = df.iloc[-1]['match_percentage'] - df.iloc[0]['match_percentage']
        
        if time_diff == 0:
            return 0
        
        return round((score_diff / time_diff) * 7, 2)  # Points per week
    
    def _calculate_next_milestone(self, latest_record: Dict) -> Dict[str, Any]:
        """
        Calculate next optimization milestone
        """
        current_score = latest_record['match_percentage']
        
        if current_score < 70:
            return {'target': 70, 'label': 'Good Match', 'points_needed': 70 - current_score}
        elif current_score < 80:
            return {'target': 80, 'label': 'Strong Match', 'points_needed': 80 - current_score}
        elif current_score < 90:
            return {'target': 90, 'label': 'Excellent Match', 'points_needed': 90 - current_score}
        else:
            return {'target': 95, 'label': 'Perfect Match', 'points_needed': 95 - current_score}
    
    def _calculate_projected_timeline(self, df: pd.DataFrame) -> str:
        """
        Calculate projected timeline to reach goals
        """
        velocity = self._calculate_optimization_velocity(df)
        
        if velocity <= 0:
            return "Unable to project - inconsistent progress"
        
        latest_score = df.iloc[-1]['match_percentage']
        target_score = 85  # Default target
        
        points_needed = target_score - latest_score
        weeks_needed = max(1, points_needed / velocity)
        
        return f"{int(weeks_needed)} weeks to reach {target_score}% match"
    
    def _generate_industry_insights(self, industry_stats: pd.DataFrame) -> List[str]:
        """
        Generate insights about industry performance
        """
        if industry_stats.empty:
            return []
        
        insights = []
        best_industry = industry_stats['match_percentage'].idxmax()
        best_score = industry_stats.loc[best_industry, 'match_percentage']
        
        insights.append(f"Highest performance in {best_industry} industry ({best_score:.1f}% match)")
        
        if len(industry_stats) > 1:
            score_range = industry_stats['match_percentage'].max() - industry_stats['match_percentage'].min()
            if score_range > 15:
                insights.append("Significant variation across industries - focus on industry-specific optimization")
        
        return insights
    
    def _get_empty_dashboard_data(self) -> Dict[str, Any]:
        """
        Return empty dashboard data structure
        """
        return {
            'summary_metrics': {},
            'trend_analysis': {},
            'goal_progress': {},
            'comparison_analysis': {},
            'industry_insights': {},
            'recommendation_effectiveness': {},
            'optimization_roadmap': {}
        }

class GoalSettingEngine:
    """
    Engine for setting and tracking optimization goals
    """
    
    def __init__(self):
        self.goal_templates = {
            'job_search_intensive': {
                'name': 'Job Search Intensive',
                'duration_weeks': 4,
                'targets': {
                    'match_percentage': 85,
                    'ats_score': 90,
                    'applications_per_week': 10
                }
            },
            'career_transition': {
                'name': 'Career Transition',
                'duration_weeks': 12,
                'targets': {
                    'match_percentage': 75,
                    'industry_alignment': 80,
                    'skill_development': 70
                }
            },
            'promotion_prep': {
                'name': 'Promotion Preparation',
                'duration_weeks': 8,
                'targets': {
                    'match_percentage': 90,
                    'leadership_indicators': 85,
                    'achievement_quantification': 80
                }
            }
        }
    
    def create_personalized_goals(self, user_profile: Dict[str, Any], 
                                target_timeline: int) -> Dict[str, Any]:
        """
        Create personalized optimization goals
        """
        experience_level = user_profile.get('experience_level', 'Mid Level')
        target_industry = user_profile.get('target_industry', 'Technology')
        current_scores = user_profile.get('current_scores', {})
        
        # Base targets by experience level
        base_targets = {
            'Entry Level': {'match_percentage': 75, 'ats_score': 85},
            'Mid Level': {'match_percentage': 82, 'ats_score': 88},
            'Senior Level': {'match_percentage': 88, 'ats_score': 92},
            'Executive': {'match_percentage': 90, 'ats_score': 95}
        }
        
        targets = base_targets.get(experience_level, base_targets['Mid Level'])
        
        # Adjust based on current performance
        for metric, target in targets.items():
            current = current_scores.get(metric, 60)
            if current > target:
                targets[metric] = min(95, current + 5)  # Aim 5 points higher
        
        return {
            'targets': targets,
            'timeline_weeks': target_timeline,
            'milestones': self._create_milestones(targets, target_timeline),
            'success_criteria': self._define_success_criteria(targets)
        }
    
    def _create_milestones(self, targets: Dict[str, float], 
                          timeline_weeks: int) -> List[Dict[str, Any]]:
        """
        Create intermediate milestones
        """
        milestones = []
        
        # Create weekly milestones
        for week in range(1, timeline_weeks + 1):
            milestone = {
                'week': week,
                'targets': {}
            }
            
            for metric, final_target in targets.items():
                # Linear progression (could be made more sophisticated)
                weekly_target = (final_target * week) / timeline_weeks
                milestone['targets'][metric] = round(weekly_target, 1)
            
            milestones.append(milestone)
        
        return milestones
    
    def _define_success_criteria(self, targets: Dict[str, float]) -> Dict[str, str]:
        """
        Define success criteria for each target
        """
        criteria = {}
        
        for metric, target in targets.items():
            if metric == 'match_percentage':
                if target >= 85:
                    criteria[metric] = "Excellent keyword alignment with job requirements"
                elif target >= 75:
                    criteria[metric] = "Strong keyword alignment with job requirements"
                else:
                    criteria[metric] = "Adequate keyword alignment with job requirements"
            elif metric == 'ats_score':
                if target >= 90:
                    criteria[metric] = "Premium ATS optimization"
                elif target >= 85:
                    criteria[metric] = "Strong ATS compatibility"
                else:
                    criteria[metric] = "Good ATS compatibility"
        
        return criteria