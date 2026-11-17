
/* ════════ MY LIST · COMPARE · EXPORT ════════ */
const LS_KEY = 'jqes-summer-2027-list';
let saved = [];
try { const r = JSON.parse(localStorage.getItem(LS_KEY) || '[]'); if (Array.isArray(r)) saved = r; } catch(e) { saved = []; }

function persistList(){ try { localStorage.setItem(LS_KEY, JSON.stringify(saved)); } catch(e) {} }
function isSaved(id){ return saved.indexOf(id) !== -1; }
function savedCamps(){ return saved.map(id => camps.find(c => c.id === id)).filter(Boolean); }

function toggleSave(ev, id){
  ev.preventDefault(); ev.stopPropagation();
  const i = saved.indexOf(id);
  if (i >= 0){ saved.splice(i,1); showToast('Removed from your list'); }
  else { saved.push(id); showToast('Added to your list'); }
  persistList(); updateListBtn(); filter();
  if (document.getElementById('list-modal').classList.contains('open')) renderCompare();
  return false;
}
function removeSaved(id){
  const i = saved.indexOf(id);
  if (i >= 0){ saved.splice(i,1); persistList(); updateListBtn(); filter(); renderCompare(); }
}
function clearList(){
  if (!saved.length) return;
  saved = []; persistList(); updateListBtn(); filter(); renderCompare();
  showToast('List cleared');
}
function updateListBtn(){
  const b = document.getElementById('list-btn');
  if (!b) return;
  b.innerHTML = saved.length
    ? '★ My List <span class="pip">' + saved.length + '</span>'
    : '☆ Save &amp; Compare';
  b.classList.toggle('has-items', saved.length > 0);
}

/* ── compare panel ── */
function openList(){
  renderCompare();
  document.getElementById('list-modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeList(){
  document.getElementById('list-modal').classList.remove('open');
  document.body.style.overflow = '';
}
function listOverlayClick(e){ if (e.target.id === 'list-modal') closeList(); }

const CMP_ROWS = [
  ['2027 dates',    c => c.dates],
  ['2027 dates published?', c => c.status === 'confirmed' ? 'Yes — published by the camp' : 'Not yet — camp has not posted them'],
  ['Ages',          c => c.ages],
  ['Cost',          c => c.cost],
  ['Hours',         c => c.hours],
  ['Extended day',  c => c.extendedDay],
  ['Registration',  c => c.registration],
  ['Opens',         c => c.regStatus === 'open' ? 'Open now' : (c.regStatus === 'opens' && c.regDate ? fmtReg(c.regDate) : 'Not announced')],
  ['Categories',    c => (c.categories || []).join(', ') || '—'],
  ['Neighborhood',  c => c.area || '—'],
  ['Location',      c => c.location || '—'],
  ['Getting there', c => c.transport || '—'],
  ['JQES favorite', c => c.favorite ? '★ Yes' : '—'],
  ['Notes',         c => c.note || (c.ref2026 ? '2026 for reference: ' + c.ref2026 : '—')],
  ['Website',       c => c.url || '—'],
  ['Last checked',  c => c.checked || '—']
];

function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }

function renderCompare(){
  const list = savedCamps();
  const body = document.getElementById('cmp-body');
  const bar  = document.getElementById('cmp-count');
  document.querySelectorAll('.exp-btn').forEach(b => b.disabled = !list.length);
  bar.textContent = list.length ? list.length + (list.length === 1 ? ' camp saved' : ' camps saved') : 'Nothing saved yet';
  if (!list.length){
    body.innerHTML = '<div class="cmp-empty"><h3>Your list is empty</h3><p>Tap the ☆ on any camp card to add it here, then compare them side by side and export the list.</p></div>';
    return;
  }
  const head = '<thead><tr><th></th>' + list.map(c =>
      '<th>' + esc(c.name) + '<button class="rm" title="Remove" onclick="removeSaved(\'' + c.id + '\')">✕</button></th>').join('') + '</tr></thead>';
  const rows = CMP_ROWS.map(([label, fn]) =>
      '<tr><th>' + esc(label) + '</th>' + list.map(c => {
        const v = fn(c) || '—';
        if (label === 'Website' && c.url)
          return '<td><a class="contact-link" href="' + esc(c.url) + '" target="_blank" rel="noopener noreferrer">' + esc(c.url.replace(/^https?:\/\//,'').slice(0,42)) + '↗</a></td>';
        return '<td>' + esc(v).replace(/\n/g,'<br>') + '</td>';
      }).join('') + '</tr>').join('');
  body.innerHTML = '<div class="cmp-scroll"><table class="cmp">' + head + '<tbody>' + rows + '</tbody></table></div>';
}

/* ── export ── */
const PLAN_HEAD = ['Pick','Status','Rating','For which child','Friends going','Family notes'];
const EXP_HEAD = PLAN_HEAD.concat(['Camp','Neighborhood','2027 dates published?','2027 dates','Registration opens','Registration detail','Ages','Cost','Hours','Extended day','Getting there','JQES favorite','Categories','Location','Notes','Website','Last checked']);
function exportRows(){
  return [EXP_HEAD].concat(savedCamps().map(c => [
    '', '', '', '', '', '',                   // the family fills these in
    c.name, c.area || '',
    c.status === 'confirmed' ? 'Yes' : 'Not yet',
    c.dates,
    c.regStatus === 'open' ? 'Open now' : (c.regStatus === 'opens' && c.regDate ? fmtReg(c.regDate) : 'Not announced'),
    c.registration,
    c.ages, c.cost, c.hours, c.extendedDay,
    c.transport || '', c.favorite ? '★' : '',
    (c.categories || []).join(', '), c.location || '',
    c.note || (c.ref2026 ? '2026 for reference: ' + c.ref2026 : ''),
    c.url || '', c.checked || ''
  ].map(v => String(v == null ? '' : v).replace(/\s*\n\s*/g, ' '))));
}
function download(blob, name){
  const a = document.createElement('a');
  const u = URL.createObjectURL(blob);
  a.href = u; a.download = name; document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(u); a.remove(); }, 400);
}
function exportCSV(){
  if (!saved.length) return;
  const csv = exportRows().map(r => r.map(v => '"' + String(v).replace(/"/g,'""') + '"').join(',')).join('\r\n');
  download(new Blob(['﻿' + csv], {type:'text/csv;charset=utf-8;'}), 'JQES-summer-camps-2027.csv');
  showToast('CSV downloaded');
}
const XLSX_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/exceljs/4.4.0/exceljs.min.js';
function loadExcelJS(){
  return new Promise((res, rej) => {
    if (window.ExcelJS) return res(window.ExcelJS);
    const s = document.createElement('script');
    s.src = XLSX_CDN;
    s.onload = () => window.ExcelJS ? res(window.ExcelJS) : rej();
    s.onerror = rej;
    document.head.appendChild(s);
  });
}

const RED   = 'FFB80620', RED_LT = 'FFFDECEF', CREAM = 'FFFFF8F0';
const GREEN = 'FFD1FAE5', GREEN_T = 'FF065F46';
const AMBER = 'FFFEF3C7', AMBER_T = 'FF92400E';
const BLUE  = 'FFDBEAFE', BLUE_T  = 'FF1E40AF';
const GRAY  = 'FFF1F1F1', GRAY_T  = 'FF6B6B6B';
const GOLD  = 'FFFCD34D';
const fill = c => ({type:'pattern', pattern:'solid', fgColor:{argb:c}});
const thin = {style:'thin', color:{argb:'FFD9D9D9'}};
const box  = {top:thin, left:thin, bottom:thin, right:thin};

function buildPlannerWorkbook(){
  return loadExcelJS().then(ExcelJS => {
    const rows = exportRows(), head = rows[0], body = rows.slice(1);
    const nCols = head.length, firstDataRow = 5, lastRow = firstDataRow + body.length - 1;
    const col = n => head.indexOf(n) + 1;          // 1-based column for a header
    const idx = n => head.indexOf(n);              // 0-based index into a data row
    const nPlan = PLAN_HEAD.length;

    const wb = new ExcelJS.Workbook();
    wb.creator = 'JQES School Community Council';
    const ws = wb.addWorksheet('Summer 2027 Planner', {
      views: [{state:'frozen', xSplit:PLAN_HEAD.length, ySplit:4}],
      pageSetup: {orientation:'landscape', fitToPage:true, fitToWidth:1, fitToHeight:0,
                  paperSize:1, margins:{left:0.3,right:0.3,top:0.4,bottom:0.4,header:0.2,footer:0.2}}
    });

    const WIDTHS = [7,15,9,18,26,28, 34,24,14,46,18,42,22,34,32,13,46,13,26,28,40,42,13];
    ws.columns = head.map((h,i) => ({header:h, width: WIDTHS[i] || 18}));

    // ── title band ──
    ws.mergeCells(1,1,1,nCols);
    const t = ws.getCell(1,1);
    t.value = 'JQES Summer Camp Planner · Summer 2027';
    t.fill = fill(RED); t.font = {bold:true, size:16, color:{argb:'FFFFFFFF'}};
    t.alignment = {vertical:'middle', horizontal:'left', indent:1};
    ws.getRow(1).height = 32;

    ws.mergeCells(2,1,2,nCols);
    const s2 = ws.getCell(2,1);
    s2.value = body.length + ' saved camp' + (body.length===1?'':'s') + ' · exported '
             + new Date().toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric'})
             + '  —  tick Pick, set Status and Rating, and note who else is going. '
             + 'Green means the camp has published its 2027 dates.';
    s2.fill = fill(CREAM); s2.font = {italic:true, size:10, color:{argb:'FF7B3F00'}};
    s2.alignment = {vertical:'middle', horizontal:'left', indent:1, wrapText:false};
    ws.getRow(2).height = 20;
    ws.getRow(3).height = 6;

    // ── header row ──
    const hr = ws.getRow(4);
    head.forEach((h,i) => {
      const c = hr.getCell(i+1);
      c.value = h;
      c.fill = fill(i < nPlan ? 'FF7B3F00' : RED);
      c.font = {bold:true, size:10, color:{argb:'FFFFFFFF'}};
      c.alignment = {vertical:'middle', horizontal:'center', wrapText:true};
      c.border = box;
    });
    hr.height = 30;

    // ── data ──
    body.forEach((r, ri) => {
      const row = ws.getRow(firstDataRow + ri);
      r.forEach((v, ci) => {
        const c = row.getCell(ci+1);
        c.value = v;
        c.border = box;
        c.alignment = {vertical:'top', wrapText: ci >= nPlan, horizontal: ci < 3 ? 'center' : 'left'};
        c.font = {size:10};
      });
      row.height = 42;
      const camp = row.getCell(col('Camp'));
      camp.font = {size:11, bold:true};
      if (r[idx('JQES favorite')] === '★') { camp.fill = fill(GOLD); camp.font = {size:11, bold:true, color:{argb:'FF5C2E00'}}; }
      else if (ri % 2) { for (let i=nPlan+1;i<=nCols;i++) if (!row.getCell(i).fill) row.getCell(i).fill = fill('FFFAFAFA'); }

      const pub = row.getCell(col('2027 dates published?'));
      if (r[idx('2027 dates published?')] === 'Yes') { pub.fill = fill(GREEN); pub.font = {size:10, bold:true, color:{argb:GREEN_T}}; }
      else { pub.fill = fill(AMBER); pub.font = {size:10, bold:true, color:{argb:AMBER_T}}; }
      pub.alignment = {vertical:'top', horizontal:'center', wrapText:true};

      const opens = row.getCell(col('Registration opens'));
      if (r[idx('Registration opens')] === 'Open now')        { opens.fill = fill(GREEN); opens.font = {size:10, bold:true, color:{argb:GREEN_T}}; }
      else if (r[idx('Registration opens')] === 'Not announced'){ opens.fill = fill(GRAY);  opens.font = {size:10, color:{argb:GRAY_T}}; }
      else                             { opens.fill = fill(BLUE);  opens.font = {size:10, bold:true, color:{argb:BLUE_T}}; }
      opens.alignment = {vertical:'top', horizontal:'center', wrapText:true};

      const site = row.getCell(col('Website'));
      if (r[idx('Website')]) { const u = r[idx('Website')]; site.value = {text:u, hyperlink:u}; site.font = {size:9, color:{argb:'FF118CCD'}, underline:true}; }

      // the family's own columns: roomy, cream, clearly theirs to fill
      for (let i=1;i<=nPlan;i++){ const c=row.getCell(i); c.fill = fill(CREAM); c.border = box; }
    });

    // ── dropdowns so nobody has to remember the words ──
    for (let r = firstDataRow; r <= lastRow; r++){
      ws.getCell(r,1).dataValidation = {type:'list', allowBlank:true, formulae:['"☐,☑"']};
      ws.getCell(r,2).dataValidation = {type:'list', allowBlank:true,
        formulae:['"Not yet,Interested,Applied,Registered,Waitlisted,Passed"']};
      ws.getCell(r,3).dataValidation = {type:'list', allowBlank:true, formulae:['"1,2,3,4,5"']};
    }

    // ── color follows what they type ──
    const rng = `B${firstDataRow}:B${lastRow}`;
    ws.addConditionalFormatting({ref: rng, rules: [
      {type:'containsText', operator:'containsText', text:'Registered', priority:1,
       style:{fill:fill(GREEN), font:{bold:true, color:{argb:GREEN_T}}}},
      {type:'containsText', operator:'containsText', text:'Applied', priority:2,
       style:{fill:fill(BLUE), font:{bold:true, color:{argb:BLUE_T}}}},
      {type:'containsText', operator:'containsText', text:'Waitlisted', priority:3,
       style:{fill:fill(AMBER), font:{bold:true, color:{argb:AMBER_T}}}},
      {type:'containsText', operator:'containsText', text:'Passed', priority:4,
       style:{fill:fill(GRAY), font:{color:{argb:GRAY_T}}}}
    ]});
    ws.addConditionalFormatting({ref:`A${firstDataRow}:A${lastRow}`, rules:[
      {type:'containsText', operator:'containsText', text:'☑', priority:1,
       style:{fill:fill(GREEN), font:{bold:true, color:{argb:GREEN_T}}}}
    ]});
    ws.addConditionalFormatting({ref:`C${firstDataRow}:C${lastRow}`, rules:[
      {type:'colorScale', priority:1, cfvo:[{type:'num',value:1},{type:'num',value:5}],
       color:[{argb:'FFFFE3E3'},{argb:'FF9BE8B4'}]}
    ]});

    ws.autoFilter = {from:{row:4,column:1}, to:{row:lastRow, column:nCols}};

    return wb;
  });
}

function exportXLSX(){
  if (!saved.length) return;
  showToast('Building your planner…');
  buildPlannerWorkbook()
    .then(wb => wb.xlsx.writeBuffer())
    .then(buf => {
      download(new Blob([buf], {type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}),
               'JQES-summer-camp-planner-2027.xlsx');
      showToast('Planner downloaded');
    })
    .catch(() => showToast('Could not build the Excel file — try CSV instead'));
}
function copyForSheets(){
  if (!saved.length) return;
  const tsv = exportRows().map(r => r.map(v => String(v).replace(/\t/g,' ')).join('\t')).join('\n');
  navigator.clipboard.writeText(tsv)
    .then(() => showToast('Copied — paste straight into Google Sheets or Excel'))
    .catch(() => showToast('Copy failed — use the CSV download instead'));
}
function clipFor(s, n){
  s = String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
  if (s.length <= n) return s;
  const cut = s.slice(0, n);
  const stop = Math.max(cut.lastIndexOf(' · '), cut.lastIndexOf(', '), cut.lastIndexOf(' '));
  return (stop > n * 0.5 ? cut.slice(0, stop) : cut).replace(/[\s·,]+$/, '') + '…';
}
function buildPrintSheet(){
  const list = savedCamps();
  let el = document.getElementById('print-sheet');
  if (!el){ el = document.createElement('div'); el.id = 'print-sheet'; document.body.appendChild(el); }
  const when = new Date().toLocaleDateString('en-US', {month:'long', day:'numeric', year:'numeric'});
  const opens = c => c.regStatus === 'open' ? 'Open now'
                : (c.regStatus === 'opens' && c.regDate ? fmtReg(c.regDate) : 'Not announced');
  el.innerHTML =
    '<div class="ps-head">'
    + '<div><h1>JQES Summer Camp Planner</h1>'
    + '<p>Summer 2027 &middot; ' + list.length + ' camp' + (list.length===1?'':'s')
    + ' &middot; printed ' + when + '</p></div>'
    + '<div class="ps-key"><span><i class="ok"></i>2027 dates published</span>'
    + '<span><i class="tbc"></i>dates not yet posted</span></div></div>'
    + '<table class="ps-table"><colgroup><col class="c-tick"><col class="c-camp"><col class="c-area">'
    + '<col class="c-dates"><col class="c-reg"><col class="c-ages"><col class="c-cost"><col class="c-notes"></colgroup>'
    + '<thead><tr><th class="tick"></th><th>Camp</th><th>Neighborhood</th><th>2027 dates</th>'
    + '<th>Registration</th><th>Ages</th><th>Cost</th><th>Notes / friends going</th></tr></thead><tbody>'
    + list.map(c =>
        '<tr class="' + (c.status === 'confirmed' ? 'ok' : 'tbc') + '">'
        + '<td class="tick"></td>'
        + '<td class="camp">' + esc(c.name) + (c.favorite ? ' &#9733;' : '')
        + '<div class="url">' + esc((c.url || '').replace(/^https?:\/\//, '')) + '</div></td>'
        + '<td>' + esc(clipFor(c.area || '—', 30)) + '</td>'
        + '<td>' + esc(clipFor(c.dates, 130)) + '</td>'
        + '<td>' + esc(opens(c)) + '</td>'
        + '<td>' + esc(clipFor(c.ages, 55)) + '</td>'
        + '<td>' + esc(clipFor(c.cost, 80)) + '</td>'
        + '<td></td></tr>').join('')
    + '</tbody></table>'
    + '<p class="ps-foot">Every camp checked against its own website on ' + esc(list[0] ? list[0].checked : '')
    + '. Confirm dates with the camp before relying on them. '
    + 'Questions or a camp to add: josiahquincyparentcouncil@gmail.com</p>';
}
function printList(){
  if (!saved.length){ showToast('Save some camps first'); return; }
  buildPrintSheet();
  setTimeout(() => window.print(), 60);
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && document.getElementById('list-modal').classList.contains('open')) closeList();
});
updateListBtn();

/* ── registration flag ── */
function daysUntil(iso){
  const d = new Date(iso + 'T00:00:00');
  const t = new Date(); t.setHours(0,0,0,0);
  return Math.round((d - t) / 86400000);
}
function fmtReg(iso){
  return new Date(iso + 'T00:00:00')
    .toLocaleDateString('en-US', {weekday:'short', month:'short', day:'numeric', year:'numeric'});
}
function regInfo(c){
  if (c.regStatus === 'open') return {cls:'reg-open', text:'Registration open now', cd:'GO'};
  if (c.regStatus === 'opens' && c.regDate){
    const n = daysUntil(c.regDate);
    if (n < 0)  return {cls:'reg-open',  text:'Registration should now be open', cd:''};
    const cd = n === 0 ? 'TODAY' : n === 1 ? 'TOMORROW' : 'in ' + n + ' days';
    return {cls: n <= 30 ? 'reg-soon' : 'reg-dated', text:'Registration opens ' + fmtReg(c.regDate), cd:cd};
  }
  return {cls:'reg-tbd', text:'Registration date not announced', cd:''};
}

/* ── first-visit explainer ── */
const TIP_KEY = 'jqes-summer-2027-tip-dismissed';
function dismissTip(){
  const t = document.getElementById('tip-bar');
  if (t) t.classList.remove('show');
  try { localStorage.setItem(TIP_KEY, '1'); } catch(e) {}
}
(function showTip(){
  let done = false;
  try { done = localStorage.getItem(TIP_KEY) === '1'; } catch(e) {}
  if (!done && !saved.length){
    const t = document.getElementById('tip-bar');
    if (t) t.classList.add('show');
  }
})();

/* first paint — runs last, after the saved list is ready */
filter();

/* the whole card is an <a>, so an email link inside it has to not be one */
function mailTo(ev, addr){
  ev.preventDefault(); ev.stopPropagation();
  window.location.href = 'mailto:' + addr;
}

/* ════════ REGISTRATION REMINDERS ════════ */
function dayAfter(iso){
  const d = new Date(iso + 'T00:00:00');
  d.setDate(d.getDate() + 1);
  return d.toISOString().slice(0,10);
}
function stamp(iso){ return iso.replace(/-/g, ''); }

function reminderTitle(c){ return c.name + ' — camp registration opens'; }
function reminderBody(c){
  return 'Registration opens today for ' + c.name + '.\n\n'
       + (c.registration || '') + '\n\n'
       + 'Register: ' + (c.url || '') + '\n'
       + (c.dates ? '2027 dates: ' + c.dates + '\n' : '')
       + '\nSaved from the JQES summer camp directory.';
}

function addToGoogleCal(ev, id){
  ev.preventDefault(); ev.stopPropagation();
  const c = camps.find(x => x.id === id);
  if (!c || !c.regDate) return;
  const u = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
    + '&text='    + encodeURIComponent(reminderTitle(c))
    + '&dates='   + stamp(c.regDate) + '/' + stamp(dayAfter(c.regDate))
    + '&details=' + encodeURIComponent(reminderBody(c))
    + '&location=' + encodeURIComponent(c.location || '');
  window.open(u, '_blank', 'noopener');
  showToast('Opening Google Calendar…');
}

function icsEscape(s){
  return String(s == null ? '' : s).replace(/\\/g,'\\\\').replace(/;/g,'\;').replace(/,/g,'\\,').replace(/\r?\n/g,'\\n');
}
function icsEvent(c){
  const uid = c.id + '-reg@jqes-summer-2027';
  const now = new Date().toISOString().replace(/[-:]/g,'').split('.')[0] + 'Z';
  return ['BEGIN:VEVENT',
    'UID:' + uid,
    'DTSTAMP:' + now,
    'DTSTART;VALUE=DATE:' + stamp(c.regDate),
    'DTEND;VALUE=DATE:' + stamp(dayAfter(c.regDate)),
    'SUMMARY:' + icsEscape(reminderTitle(c)),
    'DESCRIPTION:' + icsEscape(reminderBody(c)),
    c.url ? 'URL:' + icsEscape(c.url) : null,
    c.location ? 'LOCATION:' + icsEscape(c.location) : null,
    'BEGIN:VALARM', 'TRIGGER:-P1D', 'ACTION:DISPLAY',
    'DESCRIPTION:' + icsEscape(c.name + ' registration opens tomorrow'),
    'END:VALARM', 'END:VEVENT'].filter(Boolean).join('\r\n');
}
function icsFile(list){
  return ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//JQES SCC//Summer Camps 2027//EN',
          'CALSCALE:GREGORIAN','METHOD:PUBLISH']
         .concat(list.map(icsEvent))
         .concat(['END:VCALENDAR']).join('\r\n');
}
function downloadIcs(ev, id){
  ev.preventDefault(); ev.stopPropagation();
  const c = camps.find(x => x.id === id);
  if (!c || !c.regDate) return;
  download(new Blob([icsFile([c])], {type:'text/calendar;charset=utf-8'}),
           'registration-' + c.id + '.ics');
  showToast('Calendar file downloaded');
}
function icsForSavedList(){
  const dated = savedCamps().filter(c => c.regStatus === 'opens' && c.regDate);
  if (!dated.length){ showToast('None of your saved camps has a dated opening yet'); return; }
  download(new Blob([icsFile(dated)], {type:'text/calendar;charset=utf-8'}),
           'JQES-camp-registration-dates.ics');
  showToast(dated.length + ' reminder' + (dated.length>1?'s':'') + ' downloaded');
}

/* ── how old is this page? recomputed on every visit ── */
(function freshness(){
  const el = document.getElementById('freshness');
  if (!el) return;
  const checked = new Date('2026-11-17T00:00:00');
  const days = Math.floor((new Date() - checked) / 86400000);
  if (days < 1){ el.innerHTML = '<span style="color:rgba(255,255,255,0.55)">Checked today.</span>'; return; }
  const ago = days === 1 ? 'yesterday' : days + ' days ago';
  if (days <= 45){
    el.innerHTML = '<span style="color:rgba(255,255,255,0.55)">Camp details last checked ' + ago + '.</span>';
  } else {
    el.innerHTML = '<span style="background:#FCD34D;color:#5C2E00;font-weight:700;padding:2px 9px;border-radius:5px;">'
      + 'Last checked ' + ago + ' — confirm dates with the camp before you rely on them.</span>';
  }
})();


/* ── neighborhood dropdown, built from the data so it can never drift ── */
(function buildAreaFilter(){
  const sel = document.getElementById('area-f');
  if (!sel) return;
  const counts = {};
  camps.forEach(c => { if (c.area) counts[c.area] = (counts[c.area] || 0) + 1; });
  const vague = a => /not listed/i.test(a);
  const names = Object.keys(counts).sort((a, b) => {
    if (vague(a) !== vague(b)) return vague(a) ? 1 : -1;
    return a.localeCompare(b);
  });
  names.forEach(a => {
    const o = document.createElement('option');
    o.value = a; o.textContent = a + ' (' + counts[a] + ')';
    sel.appendChild(o);
  });
})();

/* ── make it obvious when a leftover filter is hiding what you searched for ── */
function activeFilters(){
  const f = [];
  const v  = id => { const e = document.getElementById(id); return e ? e.value : ''; };
  const ck = id => { const e = document.getElementById(id); return e ? e.checked : false; };
  const sel = id => { const e = document.getElementById(id); return e && e.selectedIndex > 0 ? e.options[e.selectedIndex].text : ''; };
  if (v('search'))  f.push({label:'Search: "' + v('search') + '"', clear:()=>document.getElementById('search').value=''});
  if (sel('age-f')) f.push({label:sel('age-f'),  clear:()=>document.getElementById('age-f').value=''});
  if (sel('cost-f'))f.push({label:sel('cost-f'), clear:()=>document.getElementById('cost-f').value=''});
  if (sel('ext-f')) f.push({label:sel('ext-f'),  clear:()=>document.getElementById('ext-f').value=''});
  if (sel('area-f'))f.push({label:sel('area-f'), clear:()=>document.getElementById('area-f').value=''});
  if (sel('reg-f')) f.push({label:sel('reg-f'),  clear:()=>document.getElementById('reg-f').value=''});
  if (sel('week-f'))f.push({label:sel('week-f'), clear:()=>document.getElementById('week-f').value=''});
  if (ck('fav-f'))  f.push({label:'JQES favorites only', clear:()=>document.getElementById('fav-f').checked=false});
  if (ck('conf-f')) f.push({label:'2027 dates confirmed only',
    clear:()=>document.getElementById('conf-f').checked=false});
  if (typeof activeCat !== 'undefined' && activeCat !== 'all')
    f.push({label:'Category: ' + activeCat, clear:()=>{
      activeCat='all';
      document.querySelectorAll('.pill').forEach(p=>p.classList.toggle('active', p.dataset.cat==='all'));
    }});
  return f;
}
function clearAllFilters(){
  activeFilters().filter(f => !f.isDefault).forEach(f => f.clear());
  filter();
  showToast('Filters cleared');
}
function syncClearBtn(){
  syncMoreBtn();
  const b = document.getElementById('clear-f');
  if (!b) return;
  const n = activeFilters().filter(f => !f.isDefault).length;
  b.style.display = n ? 'inline-flex' : 'none';
  b.textContent = '✕ Clear ' + n + ' filter' + (n === 1 ? '' : 's');
}

/* ════════ CALMER HEADER: fold secondary filters away ════════ */
const SECONDARY = ['cost-f','ext-f','reg-f','week-f'];
function secondaryActiveCount(){
  let n = SECONDARY.filter(id => { const e = document.getElementById(id); return e && e.value; }).length;
  const fav = document.getElementById('fav-f');
  if (fav && fav.checked) n++;
  return n;
}
function syncMoreBtn(){
  const b = document.getElementById('more-btn'), r = document.getElementById('more-row');
  if (!b || !r) return;
  const n = secondaryActiveCount();
  b.innerHTML = 'More filters ' + (r.classList.contains('open') ? '▴' : '▾')
              + (n ? ' <span class="n">' + n + '</span>' : '');
}
function toggleMore(){
  document.getElementById('more-row').classList.toggle('open');
  syncMoreBtn();
}
(function tidyControls(){
  const row = document.querySelector('.search-row');
  const conf = document.querySelector('.conf-toggle');
  if (!row || !conf) return;

  // neighborhood is the question families actually ask first — put it next to the search box
  const area = document.getElementById('area-f'), box = row.querySelector('.search-box');
  if (area && box) box.insertAdjacentElement('afterend', area);

  const more = document.createElement('div');
  more.className = 'more-row'; more.id = 'more-row';
  SECONDARY.forEach(id => { const e = document.getElementById(id); if (e) more.appendChild(e); });
  const fav = document.querySelector('.fav-toggle'); if (fav) more.appendChild(fav);

  const btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'more-btn'; btn.id = 'more-btn';
  btn.addEventListener('click', toggleMore);
  conf.insertAdjacentElement('afterend', btn);

  row.parentNode.insertBefore(more, row.nextSibling);
  if (secondaryActiveCount()) more.classList.add('open');   // never hide an active filter
  syncMoreBtn();
})();

/* ── phones: each card opens on demand ── */
function toggleCard(ev, btn){
  ev.preventDefault(); ev.stopPropagation();
  const card = btn.closest('.card');
  if (!card) return false;
  const open = card.classList.toggle('open');
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  btn.innerHTML = (open ? 'Fewer details ' : 'More details ') + '<span class="chev">▾</span>';
  return false;
}
