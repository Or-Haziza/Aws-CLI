import click 
import boto3 
from botocore.exceptions import ClientError



#Vars 

ec2 = boto3.client('ec2')
s3  = boto3.client('s3')
ec2_r = boto3.resource('ec2')
session = boto3.session.Session()



#cli

@click.group()
def cli():
    """Main CLI group."""
    click.echo("CLI initialized")



@cli.command()
def check():
    click.echo("tool ready")


#create instance
@cli.command()
@click.argument('instance_type', type=click.Choice(['t3.nano', 't4g.nano']))
@click.argument('ami', type=click.Choice(['ubuntu', 'amazon-linux']))
def create(instance_type,ami):
    
    count =0 
    #מיפוי לארגומנטים
    
    ami_map = {
        'ubuntu': 'ami-0e86e20dae9224db8',  # ubuntu ami
        'amazon-linux': 'ami-02c21308fed24a8ab'  # amazon - linux ami
    }

    #בדיקה לארגומנטים   
    
    if ami not in ami_map:
        click.echo("Invalid AMI choice")
        return
    

    for instance in ec2_r.instances.all():
        try:
            for tag in instance.tags:

                if tag["Key"] == "session" and tag["Value"] == "cli" and instance.state['Name'] == 'running':
                    count +=1
        
        
        except:
            print("WARRNING the instance with id - ",instance.id, " dont have tags")

   
    if count >= 2:
        click.echo("you have two EC2 running ITS YOUR LIMIT /n Try to sttop one")
        return
    
    
    else:
    
        try:
            instances = ec2.run_instances(

                ImageId= ami_map[ami],
                MinCount=1,
                MaxCount=1,
                InstanceType = instance_type,
                
            

                
                NetworkInterfaces=[
                        {
                               
                                'SubnetId': 'subnet-0a5c0b1fc881ce94d',
                                'AssociatePublicIpAddress': True,
                                'DeviceIndex': 0,
                                'Groups': ['sg-0fb73517ea4741631']
                        },


                ],

                TagSpecifications=[
                        {
                                'ResourceType': 'instance',
                                'Tags': [
                                        {
                                                'Key': 'Name',
                                                'Value': 'OrHaziza3'
                                        },
                                        {
                                                'Key': 'session',
                                                'Value': "cli",

                                        }
                                ],
                        }]
        )
            click.echo("your ec2 is initialising and few monments will be ready to use")
        except ClientError as e:
            click.echo(f"Error: {e}")



#list instacne 
@cli.command
def list():
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # קבלת תגיות המופע
            tags = instance.get('Tags', [])
            
            # בדיקת אם התגית הרצויה קיימת
            tag_found = any(tag['Key'] == 'session' and tag['Value'] == 'cli' for tag in tags)
            
            if tag_found:
                instance_id = instance.get('InstanceId')
                instance_type = instance.get('InstanceType')
                instance_state = instance.get('State', {}).get('Name')
                public_ip = instance.get('PublicIpAddress', 'No Public IP')
                
                click.echo(f"Instance ID: {instance_id}")
                click.echo(f"Instance Type: {instance_type}")
                click.echo(f"Instance State: {instance_state}")
                click.echo(f"Public IP: {public_ip}")
                click.echo('-' * 40)
    
        
        


#action (action + id)
@cli.command
@click.argument('action', type=str)
@click.argument('id', type=str)
def action(action, id):
    
    
    EC2_FROM_CLI_ID = []
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:session' ,
                'Values': ['cli']
            }
            
        ]
    )



    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
       
          EC2_FROM_CLI_ID.append(instance.get('InstanceId'))  
         
    click.echo(id)
    click.echo(EC2_FROM_CLI_ID)
    
    if id in EC2_FROM_CLI_ID:
        if action == 'start':
            response = ec2.start_instances(InstanceIds=[id])
            click.echo(f"Starting instance {id}.")
        elif action == 'stop':
            response = ec2.stop_instances(InstanceIds=[id])
            click.echo(f"Stopping instance {id}.")
        else:
            click.echo("Invalid action. Use 'start' or 'stop'.")


#create bucket(name + pub/pra option)
@cli.command()
@click.argument('bucket_name', type=str)
@click.option('--public/--private', default=False, help="Specify bucket access type")
def create_bucket(bucket_name, public):
    """
    Create a new S3 bucket with the specified access type.
    
    :param bucket_name: The name of the bucket to create
    :param public: Whether the bucket should be public (default is private)
    """
    
    click.echo(session.region_name)
    if public:
        # בקשה לאישור לפני יצירת סל ציבורי
        confirm = click.prompt("Are you sure you want to create a public bucket? (yes/no)", type=str)
        if confirm.lower() != 'yes':
            click.echo("Bucket creation cancelled.")
            return

    try:
        # יצירת סל עם LocationConstraint תלוי באיזה אזור אנחנו
        if session.region_name == 'us-east-1':
            # עבור אזור us-east-1, אין צורך ב-LocationConstraint
            s3.create_bucket(Bucket=bucket_name)
        else:
            # עבור אזורים אחרים, נצטרך לציין את ה-LocationConstraint
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': session.region_name
                }
            )

        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'session',
                        'Value': 'cli'
                    }
                ]
            }
        )
        click.echo(f"Bucket '{bucket_name}' tagged with 'session:cli'.")

        # הגדרת גישה ציבורית אם נדרש
        if public:
            s3.put_bucket_acl(Bucket=bucket_name, ACL='public-read')
            click.echo(f"Bucket '{bucket_name}' created with public access.")
        
        else:
            click.echo(f"Bucket '{bucket_name}' created with private access.")
            
    except ClientError as e:
        # טיפול בשגיאות והדפסת הודעת שגיאה
        click.echo(f"Error: {e}")


#upload-file(bucket_name + file_path)
@cli.command()
@click.argument('bucket_name', type=str)
@click.argument('file_path', type=str)
def upload_file(bucket_name, file_path):
    """
    Upload a file to the specified S3 bucket, but only if the bucket was created through the CLI.
    
    :param bucket_name: The name of the bucket to upload to
    :param file_path: The path to the file to upload
    """
    try:
        # בדוק אם הסל נוצר דרך ה-CLI
        tags = s3.get_bucket_tagging(Bucket=bucket_name).get('TagSet', [])
        if any(tag['Key'] == 'session' and tag['Value'] == 'cli' for tag in tags):
            # העלאת הקובץ לסל
            s3.upload_file(file_path, bucket_name, file_path.split('/')[-1])
            click.echo(f"File '{file_path}' uploaded to bucket '{bucket_name}'.")
        else:
            click.echo(f"Bucket '{bucket_name}' was not created via CLI. Upload denied.")
    except ClientError as e:
        click.echo(f"Error: {e}")


#list bucket
@cli.command()
def list_buckets():
    """
    List all S3 buckets created via CLI.
    """
    try:
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                tags = s3.get_bucket_tagging(Bucket=bucket_name).get('TagSet', [])
                if any(tag['Key'] == 'session' and tag['Value'] == 'cli' for tag in tags):
                    click.echo(f"Bucket '{bucket_name}' created via CLI.")
                    click.echo('-' * 40)
                else:
                    click.echo(f"Bucket '{bucket_name}' not created via CLI.")
                    click.echo('-' * 40)
            except ClientError as e:
                click.echo(f"Error getting tags for bucket '{bucket_name}': {e}")
                click.echo('-' * 40)
    except ClientError as e:
        click.echo(f"Error listing buckets: {e}")



#create zones
@cli.command()
@click.argument('domain_name')
def create_dns_zone(domain_name):
    client = boto3.client('route53')
    
    response = client.create_hosted_zone(
        Name=domain_name,
        CallerReference=str(hash(domain_name)),
        HostedZoneConfig={
            'Comment': 'Created via CLI',
            'PrivateZone': False
        }
    )
    
    click.echo(f"Hosted Zone Created: {response['HostedZone']['Id']}")


#בהתחלה המשתמש היה צריך לתת את האיי די של הזון אבל עשיתי םונקציה שתקל על המשתמש 
#Manage DNS Recordes
def get_hosted_zone_id(domain_name):
    client = boto3.client('route53')
    
    response = client.list_hosted_zones()
    click.echo(f"Available Hosted Zones: {[zone['Name'] for zone in response['HostedZones']]}")
    
    for zone in response['HostedZones']:
        zone_name = zone['Name'].rstrip('.')  # מסיר את הנקודה בסוף שם האזור
        click.echo(f"Checking against zone: {zone_name}")
        if domain_name == zone_name or domain_name.endswith('.' + zone_name):
            return zone['Id']
    
    click.echo("Error: Hosted zone not found.")
    return None


@cli.command()
@click.argument('domain_name')
@click.argument('record_name')
@click.argument('record_type')
@click.argument('record_value')
@click.argument('action')
def manage_dns_record(domain_name, record_name, record_type, record_value, action):
    client = boto3.client('route53')

    hosted_zone_id = get_hosted_zone_id(domain_name)
    if not hosted_zone_id:
        return
    
    response = client.get_hosted_zone(Id=hosted_zone_id)
    comment = response['HostedZone']['Config'].get('Comment', '')
    if comment != 'Created via CLI':
        click.echo("Error: The hosted zone was not created via CLI.")
        return

    change_batch = {
        'Changes': [
            {
                'Action': action.upper(),
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': record_type,
                    'TTL': 60,
                    'ResourceRecords': [{'Value': record_value}]
                }
            }
        ]
    }

    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch=change_batch
    )
    
    click.echo(f"DNS Record Changed: {response}")


if __name__ == '__main__':
    cli()
