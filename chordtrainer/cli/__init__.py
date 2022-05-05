from random import choice, shuffle
from time import sleep
import atexit

import click

from chordtrainer.chords import build_chord_reference, decompose_chord
from chordtrainer.progress import ProgressTracker


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


progress = ProgressTracker()
quality_mapping = {"7": "dom_7", "m7": "min_7", "M7": "maj_7"}  # , "sus47": "sus4_7"}


@click.command()
@click.option("--no-debug/--debug", help="Debug", type=bool, default=True)
@click.option(
    "--quality", type=click.Choice(["7", "m7", "M7", "sus47"], case_sensitive=False)
)
def run(no_debug, quality):
    chords = build_chord_reference()

    qualities = list(chords.keys())
    shuffle(qualities)

    for chord_quality in qualities:
        chord_collection = chords[chord_quality]
        if (quality is not None) and (quality_mapping[quality] != chord_quality):
            continue

        if not no_debug:
            click.echo(
                f"Adding '{len(chord_collection)}' chords in '{chord_quality}'..."
            )
        sleep(1)

        do_runtime_loop = True
        while do_runtime_loop:
            if no_debug:
                click.clear()
            progress.print_progress()
            if progress.is_ready_to_progress:
                if len(chord_collection) == 0:
                    do_runtime_loop = False
                    break
                candidate_chord = choice(tuple(chord_collection))
                if candidate_chord is None:
                    raise Exception(f"Selected None from '{chord_collection}'")
                chord_collection.remove(candidate_chord)
                testing_chord = progress.add_chord(candidate_chord)
            else:
                testing_chord = progress.fetch_chord()
            root, actual_upper_chord = decompose_chord(testing_chord.chord)
            user_upper_chord = click.prompt(
                f"What is upper chord of '{testing_chord.chord}'?"
            )

            if user_upper_chord == f"{actual_upper_chord}":
                click.echo(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
                testing_chord.mark_correct()
                sleep(1)
            else:
                if no_debug:
                    click.clear()
                progress.print_progress()
                click.echo(
                    f"{bcolors.FAIL}{testing_chord.chord} is composed of {root} and {actual_upper_chord}{bcolors.ENDC}"
                )
                testing_chord.mark_incorrect()
                click.pause()


@atexit.register
def on_end():
    progress.print_results()


if __name__ == "__main__":
    run()
