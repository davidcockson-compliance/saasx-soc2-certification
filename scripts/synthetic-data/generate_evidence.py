#!/usr/bin/env python3
"""
Generate synthetic evidence for SOC 2 audit
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker

fake = Faker()

# Install faker if needed
try:
    from faker import Faker
except ImportError:
    import os
    os.system("pip3 install faker")
    from faker import Faker

class EvidenceGenerator:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fake = Faker()
        
        # Generate consistent employee list
        self.employees = self.generate_employees(87)
        
    def generate_employees(self, count: int):
        """Generate employee list"""
        employees = []
        departments = ["Engineering", "Product", "Sales", "Marketing", "Finance", 
                      "HR", "Operations", "Security", "Legal"]
        
        job_titles = {
            "Engineering": ["Software Engineer", "DevOps Engineer", "QA Engineer"],
            "Product": ["Product Manager", "Product Owner", "UX Designer"],
            "Sales": ["Account Executive", "Business Development Rep", "Sales Engineer"],
            "Marketing": ["Marketing Manager", "Content Creator", "Growth Hacker"],
            "Finance": ["Financial Analyst", "Accountant", "Controller"],
            "HR": ["HR Generalist", "Recruiter", "Benefits Administrator"],
            "Operations": ["Operations Manager", "Project Manager", "Business Analyst"],
            "Security": ["Security Engineer", "Compliance Officer", "Incident Responder"],
            "Legal": ["Legal Counsel", "Contract Manager", "Privacy Officer"]
        }
        
        for _ in range(count):
            department = random.choice(departments)
            employee_id = fake.uuid4()
            employee = {
                'employee_id': employee_id,
                'name': fake.name(),
                'email': f"{fake.user_name()}@example.com",
                'department': department,
                'job_title': random.choice(job_titles[department]),
                'hire_date': fake.date_between(start_date='-5y', end_date='today'),
                'manager_id': fake.uuid4(),
                'access_level': random.choice(['standard', 'admin', 'privileged'])
            }
            employees.append(employee)
        return employees
    
    def generate_access_logs(self, days: int = 30):
        """Generate synthetic access logs"""
        access_logs = []
        actions = ['login', 'logout', 'file_access', 'system_change']
        resources = ['database', 'file_system', 'api_gateway', 'admin_panel']
        
        start_date = datetime.now() - timedelta(days=days)
        end_date = datetime.now()
        
        for employee in self.employees:
            # Generate random activity patterns
            num_actions = random.randint(50, 200)  # Reasonable activity range
            
            for _ in range(num_actions):
                log_entry = {
                    'timestamp': fake.date_time_between(start_date=start_date, 
                                                     end_date=end_date),
                    'employee_id': employee['employee_id'],
                    'action': random.choice(actions),
                    'resource': random.choice(resources),
                    'ip_address': fake.ipv4(),
                    'status': random.choice(['success', 'failure']),
                    'details': fake.text(max_nb_chars=100)
                }
                access_logs.append(log_entry)
                
        return sorted(access_logs, key=lambda x: x['timestamp'])
    
    def generate_audit_trails(self, days: int = 30):
        """Generate synthetic audit trails"""
        audit_trails = []
        actions = ['create', 'update', 'delete', 'view']
        objects = ['customer_record', 'financial_transaction', 
                  'configuration_change', 'access_request']
        
        start_date = datetime.now() - timedelta(days=days)
        end_date = datetime.now()
        
        for employee in self.employees:
            # Generate realistic audit activity
            num_actions = random.randint(20, 100)
            
            for _ in range(num_actions):
                trail_entry = {
                    'timestamp': fake.date_time_between(start_date=start_date,
                                                     end_date=end_date),
                    'employee_id': employee['employee_id'],
                    'action': random.choice(actions),
                    'object_type': random.choice(objects),
                    'object_id': fake.uuid4(),
                    'changes': json.dumps({
                        'old_value': fake.text(max_nb_chars=50),
                        'new_value': fake.text(max_nb_chars=50)
                    }),
                    'ip_address': fake.ipv4(),
                    'session_id': fake.uuid4()
                }
                audit_trails.append(trail_entry)
                
        return sorted(audit_trails, key=lambda x: x['timestamp'])
    
    def generate_incident_reports(self, count: int = 10):
        """Generate synthetic incident reports"""
        incidents = []
        incident_types = ['security', 'compliance', 'operational']
        severities = ['low', 'medium', 'high', 'critical']
        
        for _ in range(count):
            incident = {
                'incident_id': fake.uuid4(),
                'reported_by': random.choice([emp['employee_id'] 
                                           for emp in self.employees]),
                'incident_type': random.choice(incident_types),
                'severity': random.choice(severities),
                'description': fake.text(max_nb_chars=200),
                'reported_date': fake.date_between(start_date='-1y',
                                                 end_date='today'),
                'resolved_date': fake.date_between(
                    start_date='-1y', end_date='today'),
                'resolution_steps': [
                    {'step': f"Step {i}", 
                     'action': fake.text(max_nb_chars=100),
                     'completed_by': random.choice([emp['employee_id'] 
                                                 for emp in self.employees]),
                     'completed_at': fake.date_between(start_date='-1y',
                                                     end_date='today')}
                    for i in range(random.randint(2, 5))
                ]
            }
            incidents.append(incident)
            
        return sorted(incidents, key=lambda x: x['reported_date'])
    
    def generate_risk_assessment_reports(self, count: int = 5):
        """Generate synthetic risk assessment reports"""
        risks = []
        risk_categories = ['strategic', 'operational', 'financial', 'compliance']
        likelihoods = ['low', 'medium', 'high']
        impacts = ['minimal', 'moderate', 'significant', 'critical']
        
        for _ in range(count):
            risk = {
                'risk_id': fake.uuid4(),
                'category': random.choice(risk_categories),
                'description': fake.text(max_nb_chars=150),
                'likelihood': random.choice(likelihoods),
                'impact': random.choice(impacts),
                'risk_score': round(random.uniform(1.0, 10.0), 1),
                'mitigation_plans': [
                    {'plan': f"Plan {i}", 
                     'description': fake.text(max_nb_chars=100),
                     'owner': random.choice([emp['employee_id'] 
                                          for emp in self.employees]),
                     'target_date': fake.date_between(start_date='today',
                                                    end_date='+1y')}
                    for i in range(random.randint(2, 4))
                ],
                'review_date': fake.date_between(start_date='-1y',
                                               end_date='today'),
                'next_review_date': fake.date_between(start_date='today',
                                                     end_date='+1y')
            }
            risks.append(risk)
            
        return sorted(risks, key=lambda x: x['risk_score'], 
                     reverse=True)
    
    def save_evidence(self, evidence_type: str, data):
        """Save evidence to file"""
        filename = f"{evidence_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Generated {evidence_type} evidence: {filepath}")

def main():
    # Create generator instance
    generator = EvidenceGenerator(Path("./audit_evidence"))
    
    # Generate and save various types of evidence
    print("Generating SOC 2 audit evidence...")
    
    # Generate access logs
    access_logs = generator.generate_access_logs(days=90)
    generator.save_evidence("access_logs", access_logs)
    
    # Generate audit trails
    audit_trails = generator.generate_audit_trails(days=90)
    generator.save_evidence("audit_trails", audit_trails)
    
    # Generate incident reports
    incidents = generator.generate_incident_reports(count=15)
    generator.save_evidence("incident_reports", incidents)
    
    # Generate risk assessment reports
    risks = generator.generate_risk_assessment_reports(count=8)
    generator.save_evidence("risk_assessment_reports", risks)

if __name__ == "__main__":
    main()
