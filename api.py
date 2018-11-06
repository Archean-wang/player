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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

        }
        self._cookies = '_ntes_nnid=fad5dd9324002c36a8805ff5a461a7d3,1521171652144; _ntes_nuid=fad5dd9324002c36a8805ff5a461a7d3; _iuqxldmzr_=32; _ngd_tid=HxTEeqy1%2Fs%2Forv7EkY9Ji6Wp6%2FbSKWDJ; P_INFO=m13006164624_2@163.com|1521969370|0|urs|00&99|zhj&1521864605&youdaodict_client#zhj&331000#10#0#0|130624&1|youdaodict_client&note_client|13006164624@163.com; usertrack=ezq0plq5wF4YEtiXAxgsAg==; _ga=GA1.2.1866508268.1522122805; WM_TID=f5OSf23dGroc66ZvWxNC%2BJ%2FI6Qut5RR3; __f_=1536976269570; vjuids=880e4228f.166c2b3e5df.0.d6d7c6ab953e; vjlast=1540864862.1540864862.30; vinfo_n_f_l_n3=b92ac824a0610f0a.1.0.1540864861676.0.1540864914179; __utma=94650624.296949646.1521215845.1541424481.1541502844.9; __utmz=94650624.1541502844.9.4.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; WM_NI=eOVEgDeOaEGprFI%2FvMFMgwQOJ011n5cFkH9%2F%2FWg76RlF5fDXbTBJTOBpCC2i4QLWPA%2FvP8%2B4rHHEQkS2J3xXh%2FjWKx71pNmTybXmk6GM6rUx0TsL6VC11ns5tvkzW47JOVE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed4e544f387fad2ea5cb1bc8aa2c85f869e9faab86aa6b28a9abb63a2b087d7bc2af0fea7c3b92aa7919aa6e650a791afa6c67cb29a87d0f5478693a998d4458af0ffd2ed3fa19aa5a9bc25ed89a9d8b55ab09afb87c754a28c8eabd74582b08da4b163f88f84b8d34bedaaa0d9aa40b29888a6d46191ee86d4fb54acf1a6b8ca74f5efc0aff060bbbe988eea3e8593fa93d874f48cbdadb55e81efff8ff23fb8aaa59bd640f59681b7c837e2a3; __utmc=94650624; JSESSIONID-WYYY=4ten%5CNPKeuMFZSbfzR5yHcg5KTgnVUHXKDa%2BOQdTdAKtlXwzic4AqqGaryHgnXvboORmVaFxeYfE6tmMWZf2IJaUzNEUdz%5C8PIW3TBkI5syJO7Fz%2FWVPn5vGBgapndGX7kd2Y4yhSr2QhYSeke3SYBAEFHno%5CfqNaGB70eyjdAbPKCuU%3A1541508123503; __utmb=94650624.35.10.1541502844'
        self.cookies = dict(i.split('=', 1) for i in self._cookies.split(';'))

    @staticmethod
    def aes(a, b):
        iv = "0102030405060708"
        pad = 16 - len(a) % 16
        text = a + pad * chr(pad)
        encryptor = AES.new(b, AES.MODE_CBC, iv)
        text = encryptor.encrypt(text)
        return base64.b64encode(text).decode()

    def get_params(self, d):
        g = "0CoJUm6Qyw8W8jud"
        h = {}
        i = "FFFFFFFFFFFFFFFF"
        h["encSecKey"] = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        h["params"] = self.aes(d, g)
        h["params"] = self.aes(h["params"], i)
        return h

    def search(self, kw):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        d = json.dumps({"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":kw,"type":"1","offset":"0","total":"true","limit":"10","csrf_token":""})
        data = self.get_params(d)
        # data['params'] = 'TO/LEHTGmchynSFd5iFZHPtStFGvAqxLiKxhcU77uvAf9AMKjlfmybWwCcfNqKwqIhbZ8lAtbHbrjB1AsXJqNjY2+PbSYHl4if9fnFty3TMtReRkeR2PMVSV7QBjOl7FsUAqbxI3HvVgV0+V4DYZLf23JSxjaKb9nnPnyloYf88+3SX3cpXmiI0aySjOAb9OGQgfZGjJAOaaKvzMi+sSR1vjkpDDmoBxRssVc4lh1aKdYULpezpYddeVzG5cWlJSWWrNEaHuzSMFIhGKJSzw0w=='
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
    # url = wy.get_url("477662605")
    # print(url)
    wy.show()
