"""LLM client wrapper supporting multiple providers"""
import config


class LLMClient:
    """Unified interface for LLM APIs"""

    def __init__(self, provider=None):
        self.provider = provider or config.LLM_PROVIDER
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        if self.provider == "anthropic":
            try:
                import anthropic
                return anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
            except ImportError:
                raise ImportError("Install anthropic: pip install anthropic")

        elif self.provider == "openai":
            try:
                import openai
                return openai.OpenAI(api_key=config.OPENAI_API_KEY)
            except ImportError:
                raise ImportError("Install openai: pip install openai")

        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def generate(self, prompt, system_prompt=None, max_tokens=2000):
        """Generate text using the configured LLM"""
        if self.provider == "anthropic":
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": config.ANTHROPIC_MODEL,
                "max_tokens": max_tokens,
                "messages": messages
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.client.messages.create(**kwargs)
            return response.content[0].text

        elif self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

        else:
            raise ValueError(f"Unknown provider: {self.provider}")


# Global instance
llm = LLMClient()
