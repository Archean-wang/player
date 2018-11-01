import random
import json
from urllib.parse import urlencode, quote
import requests
from obj import Song, Singer, Album, Singers


def get_url(song_mid):
    # makeup g_uid
    t = random.randrange(999)
    g_uid = str(int(round(2147483647 * random.random()) * t % 1e10))

    # makeup url
    callback = "getplaysongvkey" + str(random.random()).replace("0.", "")
    param = {
        'data': '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],'
                '"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,'
                '"cv":0}}' % (g_uid, song_mid)
    }
    pre_url = f'https://u.y.qq.com/cgi-bin/musicu.fcg?' \
              f'callback={callback}&g_tk=5381&jsonpCallback={callback}&loginUin=0&hostUin=0' \
              f'&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&'
    url = pre_url + urlencode(param)
    # print(url)

    # get vkey
    _res = requests.get(url).text[32:-1]
    try:
        res = json.loads(_res, strict=False)
        vkey = res['req_0']['data']['midurlinfo'][0]['vkey']
    except json.decoder.JSONDecodeError:
        print(res)
        return

    # makup the final url
    song_url = f'http://dl.stream.qqmusic.qq.com/M800{song_mid}.mp3?vkey={vkey}&guid={g_uid}&fromtag=1'
    return song_url


def search(keyword):
    url = f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&w={quote(keyword)}&cr=1&t=0'
    res = json.loads(requests.get(url).text[9:-1], strict=False)
    search_res = []

    for i in res["data"]["song"]["list"]:
        singers = Singers()
        _singers = i["singer"]
        for s in _singers:
            singer = Singer()
            singer.name = s["name"]
            singer.mid = s["mid"]
            singers.all.append(singer)

        album = Album()
        album.name = i["album"]["name"]
        album.mid = i["album"]["mid"]

        song = Song()
        song.name = i["name"]
        song.mid = i["mid"]
        song.album = album
        song.singer = singers
        search_res.append(song)

    return search_res


def show():
    kw = input("搜索:")
    res = search(kw)
    for s in res:
        print(f'{res.index(s)+1}.{s.show}')
    try:
        a = int(input('which one:'))
    except ValueError:
        print("Please input num.")
        return
    try:
        url = get_url(res[a-1].mid)
        print(url)
    except IndexError:
        print('Out of range')
        return


if __name__ == "__main__":
    show()