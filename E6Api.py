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
    """
    Initializes the api.

    Args:
        threadedWorkers:int     How many workers to allocate for downloads. (default: 8)
    """
    global executor
    if executor: executor.shutdown(True)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threadedWorkers)

def setApiAuth(user,api):
    """
    Sets authorization.
    
    Args:
        user:str        The username to authenticate as.
        api:str         The API key to use to authenticate.
    
    Returns:
        success:bool    Whether or not it set the authorization.
    """
    global auth,dfhead
    if user == "" or api == "": return False
    dfhead["Authorization"] = "Basic " + base64.b64encode(f"{user}:{api}".encode()).decode()
    auth = requests.auth.HTTPBasicAuth(user,api)
    return True

def apiReq(endpoint:str,params:dict,service="https://e621.net",method="GET") -> tuple[bool,str|dict]:
    """
    Makes an arbitrary api request.

    Args:
        endpoint:str    The endpoint to request.
        params:dict     The parameters to pass.
        service:str     The service to send the request to.
        method:str      The method to use. (one of 'GET','POST','PUT','PATCH','DELETE')
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
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

def fetchResourceAsync(target,type="images",service="https://e621.net") -> concurrent.futures.Future:
    """
    Retrieves a file from a URL.

    Args:
        target:str                  The URL to the resource to retrieve.
        type:str                    The sub-directory to put the resultant resource in.
    
    Returns:
        future:Future               A future representing the call.
            future.result():str     A path to the file.
    """
    return executor.submit(fetchResource,target,type)

def fetchResource(target,type="images",service="https://e621.net"):
    """
    Retrieves a file from a URL.

    Args:
        target:str      The URL to the resource to retrieve.
        type:str        The sub-directory to put the resultant resource in.
    
    Returns:
        path:str        The resultant path of the file.
    """
    if target == None:
        return None
    element = target.split("/")[-1]
    path = tempfile.gettempdir().rstrip("/") + f"/esixterm/{type}/"
    os.makedirs(path,exist_ok=True)
    path += element
    if os.path.exists(path):
        return path
    if target.startswith("/"):
        # assuming this is relative!
        target = service + target
    r = requests.get(target,
                headers=dfhead)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    with open(path,"wb") as f:
        f.write(r.content)
    return path

def search(tags:list[str],limit=10,page=1,service:str=None):
    """
    Searches for posts.

    Args:
        tags:list[str]  A list of tags to search for.
        limit:int       The maximum number of posts to get. (default: 10)
        page:int        The page to retrieve posts from. (default: 1)
        service:str     The service to send the request to.
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
    success,body = apiReq("posts.json",{
        "limit":limit,
        "tags":" ".join(tags),
        "page":page
    },service=service)
    return success,body

def getPosts(ids:list[int],limit=10,page=1,service:str=None):
    """
    Searches for posts.

    Args:
        ids:list[int]   A list of ids to retrieve.
        limit:int       The maximum number of posts to get. (default: 10)
        page:int        The page to retrieve posts from. (default: 1)
        service:str     The service to send the request to.
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
    if len(ids) == 0: return True,{"posts":[]}
    tags = " ".join([f"~id:{x}" for x in ids])
    return apiReq("posts.json",{
        "limit":limit,
        "tags":tags,
        "page":page
    },service=service)

def getPost(id:int,service:str=None):
    """
    Gets a post.

    Args:
        id:int          The ID of the post to retrieve.
        service:str     The service to send the request to.
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
    return apiReq(f"posts/{id}.json",{},service=service)

def searchWiki(search:str,limit=10,service:str=None):
    """
    Searches for wiki posts.

    Args:
        search:str      Title search
        limit:int       How many results to retrieve.
        service:str     The service to send the request to.
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
    return apiReq(f"wiki_pages.json",{
        "search[title]":search,
        "limit":limit
    },service=service)

def getTag(id:int,service:str=None):
    """
    Gets a tag.

    Args:
        id:int          The ID of the tag to retrieve.
        service:str     The service to send the request to.
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
    return apiReq(f"tags/{id}.json",service=service)

def favoritePost(id:int,service:str=None):
    """
    Syncs a post favorite to the server.
    
    Args:
        id:int          The ID of the tag to retrieve.
        service:str     The service to send the request to.
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
    return apiReq(f"favorites.json",{"post_id":id},service=service,method="POST")

def unfavoritePost(id:int,service:str=None):
    """
    Removes a post favorite from the server.
    
    Args:
        id:int          The ID of the tag to retrieve.
        service:str     The service to send the request to.
    
    Returns:
        success:bool    Whether or not the request succeeded.
        data:str|dict   If success == false, the error message (str). If success == true, the JSON response.
    """
    return apiReq(f"favorites/{id}.json",{},service=service,method="DELETE")