
def url_concat(base, chunk):
    result = ""
    if base.endswith("/") and chunk.startswith("/"):
        result = base + chunk[1:]
    elif base.endswith("/") or chunk.startswith("/"):
        result = base+chunk
    else:
        result = base+"/"+chunk
    return result
