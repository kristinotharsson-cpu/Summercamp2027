
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
const EXP_HEAD = ['Camp','2027 dates','2027 dates published?','Registration opens','Registration detail','Ages','Cost','Hours','Extended day','Categories','Neighborhood','Location','Getting there','JQES favorite','Notes','Website','Last checked'];
function exportRows(){
  return [EXP_HEAD].concat(savedCamps().map(c => [
    c.name, c.dates,
    c.status === 'confirmed' ? 'Yes' : 'Not yet',
    c.regStatus === 'open' ? 'Open now' : (c.regStatus === 'opens' && c.regDate ? fmtReg(c.regDate) : 'Not announced'),
    c.registration,
    c.ages, c.cost, c.hours, c.extendedDay,
    (c.categories || []).join(', '), c.area || '', c.location || '',
    c.transport || '', c.favorite ? 'Yes' : '',
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
function loadXLSX(){
  return new Promise((res, rej) => {
    if (window.XLSX) return res(window.XLSX);
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
    s.onload = () => window.XLSX ? res(window.XLSX) : rej();
    s.onerror = rej;
    document.head.appendChild(s);
  });
}
function exportXLSX(){
  if (!saved.length) return;
  showToast('Building Excel file…');
  loadXLSX().then(XLSX => {
    const rows = exportRows();
    const ws = XLSX.utils.aoa_to_sheet(rows);
    ws['!cols'] = [{wch:34},{wch:46},{wch:20},{wch:20},{wch:44},{wch:22},{wch:34},{wch:32},{wch:13},{wch:24},{wch:28},{wch:26},{wch:50},{wch:14},{wch:46},{wch:42},{wch:14}];
    ws['!autofilter'] = {ref: XLSX.utils.encode_range({s:{r:0,c:0}, e:{r:rows.length-1, c:EXP_HEAD.length-1}})};
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Summer 2027');
    XLSX.writeFile(wb, 'JQES-summer-camps-2027.xlsx');
    showToast('Excel file downloaded');
  }).catch(() => showToast('Could not load the Excel library — try CSV instead'));
}
function copyForSheets(){
  if (!saved.length) return;
  const tsv = exportRows().map(r => r.map(v => String(v).replace(/\t/g,' ')).join('\t')).join('\n');
  navigator.clipboard.writeText(tsv)
    .then(() => showToast('Copied — paste straight into Google Sheets or Excel'))
    .catch(() => showToast('Copy failed — use the CSV download instead'));
}
function printList(){ if (saved.length) window.print(); }

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
  if (ck('conf-f')) f.push({label:'2027 dates confirmed only', clear:()=>document.getElementById('conf-f').checked=false});
  if (typeof activeCat !== 'undefined' && activeCat !== 'all')
    f.push({label:'Category: ' + activeCat, clear:()=>{
      activeCat='all';
      document.querySelectorAll('.pill').forEach(p=>p.classList.toggle('active', p.dataset.cat==='all'));
    }});
  return f;
}
function clearAllFilters(){
  activeFilters().forEach(f => f.clear());
  filter();
  showToast('Filters cleared');
}
function syncClearBtn(){
  syncMoreBtn();
  const b = document.getElementById('clear-f');
  if (!b) return;
  const n = activeFilters().length;
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
