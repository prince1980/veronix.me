import os
import json
import urllib.request
import re
import datetime

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DOCUMENTATION_DIR = "documentation"
INDEX_FILE = os.path.join(DOCUMENTATION_DIR, "index.html")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit(1)

def get_ai_article():
    """Calls OpenAI API to generate a new SEO article."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    prompt = """
    You are an expert SEO content writer for a high-end short-form video editing agency called "Veronix Co".
    Write a new, highly-targeted AEO-optimized article about a specific niche (e.g., "Real Estate Video Editing", "SaaS Video Marketing", "VFX for Creators", "Podcast clip editing").
    
    Requirements for the output:
    1. A catchy title (string).
    2. A short URL slug (e.g., "real-estate-reels-agency").
    3. A brief description (1-2 sentences for the index card).
    4. The full HTML body content (do not include <html>, <head>, or <body> tags. Just the internal <article> content).
    
    The HTML content MUST include:
    - <h1> with the title
    - <h2> and <h3> tags formatted as questions (for Answer Engine Optimization)
    - At least one <table> comparing something (e.g. costs, software, freelance vs agency)
    - A brief JSON-LD FAQ schema inside a <script type="application/ld+json"> tag (put this at the top of the article content)
    - Engaging paragraphs and bulleted lists.
    
    Output strictly as a JSON object with keys: "title", "slug", "description", "html_content".
    """
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a JSON-generating SEO agent."},
            {"role": "user", "content": prompt}
        ],
        "response_format": { "type": "json_object" },
        "temperature": 0.7
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
    except Exception as e:
        print(f"Failed to generate article from API: {e}")
        exit(1)

def create_html_file(article):
    """Wraps the AI-generated content in the Veronix HTML template and saves it."""
    slug = article["slug"].lower().replace(" ", "-")
    filepath = os.path.join(DOCUMENTATION_DIR, f"{slug}.html")
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} | Veronix Co</title>
    <meta name="description" content="{article['description']}">
    <meta property="og:title" content="{article['title']}" />
    <meta property="og:description" content="{article['description']}" />
    <meta property="og:type" content="article" />
    
    <link rel="shortcut icon" href="../logo.png" type="image/png" />
    <link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --veronix-bg: #0d0b09;
            --veronix-surface: #1a1a1a;
            --veronix-text: #f3efe8;
            --veronix-muted: rgba(243, 239, 232, 0.7);
            --veronix-gold: #c5a358;
            --veronix-stroke: rgba(255, 255, 255, 0.1);
        }}

        body {{
            background-color: var(--veronix-bg);
            color: var(--veronix-text);
            font-family: 'Albert Sans', sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.7;
        }}

        .container {{
            max-width: 760px;
            margin: 0 auto;
            padding: 80px 20px;
        }}

        .nav {{
            margin-bottom: 50px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .logo {{
            width: 40px;
            height: auto;
        }}

        .nav-link {{
            color: var(--veronix-muted);
            text-decoration: none;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: color 0.2s;
        }}

        .nav-link:hover {{
            color: var(--veronix-gold);
        }}

        h1 {{
            font-size: 46px;
            font-weight: 800;
            margin-bottom: 20px;
            line-height: 1.1;
            letter-spacing: -1px;
        }}

        h2 {{
            font-size: 28px;
            font-weight: 700;
            margin-top: 50px;
            margin-bottom: 20px;
            color: var(--veronix-gold);
        }}

        h3 {{
            font-size: 22px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        p {{
            margin-bottom: 20px;
            font-size: 18px;
            color: var(--veronix-muted);
        }}

        ul, ol {{
            margin-bottom: 30px;
            padding-left: 20px;
        }}

        li {{
            margin-bottom: 10px;
            font-size: 18px;
            color: var(--veronix-muted);
        }}

        strong {{
            color: var(--veronix-text);
        }}

        .table-wrapper {{
            overflow-x: auto;
            margin: 40px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th, td {{
            padding: 15px;
            border: 1px solid var(--veronix-stroke);
        }}

        th {{
            background-color: var(--veronix-surface);
            font-weight: 700;
            color: var(--veronix-gold);
        }}

        .cta {{
            margin-top: 60px;
            padding: 40px;
            background: var(--veronix-surface);
            border-radius: 12px;
            border: 1px solid var(--veronix-gold);
            text-align: center;
        }}

        .cta h3 {{
            margin-top: 0;
            color: var(--veronix-gold);
        }}

        .btn {{
            display: inline-block;
            background-color: var(--veronix-gold);
            color: #000;
            padding: 15px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 700;
            margin-top: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav">
            <a href="/"><img src="../logo.png" alt="Veronix Logo" class="logo"></a>
            <a href="/documentation" class="nav-link">← Documentation</a>
        </nav>

        <article>
            {article['html_content']}
            
            <div class="cta">
                <h3>Ready to elevate your short-form content?</h3>
                <p>Veronix Co is a premium video editing studio specializing in high-fidelity retention editing for global creators.</p>
                <a href="/" class="btn">View Our Portfolio</a>
            </div>
        </article>
    </div>
</body>
</html>"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"Created article: {filepath}")
    return slug

def update_index_file(article, slug):
    """Inserts the new article card into documentation/index.html"""
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_card = f"""<ul class="resource-list">
                <li class="resource-card">
                    <a href="/documentation/{slug}">
                        <h2 class="resource-title">{article['title']}</h2>
                        <p class="resource-desc">{article['description']}</p>
                    </a>
                </li>"""
    
    updated_content = content.replace('<ul class="resource-list">', new_card, 1)
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print("Updated index.html")

if __name__ == "__main__":
    print(f"Running SEO Generation Script at {datetime.datetime.now()}")
    article_data = get_ai_article()
    print(f"Successfully generated article data for: {article_data.get('title')}")
    
    slug = create_html_file(article_data)
    update_index_file(article_data, slug)
    print("SEO Automation Complete.")
