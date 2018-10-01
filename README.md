# AWS-Snapshot-Delete
A Python script used to batch delete AWS snapshots matching the supplied criteria.

## Usage Examples
* `python3 delete_snapshots.py --verbose --age 7` - Show a list of all snapshots that are to be deleted, but not delete them
* `python3 delete_snapshots.py --delete --verbose --age 7` - delete all snapshots that are older than 7 days old
* `python3 delete_snapshots.py --profile test --delete` - delete all snapshots using the 'test' profile
* `python3 delete_snapshots.py --filter "[{'Name':'tag:Test', 'Values':['yes']}]" --delete`  - delete all snapshots that have the tag "Test" with a value of "yes"

## Options
* --filter , -f : JSON formatted string to filter Snapshots
* --profile , -p : AWS Profile to use, the default is the 'default' profile
* --age , -a : The age in days you want to keep i.e: `--age 7` will delete snapshots older than 7 days old
* --delete , -d : Specify to delete snapshots, if this option is not supplied the snapshots will not be deleted
* --verbose , -v : Option to give verbose output
* --quiet , -q : Option to give no output

## Requirements
* Python 3
* boto3
* awscli
