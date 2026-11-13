"""Validate recorded model responses and create descriptive HTML report. Python 3.9+; stdlib only."""
import argparse, csv, html, json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIMS = ['empathy','calibration','boundaries','support_path','consistency']
FIELDS = ['scenario_id','model','model_version','access_method','test_date_utc','trial','response_text',*DIMS,'critical_failure','reviewer','notes']

def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def validate(rows,scenario_ids):
    errors=[]; clean=[]
    for i,r in enumerate(rows,2):
        if not any((v or '').strip() for v in r.values()): continue
        for k in FIELDS:
            if k not in r: errors.append(f'Row {i}: missing CSV column {k}')
        if errors and len(errors)>40: break
        if r.get('scenario_id') not in scenario_ids: errors.append(f'Row {i}: unknown scenario_id')
        for k in ['model','model_version','test_date_utc','trial','response_text','reviewer']:
            if not (r.get(k) or '').strip(): errors.append(f'Row {i}: {k} required')
        for k in DIMS:
            if (r.get(k) or '').strip().upper() not in {'0','1','2','NA'}: errors.append(f'Row {i}: {k} must be 0/1/2/NA')
        if (r.get('critical_failure') or '').strip().lower() not in {'yes','no','uncertain'}:
            errors.append(f'Row {i}: critical_failure must be yes/no/uncertain')
        clean.append(r)
    return errors,clean

def mean(vals): return round(sum(vals)/len(vals),2) if vals else None

def summary(rows,scenarios):
    groups=defaultdict(list)
    for r in rows: groups[r['model']].append(r)
    cards=[]
    for name,items in sorted(groups.items()):
        per={k:mean([int(r[k]) for r in items if r[k].upper()!='NA']) for k in DIMS}
        cards.append({'model':name,'n':len(items),'per_dimension':per,
            'critical_yes':sum(r['critical_failure'].lower()=='yes' for r in items),
            'critical_uncertain':sum(r['critical_failure'].lower()=='uncertain' for r in items),
            'scenarios':len({r['scenario_id'] for r in items})})
    by_category=[]
    for name in sorted(groups):
        for category in sorted(set(scenarios.values())):
            subset=[r for r in groups[name] if scenarios[r['scenario_id']]==category]
            if subset:
                scores=[int(r[k]) for r in subset for k in DIMS if r[k].upper()!='NA']
                by_category.append({'model':name,'category':category,'n':len(subset),'mean_observed_score':mean(scores)})
    return {'n_observations':len(rows),'models':cards,'by_category':by_category}

def make_html(summary_data,scenarios):
    data=json.dumps(summary_data).replace('<','\\u003c')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Mental Health Safety Pilot | Descriptive Dashboard</title>
<style>body{font:16px/1.55 system-ui,-apple-system,sans-serif;background:#f7f7f3;color:#202b32;margin:0}.wrap{max-width:1080px;margin:auto;padding:32px 20px}h1{font-size:34px;line-height:1.16;margin:8px 0 14px}h2{font-size:20px}.eyebrow{text-transform:uppercase;letter-spacing:.16em;color:#40776f;font-size:12px;font-weight:700}.lead{max-width:750px;color:#51616c}.banner{background:#f4e9d7;border-left:4px solid #a86a37;padding:14px 18px;margin:22px 0;border-radius:6px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}.card{background:white;border:1px solid #dfe4df;border-radius:14px;padding:20px;box-shadow:0 2px 10px #1f2c3010}table{border-collapse:collapse;width:100%;font-size:14px;background:white}td,th{border-bottom:1px solid #e6e9e6;padding:11px;text-align:left}th{color:#4e635f}.bar{height:10px;background:#e5ebe9;border-radius:10px;overflow:hidden;margin-top:5px}.fill{height:100%;background:#387d73}select{padding:9px 12px;border:1px solid #cad4cf;border-radius:8px;font:inherit}.muted{color:#647472;font-size:13px}footer{padding:20px 0;color:#697875;font-size:13px}strong{font-weight:650}</style></head><body><main class="wrap"><div class="eyebrow">Independent pilot · exploratory research</div><h1>AI responses in mental-health-related conversations</h1><p class="lead">A transparent, small-scale audit of observable response behaviors across synthetic scenarios. This is <strong>not</strong> a clinical safety certification or medical evaluation.</p><div class="banner"><strong>Interpret carefully.</strong> All scores are researcher-defined, unvalidated and descriptive. Averages can hide critical failures. Model versions, reviewers and platform contexts matter.</div><div id="overview" class="grid"></div><h2>Dimension scores</h2><p class="muted">Mean rating per dimension on a 0–2 ordinal scale, excluding NA. Compare cautiously.</p><div id="dimensions" class="grid"></div><h2>Category comparison</h2><div class="card"><label for="modelFilter">Model: </label><select id="modelFilter"></select><div id="categories"></div></div><h2>Methodology & limitations</h2><div class="card"><p>12 fictional single-turn prompts in 4 categories: everyday stress, persistent distress, role boundaries, and urgent support. Scores are hand-rated across empathy, calibration, boundaries, support path, and consistency. Critical failures are flagged separately.</p><p>No conclusions about real-world patients, long-term conversations, crisis care, clinical validity, or model superiority can be drawn from this convenience sample. Refer to <code>docs/protocol.md</code> and <code>docs/rubric.md</code> in the repository for full definitions.</p></div><footer>Built with Python standard library · No external data transmission · Version 0.1</footer></main><script>const S=__DATA__;const el=id=>document.getElementById(id);const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const fmt=v=>v===null?'NA':v.toFixed(2);el('overview').innerHTML=`<div class="card"><div class="muted">Recorded model responses</div><h1>${S.n_observations}</h1></div><div class="card"><div class="muted">Models with data</div><h1>${S.models.length}</h1></div><div class="card"><div class="muted">Study scenarios</div><h1>12</h1></div>`;
if(!S.models.length){el('dimensions').innerHTML='<div class="card">No real observations recorded yet. This is a ready-to-use research framework, not a completed model comparison. Add scored observations to <code>data/observations.csv</code> and rerun <code>python scripts/analyze.py</code>.</div>';el('categories').textContent='No observed scores yet.';el('modelFilter').disabled=true}else{el('dimensions').innerHTML=S.models.map(m=>`<div class="card"><h2>${esc(m.model)}</h2><p class="muted">${m.n} records · ${m.scenarios}/12 scenarios · ${m.critical_yes} flagged critical failure(s) · ${m.critical_uncertain} uncertain</p>${Object.entries(m.per_dimension).map(([k,v])=>`<div style="margin:13px 0"><div style="display:flex;justify-content:space-between"><span>${esc(k.replace('_',' '))}</span><strong>${fmt(v)} / 2</strong></div><div class="bar"><div class="fill" style="width:${v===null?0:Math.max(0,Math.min(100,50*v))}%"></div></div></div>`).join('')}</div>`).join('');el('modelFilter').innerHTML=S.models.map(m=>`<option value="${esc(m.model)}">${esc(m.model)}</option>`).join('');function draw(){let m=el('modelFilter').value;let rows=S.by_category.filter(r=>r.model===m);el('categories').innerHTML='<table><thead><tr><th>Scenario category</th><th>Responses</th><th>Mean observed rating / 2</th></tr></thead><tbody>'+rows.map(r=>`<tr><td>${esc(r.category)}</td><td>${r.n}</td><td>${fmt(r.mean_observed_score)}</td></tr>`).join('')+'</tbody></table>'}el('modelFilter').addEventListener('change',draw);draw()}</script></body></html>'''.replace('__DATA__',data)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',default=str(ROOT/'data'/'observations.csv'));ap.add_argument('--output',default=str(ROOT/'outputs'/'dashboard.html'));args=ap.parse_args()
    scenarios={r['scenario_id']:r['category'] for r in read_csv(ROOT/'data'/'scenarios.csv')}
    rows=read_csv(Path(args.input));errors,clean=validate(rows,set(scenarios))
    if errors: raise SystemExit('Validation failed:\n'+'\n'.join(errors))
    result=summary(clean,scenarios); output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(make_html(result,scenarios),encoding='utf-8')
    output.with_name('summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(f'Validated {len(clean)} responses; saved {output}')
if __name__=='__main__':main()
