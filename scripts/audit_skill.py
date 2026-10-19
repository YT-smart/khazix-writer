"""Check local evidence hashes, summary coverage and Markdown links. Does not rate prose."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

def audit(root):
    issues=[]
    manifest=json.loads((root/'raw/manifest.json').read_text(encoding='utf-8'))
    for row in manifest:
        path=root/row['raw']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:
            issues.append(f"Raw missing or modified: {row['id']}")
        if row['status']=='available' and not (root/'wiki/sources'/f"{row['id']}.md").is_file():
            issues.append(f"Missing summary: {row['id']}")
    layout=json.loads((root/'raw/layout/manifest.json').read_text(encoding='utf-8'))
    layout_path=root/layout['raw']
    if not layout_path.is_file() or hashlib.sha256(layout_path.read_bytes()).hexdigest()!=layout['sha256']:
        issues.append('Layout raw missing or modified: L001')
    for path in root.rglob('*.md'):
        if 'raw' in path.relative_to(root).parts or 'legacy' in path.relative_to(root).parts: continue
        content=path.read_text(encoding='utf-8-sig')
        for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\(([^\n)]+)\)',content):
            dest=match[1].strip().strip('<>')
            if not dest or dest.startswith('#') or urlsplit(dest).scheme: continue
            target=(path.parent/unquote(dest.split('#')[0])).resolve()
            if not target.is_relative_to(root):
                issues.append(f'External local dependency: {path.relative_to(root)} -> {dest}')
            elif not target.exists():
                issues.append(f'Broken link: {path.relative_to(root)} -> {dest}')
    for required in ['SKILL.md','wiki/index.md','wiki/log.md','wiki/AGENTS.md','wiki/conflicts.md','references/persona.md','references/writing.md','references/layout.md','references/research/index.md']:
        if not (root/required).is_file(): issues.append(f'Missing required page: {required}')
    return {'sources':len(manifest),'available':sum(r['status']=='available' for r in manifest),'summaries':len(list((root/'wiki/sources').glob('S*.md'))),'issues':issues}

if __name__=='__main__':
    result=audit(Path(__file__).resolve().parents[1])
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(bool(result['issues']))
