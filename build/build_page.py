import json, io, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

src = open('live-summercamp2026.html', encoding='utf-8').read()
camps = json.load(open('../camps2027.json'))
conf = sum(1 for c in camps if c['status'] == 'confirmed')
free = sum(1 for c in camps if c.get('free') or 'free' in (c.get('cost') or '').lower() or 'no cost' in (c.get('cost') or '').lower())
ext  = sum(1 for c in camps if c.get('extendedDay') == 'Yes')

edits = 0
def sub(old, new, label, count=1):
    global src, edits
    n = src.count(old)
    if n != count:
        print(f'!! FAILED [{label}] — found {n}, expected {count}'); sys.exit(1)
    src = src.replace(old, new); edits += 1

# ── 1. camps array ────────────────────────────────────────────────
lines = src.split('\n')
s = next(i for i, l in enumerate(lines) if l.startswith('let camps = ['))
e = next(i for i, l in enumerate(lines) if i > s and l.strip() == '];')
arr = ['let camps = ['] + ['  ' + json.dumps(c, ensure_ascii=False) + ',' for c in camps] + ['];']
src = '\n'.join(lines[:s] + arr + lines[e+1:])
edits += 1

# ── 2. styles ─────────────────────────────────────────────────────
sub('</style>', open('inject.css', encoding='utf-8').read() + '</style>', 'css')

# ── 3. head + header ──────────────────────────────────────────────
sub('<title>Boston Summer Camps 2026 · JQES Community Resource</title>',
    '<title>Boston Summer Camps 2027 · JQES Community Resource</title>', 'title')
sub('<span>Community Resource · Summer 2026</span>',
    '<span>Community Resource · Summer 2027</span>', 'topbar')
sub('<h1>Boston Summer<br>Camps <span class="accent">2026</span></h1>',
    '<h1>Boston Summer<br>Camps <span class="accent">2027</span></h1>', 'h1')
sub('<p>A community resource for JQES families — search and filter programs across the city. Updated for 2026.</p>',
    '<p>A community resource for JQES families.</p>', 'subtitle')
sub('<div class="stat-chip"><div class="n" id="total-stat">56</div><div class="l">Programs</div></div>',
    '<div class="stat-chip"><div class="n" id="total-stat">0</div><div class="l">Programs</div></div>\n'
    '      <div class="stat-chip"><div class="n" id="conf-stat">0</div><div class="l">2027 Dates Set</div></div>\n'
    '      <div class="stat-chip"><div class="n" id="reg-stat">0</div><div class="l">Registration Open</div></div>', 'stats')
sub('<div class="stat-chip"><div class="n" id="free-stat">11</div><div class="l">Free / Low-Cost</div></div>',
    '', 'free chip removed')
sub('<div class="stat-chip"><div class="n" id="ext-stat">8</div><div class="l">Extended Day</div></div>',
    '', 'ext chip removed')
sub("document.getElementById('free-stat').textContent=camps.filter(isFree).length;", '', 'free stat init')
sub("document.getElementById('ext-stat').textContent=camps.filter(c=>c.extendedDay==='Yes').length;", '', 'ext stat init')

# ── 4. replace the stale 2026 Google Sheet strip ──────────────────
a = src.index('<div style="background:rgba(255,255,255,0.08);border-top:1px solid rgba(255,255,255,0.12);padding:10px 40px;')
b = src.index('</header>', a)
src = src[:a] + (
  '<div style="background:rgba(255,255,255,0.08);border-top:1px solid rgba(255,255,255,0.12);padding:10px 40px;'
  'display:flex;align-items:center;gap:10px;flex-wrap:wrap;">\n'
  '    <span style="font-size:0.8rem;color:rgba(255,255,255,0.75);">'
  f'<strong style="color:#FCD34D;">{conf} of {len(camps)}</strong> programs have published their 2027 dates.</span>\n'
  '    <span id="freshness" style="font-size:0.8rem;"></span>\n'
  '  </div>\n') + src[b:]
edits += 1

# ── 5. controls: confirmed-only toggle + My List ──────────────────
sub("""      <select id="week-f" onchange="filter()">""",
    """      <select id="area-f" onchange="filter()">
        <option value="">\U0001f4cd Any Neighborhood</option>
      </select>
      <select id="reg-f" onchange="filter()">
        <option value="">Registration: Any</option>
        <option value="open">\u2b50 Open now</option>
        <option value="soon">\u23f0 Opening soon (30 days)</option>
        <option value="dated">\U0001f4c5 Has an opening date</option>
        <option value="tbd">Not announced yet</option>
      </select>
      <select id="week-f" onchange="filter()">""", 'reg filter')

sub('''      <button class="add-btn" onclick="openModal()">''',
    '''      <label class="conf-toggle" title="Hide programs that have not published 2027 dates">
        <input type="checkbox" id="conf-f" checked onchange="filter()"> 2027 dates confirmed only
      </label>
      <label class="fav-toggle" title="Show only camps JQES families recommend">
        <input type="checkbox" id="fav-f" onchange="filter()"> \u2605 JQES favorites
      </label>
      <button class="list-btn" id="list-btn" onclick="openList()" title="Save camps to a shortlist and compare them side by side">☆ Save &amp; Compare</button>
      <button class="add-btn" onclick="openModal()">''', 'controls')

# ── 6. week filter → 2027 Mondays ─────────────────────────────────
wk_old = '\n'.join(f'        <option value="2026-{m}">Week of {lbl}</option>' for m, lbl in [
  ('06-22','Jun 22'),('06-29','Jun 29'),('07-06','Jul 6'),('07-13','Jul 13'),('07-20','Jul 20'),
  ('07-27','Jul 27'),('08-03','Aug 3'),('08-10','Aug 10'),('08-17','Aug 17'),('08-24','Aug 24'),('08-31','Aug 31')])
wk_new = '\n'.join(f'        <option value="2027-{m}">Week of {lbl}</option>' for m, lbl in [
  ('06-14','Jun 14'),('06-21','Jun 21'),('06-28','Jun 28'),('07-05','Jul 5'),('07-12','Jul 12'),
  ('07-19','Jul 19'),('07-26','Jul 26'),('08-02','Aug 2'),('08-09','Aug 9'),('08-16','Aug 16'),
  ('08-23','Aug 23'),('08-30','Aug 30')])
sub(wk_old, wk_new, 'week options')

# ── 7. date parsing year ──────────────────────────────────────────
sub('    const start = new Date(2026, sm, sd);', '    const start = new Date(2027, sm, sd);', 'parse start')
sub('    const end   = new Date(2026, em !== undefined ? em : sm, ed);',
    '    const end   = new Date(2027, em !== undefined ? em : sm, ed);', 'parse end')
sub("    ranges[0].end = new Date(2026, 7, 31);", "    ranges[0].end = new Date(2027, 7, 31);", 'parse tail')
sub('placeholder="e.g. July 6 – August 14, 2026"', 'placeholder="e.g. July 5 – August 13, 2027"', 'modal placeholder')

# ── 8. filter(): confirmed-only ───────────────────────────────────
sub('''  const wf=document.getElementById('week-f').value;
  const list=camps.filter(c=>{
    if(activeCat!=='all'&&!c.categories.includes(activeCat)) return false;''',
    '''  const wf=document.getElementById('week-f').value;
  const confOnly=document.getElementById('conf-f').checked;
  const list=camps.filter(c=>{
    if(confOnly&&c.status!=='confirmed') return false;
    if(document.getElementById('fav-f').checked&&!c.favorite) return false;
    const arf=document.getElementById('area-f').value;
    if(arf&&c.area!==arf) return false;
    const rf=document.getElementById('reg-f').value;
    if(rf==='open'&&c.regStatus!=='open') return false;
    if(rf==='dated'&&c.regStatus!=='opens') return false;
    if(rf==='tbd'&&c.regStatus!=='tbd') return false;
    if(rf==='soon'){ if(c.regStatus!=='opens'||!c.regDate) return false; const dd=daysUntil(c.regDate); if(dd<0||dd>30) return false; }
    if(activeCat!=='all'&&!c.categories.includes(activeCat)) return false;''', 'filter confirmed')

# ── 9. card template ──────────────────────────────────────────────
sub("    const tagRow=[freeBadge,extBadge,newBadge].filter(Boolean).join('');",
    "    const favBadge=c.favorite?`<span class=\"fav-tag\">\u2605 JQES FAN FAVORITE</span>`:'';\n"
    "    const statusBadge=c.status==='confirmed'?`<span class=\"ok-tag\">2027 DATES SET</span>`:`<span class=\"tbc-tag\">2027 TBC</span>`;\n"
    "    const tagRow=[favBadge,statusBadge,freeBadge,extBadge,newBadge].filter(Boolean).join('');\n"
    "    const saveBtn=`<button class=\"save-btn${isSaved(c.id)?' on':''}\" title=\"Save to my list\" aria-label=\"Save ${c.name} to my list\" onclick=\"return toggleSave(event,'${c.id}')\">${isSaved(c.id)?'★ Saved':'☆ Save'}</button>`;\n"
    "    const strip=c.status==='confirmed'\n"
    "      ?`<div class=\"status-strip ok\"><span class=\"hd\">✓ Camp has published its 2027 dates</span><span class=\"chk\">Checked ${c.checked}</span></div>`\n"
    "      :`<div class=\"status-strip tbc\"><span class=\"hd\">2027 dates not yet posted</span>${c.note?`<span class=\"nt\">${c.note}</span>`:''}<span class=\"chk\">Checked ${c.checked}</span></div>`;\n"
    "    const ri=regInfo(c);\n"
    "    const regFlag=`<div class=\"reg-flag ${ri.cls}\"><span class=\"dot\"></span><span>${ri.text}</span>${ri.cd?`<span class=\"cd\">${ri.cd}</span>`:''}</div>`;",
    'card badges')

sub('''          ${tagRow?`<div style="display:flex;flex-direction:column;gap:4px;align-items:flex-end;flex-shrink:0">${tagRow}</div>`:''}
        </div>
        <div class="badges-row">${catBadges}</div>
        <div class="card-desc">${c.description}</div>''',
    '''          <div style="display:flex;flex-direction:column;gap:5px;align-items:flex-end;flex-shrink:0">${saveBtn}${tagRow}</div>
        </div>
        <div class="badges-row">${catBadges}</div>
        ${strip}
        ${regFlag}
        ${c.regStatus==='opens'&&c.regDate?`<div class="remind-row"><button class="remind-btn" onclick="return addToGoogleCal(event,'${c.id}')" title="Opens a pre-filled event in Google Calendar — you still have to press Save. Needs you to be signed in to Google.">\u23f0 Google Calendar</button><button class="remind-btn ics" onclick="return downloadIcs(event,'${c.id}')" title="Downloads a calendar file that opens in Apple Calendar, Outlook or Google Calendar. Works whether or not you are signed in.">\U0001f4c5 Apple / Outlook (.ics)</button></div>`:''}
        ${c.favoriteNote?`<div class="fav-note">${c.favoriteNote.replace(/([\w.+-]+@[\w.-]+)/,'<span class="mail-link" role="link" tabindex="0" onclick="mailTo(event,&quot;$1&quot;)" onkeydown="if(event.key===&quot;Enter&quot;)mailTo(event,&quot;$1&quot;)">$1</span>')}</div>`:''}
        <div class="card-desc">${c.description}</div>''', 'card top')

sub('''          <div class="mi"><span class="ml">Registration</span><span class="mv">${c.registration}</span></div>
          ${c.contact?`<div class="mi full"><span class="ml">Contact</span><span class="mv">${c.contact}</span></div>`:''}''',
    '''          <div class="mi"><span class="ml">Registration</span><span class="mv">${c.registration}</span></div>
          ${c.area&&!/not listed/i.test(c.area)?`<div class="mi"><span class="ml">Neighborhood</span><span class="mv">${c.area}</span></div>`:''}
          ${c.location?`<div class="mi full"><span class="ml">Location</span><span class="mv">${c.location}</span></div>`:''}
          ${c.transport?`<div class="mi full"><span class="ml">Getting there</span><span class="mv transport">${c.transport}</span></div>`:''}
          ${c.contact?`<div class="mi full"><span class="ml">Contact</span><span class="mv">${c.contact}</span></div>`:''}
          ${c.ref2026?`<div class="mi full"><span class="ref-line">2026 for reference: ${c.ref2026.replace(/\\n/g,' ')}</span></div>`:''}''',
    'card meta')

# ── 10. compare modal markup ──────────────────────────────────────
sub('''<div class="grid-wrap">
  <div class="grid" id="grid"></div>''',
 '''<div class="grid-wrap">
  <div class="tip-bar" id="tip-bar">
    <span class="tip-ic">\u2606</span>
    <span>Tap <strong>\u2606 Save</strong> on any camp to build a shortlist. Then <strong>Save &amp; Compare</strong> lines them up side by side \u2014 dates, cost, hours, when registration opens \u2014 and exports the lot to Excel, CSV or Google Sheets.</span>
    <button class="tip-x" onclick="dismissTip()">Got it</button>
  </div>
  <div class="grid" id="grid"></div>''', 'tip bar')

sub('<div class="toast" id="toast"></div>',
 '''<!-- MY LIST / COMPARE -->
<div class="modal-overlay" id="list-modal" onclick="listOverlayClick(event)">
  <div class="modal wide">
    <div class="modal-header">
      <div>
        <h2>My List &amp; Compare</h2>
        <p id="cmp-count">Nothing saved yet</p>
      </div>
      <button class="modal-close" onclick="closeList()">✕</button>
    </div>
    <div class="export-row">
      <button class="exp-btn exp-xlsx" onclick="exportXLSX()">⬇ Excel (.xlsx)</button>
      <button class="exp-btn exp-csv"  onclick="exportCSV()">⬇ CSV</button>
      <button class="exp-btn exp-gs"   onclick="copyForSheets()">📋 Copy for Google Sheets</button>
      <button class="exp-btn" style="background:#7C3AED" onclick="icsForSavedList()">\u23f0 Registration reminders (.ics)</button>
      <button class="exp-btn exp-print" onclick="printList()" title="Opens your print dialog — choose Save as PDF for a landscape planner">🖨 Print / Save as PDF</button>
      <button class="exp-btn" style="background:#fff;color:var(--gray);border:1.5px solid var(--border);margin-left:auto" onclick="clearList()">Clear list</button>
    </div>
    <div id="cmp-body"></div>
  </div>
</div>

<div class="toast" id="toast"></div>''', 'compare modal')

# ── 11. init stats + feature JS ───────────────────────────────────
sub("document.getElementById('total-stat').textContent=camps.length;",
    "document.getElementById('total-stat').textContent=camps.length;\n"
    "document.getElementById('conf-stat').textContent=camps.filter(c=>c.status==='confirmed').length;\n"
    "document.getElementById('reg-stat').textContent=camps.filter(c=>c.regStatus==='open').length;", 'init stats')
sub("""    const freeBadge=isFree(c)?`<span class="free-tag">FREE</span>`:'';""",
    """    const freeBadge=isFree(c)?`<span class="free-tag">FREE / LOW-COST</span>`:'';""", 'free badge')

sub("""  if(s.includes('check website')||s.includes('tbd')||s.includes('to be announced')||s.includes('coming soon')) return [];""",
    """  if(s.includes('check website')||s.includes('to be announced')||s.includes('coming soon')||s.includes('not yet posted')) return [];""",
    'date parse guard')

sub("""function campInWeek(camp, weekStr) {
  if(!weekStr) return true;""",
    """function campInWeek(camp, weekStr) {
  if(!weekStr) return true;
  // a camp that has not published 2027 dates cannot be claimed to run in any given week
  if(camp.status !== 'confirmed') return false;""",
    'week filter excludes unconfirmed')

sub("""  document.getElementById('results-bar').innerHTML=`Showing <strong>${list.length}</strong> of ${camps.length} programs`;""",
    """  document.getElementById('results-bar').innerHTML=`Showing <strong>${list.length}</strong> of ${camps.length} programs`
    + (wf?` <span style="color:var(--gray)">\u00b7 camps that have not published 2027 dates are hidden while a week is selected</span>`:'');""",
    'week filter hint')

sub("""    g.innerHTML=`<div class="no-results"><h3>No camps found</h3><p>Try adjusting your search or filters.</p></div>`;""",
    """    const af=activeFilters();
    g.innerHTML=`<div class="no-results"><h3>No camps match all of these</h3>`
      +(af.length?`<p>You have ${af.length} filter${af.length===1?'':'s'} on:</p>
         <div style="display:flex;gap:7px;flex-wrap:wrap;justify-content:center;margin:12px 0 16px">
         ${af.map(f=>`<span style="background:#FFF1E7;border:1px solid #FDBA8C;color:#9A3412;border-radius:99px;padding:4px 12px;font-size:0.78rem;font-weight:700">${f.label}</span>`).join('')}</div>
         <button onclick="clearAllFilters()" style="padding:10px 20px;background:var(--orange);color:#fff;border:none;border-radius:8px;font-family:inherit;font-size:0.88rem;font-weight:700;cursor:pointer">Clear all filters</button>`
        :`<p>Try adjusting your search or filters.</p>`)
      +`</div>`;""",
    'no-results explains itself')

sub('''      <button class="list-btn" id="list-btn" onclick="openList()"''',
    '''      <button class="list-btn" id="clear-f" onclick="clearAllFilters()" style="display:none;background:#fff;color:#9A3412;border-color:#FDBA8C"></button>
      <button class="list-btn" id="list-btn" onclick="openList()"''',
    'clear-filters button')

sub("""  renderGrid(list);""", """  renderGrid(list);
  syncClearBtn();""", 'sync clear button')

sub("""        <div class="card-desc">${c.description}</div>""",
    """        <div class="mini-dates"><span class="ml">2027 dates</span><span class="mv">${clipFor(c.dates, 95)}</span></div>
        <div class="card-desc">${c.description}</div>""", 'mobile mini dates')

sub("""        </div>
      </div>
    </a>`;""",
    """        </div>
        <button class="card-more" onclick="return toggleCard(event,this)" aria-expanded="false">More details <span class="chev">\u25be</span></button>
      </div>
    </a>`;""", 'mobile details toggle')

sub('''// Init
renderGrid(camps);''', '''// Init''', 'init render move')
sub('''document.getElementById('results-bar').innerHTML=`Showing <strong>${camps.length}</strong> programs`;''',
    '''// initial render happens at the end of this script, once the saved list is ready''', 'init render')

src = src.replace('</script>', open('inject.js', encoding='utf-8').read() + '\n</script>', 1)
edits += 1

open('../summercamp2027.html','w',encoding='utf-8').write(src)
# keep the drag-and-drop folder in step with every build
import shutil
if os.path.isdir('../deploy-folder'):
    shutil.copy('../summercamp2027.html', '../deploy-folder/summercamp2027.html')
print(f'✓ built summercamp2027.html — {edits} edits, {len(camps)} camps ({conf} confirmed, {free} free, {ext} extended day), {len(src)/1024:.0f} KB')
