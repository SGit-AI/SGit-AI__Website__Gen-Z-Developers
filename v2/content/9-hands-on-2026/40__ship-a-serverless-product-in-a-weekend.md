---
title: Ship a serverless product in a weekend
slug: ship-a-serverless-product-in-a-weekend
part: hands-on-2026
number: 40
ideas: [three-tiers-for-a-model-on-a-static-site, route-do-not-teach, billing-by-not-building-billing, the-licence-is-the-blocker, voicedebrief-stopped-at-the-billing-system, a-vault-server-in-83-lines]
answers_2018: []
sources: [news:chat-on-a-static-site, news:the-key-is-the-billing-system, news:an-agent-desktop-by-the-minute, news:cloudflare-as-lego-blocks, news:no-server-by-design, news:what-sgit-is, news:ephemeral-town-planner-services, art:gen-zx-developers]
character: zara
gravity: explorer
status: draft
---

By the end of this chapter you will have the smallest product a stranger can pay for: static files on a free host, the data in a vault the host cannot read, a model on the page that says how it chose, a payment link, and no server of yours with logic in it.

One rule for every block, from *Ephemeral town planner services*: "If it bills you by the hour when nobody is using it, it is not serverless." Storage is different. Compute that charges while idle is a server running on the other side.

## Saturday: the site and the data

**The site.** Static files on a host that charges nothing for them: GitHub Pages, or Cloudflare's static assets, free and unlimited on every plan, as its pages read on 18 October 2026. Ask the agent for the smallest site that does your one thing.

**The data.** It goes in an sgit vault, as *Privacy by design* described: encrypted before it leaves the machine, on a server that cannot read a byte. If the product only reads, no code: `sgit publish` writes a folder of ciphertext any static host can serve, and the read key is the whole credential: derived one way from the vault key, no account, safe to print on the page. The newsroom served one of 39 files this way and the real client cloned it back identically.

If users must write, you need the weekend's one piece of logic: a vault server of 83 lines, one Worker, one R2 bucket and one Durable Object per vault, on the free plan. Because the server can read nothing, it has almost nothing to do: store encrypted objects under ids, and check the write key on writes. The newsroom ran it in Cloudflare's own runtime with the real client: pushes, clones, a stale push that merged, two pushes at once, a read-only clone refused, a wrong key answered 403, no plaintext stored. The Worker and its configuration are printed in *Cloudflare as Lego blocks*; point the agent at them. It has not run on a real account, does not do files over 4 MB and has one shared access token. Those 83 lines are the honest exception to no servers of yours with logic in them: the one real limit is a write that must be checked, and this is the smallest thing that checks it.

## Sunday morning: a model on the page

A static site has no server, no session and no place to keep a secret, so the usual chat box, a backend holding the key, is not an option. Three honest choices, from *A chat box on a site with no server*. Tier 0, a deterministic matcher in the browser: free, private, offline, and it shows which words it matched on, so it is the default: a reader should never have to hold a credential to use an index. Tier 1, the reader's own key, opt-in and labelled: it lives in the page's origin, which cannot protect it as a vault app can: a trust decision the reader makes, presented as one. Tier 2, a vault bridge: the host holds the key below the permission floor and the app never sees it; not built when the article was written; its caveat travels with it: "The bridge protects your key; it is not yet a boundary that prevents all egress." When the model call fails, fall back to Tier 0 and say so.

Scope it to one question. The newsroom's directory chat answers which of nineteen sites is mine and refuses to teach the subjects: the sites already contain the arguments, and a summary that drifts from them is worse than a link that does not. It knows only the catalogue, quoted from each site's own words: the narrow thing that is right over the wide thing that drifts.

## Sunday afternoon: billing by not building billing

The model VoiceDebrief wrote down on 28 July 2026, its first day, is the shape to copy. A user pays five pounds through a payment link. You keep your cut at the moment of payment. The rest becomes the credit limit on a key you hand them; the provider meters it, and the key stops when it is spent. Against a billing system (a meter on every call, a ledger per user, disputes, refunds, fraud, custody of the data) that is a payment, a cut, a key with a ceiling and nothing else, and more profitable per pound: the margin is taken once, up front. The minimum is five pounds because a card fee with a fixed component makes a one-pound purchase return about 59 pence of inference.

Read the terms, not only the docs. OpenRouter's Management API documents "unique API keys for each customer instance" with credit limits; section 7(4) of its terms, dated 31 August 2026, forbids "reselling API access to Models". The plan was dead on the page that documented it. VoiceDebrief, which I am involved in, turns a voice note into a transcript, a translation and a debrief in the browser, on the user's own key, with no account and nothing stored; a 42-second note costs about a third of a penny. From 28 July: 239 commits and 27 releases in three weeks, then eleven commits, then three, and a last on 7 September. The counts show when it stopped, not why. What stopped it was not a server but the lack of one: the capped key per user is forbidden, and the alternative, a metering proxy, is the backend the product exists to avoid. The newsroom had found the same shape renting a Mac to an agent: every piece existed, and Apple's licence forbids leasing a Mac for less than twenty-four consecutive hours. "The Mac is not expensive per hour; it is expensive because the hour you can buy is a day."

So before you build the money on a provider, read its terms, and treat an enterprise or OEM agreement as a door to ask about, not a feature to assume; terms are read here, not interpreted, and none of this is legal advice. The nearest fit found was ElevenLabs, with per-key credit limits, OEM terms under which a business sets its own price for its end users, and a grants programme; *The credits and programmes, 2026* says how to ask. Until the answer comes, ship the user's own key, kept: honest, private, no margin; the five minutes it takes to get a key is where most people stop. It is still a product a stranger can use on Sunday night.
