import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


class UpdateProspectInfoTest(unittest.TestCase):
    prospect_id = "LEAD-71001"

    def setUp(self):
        self.original_tech_stack = list(
            data_service.PROSPECTS[self.prospect_id]["tech_stack"]
        )
        data_service._PROFILES.clear()

    def tearDown(self):
        data_service.PROSPECTS[self.prospect_id]["tech_stack"] = self.original_tech_stack
        data_service._PROFILES.clear()

    def test_update_persists_for_source_and_profile_reads(self):
        data_service.update_prospect_info(self.prospect_id, "Kafka")

        self.assertIn("Kafka", data_service.fetch_tech_stack(self.prospect_id))
        profile = build_prospect_profile.invoke({"prospect_id": self.prospect_id})
        self.assertIn("Kafka", profile["prospect_profile"]["tech_stack"])


if __name__ == "__main__":
    unittest.main()
