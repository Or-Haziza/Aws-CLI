# AWS Resource Provisioning CLI

## Overview

This CLI tool allows developers to automate the provisioning of AWS resources such as EC2 instances, S3 buckets, and Route53 DNS records. It aims to provide a self-service mechanism while adhering to strict DevOps standards.

## Features

### EC2 Instances
- **Create**: Launch a new EC2 instance with options for instance types (`t3.nano`, `t4g.nano`) and AMI selection (latest Ubuntu or Amazon Linux).
- **Manage Instances**: Start and stop instances created via this CLI.
- **List Instances**: View all EC2 instances created through the CLI.

### S3 Buckets
- **Create**: Create S3 buckets with public or private access.
- **Confirmation for Public Buckets**: Requires user confirmation for public access.
- **File Upload**: Upload files to buckets created through the CLI.
- **List Buckets**: List all S3 buckets created via the CLI.

### Route53
- **Create Zones**: Create DNS zones in Route53.
- **Manage DNS Records**: Add, update, or delete DNS records for zones created via the CLI.

## Usage

```bash
# Install Dependencies
pip install boto3 click

# Run the CLI
python your_cli_script.py

# Commands
# Check the tool
python your_cli_script.py check

# Create EC2 Instance
python your_cli_script.py create <instance_type> <ami>

# List EC2 Instances
python your_cli_script.py list

# Create S3 Bucket
python your_cli_script.py create_bucket <bucket_name> --public

# Upload File to S3 Bucket
python your_cli_script.py upload_file <bucket_name> <file_path>

# Create DNS Zone
python your_cli_script.py create_dns_zone <domain_name>

# Manage DNS Records
python your_cli_script.py manage_dns_record <domain_name> <record_name> <record_type> <record_value> <action>


# Bonus Challenge
For an additional challenge, consider integrating this CLI tool with an open-source tool like Jenkins to provide a user-friendly UI.
ן ש
