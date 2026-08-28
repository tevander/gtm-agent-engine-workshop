import unittest
from unittest.mock import patch

from gtm_agent import data_service
from gtm_agent.gtm_agent import lookup_offering, send_prospect_email


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


class TestLookupOffering(unittest.TestCase):
    def test_resolves_name_case_insensitively(self):
        result = lookup_offering.func(name="customer experience suite")

        self.assertTrue(result["found"])
        self.assertEqual(result["offering"]["offering_id"], "OFFER-10003")

    def test_returns_candidates_for_unknown_name(self):
        result = lookup_offering.func(name="Unknown Suite")

        self.assertFalse(result["found"])
        self.assertIsNone(result["offering"])
        self.assertEqual(result["candidates"], [])

    def test_returns_candidates_for_ambiguous_name(self):
        duplicate = {"offering_id": "OFFER-TEST", "name": "Analytics Cloud"}
        with patch.dict(data_service.OFFERINGS, {"OFFER-TEST": duplicate}):
            result = lookup_offering.func(name="analytics cloud")

        self.assertFalse(result["found"])
        self.assertIsNone(result["offering"])
        self.assertEqual(result["candidates"], ["Analytics Cloud", "Analytics Cloud"])

    def test_does_not_produce_record_for_unresolved_name(self):
        result = lookup_offering.func(name="Customer Experience")

        self.assertFalse(result["found"])
        self.assertIsNone(result["offering"])
