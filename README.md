# Job Application Assistant

An AI-powered tool to optimize your job applications and increase interview chances.

## Features

- **Resume Parser**: Extract skills and experience from PDF/DOCX resumes
- **Job Analyzer**: Parse job postings to identify key requirements
- **ATS Optimizer**: Match your resume against job requirements (beat Applicant Tracking Systems)
- **Cover Letter Generator**: AI-generated personalized cover letters
- **Interview Prep**: Generate likely interview questions based on the job description

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API key:
```bash
# Use either Anthropic or OpenAI
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_api_key_here

# OR
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

3. Run the assistant:
```bash
python main.py
```

## Usage

```bash
# Analyze a job and optimize your resume
python main.py optimize --resume my_resume.pdf --job job_posting.txt

# Generate a cover letter
python main.py cover-letter --resume my_resume.pdf --job job_posting.txt

# Get interview prep questions
python main.py interview-prep --job job_posting.txt
```



## License

MIT
