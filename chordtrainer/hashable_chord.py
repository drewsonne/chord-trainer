import hashlib

from pychord import Chord


class HashableChord(Chord):
    def __hash__(self):
        return int(hashlib.sha1(self._chord.encode("utf-8")).hexdigest(), 16) % (
            10 ** 8
        )
