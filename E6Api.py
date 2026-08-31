import requests,requests.auth
import urllib.request
import consts
import tempfile
import os
import base64
import concurrent,concurrent.futures

executor = None

dfhead = {"User-Agent":f"{consts.app.id}/{consts.app.version} (by {consts.author.e621} on e621)"}

auth = None

def init(threadedWorkers=8):
    global executor
    if executor: executor.shutdown(True)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threadedWorkers)

def setApiAuth(user,api):
    global auth,dfhead
    if user == "" or api == "": return False
    dfhead["Authorization"] = "Basic " + base64.b64encode(f"{user}:{api}".encode()).decode()
    auth = requests.auth.HTTPBasicAuth(user,api)
    return True

def apiReq(endpoint,params,service="https://e621.net",method="GET"):
    if service == None:
        service = "https://e621.net"
    r = requests.request(
        method,
        f"{service.rstrip('/')}/{endpoint}",
        headers=dfhead,
        params=params,
        auth=auth,
        allow_redirects=False)
    if r.status_code >= 300:
        errs = {
            301:"Permanently Moved",
            400:"Bad Request",
            401:"Unauthorized",
            403:"Forbidden; possibly missing User-Agent",
            404:"Not Found",
            405:"Method not allowed",
            406:"Format not allowed",
            410:"Gone",
            412:"Precondition failed",
            422:"Unprocessable; bad request",
            429:"Rate limited",
            500:"Internal Server Error",
            502:"Bad Gateway",
            503:"Server overloaded and/or ratelimited.",
            520:"Unknown Error",
            522:"Origin Timeout (down)",
            524:"Origin Timeout (overloaded)",
            525:"SSL Handshake Failed"
        }
        if not r.status_code in errs:
            return False,f"Unknown Error ({r.status_code})"
        return False,errs[r.status_code]
    else:
        return True,r.json()

def fetchResourceAsync(target) -> concurrent.futures.Future:
    return executor.submit(fetchResource,target)

def fetchResource(target):
    if target == None:
        return None
    element = target.split("/")[-1]
    path = tempfile.gettempdir().rstrip("/") + "/esixterm/images/"
    os.makedirs(path,exist_ok=True)
    path += element
    r = requests.get(target,
                 headers=dfhead)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    with open(path,"wb") as f:
        f.write(r.content)
    return path

def search(tags:list[str],limit=10,page=1,service:str=None):
    success,body = apiReq("posts.json",{
        "limit":limit,
        "tags":" ".join(tags),
        "page":page
    },service=service)
    return success,body

def getPost(id:int):
    return apiReq(f"posts/{id}.json",{})

def searchWiki(search:str,limit=10):
    return apiReq(f"wiki_pages.json",{
        "search[title]":search,
        "limit":limit
    })