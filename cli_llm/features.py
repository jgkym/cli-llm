from dataclasses import dataclass, field
from typing import Callable

import dspy

import cli_llm.handlers as h
import cli_llm.signatures as s


@dataclass
class Feature:
    """Represents a single capability of the CLI tool."""

    name: str
    description: str
    signature: dspy.Signature  # Should be a dspy.Signature class
    input_field: str
    response_handler: Callable[[any], None]
    number: int  # The number used to select the feature
    predictor: dspy.Module = field(init=False, default=None)

    def __post_init__(self):
        """Initializes the DSPy predictor after the instance is created."""
        self.predictor = dspy.Predict(self.signature)


# --- Feature Definitions ---


def activate_features() -> list[Feature]:
    """Returns a list of activated features for the CLI tool."""
    features = [
        Feature(
            name="ask",
            description="Ask Anything",
            signature=s.SimpleQASignature,
            input_field="question",
            response_handler=h.handle_qa_response,
            number=0,
        ),
        Feature(
            name="writing",
            description="Formal Writing",
            signature=s.WritingSignature,
            input_field="text",
            response_handler=h.handle_writing_response,
            number=1,
        ),
        Feature(
            name="commit",
            description="Commit Message",
            signature=s.CommitMessageSignature,
            input_field="commit_msg",
            response_handler=h.handle_commit_response,
            number=2,
        ),
    ]
    return features
