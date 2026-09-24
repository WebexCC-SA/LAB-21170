# Checkpoint 9: Attach the agent and test end to end

<!-- gif-capture: cp9-replace-caller-path -->

??? example "Show me: replace the starter caller path"
    1. Disconnect `NewContact` from `WelcomeMessage`; leave the starter activities on the canvas as a reference.
    2. Add **Virtual Agent V2**, name it `AIAgent`, select **Webex AI Agent (Autonomous)**, and select the published order-support agent.
    3. Connect `NewContact` directly to `AIAgent`, then connect **Handled**, **Escalated**, and **Errored** to the completion paths below.
    4. Validate, publish, and call the assigned number.

    **Expected end state:** The caller reaches the AI agent directly and never hears the starter menu.

## Replace the starter caller path

1. Return to the `ServiceDesk` draft in Flow Designer.
2. Disconnect `NewContact` from `WelcomeMessage`. Leave the starter IVR and **HTTP Request** activities on the canvas as an unconnected reference.
3. Find **Virtual Agent V2** under **Contact handling** and drag it onto the canvas.
4. Set **Activity label** to `AIAgent`.
5. Connect `NewContact` directly to `AIAgent`.
6. In the activity settings, set **Contact Center AI Config** to **Webex AI Agent (Autonomous)**.
7. For **Virtual agent**, select the published `LAB-21170 Order Support` agent.
8. Add a **Disconnect Contact** activity and label it `DisconnectContact`.
9. Connect the `AIAgent` **Handled** outcome to `DisconnectContact`.
10. Add a **Play Message** activity and label it `EscalationMessage`. Enable text to speech, select **Cisco Cloud Text-to-Speech**, and enter: `Live agent transfer is not configured in this exercise.`
11. Connect the `AIAgent` **Escalated** outcome to `EscalationMessage`, then connect `EscalationMessage` to `DisconnectContact`.
12. Add another **Play Message** activity and label it `AgentErrorMessage`. Enable text to speech, select **Cisco Cloud Text-to-Speech**, and enter: `Order support is temporarily unavailable. Please try again later.`
13. Connect the `AIAgent` **Errored** outcome to `AgentErrorMessage`, then connect `AgentErrorMessage` to `DisconnectContact`.
14. Wait for Autosave, select **Validation**, and resolve any errors. If validation rejects the disconnected practice activities, delete those disconnected activities; they are no longer part of the caller path.

<figure markdown>
  ![Reference topology for the final Flow Designer caller path](assets/lab-guide/02-final-agent-flow.png)
  <figcaption>Reference topology. The final caller path connects NewContact directly to the autonomous AI agent and handles all three outcomes.</figcaption>
</figure>

## Publish and test the final caller path

1. Publish a new flow version with a label such as `order-agent-v1`.
2. In Control Hub, open the inbound channel created in Checkpoint 2 and confirm that **Routing Flow** is `ServiceDesk` and **Version label** is **Latest**. If the channel is pinned to a fixed label, change it to **Latest** or select `order-agent-v1`.
3. Call the same inbound phone number used in Checkpoints 2 and 3.
4. Say: `I need an update on order ORD-10482.`
5. If the agent asks for the order number, provide `ORD-10482`.
6. Confirm that the agent retrieves the order data through the external action and explains the status and delivery information.
7. Make a second call and ask for a refund or another unsupported request. Confirm that you hear: “Live agent transfer is not configured in this exercise.”

**Completed path:**

```text
Caller → Flow Designer entry → AI agent → external Order Desk service via MCP → order response
```

!!! success "Confirm before continuing"
    - The connected caller path is `NewContact → AIAgent`; the starter menu and REST branch are disconnected.
    - A live caller does not hear the welcome message or menu.
    - The agent uses `lookup_order` and speaks the returned order and delivery details.
    - An unsupported request reaches `EscalationMessage` and then disconnects cleanly.
    - `AgentErrorMessage` provides a clear fallback if the AI agent errors.

Publish only the flow versions required by this guide. A human still decides whether to change organization-wide defaults or reuse the lab configuration outside the assigned sandbox.

## Optional admin stretch: Add another MCP

Run this section only if the facilitator enables it and provides the exact Webex Contact Center MCP endpoint and authorization method.

1. In MCP Lab, open **Add another MCP**.
2. Paste the approved MCP server address.
3. Choose the authentication method supplied by the facilitator.
4. Select **Discover tools**.
5. Review every discovered tool and its policy label.
6. Enable only the bounded flow-management tools required for the exercise.
7. Connect the MCP and return to the AI agent workspace.
8. Request one small, reversible flow change.
9. Stop at the approval gate and review the exact proposed change.
10. Approve only the bounded change you intend to test.
11. Read the updated flow back in Flow Designer and verify the result.

!!! danger
    Do not use delete, remove, destructive, or unrecognized tools. If the endpoint, authorization prompt, or tool contract is not the one provided by the facilitator, stop and ask for help.

[Continue to troubleshooting and completion](troubleshooting.md){ .md-button .md-button--primary }
