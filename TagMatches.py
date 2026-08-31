import shlex


def getAllTags(post:dict) -> list[str]:
    final = []
    for i in post["tags"].values():
        final += i
    return final

def matchTag(tags:list[str],post:dict,match:str) -> bool:
    tag = match.lstrip("~-")
    if ":" in tag:
        rightaliases = {
            "yes":"true",
            "no":"false"
        }
        left,_,right = tag.partition(":")
        if right in rightaliases: right = rightaliases[right]
        tag = ":".join([left,right])
        aliases = {
            "ischild:true":"parent:any",
            "isparent:true":"child:any",
            "hasparent:true":"parent:any",
            "haschild:true":"child:any",

            "ischild:false":"parent:none",
            "isparent:false":"child:none",
            "hasparent:false":"parent:none",
            "haschild:false":"child:none",

            "inpool:true":"pool:any",
            "inpool:false":"pool:none"
        }
        if tag in aliases: tag = aliases[tag]
        left,_,right = tag.partition(":")
        simple = {
            "id":("id","range"),
            "score":("score.total","range"),
            "favcount":("fav_count","range"),
            "comment_count":("comment_count","range"),
            "rating":("rating","equal"),
            "type":("file.ext","equal"),
            "width":("file.width","range"),
            "height":("file.height","range"),
            "filesize":("file.size","range"),
            "source":("sources","contains"),
            "description":("description","contains"),
            "parent":("relationships.parent_id","equal"),
            "child":("relationships.children","contains"),
            "pool":("pools","contains"),
        }
        aliases = {
            "_all":{},
            "rating":{
                "safe":"s",
                "questionable":"q",
                "explicit":"e",
                "x":"e"
            }
        }
        aliases["_all"].update(aliases.get(left,{}))
        for i,v in aliases["_all"].items():
            if right == i: right = v
        if left in simple:
            key,mode = simple[left]
            value = post
            key = key.split(".")
            for i in key:
                value = value[i]
            match mode:
                case "equal":
                    equalSimples = {
                        "any":lambda v,r : v != 0,
                        "none":lambda v,r : v == 0
                    }
                    for i,v in equalSimples.items():
                        if right == i: return v(value,right)
                    return any(x == value for x in right.split(","))
                case "contains":
                    containsSimples = {
                        "any":lambda v,r : len(v) != 0,
                        "none":lambda v,r : len(v) == 0
                    }
                    for i,v in containsSimples.items():
                        if right == i: return v(value,right)
                    return any(x in value for x in right.split(","))
                case "range":
                    def pv(val:str) -> int:
                        mul = 1
                        appliedmul = 1
                        for size in ["kb","mb","gb","tb"]:
                            appliedmul *= 1024
                            if size in val.lower():
                                mul *= appliedmul
                                val = val.lower().replace(size,"")
                        if not val.isdigit(): return 0
                        return int(val)*mul
                    rangeSimples = {
                        ">=":lambda v,r : v >= r,
                        ">":lambda v,r : v > r,
                        "<=":lambda v,r : v <= r,
                        "<":lambda v,r : v < r,
                        "any":lambda v,r : v != 0,
                        "none":lambda v,r : v == 0,
                    }
                    for i,v in rangeSimples.items():
                        if right.startswith(i):
                            return v(value,pv(right.replace(i,"")))
                    if ".." in right:
                        range1,_,range2 = right.partition("..")
                        range1,range2 = (pv(x) for x in (range1,range2))
                        if value >= range1 and value <= range2:
                            return True
                    else:
                        return any(value == pv(x) for x in right.split(","))
                case _:
                    return False
    hit = tag in tags
    return hit

def matchTags(post:dict,match:list[str],whenEmpty=True) -> bool:
    if len(match) == 0:
        return whenEmpty
    tags = getAllTags(post)
    negationTags = [x.replace("-","~") for x in match if x.startswith("-")]
    if matchTags(post,negationTags,whenEmpty=False):
        print("matched negation")
        return False
    match = [x for x in match if not x.startswith("-")]
    anyMatched = False
    for i in match:
        if i.startswith("~") and anyMatched:
            continue
        sanitized = i.replace("~","")
        matches = matchTag(tags,post,sanitized)
        if i.startswith("~") and matches:
            anyMatched = True
            continue
        elif not matches and not i.startswith("~"):
            return False
    if len([x for x in match if x.startswith("~")]) != 0:
        return anyMatched
    return True

def matchAnyTagQualifier(post:dict,matches:list[str],whenEmpty=True) -> bool:
    matches = [shlex.split(x) for x in matches if not x.startswith("!")]
    return any([matchTags(post,x,whenEmpty) for x in matches])