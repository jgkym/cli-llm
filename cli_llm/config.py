from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration for the CLI tool."""

    lm: dict[str, any] = field(
        default_factory=lambda: {
            "model": "gemini/gemini-2.5-flash",
            "temperature": 0.7,
            "cache": False,
        }
    )
    minimum_input_length: int = 5
