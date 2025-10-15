"""Keyword matching between resume and job posting"""
from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class KeywordMatcher:
    """Match keywords between resume and job posting"""

    def __init__(self, resume_data: Dict, job_data: Dict):
        self.resume_data = resume_data
        self.job_data = job_data
        self.resume_text = resume_data.get('raw_text', '')
        self.job_text = job_data.get('raw_text', '')

    def calculate_match_score(self) -> float:
        """Calculate overall match score using TF-IDF similarity"""
        if not self.resume_text or not self.job_text:
            return 0.0

        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([self.resume_text, self.job_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0] * 100)  # Convert to percentage
        except Exception:
            return 0.0

    def get_skill_match(self) -> Dict:
        """Compare skills between resume and job"""
        resume_skills = set(skill.lower() for skill in self.resume_data.get('skills', []))
        job_skills = set(skill.lower() for skill in self.job_data.get('required_skills', []))

        matched_skills = resume_skills & job_skills
        missing_skills = job_skills - resume_skills

        return {
            'matched': list(matched_skills),
            'missing': list(missing_skills),
            'match_percentage': (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
        }

    def get_missing_keywords(self) -> List[str]:
        """Get important keywords from job that are missing in resume"""
        job_skills = set(skill.lower() for skill in self.job_data.get('required_skills', []))
        resume_skills = set(skill.lower() for skill in self.resume_data.get('skills', []))
        job_keywords = set(keyword.lower() for keyword in self.job_data.get('keywords', []))

        # Find missing skills
        missing_skills = job_skills - resume_skills

        # Find missing keywords
        resume_text_lower = self.resume_text.lower()
        missing_keywords = [kw for kw in job_keywords if kw not in resume_text_lower]

        return list(missing_skills) + missing_keywords

    def get_optimization_suggestions(self) -> List[str]:
        """Generate suggestions for optimizing resume"""
        suggestions = []
        skill_match = self.get_skill_match()

        # Skill suggestions
        if skill_match['missing']:
            suggestions.append(
                f"Add these skills to your resume (if applicable): {', '.join(skill_match['missing'][:5])}"
            )

        # Experience level
        job_exp = self.job_data.get('experience_level', '')
        if job_exp and job_exp != 'not specified':
            suggestions.append(
                f"Highlight experience relevant to {job_exp} level position"
            )

        # Keywords
        missing_kw = self.get_missing_keywords()
        if missing_kw:
            suggestions.append(
                f"Include action words: {', '.join(missing_kw[:5])}"
            )

        # Education
        job_education = self.job_data.get('education', [])
        resume_education = self.resume_data.get('education', [])
        if job_education and not resume_education:
            suggestions.append("Add your education details if they match requirements")

        return suggestions

    def generate_report(self) -> Dict:
        """Generate comprehensive matching report"""
        match_score = self.calculate_match_score()
        skill_match = self.get_skill_match()
        suggestions = self.get_optimization_suggestions()

        return {
            'overall_score': round(match_score, 2),
            'skill_match_score': round(skill_match['match_percentage'], 2),
            'matched_skills': skill_match['matched'],
            'missing_skills': skill_match['missing'],
            'suggestions': suggestions,
            'status': self._get_status(match_score)
        }

    def _get_status(self, score: float) -> str:
        """Get match status based on score"""
        if score >= 75:
            return "Excellent match - Apply with confidence!"
        elif score >= 60:
            return "Good match - Consider applying"
        elif score >= 45:
            return "Fair match - Optimize resume before applying"
        else:
            return "Poor match - May need significant resume updates"
