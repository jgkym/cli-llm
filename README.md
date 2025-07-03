<div align='center'>
<h1>cli-llm</h1>

[![Release: 2025.7.0](https://img.shields.io/badge/Release-2025.7.0-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

> ***A boilerplate project designed to enhance LLM usability directly within your CLI.***

![demo](assets/demo.gif)

Stop context-switching and bring the power of LLMs to your terminal workflows. `cli-llm` provides a structured starting point to build personalized LLM tools tailored to your needs.

## About

Working in the terminal often involves repetitive text manipulation or generation tasks – drafting casual messages, refining technical writing, formatting commit messages, and more. `cli-llm` aims to streamline these tasks by integrating LLM capabilities directly into your CLI environment.

Instead of copying text to a separate web UI or application, you can use pre-defined modes within `cli-llm` to instantly apply LLM processing to your input, keeping you focused and efficient.

## Features

*   **Supercharge CLI Workflows:** Integrate LLM assistance without leaving your terminal.
*   **Rich CLI Experience:** Uses the `rich` library for a modern, visually appealing interface with formatted panels and colors.
*   **Customizable Presets:** Easily define and switch between frequently used LLM interaction modes. The included example demonstrates modes for:
    *   Asking (`ask`)
    *   Formal Writing (`writing`)
    *   Commit Messages (`commit`)
*   **Mode Persistence:** Stay in a specific interaction mode for multiple messages until you explicitly switch.
*   **DSPy Powered:** Leverages the DSPy framework for robust LLM interaction, allowing structured programming over simple prompting.
*   **Modular & Extensible:** The codebase is broken into logical modules, making it easy to add new features or change existing ones.

## Technology Stack

*   **[DSPy](https://dspy.ai/):** The core framework for programming foundation models.
*   **[Rich](https://github.com/Textualize/rich):** For beautiful and readable formatting in the terminal.
*   **LLM Backend:** Configurable to use various LLM providers (e.g., Gemini, OpenAI) supported by DSPy.

## Project Structure

The project is organized into several modules to separate concerns and make it easier to extend:

```
/
├── main.py            # Main application entry point, handles user interaction and mode switching.
├── config.py          # Central configuration for the application (e.g., LM settings).
├── features.py        # Defines the available features (modes) and their configurations.
├── signatures.py      # Contains all DSPy signatures for different tasks.
├── handlers.py        # Functions to process and format the responses from the LLM.
└── display.py         # Manages the CLI display using the `rich` library for better UI.
```

## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

*   [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jgkym/cli-llm
    cd cli-llm
    ```
2.  **Install dependencies:**
    ```bash
    uv sync --upgrade
    ```
3.  **Set up Environment Variables:**
    *   Create an environment file:
        ```bash
        touch .env
        ```
    *   Edit the `.env` file and add your API key. For Gemini:
        ```dotenv
        # .env
        GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```

## Usage

1.  **Run the main script:**
    ```bash
    python main.py

    #Or
    make run
    ```
2.  **Select an initial mode:** Enter the number corresponding to the feature you want to use. (e.g., `0` for `Summarize`, `1` for `Refine`, `2` for `YourNewFeature`)
3.  **Enter your text:** Type or paste the text you want the LLM to process.
4.  **View the output:** The script will print the refined text in a clean, formatted panel.
5.  **Switch modes:** Enter `0`, `1`, or `2` at the prompt to change the active mode.
6.  **Exit:** Press `Enter` on an empty line.

## Customization / Extending

The modular design makes it easy to add a new feature. If you're new to DSPy, there's no need to worry! It's very straightforward to learn, and [an intuitive guide](https://dspy.ai/learn/) is provided to help you get started.  

### 0. Configuration

You can configure LLMs and other settings in `config.py`. See [this link](https://dspy.ai/api/models/LM/) for details on LLM settings.


### 1. Define a Signature

In `signatures.py`, create a new class inheriting from `dspy.Signature` that defines the input and output fields for your new feature.

```python
# signatures.py
class YourNewSignature(dspy.Signature):
    """A brief description of what this signature does."""
    input_text: str = dspy.InputField(desc="Description of the input")
    output_text: str = dspy.OutputField(desc="Description of the output")
```

### 2. Create a Response Handler

In `handlers.py`, add a new function to format and display the output from your new signature. Use the functions from `display.py` to maintain a consistent UI. You can also directly allow a `lambda` function to handle the response.

```python
# handlers.py
from display import print_refined_output

def handle_your_new_feature(response: any) -> None:
    """Formats and prints the response for your new feature."""
    print_refined_output("Title for Your Feature", response.output_text)
```

### 3. Activate the Feature

In `features.py`, import your new signature and handler. Then, in the `activate_features` function, add a new `Feature` instance to the list. The order in the list determines the selection number.

```python
# features.py
from signatures import YourNewSignature
from handlers import handle_your_new_feature

def activate_features() -> List[Feature]:
    features = [
        # ... existing features
        Feature(
            name="your_feature_name",
            description="A short description for the menu",
            signature=YourNewSignature,
            input_field="input_text",  # Must match the InputField in your signature
            response_handler=handle_your_new_feature,
            number=777,  # The number for selection in the menu
        ),
    ]
    # ... rest of the function
```

That's it! The application will automatically pick up the new feature the next time you run it.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

Distributed under the MIT License. See `LICENSE` file for more information.
