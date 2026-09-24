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
| `lookup_order` does not appear in Agent Studio | If **Select available** says **No actions available**, confirm that the Agentic App was submitted in Developer Portal, is **Allowed** in Control Hub, has its Custom Headers authentication configured, and has `lookup_order` enabled under **Tools**. Refresh Studio after provisioning. |
| Preview returns unavailable | Preview can open for a draft with no working MCP tool. Confirm that the attached action is the registered **MCP** `lookup_order`, then inspect its trace, input, Control Hub header, and tool permission. |
| The agent cannot find the order | Confirm that MCP `lookup_order` is attached and receives `ORD-10482`; check the temporary sandbox bearer configured in the app's Control Hub Custom Headers setting. |
| The agent still talks about packages | If you used the optional Track Package template, replace its Profile and Instructions copy and remove `trackPackage`. |
| The practice call never enters `Queue-1` | Confirm the published `SimpleQueue` version is selected by the entry point, the welcome message reaches **Queue Contact**, and the queue choice is `Queue-1`. A saved draft alone will not handle the call. |
| Queue treatment does not play or repeat | Confirm that the published **Queue Treatment Subflow** is selected in the main flow and the link reaches it after **Queue Contact**. Its four exposed inputs may use their published defaults; any mapped override needs a matching variable type. Check that digit `2`, no-input, and unmatched menu links return to the subflow rather than Queue Contact. |
| Callback cannot be added or does not register | **Callback** is a main-flow activity and depends on queue and enterprise Courtesy Callback setup. Keep it outside the subflow; ask the facilitator to verify entitlement and caller number policy before testing the callback branch. |
| A menu selection goes nowhere | For direct `ServiceDesk` v1, check digit `1` to `GetOrder`; for refactored v2, check digit `1` to `OrderLookup`. Digit `2` should reach `GeneralSupportMessage`. |
| The phone number does not reach the intended flow | Confirm that the inbound entry point is **Active**, has the assigned Calling Location and PSTN number, and routes to the published flow's **Latest** version. The practice call uses `SimpleQueue`; later `ServiceDesk` versions require reassignment. |
| The API call returns unauthorized | Confirm that the header key is `Authorization` and the value starts with `Bearer ` followed by the current temporary token. |
| The order status is not spoken | Confirm that `orderStatus` exists as a custom **String** flow variable, the response parse content type is **JSON**, and its JSON path is `$.order.status`. |
| Flow Designer cannot run the agent | Confirm that the agent is **Published**, **Contact Center AI Config** is **Webex AI Agent (Autonomous)**, **Virtual agent** is `LAB-21170 Order Support`, and all three activity outcomes are connected. |

## Completion checklist

- [ ] Control Hub organization and Contact Center area identified.
- [ ] Native `SimpleQueue` template published, assigned to the entry point, and verified by phone, Debug, and Analyze.
- [ ] Native **Comprehensive Call Flow** post-queue path inspected and the reusable **Queue Treatment Subflow** published.
- [ ] Practice flow invokes the published queue-treatment subflow after **Queue Contact**; menu digit `2` repeats wait treatment by phone.
- [ ] If Courtesy Callback is enabled, practice menu digit `1` registers a callback and the original call ends; Debug evidence is captured.
- [ ] `ServiceDesk` Flow Designer draft created from scratch.
- [ ] `NewContact` is the voice start event.
- [ ] Starter IVR contains `WelcomeMessage` and `SupportMenu`.
- [ ] Starter IVR published and assigned to an active inbound telephony channel using the assigned Webex Calling Location, PSTN number, and **Latest** version label.
- [ ] Live call reaches the welcome prompt, menu, and digit `2` general-support message.
- [ ] Menu digit `1` reaches the Order Desk HTTP test and digit `2` reaches `GeneralSupportMessage`.
- [ ] HTTP request uses the full Order Desk URL, bearer header, Application/JSON request content type, and JSON response parsing.
- [ ] Custom **String** variable `orderStatus` exists, reads `$.order.status`, and is spoken to the caller.
- [ ] Direct REST branch is verified by phone and Debug for `ORD-10482`; check the parsed status against the Order Desk response.
- [ ] The parser Function and guarded `OrderLookup` subflow are published, mapped into `ServiceDesk`, and verified by phone and Debug.
- [ ] External Order Desk MCP discovered in MCP Lab.
- [ ] `lookup_order` returns data for `ORD-10482`.
- [ ] Automatic read behavior observed.
- [ ] Approval-required behavior observed for ticket creation.
- [ ] `LAB21170 Order Desk MCP` registered as a Streamable HTTP MCP Agentic App with Custom Headers authentication.
- [ ] Private Agentic App allowed in Control Hub and `lookup_order` enabled.
- [ ] `LAB-21170 Order Support` created as an autonomous Start Fresh agent, or the optional Track Package template fully cleaned up.
- [ ] Profile and Instructions copy replaced with the provided order-support text.
- [ ] No package-template action remains.
- [ ] Registered `lookup_order` MCP action attached to the agent.
- [ ] Agent Preview successfully returns data for `ORD-10482`.
- [ ] Agent published before Flow Designer configuration.
- [ ] Virtual Agent V2 uses **Webex AI Agent (Autonomous)** and the published `LAB-21170 Order Support` agent.
- [ ] Virtual Agent V2 is connected directly after `NewContact`, with **Handled**, **Escalated**, and **Errored** paths connected.
- [ ] End-to-end phone test completed.
- [ ] No secrets included in screenshots, notes, or shared artifacts.

[Finish the lab](conclusion.md){ .md-button .md-button--primary }
