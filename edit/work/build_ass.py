import json, re
from PIL import ImageFont
FPS=30
lines=[l.rstrip('\n').split('\t') for l in open('lines.tsv')]
LT=json.load(open('lt_matched.json'))['LT']
LS=json.load(open('line_starts.json')); fr=LS['frames']
exec(open('align.py').read().split('# whisper token stream')[0].split('W = json')[0])  # norm_tokens, num2words
src=open('align.py').read(); exec(src[src.index('def norm_tokens'):src.index('# whisper token stream')])
font=ImageFont.truetype('fonts/Montserrat-ExtraBold.ttf',64)
MAXW=920
OVR=json.load(open('phrase_overrides.json'))
YPOS={25:620,31:210,59:810, 3:1450,9:1450,46:1450,57:1450}
# in-clip camera cut on line 58 at 221.167s: bottle fills the left half from top to bottom -> move above the label
YSPLIT={58:(221.167,215)}
YPOS.update(json.load(open('ypos_override.json')) if __import__('os').path.exists('ypos_override.json') else {})
YPOS={int(k):v for k,v in YPOS.items()}
GOLD='&H0037A5D4&'; CREAM='&H00E0F4FF&'
def ts(t):
    cs=int(round(t*100)); h=cs//360000; m=cs//6000%60; s=cs//100%60; c=cs%100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"
events=[]; dump=[]
tok_i=0
for li,l in enumerate(lines):
    lstart=fr[li]/FPS; lend=fr[li+1]/FPS
    toks=[t for t in LT if t['line']==li]
    # interpolate unmatched token times inside the line
    known=[(k,t['s'],t['e']) for k,t in enumerate(toks) if 's' in t]
    if known and known[0][0]>0:   # leading unmatched words share the first matched word's span
        k0,s0,e0=known[0]; step=(e0-s0)/(k0+1)
        for k in range(k0+1): toks[k]['s']=s0+k*step; toks[k]['e']=s0+(k+1)*step
        known=[(k,t['s'],t['e']) for k,t in enumerate(toks) if 's' in t]
    for k,t in enumerate(toks):
        if 's' in t: continue
        prev=[x for x in known if x[0]<k]; nxt=[x for x in known if x[0]>k]
        a=(prev[-1][0],prev[-1][2]) if prev else (-1,lstart)
        b=(nxt[0][0],nxt[0][1]) if nxt else (len(toks),min(lend, a[1]+0.35*(len(toks)-a[0])))
        span=(b[1]-a[1])/(b[0]-a[0]); t['s']=a[1]+span*(k-a[0]); t['e']=t['s']+span*0.9; t['interp']=True
    words=l[3].split()
    wt=[]; k=0
    for w in words:
        n=len(norm_tokens(w)); grp=toks[k:k+n]; k+=n
        s=grp[0]['s'] if grp else (wt[-1][2] if wt else lstart)
        e=grp[-1]['e'] if grp else s+0.2
        wt.append([w,s,e])
    assert k==len(toks)
    # clamp words inside the line and keep them ordered
    for j,x in enumerate(wt):
        x[1]=max(x[1],lstart if j==0 else wt[j-1][1]); x[1]=min(x[1],lend-0.05)
        x[2]=min(max(x[2],x[1]+0.12), lend)
    for j in range(len(wt)-1): wt[j][2]=min(wt[j][2], wt[j+1][1]) if wt[j+1][1]>wt[j][1] else wt[j][2]
    # chunk into 2-4 word phrases (DP): fit width, break at punctuation, never end on a function word
    FUNC=set("a an the to of in on at for from and my his her our your their i he she we they by with into till but like that was is".split())
    nW=len(wt); best=[1e9]*(nW+1); prv=[0]*(nW+1); best[0]=0
    for j in range(1,nW+1):
        for k in range(max(0,j-4),j):
            grp=wt[k:j]; txt=' '.join(g[0] for g in grp)
            if font.getlength(txt)>MAXW: continue
            c=0
            last=grp[-1][0]; lastn=re.sub(r"[^a-z']","",last.lower())
            if len(grp)==1: c+=6
            if j<nW and not re.search(r'[,.?!"]$',last): c+=3
            if j<nW and lastn in FUNC: c+=6
            for g in grp[:-1]:
                if re.search(r'[,.?!]"?$',g[0]): c+=4      # punctuation inside a phrase
            if j<nW and wt[j][1]-grp[-1][2]>0.6: c-=2           # natural pause
            c+=0.5*abs(len(grp)-3)
            if best[k]+c<best[j]: best[j]=best[k]+c; prv[j]=k
    phrases=[]; j=nW
    while j>0: phrases.insert(0,wt[prv[j]:j]); j=prv[j]
    if str(li+1) in OVR:
        parts=[p.split() for p in OVR[str(li+1)].split('|')]
        assert [w for p in parts for w in p]==[x[0] for x in wt], (li+1, parts)
        phrases=[]; k=0
        for p in parts: phrases.append(wt[k:k+len(p)]); k+=len(p)
    for ph in phrases:
        wpx=font.getlength(' '.join(x[0] for x in ph))
        if wpx>MAXW: print('WIDE', li+1, ' '.join(x[0] for x in ph), int(wpx))
    y=YPOS.get(li+1,1300)
    for p_i,ph in enumerate(phrases):
        st=ph[0][1]; en=ph[-1][2]+0.30
        nxt=phrases[p_i+1][0][1] if p_i+1<len(phrases) else lend
        if nxt-en<0.5: en=nxt                # avoid flicker between close phrases
        en=min(en,nxt,lend)
        def kara(ev_st):
            txt=''; t=ev_st
            for idx,(w,s,e) in enumerate(ph):
                sep=' ' if idx<len(ph)-1 else ''
                if e<=ev_st: txt+=f"{{\\k0\\1c{CREAM}}}{w}"+sep; continue
                if s>t+0.005: txt+=f"{{\\k{int(round((s-t)*100))}}}"; t=s
                d=max(1,int(round((e-t)*100))); off=int(round((t-ev_st)*1000))+d*10
                txt+=f"{{\\k{d}\\1c{GOLD}\\t({off},{off+1},\\1c{CREAM})}}{w}"+sep
                t+=d/100
            return txt
        spans=[(st,en,y)]
        if li+1 in YSPLIT:
            tc,y2=YSPLIT[li+1]
            if st>=tc: spans=[(st,en,y2)]
            elif en>tc: spans=[(st,tc,y),(tc,en,y2)]
        for a_,b_,yy in spans:
            events.append(f"Dialogue: 0,{ts(a_)},{ts(b_)},EIS,,0,0,0,,{{\\an5\\pos(540,{yy})}}{kara(a_)}")
            dump.append(dict(line=li+1,start=round(a_,3),end=round(b_,3),y=yy,text=' '.join(w for w,_,_ in ph)))
hdr=f"""[Script Info]
Title: C299-A EIS sung-story captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: EIS,Montserrat ExtraBold,64,{GOLD[:-1]},{CREAM[:-1]},&H002B1F7A,&H002B1F7A,0,0,0,0,100,100,0,0,3,14,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open('/home/user/desi-store/edit/C299-A.ass','w').write(hdr+'\n'.join(events)+'\n')
json.dump(dump,open('phrases.json','w'),indent=0)
print(len(events),'phrases')
