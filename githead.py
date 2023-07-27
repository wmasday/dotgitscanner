from fake_useragent import UserAgent
import requests
import re
import sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

confVerify = True
confAllowRedirect = False
confTimeout = 15
confPayload = ''
confDebug = False

def debug(url, err):
    if confDebug == True:
        if 'ConnectTimeout' in err:
            open('dotgitscanner_ConnectTimeout.log', 'a').write(f'[ERR] {url} : {err}\n')
        elif 'ConnectionError' in err:
            open('dotgitscanner_ConnectionError.log', 'a').write(f'[ERR] {url} : {err}\n')
        else:
            open('dotgitscanner_dbug.log', 'a').write(f'[ERR] {url} : {err}\n')
    else:pass

def exploit(url):
    if 'http://' not in url:
        url = 'http://'+ url
    else:
        url = url
    
    try:
        UserAgent = UserAgent().chrome
    except:
        UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    
    confHeaders = {
        "User-Agent": str(UserAgent),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": str(url),
        "Origin": str(url)
    }
    
    try:
        print (f'[!] [ GIT HEAD ] Check : {url}')
        check = requests.get(url +'/.git/HEAD', headers=confHeaders, timeout=confTimeout, allow_redirects=confAllowRedirect)
        if "refs/heads" in check.text or 'refs/heads' in str(check.content):
            print (f"   [ VULN ] GIT HEAD => {url}")
            open('dotgitscanner.txt', 'a').write(f"{url}\n")
        else:pass
            
    except Exception as err:
        debug(url, str(err))
        
     

def init():
    sitelist = input(" Sitelist : ")
    thread = input(" Thread : ")
    if sitelist == "":
        print("[!] Put Sitelist!")
        init()
    else:
        try:
            sites = open(sitelist, "r").read().splitlines()
            try:
                pp = Pool(int(thread))
                pp.map(exploit, sites)
            except:
                pass
        except:
            print("[!] Sitelist not found!")
            sys.exit()

init()
