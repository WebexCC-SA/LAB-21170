# Troubleshooting and completion

## If a step fails

| Symptom | Check |
| --- | --- |
| MCP Lab rejects the token | Re-enter the event-provided **MCP Lab token**. Do not use a sandbox or Webex password. |
| **Order Desk** is missing | Open **Test tenant** and confirm that your assignment includes Order Desk. If **Connect MCP** does not load its tools, ask the facilitator to check the assignment. |
| `lookup_order` asks for approval | Confirm that the tool activity is for `lookup_order`, which the catalog labels **Runs automatically**, then ask the facilitator to check the lab tool policy. |
| The Agentic App is missing in Control Hub | In Developer Portal, check that you used the assigned sandbox account and selected **Request admin approval** if offered. Refresh **Apps → Agentic Apps** in the assigned organization. |
| `lookup_order` is missing in AI Agent Studio | In **Apps → Agentic Apps**, open `LAB21170 Order Desk MCP`. Check **General → Allowed for all users**, a saved **Authentication → Custom Headers** `Authorization` value, and **Tools → Look up mock order** enabled. Other tools may remain enabled; this lab exercises only `lookup_order`. Refresh Studio. [Webex's provisioning guide](https://developer.webex.com/mcp/docs/provisioning-on-control-hub) says tool lists can be cached for up to one hour. |
| `lookup_order` worked earlier, but **Sessions** now shows **MCP execution failure** or Control Hub **Tools** shows **No tools available** | Sign in to MCP Lab again with your event token. Open **Test tenant** and reveal the current temporary Order Desk bearer. In Control Hub, open **Apps → Agentic Apps → LAB21170 Order Desk MCP → Authentication → Custom headers**. Replace the existing `Authorization` value with `Bearer ` followed by the current bearer, then save. If **Pending reauthorization** appears, select **Reauthorize server** and wait for **Tools** to load. Confirm **Look up mock order** (`lookup_order`) is enabled. Retry `ORD-10482` in Studio Preview. Hide the bearer before taking a screenshot. |
| Preview says the order is unavailable | Confirm that the attached action is the registered MCP `lookup_order`. In **Sessions**, inspect its input and result. Check the Control Hub header and tool permission; enter `ORD-10482` again after fixing them. |
| The agent only repeats its order-support scope when you ask for general support | In AI Agent Studio, check that the published Instructions tell the agent to offer a human for requests outside order status and delivery, and to use **Agent handover** when the caller accepts. Save, preview the exchange, check **Sessions** for **Agent handover**, and republish the agent. |
| The agent mentions packages | Replace any Track Package template Profile and Instructions text, and remove `trackPackage`. |
| The starter call does not reach `Queue-1` | Check that the entry point selects your published imported `ServiceDesk` on **Latest** and that its **Queue** activity selects `Queue-1`. A saved draft does not handle calls. |
| Wait treatment does not play or repeat | In the imported starter, follow `Queue → Music → PlayMessage_c24 → Music`. Confirm the normal Queue output reaches Music and the message loops back to it. An agent may answer before the loop repeats. |
| A menu choice goes nowhere | In the imported `ServiceDesk`, digit `1` goes to `GetOrder`; digit `2` goes directly to `Queue-1`. Check `SupportMenu`'s **No-Input Timeout**, **Unmatched Entry**, and **Undefined Error** links to `MenuFallbackMessage`, then validate and republish. The final AI path has no numbered menu. |
| The number reaches the wrong flow | In Control Hub, check that the inbound entry point is **Active**, has the assigned Calling Location and PSTN number, and selects the intended **Routing flow** and **Latest** version label. |
| REST returns `401` | In MCP Lab **Test tenant**, copy the current temporary Order Desk bearer. In `GetOrder`, set the `Authorization` header to `Bearer ` followed by that bearer. Save, validate, publish, and call again; confirm `orderStatus` is populated in **Debug** and spoken on the call. Keep the bearer out of screenshots and source files. |
| The caller hears “unavailable” or no status | In **Debug**, select `GetOrder` and check **Modified Variables** for `orderStatus`. The starter defaults it to `unavailable`. Refresh the temporary bearer as above, then validate, publish, and call again. If it is still not populated, check **Parse settings → JSON** maps `$.order.status` to the **String** `orderStatus` and the prompt uses <code>&#123;&#123;orderStatus&#125;&#125;</code>. Debug may mask the HTTP response; **Success** on the activity does not prove the lookup returned an order. |
| The final flow cannot run the agent | Check that the agent is **Published**; **Contact Center AI Config** is **Webex AI Agent (Autonomous)**; **Virtual agent** selects `LAB-21170 Order Support`; and **Handled**, **Escalated**, and **Errored** are connected. Publish the final `ServiceDesk` version and confirm the entry point uses **Latest**. |
| The agent offers a human, but the call does not enter the queue | Accept the offer during a phone call. In **Debug**, follow **Escalated → EscalationMessage → HumanAgentQueue**. Check that **HumanAgentQueue** selects **Voice → Static queue → Queue-1** and its normal route enters wait treatment. A Studio **Agent handover** badge confirms the Preview action, not voice queue delivery. |

## Completion checklist

Before finishing, call both final paths and check them in **Debug**. The screenshots show `ServiceDesk` version 5 as **Latest**; your version number may differ.

### Imported flow and REST

- ☐ Open your assigned Control Hub organization, entry point, and `Queue-1`.
- ☐ Import the [credential-free `ServiceDesk` starter](assets/lab-guide/ServiceDesk-starter.json), inspect both menu choices, and confirm its Queue activity is bound to `Queue-1`.
- ☐ Replace `GetOrder`'s placeholder with your **Order Desk** bearer (not the MCP Lab sign-in token). Confirm the supplied URL, `GET`, **Application/JSON**, **JSON** parsing, and `$.order.status → orderStatus` mapping.
- ☐ Validate with **0 errors**, publish, and route the assigned entry point to `ServiceDesk` **Latest**.
- ☐ Call the direct REST branch and compare the spoken result with Order Desk and **Debug**.

### MCP and AI agent

- ☐ Connect Order Desk in MCP Lab with its default tools enabled. Exercise only `lookup_order` and confirm it returns `ORD-10482` data without approval.
- ☐ Register `LAB21170 Order Desk MCP` as a **Streamable HTTP** Agentic App with **Custom Headers** authentication. Allow it in Control Hub and confirm **Look up mock order** (`lookup_order`) is enabled. Other tools may remain enabled; do not exercise them in this lab.
- ☐ Create `LAB-21170 Order Support` as an autonomous agent. Replace the Profile and Instructions text, remove any package-template action, attach `lookup_order`, and confirm the order result in Preview. Ask for general support, accept the human offer, confirm **Agent handover** in **Sessions**, and publish the agent.

### Final phone path

- ☐ Connect the imported `NewPhoneContact` start activity directly to **Virtual Agent V2** using **Webex AI Agent (Autonomous)**. Wire **Handled**, **Escalated**, and **Errored**, including `Queue-1` wait treatment and spoken error fallbacks.
- ☐ Validate and publish the final `ServiceDesk` flow. Confirm the published version is **Latest** (version 5 in this guide) and the active entry point selects `ServiceDesk` **Latest**.
- ☐ Make an order-status call. Call again, say `I need general support`, and accept the agent's offer to connect you with a person. In **Debug**, confirm the first call reached `AIAgent` and ended after the answer or followed **Handled → DisconnectContact**; confirm the second entered `Queue-1` and wait treatment. In AI Agent Studio **Sessions**, inspect the `lookup_order` result. If a test agent is available, confirm the agent can answer.
- ☐ Keep bearer tokens, passwords, caller numbers, and customer details out of shared screenshots, GIFs, notes, and source files.

[Finish the lab](conclusion.md){ .md-button .md-button--primary }
