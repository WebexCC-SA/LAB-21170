"""Structural checks for the attendee's importable ServiceDesk flow."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "docs/assets/lab-guide/ServiceDesk-starter.json"
SOURCE = ROOT / "scripts/starter_flow_source.json"


class StarterFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flow = json.loads(STARTER.read_text())
        cls.activities = {
            activity["name"]: activity
            for activity in cls.flow["process"]["activities"].values()
        }
        ids = {activity["id"]: name for name, activity in cls.activities.items()}
        cls.links = {
            (ids[link["sourceActivityId"]], link["conditionExpr"], ids[link["targetActivityId"]])
            for link in cls.flow["process"]["links"]
        }

    def test_attendee_paths(self):
        self.assertEqual(len(self.activities), 12)
        self.assertTrue({
            ("NewPhoneContact", "out", "WelcomePrompt"),
            ("WelcomePrompt", "default", "SupportMenu"),
            ("SupportMenu", "1", "GetOrder"),
            ("GetOrder", "default", "OrderStatusMessage"),
            ("OrderStatusMessage", "default", "Queue"),
            ("SupportMenu", "2", "Queue"),
            ("Queue", "default", "Music"),
            ("Music", "default", "PlayMessage_c24"),
            ("PlayMessage_c24", "default", "Music"),
            ("MenuFallbackMessage", "default", "EndFlow_jxc"),
        }.issubset(self.links))
        for outcome in ("timeout", "invalid", "error"):
            self.assertIn(("SupportMenu", outcome, "MenuFallbackMessage"), self.links)

    def test_lookup_has_only_a_placeholder_credential(self):
        request = self.activities["GetOrder"]["properties"]
        self.assertEqual(request["httpRequestMethod"], "GET")
        self.assertEqual(
            request["httpRequestUrl"],
            "https://mcp-lab.webexdevs.com/order-desk/api/orders/ORD-10482",
        )
        self.assertEqual(request["httpRequestHeaders"], {
            "Authorization": "Bearer REPLACE_WITH_LAB_TOKEN"
        })
        self.assertEqual(request["outputVariableArray"], [{
            "outputVariable": "orderStatus", "jsonPathExp": "$.order.status"
        }])
        self.assertEqual(self.flow["variables"][0]["value"], "unavailable")
        for path in (STARTER, SOURCE):
            content = path.read_text()
            self.assertNotIn("CLASS1-", content)
            self.assertNotIn("od1.", content)

    def test_queue_target_is_portable(self):
        queue = self.activities["Queue"]["properties"]
        self.assertEqual(queue["destination"], "00000000-0000-4000-8000-000000000000")
        self.assertEqual(queue["destination:name"], "Queue-1")
        self.assertEqual(queue["destination_name"], "Queue-1")


if __name__ == "__main__":
    unittest.main()
