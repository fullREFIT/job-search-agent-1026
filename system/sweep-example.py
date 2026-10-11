# sweep-example.py - source sweep with per-source coverage ledger
# Sanitized public edition: sample board slugs only. Point the slug lists at your own targets.
# States per source/company: checked (data returned), empty (reachable, no postings), failed:<reason>.
# A failed source never counts as coverage; a quiet source is only "no jobs" when it is checked or empty.
import json, urllib.request, urllib.error, concurrent.futures as cf, re, html, sys
from datetime import date

UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}
SINCE=(date.today().isoformat()[:8]+'01')  # first of the current month; set your window
stats={}
def get(url, body=None, timeout=25):
    h=dict(UA); h['Accept']='application/json, text/html'
    data=None
    if body is not None:
        data=json.dumps(body).encode(); h['Content-Type']='application/json'
    r=urllib.request.Request(url, data=data, headers=h, method='POST' if data else 'GET')
    return urllib.request.urlopen(r,timeout=timeout).read()

# ---- slug lists ----
ash="anthropic openai notion linear ramp vercel supabase retool".split()  # sample slugs; use your own target list
gh="datadog cloudflare stripe mongodb elastic hashicorp okta gusto".split()  # sample slugs
lv="spotify palantir plaid kong".split()  # sample slugs
wk="applause action1 mod-careers noble-ai surglobal humanintelligence 1global pavago".split()
sr="Sia ServiceNow FrasersGroup turnitinllc DeliveryHero smartrecruiters Dev2 Visma BoschDigital AEGPrescott".split()

jobs=[]
def rec(src, co, st):  # st: 'checked'|'empty'|'failed:reason'
    stats.setdefault(src,[]).append((co,st))

def ashby(o):
    try: d=json.loads(get(f"https://api.ashbyhq.com/posting-api/job-board/{o}?includeCompensation=true"))
    except Exception as e: rec('ashby',o,'failed:'+str(e)[:60]); return []
    js=d.get('jobs',[])
    if not js: rec('ashby',o,'empty'); return []
    rec('ashby',o,'checked')
    out=[]
    for j in js:
        c=j.get('compensation') or {}
        out.append(dict(src='ashby',co=o,ats_id=str(j.get('id','')),title=j['title'],url=j.get('jobUrl'),loc=j.get('location'),remote=j.get('isRemote'),pub=(j.get('publishedAt') or '')[:10],pay=c.get('compensationTierSummary') or c.get('scrapeableCompensationSalarySummary'),desc=(j.get('descriptionPlain') or '')[:6000]))
    return out

def ghb(o):
    try: d=json.loads(get(f"https://boards-api.greenhouse.io/v1/boards/{o}/jobs?content=true"))
    except Exception as e: rec('greenhouse',o,'failed:'+str(e)[:60]); return []
    js=d.get('jobs',[])
    if not js: rec('greenhouse',o,'empty'); return []
    rec('greenhouse',o,'checked')
    return [dict(src='greenhouse',co=o,ats_id=str(j.get('id','')),title=j['title'],url=j['absolute_url'],loc=(j.get('location') or {}).get('name'),remote=None,pub=(j.get('first_published') or j.get('updated_at') or '')[:10],pay=None,desc=re.sub('<[^>]+>',' ',j.get('content') or '')[:6000]) for j in js]

def lever(o):
    try: d=json.loads(get(f"https://api.lever.co/v0/postings/{o}?mode=json"))
    except Exception as e: rec('lever',o,'failed:'+str(e)[:60]); return []
    if not d: rec('lever',o,'empty'); return []
    rec('lever',o,'checked')
    return [dict(src='lever',co=o,ats_id=str(j.get('id','')),title=j.get('text'),url=j.get('hostedUrl'),loc=(j.get('categories') or {}).get('location'),remote=None,pub='',pay=None,desc=(j.get('descriptionPlain') or '')[:6000]) for j in d]

def workable(o):
    try: d=json.loads(get(f"https://apply.workable.com/api/v3/accounts/{o}/jobs",{"query":"","location":[],"department":[],"worktype":[],"remote":[]}))
    except Exception as e: rec('workable',o,'failed:'+str(e)[:60]); return []
    js=d.get('results',[])
    if not js: rec('workable',o,'empty'); return []
    rec('workable',o,'checked')
    return [dict(src='workable',co=o,ats_id=str(j.get('id') or j.get('shortcode') or ''),title=j.get('title'),url=f"https://apply.workable.com/{o}/j/{j.get('shortcode','')}",loc=(j.get('location') or {}).get('city') or (j.get('location') or {}).get('country'),remote=(j.get('location') or {}).get('workplace')=='remote',pub=(j.get('published') or '')[:10],pay=None,desc='') for j in js]

def smartrec(o):
    try: d=json.loads(get(f"https://api.smartrecruiters.com/v1/companies/{o}/postings?limit=100"))
    except Exception as e: rec('smartrecruiters',o,'failed:'+str(e)[:60]); return []
    js=d.get('content',[])
    if not js: rec('smartrecruiters',o,'empty'); return []
    rec('smartrecruiters',o,'checked')
    return [dict(src='smartrecruiters',co=o,ats_id=str(j.get('id','')),title=j.get('name'),url=f"https://jobs.smartrecruiters.com/{o}/{j.get('id','')}",loc=(j.get('location') or {}).get('city') or (j.get('location') or {}).get('country'),remote=(j.get('location') or {}).get('remote'),pub=(j.get('releasedDate') or '')[:10],pay=None,desc='') for j in js]

def linkedin():
    kws=["AI enablement","AI adoption lead","forward deployed engineer","AI operations manager","AI transformation","automation lead"]
    found=[]; fails=0
    for kw in kws:
        try:
            b=get(f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={urllib.parse.quote(kw)}&location=United%20States&f_WT=2&f_TPR=r2592000&start=0").decode('utf8','ignore')
            cards=re.findall(r'<li>(.*?)</li>', b, re.S)
            for c in cards:
                t=re.search(r'base-search-card__title[^>]*>\s*(.*?)\s*<', c, re.S)
                co=re.search(r'base-search-card__subtitle[^>]*>.*?>(.*?)<', c, re.S)
                loc=re.search(r'job-search-card__location[^>]*>\s*(.*?)\s*<', c, re.S)
                dt=re.search(r'datetime="([\d-]+)"', c)
                lk=re.search(r'href="(https://[^"]*linkedin.com/jobs/view/[^"?]+)', c)
                if t and lk:
                    found.append(dict(src='linkedin',co=html.unescape(co.group(1)).strip() if co else '?',ats_id='',title=html.unescape(t.group(1)).strip(),url=lk.group(1),loc=html.unescape(loc.group(1)).strip() if loc else '',remote='remote' in (loc.group(1).lower() if loc else ''),pub=dt.group(1) if dt else '',pay=None,desc=''))
        except Exception as e:
            fails+=1
    if fails==len(kws): rec('linkedin','guest-api',f'failed: all {fails} queries failed')
    else:
        rec('linkedin','guest-api',f'checked ({len(kws)-fails}/{len(kws)} queries ok, {len(found)} cards)')
    return found

def indeed_probe():
    try:
        get('https://www.indeed.com/jobs?q=AI+enablement&l=Remote')
        rec('indeed','web','checked'); return []
    except urllib.error.HTTPError as e:
        rec('indeed','web',f'failed:HTTP {e.code}'); return []
    except Exception as e:
        rec('indeed','web','failed:'+str(e)[:60]); return []

with cf.ThreadPoolExecutor(16) as ex:
    futs=[ex.map(ashby,set(ash)),ex.map(ghb,set(gh)),ex.map(lever,set(lv)),ex.map(workable,set(wk)),ex.map(smartrec,set(sr))]
    for f in futs:
        for r in f: jobs+=r
jobs+=linkedin()
jobs+=indeed_probe()

# ---- filter ----
TITLE=re.compile(r'enablement|adoption|transformation|automation|forward deployed|solutions (engineer|architect)|implementation|customer engineer|engagement manager|gtm engineer|growth engineer|revenue (systems|operations)|business systems|operations lead|developer advocat|curriculum|knowledge engineer|prompt engineer|conversation design|deployment|technical account|professional services|technical program manager|program manager', re.I)
EXCL=re.compile(r'\b(software engineer|backend|front.?end|full.?stack|devops|sre|site reliability|infrastructure|machine learning|ml engineer|data (scientist|engineer)|security engineer|ios|android|mobile|account executive|sdr|bdr|sales manager|sales director|account manager|customer success manager)\b', re.I)
REMOTE=re.compile(r'\bremote\b', re.I)
US=re.compile(r'united states|usa|u\.s\.|us only|us remote|remote.?us|california|new york|\bUS\b', re.I)

def keep(j):
    t=j['title'] or ''
    if not TITLE.search(t): return False
    if EXCL.search(t): return False
    locstr=f"{j.get('loc') or ''} {j.get('title') or ''}"
    remote = j.get('remote') or REMOTE.search(locstr) or REMOTE.search((j.get('desc') or '')[:1500])
    if not remote: return False
    if re.search(r'emea|europe only|uk only|united kingdom|canada only|india|australia|germany|poland|ireland|netherlands|spain|france|latam|apac', locstr, re.I) and not US.search(locstr): return False
    pub=j.get('pub') or ''
    if pub and pub < SINCE: return False
    return True

kept=[j for j in jobs if keep(j)]
json.dump(jobs, open('all.json','w'))
json.dump(kept, open('kept.json','w'), indent=1)
json.dump(stats, open('stats.json','w'), indent=1)
print(f"total postings: {len(jobs)} | kept after filter: {len(kept)}")
print("=== per-source ===")
for src,rows in stats.items():
    chk=[c for c,s in rows if s.startswith('checked')]
    emp=[c for c,s in rows if s=='empty']
    fail=[(c,s) for c,s in rows if s.startswith('failed')]
    print(f"{src}: checked={len(chk)} empty={len(emp)} failed={len(fail)}")
    for c,s in fail[:12]: print(f"   FAIL {c}: {s}")
