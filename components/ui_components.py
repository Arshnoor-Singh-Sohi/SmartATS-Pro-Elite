import streamlit as st
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any

def load_custom_css():
    """Load enhanced CSS with professional dark theme"""
    css = """
    <style>
    /* App background: clean dark theme */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
        color: #f8f9fa;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #111111 0%, #1a1a1a 100%);
        border-right: 1px solid #333333;
    }

    /* Enhanced header */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1e40af 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    .main-header h1 {
        color: #ffffff;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .main-header p {
        color: #e0e7ff;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }

    /* Enhanced metrics cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #333333;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: #3b82f6;
    }

    /* Text styling */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: #f8f9fa !important;
    }

    /* Enhanced expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%) !important;
        color: #f8f9fa !important;
        border-radius: 8px !important;
        border: 1px solid #333333 !important;
    }

    /* Enhanced alerts */
    .stAlert {
        background: rgba(42, 42, 42, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid #333333;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
    }

    /* Input fields */
    textarea, input {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        color: #f8f9fa !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }

    textarea:focus, input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(26, 26, 26, 0.8);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #333333;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #9ca3af;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    }

    /* File uploader */
    .stFileUploader {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 2px dashed #3b82f6;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: #60a5fa;
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
    }

    /* Success/Error states */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
    }

    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        border: none;
    }

    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border: none;
    }

    .stInfo {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        border: none;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #60a5fa;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_header():
    """Create enhanced header with animations"""
    st.markdown(
        """
        <div class="main-header">
            <h1>🎯 SmartATS Pro Elite</h1>
            <p>Next-Generation AI Resume Optimization Platform</p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">
                Powered by Google Gemini AI ✨ | ATS Success Guaranteed 🚀
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_sidebar():
    """Create enhanced sidebar with advanced options"""
    with st.sidebar:
        st.markdown("## 💼 Analysis Configuration")
        
        # Job description input
        job_description = st.text_area(
            "📋 Job Description",
            height=200,
            placeholder="Paste the complete job description here...\n\nTip: Include requirements, responsibilities, and qualifications for best results!",
            help="💡 Pro tip: The more detailed the job description, the more accurate the analysis!"
        )
        
        # Enhanced configuration options
        st.markdown("### 🎯 Analysis Settings")
        
        # Industry selector
        industry = st.selectbox(
            "🏢 Target Industry",
            [
                "Technology", "Healthcare", "Finance", "Marketing", 
                "Sales", "Education", "Engineering", "Design",
                "Data Science", "Consulting", "Other"
            ],
            help="This helps provide industry-specific optimization tips"
        )
        
        # Experience level
        experience_level = st.selectbox(
            "📈 Experience Level",
            ["Entry Level (0-2 years)", "Mid Level (3-5 years)", 
             "Senior Level (6-10 years)", "Executive (10+ years)"],
            help="Tailors analysis to your career stage"
        )
        
        # Analysis depth
        analysis_depth = st.radio(
            "🔍 Analysis Depth",
            ["Quick Scan", "Standard Analysis", "Deep Dive"],
            help="Quick: Basic matching | Standard: Comprehensive | Deep Dive: AI-powered insights"
        )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            include_market_data = st.checkbox("📊 Include Market Intelligence", value=True)
            include_suggestions = st.checkbox("💡 AI Optimization Suggestions", value=True)
            competitive_analysis = st.checkbox("🏆 Competitive Analysis", value=False)
        
        st.markdown("---")
        
        # Tips section
        st.markdown("### 💡 Optimization Tips")
        with st.expander("🎯 ATS Success Strategies", expanded=False):
            st.markdown(
                """
                **🚀 Advanced ATS Optimization:**
                
                **1. Keyword Strategy**
                - Use exact phrases from job descriptions
                - Include both acronyms and full terms
                - Implement semantic variations
                
                **2. Format Excellence**
                - Standard fonts (Arial, Calibri, Times New Roman)
                - Consistent formatting throughout
                - Clear section headers
                
                **3. Content Structure**
                - Reverse chronological order
                - Quantified achievements
                - Action verbs and results
                """
            )
        
        return job_description, industry, experience_level, analysis_depth

def display_metrics_cards(analysis: Dict):
    """Display enhanced metrics cards"""
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        match_score = analysis.get('match_percentage', 0)
        st.metric(
            "🎯 Match Score",
            f"{match_score}%",
            delta=f"+{match_score-70}" if match_score > 70 else f"{match_score-70}",
            delta_color="normal" if match_score > 70 else "inverse"
        )
        create_progress_ring(match_score)
    
    with metrics_col2:
        keywords_found = len(analysis.get('matched_keywords', []))
        keywords_total = keywords_found + len(analysis.get('missing_keywords', []))
        st.metric(
            "🔑 Keywords",
            f"{keywords_found}/{keywords_total}",
            delta=f"{(keywords_found/keywords_total*100):.0f}%" if keywords_total > 0 else "0%"
        )
    
    with metrics_col3:
        skills_score = analysis.get('skills_coverage', 0)
        st.metric(
            "🛠️ Skills",
            f"{skills_score}%",
            delta="Excellent" if skills_score > 80 else "Good" if skills_score > 60 else "Needs Work",
            delta_color="normal" if skills_score > 60 else "inverse"
        )
    
    with metrics_col4:
        ats_rating = analysis.get('ats_friendliness', 'Medium')
        rating_emoji = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}.get(ats_rating, "🟡")
        st.metric(
            "🤖 ATS Ready",
            f"{rating_emoji} {ats_rating}",
            delta="Optimized" if ats_rating == "High" else "Improving"
        )

def create_progress_ring(percentage: int, size: int = 100, title: str = "Score"):
    """Create animated progress ring"""
    # Determine color based on score
    if percentage >= 80:
        color = "#10B981"  # Green
    elif percentage >= 60:
        color = "#F59E0B"  # Orange  
    else:
        color = "#EF4444"  # Red
    
    # Calculate circumference
    radius = 35
    circumference = 2 * 3.14159 * radius
    stroke_dasharray = f"{percentage/100 * circumference} {circumference}"
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin: 1rem 0;">
            <svg width="{size}" height="{size}" viewBox="0 0 80 80">
                <!-- Background circle -->
                <circle cx="40" cy="40" r="{radius}" fill="none" 
                        stroke="#333333" stroke-width="8"/>
                <!-- Progress circle -->
                <circle cx="40" cy="40" r="{radius}" fill="none" 
                        stroke="{color}" stroke-width="8"
                        stroke-dasharray="{stroke_dasharray}"
                        stroke-dashoffset="0"
                        stroke-linecap="round"
                        transform="rotate(-90 40 40)"
                        style="transition: stroke-dasharray 2s ease-out;"/>
                <!-- Center text -->
                <text x="40" y="45" text-anchor="middle" 
                      font-size="12" font-weight="bold" fill="{color}">
                    {percentage}%
                </text>
            </svg>
        </div>
        """,
        unsafe_allow_html=True
    )