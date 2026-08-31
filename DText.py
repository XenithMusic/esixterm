import webcolors,Colors,re

def rgb_distance_squared(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2))

def rgbToNearWebcolorName(rgb1):
    map = webcolors._conversion._get_name_to_hex_map(webcolors.HTML4)
    closest = "white"
    distance = 999999
    for k,v in map.items():
        rgb2 = webcolors.hex_to_rgb(v)
        dist = rgb_distance_squared([rgb1.red,rgb1.green,rgb1.blue],[rgb2.red,rgb2.green,rgb2.blue])
        if dist < distance:
            distance = dist
            closest = k
    return closest

def renderDText(dtext:str) -> str:
    dtext = dtext.replace("[[","[wikilink]&lsqb;&lsqb;")
    dtext = dtext.replace("]]","&rsqb;&rsqb;[/wikilink]")
    depth = {
        "color":[""],
        "b":[""],
        "i":[""],
        "s":[""],
        "u":[""],
        "spoiler":[""],
        "quote":[""],
        "wikilink":[""]
    }
    simples = {
        "b":"b",
        "i":"i",
        "s":"s",
        "u":"u",
        "spoiler":"90;100",
        "wikilink":"31"
    }
    indentation = 0
    simpleReverses = ["quote","section","color"]
    final = ""
    def addTag(final):
        final += "§"
        for i in depth.values():
            final += i[-1]
        final += "§"
        return final
    while len(dtext) >= 1:
        # add text before first [ to final, advance dtext
        if not "[" in dtext:
            final = addTag(final)
            final += dtext
            dtext = ""
            break
        rem = dtext.index("[")
        if (dtext[:rem].count("`")%2 == 1):
            remmats = re.finditer(r"(?<!\\)(\\\\)*`",dtext)
            next(remmats,None) # first (discard)
            mat = next(remmats,None) # second (i want this one)
            if mat:
                rem = mat.start()
                final = addTag(final)
                final += dtext[:rem+1]
                dtext = dtext[rem+1:]
                continue

        if (dtext[:rem] != ""):
            final = addTag(final)
            final += dtext[:rem].replace("\n","\n" + " "*indentation)
        dtext = dtext[rem+1:]
        # get the tag, place it in tag, advance dtext
        rem = dtext.index("]")
        tag = dtext[:rem].split("=")
        dtext = dtext[rem+1:]
        # parse tag
        tagName = tag[0].split(",")[0]
        tagValues = tag[1:]
        if "section" in tagName:
            tagName = tagName.replace("section","quote").replace(",expanded","")
            if len(tagValues) != 0:
                title = "=".join(tagValues)
                dtext = f"▼ << {title.replace('\n','')} >>\n\n" + dtext
            tagValues = ["blue"]
        if tagName in simples:
            depth[tagName].append(simples[tagName])
        elif tagName.startswith("/") and \
            (tagName[1:] in simples or tagName[1:] in simpleReverses):
            depth[tagName[1:]].pop()
        match tagName:
            case "quote":
                indentation += 2
                final += "\n"
                dtext = " "*indentation + dtext
                col = "107d"
                if len(depth["quote"])%2 == 0:
                    col = "100"
                depth["quote"] += [col]
            case "/quote":
                indentation -= 2
                final += "\n"
            case "color":
                if len(tagValues) == 1:
                    colors = {
                        "white":"37",
                        "silver":"97",
                        "gray":"90",
                        "black":"30",
                        "red":"31",
                        "maroon":"91",
                        "yellow":"33",
                        "olive":"93",
                        "lime":"32",
                        "green":"92",
                        "aqua":"36",
                        "teal":"96",
                        "blue":"34",
                        "navy":"94",
                        "fuchsia":"35",
                        "purple":"95",
                    }
                    if tagValues[0] in Colors.tagColors:
                        depth["color"].append(Colors.tagColors[tagValues[0]])
                    else:
                        webcolorName = "white"
                        if tagValues[0].startswith("#"):
                            webcolorName = rgbToNearWebcolorName(webcolors.hex_to_rgb(tagValues[0]))
                        else:
                            webcolorName = rgbToNearWebcolorName(webcolors.name_to_rgb(tagValues[0]))
                        depth["color"].append(colors[webcolorName])
                else:
                    pass
            case _:
                pass
    final = final.replace("&rsqb;","]").replace("&lsqb;","[")
    return final