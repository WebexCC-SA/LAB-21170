# Troubleshooting and completion

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Invalid lab token | Re-enter the event-provided token exactly; do not use a sandbox password or Webex login password. |
| No Order Desk connection appears | Open **Test tenant details** and confirm that the assigned exercise includes an Order Desk endpoint. |
| Discovery fails | Confirm that the endpoint is copied without extra spaces and the temporary bearer token has not expired. |
| A read asks for approval | Confirm that the tool name is one of the expected read tools and report the result to the facilitator. |
| A write runs automatically | Stop the test and report it; `create_ticket` and `update_ticket` must be approval-gated. |
| The agent cannot find the order | Confirm that the tool is enabled, use `ORD-10482`, and verify that the MCP action is attached to the correct draft agent. |
| A menu selection goes nowhere | Confirm that digit `1` is connected to the HTTP Request and digit `2` is connected to `GeneralSupportMessage`. |
| The phone number does not reach the starter flow | Confirm that the inbound channel is **Active**, uses the `ServiceDesk` routing flow, has a phone number assigned, and uses the latest published version. |
| The API call returns unauthorized | Confirm that the header key is `Authorization` and the value starts with `Bearer ` followed by the current temporary token. |
| The order status is not spoken | Confirm that the response parse content type is **JSON** and `orderStatus` uses the path `$.order.status`. |
| Flow Designer cannot run the agent | Confirm that the agent is saved, the Virtual Agent V2 activity points to that agent, and the flow validates before publication. |

## Completion checklist

- [ ] Control Hub organization and Contact Center area identified.
- [ ] `ServiceDesk` Flow Designer draft created from scratch.
- [ ] `NewContact` is the voice start event.
- [ ] Starter IVR contains `WelcomeMessage` and `SupportMenu`.
- [ ] Starter IVR published and assigned to an active inbound telephony channel.
- [ ] Live call reaches the welcome prompt, menu, and digit `2` general-support message.
- [ ] Menu digit `1` reaches the Order Desk HTTP test and digit `2` reaches `GeneralSupportMessage`.
- [ ] HTTP request uses the full Order Desk URL, bearer header, Application/JSON request content type, and JSON response parsing.
- [ ] Parsed variable `orderStatus` reads `$.order.status` and is spoken to the caller.
- [ ] Direct REST lookup returns order, delivery, and customer data for `ORD-10482`.
- [ ] Agent configured and saved in draft.
- [ ] Developer Portal MCP registration or facilitator-provided registration details confirmed.
- [ ] External Order Desk MCP discovered in MCP Lab.
- [ ] `lookup_order` returns data for `ORD-10482`.
- [ ] Automatic read behavior observed.
- [ ] Approval-required behavior observed for ticket creation.
- [ ] Same external MCP connected to the AI agent.
- [ ] Virtual Agent V2 connected directly after `NewContact` in the final caller path.
- [ ] End-to-end phone test completed.
- [ ] No secrets included in screenshots, notes, or shared artifacts.

[Finish the lab](conclusion.md){ .md-button .md-button--primary }
