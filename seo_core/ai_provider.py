import time
import sys
import random
import json

try:
    import g4f
except ImportError:
    print("\033[31m>\033[0m \033[1mMissing dependencies! Run 'pip install g4f'.\033[0m")
    sys.exit(1)

class AIProviderException(Exception):
    def __init__(self, message, failure_class="PROVIDER_UNAVAILABLE"):
        super().__init__(message)
        self.failure_class = failure_class

class AIProvider:
    def __init__(self, max_retries=5):
        self.max_retries = max_retries

    def generate(self, prompt, is_json=True):
        import os
        import json
        import random
        import time
        
        openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        
        # 1. Native OpenRouter API Integration (Bypass g4f entirely for ultimate stability)
        if openrouter_key:
            import urllib.request
            import urllib.error
            
            for attempt in range(self.max_retries):
                try:
                    url = "https://openrouter.ai/api/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {openrouter_key}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": "openrouter/free",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers)
                    
                    with urllib.request.urlopen(req) as response:
                        result = json.loads(response.read().decode())
                        cleaned = result['choices'][0]['message']['content'].strip()
                        
                        if is_json:
                            if cleaned.startswith("```json"):
                                cleaned = cleaned[7:]
                            elif cleaned.startswith("```"):
                                cleaned = cleaned[3:]
                            if cleaned.endswith("```"):
                                cleaned = cleaned[:-3]
                            cleaned = cleaned.strip()
                            
                            try:
                                json.loads(cleaned)
                            except json.JSONDecodeError as e:
                                raise AIProviderException(f"Invalid JSON returned: {e}. Output: {cleaned[:100]}...", "PARSING_FAILED")
                        
                        return cleaned
                        
                except AIProviderException as e:
                    if attempt < self.max_retries - 1:
                        sleep_time = (2 ** attempt) + random.uniform(0, 2)
                        print(f"\033[33m>\033[0m \033[1m[{e.failure_class}] JSON was malformed. Retrying in {sleep_time:.1f}s... ({attempt+1}/{self.max_retries})\033[0m")
                        time.sleep(sleep_time)
                    else:
                        raise e
                except urllib.error.URLError as e:
                    if attempt < self.max_retries - 1:
                        sleep_time = (2 ** attempt) + random.uniform(1, 3)
                        print(f"\033[33m>\033[0m \033[1m[PROVIDER_UNAVAILABLE] OpenRouter API Error: {e}. Backing off for {sleep_time:.1f}s... ({attempt+1}/{self.max_retries})\033[0m")
                        time.sleep(sleep_time)
                    else:
                        raise AIProviderException(f"OpenRouter API failed: {e}", "PROVIDER_UNAVAILABLE")
                except Exception as e:
                    raise AIProviderException(f"Unexpected OpenRouter error: {e}", "PROVIDER_UNAVAILABLE")

        # 2. Legacy g4f Fallback
        api_key = os.environ.get("OPENAI_API_KEY")
        groq_key = os.environ.get("GROQ_API_KEY")
        
        active_provider = None
        model_name = g4f.models.gpt_4
        kwargs = {}
        
        try:
            if api_key:
                from g4f.Provider import OpenaiAPI
                active_provider = OpenaiAPI
                model_name = "gpt-4o"
                kwargs = {"api_key": api_key}
            elif groq_key:
                from g4f.Provider import Groq
                active_provider = Groq
                model_name = "llama3-70b-8192"
                kwargs = {"api_key": groq_key}
            else:
                active_provider = None
                model_name = g4f.models.gpt_35_turbo
        except ImportError:
            active_provider = None
            
        for attempt in range(self.max_retries):
            try:
                response = g4f.ChatCompletion.create(
                    model=model_name,
                    provider=active_provider,
                    messages=[{"role": "user", "content": prompt}],
                    **kwargs
                )
                
                if not response:
                    raise AIProviderException("Empty response returned from AI provider.", "PROVIDER_UNAVAILABLE")
                    
                cleaned = response.strip()
                if not cleaned:
                    raise AIProviderException("Empty response returned from AI provider.", "PROVIDER_UNAVAILABLE")
                    
                if is_json:
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]
                    elif cleaned.startswith("```"):
                        cleaned = cleaned[3:]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                    cleaned = cleaned.strip()
                    
                    if not cleaned:
                        raise AIProviderException("Response was empty after stripping markdown.", "PROVIDER_UNAVAILABLE")
                        
                    try:
                        json.loads(cleaned)
                    except json.JSONDecodeError as e:
                        raise AIProviderException(f"Invalid JSON returned: {e}. Output: {cleaned[:100]}...", "PARSING_FAILED")
                
                return cleaned
                
            except AIProviderException as e:
                if attempt < self.max_retries - 1:
                    sleep_time = (2 ** attempt) + random.uniform(0, 2)
                    print(f"\033[33m>\033[0m \033[1m[{e.failure_class}] JSON was malformed. Retrying in {sleep_time:.1f}s... ({attempt+1}/{self.max_retries})\033[0m")
                    time.sleep(sleep_time)
                else:
                    raise e
                    
            except Exception as e:
                error_str = str(e)
                failure_class = "PROVIDER_UNAVAILABLE"
                if "RateLimitError" in error_str or "429" in error_str or "504" in error_str:
                    failure_class = "RATE_LIMITED"
                elif "NoValidHarFileError" in error_str or "CopilotApp" in error_str:
                    failure_class = "PROVIDER_UNAVAILABLE"
                    
                if attempt < self.max_retries - 1:
                    sleep_time = (2 ** attempt) + random.uniform(1, 3)
                    print(f"\033[33m>\033[0m \033[1m[{failure_class}] Network/Provider Error. Backing off for {sleep_time:.1f}s... ({attempt+1}/{self.max_retries})\033[0m")
                    time.sleep(sleep_time)
                else:
                    raise AIProviderException(f"Failed to communicate with AI provider: {e}", failure_class)
