import json, re, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from gum_content import P
from gum_guides import G
SITE = 'https://ronitkumartoppo-del.github.io/glowtheory-pages/'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = re.search(r'<style>.*?</style>', open(os.path.join(ROOT, 'picks/art-of-saying-no/index.html')).read(), re.S).group(0)
CSS = CSS.replace('</style>', 'table{width:100%;border-collapse:collapse;font-size:.92rem;margin-top:10px}th,td{border:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}th{background:var(--peach)}tr.us td{background:#fff0f6;font-weight:600}ol.steps{padding-left:1.2em}ol.steps li{margin-bottom:.6em}.price{font-size:1.6rem;font-weight:800;color:var(--magenta)}.rel{display:grid;gap:12px}@media(min-width:760px){.rel{grid-template-columns:repeat(3,1fr)}}.rel a{text-decoration:none}.rel img{border-radius:10px;margin-bottom:8px}</style>')
FAV = re.search(r'<link rel="icon"[^>]*>', open(os.path.join(ROOT, 'picks/art-of-saying-no/index.html')).read()).group(0)
E = html.escape
BY = {p['slug']: p for p in P}

def abs_img(p):
    return SITE + p['img'].replace('../../', '')

def page(p):
    canon = f"{SITE}p/{p['slug']}/"
    buy = p['url'] + ('?' if '?' not in p['url'] else '&') + 'utm_source=glowtheory_pages&utm_medium=landing&utm_campaign=' + p['slug']
    cta_word = 'Get it free' if p['price'] == '0' else f"Get it for ${p['price']}"
    price_txt = 'Free' if p['price'] == '0' else f"${p['price']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Shop", "item": SITE + "shop.html"},
            {"@type": "ListItem", "position": 2, "name": p['name'], "item": canon}]},
        {"@type": "Product", "name": p['name'], "description": p['meta'], "image": abs_img(p),
         "brand": {"@type": "Brand", "name": "Glow Theory & Co."}, "category": "Printable planner (digital download)",
         "offers": {"@type": "Offer", "price": p['price'], "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": p['url']}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}]}
    gt, gs = G[p['slug']]
    guide = '<section><div class="wrap"><h2>' + E(gt) + '</h2>' + ''.join(f'<h3>{E(h)}</h3><p>{E(t)}</p>' for h, t in gs) + '</div></section>'
    pain = ''.join(f'<h3>{E(h)}</h3><p>{E(t)}</p>' for h, t in p['pain'])
    inside = ''.join(f'<li>{E(x)}</li>' for x in p['inside'])
    how = ''.join(f'<li><b>{E(a)}.</b> {E(b)}</li>' for a, b in p['how'])
    rows = ''.join(f'<tr{" class=us" if i == len(p["compare"])-1 else ""}><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>' for i, (a, b, c, d) in enumerate(p['compare']))
    pros = ''.join(f'<li>{E(x)}</li>' for x in p['pros']); cons = ''.join(f'<li>{E(x)}</li>' for x in p['cons'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in p['faq'])
    rel = ''
    for s in p['related']:
        r = BY[s]
        rel += f'<a class="card" href="../{s}/"><img src="{r["img"].replace("../../", "../../")}" alt="{E(r["img_alt"])}" loading="lazy"><b>{E(r["name"])}</b><br><span class="note">{"Free" if r["price"]=="0" else "$"+r["price"]}</span></a>'
    pages = f"{p['pages']} printable pages · " if p['pages'] else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(p['title'])} | Glow Theory &amp; Co.</title>
<meta name="description" content="{E(p['meta'])}">
<meta name="keywords" content="{E(p['kw'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#BE185D">
<meta property="og:type" content="product">
<meta property="og:site_name" content="Glow Theory &amp; Co.">
<meta property="og:title" content="{E(p['title'])}">
<meta property="og:description" content="{E(p['meta'])}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{abs_img(p)}">
<meta name="twitter:card" content="summary_large_image">
{FAV}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap">
{CSS}
<script type="application/ld+json">{json.dumps(ld).replace('<', '\\u003c')}</script>
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="../../">Glow Theory &amp; Co.</a></div></header>
<main>
<section class="hero"><div class="wrap">
<span class="eyebrow">{E(p['eyebrow'])}</span>
<h1>{E(p['h1'])}</h1>
<p class="sub">{E(p['sub'])}</p>
<div class="shot"><img src="{p['img']}" alt="{E(p['img_alt'])}" width="1200" height="900"></div>
<p class="price">{price_txt}</p>
<a class="btn" href="{buy}" target="_blank" rel="noopener">{cta_word} on Gumroad →</a>
<p class="note">{pages}Instant digital download · US Letter + A4 PDF · Made by Glow Theory &amp; Co.</p>
</div></section>
<section class="alt"><div class="wrap">
<h2>Why this exists</h2>
{pain}
</div></section>
{guide}
<section><div class="wrap">
<h2>What's inside</h2><ul class="ck">{inside}</ul>
</div></section>
<section class="alt"><div class="wrap">
<h2>How to use it</h2><ol class="steps">{how}</ol>
</div></section>
<section><div class="wrap">
<h2>How it compares</h2>
<table><thead><tr><th>Option</th><th>What it covers</th><th>Structure</th><th>Catch</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>
<section class="alt"><div class="wrap two">
<div><h2>What you'll like</h2><ul class="ck">{pros}</ul></div>
<div><h2>Honest catches</h2><ul class="ck no">{cons}</ul></div>
</div></section>
<section><div class="wrap">
<div class="banner"><h2>{E(p['name'])}</h2><p>{E(p['sub'])}</p><a class="btn sm" href="{buy}" target="_blank" rel="noopener">{cta_word} on Gumroad →</a></div>
<h2>FAQ</h2>{faq}
<p class="disc">No reviews or results are claimed on this page. Personal use only; please don't resell or share the files. This is a planning tool, not medical, financial or mental-health advice.</p>
</div></section>
<section class="alt"><div class="wrap">
<h2>You might also like</h2><div class="rel">{rel}</div>
<p class="center" style="margin-top:18px"><a href="../../shop.html">← All Glow Theory picks</a></p>
</div></section>
</main>
<footer><div class="wrap">© 2026 Glow Theory &amp; Co. · Self-care · Planners · Printables</div></footer>
</body>
</html>
'''

for p in P:
    d = os.path.join(ROOT, 'p', p['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(page(p))
    txt = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', page(p), flags=re.S))
    print(p['slug'], len(txt.split()), 'words')
