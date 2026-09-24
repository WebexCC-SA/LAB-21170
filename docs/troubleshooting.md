# Troubleshooting and completion

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Invalid lab token | Re-enter the event-provided token exactly; do not use a sandbox password or Webex login password. |
| No Order Desk connection appears | Open **Test tenant details** and confirm that the assigned exercise includes an Order Desk endpoint. |
| MCP Lab discovery fails | Confirm that the endpoint is copied without extra spaces and the temporary bearer token has not expired. |
| A read asks for approval | Confirm that the tool name is one of the expected read tools and report the result to the facilitator. |
| A write runs automatically | Stop the test and report it; `create_ticket` and `update_ticket` must be approval-gated. |
| The registered app does not appear in Control Hub | Confirm that you registered it with the assigned sandbox account, selected **Request admin approval** if available, and then refresh **Apps → Agentic Apps**. |
| `lookup_order` does not appear in Agent Studio | Confirm that the app is **Allowed** in Control Hub, `lookup_order` is enabled under **Tools**, and the registration does not use OAuth 2.0 Authorization Code. |
| Preview is unavailable | This is expected before Checkpoint 8. Add the registered `lookup_order` action, wait for it to persist, and try again. |
| The agent cannot find the order | Confirm that `lookup_order` is attached, use `ORD-10482`, and verify that the temporary user token has not expired. |
| The agent still talks about packages | Confirm that the Profile and Instructions copy was replaced and the template `trackPackage` action was removed. |
| A menu selection goes nowhere | Confirm that digit `1` is connected to the HTTP Request and digit `2` is connected to `GeneralSupportMessage`. |
| The phone number does not reach the starter flow | Confirm that the inbound channel is **Active**, uses the `ServiceDesk` routing flow, has the assigned Webex Calling Location and PSTN number, and uses the **Latest** version label. |
| The API call returns unauthorized | Confirm that the header key is `Authorization` and the value starts with `Bearer ` followed by the current temporary token. |
| The order status is not spoken | Confirm that `orderStatus` exists as a custom **String** flow variable, the response parse content type is **JSON**, and its JSON path is `$.order.status`. |
| Flow Designer cannot run the agent | Confirm that the agent is **Published**, **Contact Center AI Config** is **Webex AI Agent (Autonomous)**, **Virtual agent** is `LAB-21170 Order Support`, and all three activity outcomes are connected. |

## Completion checklist

- [ ] Control Hub organization and Contact Center area identified.
- [ ] `ServiceDesk` Flow Designer draft created from scratch.
- [ ] `NewContact` is the voice start event.
- [ ] Starter IVR contains `WelcomeMessage` and `SupportMenu`.
- [ ] Starter IVR published and assigned to an active inbound telephony channel using the assigned Webex Calling Location, PSTN number, and **Latest** version label.
- [ ] Live call reaches the welcome prompt, menu, and digit `2` general-support message.
- [ ] Menu digit `1` reaches the Order Desk HTTP test and digit `2` reaches `GeneralSupportMessage`.
- [ ] HTTP request uses the full Order Desk URL, bearer header, Application/JSON request content type, and JSON response parsing.
- [ ] Custom **String** variable `orderStatus` exists, reads `$.order.status`, and is spoken to the caller.
- [ ] Direct REST lookup returns order, delivery, and customer data for `ORD-10482`.
- [ ] External Order Desk MCP discovered in MCP Lab.
- [ ] `lookup_order` returns data for `ORD-10482`.
- [ ] Automatic read behavior observed.
- [ ] Approval-required behavior observed for ticket creation.
- [ ] `LAB-21170 Order Desk` registered as a Streamable HTTP MCP Agentic App with User Token authentication.
- [ ] Private Agentic App allowed in Control Hub and `lookup_order` enabled.
- [ ] `LAB-21170 Order Support` created from the Track Package autonomous template.
- [ ] Profile and Instructions copy replaced with the provided order-support text.
- [ ] Template `trackPackage` action removed.
- [ ] Registered `lookup_order` MCP action attached to the agent.
- [ ] Agent Preview successfully returns data for `ORD-10482`.
- [ ] Agent published before Flow Designer configuration.
- [ ] Virtual Agent V2 uses **Webex AI Agent (Autonomous)** and the published `LAB-21170 Order Support` agent.
- [ ] Virtual Agent V2 is connected directly after `NewContact`, with **Handled**, **Escalated**, and **Errored** paths connected.
- [ ] End-to-end phone test completed.
- [ ] No secrets included in screenshots, notes, or shared artifacts.

[Finish the lab](conclusion.md){ .md-button .md-button--primary }
