# aws-snapshot-delete
A Python script used to batch delete AWS snapshots matching the supplied criteria. This script provides an easier way of deleting AWS EC2 Snapshots by wrapping the boto3 module and using a much simpler API for common problems like: deleting snapshots by age, or viewing snapshots that will be deleted based on certain filters.

## Setup
Follow the steps to install all of the requirements.
* `git clone https://github.com/darneymartin/aws-snapshot-delete.git`
* `cd aws-snapshot-delete`
* `pip3 install -r requirements.txt`

## Usage
* `python3 delete_snapshots.py --verbose --age 7` - Show a list of all snapshots that are to be deleted, but not delete them
* `python3 delete_snapshots.py --delete --verbose --age 7` - delete all snapshots that are older than 7 days old
* `python3 delete_snapshots.py --profile test --delete` - delete all snapshots using the 'test' profile
* `python3 delete_snapshots.py --filter '[{"Name":"tag:Test", "Values":["yes"]}]' --delete`  - delete all snapshots that have the tag "Test" with a value of "yes"

## Options
* --filter , -f : JSON formatted string to filter Snapshots
* --profile , -p : AWS Profile to use, the default is the 'default' profile
* --age , -a : The age in days you want to keep i.e: `--age 7` will delete snapshots older than 7 days old
* --delete , -d : Specify to delete snapshots, if this option is not supplied the snapshots will not be deleted
* --verbose , -v : Option to give verbose output

## Requirements
* Python 3
* boto3
* awscli
