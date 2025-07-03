import warnings

import dspy
from dotenv import load_dotenv

from config import Config
from display import get_user_input, print_error, print_model_info, print_welcome
from features import Feature, activate_features

# --- Configuration ---

# Load environment variables (e.g., API keys) from a .env file
load_dotenv()

# Suppress specific warnings if necessary
warnings.filterwarnings("ignore", category=UserWarning)

# --- Main Execution ---


def main(config: Config) -> None:
    """Configures LM, allows manual mode selection, refines input based on mode, and prints results."""

    # Configure the primary language model for generation tasks
    try:
        # Configure the LM with
        lm = dspy.LM(**config.lm)
        dspy.configure(lm=lm)
        print_model_info(lm.dump_state())
    except Exception as e:
        print_error(
            f"Error configuring Language Model: {e}\nPlease ensure your LM provider is configured correctly."
        )
        return  # Exit if LM can't be configured

    # --- Feature Configuration ---
    features = activate_features()
    feature_map: dict[str, Feature] = {f.name: f for f in features}

    # --- Mode Selection Logic ---
    current_mode: str | None = None
    mode_map: dict[str, str] = {str(f.number): f.name for f in features}

    print_welcome(features)

    while True:
        try:
            # Determine prompt based on current mode
            current_description = (
                feature_map[current_mode].description
                if current_mode
                else "No Mode Selected"
            )
            prompt_mode_indicator = f"[{current_description}]"
            prompt_text = (
                f"\n{prompt_mode_indicator} Enter text (or mode number to switch): "
            )
            user_input: str = get_user_input(prompt_text).strip()

            while (
                user_input
                and user_input not in mode_map
                and len(user_input) < config.minimum_input_length
            ):
                print_error(
                    f"Input too short. Please enter at least {config.minimum_input_length} characters."
                )
                user_input = get_user_input(prompt_text).strip()

            # --- Exit Condition ---
            if not user_input:
                print("\nBye! Stay chill.")
                break

            # --- Mode Switching ---
            if user_input in mode_map:
                new_mode = mode_map[user_input]
                if new_mode != current_mode:
                    current_mode = new_mode
                    print(
                        f"\n--- Switched to '{feature_map[current_mode].description}' mode ---"
                    )
                else:
                    print(
                        f"\n--- Already in '{feature_map[current_mode].description}' mode ---"
                    )
                continue

            # --- Check if Mode is Set ---
            if current_mode is None:
                print_error(
                    f"No mode selected. Please enter one of {list(mode_map.keys())} first."
                )
                continue

            # --- Process Text Based on Current Mode ---
            selected_feature = feature_map[current_mode]
            try:
                # Prepare the input for the predictor dynamically
                predictor_input = {selected_feature.input_field: user_input}
                response = selected_feature.predictor(**predictor_input)

                # Call the feature-specific response handler
                selected_feature.response_handler(response)

            except Exception as e:
                print_error(
                    f"Error processing input in '{selected_feature.description}' mode: {e}"
                )
                continue

        except EOFError:  # Handle Ctrl+D press
            print("\nBye! Stay chill.")
            break
        except KeyboardInterrupt:  # Handle Ctrl+C press
            print("\nInterrupted. Bye!")
            break


if __name__ == "__main__":
    # Instantiate the configuration
    app_config = Config()
    # Run the main application
    main(app_config)
