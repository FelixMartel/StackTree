# -*- coding: utf-8 -*-

from .context import *

import unittest

class ExectreeTestSuite(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.tv = TreeValidator()

    def test_recursion_linear(self):
        text = "the nail and gear vexillologists"
        @exectree(indices=[]) # do not keep any arguments
        def traverse(s):
          if len(s) > 0:
            traverse(s[1:])
            return s[0]
        traverse(text)
        # tree is a linked list made of
        # the chars in text
        tree = get_tree()
        self.tv.nodes = []
        for char in text:
          self.tv.nodes.append(ExecTree(ret=char))
        self.tv.nodes.append(ExecTree())
        assert self.tv.validate(tree)

    def test_recursion_4_ary(self):
        char_map = ("xxxxxxxx   "
                    "x x    x   "
                    "x xxxx xxxx"
                    "x         x"
                    "xxxxxxxxxxx")
        @exectree(indices=[1]) # keep the pos argument
        def traverse(m, pos):
          if pos >= len(m) or pos < 0 or m[pos] == 'x':
            return False
          m[pos] = 'x'
          # go left
          traverse(m, pos-1)
          # go right
          traverse(m, pos+1)
          # go down
          traverse(m, pos+11)
          # go up
          traverse(m, pos-11)
 
        traverse(list(char_map), 12)
        # tree is the path the function took
        # to fill the maze
        tree = get_tree()

        self.tv.nodes = 62*[None]
        # from the starting point
        self.tv.nodes[0] = ExecTree(args=[12],ret=None)
        # walk downward twice
        for i in range(2):
          # unable to go left and right
          self.tv.nodes[1+3*i] = ExecTree(args=[11+11*i],ret=False)
          self.tv.nodes[2+3*i] = ExecTree(args=[13+11*i],ret=False)
          # downward
          self.tv.nodes[3+3*i] = ExecTree(args=[23+11*i],ret=None)
        # rightward 5 times
        for i in range(5):
          # unable to go left
          self.tv.nodes[7+2*i] = ExecTree(args=[33+i],ret=False)
          # rightward
          self.tv.nodes[8+2*i] = ExecTree(args=[35+i],ret=None)
        # intersection: the rightward path is taken first 
        # walk rightward trice
        for i in range(3):
          self.tv.nodes[17+2*i] = ExecTree(args=[38+i],ret=False)
          self.tv.nodes[18+2*i] = ExecTree(args=[40+i],ret=None)
        # walls
        for i in range(3):
          self.tv.nodes[23+2*i] = ExecTree(args=[53-i],ret=False)
          self.tv.nodes[24+2*i] = ExecTree(args=[31-i],ret=False)
        self.tv.nodes[29] = ExecTree(args=[50],ret=False)
        # intersection: the upward path is taken second
        # walk upward twice
        self.tv.nodes[30] = ExecTree(args=[28],ret=None)
        # unable to go left, right and downward
        self.tv.nodes[31] = ExecTree(args=[27],ret=False)
        self.tv.nodes[32] = ExecTree(args=[29],ret=False)
        self.tv.nodes[33] = ExecTree(args=[39],ret=False)
        # upward
        self.tv.nodes[34] = ExecTree(args=[17],ret=None)
        # walk leftward trice
        for i in range(3):
          self.tv.nodes[35+i] = ExecTree(args=[16-i],ret=None)
        # walls
        for i in range(4):
          self.tv.nodes[38+3*i] = ExecTree(args=[15+i],ret=False)
          self.tv.nodes[39+3*i] = ExecTree(args=[ 3+i],ret=False)
          self.tv.nodes[40+3*i] = ExecTree(args=[25+i],ret=False)
        for i in range(5):
          self.tv.nodes[50+2*i] = ExecTree(args=[49-i],ret=False)
          self.tv.nodes[51+2*i] = ExecTree(args=[27-i],ret=False)
        for i in range(2):
          self.tv.nodes[60+i] = ExecTree(args=[12-11*i],ret=False)

        assert self.tv.validate(tree)

class TreeValidator:
    def __init__(self):
        # pre order traversal
        # expected nodes
        self.nodes = None
    def validate(self, tree, pos=0):
        if (tree.ret != self.nodes[pos].ret
            or tree.args != self.nodes[pos].args):
          print("{} != {}".format(tree.ret,self.nodes[pos].ret))
          print("{} != {}".format(tree.args,self.nodes[pos].args))
          return False
        else:
          for idx,c in enumerate(tree.childs):
            return self.validate(c, pos + 1 + idx)
          return True

if __name__ == '__main__':
    unittest.main()
