import os
import warnings
from typing import Optional, Dict

import dspy
from dotenv import load_dotenv

# --- Configuration ---

# Load environment variables (e.g., API keys) from a .env file
load_dotenv()

# Suppress specific warnings if necessary
warnings.filterwarnings("ignore", category=UserWarning)

# Define constants for intentions/modes
INTENTION_WRITING = "writing"
INTENTION_COMMIT = "commit"
INTENTION_ASK = "ask"

# --- DSPy Signatures ---

class CommitMessageSignature(dspy.Signature):
    """Clean up my commit message according to common conventions."""
    commit_msg: str = dspy.InputField(desc="Input commit message")
    refined_msg: str = dspy.OutputField(desc="Improved commit message")
    explanation: str = dspy.OutputField(desc="Explain the changes made or why the original was good.")

class WritingSignature(dspy.Signature):
    """Improve my English writing for clarity, grammar, and style."""
    text: str = dspy.InputField(desc="Input English text")
    improved_text: str = dspy.OutputField(desc="Rewritten text with improvements")
    suggestion: str = dspy.OutputField(desc="Alternative phrasing suggestion (optional)")
    explanation: str = dspy.OutputField(desc="Explain grammar/style issues or areas for improvement. If good, acknowledge it.")

class SimpleQASignature(dspy.Signature):
    """Straightforward and concise, offering a clear and uncomplicated answer to question"""
    question: str = dspy.InputField(desc="Input question")
    answer: str = dspy.OutputField(desc="An easy-to-understand response that doesn't involve complex details or explanations.")


# --- Helper Function ---

def print_response(
    title: str,
    refined_text: str,
    explanation: str,
    suggestion: Optional[str] = None
) -> None:
    """Formats and prints the response from the LM."""
    print(f"\n{title}")
    print("\n[[Refined]]")
    print(refined_text)
    print("\n[[Explanation]]")
    print(explanation)
    if suggestion and suggestion.strip():
        print("\n[[Suggestion]]")
        print(suggestion)
    print("-" * 40)

# --- Main Execution ---

def main() -> None:
    """Configures LM, allows manual mode selection, refines input based on mode, and prints results."""

    # Configure the primary language model for generation tasks
    try:
        generator_lm = dspy.LM('gemini/gemini-2.5-flash-preview-04-17', temperature=0.7, cache=False)
        # Set the default LM for dspy modules
        dspy.configure(lm=generator_lm)
    except Exception as e:
        print(f"Error configuring Language Model: {e}")
        print("Please ensure your LM provider (e.g., Gemini) is configured correctly.")
        print("This might involve setting API keys as environment variables.")
        return # Exit if LM can't be configured

    # Initialize the predictors (DSPy modules)
    try:
        writing_predictor = dspy.ChainOfThought(WritingSignature)
        commit_msg_predictor = dspy.ChainOfThought(CommitMessageSignature)
        simple_qa = dspy.ChainOfThought(SimpleQASignature)
    except Exception as e:
        print(f"Error initializing DSPy predictors: {e}")
        return

    # --- Mode Selection Logic ---
    current_mode: Optional[str] = None # Start with no mode selected
    mode_map: Dict[str, str] = {
        "0": INTENTION_ASK,
        "1": INTENTION_WRITING,
        "2": INTENTION_COMMIT,
    }
    mode_descriptions: Dict[str, str] = {
        INTENTION_ASK: "Ask Anything",
        INTENTION_WRITING: "Formal Writing",
        INTENTION_COMMIT: "Commit Message",
    }

    print("Welcome! Select an initial mode:")
    print("  0: Asking")
    print("  1: Formal Writing")
    print("  2: Commit Message")
    print("Enter the number to set the mode, then enter your text.")
    print("You can switch modes anytime by entering 0, 1 or 2.")
    print("Press Enter on an empty line to exit.")

    while True:
        try:
            # Determine prompt based on current mode
            prompt_mode_indicator = f"[{mode_descriptions.get(current_mode, 'No Mode Selected')}]"
            prompt_text = f"\n{prompt_mode_indicator} Enter text (or 0/1/2 to switch mode): "
            user_input: str = input(prompt_text).strip()

            # --- Exit Condition ---
            if not user_input:
                print("\nBye! Stay chill.")
                break

            # --- Mode Switching ---
            if user_input in mode_map:
                new_mode = mode_map[user_input]
                if new_mode != current_mode:
                    current_mode = new_mode
                    print(f"\n--- Switched to '{mode_descriptions[current_mode]}' mode ---")
                else:
                    # Optional: Inform user they are already in that mode
                    print(f"\n--- Already in '{mode_descriptions[current_mode]}' mode ---")
                continue # Go back to prompt for text in the new/current mode

            # --- Check if Mode is Set ---
            if current_mode is None:
                print("\nError: No mode selected. Please enter 0, 1, or 2 first.")
                continue

            # --- Process Text Based on Current Mode ---
            response = None
            try:
                if current_mode == INTENTION_WRITING:
                    response = writing_predictor(text=user_input)
                    print_response(
                        title=f"Refined for {mode_descriptions[current_mode]}",
                        refined_text=response.improved_text,
                        explanation=response.explanation,
                        suggestion=response.suggestion
                    )
                elif current_mode == INTENTION_COMMIT:
                    response = commit_msg_predictor(commit_msg=user_input)
                    print_response(
                        title=f"Refined for {mode_descriptions[current_mode]}",
                        refined_text=response.refined_msg,
                        explanation=response.explanation
                        # No suggestion field in CommitMessageSignature
                    )
                elif current_mode == INTENTION_ASK:
                    response = simple_qa(question=user_input)
                    print("\n[[Answer]]")
                    print(response.answer)

                # No else needed here as current_mode must be one of the above if not None

            except Exception as e:
                print(f"\nError processing input in '{mode_descriptions[current_mode]}' mode: {e}")
                print("Please check your input or try again.")
                # Optionally log the 'response' object if it exists before the error
                # if response: print(f"LM Raw Response before error: {response}")
                continue # Ask for new input

        except EOFError: # Handle Ctrl+D press
             print("\nBye! Stay chill.")
             break
        except KeyboardInterrupt: # Handle Ctrl+C press
            print("\nInterrupted. Bye!")
            break

if __name__ == "__main__":
    main()