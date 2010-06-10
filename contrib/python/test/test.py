#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Unittests for aterm.

TODO:
- ATerm.parents()


"""
  
import unittest
from aterm import decode, ATerm, ATuple
from itertools import izip,count
 
class TestDecode(unittest.TestCase):
    def de(self,l,r):
        lval = decode(l)
        self.assertEquals()
    
    def test_simple(self):
        #TODO test strict should fail, not strict not
        t = decode('T()')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(t.name, 'T')
        self.assertEquals(len(t), 0)
        t = decode('()')
        self.assert_(isinstance(t, ATuple))
        self.assertEquals(t.name, '()')
        self.assertEquals(len(t), 0)


    def test_annotation(self):
        t = decode("T()")
        self.assertEquals(t.annotation, None)
        t = decode("T(){}")
        self.assertEquals(t.annotation, None)
        t = decode("A(B(){C()}){1}")
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(t.annotation, 1)
        self.assertEquals(repr(t[0].annotation),"C()")

        
    def test_allatonce(self):
        t = decode('T("", "bla", "bla" , S([ "", "bla", "bla" ] ))')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(t.name, "T")
        self.assertEquals(len(t), 4)


class TestTree(unittest.TestCase):
    def test_tree(self):
        t = decode('A(B(C()),[])')
        self.assertEquals(t.up, None)
        self.assertEquals(t[0].name, "B")
        self.assertEquals(t[0].up, t)
        self.assertEquals(t[1].up, t)

    def test_walk(self):
        t = decode("A(B(C(),D()))")
        w = ''.join([n.name for n in t.walk()])
        self.assertEquals(w, "ABCD")        

class TestEncode(unittest.TestCase):
    def de(self,src,enc=None):
        d = decode(src)
        if enc is None:
            enc = src
        self.assertEquals(repr(d),enc)
        
    def test_decode_encode(self):
        self.de('A()')
        self.de('A(){}','A()')
        self.de('A(){1}','A(){1}')
        self.de('A("")')
        self.de('A("b")')
        self.de('A([])')
        self.de('A([B()])')
        self.de('A([B(),C()])')

class TestPos(unittest.TestCase):
    def test_pos(self):
        t = decode('A(B(),C(),D())')
        self.assertEquals(t[0].name, "B")
        self.assertEquals(t[0].pos(), 0)
        self.assertEquals(t[1].name, "C")
        self.assertEquals(t[1].pos(), 1)
        self.assertEquals(t[2].name, "D")
        self.assertEquals(t[2].pos(), 2)
        
class TestFind(unittest.TestCase):
    def test_find(self):
        t = decode('A(B(C(D())),[])')
        r = [i for i in t.findall('C') ]
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0][0].name,"D")        
                               
if __name__ == '__main__':
    unittest.main()
 
