import os
import warnings
from dotenv import load_dotenv
from rich import print
from rich.prompt import Prompt
from pydantic import BaseModel, Field
from typing import Optional
import langroid as lr
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.task import Task
from langroid.language_models import OpenAIGPTConfig
from langroid.agent.tools.duckduckgo_search_tool import DuckduckgoSearchTool
import fire

# Suppress Redis warnings
warnings.filterwarnings("ignore", message="REDIS_PASSWORD")
warnings.filterwarnings("ignore", category=UserWarning, module="langroid")

MODEL = "groq/llama3-70b-8192"  # or "openai/gpt-4-turbo"

class ProspectData(BaseModel):
    name: str = Field(..., description="Prospect's full name")
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job title/role")
    website: Optional[str] = Field(None, description="Company website URL")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")

def generate_outreach(prospect: ProspectData) -> str:
    """Core function that can be imported and used programmatically"""
    llm_config = OpenAIGPTConfig(
        chat_model=MODEL,
        temperature=0.3,
        max_output_tokens=500,
    )

    # Research Agent
    researcher = ChatAgent(
        ChatAgentConfig(
            name="Researcher",
            system_message="""
            You are a research assistant. Use the duckduckgo_search tool to find:
            1. Company info (mission, recent news)
            2. Prospect's public content (LinkedIn posts, interviews)
            Return raw facts only, no analysis.
            """,
            llm=llm_config,
        )
    )
    researcher.enable_message(DuckduckgoSearchTool)

    # Personalizer Agent
    personalizer = ChatAgent(
        ChatAgentConfig(
            name="Personalizer",
            system_message=f"""
            You are a sales expert. Using research data:
            1. Identify 1-2 personalization hooks
            2. Draft a SHORT email (3-4 lines) with:
               - Personal hook
               - Value proposition (we help {prospect.company} with...)
               - Clear CTA
            
            Format:
            Subject: [Hook-related subject]
            Body:
            Hi [Name], [hook]...
            We help companies like yours [value prop].
            [Call-to-action question?]
            Best, [Your Name]
            """,
            llm=llm_config,
        )
    )

    # Task setup
    research_task = Task(
        researcher,
        name="Research",
        single_round=True,
        system_message="Gather data about the prospect and company",
    )

    personalize_task = Task(
        personalizer,
        name="Personalize",
        llm_delegate=True,
        interactive=False,
        system_message="Generate the outreach email",
    )
    personalize_task.add_sub_task(research_task)

    # Execute
    query = f"""
    Find information about:
    1. Company: {prospect.company} {f'website:{prospect.website}' if prospect.website else ''}
    2. Person: {prospect.name} {prospect.role} site:linkedin.com/in
    """
    
    result = personalize_task.run(query)
    return result.content if result else "Failed to generate email"

def main(prospect: Optional[ProspectData] = None) -> None:
    """CLI interface for the outreach generator"""
    print("\n[blue]⚡ AI Cold Outreach Personalizer[/blue]")
    load_dotenv()

    if not prospect:
        print("\n[bold]Enter prospect details:[/bold]")
        prospect = ProspectData(
            name=Prompt.ask("Prospect name"),
            company=Prompt.ask("Company"),
            role=Prompt.ask("Role"),
            website=Prompt.ask("Company website (optional)", default=""),
        )

    email = generate_outreach(prospect)
    
if "Subject:" in email:
    print("\n[green]✅ Generated Outreach Email:[/green]\n")
    print(email)
    
    # Show cost stats if available
    try:
        cost = lr.language_models.base.LLM.cost_summary()
        print(f"\n[dim]Cost: ${cost.total:.4f} (in: {cost.input_tokens}, out: {cost.output_tokens})[/dim]")
    except AttributeError:
        pass
else:
    print("\n[red]Failed to generate email:[/red]\n", email)

if __name__ == "__main__":
    fire.Fire(main)
