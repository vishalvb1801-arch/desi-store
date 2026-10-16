import json, re
from PIL import ImageFont
FPS=30
P=json.load(open('plan.json')); fr=P['frames']
LT=json.load(open('../work/lt_matched.json'))['LT']
lines=[l.rstrip('\n').split('\t') for l in open('../work/lines.tsv')]
OVR=json.load(open('../work/phrase_overrides.json'))
meta={m['line']:m for m in json.load(open('render_meta.json'))}
src=open('../work/align.py').read(); exec(src[src.index('ONES='):src.index('W = json')]); exec(src[src.index('def norm_tokens'):src.index('# whisper token stream')])
font=ImageFont.truetype('../work/fonts/Montserrat-ExtraBold.ttf',64); MAXW=920
def fwd(t):
    sh=0
    for c in P['cuts']:
        if t>=c['inn']: sh+=c['removed']
        elif t>c['out']: return c['out']-sh
    return t-sh
YPOS={25:620,31:210,59:810,3:1450,9:1450,46:1450,57:1450}
split58=(fr[57]+meta[58]['parts'][0]['frames'])/FPS   # clip 58 -> hero cut
GOLD='&H0037A5D4&'; CREAM='&H00E0F4FF&'; CRIMSON='&H00080A77'
def ts(t):
    cs=int(round(t*100)); return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"
FUNC=set("a an the to of in on at for from and my his her our your their i he she we they by with into till but like that was is".split())
events=[]; dump=[]
for li,l in enumerate(lines):
    lstart=fr[li]/FPS; lend=fr[li+1]/FPS
    toks=[dict(t) for t in LT if t['line']==li]
    known=[k for k,t in enumerate(toks) if 's' in t]
    if known[0]>0:
        k0=known[0]; s0,e0=toks[k0]['s'],toks[k0]['e']; st=(e0-s0)/(k0+1)
        for k in range(k0+1): toks[k]['s']=s0+k*st; toks[k]['e']=s0+(k+1)*st
    for k,t in enumerate(toks):
        if 's' in t: continue
        a=max(j for j in range(k) if 's' in toks[j]); b=[j for j in range(k+1,len(toks)) if 's' in toks[j]]
        ta=toks[a]['e']; 
        if b: tb=toks[b[0]]['s']; sp=(tb-ta)/(b[0]-a)
        else: sp=0.3
        t['s']=ta+sp*(k-a-1); t['e']=t['s']+sp*0.9
    for t in toks: t['s']=fwd(t['s']); t['e']=fwd(t['e'])
    # line-first word starts at the stem-measured vocal onset (= the picture cut)
    if li>0:
        d=max(0.12,toks[0]['e']-toks[0]['s']); toks[0]['s']=lstart; toks[0]['e']=max(toks[0]['e'],lstart+min(d,0.5))
    words=l[3].split(); wt=[]; k=0
    for w in words:
        n=len(norm_tokens(w)); g=toks[k:k+n]; k+=n; wt.append([w,g[0]['s'],g[-1]['e']])
    for j,x in enumerate(wt):
        x[1]=max(x[1],lstart if j==0 else wt[j-1][1]); x[1]=min(x[1],lend-0.08)
        x[2]=min(max(x[2],x[1]+0.12),lend)
    for j in range(len(wt)-1):
        if wt[j+1][1]>wt[j][1]: wt[j][2]=min(wt[j][2],wt[j+1][1])
    # phrases
    nW=len(wt); best=[1e9]*(nW+1); prv=[0]*(nW+1); best[0]=0
    for j in range(1,nW+1):
        for k in range(max(0,j-4),j):
            grp=wt[k:j]; txt=' '.join(g[0] for g in grp)
            if font.getlength(txt)>MAXW: continue
            last=grp[-1][0]; ln=re.sub(r"[^a-z']","",last.lower()); c=0
            if len(grp)==1: c+=6
            if j<nW and not re.search(r'[,.?!"]$',last): c+=3
            if j<nW and ln in FUNC: c+=6
            for g in grp[:-1]:
                if re.search(r'[,.?!]"?$',g[0]): c+=4
            c+=0.5*abs(len(grp)-3)
            if best[k]+c<best[j]: best[j]=best[k]+c; prv[j]=k
    phrases=[]; j=nW
    while j>0: phrases.insert(0,wt[prv[j]:j]); j=prv[j]
    if str(li+1) in OVR:
        parts=[p.split() for p in OVR[str(li+1)].split('|')]; phrases=[]; k=0
        for p in parts: phrases.append(wt[k:k+len(p)]); k+=len(p)
    y=YPOS.get(li+1,1300)
    for pi,ph in enumerate(phrases):
        st=ph[0][1]; en=ph[-1][2]+0.30
        nxt=phrases[pi+1][0][1] if pi+1<len(phrases) else lend
        if nxt-en<0.5: en=nxt
        en=min(en,nxt,lend)
        def kara(ev):
            txt=''; t=ev
            for idx,(w,s,e) in enumerate(ph):
                sep=' ' if idx<len(ph)-1 else ''
                if e<=ev: txt+=f"{{\\k0\\1c{CREAM}}}{w}"+sep; continue
                if s>t+0.005: txt+=f"{{\\k{int(round((s-t)*100))}}}"; t=s
                d=max(1,int(round((e-t)*100))); off=int(round((t-ev)*1000))+d*10
                txt+=f"{{\\k{d}\\1c{GOLD}\\t({off},{off+1},\\1c{CREAM})}}{w}"+sep; t+=d/100
            return txt
        spans=[(st,en,y)]
        if li+1==58:
            if st>=split58: spans=[(st,en,210)]
            elif en>split58: spans=[(st,split58,y),(split58,en,210)]
        spans=[sp for sp in spans if sp[1]-sp[0]>=0.05]
        for a,b,yy in spans:
            events.append(f"Dialogue: 0,{ts(a)},{ts(b)},EIS,,0,0,0,,{{\\an5\\pos(540,{yy})}}{kara(a)}")
            dump.append(dict(line=li+1,start=round(a,3),end=round(b,3),y=yy,text=' '.join(w for w,_,_ in ph),words=[(w,round(s,2),round(e,2)) for w,s,e in ph]))
hdr=f"""[Script Info]
Title: C299-A v2 EIS sung-story captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: EIS,Montserrat ExtraBold,64,{GOLD[:-1]},{CREAM[:-1]},{CRIMSON},{CRIMSON},0,0,0,0,100,100,0,0,3,14,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open('C299-A_v2.ass','w').write(hdr+'\n'.join(events)+'\n')
json.dump(dump,open('phrases_v2.json','w'),indent=0)
# check: at every picture cut, the caption on screen is the new line's first phrase
bad=[]
for li in range(1,60):
    t=fr[li]/FPS+0.04
    on=[d for d in dump if d['start']<=t<d['end']]
    if not on or on[0]['line']!=li+1: bad.append((li+1,round(t,2),[(d['line'],d['text']) for d in on]))
print(len(events),'events; cut/caption mismatches:',bad)
