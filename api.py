import random
import json
import base64
from urllib.parse import urlencode, quote
import requests
from Crypto.Cipher import AES
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
            'Cookie': 'appver=1.5.0.75771;',
            'Referer': 'http://music.163.com/'
        }

    @staticmethod
    def aes(a, b):
        iv = b"0102030405060708"
        pad = 16 - len(a) % 16
        a = a + pad * chr(pad).encode('utf-8')
        encryptor = AES.new(b, AES.MODE_CBC, iv)
        text = encryptor.encrypt(a)
        text = base64.b64encode(text)
        return text

    def get_params(self, d):
        g = b"0CoJUm6Qyw8W8jud"
        h = {}
        i = b"FFFFFFFFFFFFFFFF"
        h["encSecKey"] = "345955431600157692da9b96cf6e125a462b8ab0aac7cad935625e7ca1f503f4e74e19b2eeda5d79eede85da5b448a135577826db6daaa30a6152104871265c637b99cf37d5b905a2885c7bc96103fd8cc2d8cb2d8d0d6044e1d7934f773ec07fcf9f817f8fe4102111a3aa07c2a4513a30dcc77264e1fec984624ee494599a3"
        h["params"] = self.aes(d, g)
        h["params"] = self.aes(h["params"], i).decode('utf-8')
        return h

    def search(self, kw):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        d = json.dumps({"s": kw, "limit": 8, "crsf_token": ""}).encode('utf-8')
        data = self.get_params(d)
        res = json.loads(requests.post(url, data=data, headers=self.headers).json())
        search_res = []

        for i in res["songs"]:
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
        c = '"[{"id": "%s"}]"' % song_id
        d = json.dumps({"id": song_id, "c": c, "csrf_token": ""}).encode('utf-8')
        data = self.get_params(d)
        print(data)
        _res = requests.post(url, data=data, headers=self.headers)
        print(_res.text)
        res = json.loads(_res.json())
        url = res[0]["url"]
        return url


if __name__ == "__main__":
    # qq = Qq()
    # qq.show()
    wy = Wy()
    url = wy.get_url("83081")
    print(url)