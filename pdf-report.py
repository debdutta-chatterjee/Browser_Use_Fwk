import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_from_json_file(json_filename, pdf_filename="output.pdf"):
    """
    Generates a PDF file from JSON data read from a file.

    Args:
        json_filename (str): The name of the JSON file.
        pdf_filename (str): The name of the output PDF file.
    """
    try:
        with open(json_filename, 'r') as file:
            json_string = file.read()
            json_data = json.loads(json_string)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_filename}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_filename}'.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for step in json_data["history"]:
        model_output = step["model_output"]
        result = step["result"]
        state = step["state"]
        metadata = step["metadata"]

        # Step Header
        story.append(Paragraph(f"<b>Step {metadata['step_number']}</b>", styles['Heading2']))
        story.append(Spacer(1, 12))

        # Model Output
        if model_output:
            story.append(Paragraph("<b>Model Output:</b>", styles['Heading3']))
            story.append(Paragraph(f"Next Goal: {model_output['current_state']['next_goal']}", styles['Normal']))
            if "memory" in model_output["current_state"]:
                story.append(Paragraph(f"Memory: {model_output['current_state']['memory']}", styles['Normal']))

            if "action" in model_output:
                story.append(Paragraph("<b>Actions:</b>", styles['Normal']))
                for action_item in model_output["action"]:
                    for action_type, action_details in action_item.items():
                        if action_type == "go_to_url":
                            story.append(Paragraph(f"- Go to URL: {action_details['url']}", styles['Normal']))
                        elif action_type == "input_text":
                            story.append(Paragraph(f"- Input Text (Index {action_details['index']}): {action_details['text']}", styles['Normal']))
                        elif action_type == "click_element":
                            story.append(Paragraph(f"- Click Element (Index {action_details['index']})", styles['Normal']))
                        elif action_type == "extract_content":
                            story.append(Paragraph(f"- Extract Content: {action_details['goal']}", styles['Normal']))
                        elif action_type == "wait":
                            story.append(Paragraph(f"- Wait: {action_details['seconds']} seconds", styles['Normal']))
                        elif action_type == "done":
                            story.append(Paragraph(f"- Done: {json.dumps(action_details, indent=2)}", styles['Normal']))

            story.append(Spacer(1, 12))

        # Result
        if result:
            story.append(Paragraph("<b>Result:</b>", styles['Heading3']))
            for result_item in result:
                story.append(Paragraph(f"- {result_item['extracted_content']}", styles['Normal']))
            story.append(Spacer(1, 12))

        # State
        if state:
            story.append(Paragraph("<b>State:</b>", styles['Heading3']))
            story.append(Paragraph(f"- URL: {state['url']}", styles['Normal']))
            story.append(Paragraph(f"- Title: {state['title']}", styles['Normal']))

            if state["interacted_element"]:
                story.append(Paragraph("<b>Interacted Elements:</b>", styles['Normal']))
                for element in state["interacted_element"]:
                    if element:
                        story.append(Paragraph(f"- Tag Name: {element['tag_name']}", styles['Normal']))
                        story.append(Paragraph(f"- XPath: {element['xpath']}", styles['Normal']))
                        if 'attributes' in element:
                            story.append(Paragraph(f"- Attributes: {json.dumps(element['attributes'], indent=2)}", styles['Normal']))

            story.append(Spacer(1, 12))

        # Metadata
        story.append(Paragraph("<b>Metadata:</b>", styles['Heading3']))
        story.append(Paragraph(f"- Step Start Time: {metadata['step_start_time']}", styles['Normal']))
        story.append(Paragraph(f"- Step End Time: {metadata['step_end_time']}", styles['Normal']))
        story.append(Paragraph(f"- Input Tokens: {metadata['input_tokens']}", styles['Normal']))
        story.append(Spacer(1, 24))

    doc.build(story)
    print(f"PDF generated successfully: {pdf_filename}")

# Example usage (assuming you have a file named 'data.json')
json_file_path = "data.json"  # Replace with your JSON file's path
generate_pdf_from_json_file('result.json')