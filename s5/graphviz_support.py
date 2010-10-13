import os, os.path, hashlib
from StringIO import StringIO
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image

OUTPUT_DIR = 'media'
from pygraphviz import AGraph

class GraphvizBlock(Image):
    required_arguments = 1
    has_content = True
    outputformat = 'png'
    def run(self):
        options = self.options
        filename = self.arguments[0]
        if self.content:
            content = u'\n'.join(self.content)
            ofilename = filename + '.' + self.outputformat
        else:
            content = open(filename).read().decode(options.get('encoding','utf-8'))
            ofilename = os.path.splitext(filename)[0] + '.' + self.outputformat

        g = AGraph(string=content)
        g.layout(prog='dot')
        opath = os.path.join(OUTPUT_DIR, ofilename)
        g.draw(opath, 'png')
        self.arguments[0] = opath
        return super(GraphvizBlock, self).run()

directives.register_directive('dotgraph', GraphvizBlock)

