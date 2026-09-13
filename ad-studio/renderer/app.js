/*
 * app.js — kie Ad Studio renderer.
 *
 * Talks to the backend only through window.api (see api.js). Holds no API key and
 * never sees one: the key is typed into Settings and posted straight through.
 */
(function () {
  'use strict';

  /* =========================================================
     State
     ========================================================= */

  var DEFAULT_FRAME_UNIT = 15;
  var RES_COST = { std: 30, pro: 50, '4k': 80 };
  var SOUND_SURCHARGE = 25;
  var POLL_MS = 2500;

  var S = {
    key: false,
    balance: null,
    spent: 0,
    frames: {
      file: null, count: 0, hasAnchor: false, unit: DEFAULT_FRAME_UNIT,
      source: null,            // 'generate' | 'upload'
      anchor: null, packshot: null,
      items: []
    },
    motion: {
      file: null, count: 0, unit: null,
      settings: { model: 'kling', res: 'pro', dur: '5', asp: '9:16', sound: false },
      items: []
    },
    song: { file: null, item: null },
    videoLog: [],
    itemLog: [],
    busy: { frames: false, motion: false, song: false }
  };

  var $  = function (id) { return document.getElementById(id); };
  var on = function (el, ev, fn) { if (el) el.addEventListener(ev, fn); };

  /* =========================================================
     Toast
     ========================================================= */

  var toastTimer;
  function toast(msg, kind) {
    var t = $('toast');
    $('toast-msg').textContent = msg;
    t.className = kind || '';
    t.style.opacity = 1;
    t.style.transform = 'translateX(-50%) translateY(0)';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      t.style.opacity = 0;
      t.style.transform = 'translateX(-50%) translateY(20px)';
    }, kind === 'err' ? 4200 : 2200);
  }
  function fail(e) { toast((e && e.message) ? e.message : String(e), 'err'); }

  /* =========================================================
     Navigation
     ========================================================= */

  document.querySelectorAll('.nav button').forEach(function (b) {
    on(b, 'click', function () {
      var v = b.dataset.v;
      document.querySelectorAll('.nav button').forEach(function (x) { x.classList.toggle('on', x === b); });
      document.querySelectorAll('.view').forEach(function (s) { s.classList.remove('on'); });
      $('v-' + v).classList.add('on');
    });
  });
  document.querySelectorAll('.logtabs button').forEach(function (b) {
    on(b, 'click', function () {
      var l = b.dataset.l;
      document.querySelectorAll('.logtabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
      $('log-video').style.display = l === 'video' ? 'block' : 'none';
      $('log-item').style.display  = l === 'item'  ? 'block' : 'none';
    });
  });

  /* =========================================================
     Credits
     ========================================================= */

  function paintCredits() {
    $('bal').textContent = S.balance === null ? '—' : Number(S.balance).toLocaleString();
    $('spend').textContent = '+' + S.spent;
  }
  // kie reports what a job actually cost via creditsConsumed; reads are never billed,
  // so the running total only ever moves on a completed generation.
  function bill(n) {
    n = Number(n) || 0;
    if (!n) return;
    S.spent += n;
    if (S.balance !== null) S.balance -= n;
    paintCredits();
  }

  /* =========================================================
     Asset cards — keyed DOM, updated in place.
     Re-rendering wholesale would restart every <img> and flash the grid.
     ========================================================= */

  var REROLL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>';
  var WARN_ICON   = '<svg class="warn" viewBox="0 0 24 24" fill="none" stroke="#e5675f" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>';

  function cardFor(stage, item) {
    var grid = $('grid-' + stage);
    var el = grid.querySelector('[data-id="' + cssEscape(item.id) + '"]');
    if (el) return el;
    el = document.createElement('div');
    el.className = 'card';
    el.dataset.id = item.id;
    el.innerHTML = '<div class="canvas"></div><div class="cardfoot"><span class="nm"></span><div class="r"></div></div>';
    grid.appendChild(el);
    return el;
  }
  function cssEscape(s) { return String(s).replace(/"/g, '\\"'); }

  function paintCard(stage, item) {
    var el = cardFor(stage, item);
    var canvas = el.querySelector('.canvas');
    var foot   = el.querySelector('.r');
    el.querySelector('.nm').textContent = item.label || item.id;

    // Footer actions
    foot.innerHTML = '';
    if (item.state === 'done') {
      foot.appendChild(actionBtn('ibtn', REROLL_ICON + ' Re-roll', function () { reroll(stage, item.id); }));
    } else if (item.state === 'failed') {
      foot.appendChild(actionBtn('ibtn retry', REROLL_ICON + ' Retry', function () { retry(stage, item.id); }));
    }

    var sig = item.state + '|' + (item.localPath || '') + '|' + (item.version || '') + '|' + (item.error || '');
    if (el._sig === sig) return;      // nothing visible changed; leave the DOM (and any <img>) alone
    el._sig = sig;

    if (item.state === 'done' && item.localPath) {
      // Keep the spinner up until the asset has actually decoded — a painted-but-unloaded
      // tile is how the old UI looked "done" while showing nothing.
      showSpinner(canvas, 'loading');
      var url = window.api.assetUrl(item.localPath, item.version);
      var isVideo = /\.(mp4|webm|mov)$/i.test(item.localPath);
      var media = document.createElement(isVideo ? 'video' : 'img');
      media.className = 'art';
      if (isVideo) { media.muted = true; media.loop = true; media.playsInline = true; media.controls = false; }
      media.addEventListener(isVideo ? 'loadeddata' : 'load', function () {
        canvas.innerHTML = '';
        canvas.appendChild(media);
        canvas.insertAdjacentHTML('beforeend',
          '<span class="cap">' + esc(item.label || item.id) + '</span>' +
          (item.creditsConsumed ? '<span class="cost">' + item.creditsConsumed + ' cr</span>' : ''));
        if (isVideo) { media.play().catch(function () {}); }
      });
      media.addEventListener('error', function () {
        // The file is gone or unreadable on disk — surface it instead of an empty tile.
        item.state = 'failed';
        item.error = 'asset missing on disk';
        el._sig = null;
        paintCard(stage, item);
      });
      media.src = url;
      return;
    }

    if (item.state === 'generating') {
      canvas.innerHTML = '<span class="statepill gen">generating…</span>' +
        '<div class="center"><div class="spin"></div><span class="lbl">rendering</span></div>';
    } else if (item.state === 'failed') {
      canvas.innerHTML = '<span class="statepill fail">failed</span>' +
        '<div class="center fail">' + WARN_ICON +
        '<span class="lbl">' + esc(item.error || 'render failed') + '</span></div>';
    } else {
      canvas.innerHTML = '<span class="statepill queued">queued</span>';
    }
  }

  function showSpinner(canvas, label) {
    canvas.innerHTML = '<span class="statepill gen">generating…</span>' +
      '<div class="center"><div class="spin"></div><span class="lbl">' + esc(label) + '</span></div>';
  }
  function actionBtn(cls, html, fn) {
    var b = document.createElement('button');
    b.className = cls; b.innerHTML = html; b.addEventListener('click', fn);
    return b;
  }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function paintGrid(stage) {
    var items = S[stage].items;
    var grid = $('grid-' + stage);
    var empty = $('empty-' + stage);
    if (empty) empty.style.display = items.length ? 'none' : 'block';
    // Drop cards whose item no longer exists (e.g. a new prompt file was loaded).
    var ids = {};
    items.forEach(function (i) { ids[i.id] = 1; });
    Array.prototype.slice.call(grid.children).forEach(function (c) {
      if (!ids[c.dataset.id]) grid.removeChild(c);
    });
    items.forEach(function (i) { paintCard(stage, i); });
  }

  /* =========================================================
     Estimates
     ========================================================= */

  function estFrames() {
    var f = S.frames, n = f.count;
    if (!n) {
      $('fcalc').textContent = 'load prompts to estimate';
      $('ftot').textContent = '';
    } else {
      $('fcalc').textContent = n + ' frames × ' + f.unit + ' cr';
      $('ftot').textContent = '= ' + (n * f.unit) + ' cr';
    }
    $('go-frames').disabled = !(n && f.anchor && f.packshot && !S.busy.frames);
  }

  function motionUnit() {
    var s = S.motion.settings;
    var per = RES_COST[s.res] || RES_COST.pro;
    if (s.dur === '10') per *= 2;
    if (s.sound) per += SOUND_SURCHARGE;
    return per;
  }
  function estMotion() {
    var n = S.motion.count, per = motionUnit();
    S.motion.unit = per;
    if (!n) {
      $('mcalc').textContent = 'load prompts to estimate';
      $('mtot').textContent = '';
    } else {
      $('mcalc').textContent = n + ' clips × ' + per + ' cr' +
        (S.motion.settings.sound ? ' (incl. sound +' + SOUND_SURCHARGE + ')' : '');
      $('mtot').textContent = '= ' + (n * per) + ' cr';
    }
    var framesReady = S.frames.items.some(function (i) { return i.state === 'done'; });
    $('go-motion').disabled = !(n && framesReady && !S.busy.motion);
  }

  /* =========================================================
     Prompt loaders
     ========================================================= */

  function wireLoader(btnId, inputId, handler) {
    on($(btnId), 'click', function () { $(inputId).click(); });
    on($(inputId), 'change', function (e) {
      var file = e.target.files && e.target.files[0];
      if (file) handler(file);
      e.target.value = '';                       // allow re-picking the same file
    });
  }

  wireLoader('btn-frame-prompts', 'fi-frame-prompts', async function (file) {
    try {
      var r = await window.api.loadFramePrompts(file);
      S.frames.file = r.name || file.name;
      S.frames.count = r.count || (r.items ? r.items.length : 0);
      S.frames.hasAnchor = !!r.hasAnchor;
      if (r.unitCost) S.frames.unit = r.unitCost;
      if (r.items && !S.frames.items.length) {
        S.frames.items = r.items.map(function (i) {
          return { id: i.id, label: i.label || i.id, kind: i.kind, state: 'queued', cost: S.frames.unit };
        });
        paintGrid('frames');
      }
      $('chip-frames').hidden = false;
      $('chip-frames-name').textContent = S.frames.file;
      $('chip-frames-count').textContent = S.frames.count + ' frames';
      $('chip-frames-anchor').hidden = !S.frames.hasAnchor;
      toast(S.frames.file + ' loaded · ' + S.frames.count + ' frames', 'ok');
      estFrames(); estMotion();
    } catch (e) { fail(e); }
  });

  wireLoader('btn-motion-prompts', 'fi-motion-prompts', async function (file) {
    try {
      var r = await window.api.loadMotionPrompts(file);
      S.motion.file = r.name || file.name;
      S.motion.count = r.count || (r.items ? r.items.length : 0);
      if (r.items && !S.motion.items.length) {
        S.motion.items = r.items.map(function (i) {
          return { id: i.id, label: i.label || i.id, kind: i.kind, state: 'queued' };
        });
        paintGrid('motion');
      }
      $('chip-motion').hidden = false;
      $('chip-motion-name').textContent = S.motion.file;
      $('chip-motion-count').textContent = S.motion.count + ' clips';
      toast(S.motion.file + ' loaded · ' + S.motion.count + ' clips', 'ok');
      estMotion();
    } catch (e) { fail(e); }
  });

  wireLoader('btn-song-prompt', 'fi-song-prompt', async function (file) {
    try {
      var r = await window.api.loadSongPrompt(file);
      S.song.file = r.name || file.name;
      if (r.style)  $('s-style').value  = r.style;
      if (r.lyrics) $('s-lyrics').value = r.lyrics;
      if (r.model)  $('s-model').value  = r.model;
      if (r.vocal)  $('s-vocal').value  = r.vocal;
      $('chip-song').hidden = false;
      $('chip-song-name').textContent = S.song.file;
      toast(S.song.file + ' loaded', 'ok');
    } catch (e) { fail(e); }
  });

  /* =========================================================
     Stage 1 — anchor / packshot uploads
     ========================================================= */

  function wireUpload(kind, inputId, uploader) {
    document.querySelectorAll('[data-upload="' + kind + '"]').forEach(function (b) {
      on(b, 'click', function () { $(inputId).click(); });
    });
    on($(inputId), 'change', async function (e) {
      var file = e.target.files && e.target.files[0];
      e.target.value = '';
      if (!file) return;
      try {
        var r = await uploader(file);
        S.frames[kind] = r;
        var th = $('th-' + kind);
        th.innerHTML = '';
        var img = document.createElement('img');
        img.src = window.api.assetUrl(r.localPath, r.version || Date.now());
        th.appendChild(img);
        $('badge-' + kind).hidden = false;
        $('sub-' + kind).textContent = (r.name || file.name) +
          (r.width && r.height ? ' · ' + r.width + '×' + r.height : '');
        document.querySelectorAll('[data-view="' + kind + '"]').forEach(function (v) { v.hidden = false; });
        toast((kind === 'anchor' ? 'Character anchor' : 'Packshot') + ' uploaded', 'ok');
        estFrames();
      } catch (err) { fail(err); }
    });
  }
  wireUpload('anchor',   'fi-anchor',   function (f) { return window.api.uploadAnchor(f); });
  wireUpload('packshot', 'fi-packshot', function (f) { return window.api.uploadPackshot(f); });

  document.querySelectorAll('[data-view]').forEach(function (b) {
    on(b, 'click', function () {
      var r = S.frames[b.dataset.view];
      if (r && r.localPath) window.open(window.api.assetUrl(r.localPath, r.version), '_blank');
    });
  });

  /* =========================================================
     Stage 1 — Option 2: bring your own frames (zip or images)
     ========================================================= */

  async function acceptOwnFrames(fileList) {
    var files = Array.prototype.slice.call(fileList);
    if (!files.length) return;
    try {
      var r = await window.api.uploadOwnFrames(files);
      S.frames.source = 'upload';
      S.frames.items = (r.items || []).map(function (i) {
        return {
          id: i.id, label: i.label || i.id, state: 'done',
          localPath: i.localPath, version: i.version || Date.now(),
          creditsConsumed: 0
        };
      });
      S.frames.count = S.frames.items.length;
      $('frames-head').textContent = 'Frames · uploaded';
      paintGrid('frames');
      toast(S.frames.items.length + ' frames uploaded ✓', 'ok');
      estFrames(); estMotion();
    } catch (e) { fail(e); }
  }

  on($('btn-own-frames'), 'click', function () { $('fi-own-frames').click(); });
  on($('fi-own-frames'), 'change', function (e) {
    var fs = e.target.files; e.target.value = '';
    acceptOwnFrames(fs);
  });

  var dz = $('dz-frames');
  ['dragenter', 'dragover'].forEach(function (ev) {
    on(dz, ev, function (e) { e.preventDefault(); dz.classList.add('over'); });
  });
  ['dragleave', 'drop'].forEach(function (ev) {
    on(dz, ev, function (e) { e.preventDefault(); dz.classList.remove('over'); });
  });
  on(dz, 'drop', function (e) {
    if (e.dataTransfer && e.dataTransfer.files) acceptOwnFrames(e.dataTransfer.files);
  });
  // Stop a stray drop elsewhere in the window from navigating away from the app.
  ['dragover', 'drop'].forEach(function (ev) {
    window.addEventListener(ev, function (e) { if (!dz.contains(e.target)) e.preventDefault(); });
  });

  /* =========================================================
     Motion controls
     ========================================================= */

  on($('m-model'), 'change', function () {
    S.motion.settings.model = this.value;
    // Veo drives its own resolution ladder; the control stays visible but inert.
    $('f-res').classList.toggle('dim', this.value === 'veo');
    $('m-res').disabled = this.value === 'veo';
    estMotion();
  });
  on($('m-res'), 'change', function () { S.motion.settings.res = this.value; estMotion(); });
  on($('m-dur'), 'change', function () { S.motion.settings.dur = this.value; estMotion(); });
  on($('m-asp'), 'change', function () { S.motion.settings.asp = this.value; });
  on($('m-sound'), 'click', function () {
    var next = !S.motion.settings.sound;
    S.motion.settings.sound = next;
    this.classList.toggle('on', next);
    this.setAttribute('aria-pressed', String(next));
    $('m-sound-lbl').textContent = next ? 'On' : 'Off';
    estMotion();
  });

  /* =========================================================
     Generation + polling
     ========================================================= */

  var MODEL_LABEL = {
    frames: function () { return 'Nano Banana Pro'; },
    motion: function () { return S.motion.settings.model === 'veo' ? 'Veo 3.1' : 'Kling 3.0'; }
  };

  function itemById(stage, id) {
    return S[stage].items.filter(function (i) { return i.id === id; })[0];
  }

  async function startStage(stage) {
    if (S.busy[stage]) return;
    S.busy[stage] = true;
    $('go-' + stage).disabled = true;
    try {
      var res = stage === 'frames'
        ? await window.api.generateFrames()
        : await window.api.generateMotion(S.motion.settings);

      (res.items || []).forEach(function (r) {
        var it = itemById(stage, r.id);
        if (!it) {
          it = { id: r.id, label: r.label || r.id, state: 'queued' };
          S[stage].items.push(it);
        }
        it.jobId = r.jobId;
        it.state = 'generating';
        it.error = null;
      });
      if (stage === 'frames') S.frames.source = 'generate';
      paintGrid(stage);
      toast('Generating ' + (res.items || []).length + ' ' +
            (stage === 'frames' ? 'frames' : 'clips') + '…', 'gen');
      await pollUntilIdle(stage);
      finishBatch(stage);
    } catch (e) {
      fail(e);
    } finally {
      S.busy[stage] = false;
      stage === 'frames' ? estFrames() : estMotion();
    }
  }

  on($('go-frames'), 'click', function () { startStage('frames'); });
  on($('go-motion'), 'click', function () { startStage('motion'); });

  // Poll every in-flight job for a stage until none remain.
  async function pollUntilIdle(stage) {
    for (;;) {
      var live = S[stage].items.filter(function (i) {
        return i.jobId && (i.state === 'generating' || i.state === 'queued');
      });
      if (!live.length) return;
      await Promise.all(live.map(function (it) { return pollOne(stage, it); }));
      paintGrid(stage);
      if (S[stage].items.some(function (i) {
        return i.jobId && (i.state === 'generating' || i.state === 'queued');
      })) await sleep(POLL_MS);
    }
  }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  async function pollOne(stage, it) {
    try {
      var r = await window.api.job(it.jobId);
      if (r.state === 'done') {
        // The backend only hands back localPath once the asset is on disk in outputs/.
        it.state = 'done';
        it.localPath = r.localPath;
        it.version = r.version || Date.now();
        it.creditsConsumed = Number(r.creditsConsumed) || 0;
        it.jobId = null;
        bill(it.creditsConsumed);
        if (typeof r.balance === 'number') { S.balance = r.balance; paintCredits(); }
        logItem(stage, it, 'done');
      } else if (r.state === 'failed') {
        it.state = 'failed';
        it.error = r.error || 'render failed';
        it.jobId = null;
        // A failed kie job bills nothing, so the running total is untouched here.
        logItem(stage, it, 'fail');
      } else {
        it.state = r.state === 'queued' ? 'queued' : 'generating';
      }
    } catch (e) {
      it.state = 'failed';
      it.error = (e && e.message) || 'poll failed';
      it.jobId = null;
      logItem(stage, it, 'fail');
    }
  }

  async function singleJob(stage, itemId, kickoff, okMsg) {
    var it = itemById(stage, itemId);
    if (!it) return;
    var prev = it.state;
    it.state = 'generating'; it.error = null;
    paintCard(stage, it);
    try {
      var r = await kickoff();
      it.jobId = r.jobId;
      while (it.jobId) {
        await sleep(POLL_MS);
        await pollOne(stage, it);
        paintCard(stage, it);
      }
      if (it.state === 'done') toast(okMsg, 'ok');
    } catch (e) {
      it.state = prev === 'done' ? 'done' : 'failed';
      it.error = (e && e.message) || 'request failed';
      paintCard(stage, it);
      fail(e);
    }
  }

  function reroll(stage, id) {
    toast('Re-rolling ' + id + '…', 'gen');
    singleJob(stage, id, function () { return window.api.reroll(stage, id); }, id + ' re-rolled');
  }
  function retry(stage, id) {
    toast('Retrying ' + id + '…', 'gen');
    singleJob(stage, id, function () { return window.api.retry(stage, id); }, id + ' recovered');
  }

  /* =========================================================
     Logs
     ========================================================= */

  function logItem(stage, it, status) {
    S.itemLog.push({
      id: it.label || it.id,
      stage: stage === 'frames' ? 'Frame' : 'Clip',
      model: MODEL_LABEL[stage](),
      status: status,
      cr: status === 'done' ? (it.creditsConsumed || 0) : 0
    });
    drawItemLog();
  }

  function finishBatch(stage) {
    var items = S[stage].items;
    var done = items.filter(function (i) { return i.state === 'done'; });
    var failed = items.some(function (i) { return i.state === 'failed'; });
    var cr = done.reduce(function (a, b) { return a + (b.creditsConsumed || 0); }, 0);
    S.videoLog.push({
      name: (S[stage].file || (stage === 'frames' ? 'frame set' : 'clips')),
      assets: done.length + ' / ' + items.length,
      status: failed ? 'gen' : 'done',
      cr: cr
    });
    drawVideoLog();
    toast(failed ? 'Batch done — some items need retry' : 'Batch complete', failed ? 'err' : 'ok');
  }

  function drawVideoLog() {
    var tb = $('tb-video');
    if (!S.videoLog.length) {
      tb.innerHTML = '<tr><td colspan="4" class="empty-log">No videos yet. Run a batch to log it here.</td></tr>';
    } else {
      tb.innerHTML = S.videoLog.map(function (r) {
        return '<tr><td>' + esc(r.name) + '</td><td>' + esc(r.assets) + '</td>' +
          '<td><span class="st ' + r.status + '"><span class="dot"></span>' +
          (r.status === 'done' ? 'complete' : 'needs retry') + '</span></td>' +
          '<td class="num">' + r.cr + ' cr</td></tr>';
      }).join('');
    }
    $('foot-video').textContent = S.spent + ' cr';
  }

  function drawItemLog() {
    var tb = $('tb-item');
    if (!S.itemLog.length) {
      tb.innerHTML = '<tr><td colspan="5" class="empty-log">No items yet.</td></tr>';
    } else {
      tb.innerHTML = S.itemLog.slice().reverse().map(function (r) {
        return '<tr><td>' + esc(r.id) + '</td><td>' + esc(r.stage) + '</td><td>' + esc(r.model) + '</td>' +
          '<td><span class="st ' + r.status + '"><span class="dot"></span>' +
          (r.status === 'done' ? 'done' : 'failed') + '</span></td>' +
          '<td class="num">' + r.cr + ' cr</td></tr>';
      }).join('');
    }
    $('foot-item').textContent = S.spent + ' cr';
  }

  /* =========================================================
     Song
     ========================================================= */

  on($('go-song'), 'click', async function () {
    if (S.busy.song) return;
    var lyrics = $('s-lyrics').value.trim();
    if (!lyrics) { toast('Add lyrics, or load a Suno prompt file', 'err'); return; }
    S.busy.song = true;
    this.disabled = true;
    try {
      toast('Generating song on kie Suno…', 'gen');
      var r = await window.api.generateSong({
        model: $('s-model').value,
        vocal: $('s-vocal').value,
        style: $('s-style').value.trim(),
        lyrics: lyrics
      });
      var jobId = r.jobId, out = null;
      for (;;) {
        await sleep(POLL_MS);
        var j = await window.api.job(jobId);
        if (j.state === 'done')   { out = j; break; }
        if (j.state === 'failed') throw new Error(j.error || 'song generation failed');
      }
      bill(out.creditsConsumed);
      if (typeof out.balance === 'number') { S.balance = out.balance; paintCredits(); }
      $('song-audio').src = window.api.assetUrl(out.localPath, out.version);
      $('song-cr').textContent = (out.creditsConsumed || 0) + ' cr';
      $('song-out').hidden = false;
      S.song.item = { localPath: out.localPath, creditsConsumed: out.creditsConsumed };
      S.itemLog.push({ id: 'song', stage: 'Song', model: 'Suno ' + $('s-model').value,
                       status: 'done', cr: out.creditsConsumed || 0 });
      drawItemLog();
      toast('Song ready — saved locally', 'ok');
    } catch (e) {
      fail(e);
    } finally {
      S.busy.song = false;
      $('go-song').disabled = false;
    }
  });

  /* =========================================================
     Save / resume + download all
     ========================================================= */

  function snapshot() {
    return {
      savedAt: new Date().toISOString(),
      spent: S.spent,
      frames: {
        file: S.frames.file, count: S.frames.count, hasAnchor: S.frames.hasAnchor,
        unit: S.frames.unit, source: S.frames.source,
        anchor: S.frames.anchor, packshot: S.frames.packshot,
        items: S.frames.items
      },
      motion: {
        file: S.motion.file, count: S.motion.count,
        settings: S.motion.settings, items: S.motion.items
      },
      song: S.song,
      videoLog: S.videoLog,
      itemLog: S.itemLog
    };
  }

  on($('btn-save'), 'click', async function () {
    try { await window.api.saveRun(snapshot()); toast('Run saved — resume anytime', 'ok'); }
    catch (e) { fail(e); }
  });

  on($('btn-download'), 'click', async function () {
    var btn = this;
    btn.disabled = true;
    try {
      toast('Zipping finished assets…', 'gen');
      var r = await window.api.downloadAll();
      toast('Saved ' + (r.localPath || 'archive'), 'ok');
    } catch (e) { fail(e); }
    finally { btn.disabled = false; }
  });

  async function restore() {
    var run;
    try { run = await window.api.loadRun(); } catch (e) { return; }
    if (!run || !run.frames) return;

    S.spent = run.spent || 0;
    Object.assign(S.frames, run.frames);
    Object.assign(S.motion, run.motion || {});
    S.song = run.song || S.song;
    S.videoLog = run.videoLog || [];
    S.itemLog = run.itemLog || [];

    // Anything caught mid-flight when the app closed is no longer being polled.
    ['frames', 'motion'].forEach(function (stage) {
      (S[stage].items || []).forEach(function (i) {
        if (i.state === 'generating' || i.state === 'queued') {
          if (i.jobId) { i.state = 'generating'; }
          else { i.state = 'failed'; i.error = 'interrupted — retry'; }
        }
      });
    });

    if (S.frames.file) {
      $('chip-frames').hidden = false;
      $('chip-frames-name').textContent = S.frames.file;
      $('chip-frames-count').textContent = S.frames.count + ' frames';
      $('chip-frames-anchor').hidden = !S.frames.hasAnchor;
    }
    if (S.frames.source === 'upload') $('frames-head').textContent = 'Frames · uploaded';
    ['anchor', 'packshot'].forEach(function (k) {
      var r = S.frames[k];
      if (!r || !r.localPath) return;
      var th = $('th-' + k); th.innerHTML = '';
      var img = document.createElement('img');
      img.src = window.api.assetUrl(r.localPath, r.version || Date.now());
      th.appendChild(img);
      $('badge-' + k).hidden = false;
      $('sub-' + k).textContent = r.name || '';
      document.querySelectorAll('[data-view="' + k + '"]').forEach(function (v) { v.hidden = false; });
    });
    if (S.motion.file) {
      $('chip-motion').hidden = false;
      $('chip-motion-name').textContent = S.motion.file;
      $('chip-motion-count').textContent = S.motion.count + ' clips';
    }
    if (S.motion.settings) {
      var s = S.motion.settings;
      $('m-model').value = s.model; $('m-res').value = s.res;
      $('m-dur').value = s.dur; $('m-asp').value = s.asp;
      $('m-sound').classList.toggle('on', !!s.sound);
      $('m-sound-lbl').textContent = s.sound ? 'On' : 'Off';
      $('f-res').classList.toggle('dim', s.model === 'veo');
      $('m-res').disabled = s.model === 'veo';
    }
    if (S.song.item && S.song.item.localPath) {
      $('song-audio').src = window.api.assetUrl(S.song.item.localPath, Date.now());
      $('song-cr').textContent = (S.song.item.creditsConsumed || 0) + ' cr';
      $('song-out').hidden = false;
    }

    paintGrid('frames'); paintGrid('motion');
    drawVideoLog(); drawItemLog(); paintCredits();
    toast('Previous run restored', 'ok');

    // Re-attach to anything the backend is still working on.
    ['frames', 'motion'].forEach(function (stage) {
      if (S[stage].items.some(function (i) { return i.jobId; })) {
        S.busy[stage] = true;
        pollUntilIdle(stage).then(function () {
          S.busy[stage] = false;
          stage === 'frames' ? estFrames() : estMotion();
        });
      }
    });
  }

  /* =========================================================
     Settings / API key
     ========================================================= */

  function paintKey() {
    $('keydot').classList.toggle('missing', !S.key);
    $('keydot-label').textContent = S.key ? 'API key loaded' : 'No API key — click to add';
  }
  on($('keydot'), 'click', function () { $('key-input').value = ''; $('settings').hidden = false; });
  on($('key-cancel'), 'click', function () { $('key-input').value = ''; $('settings').hidden = true; });
  on($('key-save'), 'click', async function () {
    var k = $('key-input').value.trim();
    if (!k) { toast('Paste a key first', 'err'); return; }
    try {
      await window.api.saveKey(k);
      $('key-input').value = '';                 // never retained in the renderer
      $('settings').hidden = true;
      S.key = true; paintKey();
      toast('API key saved', 'ok');
      refreshCredits();
    } catch (e) { fail(e); }
  });

  async function refreshCredits() {
    try {
      var c = await window.api.credits();
      S.balance = c.balance;
      paintCredits();
    } catch (e) { /* balance stays "—" */ }
  }

  /* =========================================================
     Boot
     ========================================================= */

  (async function boot() {
    paintCredits(); estFrames(); estMotion();
    drawVideoLog(); drawItemLog(); paintGrid('frames'); paintGrid('motion');
    try {
      var k = await window.api.keyStatus();
      S.key = !!(k && k.present);
    } catch (e) { S.key = false; }
    paintKey();
    if (S.key) refreshCredits();
    await restore();
  })();
})();
