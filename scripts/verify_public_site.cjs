const {chromium}=require('playwright');
const fs=require('fs');
const http=require('http');
const path=require('path');
const {default:AxeBuilder}=require('@axe-core/playwright');
const site=path.resolve(__dirname,'../site');
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.webp':'image/webp'};
const server=http.createServer((req,res)=>{
 const file=path.resolve(site,'.'+new URL(req.url,'http://localhost').pathname);
 if(!file.startsWith(site+path.sep)){res.writeHead(403).end();return;}
 fs.readFile(file,(error,data)=>{if(error){res.writeHead(404).end();return;}res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(data);});
});
(async()=>{
await new Promise(resolve=>server.listen(8765,'127.0.0.1',resolve));
const browser=await chromium.launch({headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
await context.route('**/*',route=>route.request().url().startsWith('http://127.0.0.1:8765/')?route.continue():route.abort());
const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
const base='http://127.0.0.1:8765/';
for(const path of ['index.html','areas.html','programs.html','compare.html']){
 await page.goto(base+path);if(path==='areas.html'||path==='programs.html')await page.waitForSelector('.guide-link');
 if(await page.locator('a[href*="job.html"],a[href*="jobs.html"]').count())throw Error('Retired job link '+path);
 if(await page.locator('.guide-count').count())throw Error('Decorative index number '+path);
 await page.keyboard.press('Tab');if(await page.locator(':focus').getAttribute('class')!=='skip-link')throw Error('Skip not first '+path);
 await page.keyboard.press('Enter');if(await page.locator(':focus').evaluate(el=>el.tagName)!=='MAIN')throw Error('Skip target '+path);
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Page overflow '+path);
}
const lib=JSON.parse(fs.readFileSync('site/content/programs/school-library.json'));
for(const p of lib.programs){
 await page.goto(base+'program.html?code='+p.code);await page.waitForSelector('.program-article');
 const links=await page.locator('#overview .related-links a').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
 if(links.length!==p.primaryFields.length)throw Error('Missing field links '+p.code);
}
const fields=JSON.parse(fs.readFileSync('site/content/areas/index.json'));
for(const name of fields.areas){
 await page.goto(base+'areas/'+name.replace('.json','.html'));await page.waitForSelector('#careers .career-list');
 if(await page.locator('#careers a[href*="job"]').count())throw Error('Career job link');
 if(!(await page.locator('.career-entry').count()))throw Error('Missing career content');
}
await page.goto(base+'areas/animal-behavior.html');await page.waitForSelector('#careers');
await page.evaluate(()=>scrollTo(0,1400));
const toc=await page.locator('.article-toc').evaluate(el=>({top:el.getBoundingClientRect().top,position:getComputedStyle(el).position}));
if(toc.position!=='sticky'||Math.abs(toc.top-20)>2)throw Error('TOC not sticky '+JSON.stringify(toc));
await page.emulateMedia({colorScheme:'dark'});
await page.goto(base+'compare.html');
const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();await staticPage.goto(base+'compare.html');if(await staticPage.locator('tbody tr').count()!==15)throw Error('Static table missing');await nojs.close();
await page.setViewportSize({width:390,height:844});await page.goto(base+'compare.html');
if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Mobile page overflow');
const region=page.locator('.comparison-scroll');await region.focus();await page.keyboard.press('ArrowRight');await page.waitForTimeout(150);
if(await region.evaluate(el=>el.scrollLeft)===0)throw Error('Table not keyboard scrollable');
await region.evaluate(el=>el.scrollLeft=0);
await page.locator('#menuButton').click();if(await page.locator('#primaryNav').isVisible()!==true)throw Error('Mobile menu failed');
for(const width of [700,800,999,1024,1280]){await page.setViewportSize({width,height:900});await page.goto(base+'index.html');if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Header overflow '+width);}
await page.setViewportSize({width:1440,height:1000});
for(const colorScheme of ['light','dark']){
 await page.emulateMedia({colorScheme});
 for(const file of ['index.html','areas.html','programs.html','compare.html','areas/animal-behavior.html','program.html?code=UMA-VT']){
  await page.goto(base+file);
  if(file.startsWith('areas/'))await page.waitForSelector('#careers');
  else if(file.startsWith('program.html'))await page.waitForSelector('#skills');
  else if(file==='areas.html'||file==='programs.html')await page.waitForSelector('.guide-link');
  const a11y=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
  if(a11y.violations.length)throw Error(colorScheme+' '+file+' '+JSON.stringify(a11y.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))));
 }
}
await browser.close();server.close();if(errors.length)throw Error(errors.join('\n'));console.log('Browser checks passed: 18 field guides, 15 program guides, static comparison, keyboard skip/focus/scroll, sticky TOC, dark mode, responsive navigation.');
})().catch(e=>{console.error(e);server.close();process.exit(1)});
