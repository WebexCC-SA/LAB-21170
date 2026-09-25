# Overview

## What you will build

You run the contact center for a mock online retailer. A caller wants an update on order `ORD-10482`. Build a practice IVR, then replace it with an AI agent that can look up the order and connect the caller to a person when needed.

```text
Practice path:
  Caller → welcome message → menu
         ├─ 1 order support → Order Desk REST test → status → Queue-1 → wait treatment
         └─ 2 general support ─────────────────────────→ Queue-1 → wait treatment

Final path:
  Caller → AI agent
         ├─ order request → Order Desk MCP → response → Handled → end
         ├─ general support → offer human → Escalated → Queue-1 → wait treatment
         └─ Errored → spoken error message → disconnect
```

In the practice flow, digit `1` looks up an order through REST before joining `Queue-1`; digit `2` joins the queue directly. In the final flow, the caller goes straight to the AI agent. A handled request ends, an escalation enters the human queue, and an error plays a clear fallback before disconnecting. The final path has no numbered menu.

<figure markdown>
  ![Simplified practice path through welcome, menu, REST lookup and queue treatment, and final AI-agent path with handled and human-escalation outcomes](assets/lab-guide/00-solution-evolution.png)
  <figcaption markdown="span">Practice digit 2 bypasses REST and joins the queue. The final path uses the approved Order Desk MCP action; dashed queue links are configured in later checkpoints.</figcaption>
</figure>

See [Checkpoint 9's reference topology](lab5_end_to_end.md) for the final outcomes and queue-error path.

Both paths use the same simulated Order Desk data, so you can compare the REST result with the agent's answer.

## Your role

You will:

- check the assigned sandbox in **Control Hub**;
- build and publish the call flow in **Flow Designer**;
- prepare the order-support agent in **AI Agent Studio**;
- confirm the external MCP registration in **Developer Portal**;
- test the simulated Order Desk service in **MCP Lab**; and
- call the assigned phone number to validate each published version.

In the final phone test, you speak as the caller.

## Lab tools

| Layer | Product | Open | What you do |
| --- | --- | --- | --- |
| Organization | **Control Hub** | [admin.webex.com](https://admin.webex.com/) | Check your organization, entry point, and queue. |
| Runtime | **Flow Designer** | [Open from Control Hub](https://admin.webex.com/) or use the [direct lab URL](https://flow-control.produs1.ciscoccservice.com/) | Build and publish flows, test REST, and connect the AI agent's outcomes. |
| Conversation | **AI Agent Studio** | [studio.aiagent-us1.cisco.com](https://studio.aiagent-us1.cisco.com/) for this ProdUS1 lab, or launch via **Control Hub → Contact Center → Customer Experience → AI Agents** | Set instructions, approved actions, and response behavior. |
| Developer access | **Developer Portal** | [developer.webex.com](https://developer.webex.com/) | Register the external MCP. This is not the Flow Designer canvas. |

**MCP Lab** supplies your temporary assignment and the synthetic Order Desk REST and MCP endpoints. MCP Lab and Order Desk are lab services, not Webex products.

## Lab sequence

Work through the checkpoints in order:

1. Redeem the sandbox assignment and bookmark the lab workspaces.
2. Build and publish a **Simple Inbound Call to Queue** flow, assign it to the entry point, and call the assigned number.
3. Inspect a call in **Flow Debugging**; make two or three more calls and compare them in **Flow Analytics**.
4. Build the starter IVR with general support routed to `Queue-1`. Use the **Comprehensive Call Flow** template as a reference for wait treatment and an optional callback; test by phone.
5. Publish the Order Desk REST branch in Flow Designer, then verify its response by phone, Debugging, and Analytics.
6. Move the HTTP request into a subflow and use a Function to parse its response.
7. Connect Order Desk in MCP Lab, inspect its five tools, and test `lookup_order`. The approval-gated ticket write is optional.
8. Register the external MCP in Developer Portal and enable it in Control Hub.
9. Create an autonomous order-support agent, replace any starter content, attach the approved MCP `lookup_order` action, preview it, and publish it.
10. Replace the starter caller path with the published AI agent. Call once for an order update and again for human escalation.
11. **Optional:** Review the Webex Contact Center Flow and Operations MCP services with your facilitator if the sandbox has access.

## Before you start

Bring the event-provided **MCP Lab token** and use a supported browser. After redemption, **Test tenant details** shows your sandbox URL, sign-in details, Order Desk endpoints, temporary bearer token, assignment expiration, and sample order number.

Keep Control Hub, Flow Designer, Developer Portal, AI Agent Studio, and MCP Lab in separate tabs.

!!! warning "Protect your lab credentials"
    Keep credentials inside the assigned sandbox or the lab's **Test tenant details** panel. Never paste a bearer token, client secret, or sandbox password into a slide, chat, ticket, screenshot, or source file.

[Start Checkpoint 1](lab1_getting_started.md){ .md-button .md-button--primary }
