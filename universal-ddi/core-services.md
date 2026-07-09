---
description: "DNS, DHCP, and IPAM service areas for hybrid network operations."
icon: diagram-project
---

# Core Services

```mermaid
flowchart LR
    Control[Universal DDI control plane] --> DNS[DNS]
    Control --> DHCP[DHCP]
    Control --> IPAM[IPAM]
    DNS --> Zones[Zones and records]
    DHCP --> Options[Options, filters, fingerprints]
    IPAM --> Spaces[IP spaces, networks, addresses]
    Control --> NIOS[NIOS / NIOS-X]
    Control --> Cloud[Cloud DNS providers]
```

## Common task areas

| Area | Examples |
| --- | --- |
| DNS | Zones, records, ACLs, cache clearing, transfers, DNS servers |
| DHCP | Fixed addresses, option groups, filters, fingerprints |
| IPAM | IP spaces, networks, utilization, discovered resources |
| NIOS-X | Host registration, service deployment, NIOS-X as a Service |
