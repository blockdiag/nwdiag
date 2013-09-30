# -*- coding: utf-8 -*-

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import os
import io
import tempfile
from blockdiag.tests.utils import stderr_wrapper, with_pil
from docutils import nodes
from docutils.core import publish_doctree, publish_parts
from docutils.parsers.rst import directives as docutils
from rackdiag.utils.rst import directives


class TestRstDirectives(unittest.TestCase):
    def setUp(self):
        docutils.register_directive('rackdiag',
                                    directives.RackdiagDirectiveBase)
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        if 'rackdiag' in docutils._directives:
            del docutils._directives['rackdiag']

        for file in os.listdir(self.tmpdir):
            os.unlink(self.tmpdir + "/" + file)
        os.rmdir(self.tmpdir)

    def test_setup(self):
        directives.setup()
        options = directives.directive_options

        self.assertIn('rackdiag', docutils._directives)
        self.assertEqual(directives.RackdiagDirective,
                         docutils._directives['rackdiag'])
        self.assertEqual('PNG', options['format'])
        self.assertEqual(False, options['antialias'])
        self.assertEqual(None, options['fontpath'])
        self.assertEqual(False, options['nodoctype'])
        self.assertEqual(False, options['noviewbox'])
        self.assertEqual(False, options['inline_svg'])

    def test_setup_with_args(self):
        directives.setup(format='SVG', antialias=True, fontpath='/dev/null',
                         nodoctype=True, noviewbox=True, inline_svg=True)
        options = directives.directive_options

        self.assertIn('rackdiag', docutils._directives)
        self.assertEqual(directives.RackdiagDirective,
                         docutils._directives['rackdiag'])
        self.assertEqual('SVG', options['format'])
        self.assertEqual(True, options['antialias'])
        self.assertEqual('/dev/null', options['fontpath'])
        self.assertEqual(True, options['nodoctype'])
        self.assertEqual(True, options['noviewbox'])
        self.assertEqual(True, options['inline_svg'])

    @stderr_wrapper
    def test_base_noargs(self):
        text = ".. rackdiag::"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.system_message, type(doctree[0]))

    def test_base_with_block(self):
        text = ".. rackdiag::\n\n   { 1: server\n   2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(directives.rackdiag, type(doctree[0]))
        self.assertEqual('{ 1: server\n2: database\n}', doctree[0]['code'])
        self.assertEqual(None, doctree[0]['alt'])
        self.assertEqual({}, doctree[0]['options'])

    @stderr_wrapper
    def test_base_with_emptyblock(self):
        text = ".. rackdiag::\n\n   \n"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.system_message, type(doctree[0]))

    def test_base_with_filename(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'diagrams/simple.diag')
        text = ".. rackdiag:: %s" % filename
        doctree = publish_doctree(text)

        self.assertEqual(1, len(doctree))
        self.assertEqual(directives.rackdiag, type(doctree[0]))
        self.assertEqual(io.open(filename).read(), doctree[0]['code'])
        self.assertEqual(None, doctree[0]['alt'])
        self.assertEqual({}, doctree[0]['options'])

    @stderr_wrapper
    def test_base_with_filename_not_exists(self):
        text = ".. rackdiag:: unknown.diag"
        doctree = publish_doctree(text)
        self.assertEqual(nodes.system_message, type(doctree[0]))

    @stderr_wrapper
    def test_base_with_block_and_filename(self):
        text = ".. rackdiag:: unknown.diag\n\n   { 1: server\n 2: database }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.system_message, type(doctree[0]))

    def test_base_with_options(self):
        text = ".. rackdiag::\n   :alt: hello world\n   :desctable:\n" + \
               "   :maxwidth: 100\n\n   { 1: server\n   2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(directives.rackdiag, type(doctree[0]))
        self.assertEqual('{ 1: server\n2: database\n}', doctree[0]['code'])
        self.assertEqual('hello world', doctree[0]['alt'])
        self.assertEqual(None, doctree[0]['options']['desctable'])
        self.assertEqual(100, doctree[0]['options']['maxwidth'])

    def test_block(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n\n   { 1: server\n   2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertFalse('alt' in doctree[0])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))
        self.assertFalse('target' in doctree[0])

    def test_block_alt(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n   2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('hello world', doctree[0]['alt'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))
        self.assertFalse('target' in doctree[0])

    def test_block_fontpath1(self):
        with self.assertRaises(RuntimeError):
            directives.setup(format='SVG', fontpath=['dummy.ttf'],
                             outputdir=self.tmpdir)
            text = ".. rackdiag::\n   :alt: hello world\n\n" + \
                   "   { 1: server\n    2: database\n   }"
            publish_doctree(text)

    def test_block_fontpath2(self):
        with self.assertRaises(RuntimeError):
            directives.setup(format='SVG', fontpath='dummy.ttf',
                             outputdir=self.tmpdir)
            text = ".. rackdiag::\n   :alt: hello world\n\n" + \
                   "   { 1: server\n    2: database\n   }"
            publish_doctree(text)

    def test_caption(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :caption: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.figure, type(doctree[0]))
        self.assertEqual(2, len(doctree[0]))
        self.assertEqual(nodes.image, type(doctree[0][0]))
        self.assertEqual(nodes.caption, type(doctree[0][1]))
        self.assertEqual(1, len(doctree[0][1]))
        self.assertEqual(nodes.Text, type(doctree[0][1][0]))
        self.assertEqual('hello world', doctree[0][1][0])

    def test_block_maxwidth(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :maxwidth: 100\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertFalse('alt' in doctree[0])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))
        self.assertFalse(0, doctree[0]['target'].index(self.tmpdir))

    def test_block_nodoctype_false(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, nodoctype=False)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        svg = open(doctree[0]['uri']).read()
        self.assertEqual("<?xml version='1.0' encoding='UTF-8'?>\n"
                         "<!DOCTYPE ", svg[:49])

    def test_block_nodoctype_true(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, nodoctype=True)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[-1]))
        svg = open(doctree[0]['uri']).read()
        self.assertNotEqual("<?xml version='1.0' encoding='UTF-8'?>\n"
                            "<!DOCTYPE ", svg[:49])

    def test_block_noviewbox_false(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, noviewbox=False)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        svg = open(doctree[0]['uri']).read()
        self.assertRegexpMatches(svg, '<svg viewBox="0 0 \d+ \d+" ')

    def test_block_noviewbox_true(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, noviewbox=True)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        svg = open(doctree[0]['uri']).read()
        self.assertRegexpMatches(svg, '<svg height="\d+" width="\d+" ')

    def test_block_inline_svg_false(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, inline_svg=False)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(1, len(os.listdir(self.tmpdir)))

    def test_block_inline_svg_true(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, inline_svg=True)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual('html', doctree[0]['format'])
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertEqual("<?xml version='1.0' encoding='UTF-8'?>\n"
                         "<!DOCTYPE ", doctree[0][0][:49])
        self.assertEqual(0, len(os.listdir(self.tmpdir)))

    @with_pil
    def test_block_inline_svg_true_but_nonsvg_format(self):
        directives.setup(format='PNG', outputdir=self.tmpdir, inline_svg=True)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))

    def test_block_inline_svg_true_with_multibytes(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, inline_svg=True)
        text = ".. rackdiag::\n   :alt: hello world\n\n" + \
               "   { 1: サーバ\n    2: データベース\n   }"
        publish_parts(text)

    def test_block_max_width_inline_svg(self):
        directives.setup(format='SVG', outputdir=self.tmpdir,
                         nodoctype=True, noviewbox=True, inline_svg=True)
        text = ".. rackdiag::\n   :maxwidth: 100\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertRegexpMatches(doctree[0][0],
                                 '<svg height="\d+" width="100" ')

    def test_desctable_without_description(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :desctable:\n\n" + \
               "   { 1: server\n    2: database\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

    def test_desctable(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :desctable:\n\n" + \
               "   { 1: server [description = foo];\n" + \
               "   2: database [description = bar];\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][2]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][3]))
        self.assertEqual(nodes.thead, type(doctree[1][0][4]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][5]))

        # colspec
        self.assertEqual(25, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])
        self.assertEqual(50, doctree[1][0][2]['colwidth'])
        self.assertEqual(50, doctree[1][0][3]['colwidth'])

        # thead
        thead = doctree[1][0][4]
        self.assertEqual(4, len(thead[0]))
        self.assertEqual('No', thead[0][0][0][0])
        self.assertEqual('Name', thead[0][1][0][0])
        self.assertEqual('Height', thead[0][2][0][0])
        self.assertEqual('Description', thead[0][3][0][0])

        # tbody
        tbody = doctree[1][0][5]
        self.assertEqual(2, len(tbody))
        self.assertEqual('1', tbody[0][0][0][0])
        self.assertEqual('server', tbody[0][1][0][0])
        self.assertEqual('1U', tbody[0][2][0][0])
        self.assertEqual('foo', tbody[0][3][0][0])
        self.assertEqual('2', tbody[1][0][0][0])
        self.assertEqual('database', tbody[1][1][0][0])
        self.assertEqual('1U', tbody[1][2][0][0])
        self.assertEqual('bar', tbody[1][3][0][0])

    def test_desctable_with_rest_markups(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :desctable:\n\n" + \
               "   { 1: server [description = \"foo *bar* **baz**\"];\n" + \
               "   2: database [description = \"**foo** *bar* baz\"];\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(6, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][2]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][3]))
        self.assertEqual(nodes.thead, type(doctree[1][0][4]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][5]))

        # colspec
        self.assertEqual(25, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])
        self.assertEqual(50, doctree[1][0][2]['colwidth'])
        self.assertEqual(50, doctree[1][0][3]['colwidth'])

        # thead
        thead = doctree[1][0][4]
        self.assertEqual(4, len(thead[0]))
        self.assertEqual('No', thead[0][0][0][0])
        self.assertEqual('Name', thead[0][1][0][0])
        self.assertEqual('Height', thead[0][2][0][0])
        self.assertEqual('Description', thead[0][3][0][0])

        # tbody
        tbody = doctree[1][0][5]
        self.assertEqual(2, len(tbody))
        self.assertEqual('1', tbody[0][0][0][0])
        self.assertEqual('server', tbody[0][1][0][0])
        self.assertEqual('1U', tbody[0][2][0][0])
        self.assertEqual(4, len(tbody[0][3][0]))
        self.assertEqual(nodes.Text, type(tbody[0][3][0][0]))
        self.assertEqual('foo ', str(tbody[0][3][0][0]))
        self.assertEqual(nodes.emphasis, type(tbody[0][3][0][1]))
        self.assertEqual(nodes.Text, type(tbody[0][3][0][1][0]))
        self.assertEqual('bar', tbody[0][3][0][1][0])
        self.assertEqual(nodes.Text, type(tbody[0][3][0][2]))
        self.assertEqual(' ', str(tbody[0][3][0][2]))
        self.assertEqual(nodes.strong, type(tbody[0][3][0][3]))
        self.assertEqual(nodes.Text, type(tbody[0][3][0][3][0]))
        self.assertEqual('baz', str(tbody[0][3][0][3][0]))

        self.assertEqual('2', tbody[1][0][0][0])
        self.assertEqual('database', tbody[1][1][0][0])
        self.assertEqual('1U', tbody[1][2][0][0])
        self.assertEqual(4, len(tbody[1][3][0]))
        self.assertEqual(nodes.strong, type(tbody[1][3][0][0]))
        self.assertEqual(nodes.Text, type(tbody[1][3][0][0][0]))
        self.assertEqual('foo', str(tbody[1][3][0][0][0]))
        self.assertEqual(nodes.Text, type(tbody[1][3][0][1]))
        self.assertEqual(' ', str(tbody[1][3][0][1]))
        self.assertEqual(nodes.emphasis, type(tbody[1][3][0][2]))
        self.assertEqual(nodes.Text, type(tbody[1][3][0][2][0]))
        self.assertEqual('bar', str(tbody[1][3][0][2][0]))
        self.assertEqual(nodes.Text, type(tbody[1][3][0][3]))
        self.assertEqual(' baz', str(tbody[1][3][0][3]))

    def test_desctable_with_numbered(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :desctable:\n\n" + \
               "   { 1: server [numbered = 2];\n" + \
               "   2: database [numbered = 1];\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(5, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][2]))
        self.assertEqual(nodes.thead, type(doctree[1][0][3]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][4]))

        # colspec
        self.assertEqual(25, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])
        self.assertEqual(50, doctree[1][0][2]['colwidth'])

        # thead
        thead = doctree[1][0][3]
        self.assertEqual(3, len(thead[0]))
        self.assertEqual('No', thead[0][0][0][0])
        self.assertEqual('Name', thead[0][1][0][0])
        self.assertEqual('Height', thead[0][2][0][0])

        # tbody
        tbody = doctree[1][0][4]
        self.assertEqual(2, len(tbody))
        self.assertEqual('1', tbody[0][0][0][0])
        self.assertEqual('server', tbody[0][1][0][0])
        self.assertEqual('1U', tbody[0][2][0][0])
        self.assertEqual('2', tbody[1][0][0][0])
        self.assertEqual('database', tbody[1][1][0][0])
        self.assertEqual('1U', tbody[1][2][0][0])

    def test_desctable_with_numbered_and_description(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = ".. rackdiag::\n   :desctable:\n\n" + \
               "   { 1: server [description = foo, numbered = 2];\n" + \
               "   2: database [description = bar, numbered = 1];\n   }"
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(6, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][2]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][3]))
        self.assertEqual(nodes.thead, type(doctree[1][0][4]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][5]))

        # colspec
        self.assertEqual(25, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])
        self.assertEqual(50, doctree[1][0][2]['colwidth'])
        self.assertEqual(50, doctree[1][0][3]['colwidth'])

        # thead
        thead = doctree[1][0][4]
        self.assertEqual(4, len(thead[0]))
        self.assertEqual('No', thead[0][0][0][0])
        self.assertEqual('Name', thead[0][1][0][0])
        self.assertEqual('Height', thead[0][2][0][0])
        self.assertEqual('Description', thead[0][3][0][0])

        # tbody
        tbody = doctree[1][0][5]
        self.assertEqual(2, len(tbody))
        self.assertEqual('1', tbody[0][0][0][0])
        self.assertEqual('server', tbody[0][1][0][0])
        self.assertEqual('1U', tbody[0][2][0][0])
        self.assertEqual(1, len(tbody[0][3]))
        self.assertEqual('foo', tbody[0][3][0][0])
        self.assertEqual('2', tbody[1][0][0][0])
        self.assertEqual('database', tbody[1][1][0][0])
        self.assertEqual('1U', tbody[1][2][0][0])
        self.assertEqual('bar', tbody[1][3][0][0])
