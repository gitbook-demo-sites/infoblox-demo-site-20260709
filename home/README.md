---
description: "A structured documentation hub for Infoblox networking and security products."
icon: house
cover: "https://raw.githubusercontent.com/gitbook-demo-sites/infoblox-demo-site-20260709/main/assets/infoblox-cover.svg"
coverY: 0
layout:
  width: wide
  cover:
    visible: true
    size: hero
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: false
  outline:
    visible: false
  pagination:
    visible: true
---

# Infoblox Documentation Hub

A focused demo site that turns three high-value Infoblox documentation areas into a clearer, GitBook-native journey.

The site preserves Infoblox's core product language: DDI management across hybrid and multi-cloud environments, DNS-layer threat protection, and cross-domain asset visibility. It also shows how a broad existing docs estate could become a guided homepage, product-specific sections, and a release feed that is easy to follow.

{% columns %}
{% column width="66.66666666666666%" %}
<button type="button" class="button primary" data-action="ask" data-icon="gitbook-assistant">Ask the Infoblox docs</button>

<button type="button" class="button secondary" data-action="ask" data-query="How do Universal DDI and Asset Insights work together?" data-icon="network-wired">DDI and assets</button> <button type="button" class="button secondary" data-action="ask" data-query="What is the setup path for Threat Defense?" data-icon="shield-halved">Threat Defense setup</button> <button type="button" class="button secondary" data-action="ask" data-query="Show recent Infoblox documentation updates" data-icon="clock-rotate-left">Recent updates</button>
{% endcolumn %}

{% column width="33.33333333333334%" %}
{% hint style="info" icon="sparkles" %}
Use GitBook AI to search across the curated Infoblox product spaces, compare workflows, and summarize recent release notes.
{% endhint %}
{% endcolumn %}
{% endcolumns %}

## Explore the products

<table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><h4><i class="fa-network-wired" style="color:$primary;"></i></h4></td><td><h4><strong>Universal DDI</strong></h4></td><td>Centralize DNS, DHCP, and IPAM across on-prem, branch, and public cloud services.</td><td><a href="https://app.gitbook.com/s/OLXbioOXuuV7oAjtGypM/">Universal DDI</a></td></tr>
<tr><td><h4><i class="fa-shield-halved" style="color:$primary;"></i></h4></td><td><h4><strong>Threat Defense</strong></h4></td><td>Use DNS as a first line of defense with policy, threat intelligence, and research tools.</td><td><a href="https://app.gitbook.com/s/bjmjWyZeEElnO6lY8R4x/">Threat Defense</a></td></tr>
<tr><td><h4><i class="fa-radar" style="color:$primary;"></i></h4></td><td><h4><strong>Asset Insights</strong></h4></td><td>Discover, monitor, and analyze assets across cloud, on-prem, IoT, OT, and third-party sources.</td><td><a href="https://app.gitbook.com/s/T7hfPll24m84ff2UcPva/">Asset Insights</a></td></tr>
<tr><td><h4><i class="fa-clock-rotate-left" style="color:$primary;"></i></h4></td><td><h4><strong>Changelog</strong></h4></td><td>Track realistic product documentation updates in a filterable release feed.</td><td><a href="https://app.gitbook.com/s/Jbf6lssWdfZLknskireu/">Changelog</a></td></tr>
</tbody></table>

## Recommended reader path

{% stepper %}
{% step %}
## Start with network services

Use Universal DDI to understand the common control plane for DNS, DHCP, IPAM, NIOS, NIOS-X, and cloud DNS providers.
{% endstep %}

{% step %}
## Add protection at the DNS layer

Move into Threat Defense to show how policy, threat feeds, DNS forwarding, endpoints, and reports protect users everywhere.
{% endstep %}

{% step %}
## Close visibility gaps

Use Asset Insights to show how discovery sources enrich the inventory and reduce blind spots across cloud and on-prem environments.
{% endstep %}
{% endstepper %}

## Why this structure works

{% columns %}
{% column %}
## For customers

* Product entry points are obvious.
* Getting-started pages sit before deep reference.
* Changelog updates are separated from evergreen guides.
{% endcolumn %}

{% column %}
## For docs teams

* Each product can keep its own owner and release cadence.
* Cross-product links make the site feel unified.
* AI and MCP actions can work over a cleaner source tree.
{% endcolumn %}
{% endcolumns %}
