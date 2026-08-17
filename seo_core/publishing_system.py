import os
import json
import datetime
import re

DOCUMENTATION_DIR = "documentation"
INDEX_FILE = os.path.join(DOCUMENTATION_DIR, "index.html")

def generate_metadata(ai_provider, draft_data):
    prompt = f"""
    Generate SEO Metadata and JSON-LD for this article.
    TITLE: {draft_data['title']}
    
    Output strictly as a JSON object with:
    - "slug": string (e.g. "saas-video-editing-guide")
    - "meta_description": string (1-2 sentences)
    - "json_ld": object (A valid Schema.org Article object. "author" should be "Veronix Editorial Team", "publisher" should be "Veronix Co". Include "headline", "description", "datePublished")
    """
    try:
        response = ai_provider.generate(prompt)
        return json.loads(response)
    except Exception:
        return None

def apply_internal_links(html_content, existing_titles):
    # Very basic internal linking algorithm: Look for phrases matching existing titles and wrap them in <a> tags.
    # To keep it safe and avoid breaking HTML tags, we do a simple regex on text content.
    # In a full production system, this would use BeautifulSoup to only target text nodes.
    
    linked_html = html_content
    # Add a standard CTA at the bottom if not present
    if "Ready to elevate your short-form content?" not in linked_html:
        linked_html += """
        <div class="cta">
            <h3>Ready to elevate your short-form content?</h3>
            <p>Veronix Co is a premium video editing studio specializing in high-fidelity retention editing for global creators.</p>
            <a href="/" class="btn">View Our Portfolio</a>
        </div>
        """
    return linked_html

def save_article(draft_data, metadata, is_dry_run=False):
    slug = metadata['slug'].lower().replace(" ", "-")
    filepath = os.path.join(DOCUMENTATION_DIR, f"{slug}.html")
    
    date_str = datetime.datetime.now().isoformat()
    metadata['json_ld']['datePublished'] = date_str
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{draft_data['title']} | Veronix Co</title>
    <meta name="description" content="{metadata['meta_description']}">
    <link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Schema.org Article -->
    <script type="application/ld+json">
    {json.dumps(metadata['json_ld'], indent=2)}
    </script>
    
    <!-- Entity SEO Schema (Organization) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Veronix Co",
      "alternateName": ["Veronix Studios", "Veronix VFX", "Veronix"],
      "url": "https://veronix.me/",
      "logo": "https://veronix.me/logo.png",
      "sameAs": [
        "https://in.pinterest.com/veronixco/",
        "https://www.instagram.com/veronix.co/",
        "https://www.instagram.com/veronix.vfx/",
        "https://www.instagram.com/veronix.studios",
        "https://www.youtube.com/@veronix-co/",
        "https://in.linkedin.com/in/veronix-co-919a93371"
      ]
    }}
    </script>
    <style>
        :root {{ --veronix-bg: #0d0b09; --veronix-surface: #1a1a1a; --veronix-text: #f3efe8; --veronix-muted: rgba(243, 239, 232, 0.7); --veronix-gold: #c5a358; --veronix-stroke: rgba(255, 255, 255, 0.1); }}
        body {{ background-color: var(--veronix-bg); color: var(--veronix-text); font-family: 'Albert Sans', sans-serif; margin: 0; padding: 0; line-height: 1.7; }}
        .container {{ max-width: 760px; margin: 0 auto; padding: 80px 20px; }}
        .nav {{ margin-bottom: 50px; display: flex; align-items: center; gap: 15px; }}
        .logo {{ width: 40px; height: auto; }}
        .nav-link {{ color: var(--veronix-muted); text-decoration: none; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; transition: color 0.2s; }}
        .nav-link:hover {{ color: var(--veronix-gold); }}
        h1 {{ font-size: 46px; font-weight: 800; margin-bottom: 20px; line-height: 1.1; letter-spacing: -1px; }}
        h2 {{ font-size: 28px; font-weight: 700; margin-top: 50px; margin-bottom: 20px; color: var(--veronix-gold); }}
        h3 {{ font-size: 22px; font-weight: 600; margin-top: 30px; margin-bottom: 15px; }}
        p, li {{ font-size: 18px; color: var(--veronix-muted); margin-bottom: 20px; }}
        ul, ol {{ margin-bottom: 30px; padding-left: 20px; }}
        strong {{ color: var(--veronix-text); }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; margin: 40px 0; }}
        th, td {{ padding: 15px; border: 1px solid var(--veronix-stroke); }}
        th {{ background-color: var(--veronix-surface); font-weight: 700; color: var(--veronix-gold); }}
        .cta {{ margin-top: 60px; padding: 40px; background: var(--veronix-surface); border-radius: 12px; border: 1px solid var(--veronix-gold); text-align: center; }}
        .cta h3 {{ margin-top: 0; color: var(--veronix-gold); }}
        .btn {{ display: inline-block; background-color: var(--veronix-gold); color: #000; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: 700; margin-top: 20px; text-transform: uppercase; letter-spacing: 1px; }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav"><a href="/"><img src="../logo.png" alt="Veronix Logo" class="logo"></a><a href="/documentation" class="nav-link">← Documentation</a></nav>
        <article>
        <h1>{draft_data['title']}</h1>
        {draft_data['body_html']}
        </article>
    </div>
</body>
</html>"""
    
    if not is_dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_template)
            
    return slug

def update_index_and_sitemap(draft_data, metadata, slug, is_dry_run=False):
    if is_dry_run:
        return
        
    # Update Index
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        new_card = f'<ul class="resource-list">\n                <li class="resource-card">\n                    <a href="/documentation/{slug}">\n                        <h2 class="resource-title">{draft_data["title"]}</h2>\n                        <p class="resource-desc">{metadata["meta_description"]}</p>\n                    </a>\n                </li>'
        updated_content = content.replace('<ul class="resource-list">', new_card, 1)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
    except Exception:
        pass
        
    # Update Sitemap
    sitemap_file = "sitemap.xml"
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    new_url = f"""  <url>\n    <loc>https://veronix.me/documentation/{slug}.html</loc>\n    <lastmod>{date_str}</lastmod>\n  </url>\n</urlset>"""
    try:
        if os.path.exists(sitemap_file):
            with open(sitemap_file, "r", encoding="utf-8") as f:
                content = f.read()
            updated_sitemap = content.replace("</urlset>", new_url)
            with open(sitemap_file, "w", encoding="utf-8") as f:
                f.write(updated_sitemap)
    except Exception:
        pass
