"""Tests for agent-draft-verifier."""
import unittest
from agent_draft_verifier.verifier import AgentDraftVerifier


class TestDraftVerifier(unittest.TestCase):
    def test_all_accepted(self):
        v = AgentDraftVerifier(lambda ctx, tok: True)
        s = v.verify_tokens("Ctx:", ["alpha", "beta", "gamma"])
        self.assertEqual(len(s.accepted_tokens), 3)
        self.assertEqual(s.acceptance_rate, 1.0)

    def test_divergence(self):
        v = AgentDraftVerifier(lambda ctx, tok: tok != "bad")
        s = v.verify_tokens("Ctx:", ["good", "bad", "ignored"])
        self.assertEqual(s.accepted_tokens, ["good"])
        self.assertEqual(s.rejected_tokens, ["bad", "ignored"])
        self.assertAlmostEqual(s.acceptance_rate, 1 / 3, places=2)
