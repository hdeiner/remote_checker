import argparse
import csv
import sys
import exitstatus

from ssh_for_application_and_port import ssh_for_application_and_port

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Sample DevOps Tool',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        help='CSV file for machines, userids, passwords, ps entry, port',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='localhost.csv')

    args = parser.parse_args()

    return args

def main():
    args = get_args()
    success = True

    with args.file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            machine=row['machine']
            username=row['username']
            password=row['password']
            application_signature=row['application_signature']
            port=row['port']
            success = success and (ssh_for_application_and_port(machine,username, password, application_signature, port) == exitstatus.ExitStatus.success)
            print()

    if success:
        sys.exit(exitstatus.ExitStatus.success)
    else:
        sys.exit(exitstatus.ExitStatus.failure)

if __name__ == '__main__':
    main()

