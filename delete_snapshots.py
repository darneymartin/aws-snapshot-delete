import sys
import boto3
import argparse
from datetime import datetime, timedelta, timezone
#filters = [{'Name':'tag:CreateType', 'Values':['auto']}]

VERSION = '0.0.1'
ARG_HELP ="""

                          delete_snapshots.py   (v{0})
--------------------------------------------------------------------------------
Use to delete Snapshots in AWS that match the given criteria, can be used to
delete snapshots based on time and/or filters. Requires the boto3 module
Usage:
    python3 delete_snapshots.py --delete --verbose --age 7

    ** Having trouble with filters? Use "" around the JSON **
--------------------------------------------------------------------------------
""".format(VERSION)

def main(args):
	session = boto3.Session(profile_name=args.profile)
	ec2 = session.client('ec2')

	# Check if filter parameter is defined
	if args.filter is not None:
		snapshots = ec2.describe_snapshots(Filters=filters)
	else:
		snapshots = ec2.describe_snapshots()

	delete_snapshots = []
	# Check if age parameter is defined
	if args.age is not None:
		output("Deleting any snapshots older than "+str(args.age)+" days", args)
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
			output("Deleting "+ str(snapshot['SnapshotId']), args)
			deletion_counter = deletion_counter + 1
			size_counter = size_counter + snapshot['VolumeSize']
			if args.delete is not None:
				ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'],DryRun=False)
			else:
				output("Warning: Snapshot not deleted! (add -d or --delete option)", args)
			output("Deleted "+str(deletion_counter)+" snapshots totalling "+str(size_counter)+"GB", args)

def output(str_out, level, args):
	if args.verbose == True:
		print(str_out)
	else:
		pass



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
		args.add_argument('--age','-a', dest='age', type=int, help='The max age in days you want to keep (Default: 30)')
		args.add_argument('--delete','-d', dest='delete', action='store_true', help='Specify to delete Snapshots')
		args.add_argument('--verbose','-v', dest="verbose", action='store_true', help="Show verbose output of program")
		args.add_argument('--quiet','-q', dest="quiet", action='store_true', help="Run program in quiet mode")
		args = args.parse_args()
		# Launch Main
		main(args)
	except KeyboardInterrupt:
		print("\n[!] Key Event Detected...\n\n")
		exit(0)
