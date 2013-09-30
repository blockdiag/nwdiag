# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import nwdiag.command
from nwdiag.elements import NodeGroup, DiagramNode, DiagramEdge


def extra_case(func):
    filename = "VL-PGothic-Regular.ttf"
    testdir = os.path.dirname(__file__)
    pathname = "%s/truetype/%s" % (testdir, filename)

    if os.path.exists(pathname):
        func.__test__ = True
    else:
        func.__test__ = False

    return func


def __build_diagram(filename, format, *additional_args):
    testdir = os.path.dirname(__file__)
    diagpath = "%s/diagrams/%s" % (testdir, filename)

    fontfile = "VL-PGothic-Regular.ttf"
    fontpath = "%s/truetype/%s" % (testdir, fontfile)

    try:
        tmpfile = tempfile.mkstemp()[1]
        args = ['-T', format, '-f', fontpath, '-o', tmpfile, diagpath]
        if additional_args:
            args += additional_args

        DiagramNode.clear()
        DiagramEdge.clear()
        NodeGroup.clear()

        nwdiag.command.main(args)
    finally:
        os.unlink(tmpfile)


def diagram_files():
    testdir = os.path.dirname(__file__)
    pathname = "%s/diagrams/" % testdir

    skipped = ['errors',
               'white.gif']

    return [d for d in os.listdir(pathname) if d not in skipped]


@extra_case
def test_generator():
    formats = ['svg', 'png']
    try:
        import reportlab.pdfgen.canvas
        reportlab.pdfgen.canvas
        formats.append('pdf')
    except ImportError:
        sys.stderr.write("Skip testing about pdf exporting.\n")
        pass

    for diagram in diagram_files():
        for format in formats:
            yield __build_diagram, diagram, format

            if format == 'png':
                yield __build_diagram, diagram, format, '--antialias'
