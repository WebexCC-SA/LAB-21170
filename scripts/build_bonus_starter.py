"""Build a credential-free Contact Center MCP practice draft."""

from __future__ import annotations

import copy
import json
import sys
import uuid
from pathlib import Path

BASELINE_MESSAGE = "Please contact our support team during business hours. Thank you for calling."


def build(source: dict) -> dict:
    """Reuse exported activity schemas, not the source flow's integrations."""
    # Copy only export settings; unrelated source metadata must not leak into
    # a publicly downloadable practice flow.
    flow = {key: copy.deepcopy(source[key]) for key in ("flowType", "persist", "settings", "__typename")}
    source_activities = {a["name"]: a for a in source["process"]["activities"].values()}
    source_nodes = {
        w["properties"]["name"]: w
        for w in source["diagram"]["widgets"].values()
        if w["type"] != "arrow"
    }
    activities, widgets, nodes = {}, {}, {}
    selections = (
        ("NewPhoneContact", "NewPhoneContact", (0, 100)),
        ("WelcomePrompt", "EscalationMessage", (300, 100)),
        ("EndFlow_jxc", "EndFlow", (600, 100)),
    )
    for original, name, (x, y) in selections:
        activity = copy.deepcopy(source_activities[original])
        activity["id"] = str(uuid.uuid4())
        activity["name"] = activity["properties"]["name"] = name
        activity["properties"].pop("_renderRequestTimestamp", None)
        if name == "NewPhoneContact":
            activity["properties"]["description"] = "Entry activity for the unpublished MCP practice flow."
        elif name == "EscalationMessage":
            # Explicit defaults avoid optional nulls becoming the string "null"
            # when the MCP serializes a patched draft back to Flow Designer.
            activity["properties"].update({
                "description": "Explains how to reach the support team.",
                "promptsTts": [{"type": "tts", "value": BASELINE_MESSAGE, "name": BASELINE_MESSAGE}],
                "volumeGainDb": "0", "speakingRate": "1",
                "toggleLanguage": "", "voiceLanguage_name": "", "flowDecryptAccess": "",
                "connector:type": "Cisco Cloud Text-to-Speech",
                "connector_type": "Cisco Cloud Text-to-Speech",
            })
        activities[activity["id"]] = activity
        node = copy.deepcopy(source_nodes[original])
        node["id"] = str(uuid.uuid4())
        dx, dy = x - node["point"]["x"], y - node["point"]["y"]
        node["point"] = {"x": x, "y": y}
        node["properties"] = copy.deepcopy(activity["properties"])
        for port in node["ports"]:
            port["portId"] = str(uuid.uuid4())
            port["links"], port["linkId"] = [], None
            port["properties"]["x"] += dx
            port["properties"]["y"] += dy
        widgets[activity["id"]] = node
        nodes[name] = node

    by_name = {a["name"]: a for a in activities.values()}
    arrow_template = next(w for w in source["diagram"]["widgets"].values() if w["type"] == "arrow")
    links = []
    for source_name, outcome, destination in (
        ("NewPhoneContact", "out", "EscalationMessage"),
        ("EscalationMessage", "default", "EndFlow"),
        ("EscalationMessage", "error", "EndFlow"),
    ):
        ports = (
            next(p for p in nodes[source_name]["ports"] if p["properties"]["name"] == outcome),
            next(p for p in nodes[destination]["ports"] if p["properties"]["name"] == "in"),
        )
        link_id, arrow_id = str(uuid.uuid4()), str(uuid.uuid4())
        links.append({
            "id": link_id, "sourceActivityId": by_name[source_name]["id"],
            "targetActivityId": by_name[destination]["id"], "conditionExpr": outcome,
            "properties": {"value": outcome},
        })
        arrow = copy.deepcopy(arrow_template)
        arrow["id"] = arrow_id
        for side, name, port in zip(("sourcePort", "targetPort"), (source_name, destination), ports):
            arrow[side] = {
                "id": port["portId"], "activeWidgetId": nodes[name]["id"],
                "point": {axis: round(port["properties"][axis]) for axis in ("x", "y")},
            }
            port["links"].append(arrow_id)
            port["linkId"] = port["links"][0]
        arrow["properties"]["points"] = [
            {"id": str(uuid.uuid4()), "type": "point", **arrow[side]["point"]}
            for side in ("sourcePort", "targetPort")
        ]
        arrow["properties"]["color"] = (
            "var(--mds-color-theme-outline-cancel-normal)" if outcome == "error"
            else "var(--mds-color-theme-outline-theme-normal)"
        )
        arrow["points"] = []
        widgets[link_id] = arrow

    # Keep default event entry nodes, not the source's custom event handlers.
    # Event-path End Flow nodes currently round-trip through MCP as actions;
    # avoiding them keeps this narrowly tested practice draft editable.
    event_flows = copy.deepcopy(source["eventFlows"])
    global_events = event_flows["eventsMap"]["GLOBAL_EVENTS"]
    event_activities = {
        key: value for key, value in global_events["process"]["activities"].items() if value["group"] == "event"
    }
    global_events["process"] = {"activities": event_activities, "links": []}
    global_events["diagram"]["widgets"] = {
        key: value for key, value in global_events["diagram"]["widgets"].items() if key in event_activities
    }
    for key, activity in event_activities.items():
        activity["properties"].pop("_renderRequestTimestamp", None)
        node = global_events["diagram"]["widgets"][key]
        node["properties"] = copy.deepcopy(activity["properties"])
        for port in node["ports"]:
            port["links"], port["linkId"] = [], None
    global_events["onEvents"] = {a["name"]: key for key, a in event_activities.items()}

    # Exclude variable values and org-bound assets from the practice draft.
    flow.update({
        "name": "ServiceDeskMCPBonus", "version": 0,
        "description": "LAB-21170 standalone MCP practice draft. Do not publish or route calls to it.",
        "comment": None, "variables": [], "runtimeVariables": [],
        "variableOrders": {"pop-over": [], "interaction-panel": []},
        "process": {"activities": activities, "links": links},
        "diagram": {"widgets": widgets, "properties": {"offsetX": 80, "offsetY": 80, "zoom": 100, "gridSize": 20}},
        "eventFlows": event_flows,
        "associatedChannels": [], "validationResults": [], "validating": False,
        "flowOutcome": None,
    })
    for field in ("id", "flowId", "orgId", "createdBy", "createdDate", "lastModifiedBy", "lastModifiedDate"):
        flow.pop(field, None)
    return flow


if __name__ == "__main__":
    source_path, output_path = map(Path, sys.argv[1:])
    result = build(json.loads(source_path.read_text()))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n")
