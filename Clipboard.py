import platform,subprocess,os
from ColoredString import CString

def copytext(text:str):
    match platform.system():
        case "Darwin":
            from AppKit import NSPasteBoard, NSPasteboardTypeString
            pb = NSPasteBoard.generalPasteboard()
            pb.clearContents()
            pb.setString_forType_(text,NSPasteboardTypeString)
        case "Linux":
            match os.environ.get("XDG_SESSION_TYPE","none"):
                case "wayland":
                    proc = subprocess.Popen(
                        ["wl-copy"],
                        stdin=subprocess.PIPE,
                        start_new_session=True
                    )
                    proc.stdin.write(text.encode())
                    proc.stdin.close()
                case "x11":
                    proc = subprocess.Popen(
                        ["xclip","-selection","clipboard","-i"],
                        stdin=subprocess.PIPE,
                        start_new_session=True
                    )
                    proc.stdin.write(text.encode())
                    proc.stdin.close()
                case _:
                    print(CString("§34§Cannot copy to clipboard when not in a X11 or wayland session!"))
                    return
        case _:
            print(CString("§34§Cannot copy to clipboard on Windows or Jython! (macOS support is untested)"))

def copyfile(path:str):
    # ext = path.split(".")[-1]
    # if ext == "svg": ext = "svg+xml"
    # if ext == "ico": ext = "vnd.microsoft.icon"
    # if ext == "jpg": ext = "jpeg"
    # if ext == "tif": ext = "tiff"
    # mime = f"image/{ext}"
    match platform.system():
        case "Darwin":
            from AppKit import NSPasteboard
            from Foundation import NSURL
            pb = NSPasteboard.generalPasteboard()
            pb.clearContents()
            url = NSURL.fileURLWithPath_(path)
            pb.writeObjects_([url])
        case "Linux":
            url = "file://" + path
            match os.environ.get("XDG_SESSION_TYPE","none"):
                case "wayland":
                    proc = subprocess.Popen(
                        ["wl-copy","--type","text/uri-list"],
                        stdin=subprocess.PIPE,
                        start_new_session=True
                    )
                    proc.stdin.write((url + "\n").encode())
                    proc.stdin.close()
                case "x11":
                    proc = subprocess.Popen(
                        ["xclip","-selection","clipboard","-t","text/uri-list","-i"],
                        stdin=subprocess.PIPE,
                        start_new_session=True
                    )
                    proc.stdin.write((url + "\n").encode())
                    proc.stdin.close()
                case _:
                    print(CString("§34§Cannot copy to clipboard when not in a X11 or wayland session!"))
                    return
        case _:
            print(CString("§34§Cannot copy to clipboard on Windows or Jython! (macOS support is untested)"))