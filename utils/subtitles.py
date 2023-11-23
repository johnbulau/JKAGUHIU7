import os
import subprocess
import ass
from datetime import timedelta


def correct_offset_libass(infile: str, outfile: str, time: float) -> None:
    with open(infile, encoding="utf_8_sig") as f:
        doc = ass.parse(f)

    for elem in doc.events:
        elem.start = timedelta(seconds=elem.start.total_seconds() + time)
        elem.end = timedelta(seconds=elem.end.total_seconds() + time)

    with open(outfile, "w", encoding="utf_8_sig") as f:
        doc.dump_file(f)


def correct_sub_offset_ffmpeg(in_path, out_path, offset) -> None:
    command = (
        f'ffmpeg -itsoffset {offset} -i "{in_path}" "{out_path}" -y -loglevel warning'
    )
    res = subprocess.call(command, shell=True)
    if not res != 0:
        raise RuntimeError()


def correct_sub_offset(in_path, out_path, offset) -> None:
    name = os.name
    if name == "nt":
        try:
            correct_sub_offset_ffmpeg(in_path, out_path, offset)

        except RuntimeError:
            print("resolving error")
            correct_offset_libass(in_path, out_path, offset)
    else:
        correct_offset_libass(in_path, out_path, offset)


def add_aegisub_meta(file, duration, width, height, fps=24):
    with open(file, "a", encoding="utf_8_sig") as f:
        f.write(
            "\n\n"
            "[Aegisub Project Garbage]\n"
            + f"Video File: ?dummy:{fps}:{int(duration*fps)}:{width}:{height}:25:198:57:\n"
            + f"Audio File: ../mp3/postaudio.mp3\n"
            + "Video AR Value: 0.562500\n"
            + "Video Zoom Percent: 0.375000\n"
            + "Active Line: 1\n"
            + "Video Position: 125"
        )


def checkForMannulCheck(flag, msg, file, duration, width, height) -> None:
    if flag:
        print(msg)
        add_aegisub_meta(file, duration, width, height)
        input("Press any button to continue...")


# if __name__ == "__main__":
# correct_sub_offset("test11.ass", "ct.ass", 33)
# add_aegisub_meta("some.ass",14,1920,1080)
