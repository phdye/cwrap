import os
import unittest

from cwrap import frontends
from cwrap.backend import renderer
from cwrap.config import Config, File


def create_tst(filename):
    def do_tst_file(self):
        result = self.convert(filename + '.h')
        expected = self.read_expected(filename + '.pxd')
        print(result)
        self.assertEqual(expected, result)
    return do_tst_file


class TestFiles(unittest.TestCase):

    def setUp(self):
        self.frontend = frontends.get_frontend('clang')

    def convert(self, filename):
        files = [File(filename)]
        config = Config('clang', files=files)
        asts = self.frontend.generate_asts(config)
        print('\n\n\nvmx: asts:\n', asts, '\n\n\n\n\n')
        ast_renderer = renderer.ASTRenderer()
        for ast_container in asts:
            mod_node = ast_container.module
            code = ast_renderer.render(mod_node)
            output = []
            for line in code.splitlines():
                if line.startswith('#') or not line.strip():
                    continue
                output.append(line.strip())
            return output

    def read_expected(self, filename):
        output = []
        with open(filename) as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                output.append(line.strip())
        return output


if __name__ == '__main__':
    unittest.main()


# Thanks for the hint: http://stackoverflow.com/questions/2798956/python-unittest-generate-multiple-tests-programmatically
curdir = os.path.dirname(__file__)
testfiles = os.listdir(os.path.join(curdir, 'data'))
testfiles.sort()
testfiles = [os.path.join(curdir, 'data', f) for f in testfiles]
testfiles = [os.path.splitext(f)[0] for f in testfiles if f.endswith('.h')]
print('Files to test:', testfiles)
for testfile in testfiles:
    tst_method = create_tst(testfile)
    tst_method.__name__ = 'test_' + os.path.basename(testfile)
    setattr(TestFiles, tst_method.__name__, tst_method)
