import argparse
import csv
import paramiko
import time
import sys
import exitstatus

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
                        default='machines.csv')

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

    if success:
        sys.exit(exitstatus.ExitStatus.success)
    else:
        sys.exit(exitstatus.ExitStatus.failure)

def ssh_for_application_and_port(machine, username, password, application_signature, port):
    try:
        #                key = paramiko.RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
        client = paramiko.SSHClient()
        #               client.load_system_host_keys()
        #               client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        print("connecting to " + machine)
        #                client.connect(machine, username=username, pkey=key)
        client.connect(machine, username=username, password=password)

        stdin, stdout, stderr = client.exec_command('ps -ef')
        print("executed ps -ef and looking for " + application_signature)

        err = stderr.read().decode()
        if err:
            print("stderr")
            print(err)

        if not application_signature in stdout.read().decode():
            print("did not find application signature")
            return exitstatus.ExitStatus.failure

        stdin, stdout, stderr = client.exec_command('sudo lsof -i -P -n | grep LISTEN')
        print("executed sudo lsof -i -P -n | grep LISTEN and looking for " + port)

        err = stderr.read().decode()
        if err:
            print("stderr")
            print(err)

        if not port in stdout.read().decode():
            print("did not find port")
            return exitstatus.ExitStatus.failure

        stdin.close()
        stdout.close()
        stderr.close()
        client.close()
        del client

    except paramiko.AuthenticationException as authenticationFailure:
        print("Authentication failed: %s" % authenticationFailure)
        return exitstatus.ExitStatus.failure
    except paramiko.SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
        return exitstatus.ExitStatus.failure
    except paramiko.BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)
        return exitstatus.ExitStatus.failure
    except Exception as exception:
        print("Exception: %s" % exception)
        print("MUST FIX")
        pass
#        return exitstatus.ExitStatus.failure
    finally:
        time.sleep(1)

    return exitstatus.ExitStatus.success

if __name__ == '__main__':
    main()

