from os import mkdir
from pub import task
from path import path
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
    lessons = path("lessons")

    render_ssr = partial(render, path("templates/ssr.html").text())
    render_sequences = partial(render, path("templates/sequences.html").text())

    for lesson_src in path("lessons_src").dirs():
        manifest = eval(lesson_src.files("lesson.py")[0].text())

        n = lesson_src.partition('/')[-1]

        outdir = lessons / n
        outdir.mkdir()

        if "sounds" in manifest:
            output = render_ssr(manifest)
            open((outdir / "ssr{}.html".format(n)), "w").write(output)

        if "sequences" in manifest:
            output = render_sequences(manifest)
            open((outdir / "sequences{}.html".format(n)), "w").write(output)
