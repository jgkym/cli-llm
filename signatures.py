import dspy

# --- DSPy Signatures ---


class CommitMessageSignature(dspy.Signature):
    """Clean up my commit message according to common conventions."""

    commit_msg: str = dspy.InputField(desc="Input commit message")
    refined_msg: str = dspy.OutputField(desc="Improved commit message")
    explanation: str = dspy.OutputField(
        desc="Explain the changes made or why the original was good."
    )


class WritingSignature(dspy.Signature):
    """Improve my English writing for clarity, grammar, and style."""

    text: str = dspy.InputField(desc="Input English text")
    improved_text: str = dspy.OutputField(desc="Rewritten text with improvements")
    suggestion: str = dspy.OutputField(
        desc="Alternative phrasing suggestion (optional)"
    )
    explanation: str = dspy.OutputField(
        desc="Explain grammar/style issues or areas for improvement. If good, acknowledge it."
    )


class SimpleQASignature(dspy.Signature):
    """Straightforward and concise, offering a clear and uncomplicated answer to question"""

    question: str = dspy.InputField(desc="Input question")
    answer: str = dspy.OutputField(
        desc="An easy-to-understand response that doesn't involve complex details or explanations."
    )
