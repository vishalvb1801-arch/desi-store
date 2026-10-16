"""Hinglish subtitles: exact LYRICS text, <=2 rows/event, cream text on a rounded maroon box, label-safe positions."""
import json, csv, re, sys
from PIL import ImageFont
base = sys.argv[1]
FONT = ImageFont.truetype('/root/.local/share/fonts/Montserrat-ExtraBold.ttf', 64 * 0.6396)  # = libass Fontsize 64
CREAM, MAROON, ALPHA = 'FFF3DC', '7B1C24', 0x26          # ~85% opaque box
FS, LINE_H, PADX, PADY, RADIUS = 64, 64, 30, 18, 22
MAX_CH, MAX_W = 34, 900
AUDIO_END = 210.050583
POS = {'default': ('an2', 1400), 'up': ('an2', 1110), 'top': ('an8', 240), 'top-hi': ('an8', 190)}
LINE_POS = {39: 'top-hi'}   # bottle held high at line start: extra clearance above the EIS wordmark
SEG_POS = {22: 'top', 23: 'top', 24: 'top', 35: 'top', 36: 'top', 40: 'top', 25: 'up', 39: 'up'}
plan = json.load(open(f'{base}/work/edit_plan.json'))
HL = list(csv.DictReader(open(f'{base}/out/hinglish-timing.csv')))
HA = json.load(open(f'{base}/work/hin_align.json'))
W = lambda s: FONT.getlength(s)
def norm(tok): return [w for w in re.sub(r"[^a-z' ]", ' ', tok.lower().replace('-', ' ')).split() if w.strip("'")]
def rows_for(tokens):
    """best split of tokens into 1-2 rows (prefer after punctuation, balanced)"""
    txt = ' '.join(tokens)
    if len(txt) <= MAX_CH and W(txt) <= MAX_W: return [txt]
    best = None
    for k in range(1, len(tokens)):
        a, b = ' '.join(tokens[:k]), ' '.join(tokens[k:])
        if max(len(a), len(b)) > MAX_CH or max(W(a), W(b)) > MAX_W: continue
        cost = abs(W(a) - W(b)) - (300 if re.search(r'[,?]$', tokens[k - 1]) else 0)
        if best is None or cost < best[0]: best = (cost, [a, b])
    return best[1] if best else None
def chunks(tokens, force=()):
    """split a line into events at commas so every event fits in 2 rows (always split at sung pauses >= 1 s)"""
    for k in force:
        if 0 < k < len(tokens): return chunks(tokens[:k]) + chunks(tokens[k:], [f - k for f in force if f > k])
    if rows_for(tokens): return [tokens]
    cands = [k for k in range(1, len(tokens)) if re.search(r'[,?]["]?$', tokens[k - 1])] or list(range(1, len(tokens)))
    for k in sorted(cands, key=lambda k: abs(len(' '.join(tokens[:k])) - len(' '.join(tokens[k:])))):
        a, b = chunks(tokens[:k]), chunks(tokens[k:])
        if all(rows_for(c) for c in a + b): return a + b
    raise ValueError(' '.join(tokens))
def seg_of(a, b):
    """segment overlapping the event [a, b] the most"""
    return max(plan, key=lambda p: min(b, p['end']) - max(a, p['start']))['idx']
events = []
for i, (row, al) in enumerate(zip(HL, HA)):
    toks = row['hinglish_line'].split()
    # start time of each original token (first normalised word); line 39 uses line timing only
    tstart, tend, wi = [], [], 0
    for tok in toks:
        nw = len(norm(tok)); ok = row['line_no'] != '39'
        tstart.append(al['words'][wi]['start'] if ok else None); tend.append(al['words'][wi + nw - 1]['end'] if ok else None); wi += nw
    force = [k for k in range(1, len(toks)) if tstart[k] is not None and re.search(r'[,?]["]?$', toks[k - 1]) and tstart[k] - tend[k - 1] >= 1.0]
    start, vend = float(row['start']), float(row['end'])
    nxt = float(HL[i + 1]['start']) if i + 1 < len(HL) else AUDIO_END
    k0 = 0; cs = chunks(toks, force)
    for j, c in enumerate(cs):
        s = start if j == 0 else (tstart[k0] if tstart[k0] is not None else start + (vend - start) * k0 / len(toks))
        events.append(dict(line=int(row['line_no']), rows=rows_for(c), start=s, vend=vend, nxt=nxt)); k0 += len(c)
for j, e in enumerate(events):
    if j + 1 < len(events) and events[j + 1]['line'] == e['line']: e['end'] = events[j + 1]['start']
    else:
        e['end'] = min(e['vend'] + 0.2, e['nxt'])
        if e['nxt'] - e['end'] < 0.15: e['end'] = e['nxt']        # no flicker gaps
    e['seg'] = seg_of(e['start'], e['end']); e['pos'] = LINE_POS.get(e['line'], SEG_POS.get(e['seg'], 'default'))
def ts(t, sep='.'):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}{sep}{cs:02d}"
def ass_col(hexrgb): return f"&H{hexrgb[4:6]}{hexrgb[2:4]}{hexrgb[0:2]}&"
def rrect(x0, y0, x1, y1, r):
    k = r * 0.4477
    return (f"m {x0+r:.0f} {y0:.0f} l {x1-r:.0f} {y0:.0f} b {x1-k:.0f} {y0:.0f} {x1:.0f} {y0+k:.0f} {x1:.0f} {y0+r:.0f} "
            f"l {x1:.0f} {y1-r:.0f} b {x1:.0f} {y1-k:.0f} {x1-k:.0f} {y1:.0f} {x1-r:.0f} {y1:.0f} "
            f"l {x0+r:.0f} {y1:.0f} b {x0+k:.0f} {y1:.0f} {x0:.0f} {y1-k:.0f} {x0:.0f} {y1-r:.0f} "
            f"l {x0:.0f} {y0+r:.0f} b {x0:.0f} {y0+k:.0f} {x0+k:.0f} {y0:.0f} {x0+r:.0f} {y0:.0f}")
hdr = f"""[Script Info]
Title: C202 Hinglish - The Man She Married Again
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Montserrat ExtraBold,{FS},&H00{CREAM[4:6]}{CREAM[2:4]}{CREAM[0:2]},&H00{CREAM[4:6]}{CREAM[2:4]}{CREAM[0:2]},&H{ALPHA:02X}{MAROON[4:6]}{MAROON[2:4]}{MAROON[0:2]},&H00000000,0,0,0,0,100,100,0,0,3,0,0,2,60,60,520,1
Style: Box,Arial,20,&H{ALPHA:02X}{MAROON[4:6]}{MAROON[2:4]}{MAROON[0:2]},&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines, srt = [hdr], []
for n, e in enumerate(events, 1):
    an, y = POS[e['pos']]
    h = len(e['rows']) * LINE_H
    top = y - h if an == 'an2' else y
    w = max(W(r) for r in e['rows'])
    x0, x1 = 540 - w / 2 - PADX, 540 + w / 2 + PADX
    y0, y1 = top - PADY + 4, top + h + PADY - 2
    e['box'] = [round(x0), round(y0), round(x1), round(y1)]
    st, en = ts(e['start']), ts(e['end'])
    lines.append(f"Dialogue: 0,{st},{en},Box,,0,0,0,,{{\\an7\\pos(0,0)\\bord0\\shad0\\p1}}{rrect(x0, y0, x1, y1, RADIUS)}{{\\p0}}\n")
    lines.append(f"Dialogue: 1,{st},{en},Lyric,,0,0,0,,{{\\{an}\\pos(540,{y})\\bord0\\shad0}}{'\\N'.join(e['rows'])}\n")
    srt.append(f"{n}\n{ts(e['start'], ',')}0 --> {ts(e['end'], ',')}0\n" + '\n'.join(e['rows']) + '\n')
open(f'{base}/out/C202-Hinglish.ass', 'w', encoding='utf-8').write(''.join(lines))
open(f'{base}/out/C202-Hinglish.srt', 'w', encoding='utf-8').write('\n'.join(srt))
json.dump(events, open(f'{base}/work/sub_events.json', 'w'), indent=1)
for e in events: print(f"L{e['line']:2d} {e['start']:7.2f}-{e['end']:7.2f} {e['pos']:7s} | " + ' / '.join(e['rows']))
