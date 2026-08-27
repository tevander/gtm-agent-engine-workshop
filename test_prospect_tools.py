import json
import os
import re
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect
from gtm_agent.gtm_records import PROSPECTS


class ProspectToolPrivacyTests(unittest.TestCase):
    def setUp(self):
        data_service._PROFILES.clear()

    def test_prospect_tools_exclude_billing_fields(self):
        for prospect_id in PROSPECTS:
            contact_result = get_prospect.invoke({"prospect_id": prospect_id})
            profile_result = build_prospect_profile.invoke({"prospect_id": prospect_id})

            for result in (contact_result, profile_result):
                serialized = json.dumps(result)
                self.assertNotIn("billing_qualification", serialized)
                self.assertIsNone(re.search(r"\b\d{16}\b", serialized))
                self.assertIsNone(re.search(r"\b\d{3}-\d{2}-\d{4}\b", serialized))


if __name__ == "__main__":
    unittest.main()
