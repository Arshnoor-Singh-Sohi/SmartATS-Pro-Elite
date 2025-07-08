import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
import io
import base64
from datetime import datetime, timedelta
import colorsys

class AdvancedVisualizationEngine:
    """
    Advanced visualization engine with interactive charts and comprehensive analytics
    """
    
    def __init__(self):
        # Modern color palette with accessibility in mind
        self.color_palette = {
            'primary': '#3B82F6',      # Blue
            'secondary': '#8B5CF6',    # Purple
            'success': '#10B981',      # Green
            'warning': '#F59E0B',      # Orange
            'danger': '#EF4444',       # Red
            'info': '#06B6D4',         # Cyan
            'light': '#F8FAFC',        # Light gray
            'dark': '#1E293B',         # Dark gray
            'gradient_start': '#667EEA',
            'gradient_end': '#764BA2'
        }
        
        # Chart templates for consistency
        self.chart_template = {
            'layout': {
                'font': {'family': 'Inter, sans-serif', 'size': 12},
                'colorway': list(self.color_palette.values())[:8],
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'margin': {'t': 60, 'b': 50, 'l': 50, 'r': 50}
            }
        }
    
    def create_comprehensive_dashboard(self, analysis: Dict[str, Any]) -> go.Figure:
        """
        Create a comprehensive dashboard with multiple metrics
        """
        # Create subplot figure with different chart types
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=[
                "Overall Performance", "Skills Breakdown", "Keyword Match Rate",
                "ATS Compatibility", "Industry Alignment", "Competitive Position",
                "Content Quality", "Career Progression", "Success Prediction"
            ],
            specs=[
                [{"type": "indicator"}, {"type": "scatterpolar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "pie"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "scatter"}, {"type": "indicator"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )
        
        # 1. Overall Performance Gauge
        overall_score = analysis.get('overall_score', 75)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=overall_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Score"},
                delta={'reference': 70},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': self._get_score_color(overall_score)},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 80], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=1, col=1
        )
        
        # 2. Skills Radar Chart
        skills_data = analysis.get('skills_analysis', {})
        if skills_data:
            categories = list(skills_data.keys())
            values = list(skills_data.values())
            
            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=[cat.replace('_', ' ').title() for cat in categories],
                    fill='toself',
                    fillcolor='rgba(59, 130, 246, 0.3)',
                    line=dict(color=self.color_palette['primary']),
                    name="Skills"
                ),
                row=1, col=2
            )
        
        # 3. Keyword Match Rate
        keyword_analysis = analysis.get('keyword_analysis', {})
        matched = len(keyword_analysis.get('matched_keywords', []))
        missing = len(keyword_analysis.get('missing_critical_keywords', []))
        
        fig.add_trace(
            go.Bar(
                x=['Matched', 'Missing Critical'],
                y=[matched, missing],
                marker_color=[self.color_palette['success'], self.color_palette['danger']],
                name="Keywords"
            ),
            row=1, col=3
        )
        
        # 4. ATS Compatibility Scatter
        ats_data = analysis.get('ats_analysis', {})
        if ats_data:
            ats_metrics = list(ats_data.keys())
            ats_values = list(ats_data.values())
            
            # Convert string values to numeric for visualization
            ats_numeric = []
            for val in ats_values:
                if isinstance(val, str):
                    if val == 'High':
                        ats_numeric.append(90)
                    elif val == 'Medium':
                        ats_numeric.append(70)
                    elif val == 'Low':
                        ats_numeric.append(40)
                    else:
                        ats_numeric.append(50)
                else:
                    ats_numeric.append(val)
            
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(ats_metrics))),
                    y=ats_numeric,
                    mode='lines+markers',
                    line=dict(color=self.color_palette['info'], width=3),
                    marker=dict(size=8),
                    name="ATS Metrics"
                ),
                row=2, col=1
            )
        
        # 5. Industry Fit Pie Chart
        industry_data = analysis.get('industry_fit', {})
        if industry_data:
            labels = [key.replace('_', ' ').title() for key in industry_data.keys()]
            values = list(industry_data.values())
            
            fig.add_trace(
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker_colors=[self.color_palette['primary'], self.color_palette['secondary'], 
                                 self.color_palette['success'], self.color_palette['warning']]
                ),
                row=2, col=2
            )
        
        # 6. Competitive Position
        comp_data = analysis.get('competitive_positioning', {})
        competitiveness = comp_data.get('market_competitiveness', 65)
        
        fig.add_trace(
            go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=[40, 60, competitiveness, 80, 95],
                mode='lines+markers',
                line=dict(color=self.color_palette['secondary'], width=4),
                marker=dict(size=10, color=self.color_palette['secondary']),
                name="Market Position"
            ),
            row=2, col=3
        )
        
        # 7. Content Quality Bar Chart
        content_data = analysis.get('content_quality', {})
        if content_data:
            content_labels = [key.replace('_', ' ').title() for key in content_data.keys()]
            content_values = list(content_data.values())
            
            fig.add_trace(
                go.Bar(
                    x=content_values,
                    y=content_labels,
                    orientation='h',
                    marker_color=self.color_palette['gradient_start'],
                    name="Content Quality"
                ),
                row=3, col=1
            )
        
        # 8. Career Trajectory
        career_data = analysis.get('career_trajectory', {})
        if career_data:
            trajectory_score = career_data.get('career_progression_score', 70)
            leadership_score = career_data.get('leadership_readiness', 60)
            
            fig.add_trace(
                go.Scatter(
                    x=[1, 2, 3, 4, 5],
                    y=[30, 50, leadership_score, trajectory_score, 90],
                    mode='lines+markers+text',
                    text=['Entry', 'Junior', 'Current', 'Target', 'Senior'],
                    textposition="top center",
                    line=dict(color=self.color_palette['success'], width=3),
                    marker=dict(size=8),
                    name="Career Path"
                ),
                row=3, col=2
            )
        
        # 9. Success Prediction Gauge
        success_data = analysis.get('success_prediction', {})
        success_prob = success_data.get('success_probability', 65)
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=success_prob,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Success %"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': self._get_score_color(success_prob)},
                    'steps': [
                        {'range': [0, 40], 'color': "lightcoral"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ]
                }
            ),
            row=3, col=3
        )
        
        # Update layout
        fig.update_layout(
            height=900,
            showlegend=False,
            title_text="Comprehensive Resume Analysis Dashboard",
            title_x=0.5,
            title_font_size=20,
            **self.chart_template['layout']
        )
        
        return fig
    
    def create_timeline_analysis(self, analysis: Dict[str, Any]) -> go.Figure:
        """
        Create a timeline showing optimization progress
        """
        # Simulate historical data and future projections
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        
        # Current score
        current_score = analysis.get('match_percentage', 70)
        
        # Generate realistic progression
        scores = []
        base_score = max(30, current_score - 20)  # Starting point
        
        for i, date in enumerate(dates):
            if i < 6:  # Historical data
                score = base_score + (i * 5) + np.random.normal(0, 3)
            elif i == 6:  # Current month
                score = current_score
            else:  # Future projections
                improvement_rate = 3 if current_score < 70 else 2 if current_score < 85 else 1
                score = current_score + ((i - 6) * improvement_rate)
            
            scores.append(min(95, max(20, score)))  # Keep realistic bounds
        
        fig = go.Figure()
        
        # Historical performance
        fig.add_trace(go.Scatter(
            x=dates[:7],
            y=scores[:7],
            mode='lines+markers',
            name='Historical Performance',
            line=dict(color=self.color_palette['primary'], width=3),
            marker=dict(size=8)
        ))
        
        # Future projections
        fig.add_trace(go.Scatter(
            x=dates[6:],
            y=scores[6:],
            mode='lines+markers',
            name='Projected Improvement',
            line=dict(color=self.color_palette['success'], width=3, dash='dash'),
            marker=dict(size=8, symbol='diamond')
        ))
        
        # Add milestone markers
        milestones = [
            {'date': dates[6], 'score': scores[6], 'text': 'Current Score'},
            {'date': dates[9], 'score': scores[9], 'text': '3-Month Target'},
            {'date': dates[11], 'score': scores[11], 'text': '6-Month Goal'}
        ]
        
        for milestone in milestones:
            fig.add_annotation(
                x=milestone['date'],
                y=milestone['score'],
                text=f"{milestone['text']}<br>{milestone['score']:.0f}%",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=self.color_palette['warning'],
                bgcolor=self.color_palette['warning'],
                bordercolor=self.color_palette['warning'],
                font=dict(color='white')
            )
        
        fig.update_layout(
            title='Resume Optimization Timeline & Projections',
            xaxis_title='Date',
            yaxis_title='Match Score (%)',
            height=500,
            hovermode='x unified',
            **self.chart_template['layout']
        )
        
        return fig
    
    def create_competitor_benchmark(self, analysis: Dict[str, Any]) -> go.Figure:
        """
        Create a competitive benchmarking visualization
        """
        # Simulate competitive landscape data
        categories = ['Keyword Match', 'Skills Coverage', 'ATS Compatibility', 
                     'Industry Fit', 'Experience Level', 'Content Quality']
        
        # User's scores
        user_scores = [
            analysis.get('match_percentage', 70),
            analysis.get('skills_analysis', {}).get('technical_skills', 65),
            analysis.get('ats_compatibility_score', 75),
            analysis.get('industry_fit', {}).get('industry_terminology', 70),
            75,  # Experience level match
            sum(analysis.get('content_quality', {}).values()) / 
            len(analysis.get('content_quality', {})) if analysis.get('content_quality') else 70
        ]
        
        # Market benchmarks (simulated)
        market_avg = [65, 60, 70, 65, 70, 65]
        top_10_percent = [90, 85, 90, 88, 85, 88]
        top_25_percent = [80, 75, 82, 78, 80, 78]
        
        fig = go.Figure()
        
        # Add traces for each benchmark
        fig.add_trace(go.Scatterpolar(
            r=user_scores,
            theta=categories,
            fill='toself',
            fillcolor='rgba(59, 130, 246, 0.3)',
            line=dict(color=self.color_palette['primary'], width=3),
            name="Your Resume"
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=top_10_percent,
            theta=categories,
            line=dict(color=self.color_palette['success'], width=2, dash='dash'),
            name="Top 10%"
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=top_25_percent,
            theta=categories,
            line=dict(color=self.color_palette['warning'], width=2, dash='dot'),
            name="Top 25%"
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=market_avg,
            theta=categories,
            line=dict(color=self.color_palette['danger'], width=2),
            name="Market Average"
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickvals=[20, 40, 60, 80, 100],
                    ticktext=['20%', '40%', '60%', '80%', '100%']
                )
            ),
            title='Competitive Benchmark Analysis',
            height=600,
            **self.chart_template['layout']
        )
        
        return fig
    
    def create_skill_gap_heatmap(self, analysis: Dict[str, Any]) -> go.Figure:
        """
        Create a heatmap showing skill gaps across different categories
        """
        # Skill categories and their importance levels
        skill_categories = {
            'Technical Skills': ['Python', 'SQL', 'JavaScript', 'AWS', 'Docker'],
            'Soft Skills': ['Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Creativity'],
            'Industry Knowledge': ['Domain Expertise', 'Compliance', 'Best Practices', 'Trends', 'Regulations'],
            'Tools & Platforms': ['Git', 'Jira', 'Slack', 'Confluence', 'Analytics']
        }
        
        # Simulate skill assessment data
        np.random.seed(42)  # For consistent results
        
        skills_data = []
        importance_data = []
        gap_data = []
        
        for category, skills in skill_categories.items():
            for skill in skills:
                current_level = np.random.randint(30, 90)
                required_level = np.random.randint(70, 95)
                importance = np.random.randint(60, 100)
                gap = max(0, required_level - current_level)
                
                skills_data.append({
                    'Category': category,
                    'Skill': skill,
                    'Current': current_level,
                    'Required': required_level,
                    'Gap': gap,
                    'Importance': importance
                })
        
        df = pd.DataFrame(skills_data)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=df.pivot(index='Skill', columns='Category', values='Gap').values,
            x=df['Category'].unique(),
            y=df.pivot(index='Skill', columns='Category', values='Gap').index,
            colorscale=[
                [0, self.color_palette['success']],
                [0.5, self.color_palette['warning']],
                [1, self.color_palette['danger']]
            ],
            colorbar=dict(
                title="Skill Gap",
                titleside="right",
                tickmode="array",
                tickvals=[0, 25, 50],
                ticktext=["No Gap", "Moderate", "High Gap"]
            )
        ))
        
        fig.update_layout(
            title='Skill Gap Analysis Heatmap',
            xaxis_title='Skill Categories',
            yaxis_title='Individual Skills',
            height=600,
            **self.chart_template['layout']
        )
        
        return fig
    
    def create_optimization_roadmap_gantt(self, analysis: Dict[str, Any]) -> go.Figure:
        """
        Create a Gantt chart for optimization roadmap
        """
        # Get optimization roadmap from analysis
        roadmap = analysis.get('optimization_roadmap', [])
        
        if not roadmap:
            # Create sample roadmap
            roadmap = [
                {
                    'action': 'Add Critical Keywords',
                    'priority': 'Critical',
                    'effort': 'Low',
                    'timeframe': 'Immediate'
                },
                {
                    'action': 'Improve ATS Formatting',
                    'priority': 'High',
                    'effort': 'Medium',
                    'timeframe': 'Short-term'
                },
                {
                    'action': 'Quantify Achievements',
                    'priority': 'High',
                    'effort': 'Medium',
                    'timeframe': 'Short-term'
                },
                {
                    'action': 'Add Industry Certifications',
                    'priority': 'Medium',
                    'effort': 'High',
                    'timeframe': 'Long-term'
                }
            ]
        
        # Convert to Gantt chart data
        tasks = []
        start_date = datetime.now()
        
        for i, item in enumerate(roadmap):
            # Determine duration based on effort and timeframe
            if item.get('timeframe') == 'Immediate':
                duration = 1
            elif item.get('timeframe') == 'Short-term':
                duration = 7
            else:
                duration = 30
            
            if item.get('effort') == 'High':
                duration *= 2
            elif item.get('effort') == 'Low':
                duration = max(1, duration // 2)
            
            start = start_date + timedelta(days=i*2)
            end = start + timedelta(days=duration)
            
            tasks.append({
                'Task': item['action'],
                'Start': start,
                'End': end,
                'Priority': item.get('priority', 'Medium'),
                'Effort': item.get('effort', 'Medium')
            })
        
        # Create Gantt chart
        fig = go.Figure()
        
        priority_colors = {
            'Critical': self.color_palette['danger'],
            'High': self.color_palette['warning'],
            'Medium': self.color_palette['info'],
            'Low': self.color_palette['success']
        }
        
        for i, task in enumerate(tasks):
            fig.add_trace(go.Scatter(
                x=[task['Start'], task['End']],
                y=[i, i],
                mode='lines+markers',
                line=dict(
                    color=priority_colors.get(task['Priority'], self.color_palette['primary']),
                    width=20
                ),
                marker=dict(size=8),
                name=task['Task'],
                hovertemplate=f"<b>{task['Task']}</b><br>" +
                             f"Priority: {task['Priority']}<br>" +
                             f"Effort: {task['Effort']}<br>" +
                             f"Duration: {(task['End'] - task['Start']).days} days<extra></extra>"
            ))
        
        fig.update_layout(
            title='Optimization Roadmap Timeline',
            xaxis_title='Timeline',
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(len(tasks))),
                ticktext=[task['Task'] for task in tasks]
            ),
            height=400 + len(tasks) * 30,
            showlegend=False,
            **self.chart_template['layout']
        )
        
        return fig
    
    def create_advanced_word_cloud(self, resume_text: str, 
                                 job_description: str,
                                 matched_keywords: List[str] = None,
                                 missing_keywords: List[str] = None) -> str:
        """
        Create an advanced word cloud with keyword highlighting
        """
        # Combine texts but weight job description keywords higher
        combined_text = resume_text + " " + (job_description * 2)
        
        # Custom color function
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            if matched_keywords and word.lower() in [k.lower() for k in matched_keywords]:
                return self.color_palette['success']
            elif missing_keywords and word.lower() in [k.lower() for k in missing_keywords]:
                return self.color_palette['danger']
            else:
                # Generate random color from palette
                colors = [self.color_palette['primary'], self.color_palette['secondary'], 
                         self.color_palette['info']]
                return colors[hash(word) % len(colors)]
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            color_func=color_func,
            max_words=150,
            relative_scaling=0.3,
            min_font_size=12,
            max_font_size=80,
            collocations=False
        ).generate(combined_text)
        
        # Create figure with matplotlib
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Resume & Job Description Word Cloud Analysis', 
                 fontsize=20, fontweight='bold', pad=20)
        
        # Add legend
        legend_elements = []
        if matched_keywords:
            legend_elements.append(plt.Line2D([0], [0], marker='s', color='w', 
                                            markerfacecolor=self.color_palette['success'],
                                            markersize=10, label='Matched Keywords'))
        if missing_keywords:
            legend_elements.append(plt.Line2D([0], [0], marker='s', color='w',
                                            markerfacecolor=self.color_palette['danger'],
                                            markersize=10, label='Missing Keywords'))
        
        if legend_elements:
            plt.legend(handles=legend_elements, loc='upper right', fontsize=12)
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', 
                   dpi=150, facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        plt.close()
        
        # Convert to base64
        img_str = base64.b64encode(img_buffer.read()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def create_score_evolution_chart(self, analysis: Dict[str, Any]) -> go.Figure:
        """
        Create a chart showing how scores change with different optimizations
        """
        # Simulate score evolution with different optimizations
        optimizations = [
            'Current Resume',
            '+ Critical Keywords',
            '+ ATS Formatting',
            '+ Quantified Results',
            '+ Industry Terms',
            '+ Skill Certifications'
        ]
        
        current_score = analysis.get('match_percentage', 70)
        
        # Simulate progressive improvements
        scores = [
            current_score,
            min(95, current_score + 12),  # Keywords boost
            min(95, current_score + 18),  # + ATS formatting
            min(95, current_score + 23),  # + Quantification
            min(95, current_score + 27),  # + Industry terms
            min(95, current_score + 30)   # + Certifications
        ]
        
        # Create waterfall-style chart
        fig = go.Figure()
        
        # Base bar
        fig.add_trace(go.Bar(
            x=optimizations,
            y=scores,
            marker_color=[
                self.color_palette['primary'] if i == 0 
                else self.color_palette['success'] 
                for i in range(len(optimizations))
            ],
            text=[f'{score:.0f}%' for score in scores],
            textposition='outside',
            name='Match Score'
        ))
        
        # Add improvement annotations
        for i in range(1, len(scores)):
            improvement = scores[i] - scores[i-1]
            fig.add_annotation(
                x=i,
                y=scores[i-1] + improvement/2,
                text=f'+{improvement:.0f}%',
                showarrow=True,
                arrowhead=2,
                arrowcolor=self.color_palette['success'],
                font=dict(color=self.color_palette['success'], weight='bold')
            )
        
        fig.update_layout(
            title='Score Evolution with Progressive Optimizations',
            xaxis_title='Optimization Steps',
            yaxis_title='Match Score (%)',
            yaxis_range=[0, 100],
            height=500,
            **self.chart_template['layout']
        )
        
        return fig
    
    def _get_score_color(self, score: float) -> str:
        """Get color based on score value"""
        if score >= 80:
            return self.color_palette['success']
        elif score >= 60:
            return self.color_palette['warning']
        else:
            return self.color_palette['danger']
    
    def _generate_color_scale(self, n_colors: int) -> List[str]:
        """Generate a color scale with n colors"""
        colors = []
        for i in range(n_colors):
            hue = i / n_colors
            rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
            hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            colors.append(hex_color)
        return colors