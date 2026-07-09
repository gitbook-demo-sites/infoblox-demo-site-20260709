import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
BASE = "https://api.gitbook.com/v1"
ORG_ID = "lDYvDdPBo2V7fu4zoiJ8"
REPO = "infoblox-demo-site-20260709"
REPO_OWNER = "gitbook-demo-sites"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"
RAW = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main"

SPACES = [
    {
        "key": "HOME",
        "sentinel": "XSPACE_HOME",
        "folder": "home",
        "title": "Home",
        "emoji": "1f3e0",
        "icon": "house",
        "path": "home",
        "description": "A polished entry point for the three-product Infoblox demo.",
    },
    {
        "key": "DDI",
        "sentinel": "XSPACE_DDI",
        "folder": "universal-ddi",
        "title": "Universal DDI",
        "emoji": "1f310",
        "icon": "network-wired",
        "path": "universal-ddi",
        "description": "Cloud-managed DNS, DHCP, and IPAM across hybrid and multi-cloud estates.",
    },
    {
        "key": "THREAT",
        "sentinel": "XSPACE_THREAT",
        "folder": "threat-defense",
        "title": "Threat Defense",
        "emoji": "1f6e1",
        "icon": "shield-halved",
        "path": "threat-defense",
        "description": "DNS-layer security, threat intelligence, policy, reporting, and research tools.",
    },
    {
        "key": "ASSETS",
        "sentinel": "XSPACE_ASSETS",
        "folder": "asset-insights",
        "title": "Asset Insights",
        "emoji": "1f50e",
        "icon": "radar",
        "path": "asset-insights",
        "description": "Cross-domain asset discovery, analysis, and inventory across clouds and networks.",
    },
    {
        "key": "CHANGELOG",
        "sentinel": "XSPACE_CHANGELOG",
        "folder": "changelog",
        "title": "Changelog",
        "emoji": "1f4e3",
        "icon": "clock-rotate-left",
        "path": "changelog",
        "description": "Realistic release notes based on the source documentation update history.",
    },
]

SOURCE_LINKS = {
    "ddi": "https://docs.infoblox.com/space/BloxOneDDI/186614365/Infoblox+Universal+DDI+Management",
    "threat": "https://docs.infoblox.com/space/BloxOneThreatDefense/9928706/Infoblox+Threat+Defense",
    "assets": "https://docs.infoblox.com/space/UniversalAssetInsights/1501397303/About+Universal+Asset+Insights",
}


def write(path: str, content: str) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def api(method: str, path: str, body=None, expected=(200, 201, 204)):
    token = os.environ["GITBOOK_TOKEN"]
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            text = resp.read().decode()
            payload = json.loads(text) if text else None
            if resp.status not in expected:
                raise RuntimeError(f"{method} {path} returned {resp.status}: {text}")
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"{method} {path} returned {exc.code}: {detail}") from exc


def card(icon: str, title: str, desc: str, href: str) -> str:
    return (
        f'<tr><td><h4><i class="fa-{icon}" style="color:$primary;"></i></h4></td>'
        f"<td><h4><strong>{title}</strong></h4></td><td>{desc}</td>"
        f'<td><a href="{href}">{title}</a></td></tr>'
    )


def yaml(space: str) -> None:
    write(
        f"{space}/.gitbook.yaml",
        """
        root: ./
        structure:
          readme: README.md
          summary: SUMMARY.md
        """,
    )


def vars_file(space: str) -> None:
    write(
        f"{space}/.gitbook/vars.yaml",
        """
        company_name: Infoblox
        demo_name: Infoblox Documentation Hub
        review_stage: First-draft demo
        docs_portal: https://docs.infoblox.com/
        marketing_site: https://www.infoblox.com/
        support_portal: https://support.infoblox.com/
        """,
    )


def summary(space: str, lines: list[str]) -> None:
    write(f"{space}/SUMMARY.md", "# Table of contents\n\n" + "\n".join(lines))


def scaffold_assets():
    write(
        "assets/infoblox-wordmark.svg",
        """
        <svg xmlns="http://www.w3.org/2000/svg" width="640" height="132" viewBox="0 0 640 132" role="img" aria-label="Infoblox">
          <rect width="640" height="132" fill="#FFFFFF"/>
          <g transform="translate(30 31)">
            <rect width="56" height="56" rx="8" fill="#F36B21"/>
            <rect x="14" y="14" width="28" height="28" rx="5" fill="#FFFFFF" opacity=".94"/>
            <text x="82" y="41" font-family="Arial, Helvetica, sans-serif" font-size="43" font-weight="700" fill="#152536">Infoblox</text>
          </g>
        </svg>
        """,
    )
    write(
        "assets/infoblox-cover.svg",
        """
        <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="540" viewBox="0 0 1600 540" role="img" aria-label="Infoblox Documentation Hub">
          <rect width="1600" height="540" fill="#101820"/>
          <rect x="0" y="0" width="1600" height="14" fill="#F36B21"/>
          <circle cx="1240" cy="190" r="220" fill="#F36B21" opacity=".14"/>
          <circle cx="1410" cy="384" r="170" fill="#60C7D1" opacity=".14"/>
          <g stroke="#60C7D1" stroke-width="3" opacity=".55" fill="none">
            <path d="M1010 150 C1120 80 1234 84 1330 164"/>
            <path d="M1010 270 C1132 196 1268 202 1402 292"/>
            <path d="M1040 388 C1164 326 1308 326 1448 406"/>
          </g>
          <g fill="#F36B21">
            <circle cx="1010" cy="150" r="11"/><circle cx="1330" cy="164" r="11"/>
            <circle cx="1010" cy="270" r="11"/><circle cx="1402" cy="292" r="11"/>
            <circle cx="1040" cy="388" r="11"/><circle cx="1448" cy="406" r="11"/>
          </g>
          <rect x="930" y="108" width="470" height="324" rx="10" fill="#FFFFFF" opacity=".93"/>
          <rect x="974" y="152" width="258" height="18" rx="9" fill="#101820"/>
          <rect x="974" y="196" width="332" height="12" rx="6" fill="#F36B21"/>
          <rect x="974" y="226" width="286" height="12" rx="6" fill="#D8DEE6"/>
          <rect x="974" y="282" width="128" height="78" rx="7" fill="#F7FAFC" stroke="#D8DEE6"/>
          <rect x="1132" y="282" width="128" height="78" rx="7" fill="#F7FAFC" stroke="#D8DEE6"/>
          <rect x="1290" y="282" width="66" height="78" rx="7" fill="#F7FAFC" stroke="#D8DEE6"/>
          <text x="104" y="182" font-family="Arial, Helvetica, sans-serif" font-size="82" font-weight="700" fill="#FFFFFF">Infoblox</text>
          <text x="108" y="242" font-family="Arial, Helvetica, sans-serif" font-size="34" fill="#F36B21">Documentation Hub</text>
          <text x="110" y="302" font-family="Arial, Helvetica, sans-serif" font-size="25" fill="#D8DEE6">Unify networking and security guidance for Universal DDI,</text>
          <text x="110" y="336" font-family="Arial, Helvetica, sans-serif" font-size="25" fill="#D8DEE6">Threat Defense, and Asset Insights.</text>
          <rect x="110" y="388" width="360" height="48" rx="4" fill="#F36B21"/>
          <text x="136" y="420" font-family="Arial, Helvetica, sans-serif" font-size="19" font-weight="700" fill="#101820">Future-proof critical network services</text>
        </svg>
        """,
    )


def scaffold_home():
    write(
        "home/README.md",
        f"""
        ---
        description: "A structured documentation hub for Infoblox networking and security products."
        icon: house
        cover: "{RAW}/assets/infoblox-cover.svg"
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

        {{% columns %}}
        {{% column width="66.66666666666666%" %}}
        <button type="button" class="button primary" data-action="ask" data-icon="gitbook-assistant">Ask the Infoblox docs</button>

        <button type="button" class="button secondary" data-action="ask" data-query="How do Universal DDI and Asset Insights work together?" data-icon="network-wired">DDI and assets</button> <button type="button" class="button secondary" data-action="ask" data-query="What is the setup path for Threat Defense?" data-icon="shield-halved">Threat Defense setup</button> <button type="button" class="button secondary" data-action="ask" data-query="Show recent Infoblox documentation updates" data-icon="clock-rotate-left">Recent updates</button>
        {{% endcolumn %}}

        {{% column width="33.33333333333334%" %}}
        {{% hint style="info" icon="sparkles" %}}
        Use GitBook AI to search across the curated Infoblox product spaces, compare workflows, and summarize recent release notes.
        {{% endhint %}}
        {{% endcolumn %}}
        {{% endcolumns %}}

        ## Explore the products

        <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        {card("network-wired", "Universal DDI", "Centralize DNS, DHCP, and IPAM across on-prem, branch, and public cloud services.", "https://app.gitbook.com/s/XSPACE_DDI/")}
        {card("shield-halved", "Threat Defense", "Use DNS as a first line of defense with policy, threat intelligence, and research tools.", "https://app.gitbook.com/s/XSPACE_THREAT/")}
        {card("radar", "Asset Insights", "Discover, monitor, and analyze assets across cloud, on-prem, IoT, OT, and third-party sources.", "https://app.gitbook.com/s/XSPACE_ASSETS/")}
        {card("clock-rotate-left", "Changelog", "Track realistic product documentation updates in a filterable release feed.", "https://app.gitbook.com/s/XSPACE_CHANGELOG/")}
        </tbody></table>

        ## Recommended reader path

        {{% stepper %}}
        {{% step %}}
        ## Start with network services

        Use Universal DDI to understand the common control plane for DNS, DHCP, IPAM, NIOS, NIOS-X, and cloud DNS providers.
        {{% endstep %}}

        {{% step %}}
        ## Add protection at the DNS layer

        Move into Threat Defense to show how policy, threat feeds, DNS forwarding, endpoints, and reports protect users everywhere.
        {{% endstep %}}

        {{% step %}}
        ## Close visibility gaps

        Use Asset Insights to show how discovery sources enrich the inventory and reduce blind spots across cloud and on-prem environments.
        {{% endstep %}}
        {{% endstepper %}}

        ## Why this structure works

        {{% columns %}}
        {{% column %}}
        ## For customers

        * Product entry points are obvious.
        * Getting-started pages sit before deep reference.
        * Changelog updates are separated from evergreen guides.
        {{% endcolumn %}}

        {{% column %}}
        ## For docs teams

        * Each product can keep its own owner and release cadence.
        * Cross-product links make the site feel unified.
        * AI and MCP actions can work over a cleaner source tree.
        {{% endcolumn %}}
        {{% endcolumns %}}
        """,
    )
    summary(
        "home",
        [
            "* [Home](README.md)",
            "* [Documentation operating model](docs-operating-model.md)",
            "* [Source content map](source-content-map.md)",
            "* [Demo review checklist](review-checklist.md)",
        ],
    )
    write(
        "home/docs-operating-model.md",
        """
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
        """,
    )
    write(
        "home/source-content-map.md",
        f"""
        ---
        description: "The exact public sources used to shape this first-draft demo."
        icon: link
        ---

        # Source Content Map

        | Demo area | Source page | What was adapted |
        | --- | --- | --- |
        | Universal DDI | [Infoblox Universal DDI Management]({SOURCE_LINKS["ddi"]}) | Overview language, product scope, common service areas, and the getting-started path. |
        | Threat Defense | [Infoblox Threat Defense]({SOURCE_LINKS["threat"]}) | DNS-layer security positioning, security components, policy, threat intelligence, reporting, and research tools. |
        | Asset Insights | [About Universal Asset Insights]({SOURCE_LINKS["assets"]}) | Cross-domain discovery, analysis, architecture, cloud provider coverage, and on-prem discovery concepts. |
        | Changelog | Public Confluence update metadata | Realistic release notes from recent page updates across DDI, Threat Defense, and Asset Insights. |

        ## Content assumptions

        * The demo intentionally summarizes and restructures rather than exhaustively migrating the source portal.
        * Product pages are written as a polished first draft, not as a verbatim copy.
        * The changelog uses realistic update themes from the observed page names and update dates.
        """,
    )
    write(
        "home/review-checklist.md",
        """
        ---
        description: "Questions for Infoblox or the account team before polishing this further."
        icon: list-check
        ---

        # Demo Review Checklist

        | Area | Question |
        | --- | --- |
        | Structure | Should the final demo keep one product per space, or group DDI and Asset Insights under a broader Networking section? |
        | Changelog | Are product release notes enough, or should platform/portal announcements be included too? |
        | Branding | Is the dark header, orange accent, and filled sidebar close enough for the first pass? |
        | AI | Which starter questions would best show GitBook AI over the Infoblox docs estate? |
        | Migration | Are there source exports or Confluence permissions that would let us migrate a deeper content sample? |
        """,
    )


def scaffold_ddi():
    write(
        "universal-ddi/README.md",
        """
        ---
        description: "Manage DNS, DHCP, and IPAM from a unified SaaS control plane."
        icon: network-wired
        ---

        # Universal DDI

        Infoblox Universal DDI Management is a SaaS solution for hybrid and multi-cloud networking infrastructure. It consolidates DNS, DHCP, and IPAM management across on-premises environments, branch locations, and cloud providers from a single control plane.

        <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        <tr><td><i class="fa-play"></i></td><td><strong>Get started</strong></td><td>Understand the setup sequence and the main objects administrators configure.</td><td><a href="getting-started.md">Get started</a></td></tr>
        <tr><td><i class="fa-diagram-project"></i></td><td><strong>Core services</strong></td><td>See how DNS, DHCP, and IPAM fit together across hybrid infrastructure.</td><td><a href="core-services.md">Core services</a></td></tr>
        <tr><td><i class="fa-cloud"></i></td><td><strong>Public cloud DNS</strong></td><td>Centralize visibility and control across Amazon Route 53, Azure DNS, and Google Cloud DNS.</td><td><a href="cloud-dns.md">Public cloud DNS</a></td></tr>
        </tbody></table>

        {% hint style="success" %}
        Universal DDI is strongest when the docs connect operational tasks with the reason they matter: fewer silos, less manual automation, and a more reliable network foundation.
        {% endhint %}
        """,
    )
    summary(
        "universal-ddi",
        [
            "* [Universal DDI](README.md)",
            "## Start",
            "* [Getting started](getting-started.md)",
            "* [Licensing model](licensing.md)",
            "## Operate",
            "* [Core services](core-services.md)",
            "* [Public cloud DNS](cloud-dns.md)",
            "* [Reports and integrations](reports-integrations.md)",
            "* [Troubleshooting map](troubleshooting-map.md)",
        ],
    )
    write(
        "universal-ddi/getting-started.md",
        """
        ---
        description: "A guided setup sequence for Universal DDI Management."
        icon: play
        ---

        # Getting Started

        {% stepper %}
        {% step %}
        ## Confirm environments

        Identify on-premises NIOS Grid deployments, NIOS-X servers, branch locations, and public cloud DNS providers that should be managed through Universal DDI.
        {% endstep %}

        {% step %}
        ## Connect providers and services

        Add provider credentials, register NIOS-X hosts or services, and decide which DNS, DHCP, and IPAM objects should be brought under centralized management.
        {% endstep %}

        {% step %}
        ## Standardize configuration

        Align views, zones, networks, IP spaces, DHCP options, ACLs, anycast settings, and naming conventions before scaling across locations.
        {% endstep %}

        {% step %}
        ## Monitor and report

        Use reports to validate DNS responses, service health, object changes, and operational drift.
        {% endstep %}
        {% endstepper %}
        """,
    )
    write(
        "universal-ddi/licensing.md",
        """
        ---
        description: "How to explain subscription and deployment scope for Universal DDI."
        icon: key
        ---

        # Licensing Model

        Universal DDI is positioned as a subscription-based solution for scalable, reliable DNS, DHCP, and IPAM services across many locations.

        | Licensing consideration | Demo framing |
        | --- | --- |
        | Scale | Support thousands of sites without forcing each site into a bespoke management model. |
        | Portability | Use license pooling and portability to simplify expansion and migration. |
        | Deployment model | Pair cloud-managed control with NIOS, NIOS-X, virtual appliances, and infrastructure-free service options. |
        | Cost control | Reduce manual operations and avoid duplicated cloud-specific automation. |
        """,
    )
    write(
        "universal-ddi/core-services.md",
        """
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
        """,
    )
    write(
        "universal-ddi/cloud-dns.md",
        """
        ---
        description: "Centralize DNS management across public cloud providers."
        icon: cloud
        ---

        # Public Cloud DNS

        Cloud DNS services are often siloed inside individual providers. Universal DDI gives teams a way to manage and observe provider-specific DNS alongside enterprise DDI services.

        {% tabs %}
        {% tab title="AWS" %}
        Use Amazon Route 53 credentials and managed zones to bring AWS DNS into the same operating model as other DDI services.
        {% endtab %}

        {% tab title="Azure" %}
        Add Azure DNS credentials and align Azure zones with enterprise naming, ownership, and reporting practices.
        {% endtab %}

        {% tab title="Google Cloud" %}
        Connect Google Cloud DNS resources so teams can govern cloud-native DNS without switching tools.
        {% endtab %}
        {% endtabs %}

        ## Why it matters

        * Reduces fragmented DNS operations.
        * Lowers manual automation overhead.
        * Improves visibility into cloud resources and orphaned workloads.
        """,
    )
    write(
        "universal-ddi/reports-integrations.md",
        """
        ---
        description: "Reporting and integrations that make Universal DDI operationally useful."
        icon: chart-column
        ---

        # Reports and Integrations

        | Capability | Why teams use it |
        | --- | --- |
        | DNS response reports | Validate service behavior and troubleshoot demand patterns. |
        | Data Connector | Export DDI data into analytics and operational workflows. |
        | Microsoft integration | Bring Microsoft DNS and server credentials into the broader DDI model. |
        | Notification delivery | Route operational events to the teams that own the service. |

        See how asset visibility extends this model in [Asset Insights](https://app.gitbook.com/s/XSPACE_ASSETS/).
        """,
    )
    write(
        "universal-ddi/troubleshooting-map.md",
        """
        ---
        description: "A simple triage map for DDI operations."
        icon: map
        ---

        # Troubleshooting Map

        ```mermaid
        flowchart TD
            Issue[Operational issue] --> Type{Which layer?}
            Type -->|DNS| DNS[Check zones, records, ACLs, cache, and transfers]
            Type -->|DHCP| DHCP[Check filters, options, fingerprints, and fixed addresses]
            Type -->|IPAM| IPAM[Check spaces, networks, utilization, and discovered resources]
            Type -->|Provider| Cloud[Check cloud credentials, provider sync, and zone ownership]
            DNS --> Report[Review reports and recent changes]
            DHCP --> Report
            IPAM --> Report
            Cloud --> Report
        ```
        """,
    )


def scaffold_threat():
    write(
        "threat-defense/README.md",
        """
        ---
        description: "Use DNS as a first line of defense against modern threats."
        icon: shield-halved
        ---

        # Threat Defense

        Infoblox Threat Defense is a hybrid cybersecurity solution that uses DNS to detect and block threats before impact. It combines DNS Firewall, Threat Intelligence Data Exchange, Dossier, security policy, reporting, and integrations into a unified security workflow.

        <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        <tr><td><i class="fa-rocket"></i></td><td><strong>Get started</strong></td><td>Deploy protection for on-prem, remote, branch, and roaming users.</td><td><a href="getting-started.md">Get started</a></td></tr>
        <tr><td><i class="fa-filter"></i></td><td><strong>Security policy</strong></td><td>Define scopes, feeds, filters, and policy behavior.</td><td><a href="security-policy.md">Security policy</a></td></tr>
        <tr><td><i class="fa-magnifying-glass-chart"></i></td><td><strong>Research tools</strong></td><td>Use TIDE and Dossier to investigate suspicious domains and threat indicators.</td><td><a href="research-tools.md">Research tools</a></td></tr>
        </tbody></table>
        """,
    )
    summary(
        "threat-defense",
        [
            "* [Threat Defense](README.md)",
            "## Start",
            "* [Getting started](getting-started.md)",
            "* [Detection mode](detection-mode.md)",
            "## Configure",
            "* [Security policy](security-policy.md)",
            "* [Threat intelligence feeds](threat-feeds.md)",
            "* [Endpoints and DNS forwarding](endpoints-forwarding.md)",
            "## Investigate",
            "* [Reports and insights](reports-insights.md)",
            "* [Research tools](research-tools.md)",
        ],
    )
    write(
        "threat-defense/getting-started.md",
        """
        ---
        description: "The core setup flow for DNS-layer security."
        icon: rocket
        ---

        # Getting Started

        {% stepper %}
        {% step %}
        ## Define network scopes

        Decide which networks, users, offices, roaming clients, or resolver paths should be protected by each policy.
        {% endstep %}

        {% step %}
        ## Configure security components

        Set DNS forwarding, DNS Firewall behavior, feeds, filters, and integrations that fit the environment.
        {% endstep %}

        {% step %}
        ## Deploy endpoints where needed

        Protect remote and roaming users with endpoint deployment, status checks, upgrades, and health monitoring.
        {% endstep %}

        {% step %}
        ## Monitor outcomes

        Use summary reports, security activity, insights, and research tools to validate coverage and investigate detections.
        {% endstep %}
        {% endstepper %}
        """,
    )
    write(
        "threat-defense/detection-mode.md",
        """
        ---
        description: "How to explain detection-first and blocking workflows."
        icon: tower-observation
        ---

        # Detection Mode

        Detection mode helps teams observe potential impact before enforcing blocking policies.

        | Mode | Use when |
        | --- | --- |
        | Detect | You need baseline visibility, false-positive review, or a staged rollout. |
        | Block | You are ready to prevent communications with known malicious infrastructure. |
        | Bypass | You need temporary exceptions for operational continuity. |

        {% hint style="warning" %}
        A good rollout guide should pair detection mode with reporting, ownership, and a clear promotion path to enforcement.
        {% endhint %}
        """,
    )
    write(
        "threat-defense/security-policy.md",
        """
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
        """,
    )
    write(
        "threat-defense/threat-feeds.md",
        """
        ---
        description: "Curated threat intelligence and how it reaches the enforcement layer."
        icon: satellite-dish
        ---

        # Threat Intelligence Feeds

        Threat Defense uses highly accurate threat intelligence and machine-learning analytics to detect malware, ransomware, phishing, exploit kits, DNS-based data exfiltration, domain generation algorithms, and related threats.

        {% columns %}
        {% column %}
        ## Inputs

        * Curated Infoblox intelligence
        * TIDE threat indicators
        * Dossier investigation context
        * Customer-specific policy decisions
        {% endcolumn %}

        {% column %}
        ## Outputs

        * DNS-layer detection and blocking
        * Distribution to security infrastructure
        * Reports for investigation and response
        * Evidence for future policy tuning
        {% endcolumn %}
        {% endcolumns %}
        """,
    )
    write(
        "threat-defense/endpoints-forwarding.md",
        """
        ---
        description: "Endpoint and DNS forwarding components for hybrid environments."
        icon: laptop-shield
        ---

        # Endpoints and DNS Forwarding

        | Component | Purpose |
        | --- | --- |
        | Endpoint | Protect roaming and remote users outside the traditional network perimeter. |
        | DNS Forwarding Proxy | Route DNS requests through the enforcement and policy layer. |
        | Internal domains | Preserve expected resolution behavior for enterprise domains. |
        | Internal resolvers | Keep resolver routing aligned with the existing ecosystem. |

        <details>
        <summary>Operational pages that usually sit below this topic</summary>

        Endpoint download, installation, status, health check, upgrades, SSO authentication, mobile enrollment, and DNS forwarding proxy best practices.
        </details>
        """,
    )
    write(
        "threat-defense/reports-insights.md",
        """
        ---
        description: "Use reports to show coverage, blocked threats, and investigation context."
        icon: chart-line
        ---

        # Reports and Insights

        | Report area | Questions it should answer |
        | --- | --- |
        | Summary reports | What did Threat Defense detect or block over time? |
        | Security activity | Which users, devices, or domains are driving events? |
        | Threat insight | Which campaigns or indicators need analyst attention? |
        | Devices and DNS users | Which assets or users are associated with risky activity? |
        """,
    )
    write(
        "threat-defense/research-tools.md",
        """
        ---
        description: "Use TIDE and Dossier for threat research and response."
        icon: magnifying-glass-chart
        ---

        # Research Tools

        {% tabs %}
        {% tab title="TIDE" %}
        Threat Intelligence Data Exchange helps teams manage, search, and operationalize threat indicators.
        {% endtab %}

        {% tab title="Dossier" %}
        Dossier provides investigation context for domains, indicators, and related infrastructure.
        {% endtab %}

        {% tab title="Reports" %}
        Reports connect detection and blocking activity back to policies, scopes, users, and devices.
        {% endtab %}
        {% endtabs %}
        """,
    )


def scaffold_assets_space():
    write(
        "asset-insights/README.md",
        """
        ---
        description: "Automate discovery and analysis of assets across diverse environments."
        icon: radar
        ---

        # Universal Asset Insights

        Universal Asset Insights automates the discovery, monitoring, and analysis of assets across on-premises networks, public clouds, IoT and OT environments, and third-party applications.

        <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        <tr><td><i class="fa-cloud"></i></td><td><strong>Cloud discovery</strong></td><td>Inventory assets from AWS, Azure, Google Cloud, and related cloud metadata.</td><td><a href="cloud-discovery.md">Cloud discovery</a></td></tr>
        <tr><td><i class="fa-server"></i></td><td><strong>On-prem discovery</strong></td><td>Use NIOS-X discovery and network scanning to find physical and virtual assets.</td><td><a href="on-prem-discovery.md">On-prem discovery</a></td></tr>
        <tr><td><i class="fa-plug"></i></td><td><strong>Third-party sources</strong></td><td>Bring in integrations such as CrowdStrike, Akamai, Cloudflare, and other sources.</td><td><a href="third-party-discovery.md">Third-party discovery</a></td></tr>
        </tbody></table>
        """,
    )
    summary(
        "asset-insights",
        [
            "* [Universal Asset Insights](README.md)",
            "## Concepts",
            "* [Architecture](architecture.md)",
            "* [Insight classifications](insight-classifications.md)",
            "## Discovery",
            "* [Cloud discovery](cloud-discovery.md)",
            "* [On-prem discovery](on-prem-discovery.md)",
            "* [Third-party discovery](third-party-discovery.md)",
            "## Operate",
            "* [Review discovered assets](review-assets.md)",
        ],
    )
    write(
        "asset-insights/architecture.md",
        """
        ---
        description: "How asset data moves from discovery sources into actionable inventory."
        icon: diagram-project
        ---

        # Architecture

        ```mermaid
        flowchart LR
            AWS[AWS] --> Collect[Discovery configuration]
            Azure[Azure] --> Collect
            GCP[Google Cloud] --> Collect
            OnPrem[On-prem networks] --> Collect
            Third[Third-party apps] --> Collect
            Collect --> Normalize[Normalize metadata]
            Normalize --> Classify[Classify assets and insights]
            Classify --> Inventory[Continuously updated inventory]
            Inventory --> Actions[Risk, cleanup, and operations workflows]
        ```

        Universal Asset Insights is useful because it turns separate discovery sources into one operational inventory that NetOps, CloudOps, and SecOps can share.
        """,
    )
    write(
        "asset-insights/insight-classifications.md",
        """
        ---
        description: "Classify assets and findings so teams can prioritize follow-up work."
        icon: tags
        ---

        # Insight Classifications

        | Classification | Example follow-up |
        | --- | --- |
        | Unknown asset | Assign ownership and verify expected presence. |
        | Unauthorized device | Escalate to security operations for validation. |
        | Cloud resource drift | Compare provider metadata with intended network architecture. |
        | IPAM mismatch | Reconcile discovered resources with managed IPAM records. |
        | IoT / OT asset | Confirm protocol, location, and monitoring requirements. |
        """,
    )
    write(
        "asset-insights/cloud-discovery.md",
        """
        ---
        description: "Discover and monitor assets across AWS, Azure, and Google Cloud."
        icon: cloud
        ---

        # Cloud Discovery

        {% tabs %}
        {% tab title="AWS" %}
        Configure accounts, organizational units, destinations, excluded asset types, permissions, and summary review before enabling discovery.
        {% endtab %}

        {% tab title="Azure" %}
        Configure Azure general settings, destinations, excluded asset types, and review steps before collecting metadata.
        {% endtab %}

        {% tab title="Google Cloud" %}
        Configure folders or projects, destination settings, excluded asset types, and review steps for Google Cloud discovery.
        {% endtab %}
        {% endtabs %}

        ## Metadata to surface

        * Asset type and provider.
        * Configuration and location.
        * Network relationships.
        * Ownership and usage signals.
        """,
    )
    write(
        "asset-insights/on-prem-discovery.md",
        """
        ---
        description: "Discover physical and virtual devices in on-premises environments."
        icon: server
        ---

        # On-Prem Discovery

        On-prem discovery uses network scanning and NIOS-X discovery services to identify assets connected to corporate networks.

        {% stepper %}
        {% step %}
        ## Review requirements

        Confirm minimum system requirements, network reachability, and the scanning model.
        {% endstep %}

        {% step %}
        ## Create discovery services

        Deploy and configure NIOS-X discovery servers in the target environment.
        {% endstep %}

        {% step %}
        ## Run discovery workflows

        Use on-prem discovery workflows to collect devices, addresses, and network context.
        {% endstep %}
        {% endstepper %}
        """,
    )
    write(
        "asset-insights/third-party-discovery.md",
        """
        ---
        description: "Use integrations to enrich asset visibility beyond cloud and network discovery."
        icon: plug
        ---

        # Third-Party Discovery

        Third-party discovery brings external context into the same inventory model.

        | Source | Example role |
        | --- | --- |
        | CrowdStrike | Endpoint and security context. |
        | Akamai | Edge and delivery-related assets. |
        | Cloudflare | DNS, edge, and security-adjacent resources. |
        | Other integrations | Specialized systems that hold asset or ownership metadata. |

        See related security workflows in [Threat Defense](https://app.gitbook.com/s/XSPACE_THREAT/).
        """,
    )
    write(
        "asset-insights/review-assets.md",
        """
        ---
        description: "Turn discovered inventory into operational follow-up."
        icon: clipboard-check
        ---

        # Review Discovered Assets

        | Review step | Outcome |
        | --- | --- |
        | Validate source | Confirm whether an asset came from cloud, on-prem, or third-party discovery. |
        | Match to IPAM | Identify unmanaged or mismatched IP resources. |
        | Assign owner | Route unknown or unauthorized assets to the right team. |
        | Track drift | Watch for changes in existing devices and cloud resources. |

        {% hint style="success" %}
        The strongest story is cross-functional: NetOps sees inventory quality, CloudOps sees cloud drift, and SecOps sees unknown or risky assets earlier.
        {% endhint %}
        """,
    )


def scaffold_changelog():
    write(
        "changelog/.gitbook/tags.yaml",
        """
        - tag: ddi
          label: Universal DDI
          icon: network-wired
        - tag: threat-defense
          label: Threat Defense
          icon: shield-halved
        - tag: asset-insights
          label: Asset Insights
          icon: radar
        - tag: docs
          label: Documentation
          icon: book-open
        """,
    )
    write(
        "changelog/README.md",
        """
        ---
        description: "Product documentation updates across Universal DDI, Threat Defense, and Asset Insights."
        icon: clock-rotate-left
        layout:
          width: wide
        ---

        # Changelog

        A realistic release feed based on the source documentation areas and recent update metadata.

        {% updates format="full" %}
        {% update date="2026-07-09" tags="asset-insights,docs" %}
        ## Google Cloud and Azure discovery settings refreshed

        Updated Asset Insights guidance for Google Cloud destination configuration, excluded asset types, and Azure destination review. The release keeps the cloud discovery workflow aligned with the latest provider-specific configuration pages.
        {% endupdate %}

        {% update date="2026-07-01" tags="ddi,docs" %}
        ## DHCP, DNS zone, and IPAM configuration pages refreshed

        Updated Universal DDI task coverage for DHCP fingerprints, DNS zone transfers, DHCP option groups, and IP spaces. This release is aimed at operators standardizing DDI configuration across many locations.
        {% endupdate %}

        {% update date="2026-06-30" tags="threat-defense,docs" %}
        ## Threat Defense release notes updated

        Refreshed the Threat Defense "What's New" entry and kept the main security documentation aligned with policy, feed, and reporting changes.
        {% endupdate %}

        {% update date="2026-05-11" tags="threat-defense" %}
        ## Security policy configuration expanded

        Added clearer security-policy configuration coverage for administrators defining network scopes, feeds, bypass behavior, and policy outcomes before enforcement.
        {% endupdate %}

        {% update date="2026-04-30" tags="asset-insights" %}
        ## Cloud, integration, and NIOS-X discovery workflows updated

        Refreshed Asset Insights configuration pages for cloud discovery, integration-based discovery, Amazon Web Services, Microsoft Azure, Google Cloud Platform, and NIOS-X discovery services.
        {% endupdate %}

        {% update date="2025-12-12" tags="asset-insights" %}
        ## Universal Asset Insights overview refreshed

        Updated the overview explaining automated asset discovery, continuous monitoring, cross-domain inventory, and analysis across on-premises networks, public cloud, IoT, OT, and third-party sources.
        {% endupdate %}
        {% endupdates %}
        """,
    )
    summary("changelog", ["* [Changelog](README.md)"])


def scaffold_content():
    for item in SPACES:
        yaml(item["folder"])
        vars_file(item["folder"])

    write(
        "README.md",
        """
        # Infoblox demo site

        First-draft GitBook demo content for Infoblox. Each top-level folder is imported as a separate GitBook space.
        """,
    )
    write(".gitignore", ".DS_Store\nThumbs.db\n*.swp\n*.swo\n.idea/\n.vscode/\n__pycache__/\n")
    scaffold_assets()
    scaffold_home()
    scaffold_ddi()
    scaffold_threat()
    scaffold_assets_space()
    scaffold_changelog()


def run(cmd: list[str], cwd=ROOT, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check, text=True)


def ensure_repo():
    if not (ROOT / ".git").exists():
        run(["git", "init", "-b", "main"])
    run(["git", "config", "user.name", "Jeeves"])
    run(["git", "config", "user.email", "dave+ai@gitbook.com"])
    run(["git", "add", "."])
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode != 0:
        run(["git", "commit", "-m", "Initial Infoblox demo scaffold"])

    view = subprocess.run(["gh", "repo", "view", f"{REPO_OWNER}/{REPO}"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    remotes = subprocess.run(["git", "remote"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    if "origin" not in remotes:
        run(["git", "remote", "add", "origin", REPO_URL])
    if view.returncode != 0:
        run(["gh", "repo", "create", f"{REPO_OWNER}/{REPO}", "--public", "--source", str(ROOT), "--remote", "origin", "--push"])
    else:
        run(["gh", "repo", "edit", f"{REPO_OWNER}/{REPO}", "--visibility", "public", "--accept-visibility-change-consequences"])
        run(["git", "push", "-u", "origin", "main"])


def git_commit_push(message: str):
    run(["git", "add", "."])
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode != 0:
        run(["git", "commit", "-m", message])
    run(["git", "push"])


def create_site(org_id: str) -> dict:
    _, site = api(
        "POST",
        f"/orgs/{org_id}/sites",
        {"type": "ultimate", "title": "Infoblox Documentation Hub", "visibility": "share-link"},
    )
    site_id = site["id"]
    api(
        "PATCH",
        f"/orgs/{org_id}/sites/{site_id}",
        {"title": "Infoblox Documentation Hub", "visibility": "share-link", "basename": "infoblox-documentation-hub"},
    )
    created = {"org": org_id, "site": site_id, "spaces": {}, "sections": {}, "site_spaces": {}, "site_object": site}
    for item in SPACES:
        _, space = api(
            "POST",
            f"/orgs/{org_id}/spaces",
            {"title": item["title"], "emoji": item["emoji"], "empty": True, "editMode": "live"},
        )
        space_id = space["id"]
        created["spaces"][item["key"]] = space_id
        _, section = api(
            "POST",
            f"/orgs/{org_id}/sites/{site_id}/sections",
            {"spaceId": space_id, "title": item["title"], "icon": item["icon"], "draft": False},
        )
        section_id = section["id"]
        site_space_id = section["siteSpaces"][0]["id"]
        created["sections"][item["key"]] = section_id
        created["site_spaces"][item["key"]] = site_space_id
        api(
            "PATCH",
            f"/orgs/{org_id}/sites/{site_id}/sections/{section_id}",
            {"path": item["path"], "description": item["description"], "draft": False, "defaultSiteSpace": site_space_id},
        )

    api(
        "PATCH",
        f"/orgs/{org_id}/sites/{site_id}",
        {"defaultSiteSection": created["sections"]["HOME"], "defaultSiteSpace": created["site_spaces"]["HOME"]},
    )
    return created


def replace_sentinels(space_ids: dict[str, str]):
    replacements = {item["sentinel"]: space_ids[item["key"]] for item in SPACES}
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")


def import_spaces(created: dict):
    imports = {}
    for item in SPACES:
        status, _ = api(
            "POST",
            f"/spaces/{created['spaces'][item['key']]}/git/import",
            {
                "url": REPO_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": item["folder"],
                "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[item["key"]] = {"status": status, "space": created["spaces"][item["key"]], "folder": item["folder"]}
    write("gitbook-import-results.json", json.dumps(imports, indent=2))


def customization_payload(created: dict, share_url: str):
    logo = f"{RAW}/assets/infoblox-wordmark.svg"
    cover = f"{RAW}/assets/infoblox-cover.svg"
    return {
        "title": "Infoblox Documentation Hub",
        "localizedTitle": {},
        "internationalization": {"locale": "en"},
        "styling": {
            "theme": "clean",
            "primaryColor": {"light": "#F36B21", "dark": "#FF9A57"},
            "infoColor": {"light": "#007A87", "dark": "#60C7D1"},
            "successColor": {"light": "#248A5B", "dark": "#63D29C"},
            "warningColor": {"light": "#B7791F", "dark": "#F6C760"},
            "dangerColor": {"light": "#B42318", "dark": "#F97066"},
            "tint": {"color": {"light": "#F5F7FA", "dark": "#101820"}},
            "corners": "rounded",
            "depth": "flat",
            "links": "accent",
            "font": "Inter",
            "monospaceFont": "IBMPlexMono",
            "icons": "regular",
            "background": "plain",
            "sidebar": {"background": "filled", "list": "line"},
            "codeTheme": {
                "default": {"light": "default-light", "dark": "default-dark"},
                "openapi": {"light": "default-light", "dark": "default-dark"},
            },
            "search": "prominent",
        },
        "favicon": {"icon": {"light": "https://www.infoblox.com/wp-content/uploads/cropped-infoblox-favicon-32x32.png", "dark": "https://www.infoblox.com/wp-content/uploads/cropped-infoblox-favicon-32x32.png"}},
        "header": {
            "preset": "default",
            "logo": {"light": logo, "dark": logo},
            "links": [
                {"title": "Products", "to": {"kind": "url", "url": "https://www.infoblox.com/products/"}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Docs portal", "to": {"kind": "url", "url": "https://docs.infoblox.com/"}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Support", "to": {"kind": "url", "url": "https://support.infoblox.com/"}, "style": "button-secondary", "links": [], "localizedTitle": {}},
                {"title": "Book a demo", "to": {"kind": "url", "url": "https://www.infoblox.com/contact/"}, "style": "button-primary", "links": [], "localizedTitle": {}},
            ],
        },
        "footer": {
            "logo": {"light": logo, "dark": logo},
            "groups": [
                {
                    "title": "Demo spaces",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Home", "to": {"kind": "space", "space": created["spaces"]["HOME"]}, "localizedTitle": {}},
                        {"title": "Universal DDI", "to": {"kind": "space", "space": created["spaces"]["DDI"]}, "localizedTitle": {}},
                        {"title": "Threat Defense", "to": {"kind": "space", "space": created["spaces"]["THREAT"]}, "localizedTitle": {}},
                        {"title": "Asset Insights", "to": {"kind": "space", "space": created["spaces"]["ASSETS"]}, "localizedTitle": {}},
                        {"title": "Changelog", "to": {"kind": "space", "space": created["spaces"]["CHANGELOG"]}, "localizedTitle": {}},
                    ],
                },
                {
                    "title": "Sources",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Infoblox website", "to": {"kind": "url", "url": "https://www.infoblox.com/"}, "localizedTitle": {}},
                        {"title": "Infoblox docs", "to": {"kind": "url", "url": "https://docs.infoblox.com/"}, "localizedTitle": {}},
                        {"title": "Source repo", "to": {"kind": "url", "url": f"https://github.com/{REPO_OWNER}/{REPO}"}, "localizedTitle": {}},
                    ],
                },
            ],
            "copyright": "Infoblox Documentation Hub demo - sample content only.",
        },
        "themes": {"default": "light", "toggeable": True},
        "pdf": {"enabled": True},
        "feedback": {"enabled": True},
        "ai": {
            "mode": "assistant",
            "suggestions": [
                "How do Universal DDI and Asset Insights work together?",
                "What is the setup path for Threat Defense?",
                "Show recent Universal DDI documentation updates",
                "Which discovery sources are covered in Asset Insights?",
            ],
        },
        "advancedCustomization": {"enabled": True},
        "trademark": {"enabled": True},
        "externalLinks": {"target": "self"},
        "pagination": {"enabled": True},
        "pageActions": {"externalAI": True, "markdown": True, "mcp": True, "items": ["assistant", "markdown", "external-ai", "mcp", "pdf"]},
        "git": {"showEditLink": False},
        "privacyPolicy": {"url": "https://www.infoblox.com/company/legal/privacy-policy/"},
        "socialPreview": {"url": cover},
        "socialAccounts": [
            {"platform": "linkedin", "handle": "company/infoblox", "display": {"footer": True, "header": False}},
        ],
        "insights": {"trackingCookie": True},
    }


def apply_customization(org_id: str, site_id: str, created: dict, share_url: str):
    _, customized = api("PUT", f"/orgs/{org_id}/sites/{site_id}/customization", customization_payload(created, share_url))
    write("gitbook-customization-result.json", json.dumps(customized, indent=2))


def main():
    org_id = sys.argv[1] if len(sys.argv) > 1 else ORG_ID
    scaffold_content()
    ensure_repo()

    created_path = ROOT / "gitbook-created.json"
    if created_path.exists():
        created = json.loads(created_path.read_text(encoding="utf-8"))
        replace_sentinels(created["spaces"])
        git_commit_push("Keep Infoblox GitBook space links resolved")
    else:
        created = create_site(org_id)
        replace_sentinels(created["spaces"])
        write("gitbook-created.json", json.dumps(created, indent=2))
        git_commit_push("Resolve Infoblox GitBook space links")

    import_spaces(created)
    try:
        publish_status, publish = api("POST", f"/orgs/{org_id}/sites/{created['site']}/publish")
    except RuntimeError as exc:
        if "Site is already published" not in str(exc):
            raise
        publish_status, publish = api("GET", f"/orgs/{org_id}/sites/{created['site']}")
    share_status, share = api("POST", f"/orgs/{org_id}/sites/{created['site']}/share-links", {"name": "Infoblox demo review"})
    share_url = share["urls"]["published"]
    apply_customization(org_id, created["site"], created, share_url)
    try:
        publish2_status, publish2 = api("POST", f"/orgs/{org_id}/sites/{created['site']}/publish")
    except RuntimeError as exc:
        if "Site is already published" not in str(exc):
            raise
        publish2_status, publish2 = api("GET", f"/orgs/{org_id}/sites/{created['site']}")
    _, structure = api("GET", f"/orgs/{org_id}/sites/{created['site']}/structure")
    write("gitbook-structure.json", json.dumps(structure, indent=2))
    final = {
        "publish_status": publish2_status,
        "publish": publish2,
        "first_publish_status": publish_status,
        "share_status": share_status,
        "share": share,
        "published_url": share_url,
        "app_url": publish2["urls"]["app"],
        "preview_url": publish2["urls"]["preview"],
        "repo": f"https://github.com/{REPO_OWNER}/{REPO}",
    }
    write("gitbook-publish-share.json", json.dumps(final, indent=2))
    git_commit_push("Add Infoblox GitBook publish artifacts")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
