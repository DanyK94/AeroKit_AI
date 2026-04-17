from clients.openai_client import getResponseFromOpenAI
from models.acronym_data import AcronymData
import re # Regular expression module for parsing the response text


def getAcronymExplanation(acronym):
    prompt = f"""[TASK 1] Check if {acronym} is a valid aviation acronym, if it not return the ONLY TEXT: "NOT AVIATION" without any additional information or explanations. If it is a valid aviation acronym, return the ONLY TEXT: "VALID ACRONYM" without any additional information or explanations.
    If it is, [TASK 2] give me a detailed explanation of the aviation acronym {acronym}
    following this pattern: 
    #0 *The acronym itself with long form (e.g. MEL - Minimum Equipment List).*
    #1 *A concise definition of the acronym.*
    #2 *A brief explanation of the context in which the acronym is commonly used in aviation.*
    #3 *An example of how the acronym is used in a sentence or aviation communication.*
    #4 *A brief explanation of why understanding this acronym is important for aviation professionals.*
    #5 *A list of any related acronyms, with between parentheses the long form, that are commonly associated with the given acronym in aviation (e.g: CDL (Configuration Deviation List), MMEL (Master Minimum Equipment List)).*
    DON'T include any additional information or explanations beyond these five sections neither ask questions.
    DON'T write in the response the prompt or any instructions in the response, that means that what are indicated between asterisks should not be included in the response as a text.
    DON'T include a response for the TASK 1 if the acronym is valid, and don't include a response for the TASK 2 if the acronym is not valid, that means that if the acronym is valid the response should only include the sections from TASK 2 without any mention to TASK 1, and if the acronym is not valid the response should only include the text "NOT AVIATION" without any mention to TASK 2.
    It's MANDATORY to respect the number designation, with #num, for each section and to provide the information in the exact order as specified."""
    
    response = getResponseFromOpenAI(prompt)
    explanation = parseResponse(acronym, response)
    return explanation

def parseResponse(acronym, response):
    if hasattr(response, 'output_text'):    # Check if the response has the expected attribute containing the text output
        rawText = response.output_text      # Get the raw text response from the API
    else:
        return None
    
    #split text by [num] pattern
    if rawText.strip() == "NOT AVIATION":
        return None
    sections = re.split(r'#\d+', rawText)

    return AcronymData(
        acronym=sections[1] if len(sections) > 1 else acronym, 
        definition=sections[2] if len(sections) > 2 else "",
        context=sections[3] if len(sections) > 3 else "",
        example=sections[4] if len(sections) > 4 else "",
        importance=sections[5] if len(sections) > 5 else "",
        related=sections[6].split(',') if len(sections) > 6 else []
    )
