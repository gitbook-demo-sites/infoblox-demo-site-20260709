---
    description: "Bypass code configuration, certificates, policy association, and user experience."
    icon: unlock-keyhole
    ---

    # Bypass codes

    Bypass code content includes configuration, adding codes to policies, enabling and disabling codes, and installing the Infoblox root certificate for bypass behavior.

{% stepper %}
{% step %}
## Configure bypass behavior

Decide which policies allow bypass and under what conditions.
{% endstep %}

{% step %}
## Prepare clients

Install the required certificate where bypass behavior depends on trusted inspection or redirection.
{% endstep %}

{% step %}
## Monitor use

Review security events and reports to confirm bypasses are expected and auditable.
{% endstep %}
{% endstepper %}
