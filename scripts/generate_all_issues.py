#!/usr/bin/env python3
"""
Generate all SOC 2 project issues from templates
"""

import os
from github import Github
from rich.console import Console
from rich.progress import track

console = Console()

# All issues to create
ISSUES = [
    # Phase 1: Gap Analysis
    {
        "title": "[GAP] Conduct SOC 2 Readiness Assessment",
        "body": """## Objective
Assess current state against SOC 2 requirements

## Tasks
- [ ] Review existing security policies
- [ ] Evaluate current controls
- [ ] Assess documentation maturity
- [ ] Interview key personnel
- [ ] Review system architecture
- [ ] Document findings

## Deliverables
- Readiness assessment report
- Initial gap list""",
        "labels": ["phase-1-gap", "high-priority", "audit"],
        "milestone": "Gap Analysis Complete"
    },
    {
        "title": "[GAP] Map Controls to TSC Requirements",
        "body": """## Objective
Create control matrix mapping all controls to Trust Service Criteria

## Tasks
- [ ] List all Common Criteria controls
- [ ] List Security criteria controls
- [ ] Map controls to requirements
- [ ] Identify control gaps
- [ ] Document control descriptions
- [ ] Create control matrix spreadsheet

## TSC Coverage
- CC1: Control Environment
- CC2: Communication
- CC3: Risk Assessment
- CC4: Monitoring
- CC5: Control Activities
- CC6: Logical Access
- CC7: System Operations
- Security Criteria

## Deliverables
- Control matrix (250+ controls)
- Gap analysis per control""",
        "labels": ["phase-1-gap", "critical", "documentation", "tsc-cc"],
        "milestone": "Gap Analysis Complete"
    },
    {
        "title": "[GAP] Prioritize Remediation Roadmap",
        "body": """## Objective
Prioritize gaps and create remediation plan

## Tasks
- [ ] Categorize gaps by severity
- [ ] Estimate effort for each gap
- [ ] Identify dependencies
- [ ] Create timeline
- [ ] Assign owners
- [ ] Get approval

## Priority Levels
- Critical: Must fix before audit
- High: Significant risk
- Medium: Moderate risk
- Low: Nice to have

## Deliverables
- Prioritized gap list
- Remediation roadmap
- Resource allocation plan""",
        "labels": ["phase-1-gap", "high-priority", "documentation"],
        "milestone": "Gap Analysis Complete"
    },
    
    # Phase 2: Policies
    {
        "title": "[POLICY] Create Information Security Policy",
        "body": """## Objective
Develop master information security policy

## Requirements
- [ ] Policy purpose and scope
- [ ] Roles and responsibilities
- [ ] Security principles
- [ ] Compliance requirements
- [ ] Policy review process
- [ ] Legal review
- [ ] Executive approval
- [ ] Communication to staff
- [ ] Acknowledgment collection

## TSC Mapping
- CC1.2: Board oversight
- CC1.3: Management responsibilities
- CC2.1: Communication of information

## Deliverables
- Approved policy document
- Communication records
- Acknowledgment tracking""",
        "labels": ["phase-2-policy", "critical", "policy", "tsc-cc"],
        "milestone": "Policies Approved"
    },
    {
        "title": "[POLICY] Create Access Control Policy",
        "body": """## Objective
Define access control requirements and procedures

## Requirements
- [ ] User access principles (least privilege)
- [ ] Authentication requirements
- [ ] MFA requirements
- [ ] Password standards
- [ ] Access request process
- [ ] Access review process
- [ ] Termination procedures
- [ ] Legal review
- [ ] Executive approval
- [ ] Staff training

## TSC Mapping
- CC6.1: Logical access controls
- CC6.2: Access credentials
- CC6.3: Network access

## Deliverables
- Approved policy document
- Access request forms
- Review procedures""",
        "labels": ["phase-2-policy", "critical", "policy", "tsc-security"],
        "milestone": "Policies Approved"
    },
    {
        "title": "[POLICY] Create Change Management Policy",
        "body": """## Objective
Document change control procedures

## Requirements
- [ ] Change categories (emergency, standard, normal)
- [ ] Change approval process
- [ ] Testing requirements
- [ ] Rollback procedures
- [ ] Change documentation
- [ ] Change advisory board
- [ ] Legal review
- [ ] Executive approval

## TSC Mapping
- CC8.1: Change management process
- CC7.1: System operations

## Deliverables
- Approved policy document
- Change request forms
- Approval workflow""",
        "labels": ["phase-2-policy", "high-priority", "policy", "tsc-cc"],
        "milestone": "Policies Approved"
    },
    {
        "title": "[POLICY] Create Incident Response Policy",
        "body": """## Objective
Define incident response procedures

## Requirements
- [ ] Incident categories
- [ ] Response team roles
- [ ] Escalation procedures
- [ ] Communication plan
- [ ] Investigation procedures
- [ ] Post-incident review
- [ ] Legal review
- [ ] Executive approval

## TSC Mapping
- CC7.3: Incident management
- CC7.4: Security incidents

## Deliverables
- Approved policy document
- Response playbooks
- Communication templates""",
        "labels": ["phase-2-policy", "high-priority", "policy", "tsc-security"],
        "milestone": "Policies Approved"
    },
    {
        "title": "[POLICY] Create Vendor Management Policy",
        "body": """## Objective
Define vendor risk management procedures

## Requirements
- [ ] Vendor assessment criteria
- [ ] Security requirements
- [ ] Contract requirements
- [ ] Ongoing monitoring
- [ ] Vendor reviews
- [ ] Legal review
- [ ] Executive approval

## TSC Mapping
- CC9.1: Vendor management
- CC9.2: Vendor assessment

## Deliverables
- Approved policy document
- Vendor assessment form
- Contract template""",
        "labels": ["phase-2-policy", "high-priority", "policy", "tsc-cc"],
        "milestone": "Policies Approved"
    },
    
    # Phase 3: Technical Controls
    {
        "title": "[CONTROL] Implement Multi-Factor Authentication",
        "body": """## Objective
Enforce MFA for all user access

## Tasks
- [ ] Select MFA solution
- [ ] Configure MFA for all users
- [ ] Enforce for production access
- [ ] Enforce for VPN
- [ ] Enforce for admin access
- [ ] Document configuration
- [ ] Train users
- [ ] Create evidence collection

## Acceptance Criteria
- 100% MFA enrollment
- No access without MFA
- Evidence of enforcement

## TSC Mapping
- CC6.1: Logical access controls
- CC6.2: Authentication

## Evidence Required
- MFA enrollment reports
- Access logs showing MFA
- Configuration screenshots""",
        "labels": ["phase-3-tech", "critical", "technical", "tsc-security"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[CONTROL] Implement Centralized Logging (SIEM)",
        "body": """## Objective
Deploy SIEM solution for centralized logging

## Tasks
- [ ] Select SIEM platform
- [ ] Configure log collection
- [ ] Integrate all systems
- [ ] Set retention (1+ years)
- [ ] Create alerting rules
- [ ] Document procedures
- [ ] Train security team
- [ ] Test log review process

## Log Sources
- Application logs
- System logs
- Security logs
- Network logs
- Database logs
- Cloud provider logs

## TSC Mapping
- CC7.2: System monitoring
- CC7.3: Threat detection

## Evidence Required
- SIEM configuration
- Log samples
- Alert examples
- Review documentation""",
        "labels": ["phase-3-tech", "critical", "technical", "tsc-cc"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[CONTROL] Implement Encryption at Rest",
        "body": """## Objective
Encrypt all data at rest

## Tasks
- [ ] Identify all data stores
- [ ] Enable database encryption
- [ ] Enable disk encryption
- [ ] Enable S3 encryption
- [ ] Implement key management
- [ ] Document encryption standards
- [ ] Test encryption
- [ ] Create evidence

## Encryption Standards
- AES-256 for data at rest
- Key rotation procedures
- Key access controls

## TSC Mapping
- CC6.1: Data protection
- CC6.7: Encryption

## Evidence Required
- Configuration screenshots
- Encryption verification
- Key management docs""",
        "labels": ["phase-3-tech", "critical", "technical", "tsc-confidential"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[CONTROL] Implement Vulnerability Scanning",
        "body": """## Objective
Deploy automated vulnerability scanning

## Tasks
- [ ] Select scanning tool
- [ ] Configure weekly scans
- [ ] Scan infrastructure
- [ ] Scan applications
- [ ] Scan dependencies
- [ ] Create remediation process
- [ ] Set SLAs (30/60 days)
- [ ] Document procedures

## Scan Frequency
- Infrastructure: Weekly
- Applications: Weekly
- Dependencies: Daily

## TSC Mapping
- CC7.1: Vulnerability management
- CC7.2: Security monitoring

## Evidence Required
- Scan reports
- Remediation tickets
- SLA compliance reports""",
        "labels": ["phase-3-tech", "high-priority", "technical", "tsc-security"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[CONTROL] Implement Network Segmentation",
        "body": """## Objective
Segment network into security zones

## Tasks
- [ ] Design network architecture
- [ ] Separate prod/dev/staging
- [ ] Configure firewalls
- [ ] Implement VPCs/subnets
- [ ] Document network diagram
- [ ] Test connectivity
- [ ] Document firewall rules

## Segments
- Production
- Development
- Staging
- Management
- DMZ

## TSC Mapping
- CC6.6: Network security
- CC6.1: Access controls

## Evidence Required
- Network diagrams
- Firewall rules
- Segmentation testing""",
        "labels": ["phase-3-tech", "high-priority", "technical", "tsc-security"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[CONTROL] Implement Backup and Recovery",
        "body": """## Objective
Deploy automated backup solution

## Tasks
- [ ] Configure automated backups
- [ ] Set backup schedule (daily/weekly)
- [ ] Configure offsite storage
- [ ] Test restoration (quarterly)
- [ ] Document procedures
- [ ] Set retention policy
- [ ] Monitor backup jobs

## Backup Schedule
- Daily incremental
- Weekly full
- Monthly archival

## TSC Mapping
- CC7.5: Backup procedures
- A1.2: Business continuity

## Evidence Required
- Backup job logs
- Restoration test results
- Retention documentation""",
        "labels": ["phase-3-tech", "high-priority", "technical", "tsc-availability"],
        "milestone": "Technical Controls Implemented"
    },
    
    # Phase 4: HR Controls
    {
        "title": "[HR] Implement Background Check Process",
        "body": """## Objective
Conduct background checks for all employees

## Tasks
- [ ] Select screening vendor
- [ ] Define check requirements
- [ ] Update employment agreements
- [ ] Process existing employees
- [ ] Process new hires
- [ ] Document results (securely)
- [ ] Create retention policy

## Check Components
- Criminal history
- Employment verification
- Education verification (key roles)

## TSC Mapping
- CC1.4: Personnel practices

## Evidence Required
- Vendor agreement
- Process documentation
- Sample reports (redacted)""",
        "labels": ["phase-4-hr", "high-priority", "documentation"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[HR] Implement Security Awareness Training",
        "body": """## Objective
Deploy annual security training program

## Tasks
- [ ] Select training platform
- [ ] Create training content
- [ ] Deploy to all staff
- [ ] Track completion
- [ ] Conduct phishing simulations
- [ ] Document results
- [ ] Schedule annual refresh

## Training Topics
- Security policies
- Data handling
- Phishing awareness
- Incident reporting
- Password security

## TSC Mapping
- CC1.4: Training and competence
- CC2.3: Security awareness

## Evidence Required
- Training materials
- Completion reports
- Phishing results
- Attestations""",
        "labels": ["phase-4-hr", "high-priority", "training"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[HR] Implement Access Review Process",
        "body": """## Objective
Conduct quarterly access reviews

## Tasks
- [ ] Define review process
- [ ] Identify all access points
- [ ] Schedule quarterly reviews
- [ ] Create review templates
- [ ] Assign reviewers
- [ ] Document results
- [ ] Remediate findings

## Review Scope
- System access
- Application access
- Administrative rights
- Service accounts
- Third-party access

## TSC Mapping
- CC6.2: Access reviews
- CC6.3: Access removal

## Evidence Required
- Review schedules
- Review reports
- Remediation tickets
- Management sign-offs""",
        "labels": ["phase-4-hr", "critical", "procedure"],
        "milestone": "Technical Controls Implemented"
    },
    
    # Phase 5: Vendor Management
    {
        "title": "[VENDOR] Create Vendor Inventory",
        "body": """## Objective
Document all third-party vendors and subprocessors

## Tasks
- [ ] Identify all vendors
- [ ] Classify by risk level
- [ ] Document data access
- [ ] Collect contact info
- [ ] Create inventory spreadsheet
- [ ] Review with legal
- [ ] Publish to website (if required)

## Vendor Categories
- Infrastructure (AWS, Azure, GCP)
- SaaS applications
- Payment processors
- Support tools
- Development tools

## TSC Mapping
- CC9.1: Vendor inventory
- CC9.2: Subservice organizations

## Deliverables
- Vendor inventory list
- Risk classifications
- Subprocessor list""",
        "labels": ["phase-5-vendor", "high-priority", "documentation"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[VENDOR] Collect Vendor SOC 2 Reports",
        "body": """## Objective
Obtain SOC 2 reports from critical vendors

## Tasks
- [ ] Identify critical vendors
- [ ] Request SOC 2 reports
- [ ] Review reports
- [ ] Document relevant controls
- [ ] Identify CUECs
- [ ] Store reports securely
- [ ] Schedule annual refresh

## Critical Vendors
- Cloud infrastructure provider
- Authentication service
- Payment processor
- Backup service
- Monitoring service

## TSC Mapping
- CC9.2: Vendor assessments

## Evidence Required
- SOC 2 reports
- Review documentation
- CUEC mapping""",
        "labels": ["phase-5-vendor", "critical", "evidence"],
        "milestone": "Technical Controls Implemented"
    },
    
    # Phase 6: Risk Assessment
    {
        "title": "[RISK] Conduct Annual Risk Assessment",
        "body": """## Objective
Perform comprehensive risk assessment

## Tasks
- [ ] Identify information assets
- [ ] Identify threats
- [ ] Identify vulnerabilities
- [ ] Assess likelihood
- [ ] Assess impact
- [ ] Calculate risk scores
- [ ] Document risk treatment
- [ ] Create risk register
- [ ] Get management approval

## Risk Categories
- Operational risks
- Technology risks
- External risks
- Compliance risks

## TSC Mapping
- CC3.1: Risk identification
- CC3.2: Risk analysis
- CC3.3: Risk mitigation

## Deliverables
- Risk assessment report
- Risk register
- Treatment plans""",
        "labels": ["phase-6-risk", "critical", "documentation"],
        "milestone": "Technical Controls Implemented"
    },
    {
        "title": "[BCP] Create Business Continuity Plan",
        "body": """## Objective
Develop business continuity and disaster recovery plan

## Tasks
- [ ] Conduct business impact analysis
- [ ] Identify critical functions
- [ ] Define RTOs and RPOs
- [ ] Document recovery procedures
- [ ] Identify alternate sites
- [ ] Create communication plan
- [ ] Test plan annually
- [ ] Get approval

## BCP Components
- Emergency response
- Notification procedures
- Recovery procedures
- Communication plan
- Resource requirements

## TSC Mapping
- A1.1: Business continuity
- A1.2: Disaster recovery

## Deliverables
- BCP/DR plan
- Test results
- Training materials""",
        "labels": ["phase-6-risk", "high-priority", "documentation", "tsc-availability"],
        "milestone": "Technical Controls Implemented"
    },
]


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        console.print("[red]Error: GITHUB_TOKEN not set[/red]")
        return
    
    gh = Github(token)
    user = gh.get_user()
    
    # Get repository
    repo_name = input("Enter repository name [saasx-soc2-certification]: ") or "saasx-soc2-certification"
    
    try:
        repo = user.get_repo(repo_name)
    except:
        console.print(f"[red]Error: Repository '{repo_name}' not found[/red]")
        return
    
    # Get milestones
    milestones = {m.title: m for m in repo.get_milestones()}
    
    console.print(f"\n[cyan]Creating {len(ISSUES)} issues...[/cyan]\n")
    
    created = 0
    skipped = 0
    
    for issue_data in track(ISSUES, description="Creating issues..."):
        try:
            milestone = milestones.get(issue_data["milestone"])
            
            # Check if issue already exists
            existing = list(repo.get_issues(state="all"))
            if any(i.title == issue_data["title"] for i in existing):
                skipped += 1
                continue
            
            repo.create_issue(
                title=issue_data["title"],
                body=issue_data["body"],
                labels=issue_data["labels"],
                milestone=milestone
            )
            created += 1
            
        except Exception as e:
            console.print(f"[red]Error creating {issue_data['title']}: {e}[/red]")
    
    console.print(f"\n[green]✅ Created {created} issues[/green]")
    if skipped:
        console.print(f"[yellow]⚠️  Skipped {skipped} existing issues[/yellow]")


if __name__ == "__main__":
    main()
