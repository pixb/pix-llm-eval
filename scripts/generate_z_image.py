#!/usr/bin/env python3
"""
generate_z_image.py — POST a prompt to the z-image n8n webhook, save result.png.

Usage:
  python3 scripts/generate_z_image.py prompt.txt result.png
  python3 scripts/generate_z_image.py prompt.txt result.png --width 1920 --height 1080

Webhook URL resolution (first match wins):
  1. --url argument
  2. N8N_WEBHOOK_URL env var (or repo-root .env)
  3. http://localhost:5678/webhook/z-image
"""
import argparse
import json
import os
import sys
import time
import urllib.request

DEFAULT_URL = "http://localhost:5678/webhook/z-image"
TIMEOUT = 600


def _load_env_file(path):
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def resolve_url(cli_url):
    if cli_url:
        return cli_url
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _load_env_file(os.path.join(repo_root, ".env"))
    return os.environ.get("N8N_WEBHOOK_URL", DEFAULT_URL)


def main():
    parser = argparse.ArgumentParser(description="Generate an image via n8n z-image webhook (body POST)")
    parser.add_argument("prompt_file", help="text file containing the prompt")
    parser.add_argument("output_png", help="path to save the downloaded PNG")
    parser.add_argument("--url", default=None, help="webhook URL override")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()

    with open(args.prompt_file, encoding="utf-8") as f:
        prompt = f.read().strip()
    if not prompt:
        sys.exit(f"empty prompt: {args.prompt_file}")

    url = resolve_url(args.url)
    print(f"webhook: {url}")
    body = json.dumps({"prompt": prompt, "width": args.width, "height": args.height}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")

    t0 = time.time()
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    print(f"webhook returned ({time.time() - t0:.1f}s): code={result.get('code')}")

    if result.get("code") != 200 or not result.get("image_url"):
        sys.exit(f"webhook error: {result}")

    out_dir = os.path.dirname(os.path.abspath(args.output_png))
    os.makedirs(out_dir, exist_ok=True)
    with urllib.request.urlopen(result["image_url"], timeout=TIMEOUT) as resp:
        data = resp.read()
    if len(data) < 100:
        sys.exit(f"image too small ({len(data)} bytes)")
    with open(args.output_png, "wb") as f:
        f.write(data)
    print(f"saved: {args.output_png} ({len(data) / 1024:.0f}KB)")


if __name__ == "__main__":
    main()
