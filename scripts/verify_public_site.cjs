const {chromium}=require('playwright');
const fs=require('fs');
const http=require('http');
const path=require('path');
const {default:AxeBuilder}=require('@axe-core/playwright');
const site=path.resolve(__dirname,'../site');
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.webp':'image/webp','.svg':'image/svg+xml'};
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
// Decorative assets must load, searches must still work, and small empty states must fit.
for(const [file, searchId] of [['areas.html','areaSearch'],['programs.html','programSearch']]){
 await page.goto(base+file);await page.waitForSelector('.guide-link');
 if(!await page.locator('.search-results-note img').evaluate(el=>el.complete&&el.naturalWidth>0))throw Error('Search fox did not load');
 await page.setViewportSize({width:320,height:844});
 await page.locator('#'+searchId).fill('zzzz-no-match');await page.waitForSelector('.friendly-empty');
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Empty state overflows');
 await page.locator('#'+searchId).fill('behavior');await page.waitForSelector('.guide-link');
 if(await page.locator('.friendly-empty').count())throw Error('Search results did not recover');
}
await page.setViewportSize({width:1440,height:1000});
await page.emulateMedia({reducedMotion:'reduce'});await page.goto(base+'areas.html');await page.waitForSelector('.guide-link');
await page.locator('.guide-link').first().hover();
if(await page.locator('.guide-arrow').first().evaluate(el=>getComputedStyle(el).transitionDuration)!=='0s')throw Error('Reduced motion preference ignored');
await page.emulateMedia({reducedMotion:'no-preference'});
const lib=JSON.parse(fs.readFileSync('site/content/programs/school-library.json'));
for(const p of lib.programs){
 await page.goto(base+'program.html?code='+p.code);await page.waitForSelector('.program-article');
 const links=await page.locator('#overview .related-links a').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
 if(links.length!==p.primaryFields.length)throw Error('Missing field links '+p.code);
 const sectionIds=await page.locator('.article-content > section').evaluateAll(es=>es.map(e=>e.id));
 if(sectionIds.slice(0,3).join(',')!=='overview,school,academics')throw Error('School section order '+p.code);
 if(await page.locator('#school .school-facts > div').count()!==6)throw Error('School topics missing '+p.code);
 if(await page.locator('#school .school-photo img').count()!==1)throw Error('School photo missing '+p.code);
 const numbers=await page.locator('.article-content > section .section-number').allTextContents();
 if(numbers.join(',')!=='01,02,03,04,05,06,07,08')throw Error('Section numbering '+p.code);
 for(const href of await page.locator('#school sup a').evaluateAll(es=>es.map(e=>e.getAttribute('href')))){
  if(await page.locator(href).count()!==1)throw Error('School citation target '+p.code+' '+href);
 }
 for(const width of [320,390,768]){
  await page.setViewportSize({width,height:844});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)){
   const overflow=await page.locator('body *').evaluateAll(es=>es.filter(el=>el.getBoundingClientRect().right>innerWidth+1||el.scrollWidth>el.clientWidth+1).map(el=>({tag:el.tagName,classes:el.className,width:el.getBoundingClientRect().width,right:el.getBoundingClientRect().right,scroll:el.scrollWidth,client:el.clientWidth,text:el.textContent.slice(0,60)})).slice(0,25));
   throw Error('Program overflow '+p.code+' at '+width+': '+JSON.stringify(overflow));
  }
 }
 await page.setViewportSize({width:1440,height:1000});
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
for(const width of [320,360,390,414,600,768,899,900,1024,1099,1100,1280,1440]){
 await page.setViewportSize({width,height:844});await page.goto(base+'compare.html');
 const overflow=await page.locator('.comparison-page, .comparison-scroll, .comparison-table, .comparison-table caption, .comparison-table tbody, .comparison-table tbody tr, .comparison-table tbody th, .comparison-table tbody td, .cmp-chip').evaluateAll(es=>es.filter(el=>el.scrollWidth>el.clientWidth+1||el.getBoundingClientRect().right>innerWidth+1).map(el=>({tag:el.tagName,classes:el.className,width:el.clientWidth,scroll:el.scrollWidth})));
 if(overflow.length||await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Comparison overflow at '+width+': '+JSON.stringify(overflow));
 if(await page.locator('tbody tr').count()!==lib.programs.length)throw Error('Program missing at '+width);
 if(width<1100){
  const row=await page.locator('tbody tr').first().boundingBox();
  const cells=await page.locator('tbody tr').first().locator('th,td').all();
  for(const cell of cells){const box=await cell.boundingBox();if(box.x<row.x||box.x+box.width>row.x+row.width+1)throw Error('Cell outside card at '+width);}
 }
}
await page.setViewportSize({width:390,height:844});await page.goto(base+'compare.html');
await page.locator('.comparison-key summary').click();
if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Expanded help overflows');
await page.emulateMedia({media:'print'});
if(await page.locator('.comparison-table').evaluate(el=>getComputedStyle(el).display)!=='table')throw Error('Print table did not restore');
await page.emulateMedia({media:'screen'});
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
await page.setViewportSize({width:320,height:844});
for(const colorScheme of ['light','dark']){
 await page.emulateMedia({colorScheme});await page.goto(base+'compare.html');
 const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
 if(results.violations.length)throw Error('Mobile '+colorScheme+' '+JSON.stringify(results.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))));
}
await browser.close();server.close();if(errors.length)throw Error(errors.join('\n'));console.log('Browser checks passed: 18 field guides, 15 program guides, static comparison, keyboard skip/focus/scroll, sticky TOC, dark mode, responsive navigation.');
})().catch(e=>{console.error(e);server.close();process.exit(1)});
