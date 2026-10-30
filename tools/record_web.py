"""Record a web app as PNG frames while scripted steps run (for a README demo GIF).

usage:
  uv run --with playwright python record_web.py <url> <frames_dir> [--size 1120x700] [--dpr 1]
         [--steps "waitfor:#btn:not([disabled]);wait:1.5;click:#btn;wait:2"]
         [--serve-cdn "https://cdn.jsdelivr.net/npm/pkg@1.0.0/dist/=C:/path/to/package/dist"]

steps (separated by ';'):
  wait:<sec>            keep recording
  waitfor:<css>         wait (not recorded) until the element exists
  click:<css>           click
  type:<css>=<text>     clear the field and type slowly, recorded key by key
  scroll:<px>           mouse-wheel scroll
  goto:<path>           open <url>/<path>; write the path WITHOUT a leading '/' (Git Bash rewrites /paths)
  shot:<file.png>       also save one full screenshot (e.g. for the hero image)
--serve-cdn serves a CDN prefix from a local folder (npm pack + extract) when headless Chromium cannot reach it.
Chromium: uses Playwright's bundled browser, or the newest ~/AppData/Local/ms-playwright/chromium-* if present.
"""
import argparse, glob, os, time
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("url"); ap.add_argument("out")
ap.add_argument("--size", default="1120x700"); ap.add_argument("--dpr", type=float, default=1)
ap.add_argument("--steps", default="wait:2"); ap.add_argument("--fps", type=int, default=10)
ap.add_argument("--serve-cdn", action="append", default=[])
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
W, H = map(int, a.size.split("x"))
n = 0

def grab(page, seconds):
    global n
    end = time.time() + seconds
    while time.time() < end:
        t = time.time()
        page.screenshot(path=os.path.join(a.out, f"{n:04d}.png")); n += 1
        time.sleep(max(0, 1 / a.fps - (time.time() - t)))

def cdn_route(prefix, folder):
    def handle(route):
        path = os.path.join(folder, route.request.url[len(prefix):].split("?")[0])
        types = {".wasm": "application/wasm", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css"}
        if os.path.exists(path):
            route.fulfill(path=path, content_type=types.get(os.path.splitext(path)[1], "application/octet-stream"))
        else:
            route.abort()
    return handle

local = sorted(glob.glob(os.path.expanduser("~/AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe")))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=local[-1]) if local else p.chromium.launch()
    page = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=a.dpr)
    for spec in a.serve_cdn:
        prefix, folder = spec.split("=", 1)
        page.route(prefix + "**", cdn_route(prefix, folder))
    page.goto(a.url, wait_until="domcontentloaded", timeout=60000)
    for step in filter(None, a.steps.split(";")):
        kind, _, arg = step.partition(":")
        if kind == "wait":
            grab(page, float(arg)); continue
        if kind == "waitfor":
            page.wait_for_selector(arg, timeout=60000); continue
        if kind == "click":
            page.click(arg)
        elif kind == "type":
            sel, _, text = arg.rpartition("=")  # last '=': selectors like input[name=x] contain one
            box = page.locator(sel); box.fill(""); grab(page, 0.2)
            for ch in text:
                box.type(ch); grab(page, 0.12)
        elif kind == "scroll":
            page.mouse.wheel(0, int(arg))
        elif kind == "goto":
            page.goto(a.url.rstrip("/") + "/" + arg.lstrip("/"), wait_until="domcontentloaded")
        elif kind == "shot":
            page.screenshot(path=arg); continue
        grab(page, 0.4)
    b.close()
assert n, "no frames recorded: add a wait:<sec> step"
print(n, "frames ->", a.out)
