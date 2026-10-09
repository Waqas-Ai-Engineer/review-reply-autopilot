"""Core logic: classify a review, then draft a reply. Pure standard library."""
import re

NEG = {"terrible","awful","worst","rude","late","never","refund","scam","dirty","broken","leak","leaking",
       "ignored","unprofessional","overpriced","disappointed","poor","bad","waste","no show","no-show",
       "damaged","horrible","cancelled","waiting","wait","unresponsive","mess"}
POS = {"great","excellent","amazing","friendly","professional","fast","clean","recommend","love","perfect",
       "helpful","best","on time","on-time","fair","quick","thank","thanks","happy","wonderful","reliable"}
RISK = {
    "legal": ["lawyer","attorney","sue","lawsuit","legal action","court"],
    "regulator": ["bbb","attorney general","report you","health department","licensing board"],
    "safety": ["injury","injured","unsafe","fire","gas leak","mold","hospital","danger"],
    "fraud": ["scam","fraud","stole","stolen","ripped off","overcharged"],
    "privacy": ["my data","privacy","medical record","hipaa","leaked"],
}
TOPICS = {
    "timing": ["late","on time","on-time","wait","waiting","no show","no-show","schedule","quick","fast"],
    "price": ["price","cost","expensive","overpriced","quote","fair","cheap","charge","invoice","bill"],
    "staff": ["rude","friendly","staff","technician","tech","receptionist","crew","team","nurse","stylist"],
    "quality": ["quality","work","repair","fixed","leak","result","haircut","cut","install","clean","dirty"],
    "communication": ["call","phone","email","text","responded","ignored","unresponsive","communication"],
}

def _words(text):
    return re.findall(r"[a-z'-]+", text.lower())

def classify(rating, text):
    t = (text or "").lower()
    words = set(_words(t))
    score = sum(1 for w in NEG if (w in words or (" " in w and w in t)))
    score -= sum(1 for w in POS if (w in words or (" " in w and w in t)))
    try:
        r = float(rating)
    except (TypeError, ValueError):
        r = 3.0
    if r >= 4 and score <= 0: sentiment = "positive"
    elif r <= 2 or score >= 2: sentiment = "negative"
    else: sentiment = "mixed"
    risks = sorted(k for k, kws in RISK.items() if any(kw in t for kw in kws))
    topics = [k for k, kws in TOPICS.items() if any(kw in t for kw in kws)]
    return {"sentiment": sentiment, "risks": risks, "topics": topics or ["general"], "rating": r}

OPENERS = {
    "positive": "Thank you so much, {name}, for the kind words",
    "mixed": "Thank you for the honest feedback, {name}",
    "negative": "Hi {name}, we're sorry your experience fell short of what we aim for",
}
TOPIC_LINE = {
    "timing": {"positive": "We're glad we respected your time.",
               "mixed": "We know timing matters and are tightening our scheduling.",
               "negative": "Running late or leaving you waiting isn't acceptable to us."},
    "price": {"positive": "Fair, clear pricing is something we work hard on.",
              "mixed": "We'd be glad to walk through how your quote was built.",
              "negative": "We'd like to review your invoice with you directly."},
    "staff": {"positive": "We'll pass your compliments on to the team.",
              "mixed": "We'll share your comments with the team.",
              "negative": "How you were treated matters, and we're looking into it with the team."},
    "quality": {"positive": "Quality work is the goal on every job.",
                "mixed": "We want the work to be right, and will gladly take another look.",
                "negative": "We'd like the chance to put the work right."},
    "communication": {"positive": "Good communication is a priority for us.",
                      "mixed": "We can do better at keeping you informed.",
                      "negative": "You shouldn't have had to chase us for answers."},
    "general": {"positive": "It means a lot to our whole team.",
                "mixed": "We take every comment seriously.",
                "negative": "We take this seriously."},
}

def draft_reply(review, business, sign_off=None, contact=None):
    c = classify(review.get("rating"), review.get("text", ""))
    name = (review.get("name") or "there").split()[0] if review.get("name") else "there"
    s = c["sentiment"]
    parts = [OPENERS[s].format(name=name) + ("." if s != "positive" else " about " + business + ".")]
    parts.append(TOPIC_LINE[c["topics"][0]][s])
    if s == "negative":
        parts.append("Please reach out to us directly" + (f" at {contact}" if contact else "")
                     + " so we can make this right.")
    elif s == "positive":
        parts.append("We look forward to serving you again.")
    else:
        parts.append("If you'd like to talk it through, " + (f"contact us at {contact}." if contact else "please contact us."))
    parts.append(f"- {sign_off or 'The ' + business + ' Team'}")
    reply = " ".join(parts)
    needs_human = bool(c["risks"]) or (s == "negative" and c["rating"] <= 1)
    priority = "ESCALATE" if c["risks"] else ("HIGH" if s == "negative" else ("MEDIUM" if s == "mixed" else "LOW"))
    return {**review, **c, "priority": priority, "needs_human_review": needs_human,
            "draft_reply": reply if not c["risks"] else "[HOLD - do not post. Owner must review: "
            + ", ".join(c["risks"]) + " language detected]\n(Suggested draft) " + reply}
