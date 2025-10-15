"""AI-powered interview preparation"""
from typing import Dict, List
from utils.llm_client import llm


class InterviewPrep:
    """Generate interview questions and preparation materials"""

    def __init__(self, job_data: Dict, resume_data: Dict = None):
        self.job_data = job_data
        self.resume_data = resume_data or {}

    def generate_questions(self, count: int = 10) -> List[Dict]:
        """Generate likely interview questions"""
        prompt = self._build_questions_prompt(count)

        try:
            response = llm.generate(prompt, max_tokens=2000)
            questions = self._parse_questions(response)
            return questions
        except Exception as e:
            return [{"question": f"Error generating questions: {str(e)}", "type": "error"}]

    def _build_questions_prompt(self, count: int) -> str:
        """Build prompt for question generation"""
        job_title = self.job_data.get('job_title', 'the position')
        required_skills = self.job_data.get('required_skills', [])
        experience_level = self.job_data.get('experience_level', 'not specified')

        prompt = f"""Generate {count} realistic interview questions for:

Job Title: {job_title}
Experience Level: {experience_level}
Key Skills: {', '.join(required_skills[:10])}

Include a mix of:
- Technical questions (40%)
- Behavioral questions (30%)
- Situational questions (20%)
- Company/role-specific questions (10%)

Format each question as:
Q1: [Question text]
Type: [Technical/Behavioral/Situational/Company]

Make questions specific to the role and requirements."""

        return prompt

    def _parse_questions(self, response: str) -> List[Dict]:
        """Parse LLM response into structured questions"""
        questions = []
        lines = response.split('\n')

        current_question = None
        current_type = "General"

        for line in lines:
            line = line.strip()
            if line.startswith('Q') and ':' in line:
                # Save previous question
                if current_question:
                    questions.append({
                        'question': current_question,
                        'type': current_type
                    })
                # Start new question
                current_question = line.split(':', 1)[1].strip()
            elif line.startswith('Type:'):
                current_type = line.split(':', 1)[1].strip()

        # Add last question
        if current_question:
            questions.append({
                'question': current_question,
                'type': current_type
            })

        return questions

    def generate_answer_framework(self, question: str) -> str:
        """Generate a framework for answering a specific question"""
        resume_context = ""
        if self.resume_data:
            skills = self.resume_data.get('skills', [])
            resume_context = f"\n\nCandidate's skills: {', '.join(skills[:10])}"

        prompt = f"""Provide a framework for answering this interview question:

Question: {question}
{resume_context}

Provide:
1. Question type and what they're really asking
2. STAR method outline (if applicable)
3. Key points to cover
4. Things to avoid
5. Example talking points

Be specific and actionable."""

        try:
            return llm.generate(prompt, max_tokens=1000)
        except Exception as e:
            return f"Error generating framework: {str(e)}"

    def generate_company_research(self) -> str:
        """Generate company research guide"""
        company = self.job_data.get('company', 'the company')
        job_title = self.job_data.get('job_title', 'this role')

        prompt = f"""Create a research guide for interviewing at {company} for {job_title}:

What to research:
1. Company background and mission
2. Recent news and developments
3. Products/services
4. Company culture and values
5. Interview preparation tips
6. Questions to ask the interviewer

Provide specific guidance on what to look for and how to use this information."""

        try:
            return llm.generate(prompt, max_tokens=1500)
        except Exception as e:
            return f"Error generating research guide: {str(e)}"

    def generate_questions_to_ask(self) -> List[str]:
        """Generate intelligent questions for the candidate to ask"""
        prompt = f"""Generate 10 thoughtful questions a candidate should ask the interviewer for:

Job: {self.job_data.get('job_title', 'this position')}
Company: {self.job_data.get('company', 'the company')}

Include questions about:
- Role and responsibilities
- Team and culture
- Growth opportunities
- Success metrics
- Company direction

Make them specific and demonstrate genuine interest."""

        try:
            response = llm.generate(prompt, max_tokens=1000)
            # Parse questions (simple split by lines)
            questions = [line.strip() for line in response.split('\n')
                        if line.strip() and any(char.isalnum() for char in line)]
            return questions[:10]
        except Exception as e:
            return [f"Error generating questions: {str(e)}"]

    def generate_full_prep_guide(self) -> Dict:
        """Generate comprehensive interview prep guide"""
        return {
            'questions': self.generate_questions(15),
            'company_research': self.generate_company_research(),
            'questions_to_ask': self.generate_questions_to_ask(),
            'tips': self._get_general_tips()
        }

    def _get_general_tips(self) -> List[str]:
        """Get general interview tips"""
        return [
            "Research the company thoroughly before the interview",
            "Prepare STAR method examples for behavioral questions",
            "Practice answers out loud, not just in your head",
            "Prepare questions to ask the interviewer",
            "Arrive 10-15 minutes early (or log in early for virtual)",
            "Bring extra copies of your resume",
            "Follow up with a thank-you email within 24 hours",
            "Be specific with examples - use numbers when possible",
            "Show enthusiasm for the role and company",
            "Listen carefully and ask for clarification if needed"
        ]


def generate_interview_questions(job_data: Dict, count: int = 10) -> List[Dict]:
    """Convenience function to generate interview questions"""
    prep = InterviewPrep(job_data)
    return prep.generate_questions(count)
