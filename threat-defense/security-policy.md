---
description: "Security policy ingredients for DNS-layer protection."
icon: filter
---

# Security Policy

```mermaid
flowchart LR
    Scope[Network scope] --> Policy[Security policy]
    Feeds[Threat feeds] --> Policy
    Filters[Filters and categories] --> Policy
    Bypass[Bypass codes] --> Policy
    Policy --> Action[Detect, block, redirect, or allow]
    Action --> Reports[Reports and insights]
```

## Policy checklist

* Define internal networks and domains.
* Choose threat intelligence sources.
* Configure filters and categories.
* Decide when users can bypass.
* Route events to security operations workflows.
