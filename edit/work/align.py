import json, re, sys, csv
from rapidfuzz import fuzz
ONES="zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS="_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
def num2words(n):
    if n<20: return ONES[n]
    if n<100: return TENS[n//10]+('' if n%10==0 else '-'+ONES[n%10])
    if n<1000: return ONES[n//100]+' hundred'+('' if n%100==0 else ' '+num2words(n%100))
    return ' '.join(ONES[int(c)] for c in str(n))
W = json.load(open(sys.argv[1]))
AUDIO = float(sys.argv[2])
lines = [l.rstrip('\n').split('\t') for l in open('lines.tsv')]
def norm_tokens(text):
    text = text.replace("’","'").lower()
    out=[]
    for raw in re.split(r"[\s\-–—]+", text):
        t = re.sub(r"[^a-z0-9']", "", raw).strip("'")
        if not t: continue
        if t.isdigit():
            out += [x for x in re.split(r"[\s\-]+", num2words(int(t)).replace(',', '')) if x and x!='and']
        else: out.append(t)
    return out
# whisper token stream with times (split multi-token words evenly)
WT=[]
for w in W:
    toks = norm_tokens(w['w'])
    if not toks: continue
    d = (w['e']-w['s'])/len(toks)
    for k,t in enumerate(toks): WT.append(dict(t=t, s=w['s']+k*d, e=w['s']+(k+1)*d, p=w['p']))
# lyric tokens
LT=[]
for li,l in enumerate(lines):
    for t in norm_tokens(l[3]): LT.append(dict(t=t, line=li))
def sim(a,b):
    r = fuzz.ratio(a,b)
    return r
n, m = len(LT), len(WT)
GAP=-0.6
import numpy as np
S = np.zeros((n+1,m+1)); B = np.zeros((n+1,m+1),dtype=np.int8)
S[1:,0] = GAP*np.arange(1,n+1); S[0,1:] = GAP*np.arange(1,m+1); B[1:,0]=1; B[0,1:]=2
sc = np.zeros((n,m))
for i in range(n):
    for j in range(m):
        r = sim(LT[i]['t'], WT[j]['t'])
        sc[i,j] = 1.0 if r>=85 else (0.4 if r>=65 else -1.0)
for i in range(1,n+1):
    for j in range(1,m+1):
        a=S[i-1,j-1]+sc[i-1,j-1]; b=S[i-1,j]+GAP; c=S[i,j-1]+GAP
        if a>=b and a>=c: S[i,j]=a; B[i,j]=0
        elif b>=c: S[i,j]=b; B[i,j]=1
        else: S[i,j]=c; B[i,j]=2
i,j=n,m; match={}
while i>0 or j>0:
    if B[i,j]==0:
        if sc[i-1,j-1]>0: match[i-1]=j-1
        i-=1; j-=1
    elif B[i,j]==1: i-=1
    else: j-=1
for k,t in enumerate(LT):
    if k in match: t['s']=WT[match[k]]['s']; t['e']=WT[match[k]]['e']; t['wt']=WT[match[k]]['t']
json.dump(dict(LT=LT), open('lt_matched.json','w'))
# per-line report
rep=[]
for li,l in enumerate(lines):
    toks=[t for t in LT if t['line']==li]
    mt=[ (k,t) for k,t in enumerate(toks) if 's' in t]
    frac=len(mt)/len(toks)
    first = mt[0] if mt else None
    rep.append(dict(line=l[0], ntok=len(toks), nmatch=len(mt), frac=frac, first_idx=first[0] if first else None,
                    start=first[1]['s'] if first else None, words=' '.join(t.get('wt','_') for t in toks)))
json.dump(rep, open('align_report.json','w'), indent=1)
for r in rep: print(r['line'], f"{r['nmatch']}/{r['ntok']}", r['first_idx'], None if r['start'] is None else round(r['start'],2), '|', r['words'])
