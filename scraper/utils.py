def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    endline = re.compile('<br>')
    remove_endline = re.sub(endline, '\n', text)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', remove_endline)