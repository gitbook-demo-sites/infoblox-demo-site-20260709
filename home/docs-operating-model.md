---
description: "How this demo maps a large existing documentation portal into focused GitBook spaces."
icon: sitemap
---

# Documentation Operating Model

```mermaid
flowchart LR
    Home[Home hub] --> DDI[Universal DDI]
    Home --> TD[Threat Defense]
    Home --> UAI[Asset Insights]
    Home --> CL[Changelog]
    DDI --> DNS[DNS / DHCP / IPAM]
    TD --> Policy[Policies / feeds / reports]
    UAI --> Discovery[Cloud / on-prem / third-party discovery]
    CL --> Releases[Release communication]
```

## Proposed ownership

| Area | Primary owner | Update cadence |
| --- | --- | --- |
| Universal DDI | NetOps documentation | With service and provider changes |
| Threat Defense | Security product documentation | With policy, endpoint, feed, and report updates |
| Asset Insights | Cloud and asset visibility documentation | With discovery source and architecture updates |
| Changelog | Product documentation operations | Weekly or release-driven |

{% hint style="info" %}
This draft uses only a few source pages, by design. The structure can scale to the full Infoblox docs estate without making the homepage carry every long-tail topic.
{% endhint %}
