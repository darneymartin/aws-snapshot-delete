#!/usr/bin/env python3
import sys
import boto3
import argparse
import json
import re
from datetime import datetime, timedelta, timezone

ARG_HELP ="""
                              delete_snapshots.py
    --------------------------------------------------------------------------------
    Use to delete Snapshots in AWS that match the given criteria, can be used to
    delete snapshots based on time and/or filters. Requires the boto3 module
    Usage:
        python3 delete_snapshots.py --delete --verbose --age 7

        ** Having trouble with filters? Use '' around the JSON **
    --------------------------------------------------------------------------------
    """

def main(args):
    session = boto3.Session(profile_name=args.profile)
    ec2 = session.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])
    if args.description is not None:
        pattern = re.compile(args.description)
    else:
        pattern = re.compile(r".*")
    print("Deleting any snapshots older than {0} days".format(args.age))
    delete_time = datetime.now(timezone.utc) - timedelta(days=args.age)
    size_counter = 0
    delete_count = 0
    for snapshot in snapshots["Snapshots"]:
        start_time = snapshot['StartTime']
        if((start_time < delete_time) and (re.search(pattern,snapshot['Description']) is not None)):
            size_counter = size_counter + snapshot['VolumeSize']
            delete_count = delete_count + 1
            if args.delete is True:
                print("Deleting {0} {1}".format(snapshot['SnapshotId'], "Description: {0}".format(snapshot['Description']) * args.verbose))
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'],DryRun=False)
            else:
                print("Warning: Snapshot {0} not deleted! (add -d or --delete option) {1}".format(snapshot['SnapshotId'], "Description: {0}".format(snapshot['Description']) * args.verbose))
    print("Deleted {0} snapshots totalling {1}GB".format(delete_count, size_counter))

################################################################################
#
# This is the start of the program
#
################################################################################
if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(description=ARG_HELP, formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        #args.add_argument('--filter','-f', action=JsonAction, default={}, help="JSON formatted string to filter Snapshots")
        args.add_argument('--profile','-p', dest='profile', type=str, default="default", help="Profile to use (Default: default)")
        args.add_argument('--age','-a', dest='age', type=int, default=0, help='The max age in days you want to keep')
        args.add_argument('--delete','-d', dest='delete', action='store_true', help="Specify to delete Snapshots")
        args.add_argument('--verbose','-v', dest='verbose', action='store_true', help="Show verbose output of program")
        args.add_argument('--description', dest='description', type=str, default=None, help="Description of snapshot(s) can be a regex")
        args = args.parse_args()
        # Launch Main
        main(args)
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        exit(1)
    exit(0)
