# Troubleshooting and completion

## If a step fails

| Symptom | Check |
| --- | --- |
| MCP Lab rejects the token | Re-enter the event-provided **MCP Lab token**. Do not use a sandbox or Webex password. |
| **Order Desk** is missing | Open **Test tenant details** and confirm that your assignment includes Order Desk. If **Connect MCP** does not load its tools, ask the facilitator to check the assignment. |
| An Order Desk read asks for approval | Confirm the tool name and ask the facilitator to check the lab approval policy. The ticket-write exercise is separate and optional. |
| The Agentic App is missing in Control Hub | In Developer Portal, check that you used the assigned sandbox account and selected **Request admin approval** if offered. Refresh **Apps → Agentic Apps** in the assigned organization. |
| `lookup_order` is missing in AI Agent Studio | In **Apps → Agentic Apps**, open `LAB21170 Order Desk MCP`. Check **General → Allowed for all users**, a saved **Authentication → Custom Headers** `Authorization` value, and **Tools → Look up mock order** enabled. Keep the four ticket tools off. Refresh Studio. [Webex's provisioning guide](https://developer.webex.com/mcp/docs/provisioning-on-control-hub) says tool lists can be cached for up to one hour. |
| Preview says the order is unavailable | Confirm that the attached action is the registered MCP `lookup_order`. In **Sessions**, inspect its input and result. Check the Control Hub header and tool permission; enter `ORD-10482` again after fixing them. |
| The agent only repeats its order-support scope when you ask for general support | In AI Agent Studio, check that the published Instructions tell the agent to offer a human for requests outside order status and delivery, and to use **Agent handover** when the caller accepts. Save, preview the exchange, check **Sessions** for **Agent handover**, and republish the agent. |
| The agent mentions packages | Replace any Track Package template Profile and Instructions text, and remove `trackPackage`. |
| The practice call does not reach `Queue-1` | Check that the entry point selects your published practice flow on **Latest**, **Queue Contact** selects `Queue-1`, and the welcome activity connects to the queue. A saved draft does not handle calls. |
| Wait treatment does not play or repeat | Put **Queue Treatment Subflow** after **Queue Contact** in the main flow. Check its input types and return links for digit `2`, no input, and unmatched entries. |
| Callback is unavailable | **Callback** stays in the main flow. Ask the facilitator to confirm Courtesy Callback entitlement, queue setup, and caller-number policy before testing digit `1`. |
| An earlier menu choice goes nowhere | In the menu-based `ServiceDesk` practice flow, digit `1` goes to `GetOrder` or `OrderLookup`; digit `2` goes directly to `Queue-1`. If **Debug** shows `SupportMenu` Error, check **No-Input Timeout**, **Unmatched Entry**, and **Undefined Error** links, then validate, publish, and call again. The final AI path has no numbered menu. |
| The number reaches the wrong flow | In Control Hub, check that the inbound entry point is **Active**, has the assigned Calling Location and PSTN number, and selects the intended **Routing flow** and **Latest** version label. |
| REST returns unauthorized | In **HTTP Request**, check that the header key is `Authorization` and its value begins with `Bearer ` plus the current temporary token. Keep that value out of screenshots and source files. |
| The REST order status is not spoken | Check the custom **String** `orderStatus` variable, **JSON** response parsing, and `$.order.status` path. Confirm the spoken message uses that variable. |
| The final flow cannot run the agent | Check that the agent is **Published**; **Contact Center AI Config** is **Webex AI Agent (Autonomous)**; **Virtual agent** selects `LAB-21170 Order Support`; and **Handled**, **Escalated**, and **Errored** are connected. Publish the final `ServiceDesk` version and confirm the entry point uses **Latest**. |
| The agent offers a human, but the call does not enter the queue | Accept the offer during a phone call. In **Debug**, follow **Escalated → EscalationMessage → HumanAgentQueue**. Check that **HumanAgentQueue** selects **Voice → Static queue → Queue-1** and its normal route enters wait treatment. A Studio **Agent handover** badge confirms the Preview action, not voice queue delivery. |

## Completion checklist

The guide's captured `ServiceDesk` version 5 is published as **Latest**. Complete the phone and **Debug** checks below in your own sandbox before marking the final path done.

### Practice flow and REST

- ☐ Open your assigned Control Hub organization, entry point, and `Queue-1`.
- ☐ Publish a **Simple Inbound Call to Queue** practice flow, route the entry point to it, and verify calls in **Debug** and **Analyze**.
- ☐ Publish **Queue Treatment Subflow** and connect it after **Queue Contact**. Call and press digit `2` at `CallbackOrWait` to repeat wait treatment.
- ☐ If Courtesy Callback is enabled, call again, press digit `1` at `CallbackOrWait`, and confirm the callback and original-call outcome in **Debug**.
- ☐ Publish the menu-based `ServiceDesk` practice flow. Confirm digit `1` reaches the order branch and digit `2` reaches `Queue-1`.
- ☐ Configure the Order Desk **HTTP Request** with the full URL, `Authorization` bearer header, **Application/JSON** request content type, and **JSON** response parsing. Map `$.order.status` to the custom **String** `orderStatus` variable.
- ☐ Call the direct REST branch and compare the spoken result with Order Desk and **Debug**.
- ☐ Publish the parser Function and `OrderLookup` subflow, map its output into `ServiceDesk`, republish the parent, and verify the order and general-support branches by phone and **Debug**.

### MCP and AI agent

- ☐ Connect Order Desk in MCP Lab, inspect its five tools, and confirm that `lookup_order` returns `ORD-10482` data without write approval.
- ☐ If you try the optional ticket write, approve it once and read the ticket list before retrying any uncertain result.
- ☐ Register `LAB21170 Order Desk MCP` as a **Streamable HTTP** Agentic App with **Custom Headers** authentication. Allow it in Control Hub and enable only **Look up mock order** (`lookup_order`). Leave `list_tickets`, `get_ticket`, `create_ticket`, and `update_ticket` off.
- ☐ Create `LAB-21170 Order Support` as an autonomous agent. Replace the Profile and Instructions text, remove any package-template action, attach `lookup_order`, and confirm the order result in Preview. Ask for general support, accept the human offer, confirm **Agent handover** in **Sessions**, and publish the agent.

### Final phone path

- ☐ Connect `NewContact` directly to **Virtual Agent V2** using **Webex AI Agent (Autonomous)**. Wire **Handled**, **Escalated**, and **Errored**, including `Queue-1` wait treatment and spoken error fallbacks.
- ☐ Validate and publish the final `ServiceDesk` flow. Confirm the published version is **Latest** (version 5 in this guide) and the active entry point selects `ServiceDesk` **Latest**.
- ☐ Make an order-status call. Call again, say `I need general support`, and accept the agent's offer to connect you with a person. In **Debug**, confirm the first call follows **AIAgent → Handled** and the second enters `Queue-1` and wait treatment. In AI Agent Studio **Sessions**, inspect the `lookup_order` result. If a test agent is available, confirm the agent can answer.
- ☐ Keep bearer tokens, passwords, caller numbers, and customer details out of shared screenshots, GIFs, notes, and source files.

[Finish the lab](conclusion.md){ .md-button .md-button--primary }
