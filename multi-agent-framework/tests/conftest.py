"""
Pytest configuration and fixtures.

Shared fixtures and configuration for all tests.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_llm_provider():
    """Mock LLM provider for testing."""
    mock = MagicMock()
    mock.call = AsyncMock(return_value="Mock response")
    mock.call_structured = AsyncMock(return_value={"result": "structured"})
    mock.validate_connection = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_storage():
    """Mock storage manager for testing."""
    mock = MagicMock()
    mock.start_execution = AsyncMock(return_value="exec-123")
    mock.get_execution = AsyncMock(return_value={
        "id": "exec-123",
        "status": "running",
        "briefing": "test"
    })
    mock.get_agent_outputs = AsyncMock(return_value=[])
    mock.record_agent_output = AsyncMock()
    mock.finalize_execution = AsyncMock()
    return mock


@pytest.fixture
def sample_briefing():
    """Sample briefing for testing."""
    return {
        "description": "Build a scalable e-commerce platform",
        "requirements": [
            {
                "type": "functional",
                "description": "Shopping cart",
                "priority": "must"
            }
        ]
    }


@pytest.fixture
def sample_execution_config():
    """Sample execution configuration."""
    return {
        "parallel": True,
        "max_debate_rounds": 3,
        "token_limit": 100000,
        "humanize_output": True
    }
