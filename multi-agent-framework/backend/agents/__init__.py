"""
Agents - Módulo contendo todos os agentes especializados.
"""

from backend.agents.architect import ArchitectAgent
from backend.agents.analyst import AnalystAgent
from backend.agents.developer import DeveloperAgent
from backend.agents.reviewer import TechReviewerAgent
from backend.agents.qa_engineer import QAEngineerAgent
from backend.agents.prompts import get_agent_prompt, get_all_agent_names, AGENT_PROMPTS

__all__ = [
    "ArchitectAgent",
    "AnalystAgent",
    "DeveloperAgent",
    "TechReviewerAgent",
    "QAEngineerAgent",
    "get_agent_prompt",
    "get_all_agent_names",
    "AGENT_PROMPTS",
    "create_all_agents"
]


def create_all_agents(llm_provider):
    """
    Factory para criar todos os 5 agentes especializados.

    Args:
        llm_provider: Provider de LLM

    Returns:
        Dict com todos os agentes {name: agent}
    """
    return {
        "Architect": ArchitectAgent(llm_provider),
        "Analyst": AnalystAgent(llm_provider),
        "Developer": DeveloperAgent(llm_provider),
        "TechReviewer": TechReviewerAgent(llm_provider),
        "QAEngineer": QAEngineerAgent(llm_provider)
    }
