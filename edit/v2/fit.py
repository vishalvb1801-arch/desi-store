import json
P=json.load(open('plan.json')); fr=P['frames']; FPS=30
L=121/24
CUTS={4:[1.95833],5:[2.29167],9:[2.5],11:[1.95833,3.20833],13:[2.95833],14:[2.41667],15:[1.54167],16:[2.91667],17:[1.58333],
23:[1.54167],24:[2.625],29:[1.66667,3.5],30:[2.54167],34:[3.16667],35:[2.33333],36:[2.95833],38:[2.95833],39:[2.5],42:[1.5],
44:[1.5],47:[2.95833],49:[2.83333],50:[1.95833],51:[2.79167],52:[2.04167],53:[3.0],55:[1.95833],58:[2.0]}
MINSHOT=0.8; FMAX=1.5
plan=[]
for i in range(1,61):
    n=fr[i]-fr[i-1]; T=n/FPS
    cuts=CUTS.get(i,[])
    if i==58:
        plan.append(dict(line=i,frames=n,T=T,special='58'));continue
    # default: trim if T<=L else slow to fill
    def shots(window,f):
        b=[0]+[c for c in cuts if c<window]+[window]
        return [(b[k+1]-b[k])*f for k in range(len(b)-1)]
    if T<=L: win=T; f=1.0
    else: win=L; f=T/L
    note=''
    sh=shots(win,f)
    if min(sh)<MINSHOT-1e-6:
        # drop the short tail shot: end the window on the last internal cut and slow to fill
        last=[c for c in cuts if c<win][-1]
        win2=last; f2=T/win2
        note=f'dropped {sh[-1]:.2f}s tail shot after in-clip cut at {last:.2f}s; slowed to {f2:.2f}x'
        win,f=win2,f2; sh=shots(win,f)
    hold=0.0
    if f>FMAX+1e-9: note+=f' | needs {f:.2f}x'
    plan.append(dict(line=i,frames=n,T=round(T,3),win=round(win,4),f=round(f,4),shots=[round(s,2) for s in sh],note=note))
for p in plan: print(p)
json.dump(plan,open('fit_plan.json','w'),indent=1)
