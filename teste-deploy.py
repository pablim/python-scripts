import pysftp
import sys

# with pysftp.Connection('172.16.0.5', username='mouf',
#         password='@ Fuom foi fundada em 1963') as sftp:
#     with sftp.cd('/home'):             # temporarily chdir to public
#         sftp.put('/home/pablo/enviar-producao/vazio.txt')  # upload file to public/ on remote
        # sftp.get('remote_file')         # get a remote file

home = '/home/pablo/'
folder = 'enviar-producao/'

modulos_ejb = 'modulos_ejb'

if sys.argv[1] == '-ejb':
    print(sys.argv[2])
    if 3 in sys.argv:
        print(sys.argv[3])
    else:
        print('informe o nome do projeto')

    print('scp '+home+folder+sys.argv[2] + '.ear' + ' mouf@172.16.0.5:/home/'+modulos_ejb)
    print('scp '+home+folder+sys.argv[3] + '.ear' + ' mouf@172.16.0.5:/home/jboss_'+sys.argv[3]+'/server/app_'+sys.argv[3]+'/deploy')

    # os.system('scp '+home+folder+sys.argv[2] + ' mouf@172.16.0.5:/home/'+modulos_ejb)

elif sys.argv[1] == '-files':
    print(sys.argv[2])
    print(sys.argv[3])
    print(sys.argv[4])

else:
    print(sys.argv[1])



# os.system('scp /home/pablo/teste.txt  mouf@172.16.0.5:/home')
