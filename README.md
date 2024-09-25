# Platform Engineering Python Exercise: Automating AWS Resource Provisioning

## Overview
You've just joined a new company as a junior DevOps engineer. Your team's key responsibility is provisioning AWS resources for various development projects, such as EC2 instances, S3 buckets, and Route53 DNS records. To streamline this process and empower developers, you'll develop a Python-based Command Line Interface (CLI) tool that allows them to create, update, and manage AWS resources while ensuring compliance with established DevOps standards.

## Table of Contents
1. [Scenario](#scenario)
2. [Your Task](#your-task)
3. [Phase 1: Core CLI Development](#phase-1-core-cli-development)
   - [EC2 Instances](#ec2-instances)
   - [S3 Buckets](#s3-buckets)
   - [Route53](#route53)
   - [CLI Requirements](#cli-requirements)
4. [Phase 2: Bonus Challenge – Adding a UI](#phase-2-bonus-challenge--adding-a-ui)

## Scenario
As a new member of the DevOps team, your role includes provisioning AWS resources for developers. Currently, developers rely on you to create resources, but you want to introduce a platform engineering approach that allows them to provision resources themselves, within the guidelines set by your team.

## Your Task
You will develop a Python-based CLI tool that enables developers to create and manage AWS resources while adhering to your team's standards.

---

## Phase 1: Core CLI Development

### EC2 Instances
- **Create**: Allow the creation of a new EC2 instance with options to choose between two small instance types (t3.nano and t4g.nano). Limit the creation to a maximum of two running instances.
- **AMI Choice**: Let developers select between the latest Ubuntu AMI or the latest Amazon Linux AMI.
- **Manage Instances**: Enable starting and stopping EC2 instances, but only if they were created through the CLI.
- **List Instances**: Provide a list of all EC2 instances created through the CLI, excluding those created by others.

### S3 Buckets
- **Create**: Enable the creation of new S3 buckets, with options for public and private access.
- **Confirmation for Public Buckets**: If public access is chosen, request additional approval from the user: "Are you sure?".
- **File Upload**: Allow developers to upload files to an S3 bucket only if the bucket was created through the CLI.
- **List Buckets**: Provide a list of all S3 buckets created by the CLI.

### Route53
- **Create Zones**: Allow the creation of DNS zones via Route53.
- **Manage DNS Records**: Enable developers to create, update, or delete DNS records, but only for zones created through the CLI.

### CLI Requirements
- The CLI should accept resource type, action (create, update, delete), and any required parameters.
- The CLI should provide clear output indicating the success or failure of the operation and the current status of the resource.

---

## Phase 2: Bonus Challenge – Adding a UI
For an extra challenge, integrate your Python CLI tool with an open-source tool like Jenkins to provide a user interface (UI). Each resource and action can be implemented as a different screen or job in Jenkins, providing a more accessible platform for developers to use.

---

## Getting Started
1. **Prerequisites**:
   - Python 3.x
   - Boto3 (AWS SDK for Python)
   - Click (for CLI creation)
   
2. **Installation**:
   ```bash
   pip install boto3 click
