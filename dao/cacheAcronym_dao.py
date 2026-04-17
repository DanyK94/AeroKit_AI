import json, time


CACHE_FILE = "cache/acronyms.json"
TTL = 60*60*24*7  # Time-to-live for cache entries (e.g., 7 days in seconds)

def saveAcronymExplanationToCache(acronym, explanation):
    entry = {
        "response": explanation,
        "timestamp": time.time()
    }
    #1. Read
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as file: #r = read mode because we want to read the existing cache file first to avoid overwriting it
            cache = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        cache = {}  # If the file doesn't exist or is empty, start with an empty cache

    #2. Update
    cache[acronym] = entry 

    #3. Write
    with open(CACHE_FILE, 'w', encoding='utf-8') as file:
        json.dump(cache, file)
    
    

def getAcronymExplanationFromCache(acronym):
    acronym = acronym.strip().upper()  # Normalize the acronym for consistent caching
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as file:
            cache = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None  # If the file doesn't exist or is empty, return None
    
    entry = cache.get(acronym)
    if not entry:
        return None  # Acronym not found in cache
    elif time.time() - entry.get('timestamp', 0) > TTL:  # Check if the cache entry is older than the TTL
        del cache[acronym]  # Remove stale entry from cache
        with open(CACHE_FILE, 'w', encoding='utf-8') as file:
            json.dump(cache, file)  # Update the cache file after removing the stale entry
        return None  # Return None for stale entries
    return entry.get('response') 