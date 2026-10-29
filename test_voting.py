import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from main import VotingSystem, main


class VotingTests(unittest.TestCase):
    def setUp(self):
        self.system = VotingSystem()
        self.system.add_candidate("C1", "Alice")
        self.system.add_voter("V1", "Bob")

    def test_vote_records_transaction_and_flag(self):
        self.system.cast_vote("V1", "C1")
        self.assertTrue(self.system.voters["V1"].has_voted)
        self.assertEqual(self.system.blockchain.chain[1].transactions,
                         [{"type": "VOTE", "voter_id": "V1", "candidate_id": "C1"}])
        self.assertTrue(self.system.blockchain.validate())

    def test_duplicate_ids(self):
        for action, identifier in [(self.system.add_candidate, "C1"),
                                   (self.system.add_voter, "V1")]:
            with self.assertRaises(ValueError):
                action(identifier, "Duplicate")

    def test_double_voting_rejected_without_extra_block(self):
        self.system.cast_vote("V1", "C1")
        with self.assertRaises(ValueError):
            self.system.cast_vote("V1", "C1")
        self.assertEqual(len(self.system.blockchain.chain), 2)

    def test_unknown_ids_do_not_consume_vote(self):
        for voter, candidate in [("missing", "C1"), ("V1", "missing")]:
            with self.assertRaises(ValueError):
                self.system.cast_vote(voter, candidate)
        self.assertFalse(self.system.voters["V1"].has_voted)
        self.assertEqual(len(self.system.blockchain.chain), 1)

    def test_empty_fields_and_trimmed_ids(self):
        for identifier, name in [("  ", "Name"), ("ID", " ")]:
            with self.assertRaises(ValueError):
                self.system.add_voter(identifier, name)
            with self.assertRaises(ValueError):
                self.system.add_candidate(identifier, name)
        with self.assertRaises(ValueError):
            self.system.add_voter(" V1 ", "Duplicate")

    def test_transaction_tampering_detected_and_further_vote_blocked(self):
        self.system.cast_vote("V1", "C1")
        self.system.blockchain.chain[1].transactions[0]["candidate_id"] = "changed"
        self.assertFalse(self.system.blockchain.validate())
        self.system.add_voter("V2", "Carol")
        with self.assertRaises(ValueError):
            self.system.cast_vote("V2", "C1")
        self.assertFalse(self.system.voters["V2"].has_voted)

    def test_broken_link_detected_even_with_recomputed_hash(self):
        self.system.cast_vote("V1", "C1")
        block = self.system.blockchain.chain[1]
        block.previous_hash = "wrong"
        block.hash = block.calculate_hash()
        self.assertFalse(self.system.blockchain.validate())

    def test_genesis_and_index_validation(self):
        self.assertTrue(self.system.blockchain.validate())
        self.system.blockchain.chain[0].index = 5
        self.assertFalse(self.system.blockchain.validate())

    def test_full_menu_flow(self):
        inputs = ["invalid", "1", "C1", "Alice", "2", "V1", "Bob",
                  "3", "V1", "C1", "3", "V1", "C1", "4", "5", "6"]
        output = StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            main()
        result = output.getvalue()
        for expected in ["Invalid choice", "Vote recorded successfully",
                         "already voted", "Block 1", "Previous hash:",
                         "Blockchain is valid.", "Goodbye!"]:
            self.assertIn(expected, result)
        self.assertEqual(result.count("=== Voting Management System ==="), 8)


if __name__ == "__main__":
    unittest.main()
