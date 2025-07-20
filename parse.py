import ollama # Direct Ollama client library
import os

# Define the Ollama model to use
# Ensure this model is pulled (e.g., ollama pull llama3) and running in your Ollama server
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', "llama3.2:1b") # Default model, adjust as needed

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_ollama(dom_chunks, parse_description):
    """
    Parses chunks of DOM content using an Ollama language model.
    """
    parsed_results = []

    if not dom_chunks:
        return ""

    for i, chunk in enumerate(dom_chunks, start = 1):
        # Construct the prompt for the Ollama model
        prompt_content = template.format(dom_content=chunk, parse_description=parse_description)

        try:
            # Make a direct call to the Ollama chat API
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[{'role': 'user', 'content': prompt_content}],
                options={'temperature': 0.1} # Lower temperature for more factual extraction
            )
            # Extract the content from the response
            extracted_text = response['message']['content'].strip()
            parsed_results.append(extracted_text)
            print(f"Parsed batch {i} of {len(dom_chunks)}")

        except Exception as e:
            print(f"Error parsing batch {i} with Ollama: {e}")
            parsed_results.append("") # Append empty string on error to maintain structure

    return "\n".join(parsed_results)
