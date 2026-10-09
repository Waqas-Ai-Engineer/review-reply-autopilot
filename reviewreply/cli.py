import argparse, csv, html, json, sys
from . import __version__
from .core import draft_reply
from .llm import polish

def main(argv=None):
    p = argparse.ArgumentParser(prog="reviewreply", description="Draft safe replies to customer reviews.")
    p.add_argument("csv", help="CSV with columns: name,rating,text")
    p.add_argument("--business", default="Our Business")
    p.add_argument("--contact", help="phone/email shown in negative replies")
    p.add_argument("--format", choices=["table", "json", "html", "csv"], default="table")
    p.add_argument("--llm", action="store_true", help="polish drafts via LLM_API_KEY (optional)")
    p.add_argument("--version", action="version", version=__version__)
    a = p.parse_args(argv)
    with open(a.csv, newline="", encoding="utf-8") as f:
        rows = [draft_reply(r, a.business, contact=a.contact) for r in csv.DictReader(f)]
    if a.llm:
        for r in rows:
            if not r["risks"]:
                r["draft_reply"] = polish(r["draft_reply"], a.business)
    if a.format == "json":
        print(json.dumps(rows, indent=2))
    elif a.format == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    elif a.format == "html":
        print("<!doctype html><meta charset=utf-8><title>Review replies</title><style>body{font:15px system-ui;max-width:860px;margin:2rem auto}"
              ".c{border:1px solid #ddd;border-radius:8px;padding:1rem;margin:1rem 0}.ESCALATE{border-color:#c00}.HIGH{border-color:#e90}"
              "b{font-size:12px;padding:2px 6px;background:#eee;border-radius:4px}</style><h1>Review reply drafts</h1>")
        for r in rows:
            print(f'<div class="c {r["priority"]}"><b>{r["priority"]}</b> <b>{r["sentiment"]}</b> {r["rating"]}&#9733; - {html.escape(r.get("name",""))}'
                  f'<p><i>{html.escape(r["text"])}</i></p><p>{html.escape(r["draft_reply"])}</p></div>')
    else:
        for r in rows:
            print(f'[{r["priority"]:8}] {r["sentiment"]:8} {r["rating"]:.0f}* {r.get("name","")}: {r["text"][:60]}')
            print(f'           -> {r["draft_reply"]}\n')
        esc = sum(r["priority"] == "ESCALATE" for r in rows)
        print(f"{len(rows)} reviews, {esc} need owner review before posting.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
