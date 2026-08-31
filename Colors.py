from ColoredString import CString

tagColors = {
    "invalid":"41db",
    "artist":"103bd",
    "copyright":"45db",
    "contributor":"90b",
    "character":"32",
    "species":"91",
    "general":"97",
    "meta":"37",
    "lore":"92b"
}

def colorRating(str):
    ratings = {
        "s":"§32§Safe",
        "q":"§33§Questionable",
        "e":"§31b§Explicit"
    }
    if str == "safe": str = "s"
    if str == "questionable": str = "q"
    if str == "explicit": str = "e"
    if str == "x": str = "e"
    return ratings[str]

def tagUrl(str):
    return f"https://e621.net/wiki_pages?search%5Btitle%5D={str}"
def tagInvalid(str):
    url = tagUrl(str)
    col = tagColors["invalid"]
    return CString(f"§{col}|{url}§{str}")
def tagArtist(str):
    url = tagUrl(str)
    col = tagColors["artist"]
    return CString(f"§{col}|{url}§{str}")
def tagCopyright(str):
    url = tagUrl(str)
    col = tagColors["copyright"]
    return CString(f"§{col}|{url}§{str}")
def tagContributor(str):
    url = tagUrl(str)
    col = tagColors["contributor"]
    return CString(f"§{col}|{url}§{str}")
def tagCharacter(str):
    url = tagUrl(str)
    col = tagColors["character"]
    return CString(f"§{col}|{url}§{str}")
def tagSpecies(str):
    url = tagUrl(str)
    col = tagColors["species"]
    return CString(f"§{col}|{url}§{str}")
def tagGeneral(str):
    url = tagUrl(str)
    col = tagColors["general"]
    return CString(f"§{col}|{url}§{str}")
def tagMeta(str):
    url = tagUrl(str)
    col = tagColors["meta"]
    return CString(f"§{col}|{url}§{str}")
def tagLore(str):
    url = tagUrl(str)
    col = tagColors["lore"]
    return CString(f"§{col}|{url}§{str}")