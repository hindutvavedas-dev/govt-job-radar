import json, re, hashlib, os
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(ROOT, 'sources.json')
QUEUE = os.path.join(ROOT, 'review_queue.json')
KEYWORDS = re.compile(r'vacan|recruit|advertisement|notification|apply online|career|job|selection post|constable|sub inspector|stenographer|assistant|technician|group [abc d]|direct recruitment|employment notice|recruitment notice|opening|opportunit', re.I)
SKIP = re.compile(r'privacy|accessibility|contact us|tender|procurement|login|sign in|forgot password|annual report', re.I)
HEADERS = {'User-Agent': 'GovtJobRadarBot/1.0 (public recruitment notice monitoring; polite low-frequency checks)'}

def read_json(path, fallback):
    try:
        with open(path, encoding='utf-8') as f: return json.load(f)
    except (OSError, json.JSONDecodeError): return fallback

def write_json(path, value):
    with open(path, 'w', encoding='utf-8') as f: json.dump(value, f, ensure_ascii=False, indent=2)

def main():
    sources = read_json(SOURCES, [])
    queue = read_json(QUEUE, [])
    seen = {x.get('id') for x in queue}
    run_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
    checked, errors, added = 0, [], 0
    for source in sources:
        url = source['url']
        try:
            response = requests.get(url, headers=HEADERS, timeout=18, allow_redirects=True)
            response.raise_for_status()
            content_type = response.headers.get('content-type', '').lower()
            if 'html' not in content_type and not response.text.lstrip().startswith('<'):
                continue
            soup = BeautifulSoup(response.text[:2_000_000], 'html.parser')
            for tag in soup(['script', 'style', 'noscript', 'svg']): tag.decompose()
            checked += 1
            found = 0
            for a in soup.find_all('a', href=True):
                title = ' '.join(a.get_text(' ', strip=True).split())
                href = urljoin(response.url, a['href'].strip())
                if not title or len(title) < 5 or len(title) > 220: continue
                if SKIP.search(title): continue
                if not KEYWORDS.search(title): continue
                parsed = urlparse(href)
                if parsed.scheme not in ('http', 'https'): continue
                if parsed.netloc.lower() != urlparse(response.url).netloc.lower() and not parsed.netloc.lower().endswith('.gov.in'):
                    continue
                digest = hashlib.sha256((source['name'] + '|' + href).encode('utf-8')).hexdigest()[:20]
                if digest in seen: continue
                queue.append({
                    'id': digest, 'title': title, 'source_name': source['name'],
                    'source_category': source['category'], 'source_page': url,
                    'notice_url': href, 'detected_at_utc': run_at,
                    'status': 'Needs manual review',
                    'review_note': 'Candidate link found on an official source page. Open the notice and verify it is a recruitment notification, current/open, and relevant before publishing.'
                })
                seen.add(digest); added += 1; found += 1
                if found >= 30: break
        except Exception as exc:
            errors.append({'source': source['name'], 'url': url, 'error': str(exc)[:220]})
    # Keep newest first and cap the review inbox to avoid unbounded growth.
    queue.sort(key=lambda x: x.get('detected_at_utc', ''), reverse=True)
    write_json(QUEUE, queue[:2000])
    report = {'last_run_utc': run_at, 'sources_configured': len(sources), 'pages_checked': checked, 'new_candidates': added, 'errors': errors}
    write_json(os.path.join(ROOT, 'data', 'last_run.json'), report)
    print(json.dumps(report, indent=2))

if __name__ == '__main__': main()
