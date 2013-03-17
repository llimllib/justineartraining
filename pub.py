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
        try:
            manifest = eval(lesson_src.files("lesson.py")[0].text())
        except:
            print "failed to load manifest {}".format(lesson_src / "lesson.py")
            continue

        n = lesson_src.partition('/')[-1]

        outdir = lesson_path / n
        outdir.mkdir()

        lessons.append(manifest)
        manifest["chapter"] = n

        if "ssr" in manifest:
            for soundf, _ in manifest["ssr"]:
                path(lesson_src / soundf).copy(outdir)

            manifest.setdefault("links", []).append({
                "title": "Single Chords",
                "href":  path("../..") / outdir / "ssr.html"
            })

        if "sequences" in manifest:
            for seqf, _ in manifest["sequences"]:
                path(lesson_src / seqf).copy(outdir)

            manifest.setdefault("links", []).append({
                "title": "Chord Sequences",
                "href":  path("../..") / outdir / "sequences.html"
            })

    for manifest in lessons:
        outdir = lesson_path / manifest["chapter"]

        manifest["all_lessons"] = lessons

        if "ssr" in manifest:
            output = render_ssr(manifest)
            open(outdir / "ssr.html", "w", encoding="utf8").write(output)

        if "sequences" in manifest:
            output = render_sequences(manifest)
            open(outdir / "sequences.html", "w", encoding="utf8").write(output)
