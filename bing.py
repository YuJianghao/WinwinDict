import requests
from bs4 import BeautifulSoup


def GetUrl(word):
    return "https://cn.bing.com/dict/search?q=" + str(word)


def Query(word):
    res = requests.get("https://cn.bing.com/dict/search?q=" + str(word))
    soup = BeautifulSoup(res.text, "html.parser")

    res = {}

    try:
        res['word'] = soup.select('.hd_div h1')[0].text
    except:
        res['word'] = word

    try:
        res['prus'] = soup.select('.hd_prUS')[0].text
    except:
        res['prus'] = ''

    res['qdef'] = []
    for item in soup.select(".qdef ul li"):
        res['qdef'].append({'pos': item.select(".pos")[0].text,
                            'def': item.select(".def span")[0].text})
    return res


def QueryList(words, f=print):
    lines = ''
    for word_ in words:
        word = word_.strip()
        if len(word) == 0:
            continue
        f(word)
        try:
            res = Query(word)
            line = '<tr><td>'
            line += res['word']
            line += '</td><td>'
            line += res['prus']
            line += '</td><td>'
            for item in res['qdef']:
                line += item['pos']
                if item['pos'] == '网络':
                    line += '.'
                line += item['def']
                line += '。'
            line += '</tr>'
            lines += line
        except Exception as e:
            f('Error.')
            f(e)
    f('Done.')
    return lines
