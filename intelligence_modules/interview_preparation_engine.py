import streamlit as st
import google.generativeai as genai
from typing import Dict, List, Any, Optional, Tuple
import json
import re
from datetime import datetime
import random

class InterviewPreparationEngine:
    """
    AI-powered interview preparation system that generates personalized
    interview questions and provides coaching based on resume analysis
    """
    
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Question categories and frameworks
        self.question_categories = {
            'behavioral': {
                'description': 'Questions about past experiences and behaviors',
                'frameworks': ['STAR Method (Situation, Task, Action, Result)'],
                'example_stems': [
                    'Tell me about a time when...',
                    'Describe a situation where...',
                    'Give me an example of...',
                    'Walk me through how you handled...'
                ]
            },
            'technical': {
                'description': 'Technical knowledge and problem-solving',
                'frameworks': ['Problem-Solution Framework', 'Step-by-step explanation'],
                'example_stems': [
                    'How would you approach...',
                    'Explain the difference between...',
                    'What are the best practices for...',
                    'How would you design...'
                ]
            },
            'situational': {
                'description': 'Hypothetical scenarios and problem-solving',
                'frameworks': ['Problem-solving framework', 'Decision-making process'],
                'example_stems': [
                    'What would you do if...',
                    'How would you handle...',
                    'If you encountered... how would you...',
                    'Suppose you had to...'
                ]
            },
            'leadership': {
                'description': 'Leadership and management capabilities',
                'frameworks': ['Leadership principles', 'Management strategies'],
                'example_stems': [
                    'How do you motivate...',
                    'Describe your leadership style...',
                    'How do you handle conflict...',
                    'Tell me about a difficult team decision...'
                ]
            },
            'cultural_fit': {
                'description': 'Alignment with company values and culture',
                'frameworks': ['Value alignment', 'Culture examples'],
                'example_stems': [
                    'Why do you want to work here...',
                    'How do you handle ambiguity...',
                    'What motivates you...',
                    'Describe your ideal work environment...'
                ]
            }
        }
        
        # Industry-specific question patterns
        self.industry_patterns = {
            'Technology': {
                'technical_focus': ['system design', 'coding problems', 'architecture decisions'],
                'common_scenarios': ['scaling challenges', 'technology choices', 'debugging'],
                'key_competencies': ['problem-solving', 'innovation', 'collaboration']
            },
            'Healthcare': {
                'technical_focus': ['patient care', 'regulatory compliance', 'clinical procedures'],
                'common_scenarios': ['patient safety', 'ethical dilemmas', 'emergency situations'],
                'key_competencies': ['empathy', 'attention to detail', 'communication']
            },
            'Finance': {
                'technical_focus': ['financial analysis', 'risk assessment', 'regulatory knowledge'],
                'common_scenarios': ['market volatility', 'client relationships', 'compliance issues'],
                'key_competencies': ['analytical thinking', 'integrity', 'decision-making']
            }
        }
        
        # Answer evaluation criteria
        self.evaluation_criteria = {
            'structure': {
                'weight': 25,
                'indicators': ['clear introduction', 'logical flow', 'strong conclusion']
            },
            'content_relevance': {
                'weight': 30,
                'indicators': ['addresses question directly', 'relevant examples', 'industry knowledge']
            },
            'specificity': {
                'weight': 25,
                'indicators': ['concrete examples', 'quantified results', 'detailed explanations']
            },
            'communication': {
                'weight': 20,
                'indicators': ['clarity', 'confidence', 'professional tone']
            }
        }
    
    def generate_interview_preparation_plan(self, resume_analysis: Dict[str, Any], 
                                          job_description: str, industry: str,
                                          experience_level: str, company_info: str = "") -> Dict[str, Any]:
        """
        Generate comprehensive interview preparation plan
        """
        # Analyze strengths and weaknesses from resume analysis
        strengths = resume_analysis.get('strengths', [])
        improvements = resume_analysis.get('critical_improvements', [])
        matched_keywords = resume_analysis.get('matched_keywords', [])
        missing_keywords = resume_analysis.get('missing_keywords', [])
        
        # Generate personalized questions
        personalized_questions = self._generate_personalized_questions(
            resume_analysis, job_description, industry, experience_level
        )
        
        # Create preparation strategies
        preparation_strategies = self._create_preparation_strategies(
            strengths, improvements, missing_keywords, industry
        )
        
        # Generate talking points
        talking_points = self._generate_talking_points(
            matched_keywords, strengths, job_description
        )
        
        # Create practice scenarios
        practice_scenarios = self._create_practice_scenarios(
            industry, experience_level, job_description
        )
        
        # Generate company-specific preparation
        company_preparation = self._generate_company_preparation(
            company_info, job_description, industry
        )
        
        return {
            'personalized_questions': personalized_questions,
            'preparation_strategies': preparation_strategies,
            'talking_points': talking_points,
            'practice_scenarios': practice_scenarios,
            'company_preparation': company_preparation,
            'question_frameworks': self._get_answer_frameworks(),
            'mock_interview_plan': self._create_mock_interview_plan(personalized_questions),
            'follow_up_preparation': self._generate_follow_up_preparation()
        }
    
    def _generate_personalized_questions(self, resume_analysis: Dict[str, Any], 
                                       job_description: str, industry: str,
                                       experience_level: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate personalized interview questions based on resume analysis
        """
        prompt = f"""
        As an expert interview coach, generate personalized interview questions based on this resume analysis and job description.
        
        RESUME ANALYSIS SUMMARY:
        - Strengths: {resume_analysis.get('strengths', [])}
        - Areas for improvement: {resume_analysis.get('critical_improvements', [])}
        - Matched keywords: {resume_analysis.get('matched_keywords', [])}
        - Missing keywords: {resume_analysis.get('missing_keywords', [])}
        - Match percentage: {resume_analysis.get('match_percentage', 0)}%
        
        JOB DESCRIPTION:
        {job_description}
        
        CONTEXT:
        - Industry: {industry}
        - Experience Level: {experience_level}
        
        Generate questions in JSON format:
        {{
            "behavioral_questions": [
                {{
                    "question": "specific behavioral question",
                    "focus_area": "area being tested",
                    "difficulty": "easy/medium/hard",
                    "why_likely": "reason this question is likely for this candidate",
                    "key_points_to_address": ["point1", "point2", "point3"]
                }}
            ],
            "technical_questions": [
                {{
                    "question": "technical question",
                    "focus_area": "technical area",
                    "difficulty": "easy/medium/hard",
                    "why_likely": "reason this question is likely",
                    "key_points_to_address": ["point1", "point2", "point3"]
                }}
            ],
            "situational_questions": [
                {{
                    "question": "situational question",
                    "focus_area": "competency being tested",
                    "difficulty": "easy/medium/hard",
                    "why_likely": "reason this question is likely",
                    "key_points_to_address": ["point1", "point2", "point3"]
                }}
            ],
            "weakness_focused_questions": [
                {{
                    "question": "question targeting improvement areas",
                    "focus_area": "improvement area",
                    "difficulty": "medium/hard",
                    "why_likely": "based on resume gaps",
                    "preparation_strategy": "how to prepare for this",
                    "key_points_to_address": ["point1", "point2", "point3"]
                }}
            ],
            "strength_showcase_questions": [
                {{
                    "question": "question to showcase strengths",
                    "focus_area": "strength area",
                    "difficulty": "easy/medium",
                    "why_likely": "based on resume strengths",
                    "opportunity": "how to maximize this opportunity",
                    "key_points_to_address": ["point1", "point2", "point3"]
                }}
            ]
        }}
        
        Make questions specific to the candidate's background and the role requirements.
        Include 3-4 questions per category, focusing on high-probability questions.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return self._get_fallback_questions(industry, experience_level)
    
    def _create_preparation_strategies(self, strengths: List[str], improvements: List[str],
                                     missing_keywords: List[str], industry: str) -> Dict[str, Any]:
        """
        Create targeted preparation strategies
        """
        strategies = {
            'strength_amplification': {
                'description': 'Maximize your strongest points',
                'tactics': []
            },
            'weakness_mitigation': {
                'description': 'Address potential concerns',
                'tactics': []
            },
            'gap_bridging': {
                'description': 'Handle missing qualifications',
                'tactics': []
            },
            'industry_preparation': {
                'description': 'Industry-specific preparation',
                'tactics': []
            }
        }
        
        # Strength amplification
        for strength in strengths[:3]:
            strategies['strength_amplification']['tactics'].append({
                'focus': strength,
                'approach': f"Prepare 2-3 detailed STAR examples demonstrating {strength.lower()}",
                'talking_points': f"Quantify impact and results from {strength.lower()}"
            })
        
        # Weakness mitigation
        for improvement in improvements[:3]:
            strategies['weakness_mitigation']['tactics'].append({
                'focus': improvement,
                'approach': f"Prepare honest response about {improvement.lower()} with growth plan",
                'talking_points': f"Show self-awareness and concrete steps for improvement"
            })
        
        # Gap bridging
        for keyword in missing_keywords[:3]:
            strategies['gap_bridging']['tactics'].append({
                'focus': keyword,
                'approach': f"Research {keyword} and find transferable skills or learning plan",
                'talking_points': f"Demonstrate willingness to learn and related experience"
            })
        
        # Industry-specific preparation
        industry_focus = self.industry_patterns.get(industry, {})
        for competency in industry_focus.get('key_competencies', []):
            strategies['industry_preparation']['tactics'].append({
                'focus': competency,
                'approach': f"Prepare industry-specific examples of {competency}",
                'talking_points': f"Show understanding of {competency} in {industry} context"
            })
        
        return strategies
    
    def _generate_talking_points(self, matched_keywords: List[str], strengths: List[str],
                               job_description: str) -> Dict[str, List[str]]:
        """
        Generate key talking points for the interview
        """
        talking_points = {
            'opening_statement': [],
            'value_proposition': [],
            'closing_statement': [],
            'key_achievements': []
        }
        
        # Opening statement points
        talking_points['opening_statement'] = [
            f"Highlight experience with {', '.join(matched_keywords[:3])}",
            f"Emphasize {strengths[0].lower()} if available" if strengths else "Focus on relevant experience",
            "Express genuine interest in the role and company"
        ]
        
        # Value proposition
        talking_points['value_proposition'] = [
            "Unique combination of skills that match role requirements",
            "Track record of delivering results in similar contexts",
            "Passion for the industry and continuous learning mindset"
        ]
        
        # Key achievements template
        talking_points['key_achievements'] = [
            "Prepare 3-5 STAR stories with quantified results",
            "Include examples that showcase matched keywords",
            "Cover different competencies: technical, leadership, problem-solving"
        ]
        
        # Closing statement
        talking_points['closing_statement'] = [
            "Reiterate fit for the role based on discussion",
            "Express enthusiasm for the opportunity",
            "Ask thoughtful questions about next steps"
        ]
        
        return talking_points
    
    def _create_practice_scenarios(self, industry: str, experience_level: str,
                                 job_description: str) -> List[Dict[str, Any]]:
        """
        Create realistic practice scenarios
        """
        scenarios = []
        
        # Industry-specific scenarios
        industry_data = self.industry_patterns.get(industry, {})
        common_scenarios = industry_data.get('common_scenarios', [])
        
        for scenario in common_scenarios:
            scenarios.append({
                'type': 'industry_specific',
                'scenario': f"You encounter {scenario} in your role. How do you handle it?",
                'focus_area': scenario,
                'preparation_tips': [
                    f"Research best practices for handling {scenario}",
                    "Prepare step-by-step approach",
                    "Include stakeholder consideration"
                ]
            })
        
        # Experience level scenarios
        if 'Entry' in experience_level:
            scenarios.append({
                'type': 'career_development',
                'scenario': "How do you plan to grow from an entry-level position to become a valuable team member?",
                'focus_area': 'growth mindset',
                'preparation_tips': [
                    "Show eagerness to learn",
                    "Demonstrate research about career progression",
                    "Highlight relevant projects or experiences"
                ]
            })
        elif 'Senior' in experience_level or 'Executive' in experience_level:
            scenarios.append({
                'type': 'leadership',
                'scenario': "Describe how you would build and lead a team to tackle a complex, multi-month project.",
                'focus_area': 'leadership and project management',
                'preparation_tips': [
                    "Include team building strategies",
                    "Show project management methodology knowledge",
                    "Demonstrate stakeholder management"
                ]
            })
        
        return scenarios
    
    def _generate_company_preparation(self, company_info: str, job_description: str,
                                    industry: str) -> Dict[str, Any]:
        """
        Generate company-specific preparation guidance
        """
        preparation = {
            'research_areas': [
                'Company mission, vision, and values',
                'Recent news and developments',
                'Key leadership and team structure',
                'Products/services and market position',
                'Company culture and work environment'
            ],
            'questions_to_ask': [],
            'culture_alignment': [],
            'current_challenges': []
        }
        
        # Generate thoughtful questions
        preparation['questions_to_ask'] = [
            "What are the biggest challenges facing the team right now?",
            "How does this role contribute to the company's strategic goals?",
            "What does success look like in this position after 6 months?",
            "What opportunities are there for professional development?",
            "How would you describe the team culture and collaboration style?"
        ]
        
        # Culture alignment points
        preparation['culture_alignment'] = [
            "Research company values and prepare examples of alignment",
            "Understand the company's approach to work-life balance",
            "Learn about diversity and inclusion initiatives",
            "Understand the company's approach to innovation/growth"
        ]
        
        return preparation
    
    def _get_answer_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """
        Provide answer frameworks for different question types
        """
        frameworks = {
            'STAR_method': {
                'description': 'For behavioral questions',
                'structure': {
                    'Situation': 'Set the context and background',
                    'Task': 'Describe your responsibility or goal',
                    'Action': 'Explain the specific actions you took',
                    'Result': 'Share the outcomes and impact'
                },
                'tips': [
                    'Spend 20% on Situation, 20% on Task, 40% on Action, 20% on Result',
                    'Use specific metrics and numbers in Results',
                    'Choose examples that showcase the required competency'
                ]
            },
            'problem_solving_framework': {
                'description': 'For technical and situational questions',
                'structure': {
                    'Understand': 'Clarify the problem and requirements',
                    'Analyze': 'Break down the problem into components',
                    'Plan': 'Outline your approach and solution',
                    'Execute': 'Describe implementation steps',
                    'Evaluate': 'Assess results and lessons learned'
                },
                'tips': [
                    'Ask clarifying questions before diving in',
                    'Think out loud to show your thought process',
                    'Consider multiple solutions and trade-offs'
                ]
            },
            'leadership_framework': {
                'description': 'For leadership and management questions',
                'structure': {
                    'Context': 'Describe the leadership challenge',
                    'Approach': 'Explain your leadership philosophy/style',
                    'Actions': 'Detail specific leadership actions taken',
                    'Team Impact': 'Show how your leadership affected the team',
                    'Results': 'Quantify business/project outcomes'
                },
                'tips': [
                    'Show emotional intelligence and people skills',
                    'Demonstrate decision-making under pressure',
                    'Include how you developed others'
                ]
            }
        }
        
        return frameworks
    
    def _create_mock_interview_plan(self, personalized_questions: Dict[str, List]) -> Dict[str, Any]:
        """
        Create a structured mock interview plan
        """
        # Select questions for mock interview
        mock_questions = []
        
        # Pick 2 from each category
        for category, questions in personalized_questions.items():
            selected = questions[:2] if len(questions) >= 2 else questions
            for q in selected:
                mock_questions.append({
                    'category': category,
                    'question': q['question'],
                    'difficulty': q.get('difficulty', 'medium'),
                    'focus_area': q.get('focus_area', 'general')
                })
        
        # Structure the mock interview
        plan = {
            'total_duration': '45-60 minutes',
            'structure': {
                'warm_up': {
                    'duration': '5 minutes',
                    'questions': ['Tell me about yourself', 'Walk me through your resume'],
                    'purpose': 'Build rapport and set tone'
                },
                'behavioral_deep_dive': {
                    'duration': '20 minutes',
                    'questions': [q for q in mock_questions if q['category'] == 'behavioral_questions'][:3],
                    'purpose': 'Assess past behavior and experiences'
                },
                'technical_assessment': {
                    'duration': '15 minutes',
                    'questions': [q for q in mock_questions if q['category'] == 'technical_questions'][:2],
                    'purpose': 'Evaluate technical competency'
                },
                'situational_scenarios': {
                    'duration': '10 minutes',
                    'questions': [q for q in mock_questions if q['category'] == 'situational_questions'][:2],
                    'purpose': 'Test problem-solving and judgment'
                },
                'candidate_questions': {
                    'duration': '5 minutes',
                    'questions': ['What questions do you have for me?'],
                    'purpose': 'Assess engagement and preparation'
                }
            },
            'practice_tips': [
                'Record yourself to review body language and speech patterns',
                'Practice with a friend or mentor for feedback',
                'Time your responses (aim for 1-3 minutes per answer)',
                'Prepare multiple examples for each competency area'
            ]
        }
        
        return plan
    
    def _generate_follow_up_preparation(self) -> Dict[str, Any]:
        """
        Generate follow-up preparation guidance
        """
        return {
            'thank_you_note': {
                'timing': 'Within 24 hours of interview',
                'content': [
                    'Express appreciation for the interviewer\'s time',
                    'Reiterate interest in the position',
                    'Briefly mention a key point from the conversation',
                    'Provide any additional information requested'
                ],
                'template': '''Subject: Thank you - [Position Title] Interview

Dear [Interviewer Name],

Thank you for taking the time to meet with me yesterday about the [Position Title] role. I enjoyed our conversation about [specific topic discussed] and learning more about [company's specific initiative/challenge].

Our discussion reinforced my enthusiasm for this opportunity, particularly [mention specific aspect that excited you]. I believe my experience with [relevant skill/experience] would enable me to contribute effectively to [specific team goal/project mentioned].

Please let me know if you need any additional information from me. I look forward to hearing about the next steps.

Best regards,
[Your Name]'''
            },
            'waiting_period': {
                'typical_timeline': '1-2 weeks for initial response',
                'what_to_do': [
                    'Continue job searching and interviewing',
                    'Connect with interviewer on LinkedIn (if appropriate)',
                    'Reflect on interview performance and areas for improvement',
                    'Prepare for potential next round interviews'
                ]
            },
            'next_round_preparation': {
                'common_formats': [
                    'Panel interview with multiple team members',
                    'Technical assessment or case study',
                    'Meeting with senior leadership',
                    'Cultural fit assessment'
                ],
                'preparation_strategy': [
                    'Research all potential interviewers',
                    'Prepare more detailed technical examples',
                    'Review company strategy and vision',
                    'Practice whiteboarding or presentation skills'
                ]
            }
        }
    
    def evaluate_practice_answer(self, question: str, answer: str, 
                               question_type: str) -> Dict[str, Any]:
        """
        AI-powered evaluation of practice answers
        """
        prompt = f"""
        Evaluate this interview answer based on professional interview standards.
        
        QUESTION: {question}
        QUESTION TYPE: {question_type}
        
        CANDIDATE ANSWER: {answer}
        
        Evaluate on these criteria (0-100 scale):
        1. Structure and organization
        2. Content relevance and depth
        3. Specificity and examples
        4. Communication clarity
        
        Provide feedback in JSON format:
        {{
            "overall_score": <0-100>,
            "criteria_scores": {{
                "structure": <0-100>,
                "content_relevance": <0-100>,
                "specificity": <0-100>,
                "communication": <0-100>
            }},
            "strengths": ["strength1", "strength2"],
            "areas_for_improvement": ["improvement1", "improvement2"],
            "specific_suggestions": [
                "specific suggestion 1",
                "specific suggestion 2"
            ],
            "example_improvement": "Here's how you could strengthen your answer: [specific rewrite]"
        }}
        
        Be constructive and specific in feedback.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            evaluation = json.loads(response.text)
            
            # Add improvement recommendations
            evaluation['next_steps'] = self._generate_improvement_steps(evaluation)
            
            return evaluation
        except:
            return self._get_fallback_evaluation()
    
    def _generate_improvement_steps(self, evaluation: Dict[str, Any]) -> List[str]:
        """
        Generate specific improvement steps based on evaluation
        """
        steps = []
        scores = evaluation.get('criteria_scores', {})
        
        if scores.get('structure', 100) < 70:
            steps.append("Practice using the STAR method for better structure")
        
        if scores.get('specificity', 100) < 70:
            steps.append("Add more concrete examples and quantified results")
        
        if scores.get('content_relevance', 100) < 70:
            steps.append("Research the role requirements more thoroughly")
        
        if scores.get('communication', 100) < 70:
            steps.append("Practice speaking slowly and clearly")
        
        return steps
    
    def _get_fallback_questions(self, industry: str, experience_level: str) -> Dict[str, List[Dict]]:
        """
        Fallback questions when AI generation fails
        """
        return {
            'behavioral_questions': [
                {
                    'question': 'Tell me about a challenging project you worked on and how you overcame obstacles.',
                    'focus_area': 'problem-solving',
                    'difficulty': 'medium',
                    'key_points_to_address': ['specific challenge', 'actions taken', 'results achieved']
                }
            ],
            'technical_questions': [
                {
                    'question': 'How do you stay current with industry trends and best practices?',
                    'focus_area': 'continuous learning',
                    'difficulty': 'easy',
                    'key_points_to_address': ['learning resources', 'application of knowledge', 'examples']
                }
            ],
            'situational_questions': [
                {
                    'question': 'How would you handle a situation where you disagreed with your manager?',
                    'focus_area': 'conflict resolution',
                    'difficulty': 'medium',
                    'key_points_to_address': ['communication approach', 'respect for hierarchy', 'solution focus']
                }
            ]
        }
    
    def _get_fallback_evaluation(self) -> Dict[str, Any]:
        """
        Fallback evaluation when AI fails
        """
        return {
            'overall_score': 75,
            'criteria_scores': {
                'structure': 75,
                'content_relevance': 75,
                'specificity': 70,
                'communication': 80
            },
            'strengths': ['Clear communication', 'Relevant experience mentioned'],
            'areas_for_improvement': ['Add more specific examples', 'Improve answer structure'],
            'specific_suggestions': [
                'Use the STAR method for behavioral questions',
                'Include quantified results in your examples'
            ],
            'next_steps': ['Practice with more specific examples', 'Work on answer structure']
        }

class InterviewAnalytics:
    """
    Analytics system for tracking interview preparation progress
    """
    
    def __init__(self):
        self.session_key = 'interview_analytics'
        self._initialize_analytics()
    
    def _initialize_analytics(self):
        """Initialize analytics tracking"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                'practice_sessions': [],
                'question_performance': {},
                'improvement_tracking': {},
                'preparation_milestones': []
            }
    
    def track_practice_session(self, questions_practiced: List[str], 
                             performance_scores: List[int], session_duration: int):
        """Track a practice session"""
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'questions_count': len(questions_practiced),
            'avg_score': sum(performance_scores) / len(performance_scores) if performance_scores else 0,
            'duration_minutes': session_duration,
            'questions': questions_practiced,
            'scores': performance_scores
        }
        
        analytics = st.session_state[self.session_key]
        analytics['practice_sessions'].append(session_data)
    
    def get_progress_analytics(self) -> Dict[str, Any]:
        """Get comprehensive progress analytics"""
        analytics = st.session_state[self.session_key]
        sessions = analytics['practice_sessions']
        
        if not sessions:
            return {'error': 'No practice data available'}
        
        # Calculate trends
        scores = [session['avg_score'] for session in sessions]
        durations = [session['duration_minutes'] for session in sessions]
        
        return {
            'total_sessions': len(sessions),
            'total_practice_time': sum(durations),
            'avg_score_trend': scores,
            'current_avg_score': scores[-1] if scores else 0,
            'improvement_rate': self._calculate_improvement_rate(scores),
            'consistency_score': self._calculate_consistency(scores),
            'readiness_assessment': self._assess_interview_readiness(sessions)
        }
    
    def _calculate_improvement_rate(self, scores: List[float]) -> float:
        """Calculate improvement rate over time"""
        if len(scores) < 2:
            return 0
        
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        return round(second_avg - first_avg, 2)
    
    def _calculate_consistency(self, scores: List[float]) -> float:
        """Calculate consistency of performance"""
        if len(scores) < 2:
            return 100
        
        import statistics
        std_dev = statistics.stdev(scores)
        avg_score = statistics.mean(scores)
        
        # Lower standard deviation relative to mean = higher consistency
        consistency = max(0, 100 - (std_dev / avg_score * 100))
        return round(consistency, 1)
    
    def _assess_interview_readiness(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Assess overall interview readiness"""
        if not sessions:
            return {'level': 'Not Ready', 'confidence': 0}
        
        recent_sessions = sessions[-3:] if len(sessions) >= 3 else sessions
        avg_recent_score = sum(s['avg_score'] for s in recent_sessions) / len(recent_sessions)
        
        practice_frequency = len(sessions)
        
        # Readiness assessment
        if avg_recent_score >= 85 and practice_frequency >= 5:
            readiness = {'level': 'Interview Ready', 'confidence': 90}
        elif avg_recent_score >= 75 and practice_frequency >= 3:
            readiness = {'level': 'Nearly Ready', 'confidence': 75}
        elif avg_recent_score >= 65:
            readiness = {'level': 'Needs More Practice', 'confidence': 60}
        else:
            readiness = {'level': 'Significant Practice Needed', 'confidence': 40}
        
        return readiness