# Job Application Assistant

An AI-powered assistant for improving job applications by analyzing resumes, comparing them against job descriptions, and generating targeted application materials.

## What it does

- Parses resumes from PDF/DOCX files
- Analyzes job descriptions and extracts key requirements
- Compares resume content against job requirements
- Suggests ATS-focused improvements
- Generates personalized cover letters
- Creates interview preparation questions

## Why I built it

This project helped me practice building practical AI tools around real workflows: document parsing, LLM prompting, structured outputs, and automation for job seekers.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_api_key_here

# Or use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

Run the assistant:

```bash
python main.py
```

## Usage

Analyze a job and optimize a resume:

```bash
python main.py optimize --resume my_resume.pdf --job job_posting.txt
```

Generate a cover letter:

```bash
python main.py cover-letter --resume my_resume.pdf --job job_posting.txt
```

Generate interview prep questions:

```bash
python main.py interview-prep --job job_posting.txt
```

## Tech focus

- Python CLI development
- Resume/document parsing
- LLM-powered text generation
- Prompt engineering
- Practical AI automation

## Planned improvements

- Add a simple web UI
- Add structured JSON outputs
- Add better scoring explanations
- Add example files and screenshots
- Add tests for parsing and prompt outputs

## About me

I am Ahmed, documenting my AI/ML journey publicly while building real projects from scratch.

- GitHub: [AihmedML](https://github.com/AihmedML)
- X: [@Aihmed_ML](https://x.com/Aihmed_ML)

## License

MIT
