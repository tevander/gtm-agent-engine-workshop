import unittest

from gtm_agent.gtm_agent import send_prospect_email


class TestSendProspectEmail(unittest.TestCase):
    def test_blocks_disqualified_prospect(self):
        result = send_prospect_email.func(
            {"prospect_id": "LEAD-1", "name": "Casey", "email": "casey@example.com", "disqualified": True},
            "Subject",
            "Body",
            runtime=None,
            from_rep={"name": "Rep", "email": "rep@example.com"},
        )

        self.assertEqual(result["status"], "blocked")
        self.assertNotIn("message_id", result)

    def test_sends_qualified_prospect(self):
        result = send_prospect_email.func(
            {"prospect_id": "LEAD-2", "name": "Jordan", "email": "jordan@example.com", "disqualified": False},
            "Subject",
            "Body",
            runtime=None,
            from_rep={"name": "Rep", "email": "rep@example.com"},
        )

        self.assertEqual(result["status"], "sent")
        self.assertIn("message_id", result)
