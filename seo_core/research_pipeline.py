import glob
import os
import random
import json

def get_raw_knowledge(knowledge_dir):
    allowed_folders = [
        "Editing Knowledge", 
        "High Ticket Sales",
        "Raw Viral Scripts",
        "Scripting Resources",
        "Viral Content Knowledge",
        "Viral Videos Knowledge From Youtube"
    ]
    
    valid_files = []
    for folder in allowed_folders:
        folder_path = os.path.join(knowledge_dir, folder)
        if os.path.exists(folder_path):
            search_pattern = os.path.join(folder_path, "**", "*.*")
            for f in glob.glob(search_pattern, recursive=True):
                if f.endswith('.txt') or f.endswith('.md'):
                    valid_files.append(f)
                    
    if not valid_files:
        return None
        
    file_path = random.choice(valid_files)
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if len(content) > 3000:
                start = random.randint(0, len(content) - 3000)
                chunk = content[start:start+3000]
            else:
                chunk = content
            return {"source_file": os.path.basename(file_path), "text": chunk}
    except Exception:
        return None

def verify_claims_and_extract(ai_provider, raw_knowledge):
    prompt = f"""
    You are Veronix Co's Lead Fact Checker.
    Extract the core useful insights from this raw transcription to form a Verified Knowledge Context.
    
    RAW TRANSCRIPT:
    {raw_knowledge['text']}
    
    CRITICAL RULE - BAN ON FAKE NUMBERS:
    You must NEVER extract or invent fake numerical performance claims (e.g., "70% increase", "10x faster", "sub-1 second").
    Only extract actual workflows, techniques, concepts, and advice.
    
    Summarize the raw transcript into 3-5 highly actionable bullet points that a writer can use to write an article.
    
    Output strictly as a JSON object with:
    - "verified_context": string (The summary of actionable insights, NO fake numbers allowed).
    - "suggested_topic": string (A broad, non-clickbait topic based on this context).
    """
    
    try:
        response = ai_provider.generate(prompt)
        data = json.loads(response)
        data["source_file"] = raw_knowledge["source_file"]
        return data
    except Exception as e:
        return None
