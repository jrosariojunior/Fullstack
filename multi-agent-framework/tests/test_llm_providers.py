"""
Tests for LLM provider implementations.

Tests Claude, OpenAI, and provider factory.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestLLMFactory:
    """Test LLM provider factory."""

    def test_create_claude_provider(self):
        """Factory should create Claude provider."""
        from backend.llm.llm_factory import LLMFactory

        provider = LLMFactory.create(
            "claude",
            api_key="test-key",
            temperature=0.7
        )

        assert provider is not None
        assert hasattr(provider, "call")

    def test_create_openai_provider(self):
        """Factory should create OpenAI provider."""
        from backend.llm.llm_factory import LLMFactory

        provider = LLMFactory.create(
            "openai",
            api_key="test-key",
            temperature=0.7
        )

        assert provider is not None
        assert hasattr(provider, "call")

    def test_create_invalid_provider(self):
        """Factory should raise error for invalid provider."""
        from backend.llm.llm_factory import LLMFactory

        with pytest.raises(ValueError):
            LLMFactory.create("invalid_provider", api_key="test")


class TestClaudeProvider:
    """Test Claude provider implementation."""

    @pytest.mark.asyncio
    async def test_claude_call(self):
        """Claude provider should make API calls."""
        from backend.llm.claude_provider import ClaudeProvider

        with patch('anthropic.AsyncAnthropic') as mock_client:
            provider = ClaudeProvider(api_key="test-key")

            # Mock the response
            mock_message = MagicMock()
            mock_message.content = [MagicMock(text="Test response")]
            mock_client.return_value.messages.create = AsyncMock(
                return_value=mock_message
            )

            # Test would verify the call was made
            # result = await provider.call("Test prompt")
            # assert result == "Test response"

    @pytest.mark.asyncio
    async def test_claude_validate_connection(self):
        """Claude provider should validate API connection."""
        from backend.llm.claude_provider import ClaudeProvider

        provider = ClaudeProvider(api_key="test-key")

        with patch.object(provider, 'call', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "OK"
            # result = await provider.validate_connection()
            # assert result is True


class TestOpenAIProvider:
    """Test OpenAI provider implementation."""

    @pytest.mark.asyncio
    async def test_openai_call(self):
        """OpenAI provider should make API calls."""
        from backend.llm.openai_provider import OpenAIProvider

        provider = OpenAIProvider(api_key="test-key")

        with patch.object(provider, 'client') as mock_client:
            # Mock would be setup here
            pass

    @pytest.mark.asyncio
    async def test_openai_validate_connection(self):
        """OpenAI provider should validate API connection."""
        from backend.llm.openai_provider import OpenAIProvider

        provider = OpenAIProvider(api_key="test-key")

        # Test connection validation
        # This would verify API key is valid


class TestProviderInterface:
    """Test that all providers implement required interface."""

    def test_claude_has_required_methods(self):
        """Claude provider should have all required methods."""
        from backend.llm.claude_provider import ClaudeProvider
        from backend.llm.base_provider import BaseLLMProvider

        provider = ClaudeProvider(api_key="test-key")

        # Check all abstract methods are implemented
        assert hasattr(provider, "call")
        assert hasattr(provider, "call_structured")
        assert hasattr(provider, "stream")
        assert hasattr(provider, "batch_call")
        assert hasattr(provider, "validate_connection")

    def test_openai_has_required_methods(self):
        """OpenAI provider should have all required methods."""
        from backend.llm.openai_provider import OpenAIProvider

        provider = OpenAIProvider(api_key="test-key")

        # Check all abstract methods are implemented
        assert hasattr(provider, "call")
        assert hasattr(provider, "call_structured")
        assert hasattr(provider, "stream")
        assert hasattr(provider, "batch_call")
        assert hasattr(provider, "validate_connection")


class TestHumanization:
    """Test text humanization in providers."""

    @pytest.mark.asyncio
    async def test_claude_humanize_output(self):
        """Claude provider should have humanize capability."""
        from backend.llm.claude_provider import ClaudeProvider

        provider = ClaudeProvider(api_key="test-key")

        # Test humanization
        # result = provider.humanize_text("Technical output text")
        # assert result is not None
