import unittest
from lead_finder import Lead, free_preview, score_lead

class LeadFinderTests(unittest.TestCase):
    def test_score_weights_to_100(self):
        self.assertEqual(score_lead(icp_fit=100, buying_signal=100, ability_to_pay=100, problem_fit=100, timing=100, evidence=100), 100)
    def test_score_zero(self):
        self.assertEqual(score_lead(icp_fit=0, buying_signal=0, ability_to_pay=0, problem_fit=0, timing=0, evidence=0), 0)
    def test_free_is_limited_to_three(self):
        leads=[Lead(f"Company {i}","DE","fit","signal","https://example.com","CEO","unknown",i,"medium","research",[],[]) for i in range(10)]
        self.assertEqual(len(free_preview(leads)),3)
        self.assertEqual(free_preview(leads)[0]["score"],9)

if __name__ == "__main__": unittest.main()
