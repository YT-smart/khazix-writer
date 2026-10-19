"""Report CSS evidence from the provided WeChat HTML, without fetching images."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import json

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = Counter()
        self.styles = Counter()
        self.images = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        if attrs.get('style'):
            self.styles[attrs['style']] += 1
        if tag == 'img':
            self.images.append({k:v for k,v in attrs.items() if k in ('src','data-src','style','width','height')})

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    p = Inspector()
    p.feed((root/'raw/layout/wechat-reference.html').read_text(encoding='utf-8-sig'))
    print(json.dumps({'tags':dict(p.tags), 'styles':p.styles.most_common(14), 'image_count':len(p.images), 'first_images':p.images[:2]},ensure_ascii=False,indent=2))
