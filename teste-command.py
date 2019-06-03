import subprocess
import sys
import paramiko

HOST="172.16.0.5"
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND="ls"


# ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
#                        shell=False,
#                        stdout=subprocess.PIPE,
#                        stderr=subprocess.PIPE)
#
# result = ssh.stdout.readlines()
# if result == []:
#     error = ssh.stderr.readlines()
#     print (sys.stderr, "ERROR: %s" % error)
# else:
#     print(result)
#


ssh = paramiko.SSHClient()
ssh.connect(HOST, username='mouf', password='@ Fuom foi fundada em 1963')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')

print("pronto")
