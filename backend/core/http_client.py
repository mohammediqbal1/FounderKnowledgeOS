import time
import requests


def call_gemini_with_retry(url, payload, max_retries=5, initial_delay=5):
    """
    Call Gemini API with robust exponential backoff retry logic.
    Handles 429 (Rate Limit) and 5xx (Server Error) with retries.
    """
    delay = initial_delay
    last_error = None
    
    for i in range(max_retries):
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=120,
            )
            
            # Case 1: Success
            if response.status_code == 200:
                return response.json()
                
            # Case 2: Rate Limit (429) or Server Error (5xx)
            if response.status_code == 429 or (500 <= response.status_code <= 599):
                error_msg = f"Status {response.status_code}"
                try:
                    error_json = response.json()
                    if 'error' in error_json:
                        error_msg = error_json['error'].get('message', error_msg)
                except:
                    pass
                    
                print(f"[Gemini] {error_msg}. Retrying in {delay}s... (Attempt {i+1}/{max_retries})")
                time.sleep(delay)
                delay *= 2
                last_error = error_msg
                continue
            
            # Case 3: Other errors (400, 401, 403, 404) - Do NOT retry
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if i == max_retries - 1:
                break
            print(f"[Gemini] Request error: {last_error}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2
            
    raise Exception(f"Gemini API call failed after {max_retries} attempts. Last error: {last_error}")
