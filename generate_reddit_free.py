import os
import random
import glob
import json
import time
import sys
from dotenv import load_dotenv

try:
    import g4f
    import praw
except ImportError:
    print("\033[31m>\033[0m \033[1mMissing dependencies! Run 'pip install praw g4f python-dotenv' first.\033[0m")
    sys.exit(1)

# Ensure ANSI escape sequences work on Windows CMD
os.system('')

# Load Credentials
load_dotenv()
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

if not all([CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD]):
    print("\033[31m>\033[0m \033[1mError: Missing Reddit API Credentials in .env file.\033[0m")
    sys.exit(1)

KNOWLEDGE_DIR = r"D:\workk\OUTPUT\OG OUTPUT\new style\Carson Clients\Project 6\Veronix Content"
DOCUMENTATION_DIR = r"d:\workk\OUTPUT\COMPRESSED OUTPUT\FINAL WEB\documentation"

def get_random_content():
    """Randomly chooses between a raw knowledge file or a generated SEO article."""
    choice = random.choice(["raw", "seo"])
    
    if choice == "raw":
        files = glob.glob(os.path.join(KNOWLEDGE_DIR, "**", "*.*"), recursive=True)
        valid_files = [f for f in files if f.endswith('.txt') or f.endswith('.md')]
        
        if not valid_files:
            print("\033[33m>\033[0m \033[1mNo text files found in Veronix Content. Falling back to SEO articles.\033[0m")
            choice = "seo"
        else:
            file_path = random.choice(valid_files)
            print(f"\033[36m>\033[0m \033[1mSource:\033[0m Raw Knowledge ({os.path.basename(file_path)})")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if len(content) > 3000:
                    start = random.randint(0, len(content) - 3000)
                    content = content[start:start+3000]
            return f"RAW KNOWLEDGE:\n{content}"
            
    if choice == "seo":
        files = glob.glob(os.path.join(DOCUMENTATION_DIR, "*.html"))
        if not files:
            print("\033[31m>\033[0m \033[1mNo SEO articles found!\033[0m")
            sys.exit(1)
            
        file_path = random.choice(files)
        print(f"\033[36m>\033[0m \033[1mSource:\033[0m SEO Repurposing ({os.path.basename(file_path)})")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract just the body text to save tokens
            try:
                content = content.split("<body>")[1].split("</body>")[0]
            except:
                pass
        return f"SEO ARTICLE TO REPURPOSE:\n{content}"

def generate_reddit_post(source_content):
    prompt = f"""
    You are the founder of a high-end short-form video editing agency called "Veronix Co".
    Your goal is to write a highly engaging, casual, value-driven Reddit post based on the following context.
    
    --- CONTEXT ---
    {source_content}
    ----------------
    
    Requirements:
    1. Write in the first person ("I", "my agency", "we").
    2. Provide pure, actionable value to the reader (video editing tips, retention hacks, creator advice, etc).
    3. Do NOT sound like a corporate robot or AI. Sound like a real guy sharing behind-the-scenes secrets.
    4. At the very end of the post, casually drop a backlink to your website (e.g., "If you want to see our work, check out veronix.me").
    5. Formatting: Use bold text, bullet points, and short paragraphs.
    6. Output strictly as a JSON object with two keys: "title" (a catchy Reddit title) and "body" (the markdown body of the post).
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": prompt}]
            )
            
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
                
            return json.loads(cleaned_response.strip())
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"\033[33m>\033[0m \033[1mAI Rate Limit. Retrying in 10s... ({attempt+1}/{max_retries})\033[0m")
                time.sleep(10)
            else:
                print(f"\n\033[31mError fetching from AI network: {e}\033[0m")
                sys.exit(1)

def post_to_reddit(post_data):
    try:
        print(f"\033[34m>\033[0m Authenticating with Reddit API as {USERNAME}...")
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username=USERNAME,
            password=PASSWORD,
            user_agent=f"windows:VeronixBot:v1.0 (by u/{USERNAME})"
        )
        
        # Verify authentication
        user = reddit.user.me()
        if not user:
            print("\033[31m>\033[0m \033[1mAuthentication failed. Check your .env credentials.\033[0m")
            sys.exit(1)
            
        print(f"\033[32m>\033[0m Successfully logged in as u/{user.name}")
        print(f"\033[34m>\033[0m Submitting post to your profile (u_{user.name})...")
        
        # Post directly to the user's profile
        subreddit = reddit.subreddit(f"u_{user.name}")
        submission = subreddit.submit(title=post_data['title'], selftext=post_data['body'])
        
        print(f"\n\033[32m>\033[0m \033[1mSuccess! Post is live.\033[0m")
        print(f"\033[36m>\033[0m URL: {submission.url}\n")
        
    except Exception as e:
        print(f"\n\033[31m>\033[0m \033[1mFailed to post to Reddit: {e}\033[0m")

if __name__ == "__main__":
    print(f"\n\033[35m>\033[0m \033[1mStarting Veronix Reddit Engine\033[0m")
    
    source_content = get_random_content()
    
    print(f"\033[34m>\033[0m Generating high-value Reddit post...")
    post_data = generate_reddit_post(source_content)
    
    print(f"\033[35m>\033[0m \033[1mGenerated Title:\033[0m {post_data['title']}")
    
    post_to_reddit(post_data)
