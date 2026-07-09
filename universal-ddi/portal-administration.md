---
    description: "Administration, access, RBAC, authentication, tags, notifications, and portal services."
    icon: user-gear
    ---

    # Portal administration

    Universal DDI relies on the Infoblox Portal for identity, access, shared objects, notifications, and service configuration.

## Admin task groups

| Area | Source-doc examples |
| --- | --- |
| Access and SSO | SAML applications, IdP authentication, OTP access, MFA, domain users, user groups |
| RBAC | Roles, access policies, portal admins, service API keys, user API keys |
| Shared settings | Global tags, notification subscriptions, service integrations, NTP settings |
| Operational safety | Recycle bin, audit logs, service logs, user preferences |

{% hint style="info" %}
In a full migration, this family would likely become a shared "Platform administration" space because the same concepts appear across DDI and Threat Defense.
{% endhint %}
