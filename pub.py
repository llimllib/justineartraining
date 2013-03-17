from os import mkdir
from pub import task
from path import path
from codecs import open
from os.path import isdir
from pystache import render
from functools import partial
from pub.shortcuts import rm

@task
def clean():
    """Remove the lessons dir"""
    rm("-rf lessons")

@task("clean", default=True)
def build():
    if not isdir('lessons'): mkdir('lessons')
    lesson_path = path("lessons")

    render_ssr = partial(render, path("templates/ssr.html").text(encoding='utf8'))
    render_sequences = partial(render, path("templates/sequences.html").text(encoding='utf8'))

    lessons = []

    #XXX: this assumes lessons_src will be parsed in numerical order.
    #     need to write a sorter if that's not true
    for lesson_src in path("lessons_src").dirs():
        manifest = eval(lesson_src.files("lesson.py")[0].text())
        n = lesson_src.partition('/')[-1]

        outdir = lesson_path / n
        outdir.mkdir()

        lessons.append(manifest)
        manifest["chapter"] = n

        if "sounds" in manifest:
            for soundf, _, _ in manifest["sounds"]:
                path(lesson_src / soundf).copy(outdir)

            manifest.setdefault("links", []).append({
                "title": "Single Chords",
                "href":  str(path("../..") / outdir / "ssr.html")
            })

        if "sequences" in manifest:
            for seqf, _ in manifest["sequences"]:
                path(lesson_src / soundf).copy(outdir)

            manifest.setdefault("links", []).append({
                "title": "Chord Sequences",
                "href":  str(path("../..") / outdir / "sequences.html")
            })

    for manifest in lessons:
        manifest["all_lessons"] = lessons

        if "sounds" in manifest:
            output = render_ssr(manifest)
            open((outdir / "ssr.html"), "w", encoding="utf8").write(output)

        if "sequences" in manifest:
            output = render_sequences(manifest)
            open((outdir / "sequences.html"), "w", encoding="utf8").write(output)
