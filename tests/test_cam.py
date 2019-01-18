from unittest import TestCase
import pandas as pd
from pasigram.datastructures.graph import Graph


class TestCam(TestCase):
    def test_get_canonical_code(self):
        nodes1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes.csv', sep=';')
        nodes2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes2.csv', sep=';')
        edges1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges.csv', sep=';')
        edges2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges2.csv', sep=';')

        graph1 = Graph(nodes1, edges1)
        graph2 = Graph(nodes2, edges2)
        code1 = graph1.get_canonical_code
        code2 = graph2.get_canonical_code
        self.assertEqual(code1, code2, msg="Test1")

    def test_negative_get_canonical_code(self):
        nodes1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\nodes1.csv', sep=';')
        nodes2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\nodes2.csv', sep=';')
        edges1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\edges1.csv', sep=';')
        edges2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\edges2.csv', sep=';')

        graph1 = Graph(nodes1, edges1)
        graph2 = Graph(nodes2, edges2)
        code1 = graph1.get_canonical_code
        code2 = graph2.get_canonical_code
        print(code1)
        print(code2)
        self.assertIsNot(code1, code2, msg="Test1")
