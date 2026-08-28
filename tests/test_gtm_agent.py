import unittest

from gtm_agent.gtm_agent import send_prospect_email


class TestSendProspectEmail(unittest.TestCase):
    def test_blocks_disqualified_prospect(self):
        result = send_prospect_email.func(
            {"prospect_id": "LEAD-50001", "name": "Priya Nair", "email": "priya.nair@brightwaveapps.com"},
            "Subject",
            "Body",
            runtime=None,
            from_rep={"name": "Rep", "email": "rep@example.com"},
        )

        self.assertEqual(result["status"], "blocked")
        self.assertNotIn("message_id", result)

    def test_override_sends_disqualified_prospect(self):
        result = send_prospect_email.func(
            {"prospect_id": "LEAD-50001", "name": "Priya Nair", "email": "priya.nair@brightwaveapps.com"},
            "Subject",
            "Body",
            runtime=None,
            from_rep={"name": "Rep", "email": "rep@example.com"},
            override_disqualified=True,
        )

        self.assertEqual(result["status"], "sent")
        self.assertIn("message_id", result)
