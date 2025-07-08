import streamlit as st
import json
from pathlib import Path
from typing import Dict, Any, Optional
import time

class ThemeManager:
    """Advanced theme management system with dark/light mode support"""
    
    def __init__(self):
        self.themes = {
            'light': {
                'primary': '#2563eb',
                'secondary': '#7c3aed',
                'success': '#059669',
                'warning': '#d97706',
                'error': '#dc2626',
                'info': '#0284c7',
                'background': '#ffffff',
                'surface': '#f8fafc',
                'text_primary': '#1f2937',
                'text_secondary': '#6b7280',
                'border': '#e5e7eb',
                'shadow': 'rgba(0, 0, 0, 0.1)'
            },
            'dark': {
                'primary': '#3b82f6',
                'secondary': '#8b5cf6',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'info': '#06b6d4',
                'background': '#111827',
                'surface': '#1f2937',
                'text_primary': '#f9fafb',
                'text_secondary': '#d1d5db',
                'border': '#374151',
                'shadow': 'rgba(0, 0, 0, 0.25)'
            }
        }
    
    def get_current_theme(self) -> str:
        """Get current theme from session state"""
        return st.session_state.get('app_theme', 'light')
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current = self.get_current_theme()
        new_theme = 'dark' if current == 'light' else 'light'
        st.session_state['app_theme'] = new_theme
        st.rerun()
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get colors for current theme"""
        theme = self.get_current_theme()
        return self.themes[theme]

def load_advanced_css():
    """Load advanced CSS with proper theme support"""
    theme_manager = ThemeManager()
    colors = theme_manager.get_theme_colors()
    theme = theme_manager.get_current_theme()
    
    css = f"""
    <style>
    /* CSS Variables for dynamic theming */
    :root {{
        --primary-color: {colors['primary']};
        --secondary-color: {colors['secondary']};
        --success-color: {colors['success']};
        --warning-color: {colors['warning']};
        --error-color: {colors['error']};
        --info-color: {colors['info']};
        --bg-color: {colors['background']};
        --surface-color: {colors['surface']};
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --border-color: {colors['border']};
        --shadow-color: {colors['shadow']};
    }}
    
    /* Main app styling */
    .stApp {{
        background: var(--bg-color);
        color: var(--text-primary);
        transition: all 0.3s ease;
    }}
    
    /* Header with gradient and glass effect */
    .main-header {{
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px var(--shadow-color), 0 10px 10px -5px var(--shadow-color);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
        50% {{ transform: translateX(0%) translateY(0%) rotate(45deg); }}
        100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
    }}
    
    /* Enhanced button styling */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px var(--shadow-color);
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px var(--shadow-color);
    }}
    
    .stButton > button:active {{
        transform: translateY(0px);
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: var(--surface-color);
        border: 2px solid var(--border-color);
        border-radius: 50px;
        padding: 8px 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px var(--shadow-color);
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.05);
    }}
    
    /* Enhanced metric cards */
    div[data-testid="metric-container"] {{
        background: var(--surface-color);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px var(--shadow-color);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 30px var(--shadow-color);
    }}
    
    div[data-testid="metric-container"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }}
    
    /* Enhanced sidebar */
    .css-1d391kg {{
        background: var(--surface-color);
        border-right: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: var(--surface-color);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        color: var(--text-secondary);
        border: none;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        box-shadow: 0 2px 10px var(--shadow-color);
    }}
    
    /* Enhanced file uploader */
    .stFileUploader {{
        background: var(--surface-color);
        padding: 2rem;
        border-radius: 16px;
        border: 2px dashed var(--border-color);
        transition: all 0.3s ease;
        text-align: center;
    }}
    
    .stFileUploader:hover {{
        border-color: var(--primary-color);
        background: var(--bg-color);
        transform: scale(1.02);
    }}
    
    /* Text areas and inputs */
    .stTextArea textarea, .stTextInput input {{
        background: var(--surface-color);
        color: var(--text-primary);
        border: 2px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }}
    
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }}
    
    /* Alert styling */
    .stAlert {{
        background: var(--surface-color);
        color: var(--text-primary);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 10px var(--shadow-color);
    }}
    
    /* Progress indicators */
    .progress-ring {{
        animation: rotate 2s linear infinite;
        filter: drop-shadow(0 4px 8px var(--shadow-color));
    }}
    
    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background: var(--surface-color);
        color: var(--text-primary);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: var(--bg-color);
        border-color: var(--primary-color);
    }}
    
    /* Glass effect cards */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }}
    
    /* Advanced animations */
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .slide-in-left {{
        animation: slideInLeft 0.6s ease-out;
    }}
    
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    .pulse-glow {{
        animation: pulseGlow 2s ease-in-out infinite;
    }}
    
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 5px var(--primary-color); }}
        50% {{ box-shadow: 0 0 20px var(--primary-color), 0 0 30px var(--primary-color); }}
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main-header {{
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .main-header h1 {{
            font-size: 2rem;
        }}
        
        div[data-testid="metric-container"] {{
            padding: 1rem;
        }}
        
        .theme-toggle {{
            position: relative;
            top: auto;
            right: auto;
            margin-bottom: 1rem;
        }}
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--surface-color);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--primary-color);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--secondary-color);
    }}
    
    /* Success/Error states */
    .success-state {{
        background: linear-gradient(135deg, var(--success-color), #34d399);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        animation: successPulse 0.6s ease-out;
    }}
    
    @keyframes successPulse {{
        0% {{ transform: scale(0.95); }}
        50% {{ transform: scale(1.02); }}
        100% {{ transform: scale(1); }}
    }}
    
    .error-state {{
        background: linear-gradient(135deg, var(--error-color), #f87171);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        animation: errorShake 0.6s ease-out;
    }}
    
    @keyframes errorShake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-5px); }}
        75% {{ transform: translateX(5px); }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def create_enhanced_header():
    """Create enhanced header with theme toggle"""
    theme_manager = ThemeManager()
    
    # Theme toggle button
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("🌓" if theme_manager.get_current_theme() == 'light' else "☀️", 
                    help="Toggle theme", key="theme_toggle"):
            theme_manager.toggle_theme()
    
    # Main header
    st.markdown(
        """
        <div class="main-header fade-in">
            <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🎯 SmartATS Pro Elite</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 500;">
                Next-Generation AI Resume Optimization Platform
            </p>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.85;">
                Powered by Google Gemini AI ✨ | ATS Success Guaranteed 🚀
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_enhanced_sidebar():
    """Create enhanced sidebar with advanced features"""
    with st.sidebar:
        st.markdown("## 💼 Job Analysis Center")
        
        # Job description input with enhanced features
        job_description = st.text_area(
            "📋 Job Description",
            height=200,
            placeholder="Paste the complete job description here...\n\nTip: Include requirements, responsibilities, and qualifications for best results!",
            help="💡 Pro tip: The more detailed the job description, the more accurate the analysis!"
        )
        
        # Industry selector
        st.markdown("### 🏢 Industry Focus")
        industry = st.selectbox(
            "Select your target industry",
            [
                "Technology", "Healthcare", "Finance", "Marketing", 
                "Sales", "Education", "Engineering", "Design",
                "Data Science", "Consulting", "Other"
            ],
            help="This helps provide industry-specific optimization tips"
        )
        
        # Experience level
        st.markdown("### 📈 Experience Level")
        experience_level = st.selectbox(
            "Your experience level",
            ["Entry Level (0-2 years)", "Mid Level (3-5 years)", 
             "Senior Level (6-10 years)", "Executive (10+ years)"],
            help="Tailors analysis to your career stage"
        )
        
        # Analysis depth
        st.markdown("### 🔍 Analysis Depth")
        analysis_depth = st.radio(
            "Choose analysis level",
            ["Quick Scan", "Standard Analysis", "Deep Dive"],
            help="Quick: Basic matching | Standard: Comprehensive | Deep Dive: AI-powered insights"
        )
        
        st.markdown("---")
        
        # Enhanced tips section
        st.markdown("### 💡 AI Optimization Tips")
        with st.expander("🎯 ATS Success Strategies", expanded=False):
            st.markdown(
                """
                **🚀 Advanced ATS Optimization:**
                
                **1. Keyword Strategy**
                - Use exact phrases from job descriptions
                - Include both acronyms and full terms (AI & Artificial Intelligence)
                - Implement semantic variations
                
                **2. Format Excellence**
                - Standard fonts: Arial, Calibri, Times New Roman
                - Consistent formatting throughout
                - Clear section headers
                - No images, charts, or graphics
                
                **3. Content Structure**
                - Reverse chronological order
                - Quantified achievements (increased sales by 25%)
                - Action verbs (developed, implemented, optimized)
                - Industry-specific terminology
                
                **4. ATS-Friendly Sections**
                - Professional Summary
                - Core Competencies
                - Work Experience
                - Education & Certifications
                """
            )
        
        with st.expander("📊 Success Metrics", expanded=False):
            st.markdown(
                """
                **🎯 Target Scores:**
                - Keyword Match: 80%+
                - ATS Compatibility: High
                - Skills Coverage: 75%+
                - Industry Alignment: 85%+
                
                **📈 Optimization Goals:**
                - 3x more interview calls
                - 50% faster application process
                - 90% ATS pass-through rate
                """
            )
        
        # Real-time tips based on current state
        if st.session_state.get('analysis_result'):
            st.markdown("### 🔥 Quick Wins")
            analysis = st.session_state.get('analysis_result')
            if analysis.get('match_percentage', 0) < 70:
                st.warning("🎯 Add more job-specific keywords")
            if len(analysis.get('missing_keywords', [])) > 5:
                st.info("💡 Focus on top 5 missing keywords first")
        
        # Session statistics
        st.markdown("---")
        st.markdown("### 📊 Session Stats")
        stats = {
            'Analyses': st.session_state.get('rescore_count', 0) + (1 if st.session_state.get('analysis_result') else 0),
            'Theme': st.session_state.get('app_theme', 'light').title(),
            'Industry': industry
        }
        
        for key, value in stats.items():
            st.metric(key, value)
        
        return job_description, industry, experience_level, analysis_depth

def create_progress_ring(percentage: int, size: int = 120, title: str = "Score"):
    """Create an enhanced progress ring with animations"""
    colors = ThemeManager().get_theme_colors()
    
    # Determine color based on score
    if percentage >= 80:
        color = colors['success']
    elif percentage >= 60:
        color = colors['warning']
    else:
        color = colors['error']
    
    circumference = 2 * 3.14159 * 54  # radius = 54
    stroke_dasharray = f"{percentage/100 * circumference} {circumference}"
    
    st.markdown(
        f"""
        <div style="text-align: center; margin: 1rem 0;">
            <svg width="{size}" height="{size}" viewBox="0 0 120 120" class="progress-ring">
                <!-- Background circle -->
                <circle cx="60" cy="60" r="54" fill="none" 
                        stroke="{colors['border']}" stroke-width="8"/>
                <!-- Progress circle -->
                <circle cx="60" cy="60" r="54" fill="none" 
                        stroke="{color}" stroke-width="8"
                        stroke-dasharray="{stroke_dasharray}"
                        stroke-dashoffset="0"
                        stroke-linecap="round"
                        transform="rotate(-90 60 60)"
                        style="transition: stroke-dasharray 1.5s ease-out;"/>
                <!-- Center text -->
                <text x="60" y="65" text-anchor="middle" 
                      font-size="20" font-weight="bold" fill="{color}">
                    {percentage}%
                </text>
                <text x="60" y="80" text-anchor="middle" 
                      font-size="12" font-weight="500" fill="{colors['text_secondary']}">
                    {title}
                </text>
            </svg>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_enhanced_metrics_dashboard(analysis: Dict[str, Any]):
    """Create an enhanced metrics dashboard"""
    
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        match_score = analysis.get('match_percentage', 0)
        delta_color = "normal" if match_score > 70 else "inverse"
        st.metric(
            "🎯 Match Score",
            f"{match_score}%",
            delta=f"+{match_score-70}" if match_score > 70 else f"{match_score-70}",
            delta_color=delta_color
        )
        create_progress_ring(match_score, 100, "Match")
    
    with col2:
        keywords_found = len(analysis.get('matched_keywords', []))
        keywords_total = keywords_found + len(analysis.get('missing_keywords', []))
        keyword_percentage = int((keywords_found/keywords_total*100) if keywords_total > 0 else 0)
        st.metric(
            "🔑 Keywords",
            f"{keywords_found}/{keywords_total}",
            delta=f"{keyword_percentage}%"
        )
        create_progress_ring(keyword_percentage, 100, "Keywords")
    
    with col3:
        skills_score = analysis.get('skills_coverage', 0)
        st.metric(
            "🛠️ Skills",
            f"{skills_score}%",
            delta="Excellent" if skills_score > 80 else "Good" if skills_score > 60 else "Needs Work",
            delta_color="normal" if skills_score > 60 else "inverse"
        )
        create_progress_ring(skills_score, 100, "Skills")
    
    with col4:
        ats_rating = analysis.get('ats_friendliness', 'Medium')
        rating_score = {"High": 90, "Medium": 70, "Low": 40}.get(ats_rating, 70)
        rating_emoji = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}.get(ats_rating, "🟡")
        st.metric(
            "🤖 ATS Ready",
            f"{rating_emoji} {ats_rating}",
            delta="Optimized" if ats_rating == "High" else "Improving" if ats_rating == "Medium" else "Action Needed"
        )
        create_progress_ring(rating_score, 100, "ATS")

def create_feature_cards():
    """Create feature showcase cards"""
    st.markdown("### 🚀 Platform Features")
    
    features = [
        {
            "icon": "🤖",
            "title": "AI-Powered Analysis",
            "description": "Advanced Gemini AI provides deep insights and optimization suggestions",
            "color": "primary"
        },
        {
            "icon": "📊",
            "title": "Real-time Scoring",
            "description": "Instant feedback with detailed metrics and improvement areas",
            "color": "secondary"
        },
        {
            "icon": "🎯",
            "title": "ATS Simulation",
            "description": "Test how your resume performs against real ATS systems",
            "color": "success"
        },
        {
            "icon": "📈",
            "title": "Progress Tracking",
            "description": "Monitor improvements and track optimization journey",
            "color": "info"
        }
    ]
    
    cols = st.columns(len(features))
    
    for i, feature in enumerate(features):
        with cols[i]:
            st.markdown(
                f"""
                <div class="glass-card fade-in" style="text-align: center; animation-delay: {i*0.1}s;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">{feature['icon']}</div>
                    <h4 style="margin: 0.5rem 0; color: var(--{feature['color']}-color);">{feature['title']}</h4>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{feature['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

def show_success_animation(message: str):
    """Show success animation with message"""
    st.markdown(
        f"""
        <div class="success-state">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
                <div style="font-size: 1.5rem;">✅</div>
                <div>{message}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_error_animation(message: str):
    """Show error animation with message"""
    st.markdown(
        f"""
        <div class="error-state">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
                <div style="font-size: 1.5rem;">❌</div>
                <div>{message}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_loading_spinner(message: str = "Processing..."):
    """Create enhanced loading spinner"""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 2rem;">
            <div class="progress-ring pulse-glow">
                <svg width="60" height="60" viewBox="0 0 60 60">
                    <circle cx="30" cy="30" r="25" fill="none" 
                            stroke="var(--primary-color)" stroke-width="4" 
                            stroke-dasharray="40 40" transform="rotate(-90 30 30)"/>
                </svg>
            </div>
            <p style="margin-top: 1rem; color: var(--primary-color); font-weight: 600; font-size: 1.1rem;">
                {message}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )