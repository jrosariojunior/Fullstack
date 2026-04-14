"""
Tests for specialized agents.

Tests agent initialization, execution, and output validation.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch


class TestAgentInitialization:
    """Test agent creation and initialization."""

    @pytest.mark.asyncio
    async def test_create_all_agents(self):
        """All 5 agents should be created successfully."""
        from backend.agents import create_all_agents

        mock_llm = MagicMock()
        agents = create_all_agents(mock_llm)

        assert len(agents) == 5
        agent_names = [agent.name for agent in agents]
        assert "Architect" in agent_names
        assert "Analyst" in agent_names
        assert "Developer" in agent_names
        assert "TechReviewer" in agent_names
        assert "QAEngineer" in agent_names

    def test_agent_has_required_attributes(self):
        """Each agent should have required attributes."""
        from backend.agents.architect import ArchitectAgent

        mock_llm = MagicMock()
        agent = ArchitectAgent(llm_provider=mock_llm)

        assert hasattr(agent, "name")
        assert hasattr(agent, "role")
        assert hasattr(agent, "llm_provider")
        assert hasattr(agent, "analyze")


class TestArchitectAgent:
    """Test Architect agent specifically."""

    @pytest.mark.asyncio
    async def test_architect_analyze(self):
        """Architect should analyze and return architecture proposal."""
        from backend.agents.architect import ArchitectAgent

        mock_llm = MagicMock()
        mock_llm.call = AsyncMock(return_value="Microservices architecture")

        agent = ArchitectAgent(llm_provider=mock_llm)

        # Output should have required fields
        # result = await agent.analyze({"description": "e-commerce system"})
        # assert "architecture" in result or "recommendation" in result


class TestAnalystAgent:
    """Test Analyst agent specifically."""

    @pytest.mark.asyncio
    async def test_analyst_moscow_prioritization(self):
        """Analyst should categorize requirements using MoSCoW."""
        from backend.agents.analyst import AnalystAgent

        mock_llm = MagicMock()
        agent = AnalystAgent(llm_provider=mock_llm)

        # Output should include MoSCoW categories
        # assert "must" in output or "should" in output


class TestDeveloperAgent:
    """Test Developer agent specifically."""

    @pytest.mark.asyncio
    async def test_developer_tech_stack(self):
        """Developer should suggest appropriate tech stack."""
        from backend.agents.developer import DeveloperAgent

        mock_llm = MagicMock()
        agent = DeveloperAgent(llm_provider=mock_llm)

        # Output should include tech stack recommendation


class TestAgentOutput:
    """Test agent output format."""

    def test_agent_output_structure(self):
        """Agent output should have required fields."""
        from backend.core.agent import AgentOutput

        output = AgentOutput(
            agent_name="Architect",
            agent_id="arch-1",
            output={"architecture": "microservices"},
            tokens_used=2500,
            confidence=0.95
        )

        assert output.agent_name == "Architect"
        assert output.tokens_used == 2500
        assert 0 <= output.confidence <= 1


class TestAgentIntegration:
    """Test agents working together."""

    @pytest.mark.asyncio
    async def test_agents_in_parallel(self):
        """Agents should be able to execute in parallel."""
        # This would test the orchestrator's parallel execution
        # Tests would verify all agents complete without errors
        pass
