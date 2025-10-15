"""Parse job postings and extract key requirements"""
import re
from typing import Dict, List
from utils.llm_client import llm


class JobParser:
    """Extract requirements and keywords from job postings"""

    def __init__(self, job_text: str):
        self.text = job_text
        self.data = {}

    def parse(self) -> Dict:
        """Parse job posting and extract structured data"""
        self.data = {
            'raw_text': self.text,
            'required_skills': self._extract_skills(),
            'experience_level': self._extract_experience_level(),
            'education': self._extract_education_requirements(),
            'keywords': self._extract_keywords(),
            'job_title': self._extract_job_title(),
            'company': self._extract_company(),
        }

        return self.data

    def _extract_skills(self) -> List[str]:
        """Extract required skills from job posting"""
        # Common technical skills
        skill_keywords = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'go', 'rust',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express',
            'machine learning', 'deep learning', 'ai', 'artificial intelligence',
            'data science', 'data analysis', 'statistics',
            'aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes',
            'git', 'github', 'agile', 'scrum', 'jira', 'ci/cd',
            'html', 'css', 'typescript', 'rest api', 'graphql', 'microservices',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'excel', 'powerpoint', 'word', 'office',
            'communication', 'leadership', 'teamwork', 'problem solving',
            'project management', 'stakeholder management'
        ]

        found_skills = []
        text_lower = self.text.lower()

        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill)

        return list(set(found_skills))

    def _extract_experience_level(self) -> str:
        """Determine experience level required"""
        text_lower = self.text.lower()

        # Experience patterns
        patterns = {
            'entry': ['entry level', 'junior', '0-2 years', 'recent graduate', 'new grad'],
            'mid': ['mid level', '2-5 years', '3-5 years', 'intermediate'],
            'senior': ['senior', '5+ years', '7+ years', 'experienced', 'lead'],
            'principal': ['principal', 'staff', '10+ years', 'architect']
        }

        for level, keywords in patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return level

        # Extract year ranges
        year_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', text_lower)
        if year_match:
            years = int(year_match.group(1))
            if years < 2:
                return 'entry'
            elif years < 5:
                return 'mid'
            elif years < 10:
                return 'senior'
            else:
                return 'principal'

        return 'not specified'

    def _extract_education_requirements(self) -> List[str]:
        """Extract education requirements"""
        education = []
        text_lower = self.text.lower()

        education_patterns = [
            "bachelor's degree", "master's degree", "phd", "doctorate",
            "b.s.", "m.s.", "b.a.", "m.a.", "mba",
            "computer science", "engineering", "related field"
        ]

        for pattern in education_patterns:
            if pattern in text_lower:
                education.append(pattern)

        return list(set(education))

    def _extract_keywords(self) -> List[str]:
        """Extract important keywords using TF-IDF-like approach"""
        # Common action words in job postings
        action_words = [
            'develop', 'design', 'implement', 'build', 'create', 'manage',
            'lead', 'collaborate', 'analyze', 'optimize', 'improve',
            'maintain', 'deploy', 'test', 'debug', 'troubleshoot'
        ]

        found_keywords = []
        text_lower = self.text.lower()

        for word in action_words:
            if word in text_lower:
                found_keywords.append(word)

        return found_keywords

    def _extract_job_title(self) -> str:
        """Attempt to extract job title"""
        lines = self.text.split('\n')
        # Assume job title is in the first few lines
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 5 and len(line) < 100:  # Reasonable title length
                # Check if it looks like a job title
                title_keywords = ['engineer', 'developer', 'analyst', 'manager',
                                  'scientist', 'designer', 'specialist', 'coordinator',
                                  'director', 'lead', 'senior', 'junior']
                if any(keyword in line.lower() for keyword in title_keywords):
                    return line

        return "Not found"

    def _extract_company(self) -> str:
        """Attempt to extract company name"""
        # Look for common patterns
        company_patterns = [
            r'(?:at|@)\s+([A-Z][A-Za-z0-9\s&,.-]+?)(?:\n|is|seeks)',
            r'([A-Z][A-Za-z0-9\s&,.-]+?)\s+is\s+(?:seeking|looking|hiring)',
        ]

        for pattern in company_patterns:
            match = re.search(pattern, self.text)
            if match:
                return match.group(1).strip()

        return "Not found"

    def get_ai_analysis(self) -> str:
        """Use LLM to analyze job posting"""
        prompt = f"""Analyze this job posting and provide:
1. Key technical skills required
2. Level of experience needed
3. Main responsibilities
4. Nice-to-have skills
5. Red flags or concerns

Job Posting:
{self.text[:2000]}  # Limit to avoid token limits

Provide a concise analysis."""

        try:
            return llm.generate(prompt)
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"


def parse_job(job_text: str) -> Dict:
    """Convenience function to parse a job posting"""
    parser = JobParser(job_text)
    return parser.parse()
