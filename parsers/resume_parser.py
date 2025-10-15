"""Parse resumes from PDF and DOCX files"""
import re
from pathlib import Path
from typing import Dict, List
import pdfplumber
from docx import Document


class ResumeParser:
    """Extract text and structured data from resumes"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.text = ""
        self.data = {}

    def parse(self) -> Dict:
        """Parse the resume and extract structured data"""
        # Extract raw text based on file type
        if self.file_path.suffix.lower() == '.pdf':
            self.text = self._parse_pdf()
        elif self.file_path.suffix.lower() in ['.docx', '.doc']:
            self.text = self._parse_docx()
        else:
            raise ValueError(f"Unsupported file type: {self.file_path.suffix}")

        # Extract structured information
        self.data = {
            'raw_text': self.text,
            'email': self._extract_email(),
            'phone': self._extract_phone(),
            'skills': self._extract_skills(),
            'education': self._extract_education(),
            'experience': self._extract_experience_keywords(),
        }

        return self.data

    def _parse_pdf(self) -> str:
        """Extract text from PDF"""
        text = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")

        return '\n'.join(text)

    def _parse_docx(self) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(self.file_path)
            text = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(text)
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")

    def _extract_email(self) -> str:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, self.text)
        return match.group(0) if match else ""

    def _extract_phone(self) -> str:
        """Extract phone number from text"""
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, self.text)
        return match.group(0) if match else ""

    def _extract_skills(self) -> List[str]:
        """Extract skills from resume text"""
        # Common technical skills and keywords
        skill_keywords = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'machine learning', 'deep learning', 'ai', 'data science',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'agile', 'scrum', 'jira',
            'html', 'css', 'typescript', 'rest api', 'graphql',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
        ]

        found_skills = []
        text_lower = self.text.lower()

        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill)

        return list(set(found_skills))  # Remove duplicates

    def _extract_education(self) -> List[str]:
        """Extract education information"""
        education_keywords = ['bachelor', 'master', 'phd', 'b.s.', 'm.s.',
                              'b.a.', 'm.a.', 'associate', 'diploma', 'university',
                              'college', 'degree']

        education = []
        lines = self.text.split('\n')

        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                education.append(line.strip())

        return education[:3]  # Return top 3 education entries

    def _extract_experience_keywords(self) -> List[str]:
        """Extract key experience-related terms"""
        experience_keywords = [
            'led', 'managed', 'developed', 'designed', 'implemented',
            'created', 'built', 'improved', 'increased', 'reduced',
            'collaborated', 'coordinated', 'analyzed', 'optimized',
            'years of experience', 'experience in', 'worked on'
        ]

        found_keywords = []
        text_lower = self.text.lower()

        for keyword in experience_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)

        return list(set(found_keywords))


def parse_resume(file_path: str) -> Dict:
    """Convenience function to parse a resume"""
    parser = ResumeParser(file_path)
    return parser.parse()
