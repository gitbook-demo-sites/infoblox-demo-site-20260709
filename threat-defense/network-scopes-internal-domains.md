---
    description: "Network scopes, external networks, internal domains, and resolver behavior."
    icon: diagram-project
    ---

    # Network scopes and internal domains

    Threat Defense policy depends on scoping. The source docs include network scopes, external networks, internal domains, imported internal domain lists, and internal resolver behavior for DNS Forwarding Proxy.

## Scope model

```mermaid
flowchart LR
    Network[Network scope] --> Policy[Security policy]
    Domains[Internal domains] --> Forwarding[Forwarding behavior]
    Resolvers[Internal resolvers] --> Forwarding
    Policy --> Events[Security events and reports]
```

## Common tasks

* Create, edit, and remove external networks.
* Configure network scopes for policy application.
* Create and import internal domains.
* Preserve expected resolution for enterprise domains while enforcing DNS-layer security.
