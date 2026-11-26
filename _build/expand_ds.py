import re,json,html,os,sys
sys.path.insert(0,os.path.dirname(__file__))
from ds_guides import D
E=html.escape;SITE='https://ronitkumartoppo-del.github.io/glowtheory-pages/'
for slug,g in D.items():
  f=f'picks/{slug}/index.html';s=open(f).read()
  if 'data-guide="1"' in s: continue
  guide='<section data-guide="1"><div class="wrap"><h2>'+E(g['t'])+'</h2>'+''.join(f'<h3>{E(h)}</h3><p>{E(t)}</p>' for h,t in g['s'])+'<p class="disc">General guidance written by Glow Theory &amp; Co. It is not medical, psychological or legal advice.</p></div></section>\n'
  s=s.replace('<section class="alt"><div class="wrap">\n<h2>Reviews &amp; proof</h2>',guide+'<section class="alt"><div class="wrap">\n<h2>Reviews &amp; proof</h2>',1)
  extra=''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in g['faq'])
  s=re.sub(r'(<h2>FAQ</h2>(?:<details>.*?</details>)+)',lambda m:m.group(1)+extra,s,count=1,flags=re.S)
  faqs=re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>',s)
  h1=re.search(r'<h1>(.*?)</h1>',s).group(1)
  ld={"@context":"https://schema.org","@graph":[{"@type":"Article","headline":html.unescape(h1),"author":{"@type":"Organization","name":"Glow Theory & Co."},"publisher":{"@type":"Organization","name":"Glow Theory & Co."},"dateModified":"2026-11-26","mainEntityOfPage":SITE+f'picks/{slug}/'},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":html.unescape(q),"acceptedAnswer":{"@type":"Answer","text":html.unescape(a)}} for q,a in faqs]}]}
  s=s.replace('</head>','<meta name="robots" content="index,follow,max-image-preview:large">\n<script type="application/ld+json">'+json.dumps(ld).replace('<','\\u003c')+'</script>\n</head>',1)
  open(f,'w').write(s)
  print(slug,len(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S)).split()),'words', 'guide' if 'data-guide' in s else 'NO GUIDE')
