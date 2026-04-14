"""
Humanizer - Torna outputs técnicos de IA mais legíveis e naturais.
"""

from backend.humanizer.text_humanizer import (
    TextHumanizer,
    humanize_text,
    humanize_output,
    humanizer
)

__all__ = [
    "TextHumanizer",
    "humanize_text",
    "humanize_output",
    "humanizer"
]
