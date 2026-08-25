import json, os, glob

COLLECTIONS = ["companies", "projects", "skills", "socials", "now-entries", "testimonials", "mentions", "work-history", "blog"]

os.makedirs("dist", exist_ok=True)

for coll in COLLECTIONS:
    files = sorted(glob.glob(f"content/{coll}/*.json"))
    docs = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            docs.append(json.load(fh))
    # sort by explicit "order" field when present, else by "date" desc, else filename order
    if docs and "order" in docs[0]:
        docs.sort(key=lambda d: d.get("order", 0))
    elif docs and "date" in docs[0]:
        docs.sort(key=lambda d: d.get("date", ""), reverse=True)
    with open(f"dist/{coll}.json", "w", encoding="utf-8") as out:
        json.dump({"docs": docs}, out, indent=2, ensure_ascii=False)
        out.write("\n")
    print(coll, len(docs))

# site-settings is a single file, just copy through
if os.path.exists("content/site-settings.json"):
    with open("content/site-settings.json", encoding="utf-8") as fh:
        settings = json.load(fh)
    with open("dist/site-settings.json", "w", encoding="utf-8") as out:
        json.dump(settings, out, indent=2, ensure_ascii=False)
        out.write("\n")
    print("site-settings", "ok")
