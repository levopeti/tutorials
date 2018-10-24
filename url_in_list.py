import re
import urllib.request
import urllib.error
import sys
import time
from collections import OrderedDict


def crawl(url):
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]

    else:
        print('Incorrect Playlist.')
        exit(1)

    try:
        yTUBE = urllib.request.urlopen(url).read()
        sTUBE = str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)
    # it = re.finditer(tmp_mat, sTUBE)
    # mat = []
    # try:
    #     while True:
    #         mat.append(next(it))
    # except StopIteration:
    #     pass
    print(len(mat))
    if mat:
        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])

        all_url = list(OrderedDict.fromkeys(final_url))

        i = 0
        while i < len(all_url):
            # sys.stdout.write(all_url[i] + '\n')
            time.sleep(0.04)
            i = i + 1

        print(len(all_url))
        return all_url
    else:
        print('No videos found.')
        exit(1)


if __name__ == '__main__':
    url = 'https://www.youtube.com/playlist?list=PLCQyA4-pzVUQaV0K8GeLtqy3Rk27kmGqE'

    if 'http' not in url:
        url = 'http://' + url
    crawl(url)


