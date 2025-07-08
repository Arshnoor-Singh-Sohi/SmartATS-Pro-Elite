import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

class ApplicationStatus(Enum):
    """Application status enumeration"""
    DRAFT = "draft"
    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    PHONE_SCREEN = "phone_screen"
    TECHNICAL_INTERVIEW = "technical_interview"
    ONSITE_INTERVIEW = "onsite_interview"
    FINAL_INTERVIEW = "final_interview"
    OFFER_RECEIVED = "offer_received"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

@dataclass
class JobApplication:
    """Job application data model"""
    id: str
    company_name: str
    position_title: str
    location: str
    job_type: str  # full-time, part-time, contract, remote
    industry: str
    salary_range: str
    application_date: datetime
    status: ApplicationStatus
    source: str  # LinkedIn, Company Website, Referral, etc.
    job_description: str
    resume_version: str
    cover_letter_version: str
    match_score: float
    notes: str
    follow_up_dates: List[datetime]
    interview_dates: List[datetime]
    contacts: List[Dict[str, str]]
    offer_details: Dict[str, Any]
    rejection_feedback: str
    last_updated: datetime

class JobApplicationTracker:
    """
    Comprehensive job application tracking and analytics system
    """
    
    def __init__(self):
        self.session_key = 'job_applications'
        self._initialize_tracker()
        
        # Application pipeline stages
        self.pipeline_stages = {
            ApplicationStatus.DRAFT: {'order': 0, 'color': '#94A3B8', 'label': 'Draft'},
            ApplicationStatus.APPLIED: {'order': 1, 'color': '#3B82F6', 'label': 'Applied'},
            ApplicationStatus.UNDER_REVIEW: {'order': 2, 'color': '#F59E0B', 'label': 'Under Review'},
            ApplicationStatus.PHONE_SCREEN: {'order': 3, 'color': '#8B5CF6', 'label': 'Phone Screen'},
            ApplicationStatus.TECHNICAL_INTERVIEW: {'order': 4, 'color': '#EC4899', 'label': 'Technical'},
            ApplicationStatus.ONSITE_INTERVIEW: {'order': 5, 'color': '#EF4444', 'label': 'Onsite'},
            ApplicationStatus.FINAL_INTERVIEW: {'order': 6, 'color': '#F97316', 'label': 'Final Round'},
            ApplicationStatus.OFFER_RECEIVED: {'order': 7, 'color': '#10B981', 'label': 'Offer'},
            ApplicationStatus.ACCEPTED: {'order': 8, 'color': '#059669', 'label': 'Accepted'},
            ApplicationStatus.REJECTED: {'order': -1, 'color': '#DC2626', 'label': 'Rejected'},
            ApplicationStatus.WITHDRAWN: {'order': -2, 'color': '#6B7280', 'label': 'Withdrawn'}
        }
        
        # Success metrics and KPIs
        self.success_metrics = [
            'response_rate', 'interview_rate', 'offer_rate', 'acceptance_rate',
            'time_to_response', 'time_to_offer', 'average_salary_offered'
        ]
    
    def _initialize_tracker(self):
        """Initialize the tracking system"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                'applications': {},
                'analytics': {},
                'goals': {},
                'insights': []
            }
    
    def add_application(self, application: JobApplication) -> str:
        """Add a new job application to the tracker"""
        app_id = f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(st.session_state[self.session_key]['applications'])}"
        application.id = app_id
        application.last_updated = datetime.now()
        
        st.session_state[self.session_key]['applications'][app_id] = asdict(application)
        
        # Update analytics
        self._update_analytics()
        
        return app_id
    
    def update_application_status(self, app_id: str, new_status: ApplicationStatus, 
                                notes: str = "", follow_up_date: Optional[datetime] = None):
        """Update application status and add activity log"""
        applications = st.session_state[self.session_key]['applications']
        
        if app_id in applications:
            old_status = applications[app_id]['status']
            applications[app_id]['status'] = new_status.value
            applications[app_id]['last_updated'] = datetime.now().isoformat()
            
            # Add notes if provided
            if notes:
                current_notes = applications[app_id].get('notes', '')
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                new_note = f"[{timestamp}] Status changed from {old_status} to {new_status.value}: {notes}"
                applications[app_id]['notes'] = f"{current_notes}\n{new_note}" if current_notes else new_note
            
            # Add follow-up date if provided
            if follow_up_date:
                follow_ups = applications[app_id].get('follow_up_dates', [])
                follow_ups.append(follow_up_date.isoformat())
                applications[app_id]['follow_up_dates'] = follow_ups
            
            # Update analytics
            self._update_analytics()
    
    def get_applications_dataframe(self) -> pd.DataFrame:
        """Get all applications as a pandas DataFrame"""
        applications = st.session_state[self.session_key]['applications']
        
        if not applications:
            return pd.DataFrame()
        
        df = pd.DataFrame.from_dict(applications, orient='index')
        
        # Convert date columns
        date_columns = ['application_date', 'last_updated']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        return df
    
    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Generate comprehensive analytics dashboard data"""
        df = self.get_applications_dataframe()
        
        if df.empty:
            return {'error': 'No applications data available'}
        
        analytics = {
            'summary_stats': self._calculate_summary_stats(df),
            'conversion_funnel': self._calculate_conversion_funnel(df),
            'time_analysis': self._analyze_application_timing(df),
            'source_analysis': self._analyze_application_sources(df),
            'industry_analysis': self._analyze_industry_performance(df),
            'salary_analysis': self._analyze_salary_trends(df),
            'success_predictors': self._identify_success_predictors(df),
            'recommendations': self._generate_recommendations(df)
        }
        
        return analytics
    
    def _calculate_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate key summary statistics"""
        total_applications = len(df)
        
        # Status distribution
        status_counts = df['status'].value_counts()
        
        # Calculate key rates
        responses = len(df[df['status'] != ApplicationStatus.APPLIED.value])
        interviews = len(df[df['status'].isin([
            ApplicationStatus.PHONE_SCREEN.value,
            ApplicationStatus.TECHNICAL_INTERVIEW.value,
            ApplicationStatus.ONSITE_INTERVIEW.value,
            ApplicationStatus.FINAL_INTERVIEW.value
        ])])
        offers = len(df[df['status'] == ApplicationStatus.OFFER_RECEIVED.value])
        accepted = len(df[df['status'] == ApplicationStatus.ACCEPTED.value])
        
        response_rate = (responses / total_applications * 100) if total_applications > 0 else 0
        interview_rate = (interviews / total_applications * 100) if total_applications > 0 else 0
        offer_rate = (offers / total_applications * 100) if total_applications > 0 else 0
        
        return {
            'total_applications': total_applications,
            'active_applications': len(df[~df['status'].isin([
                ApplicationStatus.REJECTED.value,
                ApplicationStatus.ACCEPTED.value,
                ApplicationStatus.WITHDRAWN.value
            ])]),
            'response_rate': round(response_rate, 1),
            'interview_rate': round(interview_rate, 1),
            'offer_rate': round(offer_rate, 1),
            'status_distribution': status_counts.to_dict(),
            'recent_activity': self._get_recent_activity(df)
        }
    
    def _calculate_conversion_funnel(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate conversion funnel metrics"""
        funnel_stages = [
            ('Applied', ApplicationStatus.APPLIED.value),
            ('Response', ApplicationStatus.UNDER_REVIEW.value),
            ('Phone Screen', ApplicationStatus.PHONE_SCREEN.value),
            ('Technical', ApplicationStatus.TECHNICAL_INTERVIEW.value),
            ('Onsite', ApplicationStatus.ONSITE_INTERVIEW.value),
            ('Final', ApplicationStatus.FINAL_INTERVIEW.value),
            ('Offer', ApplicationStatus.OFFER_RECEIVED.value),
            ('Accepted', ApplicationStatus.ACCEPTED.value)
        ]
        
        funnel_data = []
        total_apps = len(df)
        
        for stage_name, status in funnel_stages:
            if status == ApplicationStatus.APPLIED.value:
                count = total_apps
            elif status == ApplicationStatus.UNDER_REVIEW.value:
                # Count all applications that got past "applied" status
                count = len(df[df['status'] != ApplicationStatus.APPLIED.value])
            else:
                # Count applications at this specific status or beyond
                stage_order = self.pipeline_stages[ApplicationStatus(status)]['order']
                count = len(df[df['status'].apply(lambda s: self.pipeline_stages.get(ApplicationStatus(s), {'order': -10})['order'] >= stage_order)])
            
            conversion_rate = (count / total_apps * 100) if total_apps > 0 else 0
            
            funnel_data.append({
                'stage': stage_name,
                'count': count,
                'conversion_rate': round(conversion_rate, 1)
            })
        
        return {
            'funnel_data': funnel_data,
            'overall_conversion': round((funnel_data[-1]['count'] / total_apps * 100) if total_apps > 0 else 0, 1)
        }
    
    def _analyze_application_timing(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze timing patterns in applications"""
        df_copy = df.copy()
        df_copy['application_date'] = pd.to_datetime(df_copy['application_date'])
        
        # Applications by day of week
        df_copy['day_of_week'] = df_copy['application_date'].dt.day_name()
        day_counts = df_copy['day_of_week'].value_counts()
        
        # Applications by month
        df_copy['month'] = df_copy['application_date'].dt.strftime('%Y-%m')
        month_counts = df_copy['month'].value_counts().sort_index()
        
        # Response time analysis (if we have status change data)
        response_times = []
        for _, app in df_copy.iterrows():
            if app['status'] != ApplicationStatus.APPLIED.value:
                # Simplified: assume response came within a week
                # In real implementation, we'd track actual status change dates
                response_times.append(np.random.randint(1, 14))  # Random for demo
        
        avg_response_time = np.mean(response_times) if response_times else 0
        
        return {
            'applications_by_day': day_counts.to_dict(),
            'applications_by_month': month_counts.to_dict(),
            'average_response_time_days': round(avg_response_time, 1),
            'peak_application_day': day_counts.index[0] if not day_counts.empty else 'N/A',
            'application_frequency': len(df_copy) / max(1, (datetime.now() - df_copy['application_date'].min()).days) if not df_copy.empty else 0
        }
    
    def _analyze_application_sources(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze effectiveness of different application sources"""
        source_stats = {}
        
        for source in df['source'].unique():
            source_df = df[df['source'] == source]
            total = len(source_df)
            
            responses = len(source_df[source_df['status'] != ApplicationStatus.APPLIED.value])
            interviews = len(source_df[source_df['status'].isin([
                ApplicationStatus.PHONE_SCREEN.value,
                ApplicationStatus.TECHNICAL_INTERVIEW.value,
                ApplicationStatus.ONSITE_INTERVIEW.value,
                ApplicationStatus.FINAL_INTERVIEW.value
            ])])
            offers = len(source_df[source_df['status'] == ApplicationStatus.OFFER_RECEIVED.value])
            
            source_stats[source] = {
                'total_applications': total,
                'response_rate': round((responses / total * 100) if total > 0 else 0, 1),
                'interview_rate': round((interviews / total * 100) if total > 0 else 0, 1),
                'offer_rate': round((offers / total * 100) if total > 0 else 0, 1),
                'effectiveness_score': round(((responses * 0.3 + interviews * 0.5 + offers * 1.0) / total * 100) if total > 0 else 0, 1)
            }
        
        # Rank sources by effectiveness
        ranked_sources = sorted(source_stats.items(), key=lambda x: x[1]['effectiveness_score'], reverse=True)
        
        return {
            'source_performance': source_stats,
            'best_sources': [source[0] for source in ranked_sources[:3]],
            'source_recommendations': self._generate_source_recommendations(source_stats)
        }
    
    def _analyze_industry_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze performance across different industries"""
        industry_stats = {}
        
        for industry in df['industry'].unique():
            industry_df = df[df['industry'] == industry]
            total = len(industry_df)
            
            avg_match_score = industry_df['match_score'].mean() if 'match_score' in industry_df.columns else 0
            
            responses = len(industry_df[industry_df['status'] != ApplicationStatus.APPLIED.value])
            offers = len(industry_df[industry_df['status'] == ApplicationStatus.OFFER_RECEIVED.value])
            
            industry_stats[industry] = {
                'total_applications': total,
                'average_match_score': round(avg_match_score, 1),
                'response_rate': round((responses / total * 100) if total > 0 else 0, 1),
                'offer_rate': round((offers / total * 100) if total > 0 else 0, 1)
            }
        
        return {
            'industry_performance': industry_stats,
            'best_performing_industry': max(industry_stats.items(), key=lambda x: x[1]['offer_rate'])[0] if industry_stats else 'N/A'
        }
    
    def _analyze_salary_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze salary trends and ranges"""
        # Extract salary numbers from salary_range strings
        salary_data = []
        
        for _, app in df.iterrows():
            salary_range = app.get('salary_range', '')
            if salary_range:
                # Simple extraction (in production, use more robust parsing)
                numbers = re.findall(r'\$?(\d{1,3}(?:,\d{3})*(?:k|K)?)', salary_range)
                if numbers:
                    try:
                        # Convert to actual numbers
                        salaries = []
                        for num in numbers:
                            if num.endswith(('k', 'K')):
                                salaries.append(float(num[:-1]) * 1000)
                            else:
                                salaries.append(float(num.replace(',', '')))
                        
                        if salaries:
                            avg_salary = sum(salaries) / len(salaries)
                            salary_data.append({
                                'company': app['company_name'],
                                'industry': app['industry'],
                                'position': app['position_title'],
                                'salary': avg_salary,
                                'status': app['status']
                            })
                    except:
                        continue
        
        salary_df = pd.DataFrame(salary_data)
        
        if salary_df.empty:
            return {'error': 'No salary data available'}
        
        return {
            'average_target_salary': round(salary_df['salary'].mean(), 0),
            'salary_range': {
                'min': round(salary_df['salary'].min(), 0),
                'max': round(salary_df['salary'].max(), 0)
            },
            'salary_by_industry': salary_df.groupby('industry')['salary'].mean().round(0).to_dict(),
            'offer_salary_premium': self._calculate_offer_premium(salary_df)
        }
    
    def _identify_success_predictors(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify factors that predict application success"""
        successful_apps = df[df['status'].isin([
            ApplicationStatus.OFFER_RECEIVED.value,
            ApplicationStatus.ACCEPTED.value
        ])]
        
        if len(successful_apps) == 0:
            return {'error': 'No successful applications to analyze'}
        
        # Analyze success factors
        success_factors = {
            'high_match_score': len(successful_apps[successful_apps['match_score'] > 80]) / len(successful_apps) * 100,
            'referral_advantage': len(successful_apps[successful_apps['source'] == 'Referral']) / len(successful_apps) * 100,
            'optimal_timing': self._analyze_timing_success(successful_apps),
            'industry_concentration': successful_apps['industry'].value_counts().head(3).to_dict()
        }
        
        return {
            'success_factors': success_factors,
            'recommendations': self._generate_success_recommendations(success_factors)
        }
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on application data"""
        recommendations = []
        
        # Analyze current performance
        total_apps = len(df)
        response_rate = len(df[df['status'] != ApplicationStatus.APPLIED.value]) / total_apps * 100 if total_apps > 0 else 0
        
        # Response rate recommendations
        if response_rate < 20:
            recommendations.append({
                'category': 'Application Quality',
                'recommendation': 'Your response rate is below average. Focus on improving resume-job match scores and tailoring applications.',
                'priority': 'High',
                'action': 'Review and optimize your resume for each application'
            })
        
        # Application volume recommendations
        apps_per_week = total_apps / max(1, (datetime.now() - df['application_date'].min()).days / 7) if not df.empty else 0
        
        if apps_per_week < 5:
            recommendations.append({
                'category': 'Application Volume',
                'recommendation': 'Consider increasing your application volume to 5-10 applications per week.',
                'priority': 'Medium',
                'action': 'Set a weekly application goal and track progress'
            })
        
        # Source diversification
        unique_sources = df['source'].nunique()
        if unique_sources < 3:
            recommendations.append({
                'category': 'Source Diversification',
                'recommendation': 'Diversify your application sources beyond the current channels.',
                'priority': 'Medium',
                'action': 'Explore company websites, networking events, and industry job boards'
            })
        
        return recommendations
    
    def create_dashboard_visualizations(self, analytics: Dict[str, Any]) -> List[go.Figure]:
        """Create comprehensive dashboard visualizations"""
        figures = []
        
        # 1. Application Pipeline Funnel
        if 'conversion_funnel' in analytics:
            figures.append(self._create_conversion_funnel_chart(analytics['conversion_funnel']))
        
        # 2. Status Distribution Pie Chart
        if 'summary_stats' in analytics:
            figures.append(self._create_status_distribution_chart(analytics['summary_stats']))
        
        # 3. Timeline and Trends
        figures.append(self._create_timeline_chart())
        
        # 4. Source Performance Analysis
        if 'source_analysis' in analytics:
            figures.append(self._create_source_performance_chart(analytics['source_analysis']))
        
        # 5. Industry Performance Comparison
        if 'industry_analysis' in analytics:
            figures.append(self._create_industry_performance_chart(analytics['industry_analysis']))
        
        return figures
    
    def _create_conversion_funnel_chart(self, funnel_data: Dict[str, Any]) -> go.Figure:
        """Create conversion funnel visualization"""
        data = funnel_data['funnel_data']
        
        fig = go.Figure()
        
        # Create funnel chart
        fig.add_trace(go.Funnel(
            y=[item['stage'] for item in data],
            x=[item['count'] for item in data],
            textinfo="value+percent initial",
            marker=dict(
                color=['#3B82F6', '#8B5CF6', '#EC4899', '#EF4444', '#F97316', '#F59E0B', '#10B981', '#059669']
            )
        ))
        
        fig.update_layout(
            title='Application Conversion Funnel',
            height=500
        )
        
        return fig
    
    def _create_status_distribution_chart(self, summary_stats: Dict[str, Any]) -> go.Figure:
        """Create status distribution pie chart"""
        status_dist = summary_stats['status_distribution']
        
        # Map status values to readable labels
        labels = []
        values = []
        colors = []
        
        for status, count in status_dist.items():
            try:
                status_enum = ApplicationStatus(status)
                labels.append(self.pipeline_stages[status_enum]['label'])
                values.append(count)
                colors.append(self.pipeline_stages[status_enum]['color'])
            except:
                labels.append(status.title())
                values.append(count)
                colors.append('#6B7280')
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.4
        )])
        
        fig.update_layout(
            title='Application Status Distribution',
            height=400
        )
        
        return fig
    
    def _create_timeline_chart(self) -> go.Figure:
        """Create application timeline chart"""
        df = self.get_applications_dataframe()
        
        if df.empty:
            return go.Figure().add_annotation(text="No data available")
        
        # Group by week
        df['week'] = df['application_date'].dt.to_period('W').astype(str)
        weekly_counts = df['week'].value_counts().sort_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weekly_counts.index,
            y=weekly_counts.values,
            mode='lines+markers',
            name='Applications per Week',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Application Timeline',
            xaxis_title='Week',
            yaxis_title='Number of Applications',
            height=300
        )
        
        return fig
    
    def _create_source_performance_chart(self, source_analysis: Dict[str, Any]) -> go.Figure:
        """Create source performance comparison"""
        source_perf = source_analysis['source_performance']
        
        sources = list(source_perf.keys())
        response_rates = [source_perf[s]['response_rate'] for s in sources]
        interview_rates = [source_perf[s]['interview_rate'] for s in sources]
        offer_rates = [source_perf[s]['offer_rate'] for s in sources]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Response Rate',
            x=sources,
            y=response_rates,
            marker_color='#3B82F6'
        ))
        
        fig.add_trace(go.Bar(
            name='Interview Rate',
            x=sources,
            y=interview_rates,
            marker_color='#8B5CF6'
        ))
        
        fig.add_trace(go.Bar(
            name='Offer Rate',
            x=sources,
            y=offer_rates,
            marker_color='#10B981'
        ))
        
        fig.update_layout(
            title='Source Performance Comparison',
            xaxis_title='Application Source',
            yaxis_title='Rate (%)',
            barmode='group',
            height=400
        )
        
        return fig
    
    def _create_industry_performance_chart(self, industry_analysis: Dict[str, Any]) -> go.Figure:
        """Create industry performance comparison"""
        industry_perf = industry_analysis['industry_performance']
        
        industries = list(industry_perf.keys())
        match_scores = [industry_perf[i]['average_match_score'] for i in industries]
        response_rates = [industry_perf[i]['response_rate'] for i in industries]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=industries, y=match_scores, name="Match Score", marker_color='#F59E0B'),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=industries, y=response_rates, mode='lines+markers', 
                      name="Response Rate", line=dict(color='#EF4444', width=3)),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Industry")
        fig.update_yaxes(title_text="Match Score", secondary_y=False)
        fig.update_yaxes(title_text="Response Rate (%)", secondary_y=True)
        
        fig.update_layout(
            title='Industry Performance Analysis',
            height=400
        )
        
        return fig
    
    # Helper methods
    def _update_analytics(self):
        """Update analytics cache"""
        # This would typically update cached analytics
        pass
    
    def _get_recent_activity(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Get recent application activity"""
        recent_df = df.sort_values('last_updated', ascending=False).head(5)
        
        activity = []
        for _, app in recent_df.iterrows():
            activity.append({
                'company': app['company_name'],
                'position': app['position_title'],
                'status': self.pipeline_stages.get(ApplicationStatus(app['status']), {'label': app['status']})['label'],
                'date': app['last_updated'].strftime('%Y-%m-%d') if isinstance(app['last_updated'], datetime) else str(app['last_updated'])
            })
        
        return activity
    
    def _calculate_offer_premium(self, salary_df: pd.DataFrame) -> float:
        """Calculate salary premium for offers vs targets"""
        if salary_df.empty:
            return 0
        
        offer_salaries = salary_df[salary_df['status'] == ApplicationStatus.OFFER_RECEIVED.value]['salary']
        all_salaries = salary_df['salary']
        
        if len(offer_salaries) == 0:
            return 0
        
        offer_avg = offer_salaries.mean()
        target_avg = all_salaries.mean()
        
        return round(((offer_avg - target_avg) / target_avg * 100), 1)
    
    def _analyze_timing_success(self, successful_apps: pd.DataFrame) -> Dict[str, Any]:
        """Analyze timing patterns in successful applications"""
        if successful_apps.empty:
            return {}
        
        successful_apps['day_of_week'] = successful_apps['application_date'].dt.day_name()
        day_success = successful_apps['day_of_week'].value_counts()
        
        return {
            'best_day': day_success.index[0] if not day_success.empty else 'N/A',
            'day_distribution': day_success.to_dict()
        }
    
    def _generate_source_recommendations(self, source_stats: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on source performance"""
        recommendations = []
        
        # Find best performing source
        best_source = max(source_stats.items(), key=lambda x: x[1]['effectiveness_score'])
        recommendations.append(f"Focus more on {best_source[0]} - your most effective source")
        
        # Find underperforming sources
        poor_sources = [source for source, stats in source_stats.items() if stats['response_rate'] < 10]
        if poor_sources:
            recommendations.append(f"Consider reducing applications through: {', '.join(poor_sources)}")
        
        return recommendations
    
    def _generate_success_recommendations(self, success_factors: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on success factors"""
        recommendations = []
        
        if success_factors['high_match_score'] > 70:
            recommendations.append("Continue focusing on high-match applications - they're paying off")
        else:
            recommendations.append("Improve resume-job matching - successful applications need higher match scores")
        
        if success_factors['referral_advantage'] > 30:
            recommendations.append("Leverage your network more - referrals are highly effective for you")
        
        return recommendations

import re  # Add this import at the top