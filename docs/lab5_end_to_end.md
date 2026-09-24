# Checkpoint 9: Attach the agent and test end to end

??? example "Target wiring: replace the starter caller path"
    1. Disconnect `NewContact` from `WelcomeMessage`; leave the starter activities on the canvas as a reference.
    2. Add **Virtual Agent V2**, name it `AIAgent`, select **Webex AI Agent (Autonomous)**, and select the published order-support agent.
    3. Connect `NewContact` directly to `AIAgent`. Send **Handled** to a clean end, **Escalated** to the assigned human queue and wait treatment, and **Errored** to an honest fallback.
    4. Validate, publish, and call the assigned number.

    **Expected end state:** The caller reaches the AI agent directly and never hears the starter menu; a request for a person can enter `Queue-1`.

!!! warning "Complete the MCP agent prerequisite first"
    Start this checkpoint only after `lookup_order` appears as an MCP action in AI Agent Studio, its Preview returns Order Desk data, and the agent is published. A source-flow action with no MCP provider is a different fulfillment path and does not satisfy this lab's final AI-to-Order-Desk objective. If **Add actions** says **No actions available**, finish Checkpoint 6 provisioning before changing the live caller route.

## Replace the starter caller path

1. Return to the `ServiceDesk` draft in Flow Designer.
2. Disconnect `NewContact` from `WelcomeMessage`. You may leave nonsecret starter IVR activities on the canvas as an unconnected reference. Remove the direct **HTTP Request** activity or clear its temporary Authorization header; a disconnected node can still retain its configuration.
3. Find **Virtual Agent V2** under **Contact handling** and drag it onto the canvas.
4. Set **Activity label** to `AIAgent`.
5. Connect `NewContact` directly to `AIAgent`.
6. In the activity settings, set **Contact Center AI Config** to **Webex AI Agent (Autonomous)**.
7. For **Virtual agent**, select the published `LAB-21170 Order Support` agent.
8. Reuse the existing `DisconnectContact` activity from the starter IVR, or add a **Disconnect Contact** activity with that label if your flow does not have one.
9. Connect the `AIAgent` **Handled** outcome to `DisconnectContact`.
10. Add a **Play Message** activity and label it `EscalationMessage`. Enable text to speech, select **Cisco Cloud Text-to-Speech**, and enter: `I'll connect you with a human agent.`
11. Reuse the **Queue Contact** and **Play Music** activities from Checkpoint 3 if they are already on the canvas; otherwise add them. Disconnect the old practice link, label the queue activity `HumanAgentQueue`, and select the assigned `Queue-1` queue. Connect `AIAgent` **Escalated → EscalationMessage → HumanAgentQueue → Play Music** so the caller hears wait treatment while queued.
12. Add a **Play Message** activity labeled `QueueErrorMessage` with: `I can't connect you to a person right now. Please try again later.` Connect the Queue Contact **Undefined Error** output to this message, then to `DisconnectContact`. This is the safe path if the queue operation fails; a caller simply waiting for an agent stays in queue treatment. If `Queue-1` is missing from the selector, route **Escalated** directly through `QueueErrorMessage → DisconnectContact`, remove any unusable queue and music activities before validation, and mark human handoff unverified until the facilitator restores the queue.
13. Add another **Play Message** activity and label it `AgentErrorMessage`. Enable text to speech, select **Cisco Cloud Text-to-Speech**, and enter: `Order support is temporarily unavailable. Please try again later.`
14. Connect the `AIAgent` **Errored** outcome to `AgentErrorMessage`, then connect `AgentErrorMessage` to `DisconnectContact`.
15. Wait for Autosave, select **Validation**, and resolve any errors. If validation rejects the disconnected practice activities, delete those disconnected activities; their earlier published versions still preserve the learning steps.

<figure markdown>
  ![Reference topology for the final caller path with AI-agent handled, human-queue escalation, and error outcomes](assets/lab-guide/02-final-agent-flow.png)
  <figcaption>Target topology: NewContact reaches the AI agent directly. Handled ends the call, Escalated enters Queue-1 and wait treatment, and Errored ends after a fallback message.</figcaption>
</figure>

## Publish and test the final caller path

1. Select **Publish** after validation. **Latest** is applied automatically; add the offered **Test** label and a comment such as `AI agent with human queue` if useful.
2. In Control Hub, open the assigned inbound **Entry Point** from Checkpoint 2 and confirm that its routing flow is `ServiceDesk` and its version label points to this published version. If it is pinned to an older version, update the routing assignment before calling.
3. Call the same inbound phone number used in Checkpoints 2 and 3.
4. Say: `I need an update on order ORD-10482.`
5. If the agent asks for the order number, provide `ORD-10482`.
6. Confirm that the agent retrieves the order data through the external action and explains the status and delivery information.
7. Make a second call and say: `Please connect me to a human agent.` Confirm that the **Escalated** path plays `EscalationMessage` and enters `Queue-1`. If a test agent is available, answer the call in Agent Desktop. If no agent is available, confirm that the caller hears wait treatment rather than a false claim of transfer completion.
8. In **Debug**, inspect the second Interaction ID and confirm that it followed `AIAgent → EscalationMessage → HumanAgentQueue`. Check the Queue Contact error path separately when the facilitator can safely supply a controlled failure.

**Target caller path:**

```text
Caller → Flow Designer entry → AI agent → external Order Desk service via MCP → response
                                              ├─ Handled → end
                                              └─ Escalated → Queue-1 → wait treatment → human agent
```

!!! success "Confirm before continuing"
    - The connected caller path is `NewContact → AIAgent`; the starter menu and REST branch are disconnected.
    - A live caller does not hear the welcome message or menu.
    - The agent uses `lookup_order` and speaks the returned order and delivery details.
    - An explicit request for a person reaches `Queue-1` and wait treatment; an available test agent can answer it.
    - A Queue Contact error reaches `QueueErrorMessage` and ends safely.
    - `AgentErrorMessage` provides a clear fallback if the AI agent errors.

!!! warning "Facilitator validation before delivery"
    The human-escalation call and queue-error fallback are target outcomes until they have been tested in the assigned sandbox. Confirm the queue, test-agent availability, AI-agent escalation behavior, and Debug trace before presenting this checkpoint as a completed live result.

Publish only the flow versions required by this guide. A human still decides whether to change organization-wide defaults or reuse the lab configuration outside the assigned sandbox.

## Bonus: Explore the Webex Contact Center MCP services

The Order Desk MCP you used in this lab is an **external business-system tool for the voice AI agent**. The following Cisco services serve a different purpose: they let an authorized MCP client inspect Contact Center flows or operations. They have separate connection details and tool sets. Complete either bonus only when the facilitator confirms beta access, the approved MCP client, and the regional server URL shown for your organization in the Webex Developer Portal. Do not guess a server URL or use the Order Desk token to connect to a Webex service.

### A. Contact Center MCP Server: explore Flow tools

The [Contact Center MCP Server](https://developer.webex.com/mcp/docs/contact-center-mcp-server) exposes Flow Designer tools backed by the FlowV2 authoring contract. An administrator enables **Contact Center MCP** under **Control Hub → Apps → Agentic Apps**, allows the app, and enables the specific tools for this exercise. The [beta setup guide](https://developer.webex.com/create/docs/contact-center-mcp-server-beta) describes supported clients and authentication.

1. In the Webex Developer Portal, open the Contact Center MCP Server page while signed in. Copy the **regional server URL** shown for your organization into the facilitator-approved MCP client and connect using the approved Webex authentication method.
2. Confirm the client shows the server as connected and only the approved tools are available. Start with `wxcc-list-flows` to find your lab flow and `wxcc-get-flow` to read its draft or published version. Compare the returned node and edge names with the canvas.
3. Use `wxcc-view-config` to inspect the assigned entry point or queue. Use `wxcc-get-activity-definitions`, `wxcc-describe-activity`, and `wxcc-get-choices` to discover a valid activity and organization-specific choices before proposing any draft change.
4. If the facilitator has enabled write tools, make a **separate unpublished test draft**, review the exact proposed change, then use `wxcc-validate-flow`. Do not bind the test draft to the lab phone number or publish it. Confirm that the original published caller path still works.

!!! success "Flow MCP bonus complete"
    The client can read the authorized lab flow and its related configuration, and you can explain how FlowV2 nodes and edges match the visual canvas. Any optional test change remains an unpublished, validated draft.

### B. Contact Center Operation MCP Server: explore read-only tools

The [Contact Center Operation MCP Server beta](https://developer.webex.com/create/docs/contact-center-operation-mcp-server-beta) is a **separate read-only service** for investigating configuration and operational evidence. It does not create, update, publish, or delete a flow. Its beta access, enabled tools, and regional URL must be confirmed separately.

1. Connect the facilitator-approved client to the **Operation MCP Server** URL shown in the signed-in Webex Developer Portal. Confirm that it appears as connected and its approved tools are visible.
2. Run `wxcc-operations-describe-org` and `wxcc-operations-describe-metrics` to see what the authorized organization and available reporting fields contain.
3. Use `wxcc-operations-list-flows` to find your lab flow. If enabled, use `wxcc-operations-explain-queue-routing` to inspect the assigned queue's configuration. Distinguish configured queue coverage from whether an agent was actually available for your test call.
4. If the facilitator provides an approved test contact ID and the tool is enabled, use `wxcc-operations-get-contact-timeline` to inspect its arrival, IVR, queue, agent, and end events. A missing or delayed artifact is not evidence that the call never happened.

!!! success "Operations MCP bonus complete"
    The client returns only authorized read-only data, and you can relate a flow, queue, or test contact to the journey you built without changing Contact Center configuration.

!!! warning "Protect the lab and customer data"
    Use only the approved tenant, client, tools, and test contacts. Do not include tokens, transcripts, phone numbers, or customer details in screenshots. If access or the tool catalog differs from the facilitator's setup, stop this bonus and continue with the published flow.

[Continue to troubleshooting and completion](troubleshooting.md){ .md-button .md-button--primary }
