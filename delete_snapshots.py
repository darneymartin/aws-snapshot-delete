#!/usr/bin/env python3
import sys
import boto3
import argparse
import json
from datetime import datetime, timedelta, timezone

# Define Globals
VERSION = '0.0.2'
ARG_HELP ="""

                          delete_snapshots.py   (v{0})
--------------------------------------------------------------------------------
Use to delete Snapshots in AWS that match the given criteria, can be used to
delete snapshots based on time and/or filters. Requires the boto3 module
Usage:
    python3 delete_snapshots.py --delete --verbose --age 7

    ** Having trouble with filters? Use '' around the JSON **
--------------------------------------------------------------------------------
""".format(VERSION)

################################################################################
#
# Function: main
# Description: This function is responsible for applying the appropriate actions
# that are passed into the 'args' variable
#
################################################################################
def main(args):
    session = boto3.Session(profile_name=args.profile)
    ec2 = session.client('ec2')

    # Check if filter parameter is defined
    if args.filter is not None:
        try:
            filters = json.loads(args.filter)
        except Exception as e:
            raise
            exit(1)
        snapshots = ec2.describe_snapshots(Filters=filters)
    else:
        snapshots = ec2.describe_snapshots()


    delete_snapshots = []
    # Check if age parameter is defined
    if args.age is not None:
        output("Deleting any snapshots older than "+str(args.age)+" days", "", args)
        delete_time = datetime.now(timezone.utc) - timedelta(days=args.age)
        for snapshot in snapshots["Snapshots"]:
            start_time = snapshot['StartTime']
            if start_time < delete_time:
                delete_snapshots.append(snapshot['SnapshotId'])
    else:
        for snapshot in snapshots["Snapshots"]:
            delete_snapshots.append(snapshot['SnapshotId'])
    deletion_counter = 0
    size_counter = 0
    for snapshot in snapshots["Snapshots"]:
        if snapshot['SnapshotId'] in delete_snapshots:
            deletion_counter = deletion_counter + 1
            size_counter = size_counter + snapshot['VolumeSize']
            if args.delete is True:
                output("Deleting "+ str(snapshot['SnapshotId']),"Description:"+str(snapshot['Description']), args)
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'],DryRun=False)
            else:
                output("Warning: Snapshot "+ str(snapshot['SnapshotId']) +" not deleted! (add -d or --delete option)", "Description:"+str(snapshot['Description']), args)
    output("Deleted "+str(deletion_counter)+" snapshots totalling "+str(size_counter)+"GB", "", args)

################################################################################
#
# Function: output
# Description: Print out the String passed into the function denoted by the
# parameter 'str_out' unless the parameter 'args.verbose' is set to False
#
################################################################################
def output(str_out, verbose, args):
    if args.verbose == True:
        print(str_out+" "+verbose)
    else:
        print(str_out)

################################################################################
#
# This is the start of the program
#
################################################################################
if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(description=ARG_HELP, formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        args.add_argument('--filter','-f', dest='filter', type=str, help="JSON formatted string to filter Snapshots")
        args.add_argument('--profile','-p', dest='profile', type=str, default="default", help="Profile to use (Default: default)")
        args.add_argument('--age','-a', dest='age', type=int, help='The max age in days you want to keep')
        args.add_argument('--delete','-d', dest='delete', action='store_true', help='Specify to delete Snapshots')
        args.add_argument('--verbose','-v', dest="verbose", action='store_true', help="Show verbose output of program")
        args = args.parse_args()
        # Launch Main
        main(args)
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        exit(1)
    exit(0)
