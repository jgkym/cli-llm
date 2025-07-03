from cli_llm.display import print_refined_output


def handle_writing_response(response: any) -> None:
    """Formats and prints the response for the Writing feature."""
    output = f"""[bold turquoise2]Refined[/bold turquoise2]\n{response.improved_text}\n\n[bold turquoise2]Explanation[/bold turquoise2]\n{response.explanation}"""
    if (
        hasattr(response, "suggestion")
        and response.suggestion
        and response.suggestion.strip()
    ):
        output += f"\n\n[bold turquoise2]Suggestion[/bold turquoise2]\n{response.suggestion}"
    print_refined_output("Refined for Formal Writing", output)


def handle_commit_response(response: any) -> None:
    """Formats and prints the response for the Commit Message feature."""
    output = f"""[bold turquoise2]Refined[/bold turquoise2]\n{response.refined_msg}\n\n[bold turquoise2]Explanation[/bold turquoise2]\n{response.explanation}"""
    print_refined_output("Refined for Commit Message", output)


def handle_qa_response(response: any) -> None:
    """Formats and prints the response for the Simple QA feature."""
    print_refined_output("Answer", response.answer)
