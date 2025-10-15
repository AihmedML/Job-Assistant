#!/usr/bin/env python3
"""
Job Application Assistant - AI-powered job application optimizer
"""
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from pathlib import Path
import sys

from parsers.resume_parser import parse_resume
from parsers.job_parser import parse_job
from analyzer.ats_optimizer import ATSOptimizer
from generators.cover_letter import CoverLetterGenerator
from generators.interview_prep import InterviewPrep
import config

console = Console()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Job Application Assistant - Your AI-powered career companion"""
    pass


@cli.command()
@click.option('--resume', '-r', required=True, type=click.Path(exists=True),
              help='Path to your resume (PDF or DOCX)')
@click.option('--job', '-j', required=True, type=click.Path(exists=True),
              help='Path to job posting text file')
@click.option('--output', '-o', type=click.Path(), help='Save report to file')
def optimize(resume, job, output):
    """Analyze resume against job posting and get ATS optimization suggestions"""
    console.print("\n[bold cyan]Job Application Assistant[/bold cyan]", justify="center")
    console.print("[dim]Optimizing your resume for ATS systems...[/dim]\n")

    try:
        # Parse resume
        with console.status("[bold green]Parsing resume..."):
            resume_data = parse_resume(resume)
        console.print("[green][/green] Resume parsed successfully")

        # Parse job posting
        with console.status("[bold green]Analyzing job posting..."):
            with open(job, 'r', encoding='utf-8') as f:
                job_text = f.read()
            job_data = parse_job(job_text)
        console.print("[green][/green] Job posting analyzed successfully")

        # Run ATS optimization
        with console.status("[bold green]Running ATS analysis..."):
            optimizer = ATSOptimizer(resume_data, job_data)
            analysis = optimizer.analyze()
            ats_score = optimizer.get_ats_score()

        console.print("[green][/green] Analysis complete!\n")

        # Display results
        _display_optimization_results(analysis, ats_score)

        # Save to file if requested
        if output:
            _save_report(analysis, ats_score, output)
            console.print(f"\n[green]Report saved to: {output}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--resume', '-r', required=True, type=click.Path(exists=True),
              help='Path to your resume (PDF or DOCX)')
@click.option('--job', '-j', required=True, type=click.Path(exists=True),
              help='Path to job posting text file')
@click.option('--tone', '-t', default='professional',
              type=click.Choice(['professional', 'enthusiastic', 'confident']),
              help='Cover letter tone')
@click.option('--output', '-o', type=click.Path(), help='Save cover letter to file')
def cover_letter(resume, job, tone, output):
    """Generate AI-powered cover letter"""
    console.print("\n[bold cyan]Generating Cover Letter[/bold cyan]", justify="center")
    console.print(f"[dim]Tone: {tone}[/dim]\n")

    try:
        # Parse resume
        with console.status("[bold green]Parsing resume..."):
            resume_data = parse_resume(resume)

        # Parse job posting
        with console.status("[bold green]Analyzing job posting..."):
            with open(job, 'r', encoding='utf-8') as f:
                job_text = f.read()
            job_data = parse_job(job_text)

        # Generate cover letter
        with console.status("[bold green]Generating cover letter... (this may take a moment)"):
            generator = CoverLetterGenerator(resume_data, job_data)
            letter = generator.generate(tone=tone)

        console.print("[green][/green] Cover letter generated!\n")

        # Display cover letter
        panel = Panel(
            letter,
            title="[bold]Your Cover Letter[/bold]",
            border_style="cyan"
        )
        console.print(panel)

        # Save to file if requested
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(letter)
            console.print(f"\n[green]Cover letter saved to: {output}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--job', '-j', required=True, type=click.Path(exists=True),
              help='Path to job posting text file')
@click.option('--count', '-c', default=10, help='Number of questions to generate')
@click.option('--resume', '-r', type=click.Path(exists=True),
              help='Optional: Your resume for personalized prep')
def interview_prep(job, count, resume):
    """Generate interview preparation questions and tips"""
    console.print("\n[bold cyan]Interview Preparation[/bold cyan]", justify="center")
    console.print(f"[dim]Generating {count} likely interview questions...[/dim]\n")

    try:
        # Parse job posting
        with console.status("[bold green]Analyzing job posting..."):
            with open(job, 'r', encoding='utf-8') as f:
                job_text = f.read()
            job_data = parse_job(job_text)

        resume_data = None
        if resume:
            with console.status("[bold green]Parsing resume..."):
                resume_data = parse_resume(resume)

        # Generate interview prep
        with console.status("[bold green]Generating interview questions..."):
            prep = InterviewPrep(job_data, resume_data)
            questions = prep.generate_questions(count)
            questions_to_ask = prep.generate_questions_to_ask()

        console.print("[green][/green] Interview prep ready!\n")

        # Display questions
        _display_interview_questions(questions)

        # Display questions to ask
        console.print("\n[bold cyan]Questions You Should Ask:[/bold cyan]")
        for i, q in enumerate(questions_to_ask[:5], 1):
            console.print(f"{i}. {q}")

        # General tips
        console.print("\n[bold cyan]Quick Tips:[/bold cyan]")
        tips = prep._get_general_tips()
        for tip in tips[:5]:
            console.print(f"• {tip}")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--resume', '-r', required=True, type=click.Path(exists=True),
              help='Path to your resume (PDF or DOCX)')
def parse(resume):
    """Parse and display resume information"""
    console.print("\n[bold cyan]Resume Parser[/bold cyan]", justify="center")

    try:
        with console.status("[bold green]Parsing resume..."):
            resume_data = parse_resume(resume)

        console.print("[green][/green] Resume parsed successfully!\n")

        # Display parsed data
        if resume_data.get('email'):
            console.print(f"[cyan]Email:[/cyan] {resume_data['email']}")
        if resume_data.get('phone'):
            console.print(f"[cyan]Phone:[/cyan] {resume_data['phone']}")

        if resume_data.get('skills'):
            console.print(f"\n[cyan]Skills Found ({len(resume_data['skills'])}):[/cyan]")
            console.print(", ".join(resume_data['skills'][:20]))

        if resume_data.get('education'):
            console.print(f"\n[cyan]Education:[/cyan]")
            for edu in resume_data['education'][:3]:
                console.print(f"• {edu}")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


def _display_optimization_results(analysis, ats_score):
    """Display optimization results in a nice format"""
    # Overall scores
    table = Table(title="[bold]Match Analysis[/bold]")
    table.add_column("Metric", style="cyan")
    table.add_column("Score", justify="right", style="green")
    table.add_column("Status", style="yellow")

    table.add_row(
        "Overall Match",
        f"{analysis['overall_score']}%",
        analysis['status']
    )
    table.add_row(
        "Skill Match",
        f"{analysis['skill_match_score']}%",
        "Good" if analysis['skill_match_score'] >= 60 else "Needs Work"
    )
    table.add_row(
        "ATS Compatibility",
        f"{ats_score['score']}%",
        ats_score['recommendation']
    )

    console.print(table)

    # Matched skills
    if analysis['matched_skills']:
        console.print(f"\n[green]Matched Skills ({len(analysis['matched_skills'])}):[/green]")
        console.print(", ".join(analysis['matched_skills'][:15]))

    # Missing skills
    if analysis['missing_skills']:
        console.print(f"\n[yellow]Missing Skills (Add if applicable):[/yellow]")
        console.print(", ".join(analysis['missing_skills'][:15]))

    # Suggestions
    console.print("\n[bold cyan]Optimization Suggestions:[/bold cyan]")
    for i, suggestion in enumerate(analysis['suggestions'], 1):
        console.print(f"{i}. {suggestion}")


def _display_interview_questions(questions):
    """Display interview questions in a nice format"""
    table = Table(title="[bold]Likely Interview Questions[/bold]")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Question", style="white")
    table.add_column("Type", style="yellow", width=15)

    for i, q in enumerate(questions, 1):
        table.add_row(
            str(i),
            q['question'],
            q['type']
        )

    console.print(table)


def _save_report(analysis, ats_score, output_path):
    """Save analysis report to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("JOB APPLICATION ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Overall Match Score: {analysis['overall_score']}%\n")
        f.write(f"Skill Match Score: {analysis['skill_match_score']}%\n")
        f.write(f"ATS Score: {ats_score['score']}%\n\n")
        f.write(f"Status: {analysis['status']}\n\n")

        f.write("MATCHED SKILLS\n")
        f.write("-" * 50 + "\n")
        f.write(", ".join(analysis['matched_skills']) + "\n\n")

        f.write("MISSING SKILLS\n")
        f.write("-" * 50 + "\n")
        f.write(", ".join(analysis['missing_skills']) + "\n\n")

        f.write("SUGGESTIONS\n")
        f.write("-" * 50 + "\n")
        for i, suggestion in enumerate(analysis['suggestions'], 1):
            f.write(f"{i}. {suggestion}\n")


if __name__ == '__main__':
    # Check for API key
    if not config.ANTHROPIC_API_KEY and not config.OPENAI_API_KEY:
        console.print("[red]Error: No API key found![/red]")
        console.print("Please set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env file")
        sys.exit(1)

    cli()
