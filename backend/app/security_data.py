"""Security Engineering module data — Enterprise Agentic Platforms on Public Clouds."""

SECURITY_CHAPTERS = [
    {
        "id": "ch-01-intro",
        "chapter_num": 1,
        "title": "Introduction to Enterprise Agentic Security",
        "subtitle": "Why securing AI agents is fundamentally different",
        "description": "Understand the threat landscape for enterprise agentic systems, the unique challenges they introduce, and the core principles that govern securing them on public clouds.",
        "tags": ["foundations", "threat-modeling", "zero-trust"],
        "estimated_minutes": 20,
        "sections": [
            {
                "id": "s1-1",
                "title": "The Agentic Revolution & Its Security Implications",
                "blocks": [
                    {"type": "paragraph", "content": "Enterprise AI agents are no longer simple chatbots. They autonomously plan, reason, and execute actions — calling APIs, reading databases, invoking tools, and orchestrating other agents. This shift from passive inference to active execution fundamentally changes the security model."},
                    {"type": "paragraph", "content": "A traditional web application has a well-defined trust boundary: users authenticate once, sessions are short-lived, and every action traces back to a human identity. Agents break this model. A single user request can fan out into dozens of downstream actions, each crossing service boundaries, each potentially with elevated privileges."},
                    {"type": "callout", "kind": "warning", "title": "The Core Problem", "content": "Agents act autonomously on behalf of users and systems. Without proper identity controls, a compromised agent or malicious tool invocation can result in privilege escalation, data exfiltration, or cascading failures across your entire platform."},
                    {"type": "bullets", "items": [
                        "Agents maintain long-running sessions that outlive typical auth tokens",
                        "Multi-hop tool calls create transitive trust that is hard to audit",
                        "LLM prompt injection can hijack agent behavior and bypass business logic",
                        "Agents may spawn sub-agents, creating complex identity delegation chains",
                        "Cloud-native agents often run serverless, making network-based controls insufficient"
                    ]},
                ]
            },
            {
                "id": "s1-2",
                "title": "Threat Landscape for Agentic Systems",
                "blocks": [
                    {"type": "paragraph", "content": "Before designing controls, you must understand what you are defending against. The OWASP Top 10 for LLM Applications and emerging agentic security research identify several critical threat vectors."},
                    {"type": "heading", "level": 3, "content": "Confused Deputy Attack"},
                    {"type": "paragraph", "content": "A confused deputy attack occurs when an agent with elevated privileges is tricked into performing actions on behalf of a less-privileged principal. In agentic systems, this often manifests through prompt injection — a malicious document or web page injects instructions that cause the agent to use its legitimate credentials to exfiltrate data or take unauthorized actions."},
                    {"type": "heading", "level": 3, "content": "Token Exfiltration"},
                    {"type": "paragraph", "content": "Agents receive access tokens to call downstream services. If these tokens are logged, included in LLM context, or returned in tool outputs, they can be exfiltrated. Short-lived, scoped tokens with strict audience validation are the primary defense."},
                    {"type": "heading", "level": 3, "content": "Privilege Escalation via Tool Chaining"},
                    {"type": "paragraph", "content": "Each tool an agent can call represents a potential privilege escalation vector. If Tool A can read secrets and Tool B can write to external endpoints, an attacker who can influence the agent's reasoning can chain these to exfiltrate secrets — even if no single tool is individually dangerous."},
                    {"type": "heading", "level": 3, "content": "Identity Spoofing in Multi-Agent Systems"},
                    {"type": "paragraph", "content": "In orchestrator/sub-agent architectures, sub-agents must verify the identity of orchestrating agents. Without cryptographic verification, a compromised component can impersonate a trusted orchestrator to gain elevated permissions."},
                    {"type": "callout", "kind": "danger", "title": "Real-World Impact", "content": "Enterprise agentic platforms with access to internal tools (databases, code repos, communication channels) can cause irreversible damage if an agent is hijacked. One successful prompt injection in a customer-facing agent with CRM write access can modify thousands of records before detection."},
                ]
            },
            {
                "id": "s1-3",
                "title": "Core Security Principles",
                "blocks": [
                    {"type": "paragraph", "content": "Securing agentic platforms requires applying established security principles with new rigor, adapted for the autonomous, multi-hop nature of agent execution."},
                    {"type": "heading", "level": 3, "content": "Zero Trust for Agents"},
                    {"type": "paragraph", "content": "Zero trust means never implicitly trusting any entity — even internal services. Every request from an agent must carry a verifiable identity credential, and every service must validate it independently. The fact that a request arrived from inside your VPC is not sufficient evidence of legitimacy."},
                    {"type": "heading", "level": 3, "content": "Least Privilege"},
                    {"type": "paragraph", "content": "Each agent identity should have the minimum permissions required to complete its task. Rather than granting broad read/write access, issue scoped tokens with explicit resource and action constraints. An agent that summarizes documents does not need write access."},
                    {"type": "heading", "level": 3, "content": "Identity Propagation"},
                    {"type": "paragraph", "content": "As requests flow through multiple services, the original user identity and the acting agent identity must both be propagated. This enables downstream services to enforce user-level policies and supports comprehensive audit trails."},
                    {"type": "heading", "level": 3, "content": "Defense in Depth"},
                    {"type": "paragraph", "content": "No single control is sufficient. Layer network controls (VPC isolation), identity controls (OIDC/OAuth tokens), application controls (tool-level authorization), and detective controls (audit logging) so that a failure in one layer does not result in a breach."},
                    {"type": "code", "language": "python", "title": "Security Checklist: Agent Design Review", "content": """# Run this checklist before deploying any agent to production

AGENT_SECURITY_CHECKLIST = {
    "identity": [
        "Agent has a dedicated workload identity (not shared with other services)",
        "Agent credentials are short-lived and automatically rotated",
        "Agent identity is separate from the user identity it acts on behalf of",
    ],
    "authorization": [
        "Agent permissions follow least-privilege principle",
        "Tool access is explicitly scoped per agent role",
        "User identity is propagated to all downstream services",
    ],
    "token_management": [
        "Access tokens have short TTLs (< 15 minutes for sensitive resources)",
        "Tokens are never included in LLM prompts or tool outputs",
        "Token exchange is used when crossing service boundaries",
    ],
    "observability": [
        "Every tool invocation is logged with user + agent identity",
        "Structured audit logs are shipped to immutable storage",
        "Anomaly detection alerts are configured for unusual access patterns",
    ],
    "network": [
        "MCP servers are VPC-isolated",
        "External tool calls go through egress controls",
        "mTLS is enabled for cross-service communication",
    ],
}

def review_agent(agent_config: dict) -> list[str]:
    failures = []
    for category, checks in AGENT_SECURITY_CHECKLIST.items():
        for check in checks:
            if not agent_config.get(check, False):
                failures.append(f"[{category.upper()}] FAIL: {check}")
    return failures
"""},
                ]
            },
        ],
        "challenges": [
            {
                "id": "ch01-c1",
                "title": "Identify Agentic Security Vulnerabilities",
                "difficulty": "Easy",
                "description": "Given a description of an agentic workflow, identify all security vulnerabilities present and classify them by threat type.",
                "context": """An enterprise agent has the following design:
- Single IAM role shared across all agent instances
- Access tokens for downstream services are passed as tool arguments (visible in logs)
- Agent can call: read_database(), write_email(), search_web(), execute_code()
- No user identity is propagated to downstream services
- Sessions persist for 24 hours with no re-authentication
- All tool outputs are included verbatim in the LLM context window""",
                "starter_code": """def identify_vulnerabilities(agent_design: str) -> list[dict]:
    \"\"\"
    Analyze the agent design and return a list of vulnerabilities.
    Each vulnerability should have:
    - 'type': threat category (e.g., 'privilege_escalation', 'token_exfiltration', etc.)
    - 'severity': 'critical', 'high', 'medium', 'low'
    - 'description': what the vulnerability is
    - 'remediation': how to fix it
    \"\"\"
    vulnerabilities = []
    # Your analysis here
    return vulnerabilities
""",
                "solution_code": """def identify_vulnerabilities(agent_design: str) -> list[dict]:
    return [
        {
            "type": "shared_identity",
            "severity": "critical",
            "description": "Single IAM role shared across all agent instances prevents per-agent audit trails and makes blast radius of any compromise the entire role's permissions.",
            "remediation": "Create dedicated workload identities per agent type. Use AWS AgentCore Identity or similar to manage agent-specific credentials."
        },
        {
            "type": "token_exfiltration",
            "severity": "critical",
            "description": "Access tokens passed as tool arguments appear in application logs, LLM context, and potentially tool outputs — trivially exfiltrated via prompt injection.",
            "remediation": "Never pass tokens as arguments. Use credential providers that inject tokens at the infrastructure level (e.g., IAM roles, service mesh mTLS)."
        },
        {
            "type": "excessive_privilege",
            "severity": "high",
            "description": "Agent can both read databases AND send emails AND execute code — a classic confused deputy setup. A prompt injection reading sensitive data + sending email = instant exfiltration.",
            "remediation": "Scope tool access per agent role. A summarization agent does not need execute_code(). Use separate agents for separate capabilities."
        },
        {
            "type": "missing_identity_propagation",
            "severity": "high",
            "description": "No user identity propagated downstream means all actions appear as agent actions, impossible to enforce user-level policies or reconstruct who caused what.",
            "remediation": "Propagate user identity via OAuth token (OIDC sub claim) or ID-JAG token through all service calls."
        },
        {
            "type": "long_lived_sessions",
            "severity": "medium",
            "description": "24-hour sessions vastly exceed the time needed for any single task. A stolen session token has a 24-hour blast window.",
            "remediation": "Use short-lived tokens (< 15 min). Implement step-up authentication for sensitive operations."
        },
        {
            "type": "prompt_injection_surface",
            "severity": "high",
            "description": "Tool outputs included verbatim in LLM context create prompt injection surface. A malicious document returned by search_web() can hijack agent behavior.",
            "remediation": "Sanitize tool outputs before including in context. Use separate context windows for untrusted content. Apply output validation."
        },
    ]
""",
                "solution_explanation": "Each vulnerability maps to a specific threat class. The shared IAM role and token-as-argument patterns are the most critical because they're trivially exploitable. Identity propagation is essential for audit trails. The combination of database read + email write is a classic confused deputy setup.",
                "hints": [
                    "Think about what happens if a malicious document is returned by search_web()",
                    "Consider what an attacker gains if they can read the application logs",
                    "What is the blast radius if one agent instance is compromised?",
                ]
            }
        ],
        "references": [
            {"title": "OWASP Top 10 for LLM Applications", "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/"},
            {"title": "NIST AI Risk Management Framework", "url": "https://www.nist.gov/system/files/documents/2023/01/26/NIST-AI-RMF-1.0.pdf"},
            {"title": "AWS Security Best Practices for Generative AI", "url": "https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/gen-ai.html"},
        ]
    },
    {
        "id": "ch-02-workload-identity",
        "chapter_num": 2,
        "title": "Workload Identities for AI Agents",
        "subtitle": "AWS AgentCore Identity and the agent identity lifecycle",
        "description": "Deep dive into workload identities — what they are, how AWS AgentCore manages them, and how to create, rotate, and govern agent credentials at enterprise scale.",
        "tags": ["workload-identity", "aws-agentcore", "iam", "credentials"],
        "estimated_minutes": 35,
        "sections": [
            {
                "id": "s2-1",
                "title": "Workload Identities vs. User Identities",
                "blocks": [
                    {"type": "paragraph", "content": "A workload identity represents a non-human entity — a service, a container, a function, or an AI agent — rather than a human user. The key distinction is that workload identities are designed for machine-to-machine authentication without human interaction."},
                    {"type": "paragraph", "content": "Traditional IAM users rely on long-lived credentials (passwords, access keys) that humans manage. Workload identities use short-lived, automatically rotated credentials issued by a trusted authority, typically via federated identity protocols like OIDC or SPIFFE/SPIRE."},
                    {"type": "heading", "level": 3, "content": "Why AI Agents Need Dedicated Workload Identities"},
                    {"type": "bullets", "items": [
                        "Agents may act on behalf of multiple users — their identity must be distinct from any single user",
                        "Agent credentials must be scoped to specific capabilities independent of the user's permissions",
                        "Audit logs must distinguish 'user X via agent Y' from 'user X directly' for compliance",
                        "Agents can be compromised independently of user accounts — blast radius must be isolated",
                        "Multi-cloud deployments need environment-agnostic identity that is not tied to one cloud's IAM system",
                    ]},
                    {"type": "diagram", "title": "Workload Identity vs User Identity Comparison", "content": """┌─────────────────────────────────────────────────────────────────┐
│              User Identity              Workload Identity        │
│                                                                  │
│  Credential type    Password/MFA         Short-lived JWT/token  │
│  Rotation           Manual               Automatic (minutes)    │
│  Tied to            Human person         Service/agent instance │
│  Auth method        Interactive login    Federated/OIDC         │
│  Session length     Hours               Minutes to hours        │
│  Revocation         Account disable      Token expiry + CRL     │
│  Audit context      User actions         Agent+user context     │
└─────────────────────────────────────────────────────────────────┘"""},
                ]
            },
            {
                "id": "s2-2",
                "title": "AWS AgentCore Identity Directory",
                "blocks": [
                    {"type": "paragraph", "content": "AWS Bedrock AgentCore provides a dedicated Identity service that acts as a centralized registry for agent workload identities. Rather than managing agent credentials as ad-hoc IAM users or roles, AgentCore Identity gives each agent a structured identity with rich metadata, lifecycle management, and multi-credential support."},
                    {"type": "heading", "level": 3, "content": "Key Characteristics of AgentCore Workload Identities"},
                    {"type": "bullets", "items": [
                        "Environment-agnostic: Agent identities are not tied to specific infrastructure (Lambda, ECS, EC2) — the same logical agent identity works across deployment environments",
                        "Multi-credential support: A single agent identity can hold multiple credential types (AWS IAM, OIDC tokens, API keys) for different downstream services",
                        "Centralized governance: The AgentCore Identity directory serves as the single source of truth for all agent identities in your organization",
                        "Granular attributes: Identities carry metadata about the agent's role, capabilities, owner team, and allowed actions",
                        "Lifecycle management: Built-in support for credential rotation, suspension, and revocation",
                    ]},
                    {"type": "heading", "level": 3, "content": "The AgentCore Identity Directory Model"},
                    {"type": "paragraph", "content": "The identity directory maintains a registry of all agent identities. Each entry includes the agent's logical name, its associated credentials, the IAM role it assumes for AWS service access, and metadata for governance. This centralized model enables consistent policy enforcement across all agents regardless of where they run."},
                    {"type": "code", "language": "python", "title": "Creating an Agent Workload Identity with boto3", "content": """import boto3
import json

bedrock_agentcore = boto3.client('bedrock-agentcore', region_name='us-east-1')

def create_agent_identity(
    agent_name: str,
    description: str,
    iam_role_arn: str,
    allowed_tools: list[str],
    owner_team: str
) -> dict:
    \"\"\"
    Create a new workload identity for an AI agent in AgentCore Identity directory.

    Args:
        agent_name: Logical name for the agent (e.g., 'document-summarizer-v2')
        description: Human-readable description of the agent's purpose
        iam_role_arn: The IAM role the agent will assume for AWS service access
        allowed_tools: List of MCP tool IDs this agent is permitted to invoke
        owner_team: Team responsible for this agent (for governance)

    Returns:
        The created agent identity record including its workload_identity_id
    \"\"\"
    response = bedrock_agentcore.create_agent_runtime_endpoint(
        agentRuntimeName=agent_name,
        description=description,
        agentRuntimeRoleArn=iam_role_arn,
        tags={
            'owner-team': owner_team,
            'allowed-tools': ','.join(allowed_tools),
            'created-by': 'security-automation',
        }
    )

    identity_id = response['agentRuntimeId']
    print(f"Created agent identity: {identity_id}")
    print(f"Agent ARN: {response['agentRuntimeArn']}")

    return {
        'identity_id': identity_id,
        'arn': response['agentRuntimeArn'],
        'name': agent_name,
        'status': response['status'],
    }


def list_agent_identities(owner_team: str = None) -> list[dict]:
    \"\"\"List all agent identities, optionally filtered by owner team.\"\"\"
    paginator = bedrock_agentcore.get_paginator('list_agent_runtime_endpoints')
    identities = []

    for page in paginator.paginate():
        for identity in page.get('agentRuntimeEndpoints', []):
            if owner_team and identity.get('tags', {}).get('owner-team') != owner_team:
                continue
            identities.append({
                'id': identity['agentRuntimeId'],
                'name': identity['agentRuntimeName'],
                'status': identity['status'],
                'owner': identity.get('tags', {}).get('owner-team', 'unknown'),
            })

    return identities


def rotate_agent_credentials(identity_id: str) -> dict:
    \"\"\"
    Trigger credential rotation for an agent identity.
    New credentials take effect immediately; old credentials are invalidated
    after a configurable grace period.
    \"\"\"
    response = bedrock_agentcore.rotate_agent_runtime_endpoint_secret(
        agentRuntimeId=identity_id
    )
    print(f"Credential rotation initiated for {identity_id}")
    print(f"New credentials effective: {response['rotationTimestamp']}")
    return response
"""},
                    {"type": "callout", "kind": "info", "title": "Service Quotas", "content": "AgentCore Identity has default service quotas: 100 agent identities per account, 10 credentials per identity, and 1000 API calls per second. For large-scale deployments, request quota increases via AWS Support before going to production."},
                ]
            },
            {
                "id": "s2-3",
                "title": "Credential Management & Rotation",
                "blocks": [
                    {"type": "paragraph", "content": "One of the most critical aspects of workload identity management is credential rotation. Unlike user passwords that humans manually change, agent credentials should rotate automatically on a schedule — or immediately after any suspected compromise."},
                    {"type": "heading", "level": 3, "content": "Rotation Strategy"},
                    {"type": "bullets", "items": [
                        "Short-lived tokens (< 15 minutes): Use for all sensitive resource access. These don't need explicit rotation — they expire naturally.",
                        "Medium-lived service credentials (hours): Rotate on every agent deployment. Use AWS Lambda environment variable rotation or Secrets Manager.",
                        "Long-lived identity certificates: Rotate quarterly minimum. Use automated rotation via AWS Certificate Manager or HashiCorp Vault.",
                        "Emergency revocation: Every identity must support immediate revocation without waiting for expiry.",
                    ]},
                    {"type": "code", "language": "python", "title": "Automated Credential Rotation with AWS Secrets Manager", "content": """import boto3
import json
from datetime import datetime, timedelta

secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
bedrock_agentcore = boto3.client('bedrock-agentcore', region_name='us-east-1')

def setup_automatic_rotation(
    agent_identity_id: str,
    secret_name: str,
    rotation_days: int = 1
) -> None:
    \"\"\"
    Configure automatic rotation for an agent's credentials using
    AWS Secrets Manager with a Lambda rotation function.

    The rotation function:
    1. Creates new AgentCore credentials
    2. Validates new credentials work
    3. Updates the secret with new credentials
    4. Revokes old credentials (after grace period)
    \"\"\"
    # Create or update the secret that holds agent credentials
    try:
        secrets_client.create_secret(
            Name=secret_name,
            Description=f'Credentials for AgentCore identity {agent_identity_id}',
            SecretString=json.dumps({
                'agent_identity_id': agent_identity_id,
                'api_key': '',  # Will be populated on first rotation
                'created_at': datetime.utcnow().isoformat(),
            }),
            Tags=[
                {'Key': 'agent-identity-id', 'Value': agent_identity_id},
                {'Key': 'rotation-enabled', 'Value': 'true'},
            ]
        )
    except secrets_client.exceptions.ResourceExistsException:
        pass  # Secret already exists

    # Enable automatic rotation
    secrets_client.rotate_secret(
        SecretId=secret_name,
        RotationRules={
            'AutomaticallyAfterDays': rotation_days,
            'Duration': '2h',  # How long the rotation window stays open
        },
        RotationLambdaARN='arn:aws:lambda:us-east-1:123456789:function:agent-cred-rotator',
        RotateImmediately=True
    )

    print(f"Automatic {rotation_days}-day rotation enabled for agent {agent_identity_id}")


def emergency_revoke_agent(agent_identity_id: str, reason: str) -> None:
    \"\"\"
    Immediately revoke all credentials for an agent identity.
    Use this when compromise is suspected.
    \"\"\"
    # 1. Disable the agent identity immediately
    bedrock_agentcore.update_agent_runtime_endpoint(
        agentRuntimeId=agent_identity_id,
        # Suspend all operations
    )

    # 2. Invalidate all active tokens by rotating credentials
    bedrock_agentcore.rotate_agent_runtime_endpoint_secret(
        agentRuntimeId=agent_identity_id
    )

    # 3. Log the revocation event for audit trail
    cloudwatch = boto3.client('logs')
    cloudwatch.put_log_events(
        logGroupName='/security/agent-identity-events',
        logStreamName='revocations',
        logEvents=[{
            'timestamp': int(datetime.utcnow().timestamp() * 1000),
            'message': json.dumps({
                'event': 'AGENT_IDENTITY_REVOKED',
                'agent_identity_id': agent_identity_id,
                'reason': reason,
                'revoked_at': datetime.utcnow().isoformat(),
                'revoked_by': 'security-automation',
            })
        }]
    )

    print(f"EMERGENCY REVOCATION complete for agent {agent_identity_id}")
    print(f"Reason: {reason}")
"""},
                ]
            },
        ],
        "challenges": [
            {
                "id": "ch02-c1",
                "title": "Agent Identity Registry",
                "difficulty": "Medium",
                "description": "Implement an in-memory agent identity registry that tracks agent identities, their credentials, and enforces rotation policies.",
                "context": "You are building the core identity management layer for an enterprise agentic platform. The registry must track all agent identities, detect when credentials are about to expire, and enforce rotation before they do.",
                "starter_code": """from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid

class CredentialStatus(Enum):
    ACTIVE = "active"
    EXPIRING_SOON = "expiring_soon"  # < 24h remaining
    EXPIRED = "expired"
    REVOKED = "revoked"

@dataclass
class AgentCredential:
    credential_id: str
    agent_identity_id: str
    credential_type: str  # 'api_key', 'oidc_token', 'iam_role'
    value: str
    issued_at: datetime
    expires_at: datetime
    status: CredentialStatus = CredentialStatus.ACTIVE

@dataclass
class AgentIdentity:
    identity_id: str
    name: str
    owner_team: str
    allowed_tools: list[str]
    credentials: list[AgentCredential] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

class AgentIdentityRegistry:
    def __init__(self):
        self._identities: dict[str, AgentIdentity] = {}

    def register(self, name: str, owner_team: str, allowed_tools: list[str]) -> AgentIdentity:
        \"\"\"Register a new agent identity. Return the created identity.\"\"\"
        # TODO: implement
        pass

    def add_credential(self, identity_id: str, cred_type: str, value: str, ttl_hours: int) -> AgentCredential:
        \"\"\"Add a credential to an existing identity with the given TTL.\"\"\"
        # TODO: implement
        pass

    def get_active_credential(self, identity_id: str, cred_type: str) -> AgentCredential | None:
        \"\"\"Return the active (non-expired, non-revoked) credential of given type.\"\"\"
        # TODO: implement
        pass

    def find_expiring_soon(self, within_hours: int = 24) -> list[tuple[AgentIdentity, AgentCredential]]:
        \"\"\"Return all (identity, credential) pairs expiring within the given window.\"\"\"
        # TODO: implement
        pass

    def revoke(self, identity_id: str) -> None:
        \"\"\"Revoke all credentials and deactivate the identity.\"\"\"
        # TODO: implement
        pass

    def audit_report(self) -> dict:
        \"\"\"Return a summary: total identities, active, revoked, credentials expiring soon.\"\"\"
        # TODO: implement
        pass
""",
                "solution_code": """from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid

class CredentialStatus(Enum):
    ACTIVE = "active"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"
    REVOKED = "revoked"

@dataclass
class AgentCredential:
    credential_id: str
    agent_identity_id: str
    credential_type: str
    value: str
    issued_at: datetime
    expires_at: datetime
    status: CredentialStatus = CredentialStatus.ACTIVE

@dataclass
class AgentIdentity:
    identity_id: str
    name: str
    owner_team: str
    allowed_tools: list[str]
    credentials: list[AgentCredential] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

class AgentIdentityRegistry:
    def __init__(self):
        self._identities: dict[str, AgentIdentity] = {}

    def register(self, name: str, owner_team: str, allowed_tools: list[str]) -> AgentIdentity:
        identity = AgentIdentity(
            identity_id=str(uuid.uuid4()),
            name=name,
            owner_team=owner_team,
            allowed_tools=allowed_tools,
        )
        self._identities[identity.identity_id] = identity
        return identity

    def add_credential(self, identity_id: str, cred_type: str, value: str, ttl_hours: int) -> AgentCredential:
        identity = self._identities[identity_id]
        now = datetime.utcnow()
        cred = AgentCredential(
            credential_id=str(uuid.uuid4()),
            agent_identity_id=identity_id,
            credential_type=cred_type,
            value=value,
            issued_at=now,
            expires_at=now + timedelta(hours=ttl_hours),
        )
        identity.credentials.append(cred)
        return cred

    def get_active_credential(self, identity_id: str, cred_type: str) -> AgentCredential | None:
        identity = self._identities.get(identity_id)
        if not identity or not identity.is_active:
            return None
        now = datetime.utcnow()
        for cred in identity.credentials:
            if (cred.credential_type == cred_type
                    and cred.status not in (CredentialStatus.REVOKED, CredentialStatus.EXPIRED)
                    and cred.expires_at > now):
                return cred
        return None

    def find_expiring_soon(self, within_hours: int = 24) -> list[tuple[AgentIdentity, AgentCredential]]:
        threshold = datetime.utcnow() + timedelta(hours=within_hours)
        now = datetime.utcnow()
        results = []
        for identity in self._identities.values():
            for cred in identity.credentials:
                if (cred.status == CredentialStatus.ACTIVE
                        and now < cred.expires_at <= threshold):
                    cred.status = CredentialStatus.EXPIRING_SOON
                    results.append((identity, cred))
        return results

    def revoke(self, identity_id: str) -> None:
        identity = self._identities[identity_id]
        identity.is_active = False
        for cred in identity.credentials:
            cred.status = CredentialStatus.REVOKED

    def audit_report(self) -> dict:
        now = datetime.utcnow()
        total = len(self._identities)
        active = sum(1 for i in self._identities.values() if i.is_active)
        revoked = total - active
        expiring_soon = len(self.find_expiring_soon(24))
        all_creds = [c for i in self._identities.values() for c in i.credentials]
        expired_creds = sum(1 for c in all_creds if c.expires_at <= now and c.status != CredentialStatus.REVOKED)
        return {
            "total_identities": total,
            "active_identities": active,
            "revoked_identities": revoked,
            "credentials_expiring_24h": expiring_soon,
            "expired_credentials": expired_creds,
            "total_credentials": len(all_creds),
        }
""",
                "solution_explanation": "The registry uses an in-memory dict keyed by identity_id. Credential expiry is checked at query time (lazy evaluation). find_expiring_soon also updates status to EXPIRING_SOON as a side effect, which is intentional — it keeps status current. The audit_report method calls find_expiring_soon to force status refresh before counting.",
                "hints": [
                    "For get_active_credential, check both status and expires_at — a credential can be technically not-revoked but still expired",
                    "find_expiring_soon should update credential status as a side effect",
                    "revoke() must deactivate the identity AND mark all credentials as revoked",
                ]
            }
        ],
        "references": [
            {"title": "AWS AgentCore: Understanding Workload Identities", "url": "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-manage-agent-ids.html"},
            {"title": "SPIFFE: Secure Production Identity Framework for Everyone", "url": "https://spiffe.io/"},
            {"title": "AWS IAM Roles for Workloads", "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html"},
        ]
    },
    {
        "id": "ch-03-agentcore-mcp",
        "chapter_num": 3,
        "title": "AWS AgentCore MCP Gateway",
        "subtitle": "Using AgentCore as the identity boundary for MCP tool access",
        "description": "Explore how AWS AgentCore MCP Gateway acts as the central authentication and authorization point for all MCP server access in an enterprise agentic platform — including the enterprise reference architecture combining Okta, AgentCore, and downstream services.",
        "tags": ["aws-agentcore", "mcp-gateway", "pat", "enterprise-architecture"],
        "estimated_minutes": 40,
        "sections": [
            {
                "id": "s3-1",
                "title": "AgentCore MCP Gateway Architecture",
                "blocks": [
                    {"type": "paragraph", "content": "The AWS AgentCore MCP Gateway is a managed proxy that sits between AI agents and MCP servers. Rather than allowing agents to call MCP servers directly, all tool invocations flow through the gateway, which enforces authentication, authorization, and audit logging at a single control point."},
                    {"type": "paragraph", "content": "This architecture is critical for enterprise deployments because it centralizes all the security controls that would otherwise need to be implemented independently in each MCP server — token validation, rate limiting, access logging, and identity context injection."},
                    {"type": "diagram", "title": "Enterprise Agentic Platform: Full Architecture", "content": """┌──────────────────────────────────────────────────────────────────────────────┐
│                        Enterprise Agentic Platform                           │
│                                                                              │
│  ┌─────────────┐    ┌──────────────┐                                        │
│  │ Okta / LDAP │    │  Pharos App  │──── API Key for Metriced access        │
│  │    Login    │───▶│  (Internal)  │──── Solas Log access via LDAP perms    │
│  └─────────────┘    └──────────────┘                                        │
│         │                  │                                                 │
│         │            Personal Access                                         │
│         │            Token (PAT)                                             │
│         │                  │                                                 │
│  ┌──────┴──────┐           │      ┌─────────────────────┐                  │
│  │    User     │           │      │  AgentCore MCP      │                  │
│  │  Identity   │───────────┴─────▶│  Gateway VPC        │                  │
│  └─────────────┘                  └──────────┬──────────┘                  │
│  ┌─────────────┐                             │                              │
│  │    Agent    │                             │                              │
│  │  Identity   │─────────────────────────────┘                             │
│  └─────────────┘                             │                              │
│                                              ▼                              │
│                                   ┌──────────────────┐                     │
│                                   │  Scout VPC        │                     │
│                                   │                  │                     │
│                                   │  ┌─────────────┐ │                     │
│                                   │  │ Scout MCP   │ │                     │
│                                   │  │   Server    │ │                     │
│                                   │  └──────┬──────┘ │                     │
│                                   │         │        │                     │
│                                   │  ┌──────▼──────┐ │                     │
│                                   │  │   Scout     │ │                     │
│                                   │  │ Data Access │ │                     │
│                                   │  │  Svc Acct   │ │                     │
│                                   │  └──────┬──────┘ │                     │
│                                   └─────────┼────────┘                     │
│                                             │                              │
│                                             ▼                              │
│                                   ┌──────────────────┐                     │
│                                   │   Solas-Logs DB  │                     │
│                                   │                  │                     │
│                                   │ (User/Agent +    │                     │
│                                   │  Service Identity│                     │
│                                   │  based authZ)    │                     │
│                                   └──────────────────┘                     │
└──────────────────────────────────────────────────────────────────────────────┘"""},
                    {"type": "paragraph", "content": "This architecture from a real enterprise deployment illustrates several key patterns. Users authenticate via Okta/LDAP to obtain a session. The Pharos application obtains a Personal Access Token that the agent uses to authenticate to the AgentCore MCP Gateway. The gateway sits in its own VPC (AgentCore MCP Gateway VPC) and acts as the sole ingress point for all tool calls. Downstream, the Scout MCP Server runs in a separate Scout VPC, and access to the Solas-Logs database is controlled by a combination of User Identity, Agent Identity, and Service Identity (the Scout Data Access Service Account)."},
                ]
            },
            {
                "id": "s3-2",
                "title": "Personal Access Tokens (PAT) for Agent Authentication",
                "blocks": [
                    {"type": "paragraph", "content": "Personal Access Tokens are a common mechanism for agent-to-gateway authentication, particularly in enterprise environments that already use PATs for CI/CD and service accounts. For agentic use, PATs must be treated as machine credentials — short-lived, scoped, and never exposed in logs or LLM context."},
                    {"type": "heading", "level": 3, "content": "PAT Scoping for Agents"},
                    {"type": "paragraph", "content": "Unlike user-generated PATs that often have broad scopes (read all repos, manage issues), agent PATs should be scoped to the minimum set of capabilities the agent needs. In the reference architecture, the Pharos App generates a PAT scoped specifically to MCP Gateway access — not to the underlying Solas database or Scout service directly."},
                    {"type": "code", "language": "python", "title": "Agent PAT Management — Generation and Injection", "content": """import boto3
import secrets
import hashlib
import time
from typing import Optional

class AgentPATManager:
    \"\"\"
    Manages Personal Access Tokens for agent authentication to MCP Gateway.
    PATs are stored in AWS Secrets Manager and injected into agents at runtime.
    \"\"\"

    def __init__(self, region: str = 'us-east-1'):
        self.secrets_client = boto3.client('secretsmanager', region_name=region)
        self.token_prefix = 'agp_'  # Agent Gateway PAT prefix (never 'ghp_' or user tokens)

    def generate_pat(
        self,
        agent_name: str,
        scopes: list[str],
        ttl_seconds: int = 3600,  # 1 hour default
    ) -> dict:
        \"\"\"
        Generate a new scoped PAT for an agent.

        Args:
            agent_name: Logical name of the agent (for audit trail)
            scopes: List of MCP tool scopes this PAT allows
                    e.g., ['mcp:logs:read', 'mcp:metrics:read']
            ttl_seconds: Token lifetime in seconds (max 86400 = 24h)

        Returns:
            {'token': '...', 'token_id': '...', 'expires_at': timestamp}
        \"\"\"
        # Generate cryptographically secure random token
        raw_token = secrets.token_urlsafe(32)
        token = f"{self.token_prefix}{raw_token}"

        # Hash for storage (never store raw tokens)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        token_id = f"pat_{agent_name}_{int(time.time())}"

        expires_at = int(time.time()) + ttl_seconds

        # Store token metadata (NOT the raw token) in Secrets Manager
        self.secrets_client.create_secret(
            Name=f"/agents/pats/{token_id}",
            SecretString={
                'token_hash': token_hash,
                'agent_name': agent_name,
                'scopes': scopes,
                'expires_at': expires_at,
                'created_at': int(time.time()),
            },
        )

        # Return raw token ONCE — caller must inject into agent runtime
        # Never log this token, never store it unencrypted
        return {
            'token': token,          # Raw token — inject into agent env vars
            'token_id': token_id,    # Reference ID for revocation/audit
            'scopes': scopes,
            'expires_at': expires_at,
        }

    def validate_pat(self, token: str, required_scope: str) -> Optional[dict]:
        \"\"\"
        Validate a PAT at the MCP Gateway.
        Returns token metadata if valid, None if invalid.
        \"\"\"
        if not token.startswith(self.token_prefix):
            return None  # Not an agent PAT

        token_hash = hashlib.sha256(token.encode()).hexdigest()

        # Look up token by hash (scan — in production, use token_id + hash index)
        # This is simplified — production uses Redis or DynamoDB for O(1) lookup
        try:
            # In practice, the token_id is passed alongside the token in the header
            # e.g., Authorization: AgentPAT {token_id}:{token}
            secret_value = self.secrets_client.get_secret_value(
                SecretId=f"/agents/pats/lookup/{token_hash}"
            )
            metadata = secret_value['SecretString']
        except self.secrets_client.exceptions.ResourceNotFoundException:
            return None  # Token not found

        # Check expiry
        if metadata['expires_at'] < int(time.time()):
            return None  # Expired

        # Check scope
        if required_scope not in metadata['scopes']:
            return None  # Insufficient scope

        return metadata

    def inject_pat_into_lambda(
        self,
        function_name: str,
        agent_name: str,
        scopes: list[str]
    ) -> None:
        \"\"\"
        Generate a PAT and inject it into a Lambda function's environment
        variables. The Lambda never sees the generation process.
        \"\"\"
        pat_data = self.generate_pat(agent_name, scopes, ttl_seconds=3600)

        lambda_client = boto3.client('lambda')
        # Get current config
        current_config = lambda_client.get_function_configuration(FunctionName=function_name)
        current_env = current_config.get('Environment', {}).get('Variables', {})

        # Inject PAT — it will be available as os.environ['MCP_GATEWAY_PAT']
        current_env['MCP_GATEWAY_PAT'] = pat_data['token']
        current_env['MCP_GATEWAY_PAT_ID'] = pat_data['token_id']
        current_env['MCP_GATEWAY_PAT_EXPIRES'] = str(pat_data['expires_at'])

        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Environment={'Variables': current_env}
        )

        print(f"PAT injected into {function_name}, expires at {pat_data['expires_at']}")
        print("WARNING: Token is now in Lambda environment — ensure CloudTrail is monitoring")
"""},
                    {"type": "callout", "kind": "warning", "title": "PAT Security Anti-Patterns", "content": "Never hardcode PATs in source code. Never log PATs at any log level. Never include PATs in error messages or stack traces. Never return PATs in API responses. Never include PATs in LLM prompts. Use AWS Secrets Manager or environment variable injection exclusively."},
                ]
            },
            {
                "id": "s3-3",
                "title": "VPC Isolation and Network Security",
                "blocks": [
                    {"type": "paragraph", "content": "The reference architecture places the AgentCore MCP Gateway in its own dedicated VPC, separate from the Scout MCP Server VPC. This VPC isolation ensures that even if a component in the Scout VPC is compromised, an attacker cannot directly reach the gateway or other services — they must traverse the explicit VPC peering with its associated security groups and NACLs."},
                    {"type": "code", "language": "python", "title": "VPC Security Group Configuration for MCP Gateway", "content": """import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

def configure_mcp_gateway_security(
    gateway_vpc_id: str,
    scout_vpc_cidr: str,
    agent_subnet_cidrs: list[str]
) -> dict:
    \"\"\"
    Configure security groups for the AgentCore MCP Gateway VPC.

    Rules:
    - Inbound: Only from agent subnets on port 443 (HTTPS/MCP)
    - Outbound: Only to Scout VPC CIDR on port 443
    - No direct internet access (all traffic via NAT Gateway)
    \"\"\"
    # Create security group for MCP Gateway
    sg_response = ec2.create_security_group(
        GroupName='agentcore-mcp-gateway-sg',
        Description='Security group for AgentCore MCP Gateway — controls who can reach gateway',
        VpcId=gateway_vpc_id,
        TagSpecifications=[{
            'ResourceType': 'security-group',
            'Tags': [
                {'Key': 'Name', 'Value': 'agentcore-mcp-gateway-sg'},
                {'Key': 'Purpose', 'Value': 'mcp-gateway-inbound-control'},
            ]
        }]
    )
    sg_id = sg_response['GroupId']

    # Inbound rules: only agent subnets can reach the gateway
    inbound_rules = []
    for cidr in agent_subnet_cidrs:
        inbound_rules.append({
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': cidr, 'Description': 'Agent subnet — HTTPS/MCP only'}]
        })

    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=inbound_rules
    )

    # Outbound rules: only to Scout VPC on port 443
    ec2.authorize_security_group_egress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': scout_vpc_cidr, 'Description': 'Scout VPC — MCP downstream'}]
        }]
    )

    # Revoke default outbound all-traffic rule
    ec2.revoke_security_group_egress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': '-1',  # All traffic
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
    )

    print(f"MCP Gateway security group configured: {sg_id}")
    print(f"  Inbound: {len(agent_subnet_cidrs)} agent subnets → port 443")
    print(f"  Outbound: Scout VPC ({scout_vpc_cidr}) → port 443 only")
    print(f"  All other traffic: DENY")

    return {'security_group_id': sg_id}
"""},
                ]
            },
        ],
        "challenges": [
            {
                "id": "ch03-c1",
                "title": "MCP Gateway Request Validator",
                "difficulty": "Medium",
                "description": "Implement a request validation middleware for the MCP Gateway that validates PATs, checks scopes, enforces rate limits, and attaches identity context to forwarded requests.",
                "context": "The MCP Gateway receives requests from agents. Each request has an Authorization header with a PAT. Before forwarding to the Scout MCP Server, the gateway must validate the token, check the requested tool is in the token's allowed scopes, enforce per-agent rate limits, and attach the full identity context (user+agent) as headers.",
                "starter_code": """from dataclasses import dataclass
from collections import defaultdict
import time

@dataclass
class GatewayRequest:
    pat_token: str
    tool_name: str
    tool_args: dict
    user_identity_token: str  # OIDC token from user session

@dataclass
class ForwardedRequest:
    tool_name: str
    tool_args: dict
    headers: dict  # Identity context injected by gateway

class MCPGatewayValidator:
    def __init__(self, rate_limit_per_minute: int = 60):
        self.rate_limit = rate_limit_per_minute
        # Simplified token store: token_hash -> {agent_name, scopes, expires_at}
        self._tokens: dict[str, dict] = {}
        self._request_counts: dict[str, list] = defaultdict(list)

    def register_token(self, token: str, agent_name: str, scopes: list[str], ttl_seconds: int = 3600):
        \"\"\"Register a token for testing purposes.\"\"\"
        import hashlib
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self._tokens[token_hash] = {
            'agent_name': agent_name,
            'scopes': scopes,
            'expires_at': time.time() + ttl_seconds,
        }

    def validate_and_forward(self, request: GatewayRequest) -> ForwardedRequest:
        \"\"\"
        Validate the request and return a ForwardedRequest with identity context.
        Raise ValueError with descriptive message for any validation failure.
        \"\"\"
        # TODO: implement
        pass

    def _validate_token(self, token: str) -> dict:
        \"\"\"Validate PAT, return metadata. Raise ValueError if invalid.\"\"\"
        # TODO: implement
        pass

    def _check_rate_limit(self, agent_name: str) -> None:
        \"\"\"Enforce per-agent rate limit. Raise ValueError if exceeded.\"\"\"
        # TODO: implement
        pass

    def _extract_user_sub(self, oidc_token: str) -> str:
        \"\"\"
        Extract subject claim from OIDC token (simplified: token is 'sub:value').
        In production this would verify the JWT signature.
        \"\"\"
        # Simplified: token format is 'sub:<subject_value>'
        if oidc_token.startswith('sub:'):
            return oidc_token[4:]
        return 'unknown'
""",
                "solution_code": """from dataclasses import dataclass
from collections import defaultdict
import hashlib
import time

@dataclass
class GatewayRequest:
    pat_token: str
    tool_name: str
    tool_args: dict
    user_identity_token: str

@dataclass
class ForwardedRequest:
    tool_name: str
    tool_args: dict
    headers: dict

class MCPGatewayValidator:
    def __init__(self, rate_limit_per_minute: int = 60):
        self.rate_limit = rate_limit_per_minute
        self._tokens: dict[str, dict] = {}
        self._request_counts: dict[str, list] = defaultdict(list)

    def register_token(self, token: str, agent_name: str, scopes: list[str], ttl_seconds: int = 3600):
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self._tokens[token_hash] = {
            'agent_name': agent_name,
            'scopes': scopes,
            'expires_at': time.time() + ttl_seconds,
        }

    def validate_and_forward(self, request: GatewayRequest) -> ForwardedRequest:
        # Step 1: Validate PAT
        token_meta = self._validate_token(request.pat_token)
        agent_name = token_meta['agent_name']

        # Step 2: Check scope
        required_scope = f"mcp:tool:{request.tool_name}"
        wildcard_scope = "mcp:tool:*"
        if required_scope not in token_meta['scopes'] and wildcard_scope not in token_meta['scopes']:
            raise ValueError(
                f"Token scope insufficient: tool '{request.tool_name}' requires scope "
                f"'{required_scope}' but token only has {token_meta['scopes']}"
            )

        # Step 3: Rate limiting
        self._check_rate_limit(agent_name)

        # Step 4: Extract user identity
        user_sub = self._extract_user_sub(request.user_identity_token)

        # Step 5: Build forwarded request with identity context headers
        return ForwardedRequest(
            tool_name=request.tool_name,
            tool_args=request.tool_args,
            headers={
                'X-Agent-Identity': agent_name,
                'X-User-Identity': user_sub,
                'X-Identity-Context': f"user={user_sub};agent={agent_name}",
                'X-Request-Timestamp': str(int(time.time())),
                'X-Token-Scopes': ','.join(token_meta['scopes']),
                # Never forward the raw PAT
            }
        )

    def _validate_token(self, token: str) -> dict:
        if not token:
            raise ValueError("Missing PAT token")
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        meta = self._tokens.get(token_hash)
        if not meta:
            raise ValueError("Invalid PAT: token not found")
        if meta['expires_at'] < time.time():
            raise ValueError("Invalid PAT: token has expired")
        return meta

    def _check_rate_limit(self, agent_name: str) -> None:
        now = time.time()
        window_start = now - 60  # 1-minute sliding window
        # Remove requests outside the window
        self._request_counts[agent_name] = [
            t for t in self._request_counts[agent_name] if t > window_start
        ]
        if len(self._request_counts[agent_name]) >= self.rate_limit:
            raise ValueError(
                f"Rate limit exceeded for agent '{agent_name}': "
                f"{self.rate_limit} requests/minute"
            )
        self._request_counts[agent_name].append(now)

    def _extract_user_sub(self, oidc_token: str) -> str:
        if oidc_token.startswith('sub:'):
            return oidc_token[4:]
        return 'unknown'
""",
                "solution_explanation": "The validator follows a strict order: authenticate (PAT validation), authorize (scope check), rate-limit, then enrich (add identity headers). The sliding window rate limiter uses a list of timestamps and trims it on each request. The forwarded request never includes the raw PAT — only derived identity context headers.",
                "hints": [
                    "Scope checking: consider supporting wildcard scopes like 'mcp:tool:*' for admin agents",
                    "Rate limiting: use a sliding window (list of timestamps) rather than a fixed counter",
                    "Never forward the raw PAT in outgoing headers to the MCP server",
                ]
            }
        ],
        "references": [
            {"title": "AWS AgentCore Identity: Manage Workload Identities", "url": "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-manage-agent-ids.html"},
            {"title": "Securing Serverless AI Agents and MCP Servers on AWS with Okta", "url": "https://www.okta.com/blog/ai/securing-serverless-ai-agents-and-mcp-servers-on-aws-with-okta/"},
            {"title": "Model Context Protocol Specification", "url": "https://modelcontextprotocol.io/specification"},
        ]
    },
    {
        "id": "ch-04-oauth-oidc",
        "chapter_num": 4,
        "title": "OAuth 2.0 & OIDC for Agentic Systems",
        "subtitle": "Token-based authentication and authorization flows for AI agents",
        "description": "Master OAuth 2.0 flows adapted for agentic systems, OIDC token structure and validation, token lifecycle management for long-running agents, and the emerging Identity Assertion Grant standard.",
        "tags": ["oauth2", "oidc", "jwt", "token-validation", "id-jag"],
        "estimated_minutes": 45,
        "sections": [
            {
                "id": "s4-1",
                "title": "OAuth 2.0 Flows for Agents",
                "blocks": [
                    {"type": "paragraph", "content": "OAuth 2.0 defines several authorization flows ('grants') for different client types. For AI agents, the choice of grant type depends on whether the agent acts on behalf of a user or as an autonomous system service."},
                    {"type": "heading", "level": 3, "content": "Client Credentials Grant (Agent-as-Service)"},
                    {"type": "paragraph", "content": "When an agent acts as an autonomous service without a human user context, use the Client Credentials grant. The agent authenticates directly with the authorization server using its client_id and client_secret (or a signed JWT assertion), and receives an access token scoped to the agent's allowed capabilities."},
                    {"type": "code", "language": "python", "title": "Client Credentials Grant for Autonomous Agent", "content": """import httpx
import time
from typing import Optional

class AgentTokenProvider:
    \"\"\"
    Obtains and caches OAuth 2.0 access tokens for an autonomous agent
    using the Client Credentials grant flow.
    \"\"\"

    def __init__(
        self,
        token_endpoint: str,
        client_id: str,
        client_secret: str,
        scopes: list[str],
    ):
        self.token_endpoint = token_endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self._cached_token: Optional[str] = None
        self._token_expiry: float = 0
        self._refresh_buffer_seconds = 60  # Refresh 60s before expiry

    def get_token(self) -> str:
        \"\"\"
        Return a valid access token, fetching a new one if needed.
        Implements proactive refresh to avoid token expiry mid-request.
        \"\"\"
        if self._should_refresh():
            self._fetch_new_token()
        return self._cached_token

    def _should_refresh(self) -> bool:
        if self._cached_token is None:
            return True
        # Refresh before actual expiry to avoid race conditions
        return time.time() >= (self._token_expiry - self._refresh_buffer_seconds)

    def _fetch_new_token(self) -> None:
        response = httpx.post(
            self.token_endpoint,
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': ' '.join(self.scopes),
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10.0,
        )
        response.raise_for_status()
        token_data = response.json()

        self._cached_token = token_data['access_token']
        # Cache with expiry — subtract buffer
        self._token_expiry = time.time() + token_data.get('expires_in', 3600)

        print(f"New token obtained, expires in {token_data.get('expires_in')}s")
        print(f"Token type: {token_data.get('token_type')}")
        print(f"Scopes granted: {token_data.get('scope', 'not specified')}")
"""},
                    {"type": "heading", "level": 3, "content": "Authorization Code + PKCE (Agent Acting on Behalf of User)"},
                    {"type": "paragraph", "content": "When an agent needs to act on behalf of a specific user (e.g., the user authorizes the agent to access their data), use Authorization Code with PKCE. The user authenticates interactively once, and the agent receives a refresh token it can use to obtain short-lived access tokens throughout the session."},
                    {"type": "callout", "kind": "info", "title": "Refresh Token Strategy for Long-Running Agents", "content": "Long-running agents must handle token expiry gracefully. Store refresh tokens in AWS Secrets Manager (not environment variables). Implement proactive refresh — fetch a new access token 60 seconds before expiry. Never let an access token expire mid-task, as this can leave downstream systems in inconsistent state."},
                ]
            },
            {
                "id": "s4-2",
                "title": "OIDC Token Validation — Defense in Depth",
                "blocks": [
                    {"type": "paragraph", "content": "Every service that receives a request from an agent must independently validate the identity token. Relying on upstream services to have validated the token is a critical security mistake — a compromised intermediary can forward arbitrary tokens."},
                    {"type": "heading", "level": 3, "content": "The 6 Claims You Must Always Validate"},
                    {"type": "bullets", "items": [
                        "iss (issuer): Must exactly match your expected identity provider URL. Reject tokens from unexpected issuers even if the signature is valid.",
                        "aud (audience): Must include your service's identifier. Prevents token replay attacks where a valid token for Service A is replayed against Service B.",
                        "exp (expiration): Must be in the future. Use server time, not client-provided time. Reject with <5 second clock skew tolerance.",
                        "iat (issued at): Should be recent. Reject tokens issued too far in the past even if exp is still valid.",
                        "sub (subject): The identity of the agent or user. Must be in your allow-list for sensitive operations.",
                        "scope / scp: The permissions granted. Verify the token has the specific scope required for this operation — not just any scope.",
                    ]},
                    {"type": "code", "language": "python", "title": "Production JWT Validation with Full Claim Checking", "content": """import time
import httpx
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from functools import lru_cache

class OIDCTokenValidator:
    \"\"\"
    Production-grade OIDC/JWT validator for MCP server endpoints.
    Validates signature, claims, and scope for every incoming request.
    \"\"\"

    def __init__(
        self,
        issuer: str,
        audience: str,
        clock_skew_seconds: int = 5,
    ):
        self.issuer = issuer  # e.g., 'https://your-okta-domain.okta.com/oauth2/default'
        self.audience = audience  # e.g., 'api://mcp-server'
        self.clock_skew = clock_skew_seconds
        self._jwks_cache: dict = {}
        self._jwks_fetched_at: float = 0
        self._jwks_ttl: int = 3600  # Refresh JWKS hourly

    def validate(self, token: str, required_scope: str) -> dict:
        \"\"\"
        Fully validate a JWT token. Returns decoded claims if valid.
        Raises ValueError with descriptive message on any failure.

        This method is designed to be used at every service boundary —
        never skip validation because 'upstream already checked it'.
        \"\"\"
        if not token or not token.startswith('Bearer '):
            # Also accept raw token (for internal service calls)
            raw_token = token.replace('Bearer ', '') if token else ''
        else:
            raw_token = token[7:]  # Strip 'Bearer ' prefix

        if not raw_token:
            raise ValueError("UNAUTHORIZED: Missing authentication token")

        # Step 1: Decode header to find key ID (kid)
        try:
            unverified_header = jwt.get_unverified_header(raw_token)
        except JWTError as e:
            raise ValueError(f"UNAUTHORIZED: Malformed token header: {e}")

        # Step 2: Fetch JWKS and find the signing key
        jwks = self._get_jwks()
        signing_key = self._find_signing_key(jwks, unverified_header.get('kid'))

        # Step 3: Verify signature and decode claims
        try:
            claims = jwt.decode(
                raw_token,
                signing_key,
                algorithms=['RS256', 'ES256'],
                audience=self.audience,
                issuer=self.issuer,
                options={
                    'verify_exp': True,
                    'verify_iat': True,
                    'verify_iss': True,
                    'verify_aud': True,
                    'leeway': self.clock_skew,
                }
            )
        except ExpiredSignatureError:
            raise ValueError("UNAUTHORIZED: Token has expired")
        except JWTClaimsError as e:
            raise ValueError(f"UNAUTHORIZED: Invalid token claims: {e}")
        except JWTError as e:
            raise ValueError(f"UNAUTHORIZED: Token validation failed: {e}")

        # Step 4: Validate scope (not handled by jose.jwt.decode)
        token_scopes = claims.get('scp', claims.get('scope', '')).split()
        if required_scope not in token_scopes:
            raise ValueError(
                f"FORBIDDEN: Token missing required scope '{required_scope}'. "
                f"Token has: {token_scopes}"
            )

        # Step 5: Validate iat is not too old (defense against long-delayed replay)
        iat = claims.get('iat', 0)
        max_token_age = 3600  # Reject tokens > 1 hour old even if exp is valid
        if time.time() - iat > max_token_age:
            raise ValueError(f"UNAUTHORIZED: Token is too old (issued {int(time.time()-iat)}s ago)")

        return claims

    def _get_jwks(self) -> dict:
        \"\"\"Fetch JWKS from identity provider with caching.\"\"\"
        now = time.time()
        if now - self._jwks_fetched_at < self._jwks_ttl and self._jwks_cache:
            return self._jwks_cache

        jwks_uri = f"{self.issuer}/.well-known/jwks.json"
        response = httpx.get(jwks_uri, timeout=5.0)
        response.raise_for_status()

        self._jwks_cache = response.json()
        self._jwks_fetched_at = now
        return self._jwks_cache

    def _find_signing_key(self, jwks: dict, kid: str) -> dict:
        \"\"\"Find the signing key matching the token's kid.\"\"\"
        for key in jwks.get('keys', []):
            if key.get('kid') == kid:
                return key
        raise ValueError(f"UNAUTHORIZED: No signing key found for kid='{kid}'")


# Usage at MCP server endpoint
validator = OIDCTokenValidator(
    issuer='https://your-org.okta.com/oauth2/default',
    audience='api://mcp-scout-server',
)

def handle_tool_request(auth_header: str, tool_name: str, tool_args: dict):
    # Validate token and check scope at every endpoint
    claims = validator.validate(
        token=auth_header,
        required_scope=f'mcp:tool:{tool_name}'
    )

    # Now safe to proceed — claims contains verified identity
    user_sub = claims.get('sub')
    agent_name = claims.get('agent_name')  # Custom claim set by gateway

    print(f"Authorized request: user={user_sub}, agent={agent_name}, tool={tool_name}")
    # ... execute tool
"""},
                ]
            },
            {
                "id": "s4-3",
                "title": "Identity Assertion Grant (ID-JAG) — Token Exchange for Agents",
                "blocks": [
                    {"type": "paragraph", "content": "The Identity Assertion Grant (ID-JAG) is an emerging IETF standard (draft) specifically designed for agentic systems. It enables token exchange where an agent can prove it is acting on behalf of a user while presenting its own identity — producing a combined token that downstream services can use to enforce both user-level and agent-level policies."},
                    {"type": "paragraph", "content": "Okta's Cross-App Access (XAA) implements a variant of this pattern. When an agent needs to call a downstream service, it presents its own credential plus the user's OIDC token to Okta's token exchange endpoint. Okta issues an ID-JAG token that encodes both identities and is scoped to the specific downstream audience."},
                    {"type": "diagram", "title": "ID-JAG Token Exchange Flow", "content": """User authenticates → OIDC ID Token (user identity)
        │
        ▼
Agent presents: {
  grant_type: 'urn:ietf:params:oauth:grant-type:id-jag',
  subject_token: <user OIDC token>,
  subject_token_type: 'urn:ietf:params:oauth:token-type:id_token',
  actor_token: <agent credential>,
  actor_token_type: 'urn:ietf:params:oauth:token-type:access_token',
  audience: 'api://scout-mcp-server',
  scope: 'mcp:logs:read'
}
        │
        ▼
Okta issues ID-JAG token with claims: {
  sub: 'user@company.com',        ← original user
  act: { sub: 'agent-scout-v2' }, ← acting agent
  aud: 'api://scout-mcp-server',  ← specific audience (can't replay)
  scope: 'mcp:logs:read',         ← minimal scope
  exp: now + 900                  ← 15 min lifetime
}
        │
        ▼
Scout MCP Server validates ID-JAG:
  ✓ iss = Okta
  ✓ aud = api://scout-mcp-server (exact match)
  ✓ scope includes 'mcp:logs:read'
  ✓ act.sub is authorized agent
  ✓ sub is authorized user
  → Execute tool with (user=sub, agent=act.sub) context"""},
                    {"type": "code", "language": "python", "title": "Implementing ID-JAG Token Exchange with Okta XAA", "content": """import httpx
import os
from typing import Optional

class OktaXAATokenExchange:
    \"\"\"
    Implements Okta Cross-App Access (XAA) / Identity Assertion Grant
    for agent-on-behalf-of-user token exchange.

    Reference: https://www.okta.com/blog/ai/securing-serverless-ai-agents-and-mcp-servers-on-aws-with-okta/
    \"\"\"

    ID_JAG_GRANT_TYPE = 'urn:ietf:params:oauth:grant-type:id-jag'
    ID_TOKEN_TYPE = 'urn:ietf:params:oauth:token-type:id_token'
    ACCESS_TOKEN_TYPE = 'urn:ietf:params:oauth:token-type:access_token'

    def __init__(
        self,
        okta_domain: str,
        authorization_server_id: str,
        agent_client_id: str,
        agent_client_secret: str,
    ):
        self.token_endpoint = (
            f"https://{okta_domain}/oauth2/{authorization_server_id}/v1/token"
        )
        self.agent_client_id = agent_client_id
        self.agent_client_secret = agent_client_secret

    def exchange_for_downstream(
        self,
        user_id_token: str,     # OIDC token from user's session
        agent_access_token: str, # Agent's own OAuth token
        downstream_audience: str, # e.g., 'api://scout-mcp-server'
        required_scopes: list[str], # e.g., ['mcp:logs:read']
    ) -> str:
        \"\"\"
        Exchange user + agent tokens for a downstream-scoped ID-JAG token.

        The resulting token:
        - Is scoped ONLY to downstream_audience (can't be replayed elsewhere)
        - Has both user (sub) and agent (act.sub) identity
        - Has minimal scopes (required_scopes only)
        - Has short lifetime (typically 15 minutes)

        Returns the raw ID-JAG access token string.
        \"\"\"
        response = httpx.post(
            self.token_endpoint,
            auth=(self.agent_client_id, self.agent_client_secret),
            data={
                'grant_type': self.ID_JAG_GRANT_TYPE,
                'subject_token': user_id_token,
                'subject_token_type': self.ID_TOKEN_TYPE,
                'actor_token': agent_access_token,
                'actor_token_type': self.ACCESS_TOKEN_TYPE,
                'audience': downstream_audience,
                'scope': ' '.join(required_scopes),
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10.0,
        )

        if response.status_code != 200:
            error_data = response.json()
            raise ValueError(
                f"Token exchange failed: {error_data.get('error')}: "
                f"{error_data.get('error_description')}"
            )

        token_data = response.json()
        return token_data['access_token']

    def call_mcp_tool_with_exchange(
        self,
        user_id_token: str,
        agent_access_token: str,
        mcp_server_url: str,
        tool_name: str,
        tool_args: dict,
    ) -> dict:
        \"\"\"
        Full flow: exchange tokens then call MCP tool with the resulting ID-JAG token.
        \"\"\"
        # Derive audience from MCP server URL (or use a configured mapping)
        audience = f"api://mcp-server-{mcp_server_url.split('//')[-1].split('.')[0]}"

        # Exchange for a scoped ID-JAG token
        id_jag_token = self.exchange_for_downstream(
            user_id_token=user_id_token,
            agent_access_token=agent_access_token,
            downstream_audience=audience,
            required_scopes=[f'mcp:tool:{tool_name}'],
        )

        # Call MCP tool with ID-JAG token
        response = httpx.post(
            f"{mcp_server_url}/tools/{tool_name}",
            json=tool_args,
            headers={
                'Authorization': f'Bearer {id_jag_token}',
                'Content-Type': 'application/json',
            },
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()
"""},
                ]
            },
        ],
        "challenges": [
            {
                "id": "ch04-c1",
                "title": "JWT Validator with Full Claim Enforcement",
                "difficulty": "Easy",
                "description": "Implement a JWT validator that checks all 6 required claims (iss, aud, exp, iat, sub, scope) and returns structured validation results.",
                "context": "You are building the token validation layer for a MCP server. The server receives JWTs from the AgentCore MCP Gateway. Tokens are pre-signed — your job is to decode and validate claims (no signature verification needed for this challenge; use the provided decode_claims function).",
                "starter_code": """from dataclasses import dataclass
import time

@dataclass
class ValidationResult:
    valid: bool
    claims: dict | None
    error: str | None

def decode_claims(token: str) -> dict:
    \"\"\"
    Simulated JWT decoder — in production this verifies signature.
    For this challenge, tokens are JSON strings encoded as:
    'eyJ<base64-encoded-json>'
    \"\"\"
    import base64, json
    parts = token.split('.')
    if len(parts) < 2:
        raise ValueError("Invalid token format")
    # Pad base64 as needed
    payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))

class MCPTokenValidator:
    def __init__(
        self,
        expected_issuer: str,
        expected_audience: str,
        clock_skew_seconds: int = 5,
        max_token_age_seconds: int = 3600,
    ):
        self.expected_issuer = expected_issuer
        self.expected_audience = expected_audience
        self.clock_skew = clock_skew_seconds
        self.max_token_age = max_token_age_seconds

    def validate(self, token: str, required_scope: str) -> ValidationResult:
        \"\"\"
        Validate all claims. Return ValidationResult.
        Do NOT raise exceptions — return error in ValidationResult.
        \"\"\"
        # TODO: implement
        pass
""",
                "solution_code": """from dataclasses import dataclass
import time, base64, json

@dataclass
class ValidationResult:
    valid: bool
    claims: dict | None
    error: str | None

def decode_claims(token: str) -> dict:
    parts = token.split('.')
    if len(parts) < 2:
        raise ValueError("Invalid token format")
    payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))

class MCPTokenValidator:
    def __init__(self, expected_issuer, expected_audience, clock_skew_seconds=5, max_token_age_seconds=3600):
        self.expected_issuer = expected_issuer
        self.expected_audience = expected_audience
        self.clock_skew = clock_skew_seconds
        self.max_token_age = max_token_age_seconds

    def validate(self, token: str, required_scope: str) -> ValidationResult:
        try:
            claims = decode_claims(token)
        except Exception as e:
            return ValidationResult(valid=False, claims=None, error=f"Token decode failed: {e}")

        now = time.time()

        # 1. Issuer
        if claims.get('iss') != self.expected_issuer:
            return ValidationResult(False, None, f"Invalid issuer: got '{claims.get('iss')}', expected '{self.expected_issuer}'")

        # 2. Audience (aud can be a string or list)
        aud = claims.get('aud', '')
        aud_list = [aud] if isinstance(aud, str) else aud
        if self.expected_audience not in aud_list:
            return ValidationResult(False, None, f"Invalid audience: '{self.expected_audience}' not in {aud_list}")

        # 3. Expiration (with clock skew tolerance)
        exp = claims.get('exp', 0)
        if now > exp + self.clock_skew:
            return ValidationResult(False, None, f"Token expired at {exp} (now={int(now)})")

        # 4. Issued at — not too old
        iat = claims.get('iat', 0)
        if now - iat > self.max_token_age:
            return ValidationResult(False, None, f"Token too old: issued {int(now-iat)}s ago (max {self.max_token_age}s)")

        # 5. Subject must be present
        if not claims.get('sub'):
            return ValidationResult(False, None, "Missing 'sub' claim — cannot identify principal")

        # 6. Scope check
        raw_scope = claims.get('scp', claims.get('scope', ''))
        scopes = raw_scope if isinstance(raw_scope, list) else raw_scope.split()
        if required_scope not in scopes:
            return ValidationResult(False, None, f"Missing required scope '{required_scope}'. Token has: {scopes}")

        return ValidationResult(valid=True, claims=claims, error=None)
""",
                "solution_explanation": "Each claim is validated in a logical order: decode → iss → aud → exp → iat → sub → scope. Returning ValidationResult instead of raising exceptions allows callers to handle errors uniformly. The audience check handles both string and list aud claims. The scope check handles both space-delimited strings and array formats.",
                "hints": [
                    "The 'aud' claim can be either a string or a JSON array — handle both cases",
                    "The 'scp' claim (Okta style) and 'scope' claim (standard) are both common — check both",
                    "Return errors as ValidationResult, not exceptions — this makes logging easier",
                ]
            }
        ],
        "references": [
            {"title": "Okta XAA: Securing Serverless AI Agents on AWS", "url": "https://www.okta.com/blog/ai/securing-serverless-ai-agents-and-mcp-servers-on-aws-with-okta/"},
            {"title": "IETF Draft: Identity Assertion Authorization Grant", "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-chaining/"},
            {"title": "RFC 8693: OAuth 2.0 Token Exchange", "url": "https://datatracker.ietf.org/doc/html/rfc8693"},
            {"title": "OpenID Connect Core 1.0", "url": "https://openid.net/specs/openid-connect-core-1_0.html"},
        ]
    },
    {
        "id": "ch-05-authz",
        "chapter_num": 5,
        "title": "Multi-Layer Authorization Controls",
        "subtitle": "User + Agent + Service Identity-based access control",
        "description": "Implement multi-layered authorization that combines user identity, agent identity, and service account identity to enforce fine-grained access controls across enterprise agentic platforms.",
        "tags": ["authorization", "rbac", "abac", "iam", "service-accounts"],
        "estimated_minutes": 40,
        "sections": [
            {
                "id": "s5-1",
                "title": "The Three Identity Layers",
                "blocks": [
                    {"type": "paragraph", "content": "In the reference architecture (see Chapter 3 diagram), access to the Solas-Logs database is controlled by a combination of three identity layers: User Identity, Agent Identity, and Service Identity (the Scout Data Access Service Account). Each layer provides a different level of authorization granularity."},
                    {"type": "heading", "level": 3, "content": "Layer 1: User Identity"},
                    {"type": "paragraph", "content": "The user identity represents the human who initiated the request (e.g., via Okta/LDAP). User-level authorization enforces 'what data does this user have permission to see?' — regardless of which agent is serving the request. A user with read-only LDAP permissions cannot use an agent to bypass that restriction and write data."},
                    {"type": "heading", "level": 3, "content": "Layer 2: Agent Identity"},
                    {"type": "paragraph", "content": "The agent identity represents the AI system acting on the user's behalf. Agent-level authorization enforces 'what tools and capabilities is this specific agent authorized to use?' — regardless of who the user is. An agent designed for log summarization cannot be used to execute database schema changes, even if the user has that permission."},
                    {"type": "heading", "level": 3, "content": "Layer 3: Service Identity"},
                    {"type": "paragraph", "content": "The service identity is the technical credential that a microservice (like the Scout Data Access Service Account) uses to authenticate to downstream systems. This is the 'last mile' identity — it represents the service itself, not the user or agent. Service-level authorization is a technical guardrail independent of business logic."},
                    {"type": "diagram", "title": "Multi-Layer Authorization Decision Matrix", "content": """Request: User A (data-analyst) via Agent B (log-summarizer) → read logs

┌─────────────────────────────────────────────────────────────────┐
│              Multi-Layer Authorization Check                    │
│                                                                 │
│  Layer 1: User Identity Check                                   │
│  ─────────────────────────                                      │
│  User A role = 'data-analyst'                                   │
│  Data Analyst → can read: logs, metrics                        │
│  Data Analyst → cannot: write, delete, admin                   │
│  Result: ✓ ALLOW (read logs)                                    │
│                                                                 │
│  Layer 2: Agent Identity Check                                  │
│  ──────────────────────────────                                 │
│  Agent B = 'log-summarizer' agent                               │
│  log-summarizer → allowed tools: read_logs, summarize          │
│  log-summarizer → NOT allowed: write_logs, schema_admin        │
│  Result: ✓ ALLOW (read_logs tool in allowed list)              │
│                                                                 │
│  Layer 3: Service Account Check                                 │
│  ──────────────────────────────                                 │
│  Scout Data Access SA → DB permissions: SELECT on logs table   │
│  Scout Data Access SA → cannot: INSERT, UPDATE, DELETE         │
│  Result: ✓ ALLOW (SELECT matches read operation)               │
│                                                                 │
│  FINAL DECISION: ✓ ALLOW                                        │
│  (All three layers must ALLOW — any DENY is a final DENY)       │
└─────────────────────────────────────────────────────────────────┘"""},
                ]
            },
            {
                "id": "s5-2",
                "title": "Implementing Multi-Layer Authorization",
                "blocks": [
                    {"type": "paragraph", "content": "A practical implementation of multi-layer authorization uses a policy engine that evaluates all three layers in sequence. The implementation below shows how this works in Python using a simple RBAC model — in production you would replace the role lookups with calls to an OPA policy engine or AWS Verified Permissions."},
                    {"type": "code", "language": "python", "title": "Multi-Layer Authorization Engine", "content": """from dataclasses import dataclass
from enum import Enum
from typing import Optional

class AuthzDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"

@dataclass
class AuthzContext:
    user_sub: str           # e.g., 'alice@company.com'
    user_roles: list[str]   # e.g., ['data-analyst', 'okta-group-logs']
    agent_id: str           # e.g., 'log-summarizer-v2'
    agent_allowed_tools: list[str]  # e.g., ['read_logs', 'summarize']
    service_account: str    # e.g., 'scout-data-access-sa'
    requested_action: str   # e.g., 'read_logs'
    resource: str           # e.g., 'solas-logs-db/production'

@dataclass
class AuthzResult:
    decision: AuthzDecision
    reason: str
    layer: Optional[str] = None  # Which layer made the decision

# Role-to-permission mappings (in production: OPA/Cedar policy)
USER_ROLE_PERMISSIONS = {
    'data-analyst': ['read_logs', 'read_metrics', 'read_dashboards'],
    'sre': ['read_logs', 'read_metrics', 'read_dashboards', 'write_runbooks'],
    'admin': ['*'],  # Wildcard — can do anything
    'readonly': ['read_logs'],
}

SERVICE_ACCOUNT_PERMISSIONS = {
    'scout-data-access-sa': ['read_logs', 'read_metrics'],
    'scout-write-sa': ['read_logs', 'write_logs', 'read_metrics'],
    'admin-sa': ['*'],
}

class MultiLayerAuthorizationEngine:

    def authorize(self, ctx: AuthzContext) -> AuthzResult:
        \"\"\"
        Evaluate all three authorization layers in sequence.
        Returns DENY if ANY layer denies. All must ALLOW.
        \"\"\"
        # Layer 1: User Identity check
        result = self._check_user_layer(ctx)
        if result.decision == AuthzDecision.DENY:
            return result

        # Layer 2: Agent Identity check
        result = self._check_agent_layer(ctx)
        if result.decision == AuthzDecision.DENY:
            return result

        # Layer 3: Service Account check
        result = self._check_service_layer(ctx)
        if result.decision == AuthzDecision.DENY:
            return result

        return AuthzResult(
            decision=AuthzDecision.ALLOW,
            reason=f"All three authorization layers approved: action='{ctx.requested_action}' "
                   f"user='{ctx.user_sub}' agent='{ctx.agent_id}' sa='{ctx.service_account}'",
        )

    def _check_user_layer(self, ctx: AuthzContext) -> AuthzResult:
        \"\"\"Check if the user's roles permit the requested action.\"\"\"
        allowed_actions = set()
        for role in ctx.user_roles:
            perms = USER_ROLE_PERMISSIONS.get(role, [])
            if '*' in perms:
                return AuthzResult(
                    decision=AuthzDecision.ALLOW,
                    reason=f"User '{ctx.user_sub}' has admin role",
                    layer='user',
                )
            allowed_actions.update(perms)

        if ctx.requested_action not in allowed_actions:
            return AuthzResult(
                decision=AuthzDecision.DENY,
                reason=f"User '{ctx.user_sub}' with roles {ctx.user_roles} "
                       f"is not permitted to '{ctx.requested_action}'. "
                       f"Allowed: {sorted(allowed_actions)}",
                layer='user',
            )
        return AuthzResult(
            decision=AuthzDecision.ALLOW,
            reason=f"User layer approved: '{ctx.user_sub}' → '{ctx.requested_action}'",
            layer='user',
        )

    def _check_agent_layer(self, ctx: AuthzContext) -> AuthzResult:
        \"\"\"Check if the agent's allowed tools include the requested action.\"\"\"
        if '*' in ctx.agent_allowed_tools:
            return AuthzResult(
                decision=AuthzDecision.ALLOW,
                reason=f"Agent '{ctx.agent_id}' has wildcard tool access",
                layer='agent',
            )
        if ctx.requested_action not in ctx.agent_allowed_tools:
            return AuthzResult(
                decision=AuthzDecision.DENY,
                reason=f"Agent '{ctx.agent_id}' is not authorized to use tool "
                       f"'{ctx.requested_action}'. Allowed tools: {ctx.agent_allowed_tools}",
                layer='agent',
            )
        return AuthzResult(
            decision=AuthzDecision.ALLOW,
            reason=f"Agent layer approved: '{ctx.agent_id}' → '{ctx.requested_action}'",
            layer='agent',
        )

    def _check_service_layer(self, ctx: AuthzContext) -> AuthzResult:
        \"\"\"Check if the service account has the required database/resource permissions.\"\"\"
        sa_perms = SERVICE_ACCOUNT_PERMISSIONS.get(ctx.service_account, [])
        if '*' in sa_perms:
            return AuthzResult(
                decision=AuthzDecision.ALLOW,
                reason=f"Service account '{ctx.service_account}' has admin permissions",
                layer='service',
            )
        if ctx.requested_action not in sa_perms:
            return AuthzResult(
                decision=AuthzDecision.DENY,
                reason=f"Service account '{ctx.service_account}' lacks permission for "
                       f"'{ctx.requested_action}' on '{ctx.resource}'. "
                       f"SA permissions: {sa_perms}",
                layer='service',
            )
        return AuthzResult(
            decision=AuthzDecision.ALLOW,
            reason=f"Service layer approved: '{ctx.service_account}' → '{ctx.requested_action}'",
            layer='service',
        )


# Usage example
authz = MultiLayerAuthorizationEngine()

result = authz.authorize(AuthzContext(
    user_sub='alice@company.com',
    user_roles=['data-analyst'],
    agent_id='log-summarizer-v2',
    agent_allowed_tools=['read_logs', 'summarize'],
    service_account='scout-data-access-sa',
    requested_action='read_logs',
    resource='solas-logs-db/production',
))
print(f"Decision: {result.decision.value} — {result.reason}")
# Decision: allow — All three authorization layers approved...
"""},
                ]
            },
        ],
        "challenges": [
            {
                "id": "ch05-c1",
                "title": "Policy Inheritance and Override",
                "difficulty": "Hard",
                "description": "Extend the MultiLayerAuthorizationEngine to support resource-level policies that can override role-level policies, and implement deny-override semantics (an explicit deny always wins).",
                "context": "Your authorization engine needs to handle cases where a resource has explicit deny policies (e.g., a sensitive log table denies all access except from specific agents, even for admin users). Explicit deny must always override allow.",
                "starter_code": """from dataclasses import dataclass, field
from enum import Enum

class PolicyEffect(Enum):
    ALLOW = "allow"
    DENY = "deny"

@dataclass
class Policy:
    effect: PolicyEffect
    principals: list[str]  # user subs, agent ids, or '*'
    actions: list[str]     # actions or '*'
    resources: list[str]   # resource patterns or '*'
    priority: int = 0      # Higher = evaluated first

@dataclass
class PolicyEngine:
    policies: list[Policy] = field(default_factory=list)

    def add_policy(self, policy: Policy) -> None:
        self.policies.append(policy)
        # Keep sorted by priority descending
        self.policies.sort(key=lambda p: p.priority, reverse=True)

    def evaluate(
        self,
        principal: str,  # user sub or agent id
        action: str,
        resource: str
    ) -> tuple[PolicyEffect, str]:
        \"\"\"
        Evaluate all matching policies.

        Rules:
        1. Explicit DENY always wins (deny-override semantics)
        2. If no policy matches, default to DENY (default-deny)
        3. Policies are evaluated in priority order
        4. '*' in principals/actions/resources is a wildcard

        Returns (effect, reason_string)
        \"\"\"
        # TODO: implement
        pass

    def _matches(self, pattern: str, value: str) -> bool:
        \"\"\"Check if a policy field matches a value. '*' is wildcard.\"\"\"
        # TODO: implement
        pass
""",
                "solution_code": """from dataclasses import dataclass, field
from enum import Enum

class PolicyEffect(Enum):
    ALLOW = "allow"
    DENY = "deny"

@dataclass
class Policy:
    effect: PolicyEffect
    principals: list[str]
    actions: list[str]
    resources: list[str]
    priority: int = 0

@dataclass
class PolicyEngine:
    policies: list[Policy] = field(default_factory=list)

    def add_policy(self, policy: Policy) -> None:
        self.policies.append(policy)
        self.policies.sort(key=lambda p: p.priority, reverse=True)

    def evaluate(self, principal: str, action: str, resource: str) -> tuple[PolicyEffect, str]:
        matched_allows = []
        matched_denies = []

        for policy in self.policies:
            principal_match = any(self._matches(p, principal) for p in policy.principals)
            action_match = any(self._matches(a, action) for a in policy.actions)
            resource_match = any(self._matches(r, resource) for r in policy.resources)

            if principal_match and action_match and resource_match:
                if policy.effect == PolicyEffect.DENY:
                    matched_denies.append(policy)
                else:
                    matched_allows.append(policy)

        # Deny-override: any explicit deny wins immediately
        if matched_denies:
            reasons = '; '.join(
                f"explicit DENY (priority={p.priority}): "
                f"principals={p.principals} actions={p.actions} resources={p.resources}"
                for p in matched_denies
            )
            return (PolicyEffect.DENY, f"Explicit deny policy matched: {reasons}")

        # Allow if any allow policy matched
        if matched_allows:
            best = matched_allows[0]  # Highest priority
            return (
                PolicyEffect.ALLOW,
                f"ALLOW policy matched (priority={best.priority}): "
                f"principal='{principal}' action='{action}' resource='{resource}'"
            )

        # Default deny
        return (PolicyEffect.DENY, f"No matching ALLOW policy for principal='{principal}' action='{action}' resource='{resource}'. Default deny.")

    def _matches(self, pattern: str, value: str) -> bool:
        if pattern == '*':
            return True
        if pattern.endswith('*'):
            return value.startswith(pattern[:-1])
        return pattern == value
""",
                "solution_explanation": "The key insight is deny-override: collect ALL matching policies first, then if any are DENY, return DENY regardless of any ALLOW matches. The _matches method handles wildcards including prefix wildcards (e.g., 'resource:logs:*' matches 'resource:logs:production'). Default deny means no explicit allow = denied.",
                "hints": [
                    "Collect all matching policies first, then apply deny-override — don't short-circuit on first match",
                    "A wildcard '*' in principals means 'any principal including anonymous'",
                    "Consider prefix wildcards: 'logs:*' should match 'logs:production' and 'logs:staging'",
                ]
            }
        ],
        "references": [
            {"title": "AWS Verified Permissions — Cedar Policy Language", "url": "https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/cedar-policy-language.html"},
            {"title": "Open Policy Agent (OPA)", "url": "https://www.openpolicyagent.org/docs/latest/"},
            {"title": "NIST RBAC Standard", "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final"},
        ]
    },
    {
        "id": "ch-06-observability",
        "chapter_num": 6,
        "title": "Observability & Audit Logging for Agents",
        "subtitle": "Structured logging, CloudWatch, X-Ray, and immutable audit trails",
        "description": "Build comprehensive observability for enterprise agentic platforms — structured event logging at every service boundary, distributed tracing with AWS X-Ray, and immutable audit trails that satisfy compliance requirements.",
        "tags": ["observability", "audit-logging", "cloudwatch", "x-ray", "compliance"],
        "estimated_minutes": 35,
        "sections": [
            {
                "id": "s6-1",
                "title": "Why Observability is a Security Control",
                "blocks": [
                    {"type": "paragraph", "content": "For agentic systems, observability is not just an operational concern — it is a primary security control. Because agents act autonomously and can chain multiple tool calls, detective controls (logging, monitoring, alerting) are often the only mechanism to detect compromised or misbehaving agents before significant damage occurs."},
                    {"type": "bullets", "items": [
                        "Audit trails enable forensic reconstruction of what an agent did, on whose behalf, and when",
                        "Anomaly detection on agent behavior can surface prompt injection attacks before they complete",
                        "Compliance frameworks (SOC 2, ISO 27001) require immutable logs of all access to sensitive data",
                        "Structured logs enable automated policy violation detection — e.g., an agent accessing data outside its normal pattern",
                        "End-to-end tracing with X-Ray connects user → agent → tool → database with a single trace ID",
                    ]},
                ]
            },
            {
                "id": "s6-2",
                "title": "Structured Audit Event Schema",
                "blocks": [
                    {"type": "paragraph", "content": "Every tool invocation by an agent must produce a structured audit event. The event must capture the full actor chain (user identity + agent identity + service account), the specific action, the resource, the authorization decision, and the outcome."},
                    {"type": "code", "language": "python", "title": "Agent Audit Event Logger", "content": """import boto3
import json
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Optional, Any

@dataclass
class AgentAuditEvent:
    # Immutable identity context
    trace_id: str              # X-Ray trace ID for end-to-end correlation
    event_id: str              # Unique event ID
    timestamp_utc: str         # ISO 8601 UTC timestamp

    # Actor chain (who caused this)
    user_sub: str              # Original user identity (OIDC sub)
    user_email: str            # Human-readable user identifier
    agent_id: str              # Agent workload identity
    agent_version: str         # Agent deployment version
    service_account: str       # Service account used for data access

    # Action
    event_type: str            # e.g., 'TOOL_INVOCATION', 'TOKEN_EXCHANGE', 'AUTH_DECISION'
    tool_name: str             # MCP tool that was called
    resource: str              # Target resource (DB table, API endpoint, etc.)
    action: str                # Specific action (read, write, delete)

    # Inputs (sanitized — never include tokens, passwords, PII)
    tool_args_summary: dict    # Sanitized summary of tool arguments

    # Outcome
    authorization_decision: str  # 'allow' or 'deny'
    outcome: str               # 'success', 'failure', 'error'
    error_code: Optional[str]  # If outcome != success
    duration_ms: int           # Execution time

    # Risk signals
    anomaly_flags: list[str]   # e.g., ['unusual_hour', 'high_volume', 'new_resource']

class AgentAuditLogger:
    \"\"\"
    Structured audit logger that ships events to CloudWatch Logs with
    guaranteed ordering and immutability.
    \"\"\"

    LOG_GROUP = '/enterprise/agents/audit'

    def __init__(self, region: str = 'us-east-1'):
        self.logs_client = boto3.client('logs', region_name=region)
        self._sequence_tokens: dict[str, str] = {}
        self._ensure_log_group()

    def _ensure_log_group(self):
        try:
            self.logs_client.create_log_group(
                logGroupName=self.LOG_GROUP,
                tags={
                    'Purpose': 'agent-audit-trail',
                    'Retention': 'immutable',
                    'Classification': 'security-sensitive',
                }
            )
            # Set retention policy
            self.logs_client.put_retention_policy(
                logGroupName=self.LOG_GROUP,
                retentionInDays=2557  # 7 years for compliance
            )
        except self.logs_client.exceptions.ResourceAlreadyExistsException:
            pass

    def log_tool_invocation(
        self,
        trace_id: str,
        user_sub: str,
        user_email: str,
        agent_id: str,
        agent_version: str,
        service_account: str,
        tool_name: str,
        resource: str,
        tool_args: dict,
        authz_decision: str,
        outcome: str,
        duration_ms: int,
        error_code: str = None,
    ) -> str:
        \"\"\"
        Log a tool invocation event. Returns the event_id.

        Args:
            tool_args: Raw tool args — will be sanitized before logging
        \"\"\"
        event = AgentAuditEvent(
            trace_id=trace_id,
            event_id=str(uuid.uuid4()),
            timestamp_utc=_utc_now(),
            user_sub=user_sub,
            user_email=user_email,
            agent_id=agent_id,
            agent_version=agent_version,
            service_account=service_account,
            event_type='TOOL_INVOCATION',
            tool_name=tool_name,
            resource=resource,
            action=_infer_action(tool_name),
            tool_args_summary=_sanitize_args(tool_args),
            authorization_decision=authz_decision,
            outcome=outcome,
            error_code=error_code,
            duration_ms=duration_ms,
            anomaly_flags=_detect_anomalies(user_sub, agent_id, tool_name),
        )

        self._ship_event(event)
        return event.event_id

    def _ship_event(self, event: AgentAuditEvent) -> None:
        log_stream = f"agents/{event.agent_id}/{event.timestamp_utc[:10]}"

        # Create log stream if needed
        try:
            self.logs_client.create_log_stream(
                logGroupName=self.LOG_GROUP,
                logStreamName=log_stream,
            )
        except self.logs_client.exceptions.ResourceAlreadyExistsException:
            pass

        kwargs = dict(
            logGroupName=self.LOG_GROUP,
            logStreamName=log_stream,
            logEvents=[{
                'timestamp': int(time.time() * 1000),
                'message': json.dumps(asdict(event)),
            }]
        )

        # Use sequence token if we have one (required for ordered writes)
        if log_stream in self._sequence_tokens:
            kwargs['sequenceToken'] = self._sequence_tokens[log_stream]

        response = self.logs_client.put_log_events(**kwargs)
        self._sequence_tokens[log_stream] = response.get('nextSequenceToken', '')


def _utc_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()

def _infer_action(tool_name: str) -> str:
    tool_name_lower = tool_name.lower()
    if any(x in tool_name_lower for x in ['read', 'get', 'list', 'search', 'query']):
        return 'read'
    if any(x in tool_name_lower for x in ['write', 'create', 'insert', 'post']):
        return 'write'
    if any(x in tool_name_lower for x in ['delete', 'remove', 'drop']):
        return 'delete'
    if any(x in tool_name_lower for x in ['update', 'modify', 'patch']):
        return 'update'
    return 'execute'

def _sanitize_args(args: dict) -> dict:
    \"\"\"Remove sensitive fields from tool args before logging.\"\"\"
    sensitive_keys = {'password', 'token', 'secret', 'key', 'credential', 'auth', 'bearer'}
    return {
        k: '[REDACTED]' if any(s in k.lower() for s in sensitive_keys) else v
        for k, v in args.items()
    }

def _detect_anomalies(user_sub: str, agent_id: str, tool_name: str) -> list[str]:
    \"\"\"
    Simple anomaly detection. In production, replace with ML-based
    behavioral analysis (Amazon GuardDuty or custom model).
    \"\"\"
    from datetime import datetime
    flags = []

    hour = datetime.utcnow().hour
    if hour < 6 or hour > 22:  # Outside business hours
        flags.append('unusual_hour')

    # In production: check against historical baseline for this user/agent pair
    return flags
"""},
                ]
            },
            {
                "id": "s6-3",
                "title": "Distributed Tracing with AWS X-Ray",
                "blocks": [
                    {"type": "paragraph", "content": "AWS X-Ray provides end-to-end distributed tracing that connects a user request through the AgentCore MCP Gateway, to the Scout MCP Server, through the Data Access Service Account, and into the Solas-Logs database. A single trace ID allows security teams to reconstruct the complete execution path of any agent action."},
                    {"type": "code", "language": "python", "title": "X-Ray Tracing for Agent Tool Calls", "content": """from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.core import AWSXRayDaemonWriter
import functools

# Patch all AWS SDK clients to auto-trace
patch_all()

def trace_agent_tool(tool_name: str):
    \"\"\"
    Decorator that wraps an MCP tool function with X-Ray tracing.
    Adds identity metadata as trace annotations for filtering.
    \"\"\"
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get identity context from request (injected by gateway)
            identity_ctx = kwargs.pop('_identity_ctx', {})

            with xray_recorder.in_subsegment(f'mcp-tool:{tool_name}') as subsegment:
                # Add identity context as annotations (indexed, searchable)
                subsegment.put_annotation('user_sub', identity_ctx.get('user_sub', 'unknown'))
                subsegment.put_annotation('agent_id', identity_ctx.get('agent_id', 'unknown'))
                subsegment.put_annotation('tool_name', tool_name)

                # Add full context as metadata (not indexed, but fully stored)
                subsegment.put_metadata('identity_context', identity_ctx)
                subsegment.put_metadata('tool_args_keys', list(kwargs.keys()))

                try:
                    result = func(*args, **kwargs)
                    subsegment.put_annotation('outcome', 'success')
                    return result
                except PermissionError as e:
                    subsegment.put_annotation('outcome', 'authz_denied')
                    subsegment.add_exception(e, fatal=False)
                    raise
                except Exception as e:
                    subsegment.put_annotation('outcome', 'error')
                    subsegment.add_exception(e, fatal=True)
                    raise
        return wrapper
    return decorator


# Usage on MCP Server tool implementations
@trace_agent_tool('read_logs')
def read_logs(log_group: str, start_time: str, end_time: str, **kwargs) -> dict:
    \"\"\"
    MCP tool: read logs from Solas-Logs DB.
    X-Ray will trace this call including the downstream DynamoDB/RDS calls.
    \"\"\"
    # X-Ray automatically traces boto3 calls (via patch_all())
    # The full call chain: Gateway → MCP Server → read_logs() → DB
    # is visible as a single trace in X-Ray console
    logs_client = boto3.client('logs')
    response = logs_client.filter_log_events(
        logGroupName=log_group,
        startTime=int(start_time),
        endTime=int(end_time),
    )
    return {'events': response['events']}
"""},
                ]
            },
        ],
        "challenges": [
            {
                "id": "ch06-c1",
                "title": "Behavioral Anomaly Detector",
                "difficulty": "Medium",
                "description": "Implement a sliding-window behavioral anomaly detector for agent audit events. Detect: request volume spikes, access to unusual resources, and off-hours activity patterns.",
                "context": "Your security team wants automated alerts when agents behave unusually. Given a stream of audit events, detect anomalies based on: volume (> 2x normal rate for this agent in past 5 min), resource diversity (accessing > 5 distinct resources in 1 min), and time-of-day (outside 7am-10pm UTC).",
                "starter_code": """from dataclasses import dataclass
from collections import defaultdict, deque
import time

@dataclass
class AuditEvent:
    timestamp: float  # Unix timestamp
    agent_id: str
    user_sub: str
    tool_name: str
    resource: str
    outcome: str  # 'success' | 'failure' | 'error'

@dataclass
class Anomaly:
    event: AuditEvent
    anomaly_type: str  # 'volume_spike' | 'resource_diversity' | 'off_hours' | 'failure_burst'
    severity: str  # 'low' | 'medium' | 'high' | 'critical'
    details: str

class AgentAnomalyDetector:
    def __init__(self):
        # Sliding windows: agent_id -> deque of (timestamp, resource, outcome)
        self._windows: dict[str, deque] = defaultdict(deque)
        # Baseline: agent_id -> average requests per minute (from history)
        self._baselines: dict[str, float] = {}

    def set_baseline(self, agent_id: str, avg_requests_per_minute: float):
        \"\"\"Set the normal request rate baseline for an agent.\"\"\"
        self._baselines[agent_id] = avg_requests_per_minute

    def process_event(self, event: AuditEvent) -> list[Anomaly]:
        \"\"\"
        Process an audit event and return any anomalies detected.
        Maintain sliding 5-minute and 1-minute windows per agent.
        \"\"\"
        # TODO: implement
        pass
""",
                "solution_code": """from dataclasses import dataclass
from collections import defaultdict, deque
from datetime import datetime, timezone
import time

@dataclass
class AuditEvent:
    timestamp: float
    agent_id: str
    user_sub: str
    tool_name: str
    resource: str
    outcome: str

@dataclass
class Anomaly:
    event: AuditEvent
    anomaly_type: str
    severity: str
    details: str

class AgentAnomalyDetector:
    def __init__(self):
        self._windows: dict[str, deque] = defaultdict(deque)
        self._baselines: dict[str, float] = {}

    def set_baseline(self, agent_id: str, avg_requests_per_minute: float):
        self._baselines[agent_id] = avg_requests_per_minute

    def process_event(self, event: AuditEvent) -> list[Anomaly]:
        anomalies = []
        window = self._windows[event.agent_id]

        # Add event to window
        window.append(event)

        # Prune events older than 5 minutes
        cutoff_5m = event.timestamp - 300
        while window and window[0].timestamp < cutoff_5m:
            window.popleft()

        # 1. Volume spike detection (5-minute window)
        baseline = self._baselines.get(event.agent_id, 10.0)  # Default 10 rpm
        window_minutes = 5
        expected_5m = baseline * window_minutes
        actual_5m = len(window)
        if actual_5m > expected_5m * 2:
            anomalies.append(Anomaly(
                event=event,
                anomaly_type='volume_spike',
                severity='high',
                details=f"Agent '{event.agent_id}' made {actual_5m} requests in 5 min "
                        f"(baseline: {expected_5m:.1f}, threshold: {expected_5m*2:.1f})"
            ))

        # 2. Resource diversity (1-minute window)
        cutoff_1m = event.timestamp - 60
        recent_1m = [e for e in window if e.timestamp >= cutoff_1m]
        unique_resources = len(set(e.resource for e in recent_1m))
        if unique_resources > 5:
            anomalies.append(Anomaly(
                event=event,
                anomaly_type='resource_diversity',
                severity='medium',
                details=f"Agent '{event.agent_id}' accessed {unique_resources} distinct "
                        f"resources in 1 minute (threshold: 5)"
            ))

        # 3. Off-hours detection
        dt = datetime.fromtimestamp(event.timestamp, tz=timezone.utc)
        if not (7 <= dt.hour < 22):
            anomalies.append(Anomaly(
                event=event,
                anomaly_type='off_hours',
                severity='low',
                details=f"Agent '{event.agent_id}' active at {dt.strftime('%H:%M')} UTC "
                        f"(outside 07:00-22:00 window)"
            ))

        # 4. Failure burst (5 failures in 1 minute = possible attack probing)
        recent_failures = [e for e in recent_1m if e.outcome in ('failure', 'error')]
        if len(recent_failures) >= 5:
            anomalies.append(Anomaly(
                event=event,
                anomaly_type='failure_burst',
                severity='critical',
                details=f"Agent '{event.agent_id}' had {len(recent_failures)} failures/errors "
                        f"in 1 minute — possible probing or compromise"
            ))

        return anomalies
""",
                "solution_explanation": "The detector maintains a per-agent deque (sliding window) that is pruned on every event. The 5-minute window tracks volume; a 1-minute slice is computed on-the-fly for resource diversity and failure bursts. The failure burst check is the most critical — 5+ failures in a minute often indicates an attacker probing for accessible resources or a compromised agent.",
                "hints": [
                    "Use a deque for the sliding window — append right, popleft when events are too old",
                    "Don't maintain separate 1m and 5m windows — slice the 5m window on demand for 1m checks",
                    "Failure burst detection (outcome != 'success') is the highest-severity signal — prioritize it",
                ]
            }
        ],
        "references": [
            {"title": "AWS CloudWatch Logs Insights", "url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html"},
            {"title": "AWS X-Ray Developer Guide", "url": "https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html"},
            {"title": "SIEM Integration: Shipping CloudWatch to Security Hub", "url": "https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-cloudwatch-events.html"},
        ]
    },
]


def get_all_chapters() -> list[dict]:
    return SECURITY_CHAPTERS


def get_chapter_by_id(chapter_id: str) -> dict | None:
    for ch in SECURITY_CHAPTERS:
        if ch['id'] == chapter_id:
            return ch
    return None


def get_chapter_list() -> list[dict]:
    """Return lightweight chapter list (no sections/challenges content)."""
    return [
        {
            'id': ch['id'],
            'chapter_num': ch['chapter_num'],
            'title': ch['title'],
            'subtitle': ch['subtitle'],
            'description': ch['description'],
            'tags': ch['tags'],
            'estimated_minutes': ch['estimated_minutes'],
            'section_count': len(ch['sections']),
            'challenge_count': len(ch['challenges']),
        }
        for ch in SECURITY_CHAPTERS
    ]
