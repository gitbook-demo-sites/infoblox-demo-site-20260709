---
    description: "Single inheritance, multiple inheritance, and additional inheritance criteria."
    icon: layer-group
    ---

    # Inheritance and templates

    The source docs contain a dedicated inheritance family covering single inheritance, multiple inheritance, additional inheritance criteria, and DHCP overrides.

## Why inheritance matters

Inheritance helps large teams avoid repeating DNS, DHCP, and IPAM configuration across every object. Administrators can set policy once, override when needed, and keep local exceptions visible.

| Pattern | Use when |
| --- | --- |
| Single inheritance | A child object should follow one clear parent default. |
| Multiple inheritance | Defaults come from more than one relevant parent or policy source. |
| Additional criteria | Matching depends on attributes beyond the direct object hierarchy. |
| Overrides | A subnet, range, or service needs explicit local behavior. |
