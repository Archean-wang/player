import random
import json
import base64
from urllib.parse import urlencode, quote
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from obj import Song, Singer, Album, Singers


class Qq(object):
    def __init__(self):
        pass

    @staticmethod
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
        _res = requests.get(url).text[len(callback)+1:-1]
        try:
            res = json.loads(_res, strict=False)
            vkey = res['req_0']['data']['midurlinfo'][0]['vkey']
        except json.decoder.JSONDecodeError:
            print(_res)
            return

        # makeup the final url
        song_url = f'http://dl.stream.qqmusic.qq.com/M800{song_mid}.mp3?vkey={vkey}&guid={g_uid}&fromtag=1'
        return song_url

    @staticmethod
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

    def show(self):
        kw = input("搜索:")
        res = self.search(kw)
        for s in res:
            print(f'{res.index(s)+1}.{s.show}')
        try:
            a = int(input('which one:'))
        except ValueError:
            print("Please input num.")
            return
        try:
            url = self.get_url(res[a-1].mid)
            print(url)
        except IndexError:
            print('Out of range')
            return


class Wy(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

        }

    @staticmethod
    def aes(a, b):
        iv = b"0102030405060708"
        # pad = 16 - len(a) % 16
        # text = a + pad * chr(pad).encode()
        text = pad(a.encode(), 16)
        encryptor = AES.new(b, AES.MODE_CBC, iv)
        text = encryptor.encrypt(text)
        return base64.b64encode(text).decode()

    def get_params(self, d):
        g = b"0CoJUm6Qyw8W8jud"
        h = {}
        i = b"FFFFFFFFFFFFFFFF"
        h["encSecKey"] = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        _params = self.aes(d, g)
        h["params"] = self.aes(_params, i)
        return h

    def search(self, kw):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        d = json.dumps({"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":kw,"type":"1","offset":"0","total":"true","limit":"10","csrf_token":""})
        data = self.get_params(d)
        _res = requests.post(url, data=data, headers=self.headers)
        res = _res.json()
        search_res = []

        for i in res["result"]["songs"]:
            singers = Singers()
            _singers = i["ar"]
            for s in _singers:
                singer = Singer()
                singer.name = s["name"]
                singer.mid = s["id"]
                singers.all.append(singer)

            album = Album()
            album.name = i["al"]["name"]
            album.mid = i["al"]["id"]

            song = Song()
            song.name = i["name"]
            song.mid = i["id"]
            song.album = album
            song.singer = singers
            search_res.append(song)

        return search_res

    def get_url(self, song_id):
        url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        c = '[%s]' % song_id
        d = json.dumps({"ids": c, "br": 128000, "csrf_token": ""})
        data = self.get_params(d)
        _res = requests.post(url, data=data, headers=self.headers)
        res = _res.json()
        url = res["data"][0]["url"]
        return url

    def show(self):
        kw = input("搜索:")
        res = self.search(kw)
        for s in res:
            print(f'{res.index(s)+1}.{s.show}')
        try:
            a = int(input('which one:'))
        except ValueError:
            print("Please input num.")
            return
        try:
            url = self.get_url(res[a-1].mid)
            print(url)
        except IndexError:
            print('Out of range')
            return


if __name__ == "__main__":
    # qq = Qq()
    # qq.show()
    wy = Wy()
    wy.show()
