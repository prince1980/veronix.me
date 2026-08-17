import json
import glob
import os
import re

AUTHORIZED_CLUSTERS = [
    "Short-Form Editing",
    "SaaS Video",
    "Real Estate Video",
    "VFX / Motion Design",
    "Creator Systems"
]

def get_existing_article_titles(docs_dir):
    titles = []
    for filepath in glob.glob(os.path.join(docs_dir, "*.html")):
        if "index.html" in filepath:
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'<title>(.*?) \|', content)
            if match:
                titles.append(match.group(1).strip())
        except Exception:
            pass
    return titles

def evaluate_topic(ai_provider, proposed_topic, existing_titles):
    prompt = f"""
    You are the Chief Content Strategist for Veronix Co, a premium video editing and VFX agency.
    A new article topic has been proposed: "{proposed_topic}"
    
    We currently have these published articles:
    {json.dumps(existing_titles, indent=2)}
    
    AUTHORIZED TOPIC CLUSTERS:
    {json.dumps(AUTHORIZED_CLUSTERS, indent=2)}
    
    Evaluate this proposed topic based on three criteria:
    1. CLUSTER MATCH: Does it fit perfectly into one of the Authorized Topic Clusters?
    2. CANNIBALIZATION: Does this topic overlap in search intent with ANY of the existing articles? (If yes, reject it).
    3. VALUE: Is this topic genuinely useful for our target audience (creators, SaaS founders, real estate brokers)?
    
    Output strictly as a JSON object with keys:
    - "approved": boolean (true/false)
    - "reason": string (Explanation of why it was approved or rejected)
    - "cluster": string (The name of the authorized cluster it fits into, or null if none)
    """
    
    try:
        response = ai_provider.generate(prompt)
        return json.loads(response)
    except Exception as e:
        return {"approved": False, "reason": f"Evaluation failed: {e}", "cluster": None}
