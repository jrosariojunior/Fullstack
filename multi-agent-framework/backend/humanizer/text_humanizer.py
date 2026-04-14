"""
Text Humanizer - Converte output técnico AI em texto legível e fluido.

Transforma saídas estruturadas de agentes em narrativa mais humana e acessível.
"""

import re
from typing import Dict, Any, List, Optional


class TextHumanizer:
    """
    Humaniza textos técnicos de IA para leitura mais natural.

    Aplica técnicas de reescrita e reformatação para melhorar fluidez.
    """

    def __init__(self):
        """Inicializa humanizer com padrões e regras."""
        self.verbose_patterns = {
            r"The\s+(system|application|software)": "This solution",
            r"shall\s+be": "should be",
            r"must\s+be": "needs to be",
            r"in\s+order\s+to": "to",
            r"as\s+a\s+result\s+of": "because",
        }

    def humanize(self, text: str) -> str:
        """
        Humaniza texto removendo jargão técnico excessivo.

        Args:
            text: Texto a humanizar

        Returns:
            Texto mais humanizado
        """
        if not text or not isinstance(text, str):
            return text

        # Remove redundâncias
        text = self._remove_redundancy(text)

        # Simplifica linguagem técnica
        text = self._simplify_technical_language(text)

        # Melhora fluidez
        text = self._improve_readability(text)

        # Remove excesso de pontuação
        text = self._clean_punctuation(text)

        return text.strip()

    def humanize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Humaniza valores de um dicionário.

        Processa strings recursivamente, deixando estruturas intactas.

        Args:
            data: Dicionário com dados

        Returns:
            Dicionário com valores humanizados
        """
        if not isinstance(data, dict):
            return data

        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.humanize(value)
            elif isinstance(value, dict):
                result[key] = self.humanize_dict(value)
            elif isinstance(value, list):
                result[key] = self.humanize_list(value)
            else:
                result[key] = value

        return result

    def humanize_list(self, items: List[Any]) -> List[Any]:
        """Humaniza items em uma lista."""
        return [
            self.humanize(item) if isinstance(item, str)
            else self.humanize_dict(item) if isinstance(item, dict)
            else item
            for item in items
        ]

    def _remove_redundancy(self, text: str) -> str:
        """Remove palavras e frases redundantes."""
        # Remove repetições de palavras consecutivas
        text = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', text, flags=re.IGNORECASE)

        # Remove "very" antes de intensificadores
        text = re.sub(r'\bvery\s+(very|extremely|incredibly)\b', r'\1', text, flags=re.IGNORECASE)

        # Remove "it is" redundante
        text = re.sub(r'\bit\s+is\s+(that\s+)?important\s+to\s+note\s+that\s+', '', text, flags=re.IGNORECASE)

        return text

    def _simplify_technical_language(self, text: str) -> str:
        """Substitui jargão técnico por linguagem mais simples."""
        simplifications = {
            r'\bimplement\s+(\w+)\b': r'use \1',
            r'\butilize\b': 'use',
            r'\bfacilitate\b': 'enable',
            r'\boptimize\b': 'improve',
            r'\bmaintain\b': 'keep',
            r'\bmitigate\b': 'reduce',
            r'\bmitigating\b': 'reducing',
            r'\bensure\b': 'make sure',
            r'\bvalidate\b': 'check',
            r'\bverify\b': 'confirm',
            r'\bscalable\b': 'able to grow',
            r'\bresilience\b': 'ability to recover',
            r'\nasynchronous\b': 'non-blocking',
            r'\bdeployment\b': 'release',
            r'\binfrastructure\b': 'system',
            r'\barchitecture\b': 'design',
            r'\bmonolithic\b': 'single-piece',
            r'\bmicroservices\b': 'small connected services',
        }

        for pattern, replacement in simplifications.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text

    def _improve_readability(self, text: str) -> str:
        """Melhora legibilidade com quebras de linha e formatação."""
        # Converte listas bullet para formatação clara
        text = re.sub(r'^\s*[-•*]\s+', '- ', text, flags=re.MULTILINE)

        # Adiciona espaço após pontuação se necessário
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)

        # Remove múltiplos espaços
        text = re.sub(r'\s{2,}', ' ', text)

        # Remove quebras de linha desnecessárias
        text = re.sub(r'\n\s*\n+', '\n\n', text)

        return text

    def _clean_punctuation(self, text: str) -> str:
        """Remove pontuação excessiva."""
        # Remove múltiplos pontos finais
        text = re.sub(r'\.{2,}', '.', text)

        # Remove pontuação duplicada
        text = re.sub(r'([!?]){2,}', r'\1', text)

        # Remove espaços antes de pontuação
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)

        return text

    def humanize_agent_output(
        self,
        agent_name: str,
        output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Humaniza output de um agente específico.

        Aplica formatação e linguagem apropriada para cada tipo de agente.

        Args:
            agent_name: Nome do agente (Architect, Developer, etc)
            output: Output estruturado do agente

        Returns:
            Output humanizado
        """
        humanized = {}

        for key, value in output.items():
            if isinstance(value, str):
                humanized[key] = self.humanize(value)
            elif isinstance(value, dict):
                humanized[key] = self.humanize_dict(value)
            elif isinstance(value, list):
                humanized[key] = self.humanize_list(value)
            else:
                humanized[key] = value

        return humanized

    @staticmethod
    def format_analysis(title: str, content: str, items: Optional[List[str]] = None) -> str:
        """
        Formata análise estruturada com título e itens.

        Args:
            title: Título da análise
            content: Descrição principal
            items: Itens da análise (opcional)

        Returns:
            Análise formatada
        """
        result = f"{title}\n\n{content}"

        if items:
            result += "\n\nKey points:\n"
            for item in items:
                result += f"• {item}\n"

        return result

    @staticmethod
    def format_recommendation(action: str, reasoning: str) -> str:
        """
        Formata recomendação estruturada.

        Args:
            action: Ação recomendada
            reasoning: Justificativa

        Returns:
            Recomendação formatada
        """
        return f"**Recommendation:** {action}\n\n**Why:** {reasoning}"


# Instância global
humanizer = TextHumanizer()


async def humanize_text(text: str) -> str:
    """
    Função assíncrona para humanizar texto.

    Compatível com pipeline assíncrono.

    Args:
        text: Texto a humanizar

    Returns:
        Texto humanizado
    """
    return humanizer.humanize(text)


async def humanize_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Humaniza output estruturado.

    Args:
        output: Output a humanizar

    Returns:
        Output humanizado
    """
    return humanizer.humanize_dict(output)
