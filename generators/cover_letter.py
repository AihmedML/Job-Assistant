"""AI-powered cover letter generation"""
from typing import Dict
from utils.llm_client import llm


class CoverLetterGenerator:
    """Generate personalized cover letters using LLM"""

    def __init__(self, resume_data: Dict, job_data: Dict):
        self.resume_data = resume_data
        self.job_data = job_data

    def generate(self, tone: str = "professional", include_salary: bool = False) -> str:
        """Generate a cover letter"""
        prompt = self._build_prompt(tone, include_salary)
        system_prompt = self._get_system_prompt()

        try:
            cover_letter = llm.generate(prompt, system_prompt=system_prompt, max_tokens=1500)
            return cover_letter
        except Exception as e:
            return f"Error generating cover letter: {str(e)}"

    def _build_prompt(self, tone: str, include_salary: bool) -> str:
        """Build the prompt for cover letter generation"""
        # Extract key information
        job_title = self.job_data.get('job_title', 'the position')
        company = self.job_data.get('company', 'your company')
        required_skills = self.job_data.get('required_skills', [])
        resume_skills = self.resume_data.get('skills', [])
        experience = self.resume_data.get('experience', [])

        # Match skills
        matched_skills = list(set(required_skills) & set(resume_skills))

        prompt = f"""Write a {tone} cover letter for:

Job Title: {job_title}
Company: {company}

Key Requirements from Job Posting:
{', '.join(required_skills[:10])}

My Relevant Skills:
{', '.join(matched_skills[:10]) if matched_skills else ', '.join(resume_skills[:10])}

Experience Keywords:
{', '.join(experience[:10]) if experience else 'N/A'}

Instructions:
- Keep it concise (3-4 paragraphs)
- Highlight how my skills match the job requirements
- Show enthusiasm for the role
- Use {tone} tone
- Make it ATS-friendly with relevant keywords
{'- Mention salary expectations if asked' if include_salary else '- Do not mention salary'}
- Start with a strong opening
- End with a clear call to action

Additional context from job posting:
{self.job_data.get('raw_text', '')[:500]}
"""
        return prompt

    def _get_system_prompt(self) -> str:
        """Get system prompt for cover letter generation"""
        return """You are an expert career coach and professional cover letter writer.
You write compelling, personalized cover letters that:
1. Match the candidate's experience to job requirements
2. Are ATS-optimized with relevant keywords
3. Show genuine interest and enthusiasm
4. Are concise and impactful (under 400 words)
5. Avoid generic phrases and cliches
6. Use active voice and strong action verbs

Generate cover letters that help candidates stand out."""

    def generate_multiple_versions(self, count: int = 3) -> list[str]:
        """Generate multiple versions with different tones"""
        tones = ["professional", "enthusiastic", "confident"]
        versions = []

        for i, tone in enumerate(tones[:count]):
            try:
                version = self.generate(tone=tone)
                versions.append({
                    'version': i + 1,
                    'tone': tone,
                    'content': version
                })
            except Exception as e:
                versions.append({
                    'version': i + 1,
                    'tone': tone,
                    'content': f"Error: {str(e)}"
                })

        return versions

    def get_improvement_suggestions(self, existing_letter: str) -> str:
        """Analyze and suggest improvements for an existing cover letter"""
        prompt = f"""Analyze this cover letter and provide specific improvement suggestions:

Cover Letter:
{existing_letter}

Job Requirements:
{', '.join(self.job_data.get('required_skills', [])[:10])}

Provide:
1. Overall assessment (score out of 10)
2. Strengths
3. Weaknesses
4. Specific improvements to make
5. Keywords to add for ATS optimization"""

        try:
            return llm.generate(prompt, max_tokens=1000)
        except Exception as e:
            return f"Error analyzing cover letter: {str(e)}"


def generate_cover_letter(resume_data: Dict, job_data: Dict, tone: str = "professional") -> str:
    """Convenience function to generate a cover letter"""
    generator = CoverLetterGenerator(resume_data, job_data)
    return generator.generate(tone=tone)
