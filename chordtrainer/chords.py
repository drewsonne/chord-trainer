import json
from typing import Dict, Tuple, Set

from pychord import Chord

from chordtrainer.hashable_chord import HashableChord


class ChordEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Chord):
            return obj.chord
        return json.JSONEncoder.default(self, obj)


def build_chord_reference() -> Dict[str, Set[HashableChord]]:
    # Major 7 chords

    chords = {"min_7": set(), "dom_7": set(), "maj_7": set()}  # , "sus4_7": set()}

    dom_7 = HashableChord("C7")
    maj_7 = HashableChord("Cmaj7")
    min_7 = HashableChord("Cm7")
    # sus4_7 = HashableChord("C7sus4")
    for i in range(12):
        chords["min_7"].add(HashableChord(min_7.chord))
        chords["dom_7"].add(HashableChord(dom_7.chord))
        chords["maj_7"].add(HashableChord(maj_7.chord))
        # chords["sus4_7"].add(HashableChord(sus4_7.chord))

        dom_7.transpose(1)
        maj_7.transpose(1)
        min_7.transpose(1)
        # sus4_7.transpose(1)

    return chords


def decompose_chord(chord: Chord) -> Tuple[str, Chord]:
    # Decompose a chord
    upper_chord_root = chord.components()[1]
    if chord.quality.quality == "7":
        upper_chord = Chord(f"{upper_chord_root}dim")
    elif chord.quality.quality == "maj7":
        upper_chord = Chord(f"{upper_chord_root}m")
    elif chord.quality.quality == "m7":
        upper_chord = Chord(f"{upper_chord_root}")
    else:
        raise Exception(f"Unexpected quality {chord.quality}")

    return chord.root, upper_chord
