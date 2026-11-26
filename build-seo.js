// Prerender crawlable pages from shop.src.html. Run: node build-seo.js
const fs=require('fs');const {JSDOM}=require('jsdom');
const SITE='https://ronitkumartoppo-del.github.io/glowtheory-pages/';
const tpl=fs.readFileSync('shop.src.html','utf8');
const dataJs=fs.readFileSync('shop-data.js','utf8'),seoJs=fs.readFileSync('shop-seo.js','utf8');
global.window={};eval(dataJs);eval(seoJs);const D=window.GLOW;
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const img=id=>{const p=(D.photos||{})[id];return p?`https://images.unsplash.com/${p[0]}?w=1200&h=630&fit=crop&q=80`:'https://images.unsplash.com/photo-1578747763484-51b21a33e4fa?w=1200&h=630&fit=crop&q=80'};
const amz=a=>`https://www.amazon.com/dp/${a}?tag=glowtheoryig-20`;
function render(page){
  const html=tpl.replace(/<script src="\/glowtheory-pages\/shop-data\.js[^"]*"><\/script>/,`<script>${dataJs}</script>`).replace(/<script src="\/glowtheory-pages\/shop-seo\.js[^"]*"><\/script>/,`<script>${seoJs}</script>`).replace('<script>',`<script>window.ResizeObserver=class{observe(){}disconnect(){}};window.scrollTo=()=>{};${page!==null?`window.GLOW_PAGE=${JSON.stringify(page)};`:''}</script><script>`);
  const dom=new JSDOM(html,{runScripts:'dangerously',url:SITE+(page?page+'/':'shop.html')});
  const out=dom.window.document.getElementById('app').innerHTML;dom.window.close();return out}
function head({title,desc,canon,image,ld}){return `<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${canon}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="article"><meta property="og:site_name" content="The Glow Theory">
<meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${canon}"><meta property="og:image" content="${image}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">${JSON.stringify(ld).replace(/</g,'\\u003c')}</script>`}
function page(key,{title,desc,image,ld}){
  const canon=key?SITE+key+'/':SITE+'shop.html';
  let h=tpl.replace(/<title>[\s\S]*?<\/title>\s*<meta name="description"[^>]*>/,head({title,desc,canon,image,ld}));
  h=h.replace('<div id="app"></div>',`<div id="app">${render(key)}</div>`);
  if(key)h=h.replace('<script src="/glowtheory-pages/shop-data.js',`<script>window.GLOW_PAGE=${JSON.stringify(key)}</script>\n<script src="/glowtheory-pages/shop-data.js`);
  return h}
const org={"@type":"Organization","name":"The Glow Theory","url":SITE+"shop.html","sameAs":["https://www.instagram.com/theglowtheory.edit/"]};
const urls=[];const today='2026-11-26';
// home
fs.writeFileSync('shop.html',page(null,{title:'The Glow Theory: Skincare & Self-Care Picks, Honestly Compared',desc:'Skincare and self-care tools compared side by side: ice rollers, gua sha, LED masks, sunscreen, serums and gifts, with what real buyers love and complain about.',image:img('ice-rollers'),ld:{"@context":"https://schema.org","@graph":[{"@type":"WebSite","name":"The Glow Theory","url":SITE+"shop.html"},org,{"@type":"ItemList","itemListElement":Object.keys(D.cats).map((id,i)=>({"@type":"ListItem","position":i+1,"name":D.cats[id].name,"url":SITE+id+'/'}))}]}}));
urls.push(SITE+'shop.html');
for(const [id,c] of Object.entries(D.cats)){const z=D.seo[id];const canon=SITE+id+'/';
 const ld={"@context":"https://schema.org","@graph":[
  {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Shop","item":SITE+"shop.html"},{"@type":"ListItem","position":2,"name":c.name,"item":canon}]},
  {"@type":"Article","headline":z.t,"description":z.d,"image":img(id),"datePublished":"2026-11-02","dateModified":today,"author":org,"publisher":org,"mainEntityOfPage":canon},
  {"@type":"ItemList","name":c.name+" compared","itemListElement":c.items.map((p,i)=>({"@type":"ListItem","position":i+1,"name":p.b+' '+p.n,"url":amz(p.a)}))},
  {"@type":"FAQPage","mainEntity":z.f.map(([q,a])=>({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}))}]};
 fs.mkdirSync(id,{recursive:true});fs.writeFileSync(id+'/index.html',page(id,{title:z.t+' | The Glow Theory',desc:z.d,image:img(id),ld}));urls.push(canon)}
for(const [k,v] of Object.entries(D.collections)){const z=D.seoCol[k];const canon=SITE+k+'/';
 const ld={"@context":"https://schema.org","@graph":[{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Shop","item":SITE+"shop.html"},{"@type":"ListItem","position":2,"name":v.title,"item":canon}]},{"@type":"Article","headline":z.t,"description":z.d,"image":img(v.cats[0]),"dateModified":today,"author":org,"publisher":org,"mainEntityOfPage":canon}].concat(z.f?[{"@type":"FAQPage","mainEntity":z.f.map(([q,a])=>({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}))}]:[])};
 fs.mkdirSync(k,{recursive:true});fs.writeFileSync(k+'/index.html',page(k,{title:z.t+' | The Glow Theory',desc:z.d,image:img(v.cats[0]),ld}));urls.push(canon)}
// sitemap: keep existing urls, add ours
let sm=fs.readFileSync('sitemap.xml','utf8');const have=new Set([...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m=>m[1]));
const add=urls.filter(u=>!have.has(u)).map(u=>`  <url><loc>${u}</loc><lastmod>${today}</lastmod></url>`).join('\n');
if(add)sm=sm.replace('</urlset>',add+'\n</urlset>');fs.writeFileSync('sitemap.xml',sm);
console.log('pages',urls.length,'sitemap urls',(sm.match(/<loc>/g)||[]).length);
