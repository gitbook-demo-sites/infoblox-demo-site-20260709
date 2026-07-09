---
    description: "Anycast configuration, HA groups, NIOS-X services, and resilient service delivery."
    icon: arrows-split-up-and-left
    ---

    # Anycast and high availability

    The source docs include Anycast creation, modification, deletion, host configuration, HA groups, and service placement topics.

## Design considerations

| Decision | Impact |
| --- | --- |
| Anycast address plan | Determines how clients reach nearby DNS or DHCP services. |
| HA group membership | Controls resilient service placement and failover behavior. |
| Host-level configuration | Aligns network interfaces and services with routing design. |
| Monitoring | Confirms that service placement and failover remain healthy. |
