from random import choices
from typing import Set, List, Tuple

import click

from chordtrainer.hashable_chord import HashableChord


class ProgressTracker:
    def __init__(self):
        self._chords: Set[ChordProgress] = set()

        self._understood_threshold = 0.7

    def add_chord(self, chord: HashableChord) -> "ChordProgress":
        chord_progress = ChordProgress(chord)
        self._chords.add(chord_progress)
        return chord_progress

    @property
    def is_ready_to_progress(self) -> bool:
        if len(self._chords) <= 1:
            return True
        else:
            _, _, num_not_understood = self._progress
            return not (num_not_understood > 2)

    @property
    def chords(self):
        return

    def fetch_chord(self) -> "ChordProgress":
        chords = list(self._chords)
        chosen = choices(
            population=chords,
            weights=[
                max(1 - c.confidence, 0.3) for c in chords
            ],  # Pick the chords we're worst at, and don't over weigh for poor performers
        )
        return chosen[0]

    @property
    def _progress(self) -> Tuple[List[float], int, int]:
        # Return confidences: List[float], understood: int, not_understood: int
        confidences = [c.confidence for c in self._chords]
        not_understood = list(
            filter(lambda c: c <= self._understood_threshold, confidences)
        )
        num_not_understood = len(not_understood)
        num_understood = len(confidences) - num_not_understood

        return confidences, num_understood, num_not_understood

    def print_progress(self):
        if len(self._chords) == 0:
            average_score, understood, not_understood, percentage = (0.0, 0, 0, 0.0)
        else:
            confidences, understood, not_understood = self._progress
            average_score = sum(confidences) / len(confidences)
            percentage = understood / (understood + not_understood) * 100.0
        click.echo(
            f"{percentage:.0f}%, x̄: {average_score:.2f}, |c|: {len(self._chords)}, +: {understood}, -: {not_understood}"
        )

    def print_results(self):
        for progress in self._chords:
            click.echo(
                f"{str(progress.chord): <5}: {progress.confidence * 100.00:3.0f}%"
            )


class ChordProgress:
    def __init__(self, chord: HashableChord):
        self.chord = chord
        self._results = []
        self._max_tries = 5

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.chord} {self.confidence:0.2f}>"

    @property
    def confidence(self) -> float:
        if len(self._results) > 0:
            results = self._results[-self._max_tries :]
            return results.count(True) / len(results)
        else:
            return 0.0

    def mark_incorrect(self):
        self._results.append(False)

    def mark_correct(self):
        self._results.append(True)
