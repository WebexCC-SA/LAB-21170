"""Build a portable lab starter from a Flow Designer draft export.

Usage: .venv/bin/python scripts/build_starter_flow.py \
    scripts/starter_flow_source.json docs/assets/lab-guide/ServiceDesk-starter.json

The input is a credential-free ServiceDesk draft exported in the sandbox.
This script is retained so the topology can be regenerated and audited.
"""

from __future__ import annotations

import copy
import json
import sys
import uuid
from pathlib import Path


def uid() -> str:
    return str(uuid.uuid4())


def main(source: Path, output: Path) -> None:
    flow = json.loads(source.read_text())
    activities = flow["process"]["activities"]
    widgets = flow["diagram"]["widgets"]
    by_name = {activity["name"]: activity for activity in activities.values()}
    node_by_name = {
        widget["properties"]["name"]: widget
        for widget in widgets.values()
        if widget["type"] != "arrow"
    }

    # The source export has its original queue ID sanitized. Attendees confirm
    # the queue binding after import; Flow Designer resolves it by name.
    flow["name"] = "ServiceDesk"
    flow["description"] = (
        "LAB-21170 starter: IVR menu, direct Order Desk HTTP lookup, and queue treatment. "
        "Replace only the placeholder bearer, then verify the queue target."
    )
    flow["variables"][0]["value"] = "unavailable"
    for queue_properties in (
        by_name["Queue"]["properties"],
        node_by_name["Queue"]["properties"],
    ):
        # Flow Designer resolves this by the preserved Queue-1 name at import.
        # A sanitized invalid ID verified that its importer rebinds the queue.
        queue_properties["destination"] = "00000000-0000-4000-8000-000000000000"
    by_name["WelcomePrompt"]["properties"]["description"] = "Welcome the caller before the IVR menu"
    node_by_name["WelcomePrompt"]["properties"]["description"] = "Welcome the caller before the IVR menu"

    def make_message(name: str, message: str, point: tuple[int, int]) -> None:
        activity = copy.deepcopy(by_name["WelcomePrompt"])
        activity["id"] = uid()
        activity["name"] = name
        activity["properties"]["name"] = name
        activity["properties"]["description"] = ""
        activity["properties"]["promptsTts"] = [
            {"type": "tts", "value": message, "name": message}
        ]
        activities[activity["id"]] = activity
        by_name[name] = activity

        node = copy.deepcopy(node_by_name["WelcomePrompt"])
        node["id"] = uid()
        node["point"] = {"x": point[0], "y": point[1]}
        node["properties"] = copy.deepcopy(activity["properties"])
        for port in node["ports"]:
            port["portId"] = uid()
            port["linkId"] = None
            port["links"] = []
        widgets[activity["id"]] = node
        node_by_name[name] = node

    make_message(
        "OrderStatusMessage", "Your order status is {{orderStatus}}.", (920, 70)
    )
    make_message(
        "MenuFallbackMessage", "I did not get a valid choice. Please call again.", (690, 500)
    )

    locations = {
        "NewPhoneContact": (0, 150),
        "WelcomePrompt": (210, 150),
        "SupportMenu": (420, 150),
        "GetOrder": (690, 70),
        "OrderStatusMessage": (920, 70),
        "Queue": (1170, 170),
        "Music": (1400, 170),
        "PlayMessage_c24": (1630, 170),
        "MenuFallbackMessage": (690, 500),
        "EndFlow_jxc": (920, 500),
        "EndFlow_p88": (1400, 500),
        "EndFlow_vb9": (1630, 500),
    }
    for name, (x, y) in locations.items():
        widget = node_by_name[name]
        dx, dy = x - widget["point"]["x"], y - widget["point"]["y"]
        widget["point"] = {"x": x, "y": y}
        for port in widget["ports"]:
            port["properties"]["x"] += dx
            port["properties"]["y"] += dy

    def port(name: str, edge: str) -> dict:
        return next(
            p for p in node_by_name[name]["ports"] if p["properties"]["name"] == edge
        )

    # Preserve the working template's queue/music loop and error destinations.
    # Replace only the default WelcomePrompt -> Queue arrow.
    old = next(
        link
        for link in flow["process"]["links"]
        if link["sourceActivityId"] == by_name["WelcomePrompt"]["id"]
        and link["conditionExpr"] == "default"
    )
    flow["process"]["links"].remove(old)
    arrow = next(
        widget
        for widget in widgets.values()
        if widget["type"] == "arrow"
        and widget["sourcePort"]["activeWidgetId"] == node_by_name["WelcomePrompt"]["id"]
        and widget["sourcePort"]["id"] == port("WelcomePrompt", "default")["portId"]
    )
    del widgets[old["id"]]
    for p in (port("WelcomePrompt", "default"), port("Queue", "in")):
        p["links"].remove(arrow["id"])
        p["linkId"] = p["links"][0] if p["links"] else None

    arrow_template = next(widget for widget in widgets.values() if widget["type"] == "arrow")

    def connect(source_name: str, edge: str, target_name: str) -> None:
        source_node, target_node = node_by_name[source_name], node_by_name[target_name]
        source_port, target_port = port(source_name, edge), port(target_name, "in")
        link_id = uid()
        flow["process"]["links"].append({
                "id": link_id,
                "sourceActivityId": by_name[source_name]["id"],
                "targetActivityId": by_name[target_name]["id"],
                "conditionExpr": edge,
                "properties": {"value": edge},
            })
        new_arrow = copy.deepcopy(arrow_template)
        new_arrow["id"] = uid()
        new_arrow["sourcePort"] = {
            "id": source_port["portId"],
            "activeWidgetId": source_node["id"],
            "point": {
                "x": round(source_port["properties"]["x"]),
                "y": round(source_port["properties"]["y"]),
            },
        }
        new_arrow["targetPort"] = {
            "id": target_port["portId"],
            "activeWidgetId": target_node["id"],
            "point": {
                "x": round(target_port["properties"]["x"]),
                "y": round(target_port["properties"]["y"]),
            },
        }
        new_arrow["properties"]["points"] = [
            {"id": uid(), "type": "point", "x": p["properties"]["x"], "y": p["properties"]["y"]}
            for p in (source_port, target_port)
        ]
        new_arrow["properties"]["color"] = (
            "var(--mds-color-theme-outline-cancel-normal)"
            if edge in {"error", "failure", "timeout", "invalid"}
            else "var(--mds-color-theme-outline-theme-normal)"
        )
        widgets[link_id] = new_arrow
        for p in (source_port, target_port):
            p["links"].append(new_arrow["id"])
            p["linkId"] = p["links"][0]

    connect("WelcomePrompt", "default", "SupportMenu")
    connect("SupportMenu", "1", "GetOrder")
    connect("SupportMenu", "2", "Queue")
    for edge in ("timeout", "invalid", "error"):
        connect("SupportMenu", edge, "MenuFallbackMessage")
    connect("GetOrder", "default", "OrderStatusMessage")
    connect("OrderStatusMessage", "default", "Queue")
    connect("MenuFallbackMessage", "default", "EndFlow_jxc")

    assert set(activities) <= set(widgets), "Every activity needs a diagram widget"
    assert all(link["id"] in widgets for link in flow["process"]["links"])
    assert all(
        link["sourceActivityId"] in activities and link["targetActivityId"] in activities
        for link in flow["process"]["links"]
    )
    assert by_name["GetOrder"]["properties"]["httpRequestHeaders"] == {
        "Authorization": "Bearer REPLACE_WITH_LAB_TOKEN"
    }

    # Import creates a new flow identity. Keep only the exported flow payload;
    # import validation will show whether the target org accepts queue binding.
    for field in ("id", "flowId", "orgId", "createdBy", "createdDate", "lastModifiedBy", "lastModifiedDate"):
        flow.pop(field, None)
    assert "CLASS1-" not in json.dumps(flow), "Never export a live lab token"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(flow, indent=2) + "\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
