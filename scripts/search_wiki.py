"""Small lexical search over compiled Wiki; optional raw-source fallback. Stdlib only."""
import argparse
import json
from pathlib import Path
import re
import sys

def terms(query):
    found=[]
    for term in re.findall(r'[a-z0-9][a-z0-9._-]*|[\u4e00-\u9fff]+',query.lower()):
        found.append(term)
        if re.fullmatch(r'[\u4e00-\u9fff]{3,}',term):
            found.extend(term[i:i+2] for i in range(len(term)-1))
    return list(dict.fromkeys(found))

def main():
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--limit',type=int,default=6)
    parser.add_argument('--raw',action='store_true')
    args=parser.parse_args()
    if args.limit < 1: parser.error('--limit must be positive')
    root=Path(__file__).resolve().parents[1]
    tokens=terms(args.query)
    if not tokens: parser.error('query needs Chinese or alphanumeric text')
    files=[p for part in ('sources','concepts','entities') for p in (root/'wiki'/part).glob('*.md')]
    if args.raw: files+=list((root/'raw/articles').glob('*.md'))
    results=[]
    for path in files:
        text=path.read_text(encoding='utf-8-sig')
        lower=text.lower()
        title=next((line.lstrip('# ') for line in text.splitlines() if line.startswith('# ')),path.stem)
        score=sum(min(lower.count(t),10)+5*title.lower().count(t) for t in tokens)
        if score:
            lines=[line.strip() for line in text.splitlines() if any(t in line.lower() for t in tokens)]
            excerpt=' '.join(lines[:3])[:500]
            results.append({'path':path.relative_to(root).as_posix(),'title':title,'score':score,'excerpt':excerpt})
    results.sort(key=lambda r:(-r['score'],r['path']))
    print(json.dumps(results[:args.limit],ensure_ascii=False,indent=2))

if __name__=='__main__': main()
