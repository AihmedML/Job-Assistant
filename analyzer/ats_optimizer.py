"""ATS (Applicant Tracking System) optimization tools"""
from typing import Dict, List
from analyzer.keyword_matcher import KeywordMatcher


class ATSOptimizer:
    """Optimize resume for ATS systems"""

    def __init__(self, resume_data: Dict, job_data: Dict):
        self.resume_data = resume_data
        self.job_data = job_data
        self.matcher = KeywordMatcher(resume_data, job_data)

    def analyze(self) -> Dict:
        """Perform complete ATS analysis"""
        report = self.matcher.generate_report()

        # Add ATS-specific checks
        ats_checks = self._perform_ats_checks()
        report['ats_checks'] = ats_checks

        return report

    def _perform_ats_checks(self) -> Dict:
        """Check for common ATS compatibility issues"""
        checks = {
            'has_contact_info': self._check_contact_info(),
            'has_skills_section': self._check_skills_section(),
            'keyword_density': self._check_keyword_density(),
            'format_simple': True,  # We're assuming text extraction worked
        }

        return checks

    def _check_contact_info(self) -> bool:
        """Check if resume has contact information"""
        email = self.resume_data.get('email', '')
        phone = self.resume_data.get('phone', '')
        return bool(email or phone)

    def _check_skills_section(self) -> bool:
        """Check if resume has identifiable skills"""
        skills = self.resume_data.get('skills', [])
        return len(skills) > 0

    def _check_keyword_density(self) -> str:
        """Analyze keyword usage"""
        resume_text = self.resume_data.get('raw_text', '')
        job_skills = self.job_data.get('required_skills', [])

        if not job_skills:
            return "Cannot assess - no job skills identified"

        keyword_count = sum(1 for skill in job_skills if skill.lower() in resume_text.lower())
        density = (keyword_count / len(job_skills)) * 100

        if density >= 70:
            return "Good - Strong keyword presence"
        elif density >= 50:
            return "Fair - Could use more keywords"
        else:
            return "Low - Add more relevant keywords"

    def get_ats_score(self) -> Dict:
        """Calculate ATS compatibility score"""
        checks = self._perform_ats_checks()

        # Calculate score
        score = 0
        max_score = 0

        # Contact info (20 points)
        max_score += 20
        if checks['has_contact_info']:
            score += 20

        # Skills section (20 points)
        max_score += 20
        if checks['has_skills_section']:
            score += 20

        # Keyword density (40 points)
        max_score += 40
        density_status = checks['keyword_density']
        if "Good" in density_status:
            score += 40
        elif "Fair" in density_status:
            score += 25

        # Format (20 points)
        max_score += 20
        if checks['format_simple']:
            score += 20

        percentage = (score / max_score) * 100

        return {
            'score': round(percentage, 2),
            'details': checks,
            'recommendation': self._get_ats_recommendation(percentage)
        }

    def _get_ats_recommendation(self, score: float) -> str:
        """Get recommendation based on ATS score"""
        if score >= 80:
            return "Your resume is well-optimized for ATS systems"
        elif score >= 60:
            return "Your resume should pass most ATS systems with minor improvements"
        else:
            return "Your resume needs optimization to pass ATS screening"

    def generate_optimized_keywords(self) -> List[str]:
        """Generate list of keywords to add to resume"""
        missing_keywords = self.matcher.get_missing_keywords()

        # Prioritize skills over generic keywords
        job_skills = set(self.job_data.get('required_skills', []))
        resume_skills = set(self.resume_data.get('skills', []))
        missing_skills = job_skills - resume_skills

        # Return top priority keywords
        priority_keywords = list(missing_skills)[:10]
        other_keywords = [kw for kw in missing_keywords if kw not in priority_keywords][:5]

        return priority_keywords + other_keywords


def optimize_resume(resume_data: Dict, job_data: Dict) -> Dict:
    """Convenience function to optimize resume"""
    optimizer = ATSOptimizer(resume_data, job_data)
    return optimizer.analyze()
