# HW Scraper - Hacker-Style Proxy Scraper
# Author: Naman

import requests
import re
import os
import threading
import concurrent.futures
from bs4 import BeautifulSoup
from colorama import init, Fore

init(autoreset=True)

SAVE_FILE = "proxies.txt"
ALL_RAW_FILE = "all_scraped.txt"
HEADERS = {"User-Agent": "Mozilla/5.0"}

SOURCES = {
    "ProxyScrape": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country=all",
    "FreeProxyList": "https://free-proxy-list.net/",
    "Spys.one": "https://spys.one/en/http-proxy-list/",
    "ProxyListDownload": "https://www.proxy-list.download/api/v1/get?type=http",
    "OpenProxySpace": "https://openproxy.space/list/http",
    "Geonode Free": "https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc",
    "Proxifly HTTP": "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt"
}

def banner():
    print(Fore.GREEN + r'''
██╗  ██╗██╗    ██╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██║  ██║██║    ██║    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
███████║██║ █╗ ██║    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██╔══██║██║███╗██║    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║  ██║╚███╔███╔╝    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═╝  ╚═╝ ╚══╝╚══╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝ by Naman
''')

def get_proxies_from_source(name, url):
    proxies = set()
    print(Fore.YELLOW + f"[*] Scraping from {name}...")

    try:
        if "proxyscrape" in url or "proxy-list.download" in url or "proxifly" in url:
            r = requests.get(url, headers=HEADERS)
            proxies.update(re.findall(r"(\d+\.\d+\.\d+\.\d+:\d+)", r.text))

        elif "free-proxy-list" in url:
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find("table", id="proxylisttable")
            if table:
                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 7 and cols[6].text.strip().lower() == "yes":
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        proxies.add(f"{ip}:{port}")
            else:
                print(Fore.RED + f"[!] Could not find proxy table on FreeProxyList")

        elif "spys.one" in url:
            r = requests.post(url, headers=HEADERS, data={'xpp': '5', 'xf1': '0', 'xf2': '0', 'xf4': '0', 'xf5': '1'})
            matches = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+", r.text)
            proxies.update(matches)

        elif "openproxy.space" in url:
            r = requests.get(url, headers=HEADERS)
            matches = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+", r.text)
            proxies.update(matches)

        elif "geonode" in url:
            r = requests.get(url, headers=HEADERS)
            data = r.json()
            for proxy in data['data']:
                if 'http' in proxy.get('protocols', []):
                    proxies.add(f"{proxy['ip']}:{proxy['port']}")

    except Exception as e:
        print(Fore.RED + f"[!] Error scraping {name}: {e}")

    return proxies

def check_proxy(proxy):
    test_urls = ["http://icanhazip.com", "https://icanhazip.com", "http://httpbin.org/ip"]
    for url in test_urls:
        try:
            r = requests.get(url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
            if r.status_code == 200:
                return True
        except:
            continue
    return False

def save_proxies(proxies):
    with open(SAVE_FILE, "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    print(Fore.GREEN + f"\n[+] Saved {len(proxies)} working proxies to {SAVE_FILE}")

def save_all_scraped(proxies):
    with open(ALL_RAW_FILE, "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    print(Fore.BLUE + f"[i] Saved all scraped proxies to {ALL_RAW_FILE}")

def scrape_all():
    all_proxies = set()
    threads = []

    def collect(name, url):
        result = get_proxies_from_source(name, url)
        all_proxies.update(result)

    for name, url in SOURCES.items():
        t = threading.Thread(target=collect, args=(name, url))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(Fore.CYAN + f"\n[*] Total scraped proxies: {len(all_proxies)}")
    return all_proxies

def filter_working(proxies):
    print(Fore.MAGENTA + "[*] Checking proxies for validity...\n")
    working = []

    def tester(p):
        if check_proxy(p):
            print(Fore.GREEN + f"[+] WORKING: {p}")
            working.append(p)
        else:
            print(Fore.RED + f"[-] DEAD: {p}")

    # Use ThreadPoolExecutor to limit threads and avoid crash
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(tester, proxies)

    return working

def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    scraped = scrape_all()
    save_all_scraped(scraped)
    working = filter_working(scraped)
    save_proxies(working)

if __name__ == "__main__":
    main()