# Overview

## What you will build

You operate a customer service contact center for an online retailer. A customer calls for an update on order `ORD-10482`. Your job is to build the contact-center experience that handles that request safely and returns current order and delivery information.

You will build two versions of the caller path:

```text
Practice path: Caller → welcome message → menu → Order Desk REST test
Final path:    Caller → AI agent → external Order Desk system → response
```

The starter IVR teaches the core Flow Designer activities and gives you a direct REST response to compare with the finished experience. In the final version, you bypass the menu and connect the caller directly to the AI agent. The completed solution does not use a press-one/press-two menu.

<figure markdown>
  ![The lab begins with a starter IVR and REST lookup, then replaces that caller path with an AI agent and MCP lookup](assets/lab-guide/00-solution-evolution.png)
  <figcaption>The starter IVR is a temporary learning and data-validation path. The completed call goes directly to the AI agent, which uses the external MCP tool.</figcaption>
</figure>

The two stages use the same simulated Order Desk data. The first exposes the mechanics; the second gives the caller a natural conversation without requiring the agent to construct or parse a REST request.

## Your role

You are the Webex Contact Center administrator and automation developer. You will:

- administer the assigned sandbox in **Control Hub**;
- build and publish the call flow in **Flow Designer**;
- prepare the order-support agent in **AI Agent Studio**;
- confirm the external MCP registration in **Developer Portal**;
- inspect and test the simulated external service in **MCP Lab**; and
- call the assigned phone number to validate each published version.

During the final test, you speak as the caller. The AI agent plays the order-support assistant.

## Product journey

| Layer | Product | What it contributes |
| --- | --- | --- |
| Organization | **Control Hub** | Administer the organization and open Contact Center configuration. |
| Runtime | **Flow Designer** | Build the starter IVR, test the REST branch, and connect the agent's outcomes. |
| Conversation | **AI Agent Studio** | Set the agent's instructions, response behavior, and approved actions. |
| Developer access | **Developer Portal** | Register the external MCP data source before the agent uses it. |

MCP Lab and Order Desk support the exercise, but they are not Webex products. MCP Lab provides the temporary sandbox assignment and the synthetic Order Desk REST and MCP endpoints.

## Lab sequence

You will build and validate one layer at a time:

1. Redeem the sandbox assignment.
2. Build and call the starter IVR.
3. Prove the Order Desk REST response in Flow Designer.
4. Connect Order Desk and inspect its MCP tool contract.
5. Test the order lookup in MCP Lab.
6. Register the external MCP in Developer Portal and enable it in Control Hub.
7. Customize the **Track Package - Autonomous** template for order support.
8. Add `lookup_order`, preview the agent, and publish it.
9. Replace the starter caller path with the published AI agent and call the final flow.

This order lets you see the raw API response before the agent uses the same business data through a structured MCP tool.

## Before you start

Bring the event-provided **MCP Lab token** and use a supported browser. MCP Lab supplies the sandbox URL, sign-in details, Order Desk endpoints, temporary bearer token, assignment expiration, and sample order number after you redeem the token.

Keep separate browser tabs open for Control Hub, Flow Designer, Developer Portal, AI Agent Studio, and MCP Lab.

!!! warning "Protect your lab credentials"
    Keep credentials inside the assigned sandbox or the lab's **Test tenant details** panel. Never paste a bearer token, client secret, or sandbox password into a slide, chat, ticket, screenshot, or source file.

## Downloadable guide

- [Word walkthrough](assets/downloads/LAB-21170-flow-lab-walkthrough.docx)
- [PDF walkthrough](assets/downloads/LAB-21170-flow-lab-walkthrough.pdf)

[Start Checkpoint 1](lab1_getting_started.md){ .md-button .md-button--primary }
