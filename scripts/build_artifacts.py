from pathlib import Path
import zipfile, shutil, os
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
OUT=ROOT/'exports'
# standalone HTML
idx=(SITE/'index.html').read_text(encoding='utf-8')
css=(SITE/'styles.css').read_text(encoding='utf-8')
data=(SITE/'data.js').read_text(encoding='utf-8')
app=(SITE/'app.js').read_text(encoding='utf-8')
stand=idx.replace('<link rel="stylesheet" href="styles.css">',f'<style>\n{css}\n</style>')
stand=stand.replace('<script src="data.js"></script><script src="app.js"></script>',f'<script>\n{data}\n</script><script>\n{app}\n</script>')
stand=stand.replace('<span class="footer-links"><a id="guideLink">Full guide</a><a id="workbookLink">Workbook</a><a id="sheetLink">Data spreadsheet</a></span>','<span class="footer-links">Companion files and research database are included in the full project package.</span>')
# Protect footer link assignment in standalone
stand=stand.replace("document.getElementById('guideLink').href=D.resources.guide;document.getElementById('workbookLink').href=D.resources.workbook;document.getElementById('sheetLink').href=D.resources.spreadsheet;", "if(document.getElementById('guideLink'))document.getElementById('guideLink').href=D.resources.guide;if(document.getElementById('workbookLink'))document.getElementById('workbookLink').href=D.resources.workbook;if(document.getElementById('sheetLink'))document.getElementById('sheetLink').href=D.resources.spreadsheet;")
stand_path=OUT/'Animal_Career_College_Explorer_Evidence_Expanded.html';stand_path.write_text(stand,encoding='utf-8')
# site-only zip
sitezip=OUT/'Animal_Career_College_Explorer_Evidence_Expanded_Website.zip'
with zipfile.ZipFile(sitezip,'w',zipfile.ZIP_DEFLATED) as z:
    for p in SITE.rglob('*'):
        if p.is_file():z.write(p,p.relative_to(SITE))
# full project ZIPs (exclude generated archives so rebuilds never nest old ZIPs)
masterzip=OUT/'Animal_Career_Data_Project_with_AZA_Scraper.zip'
projzip=OUT/'Animal_Career_Data_Project.zip'
azazip=OUT/'AZA_Job_Scraper_Package.zip'
generated={masterzip,projzip,azazip,sitezip}
with zipfile.ZipFile(masterzip,'w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file() and p not in generated and '__pycache__' not in p.parts:
            z.write(p,p.relative_to(ROOT))
shutil.copyfile(masterzip,projzip)

# portable AZA collection/classification/review subset
aza_files={
    ROOT/'docs'/'AZA_PACKAGE_README.md':'AZA_Job_Scraper_Package/README.md',
    ROOT/'docs'/'AZA_JOB_INGESTION.md':'AZA_Job_Scraper_Package/docs/AZA_JOB_INGESTION.md',
    ROOT/'docs'/'DATA_MODEL.md':'AZA_Job_Scraper_Package/docs/DATA_MODEL.md',
    ROOT/'database'/'migration_aza_market_jobs.sql':'AZA_Job_Scraper_Package/database/migration_aza_market_jobs.sql',
    ROOT/'scripts'/'scrape_aza_jobs.py':'AZA_Job_Scraper_Package/scripts/scrape_aza_jobs.py',
    ROOT/'scripts'/'propose_aza_job_matches.py':'AZA_Job_Scraper_Package/scripts/propose_aza_job_matches.py',
    ROOT/'scripts'/'review_aza_job_matches.py':'AZA_Job_Scraper_Package/scripts/review_aza_job_matches.py',
    ROOT/'scripts'/'export_aza_jobs.py':'AZA_Job_Scraper_Package/scripts/export_aza_jobs.py',
}
with zipfile.ZipFile(azazip,'w',zipfile.ZIP_DEFLATED) as z:
    for source,arcname in aza_files.items(): z.write(source,arcname)
print(stand_path);print(sitezip);print(masterzip);print(projzip);print(azazip)
