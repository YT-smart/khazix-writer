"""Reproducible descriptive counts; numbers are observations, not writing quotas."""
import json
from pathlib import Path
import re
import statistics

def main():
    root=Path(__file__).resolve().parents[1]
    rows=json.loads((root/'raw/manifest.json').read_text(encoding='utf-8'))
    stats=[]
    for row in rows:
        if row['status']!='available': continue
        text=(root/row['raw']).read_text(encoding='utf-8-sig')
        # Strip known export wrapper and image URLs. Keep text and source punctuation.
        lines=text.splitlines()
        start=next((i+1 for i,l in enumerate(lines[:20]) if l.strip()=='去阅读'),0)
        body='\n'.join(lines[start:])
        body=re.sub(r'!\[[^\]]*\]\([^\n]*\)','',body)
        body=re.sub(r'https?://\S+','',body)
        body=re.sub(r'(?m)^# .*$','',body)
        paragraphs=[p.strip() for p in re.split(r'\n\s*\n',body) if p.strip()]
        stats.append({'id':row['id'],'date':row['date'],'prose_chars_approx':len(body),'paragraphs_export':len(paragraphs),'median_paragraph_chars':statistics.median([len(p) for p in paragraphs]) if paragraphs else 0,'colon_cn':body.count('：'),'double_quotes':sum(body.count(c) for c in ('"','“','”')),'em_dash':body.count('——'),'questions':body.count('？')+body.count('?'),'first_person':body.count('我')})
    result={'method':'Approximate prose counts: strip export intro when known, Markdown image links, raw URLs and first-level headings. Export paragraph merges remain. Not true rendered sentence statistics; never use as quotas.','available':len(stats),'date_min':min(r['date'] for r in stats),'date_max':max(r['date'] for r in stats),'articles_with_colon':sum(r['colon_cn']>0 for r in stats),'articles_with_double_quotes':sum(r['double_quotes']>0 for r in stats),'articles_with_em_dash':sum(r['em_dash']>0 for r in stats),'median_prose_chars_approx':statistics.median(r['prose_chars_approx'] for r in stats),'articles':stats}
    dest=root/'references/research/corpus-statistics.json'
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='articles'},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
