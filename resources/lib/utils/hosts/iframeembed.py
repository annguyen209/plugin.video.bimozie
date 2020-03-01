import re, json, base64, xbmcgui
from utils.mozie_request import Request
from urlparse import urlparse
from urllib import urlencode


def get_link(url, media):
    request = Request()
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc
    header = {
            'Referer': media.get('originUrl'),
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Origin': base_url
        }

    resp = request.get(url, headers=header)

    print resp
    sources = re.search(r'sources\s?[=:]\s?(\[.*?\])', resp)
    if sources:
        sources = json.loads(sources.group(1))
        if len(sources) > 1:
            listitems = []
            for i in sources:
                listitems.append("%s (%s)" % (i.get('label'), i.get('file')))
            index = xbmcgui.Dialog().select("Select stream", listitems)
            if index == -1:
                return None, None
            else:
                return sources[index].get('file') + "|%s" % urlencode(header), sources[index].get('label')
        else:
            return sources[0].get('file') + "|%s" % urlencode(header), sources[0].get('label')

    return None, None
