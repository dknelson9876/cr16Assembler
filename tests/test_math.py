import unittest
from io import StringIO
import sys

from src.assembler2 import Assembler

class AssemblerTest(unittest.TestCase):
    
    def test_add(self):
        with StringIO() as output:
            sys.stdout = output
            asmblr = Assembler()
            asmblr.assemble(['ADD r1 r2'])
            self.assertEqual(output.getvalue().strip(), "0251")
            sys.stdout = sys.__stdout__
            
    def test_addi(self):
        with StringIO() as output:
            sys.stdout = output
            asmblr = Assembler()
            asmblr.assemble(['ADDI $1 r1'])
            self.assertEqual(output.getvalue().strip(), '5101')
            sys.stdout = sys.__stdout__
            
    def test_addu(self):
        with StringIO() as output:
            sys.stdout = output
            asmblr = Assembler()
            asmblr.assemble(['ADDU r2 r1'])
            self.assertEqual(output.getvalue().strip(), '0162')
            sys.stdout = sys.__stdout__
            
    def test_addui(self):
        with StringIO() as output:
            sys.stdout = output
            asmblr = Assembler()
            asmblr.assemble(['ADDUI $1 r1'])
            self.assertEqual(output.getvalue().strip(), '6101')
            sys.stdout = sys.__stdout__
            
    def test_add_series(self):
        with StringIO() as output:
            sys.stdout = output
            asmblr = Assembler()
            asmblr.assemble([
                'ADD r1 r2',
                'ADD r2 r3',
                'ADD r3 r4',
                'ADD r4 r5',
                'ADD r5 r6',
                'ADD r6 r7',
                'ADD r7 r8',
                'ADD r8 r9',
                'ADD r9 r10',
                'ADD r10 r11',
                'ADD r11 r12',
                'ADD r12 r13',
                'ADD r13 rA',
                'ADD rA rsp'
            ])
            expected = '0251\n0352\n0453\n0554\n0655\n0756\n0857\n0958\n0A59\n0B5A\n0C5B\n0D5C\n0E5D\n0F5E'
            self.assertEqual(output.getvalue().strip(), expected)
            sys.stdout = sys.__stdout__
            
    
            