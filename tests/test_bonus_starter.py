"""Regression checks for the standalone bonus attendee download."""

import json
import re
import unittest
from pathlib import Path

from scripts.build_bonus_starter import BASELINE_MESSAGE, build


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "docs/assets/lab-guide/ServiceDeskMCPBonus-starter.json"


class BonusStarterTests(unittest.TestCase):
    def setUp(self):
        self.flow = json.loads(ASSET.read_text())

    def test_only_the_three_practice_activities_and_complete_path(self):
        activities = self.flow["process"]["activities"]
        names = {key: a["name"] for key, a in activities.items()}
        self.assertEqual(set(names.values()), {"NewPhoneContact", "EscalationMessage", "EndFlow"})
        self.assertEqual({
            (names[link["sourceActivityId"]], link["conditionExpr"], names[link["targetActivityId"]])
            for link in self.flow["process"]["links"]
        }, {
            ("NewPhoneContact", "out", "EscalationMessage"),
            ("EscalationMessage", "default", "EndFlow"),
            ("EscalationMessage", "error", "EndFlow"),
        })
        self.assertEqual(self.flow["version"], 0)
        self.assertEqual(self.flow["name"], "ServiceDeskMCPBonus")
        end = next(a for a in activities.values() if a["name"] == "EndFlow")
        self.assertEqual(end["properties"]["description"], "Ends the Flow")
        self.assertEqual(end["group"], "end")
        self.assertEqual(self.flow["diagram"]["widgets"][end["id"]]["type"], "end")
        self.assertEqual([p["properties"]["name"] for p in self.flow["diagram"]["widgets"][end["id"]]["ports"]], ["in"])

    def test_voice_message_and_round_trip_defaults(self):
        message = next(a for a in self.flow["process"]["activities"].values() if a["name"] == "EscalationMessage")
        props = message["properties"]
        self.assertEqual(message["group"], "action")
        self.assertEqual(props["activityType"], "core")
        self.assertEqual(props["activityName"], "play-message")
        self.assertTrue(props["toggle"])
        self.assertEqual(props["connector"], "Cisco Cloud Text-to-Speech")
        self.assertEqual(props["promptsTts"], [{"type": "tts", "value": BASELINE_MESSAGE, "name": BASELINE_MESSAGE}])
        self.assertEqual(props["volumeGainDb"], "0")
        self.assertEqual(props["speakingRate"], "1")
        for key in ("toggleLanguage", "voiceLanguage_name", "flowDecryptAccess"):
            self.assertEqual(props[key], "")

    def test_no_credentials_org_identity_or_integrations(self):
        for field in ("id", "flowId", "orgId", "createdBy", "lastModifiedBy"):
            self.assertNotIn(field, self.flow)
        self.assertEqual(self.flow["variables"], [])
        self.assertEqual(self.flow["runtimeVariables"], [])
        self.assertEqual(self.flow["associatedChannels"], [])
        event = self.flow["eventFlows"]["eventsMap"]["GLOBAL_EVENTS"]
        self.assertTrue(event["process"]["activities"])
        self.assertTrue(all(a["group"] == "event" for a in event["process"]["activities"].values()))
        self.assertIn("GlobalErrorHandling", event["onEvents"])
        self.assertEqual(event["process"]["links"], [])
        self.assertEqual(set(event["onEvents"].values()), set(event["process"]["activities"]))
        for node in event["diagram"]["widgets"].values():
            self.assertEqual(node["type"], "event")
            for port in node["ports"]:
                self.assertEqual(port["links"], [])
                self.assertIsNone(port["linkId"])
        text = ASSET.read_text()
        for forbidden in ("CLASS1-", "od1.", "Bearer", "Authorization", "httpRequest", "destination", "virtualAgent", "SandboxUpload", "httpbin", "Queue-1", "ScreenPop"):
            self.assertNotIn(forbidden, text)

    def test_diagram_and_process_agree(self):
        widgets = self.flow["diagram"]["widgets"]
        for activity_id, activity in self.flow["process"]["activities"].items():
            self.assertEqual(widgets[activity_id]["properties"], activity["properties"])
        for link in self.flow["process"]["links"]:
            arrow = widgets[link["id"]]
            for side, field in (("sourcePort", "sourceActivityId"), ("targetPort", "targetActivityId")):
                node = widgets[link[field]]
                self.assertEqual(arrow[side]["activeWidgetId"], node["id"])
                port = next(p for p in node["ports"] if p["portId"] == arrow[side]["id"])
                self.assertIn(arrow["id"], port["links"])
                self.assertIn(port["linkId"], port["links"])

    def test_builder_does_not_mutate_source_and_assigns_fresh_ids(self):
        source = json.loads((ROOT / "scripts/starter_flow_source.json").read_text())
        before = json.dumps(source, sort_keys=True)
        first, second = build(source), build(source)
        self.assertEqual(json.dumps(source, sort_keys=True), before)
        first_ids = set(first["process"]["activities"])
        self.assertTrue(first_ids.isdisjoint(second["process"]["activities"]))
        self.assertTrue(first_ids.isdisjoint(source["process"]["activities"]))

    def test_unrelated_source_metadata_is_not_exported(self):
        source = json.loads((ROOT / "scripts/starter_flow_source.json").read_text())
        source.update({"orgId": "PRIVATE-ORG", "createdBy": "PRIVATE-USER", "secret": "PRIVATE-TOKEN"})
        source["variables"] = [{"name": "secret", "value": "PRIVATE-TOKEN"}]
        result = json.dumps(build(source))
        for value in ("PRIVATE-ORG", "PRIVATE-USER", "PRIVATE-TOKEN"):
            self.assertNotIn(value, result)

    def test_attendee_patch_keeps_the_tested_serialization_guards(self):
        guide = (ROOT / "docs/bonus_contact_center_mcp.md").read_text()
        section = guide.split("### Apply the bounded patch\n", 1)[1]
        prompt = re.search(r"```text\n(.*?)\n```", section, re.DOTALL).group(1)
        request = json.loads(prompt[prompt.index("{"):].replace("<current draft version>", "7"))
        self.assertEqual(request["expected_version"], 7)
        self.assertEqual(request["org_id"], "<your organization ID>")
        self.assertEqual(request["flow_id"], "<your ServiceDeskMCPBonus flow ID>")
        self.assertEqual(request["flow_type"], "FLOW")
        self.assertEqual(set(request["patch"]), {"upsert_nodes"})
        message, end = request["patch"]["upsert_nodes"]
        self.assertEqual(end, {"name": "EndFlow", "activityType": "end"})
        self.assertEqual(message["name"], "EscalationMessage")
        self.assertEqual(message["activityType"], "action")
        baseline = next(a["properties"] for a in self.flow["process"]["activities"].values() if a["name"] == message["name"])
        for field in ("volumeGainDb", "speakingRate", "toggleLanguage", "voiceLanguage_name", "flowDecryptAccess"):
            self.assertEqual(message["properties"][field], baseline[field])
        tts = message["properties"]["promptsTts"][0]
        self.assertEqual(tts["name"], tts["value"])
        self.assertEqual(tts["type"], "tts")
        self.assertNotEqual(tts["value"], BASELINE_MESSAGE)
        self.assertIn("zero errors", guide)
        self.assertNotIn("### Create a copy, not a replacement", guide)


if __name__ == "__main__":
    unittest.main()
