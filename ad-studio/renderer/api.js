/*
 * api.js — the ONLY place the renderer talks to the backend.
 *
 * Every function here maps onto one call in the existing kie pipeline. Swapping this
 * file's internals for direct IPC (Electron) or a different route prefix is the entire
 * integration surface; app.js never calls fetch() itself.
 *
 * Two rules this file enforces on behalf of the whole app:
 *
 *   1. assetUrl() refuses anything that is not a local path. A kie CDN URL reaching the
 *      renderer is the frames-vanish bug (they expire), so it is treated as a programming
 *      error and thrown, loudly, rather than rendered and silently broken minutes later.
 *   2. Every asset URL carries a cache-buster, so a re-rolled asset written to the same
 *      path still repaints, and a rebuild never shows a stale copy.
 */
(function (global) {
  'use strict';

  var BASE = '/api';

  /* ---------- low-level ---------- */

  function noCache(headers) {
    var h = headers || {};
    h['Cache-Control'] = 'no-cache, no-store, must-revalidate';
    h['Pragma'] = 'no-cache';
    return h;
  }

  async function req(method, path, body, isForm) {
    var opts = { method: method, headers: noCache({}), cache: 'no-store' };
    if (body !== undefined && body !== null) {
      if (isForm) {
        opts.body = body;                      // browser sets the multipart boundary
      } else {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(body);
      }
    }
    var res = await fetch(BASE + path, opts);
    var payload = null;
    try { payload = await res.json(); } catch (e) { /* empty or non-JSON body */ }
    if (!res.ok) {
      var msg = (payload && (payload.error || payload.message)) || (res.status + ' ' + res.statusText);
      throw new Error(msg);
    }
    return payload;
  }

  var get  = function (p) { return req('GET', p); };
  var post = function (p, b) { return req('POST', p, b === undefined ? {} : b); };
  var form = function (p, fd) { return req('POST', p, fd, true); };

  /* ---------- asset URLs (bugs 1 + 2) ---------- */

  // Anything that points off-box. kie's signed CDN links expire, which is exactly why
  // a frame shows and then vanishes; we never let one reach an <img>.
  var REMOTE = /^(https?:)?\/\//i;

  /**
   * Turn a backend-supplied local path into a URL safe to put in an <img>/<video>.
   * Throws on a remote URL — the backend must download to outputs/ first and hand
   * back the local path.
   */
  function assetUrl(localPath, version) {
    if (!localPath) return '';
    if (REMOTE.test(localPath) || /^data:/i.test(localPath)) {
      throw new Error(
        'Refusing to render a non-local asset: "' + String(localPath).slice(0, 80) + '". ' +
        'kie URLs expire — download the asset into outputs/ and return its local path.'
      );
    }
    var clean = String(localPath).replace(/^\/+/, '');
    // Cache-buster: re-rolls reuse the path, and a rebuild must not serve a stale copy.
    var v = version || Date.now();
    return '/outputs/' + clean + (clean.indexOf('?') === -1 ? '?v=' : '&v=') + encodeURIComponent(v);
  }

  /* ---------- API surface ---------- */

  var api = {
    assetUrl: assetUrl,

    // -- key + credits --
    keyStatus:  function ()    { return get('/key'); },                  // -> {present:bool}
    saveKey:    function (key) { return post('/key', { key: key }); },   // -> {present:true}
    credits:    function ()    { return get('/credits'); },              // -> {balance:number}

    // -- prompt files --
    // -> {name, count, hasAnchor?, items:[{id,label,kind?}]}
    loadFramePrompts:  function (file) { return form('/prompts/frames',  fd('file', file)); },
    loadMotionPrompts: function (file) { return form('/prompts/motion',  fd('file', file)); },
    loadSongPrompt:    function (file) { return form('/prompts/song',    fd('file', file)); },

    // -- stage 1 uploads --
    // -> {name, width, height, localPath}
    uploadAnchor:   function (file) { return form('/upload/anchor',   fd('file', file)); },
    uploadPackshot: function (file) { return form('/upload/packshot', fd('file', file)); },

    // Option 2: a .zip of frames OR any number of individual images, kept in order.
    // -> {count, items:[{id,label,localPath}]}
    uploadOwnFrames: function (files) {
      var fd_ = new FormData();
      for (var i = 0; i < files.length; i++) fd_.append('files', files[i]);
      return form('/upload/frames', fd_);
    },

    // -- generation --
    // Each returns {items:[{id, jobId}]}; progress is read back via job().
    generateFrames: function ()         { return post('/generate/frames'); },
    generateMotion: function (settings) { return post('/generate/motion', settings); },
    generateSong:   function (payload)  { return post('/generate/song', payload); },

    // Per-item job poll. The backend must not return `localPath` until the asset is
    // downloaded into outputs/ — that ordering is what fixes the vanishing frames.
    // -> {state:'queued'|'generating'|'done'|'failed',
    //     localPath?, creditsConsumed?, error?, balance?}
    job: function (jobId) { return get('/jobs/' + encodeURIComponent(jobId)); },

    reroll: function (stage, itemId) { return post('/jobs/reroll', { stage: stage, itemId: itemId }); },
    retry:  function (stage, itemId) { return post('/jobs/retry',  { stage: stage, itemId: itemId }); },

    // -- run persistence --
    saveRun:   function (runState) { return post('/run/save', runState); },
    loadRun:   function ()         { return get('/run/load'); },          // -> run state or null
    downloadAll: function ()       { return post('/run/zip'); }           // -> {localPath}
  };

  function fd(field, file) { var f = new FormData(); f.append(field, file); return f; }

  global.api = api;
})(window);
