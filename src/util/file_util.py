class FileUtil:
    
    @staticmethod
    def read_file_to_string(file_path):
        """ 
        Reads a file line by line and returns its content as a single string.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The content of the file as a single string.
        """
        result = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # Open file with UTF-8 encoding
                for line in file:
                    result += line  # Append each line to the result string
            return result
        except FileNotFoundError:
            return "Error: File not found."
        except Exception as e:
            return f"An error occurred: {e}"
    
    @staticmethod
    def extract_steps(feature_text):
        """
        Removes Gherkin keywords from the feature text and returns only the steps.

        Args:
            feature_text (str): The full Gherkin-style feature description.

        Returns:
            str: The steps without the Gherkin keywords.
        """
        gherkin_keywords = ["GIVEN", "WHEN", "AND", "THEN","Feature:"]
        result = []
        
        # Split the text into lines and process each line
        for line in feature_text.split("\n"):
            stripped_line = line.strip()
            if stripped_line:  # Ignore empty lines
                # Remove the keyword if the line starts with one
                for keyword in gherkin_keywords:
                    if stripped_line.startswith(keyword):
                        stripped_line = stripped_line.replace(keyword, "").strip() +"."
                        break  # Remove only the first keyword, if found
                result.append(stripped_line)
        
        return "\n".join(result)
