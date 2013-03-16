from pub import task
from path import path
from pystache import render
from functools import partial

@task
def build():
    render_lesson = partial(render, path("templates/lesson.html").text())
    for lesson in path("lessons").dirs():
        manifest = eval(lesson.files("lesson.py")[0].text())

        n = lesson.partition('/')[-1]

        output = render_lesson(manifest)

        open((lesson / "lesson{}.html".format(n)), "w").write(output)
