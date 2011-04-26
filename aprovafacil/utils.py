from xml.dom import minidom
from xml.parsers.expat import ExpatError

__all__ = ['xmltodict', ]

def xmltodict(xmlstring):
    try:
        doc = minidom.parseString(grant_utf8(xmlstring))
        remove_whitespace_nodes(doc.documentElement)
        return elementtodict(doc.documentElement)
    except ExpatError:
        return {}

def grant_utf8(string):
    if isinstance(string, unicode):
        return string.encode('utf-8')

    try:
        string.decode('utf-8')
        return string

    except UnicodeDecodeError:
        return string.decode('latin-1').encode('utf-8')

def elementtodict(parent):
    child = parent.firstChild

    if child and (child.nodeType == minidom.Node.TEXT_NODE):
        return child.nodeValue.strip()

    d = {}
    while child is not None:
        if child.nodeType == minidom.Node.ELEMENT_NODE:
            key = str(child.tagName)
            e = elementtodict(child)

        if isinstance(e, (str, unicode)) and (e == 'None' or e == 'NULL'):
            e = None # WOP!!!
        if key not in d:
            d[key] = e
        elif not isinstance(d[key], list):
            d[key] = [d[key], e]
        else:
            d[key].append(e)

        child = child.nextSibling

    return d

def remove_whitespace_nodes(node, unlink=True):
    remove_list = []

    for child in node.childNodes:
        if child.nodeType == minidom.Node.TEXT_NODE and not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whitespace_nodes(child, unlink)

    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()

    return node
