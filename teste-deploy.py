import pysftp


print("enviando")

with pysftp.Connection('172.16.0.5', username='mouf',
        password='@ Fuom foi fundada em 1963') as sftp:
    with sftp.cd('/home'):             # temporarily chdir to public
        sftp.put('/home/pablo/enviar-producao/vazio.txt')  # upload file to public/ on remote
        # sftp.get('remote_file')         # get a remote file



print("enviando")
