class Song(object):
    def __init__(self):
        self.name = ''
        self.singer = ''
        self.album = ''
        self.mid = ''

    @property
    def show(self):
        if self.album.name == '':
            res = f'{self.name} - {self.singer.name} ---未知专辑'
        else:
            res = f'{self.name} - {self.singer.name} ---{self.album.name}'
        return res


class Singer(object):
    def __init__(self):
        self._name = ''
        self.mid = ''


class Singers(object):
    def __init__(self):
        self.all = []

    @property
    def name(self):
        _name = ''
        for i in self.all:
            _name += f'{i.name}/'
        return _name[:-1]


class Album(object):
    def __init__(self):
        self.name = ''
        self.mid = ''