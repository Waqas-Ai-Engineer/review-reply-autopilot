"""Optional: polish drafts through any OpenAI-compatible endpoint. Off unless env vars are set."""
import json, os, urllib.request

def polish(draft, business):
    key, base = os.environ.get("LLM_API_KEY"), os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    if not key:
        return draft
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": f"Rewrite this review reply for {business}. Warm, concise, no promises of refunds, no admissions of liability. Keep under 80 words."},
        {"role": "user", "content": draft}]}).encode()
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", body,
                                 {"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["choices"][0]["message"]["content"].strip()
    except Exception:
        return draft
