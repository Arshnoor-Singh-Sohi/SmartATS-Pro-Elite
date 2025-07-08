import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import pandas as pd
from typing import Dict, Any
import json

class ReportGenerator:
    """
    Generates various report formats (PDF, CSV, Text) from analysis results
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for reports"""
        # Create custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1e40af')
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#3b82f6')
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#1f2937')
        )
    
    def generate_pdf_report(self, analysis: Dict[str, Any], 
                          resume_text: str, job_description: str) -> bytes:
        """
        Generate comprehensive PDF report
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=inch)
        
        # Build story
        story = []
        
        # Title
        story.append(Paragraph("SmartATS Pro Elite - Analysis Report", self.title_style))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.heading_style))
        
        summary_data = [
            ['Metric', 'Score', 'Status'],
            ['Overall Match', f"{analysis.get('match_percentage', 0)}%", 
             self._get_status(analysis.get('match_percentage', 0))],
            ['ATS Compatibility', analysis.get('ats_friendliness', 'Medium'), 
             analysis.get('ats_friendliness', 'Medium')],
            ['Skills Coverage', f"{analysis.get('skills_coverage', 0)}%", 
             self._get_status(analysis.get('skills_coverage', 0))],
            ['Keywords Found', f"{len(analysis.get('matched_keywords', []))}", 
             f"Missing: {len(analysis.get('missing_keywords', []))}"]
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Key Strengths
        story.append(Paragraph("Key Strengths", self.heading_style))
        strengths = analysis.get('strengths', [])
        for i, strength in enumerate(strengths[:5], 1):
            story.append(Paragraph(f"{i}. {strength}", self.styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Areas for Improvement
        story.append(Paragraph("Areas for Improvement", self.heading_style))
        improvements = analysis.get('improvements', [])
        for i, improvement in enumerate(improvements[:5], 1):
            story.append(Paragraph(f"{i}. {improvement}", self.styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Keyword Analysis
        story.append(Paragraph("Keyword Analysis", self.heading_style))
        
        matched_kw = analysis.get('matched_keywords', [])
        missing_kw = analysis.get('missing_keywords', [])
        
        story.append(Paragraph(f"<b>Matched Keywords ({len(matched_kw)}):</b> {', '.join(matched_kw[:10])}", 
                              self.styles['Normal']))
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<b>Missing Keywords ({len(missing_kw)}):</b> {', '.join(missing_kw[:10])}", 
                              self.styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Skills Analysis
        if 'skills_analysis' in analysis:
            story.append(Paragraph("Skills Analysis", self.heading_style))
            skills = analysis['skills_analysis']
            
            skills_data = [
                ['Skill Category', 'Score'],
                ['Technical Skills', f"{skills.get('technical_skills', 0)}%"],
                ['Soft Skills', f"{skills.get('soft_skills', 0)}%"],
                ['Industry Knowledge', f"{skills.get('industry_knowledge', 0)}%"],
                ['Experience Relevance', f"{skills.get('experience_relevance', 0)}%"]
            ]
            
            skills_table = Table(skills_data)
            skills_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(skills_table)
            story.append(Spacer(1, 15))
        
        # Optimization Roadmap (if available)
        if 'optimization_roadmap' in analysis:
            story.append(Paragraph("Optimization Roadmap", self.heading_style))
            roadmap = analysis['optimization_roadmap']
            
            for i, action in enumerate(roadmap[:3], 1):
                story.append(Paragraph(f"<b>{i}. {action.get('action', 'Action needed')}</b>", 
                                     self.subheading_style))
                story.append(Paragraph(f"Priority: {action.get('priority', 'Medium')}", 
                                     self.styles['Normal']))
                story.append(Paragraph(f"Impact: {action.get('estimated_impact', 'TBD')}", 
                                     self.styles['Normal']))
                story.append(Paragraph(f"Time Required: {action.get('time_required', 'TBD')}", 
                                     self.styles['Normal']))
                story.append(Spacer(1, 10))
        
        # Footer
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              self.styles['Normal']))
        story.append(Paragraph("SmartATS Pro Elite - Next-Generation AI Resume Optimization", 
                              self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.read()
    
    def generate_csv_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate CSV report with analysis data
        """
        # Prepare data for CSV
        data = {
            'Metric': [
                'Overall Match Percentage',
                'ATS Friendliness',
                'Skills Coverage',
                'Technical Skills',
                'Soft Skills',
                'Industry Knowledge',
                'Experience Relevance',
                'Keywords Matched',
                'Keywords Missing',
                'Total Keywords Analyzed'
            ],
            'Value': [
                f"{analysis.get('match_percentage', 0)}%",
                analysis.get('ats_friendliness', 'Medium'),
                f"{analysis.get('skills_coverage', 0)}%",
                f"{analysis.get('skills_analysis', {}).get('technical_skills', 0)}%",
                f"{analysis.get('skills_analysis', {}).get('soft_skills', 0)}%",
                f"{analysis.get('skills_analysis', {}).get('industry_knowledge', 0)}%",
                f"{analysis.get('skills_analysis', {}).get('experience_relevance', 0)}%",
                len(analysis.get('matched_keywords', [])),
                len(analysis.get('missing_keywords', [])),
                len(analysis.get('matched_keywords', [])) + len(analysis.get('missing_keywords', []))
            ]
        }
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    
    def generate_text_summary(self, analysis: Dict[str, Any]) -> str:
        """
        Generate text summary of analysis
        """
        summary = f"""# SmartATS Pro Elite - Analysis Summary

## Overall Performance
- **Match Score:** {analysis.get('match_percentage', 0)}%
- **ATS Compatibility:** {analysis.get('ats_friendliness', 'Medium')}
- **Skills Coverage:** {analysis.get('skills_coverage', 0)}%

## Key Metrics
- **Keywords Matched:** {len(analysis.get('matched_keywords', []))}
- **Keywords Missing:** {len(analysis.get('missing_keywords', []))}
- **Technical Skills:** {analysis.get('skills_analysis', {}).get('technical_skills', 0)}%
- **Soft Skills:** {analysis.get('skills_analysis', {}).get('soft_skills', 0)}%

## Top Strengths
"""
        
        for i, strength in enumerate(analysis.get('strengths', [])[:3], 1):
            summary += f"{i}. {strength}\n"
        
        summary += "\n## Priority Improvements\n"
        
        for i, improvement in enumerate(analysis.get('improvements', [])[:3], 1):
            summary += f"{i}. {improvement}\n"
        
        summary += f"\n## Matched Keywords\n{', '.join(analysis.get('matched_keywords', [])[:10])}\n"
        summary += f"\n## Missing Keywords\n{', '.join(analysis.get('missing_keywords', [])[:10])}\n"
        
        summary += f"\n---\n*Report generated on {datetime.now().strftime('%B %d, %Y')}*"
        
        return summary
    
    def _get_status(self, score: int) -> str:
        """Get status based on score"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Needs Work"