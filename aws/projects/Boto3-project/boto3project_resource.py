import json
from datetime import datetime
import boto3
from tabulate import tabulate

# Define the tag key values
label_start_time = "SchedulerStartTime"
label_stop_time = "SchedulerStopTime"

# Create EC2 and S3 resource objects
ec2_resource = boto3.resource('ec2')
s3_resource = boto3.resource('s3')

def get_instance_tag_value(key, tags):
    value = None
    for tag in tags:
        if tag['Key'] == key:
            value = tag['Value']
            break
    return value

def get_instances_with_tag(list_of_keys):
    instances = []
    for instance in ec2_resource.instances.filter(Filters=[{'Name': 'tag-key', 'Values': list_of_keys}]):
        instances.append(instance)
    return instances

def table_it():
    instances = get_instances_with_tag([label_start_time])
    table_data = []
    for instance in instances:
        instance_id = instance.id
        instance_state = instance.state['Name']
        instance_tags = instance.tags
        table_data.append([instance_id, instance_state, instance_tags])
    headers = ["Instance ID", "Instance State", "Instance Tags"]
    return tabulate(table_data, headers, tablefmt="grid")

def process_instance(instance, current_hour):
    instance_id = instance.id
    instance_state = instance.state['Name']
    instance_tags = instance.tags

    print(f"Checking instance {instance_id}")

    do_nothing = True

    if instance_state == "running":
        stop_time_tag = get_instance_tag_value(label_stop_time, instance_tags)
        if stop_time_tag is not None and stop_time_tag.isdigit() and int(stop_time_tag) == current_hour:
            do_nothing = False
            result = f"Stopping instance {instance_id}"
            instance.stop()
    elif instance_state == "stopped":
        start_time_tag = get_instance_tag_value(label_start_time, instance_tags)
        if start_time_tag is not None and start_time_tag.isdigit() and int(start_time_tag) == current_hour:
            do_nothing = False
            result = f"Starting instance {instance_id}"
            instance.start()
    
    if do_nothing:
        result = f"{instance_id} is in {instance_state}. Therefore there is no action required at the moment."

    return result

def process_instances():
    instances = get_instances_with_tag([label_start_time])
    if not instances:
        return_status = "No instances found."
    else:
        print(f"Found {len(instances)} instances to process")
        now = datetime.now()
        current_hour = int(now.strftime('%H'))
        print(f"Current hour is {current_hour}")
        for instance in instances:
            message = process_instance(instance, current_hour)
            print(message)
        return_status = "Finished processing all instances."
    return return_status

def process_bucket(bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    versioning = bucket.Versioning()
    if versioning.status == 'Enabled':
        result = f"Versioning is enabled on bucket {bucket_name}"
    else:
        versioning.enable()
        result = f"Enabling versioning on bucket {bucket_name}"
    return result

def process_buckets():
    prefix = "aslan"
    bucket_list = list(s3_resource.buckets.all())
    if not bucket_list:
        return_status = "No buckets found."
    else:
        print(f"Found {len(bucket_list)} buckets to process")
        for bucket in bucket_list:
            bucket_name = bucket.name
            if bucket_name.startswith(prefix):
                message = process_bucket(bucket_name)
            else:
                message = f"Skipping bucket {bucket_name}"
            print(message)
        return_status = "Finished processing all buckets."
    return return_status

def lambda_handler(event, context):
    try:
        ec2_status = process_instances()
        s3_status = process_buckets()
        return_code = 200
        return_status = f"{ec2_status} {s3_status}"
    except Exception as e:
        return_code = 500
        return_status = f"Unexpected error occurred: {e}"
    finally:
        print(return_status)
        return {"statusCode": return_code, "body": json.dumps(return_status)}

if __name__ == "__main__":
    lambda_handler(None, None)
