import typing,copy

import platformdirs as dirs
import json,os,consts

defaults = {}

def registerKey(key:str,value:typing.Any,kind:str="conf.json"):
    """
    Registers a default.
    
    Args:
        key:str     The key to give a default to.
        value:Any   The default value.
        kind:str    The config file to apply this to. (default: "conf.json")
    """
    if not kind in defaults:
        defaults[kind] = {}
    defaults[kind][key] = value

def getConfPath(kind="") -> str:
    """
    Returns the config path.
    
    Args:
        kind:str   The file to get the path to. If blank, gives the directory. (default: "")
    """
    return dirs.user_config_dir(appname=consts.app.id).rstrip("/")+"/"+kind

def getConfig(kind="conf.json") -> dict:
    """
    Gets a config, or creates it if it didn't exist.
    
    Args:
        kind:str    The config file to apply this to. (default: "conf.json")
    """
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

def saveConfig(conf:dict,kind="conf.json"):
    """
    Saves a config file.
    
    Args:
        conf:dict   A value representing the config file to be saved.
        kind:str    The config file to save to. (default: "conf.json")
    """
    if not isinstance(conf,dict):
        raise TypeError("Expected config to be a dictionary, but it wasn't.")
    configDir = getConfPath()
    configPath = getConfPath(kind)
    if not os.path.exists(configDir):
        os.makedirs(configDir,exist_ok=True)
    with open(configPath,"w") as f:
        json.dump(conf,f)