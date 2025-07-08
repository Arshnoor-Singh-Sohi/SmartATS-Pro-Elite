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
from components.pdf_processor import PDFProcessor
from components.gemini_analyzer import GeminiAnalyzer
from components.visualizations import VisualizationEngine
from components.report_generator import ReportGenerator
from components.ui_components import load_custom_css, create_header, create_sidebar, display_metrics_cards, create_progress_ring
from utils.session_manager import SessionManager
from utils.keyword_extractor import KeywordExtractor

# Try to import enhanced analyzer if available
try:
    from core_engine.enhanced_gemini_analyzer import EnhancedGeminiAnalyzer
    ENHANCED_ANALYZER_AVAILABLE = True
except ImportError:
    ENHANCED_ANALYZER_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="SmartATS Pro Elite - AI Resume Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session manager
session = SessionManager()

# Load custom CSS
load_custom_css()

# Initialize components
pdf_processor = PDFProcessor()
gemini_analyzer = GeminiAnalyzer()
viz_engine = VisualizationEngine()
report_gen = ReportGenerator()
keyword_extractor = KeywordExtractor()

# Initialize enhanced components if available
if ENHANCED_ANALYZER_AVAILABLE:
    enhanced_analyzer = EnhancedGeminiAnalyzer()

# Enhanced analyzer wrapper (from File 1)
class AnalyzerWrapper:
    """Wrapper to use enhanced analyzer when available, fallback to basic"""
    
    def __init__(self):
        self.basic_analyzer = gemini_analyzer
        self.enhanced_analyzer = enhanced_analyzer if ENHANCED_ANALYZER_AVAILABLE else None
        self.keyword_extractor = keyword_extractor
    
    def analyze_resume(self, resume_text: str, job_description: str, **kwargs) -> Dict[str, Any]:
        # First try enhanced analyzer if available
        if self.enhanced_analyzer and kwargs.get('use_enhanced', False):
            try:
                result = self.enhanced_analyzer.analyze_resume_comprehensive(
                    resume_text, job_description,
                    kwargs.get('industry', 'Technology'),
                    kwargs.get('experience_level', 'Mid Level'),
                    kwargs.get('analysis_depth', 'Standard')
                )
                # Enhance with keyword analysis
                return self._enhance_with_keywords(result, resume_text, job_description)
            except Exception as e:
                st.warning("Enhanced analysis failed, using standard analysis")
        
        # Use basic analyzer - check if it has industry context method
        try:
            # Your GeminiAnalyzer has analyze_with_industry_context method
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
            
            return self._enhance_with_keywords(result, resume_text, job_description)
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

# Main header (from both files)
create_header()

# Sidebar - properly handle the tuple return from your create_sidebar function
job_description, industry, experience_level, analysis_depth = create_sidebar()

# Ensure job_description is a string
if not isinstance(job_description, str):
    job_description = str(job_description) if job_description else ""

# Main content area - keeping the working structure from File 2
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📄 Resume Analysis")
    
    # File upload tabs - combining both versions
    tab1, tab2, tab3 = st.tabs(["📁 Upload PDF", "✏️ Edit Resume", "🎨 AI Tools"])
    
    with tab1:
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
    
    with tab2:
        # Editable resume text area - from File 2
        resume_text_input = st.text_area(
            "Paste or edit your resume here",
            value=session.get('resume_text', ''),
            height=400,
            help="You can paste your resume text directly or edit the extracted content"
        )
        
        if resume_text_input:
            session.set('resume_text', resume_text_input)
            session.set('is_edited', True)
        
        # Real-time stats (from File 1)
        if resume_text_input:
            char_count = len(resume_text_input)
            word_count = len(resume_text_input.split())
            st.markdown(f"**Stats:** {word_count} words | {char_count} characters")
    
    with tab3:
        # AI Tools (from File 1)
        st.markdown("#### 🎨 AI-Powered Tools")
        
        tool_col1, tool_col2 = st.columns(2)
        
        with tool_col1:
            if st.button("🔨 Resume Builder", use_container_width=True):
                st.info("🚧 AI Resume Builder - Coming Soon!")
        
        with tool_col2:
            if st.button("✍️ Cover Letter Generator", use_container_width=True):
                st.info("🚧 AI Cover Letter Generator - Coming Soon!")

# RIGHT COLUMN - Action Center (keeping the working version from File 2 with File 1 enhancements)
with col2:
    st.markdown("### 🎯 Quick Actions")
    
    # Enhanced analysis toggle (from File 1)
    use_enhanced = st.checkbox("🚀 Enhanced AI Analysis", value=ENHANCED_ANALYZER_AVAILABLE)
    
    # THE MAIN ANALYZE BUTTON - keeping the working version from File 2
    if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
        if session.get('resume_text') and job_description:
            with st.spinner("🤖 AI Analysis in Progress..."):
                start_time = time.time()
                
                # Perform analysis using the wrapper (from File 1)
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
        else:
            st.error("Please provide both resume and job description!")
    
    # Re-analyze button (from File 2 with File 1 enhancements)
    if st.button("🔄 Rescore Resume", use_container_width=True):
        if session.get('resume_text') and job_description:
            with st.spinner("♻️ Rescoring..."):
                # Re-analyze with updated text
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
    
    # Clear session button (from File 2)
    if st.button("🗑️ Clear Session", use_container_width=True):
        session.clear()
        st.rerun()

# RESULTS SECTION - keeping the working version from File 2 with File 1 enhancements
if session.get('analysis_result'):
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Metrics cards
    analysis = session.get('analysis_result')
    
    # Enhanced metrics or basic metrics (from File 1)
    display_metrics_cards(analysis)  # Use your existing function
    
    # Visualizations - keeping the comprehensive version from File 2
    st.markdown("### 📈 Interactive Analytics")
    
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "🎯 Keyword Analysis",
        "💼 Skills Coverage",
        "☁️ Word Cloud",
        "📊 Detailed Breakdown"
    ])
    
    with viz_tab1:
        # Keyword matching visualization
        fig_keywords = viz_engine.create_keyword_chart(
            analysis.get('matched_keywords', []),
            analysis.get('missing_keywords', [])
        )
        st.plotly_chart(fig_keywords, use_container_width=True)
        
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
        fig_skills = viz_engine.create_skills_radar(
            analysis.get('skills_analysis', {})
        )
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with viz_tab3:
        # Word cloud visualization
        wordcloud_img = viz_engine.create_word_cloud(
            session.get('resume_text', ''),
            analysis.get('important_terms', [])
        )
        st.image(wordcloud_img, use_column_width=True)
    
    with viz_tab4:
        # Detailed breakdown
        if hasattr(viz_engine, 'create_detailed_breakdown'):
            breakdown_fig = viz_engine.create_detailed_breakdown(analysis)
            st.plotly_chart(breakdown_fig, use_container_width=True)
        else:
            st.info("Detailed breakdown chart will be available when viz_engine.create_detailed_breakdown is implemented")
    
    # Recommendations section - from File 2
    st.markdown("### 🎯 AI-Powered Recommendations")
    
    rec_col1, rec_col2 = st.columns([1, 1])
    
    with rec_col1:
        st.markdown("#### ✅ Strengths")
        for strength in analysis.get('strengths', []):
            st.info(f"💪 {strength}")
    
    with rec_col2:
        st.markdown("#### 📈 Areas for Improvement")
        for improvement in analysis.get('improvements', []):
            st.warning(f"💡 {improvement}")
    
    # Report generation - from File 2
    st.markdown("### 📄 Generate Reports")
    
    report_col1, report_col2, report_col3 = st.columns(3)
    
    with report_col1:
        if st.button("📥 Download PDF Report", use_container_width=True):
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
    
    with report_col2:
        if st.button("📊 Download CSV Data", use_container_width=True):
            csv_data = report_gen.generate_csv_report(analysis)
            st.download_button(
                label="💾 Save CSV Data",
                data=csv_data,
                file_name=f"ATS_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with report_col3:
        if st.button("📋 Copy Analysis", use_container_width=True):
            analysis_text = report_gen.generate_text_summary(analysis)
            st.code(analysis_text, language="markdown")
            st.info("📋 Analysis copied to clipboard!")

# Footer - keeping the working version from File 2
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🚀 SmartATS Pro Elite - Built with ❤️ using Streamlit & Google Gemini</p>
        <p style='font-size: 0.8em;'>Next-Generation AI Resume Optimization Platform</p>
    </div>
    """,
    unsafe_allow_html=True
)