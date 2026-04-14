#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Threezh1  (revised by GPT)

import os, sys, time, argparse, urllib3, requests, hashlib, urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Optional

# =============== 全局配置 ===============
START_DIR   = "/calculator-web/"                 # 限定只抓取该目录
DOMAIN      = "it.vazyme.com:8002"
START_URL   = f"https://{DOMAIN}{START_DIR}"
MAX_DEPTH   = 3                         # 向下递归深度
DELAY       = 0.5                       # 每次请求间隔(秒)
TIMEOUT     = 15
RETRY       = 3

# 关闭 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/125.0 Safari/537.36")
}

# ============ 工具函数 ============
def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

def abs_url(base: str, link: str) -> str:
    return urljoin(base, link).split("#")[0]

def in_scope(url: str) -> bool:
    """只保留 tools 目录下的 https 链接"""
    parsed = urlparse(url)
    return (parsed.scheme == "https" and
            parsed.netloc == DOMAIN and
            parsed.path.startswith(START_DIR))



def fetch(url: str) -> Optional[str]:
    """带重试的抓取"""
    for i in range(RETRY):
        try:
            time.sleep(DELAY)
            r = requests.get(url, headers=HEADERS,
                             timeout=TIMEOUT,
                             allow_redirects=True,
                             verify=False)
            if r.status_code == 200 and r.text.strip():
                return r.text
        except Exception as e:
            print(f"[retry {i+1}/{RETRY}] {url} ({e})")
    print(f"[error] {url}")
    return None

# ============ 保存文件 ============
def save_html(url: str, html: str):
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")
    if not path or path.endswith("/"):
        path += "index.html"
    safe_domain = DOMAIN.replace(":", "_")          # ← 关键修复
    local_file = Path("website") / safe_domain / path
    local_file.parent.mkdir(parents=True, exist_ok=True)
    local_file.write_text(html, encoding="utf-8")
    print(f"[saved] {local_file}")

# ============ 抓取逻辑 ============
def crawl(start: str, max_depth: int):
    visited = set()
    queue = [(start, 0)]

    while queue:
        url, depth = queue.pop(0)
        if depth > max_depth or url in visited:
            continue
        visited.add(url)

        html = fetch(url)
        if not html:
            continue

        save_html(url, html)

        if depth == max_depth:
            continue

        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            link = abs_url(url, a["href"])
            if in_scope(link) and link not in visited:
                queue.append((link, depth + 1))

# ============ 入口 ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default=START_URL,
                        help="起始 URL")
    parser.add_argument("-d", "--depth", type=int, default=MAX_DEPTH,
                        help="递归深度")
    args = parser.parse_args()

    print(f"开始抓取 {args.url}  (深度={args.depth})")
    crawl(args.url, args.depth)
    print("全部完成！文件保存在 website/ 目录")
    # 使用方式
    #python version 3.7
    #环境依赖项pip install requests beautifulsoup4 lxml
    # python sitecopy.py -u "https://www.novopro.cn/tools/" -d 2