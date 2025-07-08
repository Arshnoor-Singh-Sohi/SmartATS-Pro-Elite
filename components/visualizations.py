import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import io
import base64

class VisualizationEngine:
    """
    Creates interactive visualizations for resume analysis results
    """
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#48bb78',
            'warning': '#f6ad55',
            'danger': '#f56565',
            'info': '#4299e1'
        }
    
    def create_keyword_chart(self, matched_keywords: List[str], 
                           missing_keywords: List[str]) -> go.Figure:
        """
        Create an interactive bar chart showing keyword analysis
        """
        # Prepare data
        all_keywords = matched_keywords[:10] + missing_keywords[:10]
        values = [1] * len(matched_keywords[:10]) + [0] * len(missing_keywords[:10])
        colors = [self.color_scheme['success']] * len(matched_keywords[:10]) + \
                [self.color_scheme['danger']] * len(missing_keywords[:10])
        
        # Create figure
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=all_keywords,
            y=[100 if v == 1 else 50 for v in values],
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>Status: %{text}<extra></extra>',
            text=['Matched' if v == 1 else 'Missing' for v in values],
            name='Keywords'
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Keyword Analysis: Matched vs Missing',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='Keywords',
            yaxis_title='Match Status',
            yaxis={'tickvals': [0, 50, 100], 'ticktext': ['', 'Missing', 'Matched']},
            showlegend=False,
            height=400,
            template='plotly_white',
            hovermode='x unified'
        )
        
        # Add custom styling
        fig.update_xaxes(tickangle=-45)
        
        return fig
    
    def create_skills_radar(self, skills_analysis: Dict[str, int]) -> go.Figure:
        """
        Create a radar chart for skills analysis
        """
        # Prepare data
        categories = list(skills_analysis.keys())
        values = list(skills_analysis.values())
        
        # Ensure we have a complete circle
        categories = [cat.replace('_', ' ').title() for cat in categories]
        values.append(values[0])
        categories.append(categories[0])
        
        # Create figure
        fig = go.Figure()
        
        # Add trace
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color=self.color_scheme['primary'], width=2),
            marker=dict(size=8, color=self.color_scheme['primary']),
            hovertemplate='<b>%{theta}</b><br>Score: %{r}%<extra></extra>',
            name='Skills'
        ))
        
        # Add reference line at 70%
        fig.add_trace(go.Scatterpolar(
            r=[70] * len(categories),
            theta=categories,
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['0%', '25%', '50%', '75%', '100%']
                )
            ),
            title={
                'text': 'Skills Coverage Analysis',
                'x': 0.5,
                'xanchor': 'center'
            },
            showlegend=False,
            height=450,
            template='plotly_white'
        )
        
        return fig
    
    def create_word_cloud(self, text: str, important_terms: List[str]) -> str:
        """
        Create a word cloud visualization from resume text
        """
        # Create custom colormap
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            if word.lower() in [term.lower() for term in important_terms]:
                return self.color_scheme['primary']
            return self.color_scheme['secondary']
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            color_func=color_func,
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)
        
        # Create figure
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Resume Keywords Visualization', fontsize=16, pad=20)
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        plt.close()
        
        # Convert to base64
        img_str = base64.b64encode(img_buffer.read()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def create_detailed_breakdown(self, analysis: Dict[str, Any]) -> go.Figure:
        """
        Create a comprehensive breakdown chart
        """
        # Extract score breakdown
        score_breakdown = analysis.get('score_breakdown', {
            'keyword_match': 70,
            'skills_alignment': 75,
            'experience_relevance': 80,
            'education_fit': 85,
            'overall_presentation': 90
        })
        
        # Prepare data
        categories = [cat.replace('_', ' ').title() for cat in score_breakdown.keys()]
        values = list(score_breakdown.values())
        
        # Create figure with subplots
        fig = go.Figure()
        
        # Add horizontal bar chart
        colors = [self._get_color_by_score(v) for v in values]
        
        fig.add_trace(go.Bar(
            y=categories,
            x=values,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            text=[f'{v}%' for v in values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Score: %{x}%<extra></extra>'
        ))
        
        # Add target line at 80%
        fig.add_vline(
            x=80, 
            line_dash="dash", 
            line_color="gray",
            annotation_text="Target: 80%",
            annotation_position="top"
        )
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Detailed Score Breakdown',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='Score (%)',
            yaxis_title='',
            xaxis_range=[0, 100],
            showlegend=False,
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    def create_match_gauge(self, match_percentage: int) -> go.Figure:
        """
        Create a gauge chart for match percentage
        """
        # Determine color based on score
        if match_percentage >= 80:
            color = self.color_scheme['success']
        elif match_percentage >= 60:
            color = self.color_scheme['warning']
        else:
            color = self.color_scheme['danger']
        
        # Create figure
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=match_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Match Score"},
            delta={'reference': 70, 'relative': True},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        # Update layout
        fig.update_layout(
            height=300,
            template='plotly_white'
        )
        
        return fig
    
    def create_comparison_chart(self, resume_data: Dict[str, Any], 
                              target_data: Dict[str, Any]) -> go.Figure:
        """
        Create a comparison chart between resume and job requirements
        """
        categories = ['Experience', 'Skills', 'Education', 'Keywords', 'Overall']
        
        # Create figure with grouped bars
        fig = go.Figure()
        
        # Add resume scores
        fig.add_trace(go.Bar(
            name='Your Resume',
            x=categories,
            y=[75, 80, 85, 70, 77],  # Example values
            marker_color=self.color_scheme['primary']
        ))
        
        # Add target scores
        fig.add_trace(go.Bar(
            name='Job Requirements',
            x=categories,
            y=[80, 85, 80, 90, 84],  # Example values
            marker_color=self.color_scheme['secondary']
        ))
        
        # Update layout
        fig.update_layout(
            title='Resume vs Job Requirements',
            xaxis_title='Categories',
            yaxis_title='Score (%)',
            barmode='group',
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    def _get_color_by_score(self, score: int) -> str:
        """
        Get color based on score value
        """
        if score >= 80:
            return self.color_scheme['success']
        elif score >= 60:
            return self.color_scheme['warning']
        else:
            return self.color_scheme['danger']