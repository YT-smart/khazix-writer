"""Render an article JSON into inline-styled WeChat HTML and a preview. Stdlib only."""
import argparse
import base64
from html import escape
import json
import mimetypes
import sys
from pathlib import Path
from urllib.parse import urlsplit

FONT = '-apple-system,BlinkMacSystemFont,&quot;PingFang SC&quot;,&quot;Microsoft YaHei&quot;,Arial,sans-serif'
BODY = f'color:rgba(0,0,0,0.9);font-size:16px;font-family:{FONT};line-height:1.6;letter-spacing:0.034em;overflow-wrap:break-word;'
PARA = 'margin:0px 8px 24px;'

def safe_url(value, image=False):
    value = str(value).strip()
    parsed = urlsplit(value)
    if not value or any(ord(c) < 32 for c in value) or '\\' in value:
        raise ValueError('Empty or invalid URL')
    if parsed.scheme:
        if parsed.scheme not in ('http','https') or not parsed.netloc:
            raise ValueError(f'Unsupported URL: {value}')
    elif not image or parsed.netloc or value.startswith('/') or '..' in Path(parsed.path).parts:
        raise ValueError(f'Use http(s) links or a relative image path: {value}')
    return escape(value, quote=True)

def inline(block):
    if 'spans' not in block:
        return escape(str(block.get('text',''))).replace('\n','<br>')
    result=[]
    for span in block['spans']:
        text = escape(str(span.get('text',''))).replace('\n','<br>')
        if span.get('bold'):
            text = f'<strong style="font-weight:bold;">{text}</strong>'
        if span.get('href'):
            text = f'<a href="{safe_url(span["href"])}" style="color:#576b95;text-decoration:underline;">{text}</a>'
        result.append(text)
    return ''.join(result)

def image_data_uri(value, base_dir=None):
    value = str(value).strip()
    if value.startswith('data:'):
        if not value.startswith(('data:image/png;base64,', 'data:image/jpeg;base64,', 'data:image/gif;base64,', 'data:image/webp;base64,')):
            raise ValueError('Final image data must be a base64 PNG, JPEG, GIF, or WebP data URI')
        return value
    parsed = urlsplit(value)
    if parsed.scheme in ('http', 'https'):
        raise ValueError('Download remote images into the article asset folder before rendering; final HTML requires base64 data URIs')
    if parsed.scheme:
        raise ValueError(f'Unsupported image URL: {value}')
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = (base_dir or Path.cwd()) / candidate
    candidate = candidate.resolve()
    try:
        exists = candidate.is_file()
    except OSError as exc:
        raise ValueError(f'Image path cannot be accessed: {candidate}') from exc
    if not exists:
        raise ValueError(f'Image file not found: {candidate}')
    mime = mimetypes.guess_type(candidate.name)[0] or ''
    if not mime.startswith('image/'):
        raise ValueError(f'Unsupported image type: {candidate.name}')
    try:
        encoded = base64.b64encode(candidate.read_bytes()).decode('ascii')
    except OSError as exc:
        raise ValueError(f'Image file cannot be read: {candidate}') from exc
    return f'data:{mime};base64,{encoded}'

def render(document, base_dir=None):
    if not isinstance(document.get('blocks'),list):
        raise ValueError('blocks must be a list')
    output=[f'<section style="{BODY}background-color:#fff;text-align:left;">']
    for block in document['blocks']:
        kind=block.get('type','paragraph')
        text=inline(block)
        if kind=='paragraph':
            output.append(f'<section style="{PARA}">{text}</section>')
        elif kind=='heading':
            output.append(f'<section style="{PARA}font-weight:bold;font-size:17px;">{text}</section>')
        elif kind=='quote':
            output.append(f'<section style="{PARA}font-weight:bold;">{text}</section>')
        elif kind=='image':
            caption=escape(str(block.get('caption','')))
            alt=escape(str(block.get('alt','待补充证据图片')))
            if block.get('src'):
                picture=f'<img src="{escape(image_data_uri(block["src"],base_dir), quote=True)}" alt="{alt}" style="display:block;width:100%;max-width:100%;height:auto;">'
            else:
                picture=f'<p style="margin:0;color:#888;font-size:13px;">[待补图：{alt}]</p>'
            if caption:
                picture+=f'<p style="margin:8px 0 0;color:#888;font-size:12px;line-height:1.6;">{caption}</p>'
            output.append(f'<section style="{PARA}">{picture}</section>')
        elif kind=='list':
            for i,item in enumerate(block.get('items',[]),1):
                value = inline(item) if isinstance(item,dict) else escape(str(item))
                output.append(f'<section style="{PARA}">{i}、{value}</section>')
        else:
            raise ValueError(f'Unknown block type: {kind}')
    if document.get('cta'):
        output.append(f'<section style="{PARA}font-size:15px;">{escape(str(document["cta"]))}</section>')
    for key,label in [('author','作者'),('contact','联系')]:
        if document.get(key):
            output.append(f'<section style="margin:0 8px 8px;color:#b2b2b2;font-size:12px;">&gt;/ {label}：{escape(str(document[key]))}</section>')
    output.append('</section>')
    return '\n'.join(output)+'\n'

def main():
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args()
    data=json.loads(args.input.read_text(encoding='utf-8-sig'))
    fragment=render(data, args.input.parent)
    title=escape(str(data.get('title','公众号正文预览')))
    preview=f'<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title></head><body style="margin:0;background:#f5f5f5;"><main style="max-width:677px;margin:0 auto;padding:24px 12px;background:#fff;">{fragment}</main></body></html>\n'
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'article.html').write_text(fragment,encoding='utf-8')
    (args.output_dir/'article.preview.html').write_text(preview,encoding='utf-8')
    print(f'Rendered {len(data["blocks"])} blocks to {args.output_dir}')

if __name__=='__main__':
    main()
