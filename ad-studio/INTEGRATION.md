# kie Ad Studio — renderer integration contract

The renderer in `renderer/` is complete and matches the approved preview. It reaches the
backend **only** through `renderer/api.js`; `app.js` never calls `fetch` itself. To wire this
to the existing kie pipeline, implement the routes below (or rewrite `api.js`'s bodies to call
your existing functions / Electron IPC directly — the function names and return shapes are the
contract, the HTTP transport is not).

Every response is JSON. Non-2xx should carry `{"error": "..."}`; the renderer surfaces that
string in a red toast.

## The two bug fixes — what the backend must guarantee

### 1. Frames show then vanish

kie's asset URLs are short-lived signed links. The renderer now **refuses** to render anything
that is not a local path: `api.assetUrl()` throws on `http(s)://`, protocol-relative and `data:`
URIs (see `test/asseturl.test.js`). So the backend must, on every completed generation:

1. Poll kie until the job reports complete.
2. **Download the asset bytes into `outputs/` first.**
3. Only then report `state: "done"` with a `localPath` relative to `outputs/`.

A job must never return `state: "done"` while the asset still only exists at a kie URL — that
ordering *is* the fix. If the download fails, report `state: "failed"` with the reason; the tile
then shows red with a one-click Retry.

`localPath` is relative to the `outputs/` root (`beat01.png`, or `frames/beat01.png`). The
renderer prefixes `/outputs/` itself, so `outputs/` must be served as a static route.

### 2. Stale UI

- Serve `outputs/` **and** the renderer files with
  `Cache-Control: no-cache, no-store, must-revalidate`.
- Return a `version` (any changing value — mtime or timestamp) alongside `localPath`. The
  renderer appends it as `?v=` so a re-roll that overwrites the same path still repaints.

## Routes

### Key + credits
| Route | Body | Returns |
|---|---|---|
| `GET /api/key` | — | `{present: bool}` |
| `POST /api/key` | `{key}` | `{present: true}` |
| `GET /api/credits` | — | `{balance: number}` |

`POST /api/key` must hand the key to secure storage and **never** return it. The renderer clears
its input immediately and keeps no copy.

### Prompt files (multipart, field `file`)
| Route | Returns |
|---|---|
| `POST /api/prompts/frames` | `{name, count, hasAnchor, unitCost?, items:[{id,label?,kind?}]}` |
| `POST /api/prompts/motion` | `{name, count, items:[{id,label?,kind?}]}` |
| `POST /api/prompts/song` | `{name, style?, lyrics?, model?, vocal?}` |

`unitCost` drives the Stage 1 estimate (defaults to 15 if omitted). `hasAnchor` lights the
`anchor ✓` chip.

### Stage 1 uploads
| Route | Body | Returns |
|---|---|---|
| `POST /api/upload/anchor` | multipart `file` | `{name, width, height, localPath, version?}` |
| `POST /api/upload/packshot` | multipart `file` | `{name, width, height, localPath, version?}` |
| `POST /api/upload/frames` | multipart `files` (repeated) | `{count, items:[{id,label?,localPath,version?}]}` |

`/upload/frames` is Option 2 and receives **either** a single `.zip` **or** N image files.
Expand a zip server-side and return the frames in playback order (sort entries naturally —
`beat2` before `beat10`). Items come back already `done`, cost 0, and skip generation entirely.

### Generation
| Route | Body | Returns |
|---|---|---|
| `POST /api/generate/frames` | `{}` | `{items:[{id, jobId, label?}]}` |
| `POST /api/generate/motion` | `{model,res,dur,asp,sound}` | `{items:[{id, jobId, label?}]}` |
| `POST /api/generate/song` | `{model,vocal,style,lyrics}` | `{jobId}` |
| `GET /api/jobs/:jobId` | — | see below |
| `POST /api/jobs/reroll` | `{stage,itemId}` | `{jobId}` |
| `POST /api/jobs/retry` | `{stage,itemId}` | `{jobId}` |

Motion settings arrive as the raw control values: `model` is `kling`\|`veo`, `res` is
`std`\|`pro`\|`4k`, `dur` is `"5"`\|`"10"`, `asp` is `9:16`\|`1:1`\|`16:9`, `sound` is a boolean.
Map these onto the kie request the existing pipeline already builds.

**Job poll** returns one of:

```jsonc
{"state": "queued"}
{"state": "generating"}
{"state": "done",   "localPath": "beat01.png", "version": 1736432111,
                    "creditsConsumed": 15, "balance": 28962}
{"state": "failed", "error": "human-readable reason"}
```

`creditsConsumed` comes straight from kie's field of the same name and is what the credit logs
and the running spend counter use. Polls themselves are not billed, so only a `done` moves the
counter. `balance` is optional; when present the renderer treats it as authoritative.

### Run persistence
| Route | Body | Returns |
|---|---|---|
| `POST /api/run/save` | run snapshot | `{ok:true}` |
| `GET /api/run/load` | — | the snapshot, or `null` |
| `POST /api/run/zip` | `{}` | `{localPath}` |

The snapshot is opaque JSON — store and return it verbatim. On boot the renderer restores it and
re-attaches to any job still carrying a `jobId`; items that were mid-flight without one are
marked `interrupted — retry`.

## Local check

```bash
node test/asseturl.test.js     # asset-URL guard (no dependencies)
```
