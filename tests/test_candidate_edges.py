from unittest import TestCase
import pandas as pd
from pasigram.service.candidate_edges_service import *
from pasigram.model.edges import *


class TestCandidateEdges(TestCase):
    def test_compute_frequent_edges(self):
        edges = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\tests_data\edges_with_labels.csv', sep=';',
                            index_col=['id'])

        result = compute_frequent_edges(2, edges)
        print(result)
