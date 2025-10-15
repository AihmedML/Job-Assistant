"""Configuration for Job Application Assistant"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RESUMES_DIR = DATA_DIR / "resumes"
OUTPUTS_DIR = DATA_DIR / "outputs"

# Create directories if they don't exist
for dir_path in [DATA_DIR, RESUMES_DIR, OUTPUTS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # anthropic or openai
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Model settings
ANTHROPIC_MODEL = "claude-3-haiku-20240307"  # Claude 3 Haiku (most accessible)
OPENAI_MODEL = "gpt-4o-mini"  # Using gpt-4o-mini (more accessible and cost-effective)

# ATS Keywords - Common skills and technologies
COMMON_SKILLS = [
    "python", "java", "javascript", "sql", "react", "node.js",
    "machine learning", "data analysis", "project management",
    "agile", "scrum", "communication", "leadership"
]

# Application limits (for monetization)
FREE_TIER_LIMIT = 3
PAID_TIER_LIMIT = -1  # unlimited
