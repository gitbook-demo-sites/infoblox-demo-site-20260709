---
    description: "Authoritative DNS, views, zones, records, transfers, forwarding, and DNS profiles."
    icon: globe
    ---

    # DNS zones and records

    DNS administration is one of the deepest Universal DDI content families. The source docs include views, zones, subzones, reverse-mapping zones, resource records, DNS profiles, ACLs, zone transfers, cache operations, and forwarding behavior.

{% tabs %}
{% tab title="Zones" %}
Use DNS views, primary zones, secondary zones, authoritative subzones, forward reverse-mapping zones, zone delegation, and zone transfer settings to model authority and delegation.
{% endtab %}

{% tab title="Records" %}
Create and maintain record types including NS, HTTPS, NAPTR, PTR, MX, CNAME, and other resource records. The source docs split these into task pages; this demo groups them by lifecycle.
{% endtab %}

{% tab title="Controls" %}
Use named ACLs, DNS config profiles, DNS servers, cache clearing, forwarding, and default zone settings to standardize behavior across services.
{% endtab %}
{% endtabs %}

## Recommended page split for a full build

* DNS views and zone lifecycle
* Resource record lifecycle
* DNS defaults, ACLs, and transfers
* Forwarders, cache, and troubleshooting
