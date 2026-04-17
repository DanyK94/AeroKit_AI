from clients.openai_client import getResponseFromAI
from models.acronym_data import AcronymData
from dao.cacheAcronym_dao import saveAcronymExplanationToCache, getAcronymExplanationFromCache
import re # Regular expression module for parsing the response text



def getAcronymExplanation(acronym):

    cached = getAcronymExplanationFromCache(acronym)
    if cached:
        return parseResponse(acronym,cached)
    
    prompt = f"""You are an aviation expert. Explain the acronym {acronym}.
    Format your response EXACTLY as follows:
    #0 Full form (e.g. MEL - Minimum Equipment List)
    #1 Definition
    #2 Context in aviation
    #3 Usage Example
    #4 Importance
    #5 Related Acronyms (comma-separated with full forms)
    If not an aviation acronym respond ONLY with: NOT AVIATION"""

    response = getResponseFromAI(prompt)
    if response:
        saveAcronymExplanationToCache(acronym,response)
        explanation = parseResponse(acronym, response)
        return explanation
    return None

def parseResponse(acronym, response):
    if not response:
        return None  
    
    raw_text = response
    #split text by [num] pattern
    if raw_text.strip() == "NOT AVIATION":
        return None
    sections = re.split(r'#\d+', raw_text)

    return AcronymData(
        acronym=sections[1] if len(sections) > 1 else acronym, 
        definition=sections[2] if len(sections) > 2 else "",
        context=sections[3] if len(sections) > 3 else "",
        example=sections[4] if len(sections) > 4 else "",
        importance=sections[5] if len(sections) > 5 else "",
        related=sections[6].split(',') if len(sections) > 6 else []
    )
