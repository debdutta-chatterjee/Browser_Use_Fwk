import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import simpleSplit
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return ''.join(self.text)

def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()

class ReportUtil:

    def generate_pdf_from_json_file(json_filename, pdf_filename="./output/output.pdf"):
        """
        Generates a PDF file with table format for each step from JSON data read from a file.
        Fits text in cells, makes table width compact and consistent, and removes HTML tags.

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

            # Table Data
            table_data = []

            # Model Output
            if model_output:
                table_data.append([Paragraph("<b>Model Output</b>", styles['Normal']), ""])
                table_data.append(["Next Goal", strip_tags(model_output['current_state']['next_goal'])])
                if "memory" in model_output["current_state"]:
                    table_data.append(["Memory", strip_tags(model_output['current_state']['memory'])])

                if "action" in model_output:
                    actions = []
                    for action_item in model_output["action"]:
                        for action_type, action_details in action_item.items():
                            if action_type == "go_to_url":
                                actions.append(f"Go to URL: {strip_tags(action_details['url'])}")
                            elif action_type == "input_text":
                                actions.append(f"Input Text (Index {action_details['index']}): {strip_tags(action_details['text'])}")
                            elif action_type == "click_element":
                                actions.append(f"Click Element (Index {action_details['index']})")
                            elif action_type == "extract_content":
                                actions.append(f"Extract Content: {strip_tags(action_details['goal'])}")
                            elif action_type == "wait":
                                actions.append(f"Wait: {action_details['seconds']} seconds")
                            elif action_type == "done":
                                actions.append(f"Done: {strip_tags(json.dumps(action_details, indent=2))}")
                    table_data.append(["Actions", "<br/>".join([strip_tags(action) for action in actions])])

            # Result
            if result:
                table_data.append([Paragraph("<b>Result</b>", styles['Normal']), ""])
                for result_item in result:
                    content = strip_tags(result_item['extracted_content'])
                    if len(content) > 500:  # Adjust chunk size as needed
                        chunks = [content[i:i + 500] for i in range(0, len(content), 500)]
                        for chunk in chunks:
                            table_data.append(["", Paragraph(chunk, styles['Normal'])])
                    else:
                        table_data.append(["", Paragraph(content, styles['Normal'])])

            # State
            if state:
                table_data.append([Paragraph("<b>State</b>", styles['Normal']), ""])
                table_data.append(["URL", strip_tags(state['url'])])
                table_data.append(["Title", strip_tags(state['title'])])

                if state["interacted_element"]:
                    elements = []
                    for element in state["interacted_element"]:
                        if element:
                            elements.append(f"Tag Name: {strip_tags(element['tag_name'])}")
                            elements.append(f"XPath: {strip_tags(element['xpath'])}")
                            if 'attributes' in element:
                                elements.append(f"Attributes: {strip_tags(json.dumps(element['attributes'], indent=2))}")
                    table_data.append(["Interacted Elements", "<br/>".join([strip_tags(el) for el in elements])])

            # Metadata
            table_data.append([Paragraph("<b>Metadata</b>", styles['Normal']), ""])
            table_data.append(["Step Start Time", metadata['step_start_time']])
            table_data.append(["Step End Time", metadata['step_end_time']])
            table_data.append(["Input Tokens", metadata['input_tokens']])

            # Create Table with adjusted style for text wrapping
            col_widths = [150, doc.width - 150]  # Adjust the first column width as needed
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'), # Align text to the top of the cell
            ]))
            story.append(table)
            story.append(Spacer(1, 24))

        doc.build(story)
        print(f"PDF generated successfully: {pdf_filename}")