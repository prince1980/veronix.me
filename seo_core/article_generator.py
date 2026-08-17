import json

def completeness_check(ai_provider, html_content):
    if not html_content or len(html_content.split()) < 200:
        return False
        
    prompt = f"""
    You are an editorial auditor. Check if this article draft was cut off or truncated.
    
    ARTICLE ENDING:
    {html_content[-1500:] if len(html_content) > 1500 else html_content}
    
    Check for:
    1. Ends abruptly mid-sentence or mid-word.
    2. Missing a proper conclusion.
    3. Unclosed HTML tags.
    
    Output ONLY "true" if the article finishes naturally, or ONLY "false" if it was truncated. No other text.
    """
    
    max_retries = 3
    for _ in range(max_retries):
        try:
            response = ai_provider.generate(prompt, is_json=False).strip().lower()
            return "true" in response
        except Exception:
            continue
            
    # Fallback to simple heuristic if AI completely fails
    return not (html_content.rstrip().endswith(",") or html_content.rstrip().endswith("and") or html_content.rstrip().endswith("the"))

def generate_draft(ai_provider, verified_context, approved_topic):
    prompt = f"""
    You are the Senior Editorial Writer for Veronix Co, a premium short-form video editing and VFX studio.
    Write an in-depth, authoritative, and helpful article based purely on this verified knowledge:
    
    TOPIC: {approved_topic}
    VERIFIED KNOWLEDGE: {verified_context}
    
    WRITING GUIDELINES:
    1. Write for humans first. Answer WHO this is for, WHAT problem it solves, WHY it matters, and HOW to apply it.
    2. VOICE: Premium, technical, confident, specific. No corporate filler. Do NOT use fake statistics ("10x", "70%").
    3. Do NOT use repetitive phrasing like "Veronix Co's Secret to...".
    4. Provide clear structure: Introduction, detailed sections with H2s/H3s, practical examples, and a conclusion.
    5. CRITICAL: Provide the complete article. DO NOT cut off mid-sentence. Keep it concise enough to fit within output limits if necessary, but FINISH your thoughts.
    6. BAN ON RAW CODE: This is a business/marketing blog for creators and founders, not a developer wiki. DO NOT include any raw code blocks, terminal commands, or JSON configuration.
    
    Output strictly as a JSON object with:
    - "title": string (Specific, descriptive, non-clickbait)
    - "body_html": string (The HTML content of the article WITHOUT <html> or <body> tags. Just the internal headings, paragraphs, lists, etc).
    """
    
    max_draft_retries = 3
    best_draft = None
    
    for attempt in range(max_draft_retries):
        try:
            print(f"\033[36m>\033[0m Drafting article (Attempt {attempt+1}/{max_draft_retries})...")
            response = ai_provider.generate(prompt)
            draft_data = json.loads(response)
            
            best_draft = draft_data # Save the latest one just in case
            
            # Check completeness
            if completeness_check(ai_provider, draft_data.get('body_html', '')):
                return draft_data
            else:
                print(f"\033[33m>\033[0m Draft was truncated mid-sentence. Retrying...")
                
        except Exception as e:
            failure_class = getattr(e, "failure_class", "GENERATION_FAILED")
            print(f"\033[31m>\033[0m [{failure_class}] Draft generation error: {e}")
            
    # If we exhaust retries, return the last one (it will likely fail the quality gate, which is fine)
    print(f"\033[31m>\033[0m \033[1mWarning: Could not generate a complete draft after {max_draft_retries} attempts. Proceeding with best attempt.\033[0m")
    return best_draft

def quality_gate_check(ai_provider, draft_data):
    prompt = f"""
    You are the Editor-in-Chief at Veronix Co.
    Audit this drafted article.
    
    TITLE: {draft_data['title']}
    BODY: {draft_data['body_html'][:1500]}... (truncated for review)
    
    Score this draft out of 100 based on:
    - Search intent match (0-10)
    - Originality (0-15)
    - First-hand expertise (0-15)
    - Factual accuracy / No fake numbers (0-15)
    - Topic relevance to Veronix (0-10)
    - Readability / Human-first voice (0-10)
    
    If the total score is below 85, we will reject it.
    
    Output strictly as a JSON object:
    - "total_score": integer (0-100)
    - "feedback": string (Why it got this score)
    - "passed": boolean (true if total_score >= 85, else false)
    """
    
    try:
        response = ai_provider.generate(prompt)
        return json.loads(response)
    except Exception as e:
        failure_class = getattr(e, "failure_class", "QUALITY_CHECK_FAILED")
        return {"total_score": None, "feedback": f"[{failure_class}] Error: {e}", "passed": False, "status": failure_class}

def revise_draft(ai_provider, draft_data, feedback):
    prompt = f"""
    You are the Senior Editorial Writer for Veronix Co.
    Your previous article draft was rejected by the Editor-in-Chief.
    
    ORIGINAL TITLE: {draft_data.get('title')}
    ORIGINAL BODY: {draft_data.get('body_html')}
    
    EDITOR FEEDBACK (Why it failed):
    {feedback}
    
    Please REVISE the article completely to address this feedback. Improve the depth, originality, formatting, and alignment with the feedback provided.
    
    Output strictly as a JSON object with:
    - "title": string (Revised title, if necessary)
    - "body_html": string (The REVISED HTML content of the article)
    """
    
    try:
        response = ai_provider.generate(prompt)
        revised_data = json.loads(response)
        
        # Check completeness on revision too
        if completeness_check(ai_provider, revised_data.get('body_html', '')):
            return revised_data
        else:
            print(f"\033[33m>\033[0m Revised draft was truncated. Returning original draft.")
            return draft_data
    except Exception as e:
        failure_class = getattr(e, "failure_class", "GENERATION_FAILED")
        print(f"\033[31m>\033[0m [{failure_class}] Revision generation error: {e}")
        return draft_data
