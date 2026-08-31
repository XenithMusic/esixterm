import typing,copy

import platformdirs as dirs
import json,os,consts

defaults = {}

def registerKey(key:str,value:typing.Any,kind="conf.json"):
    if not kind in defaults:
        defaults[kind] = {}
    defaults[kind][key] = value

def getConfPath(extra=""):
    return dirs.user_config_dir(appname=consts.app.id).rstrip("/")+"/"+extra

def getConfig(kind="conf.json"):
    configPath = getConfPath(kind)
    if not os.path.exists(configPath):
        conf = copy.deepcopy(defaults[kind])
        saveConfig(conf,kind=kind)
    else:
        conf = copy.deepcopy(defaults[kind])
        with open(configPath,"r") as f:
            jd = json.load(f)
        if not isinstance(jd,dict):
            raise TypeError("Expected config to be a JSON object (enclosed with curly braces), but it wasn't.")
        for k,v in jd.items():
            conf[k] = v
        shouldSave = len([x for x in defaults[kind].keys() if not x in jd]) > 0
        if shouldSave:
            saveConfig(conf,kind=kind)
    return conf

def saveConfig(conf,kind="conf.json"):
    if not isinstance(conf,dict):
        raise TypeError("Expected config to be a dictionary, but it wasn't.")
    configDir = getConfPath()
    configPath = getConfPath(kind)
    if not os.path.exists(configDir):
        os.makedirs(configDir,exist_ok=True)
    with open(configPath,"w") as f:
        json.dump(conf,f)