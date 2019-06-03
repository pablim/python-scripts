def contrato_dependencia(matricula_id, dependencia_id):
    import json
    import os.path
    import io
    import pickle
    import pdfkit
    import datetime
    import time
    from weasyprint import HTML, CSS
    from apiclient import discovery
    from googleapiclient.http import MediaIoBaseDownload
    from googleapiclient.http import MediaFileUpload
    from httplib2 import Http
    from oauth2client import client
    from oauth2client import file
    from oauth2client import tools
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    # dependencia_id = request.vars.dependencia_id

    usuario_id = auth.user.id
    pessoa = db(db.pessoa.usuario == usuario_id).select().first()

    dependencia = db(
        (db.dependencia.id == dependencia_id) &
        (db.matriz.id == db.dependencia.matriz) &
        (db.curso.id == db.matriz.curso) &
        (db.disciplina.id == db.dependencia.disciplina) &
        (db.dependencia.calendario == db.calendario.id) &
        (db.dependencia.preco == db.preco.id)
    ).select().first()

    print('aqui erro')
    print(dependencia_id)
    print(dependencia)

    folder = request.folder

    # Set the scopes and discovery info
    SCOPES = ['https://www.googleapis.com/auth/drive']

    TOKEN = os.path.join(os.path.join(folder, 'private','token.pickle'))
    CREDENTIALS = os.path.join(os.path.join(folder, 'private','credentials.json'))

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN):
        with open(TOKEN, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open(TOKEN, 'wb') as token:
            pickle.dump(creds, token)

    drive_service = discovery.build('drive', 'v3', credentials=creds)
    docs_service = discovery.build('docs', 'v1', credentials=creds)

    contrato_dependencia = db(
        (db.contrato.tipo == 3) &
        (db.contrato.inicio_validade <= datetime.datetime.now()) &
        (db.contrato.fim_validade >= datetime.datetime.now())
    ).select().first()
    print(datetime.datetime.now())
    print(contrato_dependencia)
    # file_id = '1ogqWtDKWK7Yzv9kMCV_OjzXUnVQl6jdZCLdKoRgkEnY'
    file_id = contrato_dependencia.codigo_drive

    # customer_name = 'Alice'
    pasta_contatos_id = '18r1sUgnI_Y9Cu5ERhjkG4lkOwk_yb4nP'
    date = datetime.datetime.now().strftime("%y/%m/%d")
    ano = datetime.datetime.now().strftime("%Y")
    mes = datetime.datetime.now().strftime("%m")

    curso_id = dependencia.curso.id

    calendario = db(
        (db.calendario.ano == ano) &
        (db.calendario.mes_inicio < mes) &
        (db.calendario.mes_fim > mes) &
        (db.calendario.nivel == 4) &
        (db.calendario.modalidade == 1)
    ).select().first()
    print(calendario)

    profissao = db(db.profissao.id == pessoa.profissao).select(db.profissao.nome).first()

    valor_parcela = dependencia.preco.valor
    parcelas = dependencia.preco.parcelamento

    numero_parcelas_extenso = extenso_normal(str(parcelas))
    reais_centavos = str(valor_parcela).split('.')
    reais = reais_centavos[0]
    centavos = reais_centavos[1]
    valor_parcela_extenso = extenso(reais, centavos)

    valor_total = valor_parcela * parcelas
    reais_centavos = str(valor_total).split('.')
    reais = reais_centavos[0]
    centavos = reais_centavos[1]
    valor_total_extenso = extenso(reais, centavos)

    requests = []
    requests.append(get_replace_field('pessoa.id', str(pessoa.id)))
    requests.append(get_replace_field('pessoa.nome', pessoa.nome + ' ' + pessoa.sobrenome))
    requests.append(get_replace_field('pessoa.cpf', pessoa.cpf))
    requests.append(get_replace_field('pessoa.rg', pessoa.rg))
    requests.append(get_replace_field('pessoa.endereco', pessoa.endereco))
    requests.append(get_replace_field('pessoa.numero', str(pessoa.numero)))
    requests.append(get_replace_field('pessoa.bairro', pessoa.bairro))
    requests.append(get_replace_field('pessoa.cidade', str(pessoa.cidade)))
    requests.append(get_replace_field('pessoa.uf', str(pessoa.uf)))
    requests.append(get_replace_field('pessoa.cep', pessoa.cep))
    requests.append(get_replace_field('pessoa.email', pessoa.email))
    requests.append(get_replace_field('pessoa.celular', pessoa.celular))
    requests.append(get_replace_field('pessoa.nome_social', ''))
    requests.append(get_replace_field('pessoa.nome_pai', pessoa.nome_pai))
    requests.append(get_replace_field('pessoa.nome_mae', pessoa.nome_mae))
    requests.append(get_replace_field('pessoa.nacionalidade', pessoa.nacionalidade))
    requests.append(get_replace_field('pessoa.profissao', profissao.nome))
    requests.append(get_replace_field('pessoa.estado_civil', pessoa.estado_civil))

    requests.append(get_replace_field('disciplina_dependencia', dependencia.disciplina.nome))
    requests.append(get_replace_field('curso', dependencia.curso.nome))
    requests.append(get_replace_field('habilitacao', dependencia.curso.descricao))
    requests.append(get_replace_field('semestre', '1' if dependencia.calendario.mes_inicio < 6 else '2' ))
    requests.append(get_replace_field('ano', str(dependencia.calendario.ano)))

    requests.append(get_replace_field('valor', str(valor_total)))
    requests.append(get_replace_field('valor_extenso', str(valor_total_extenso)))
    requests.append(get_replace_field('numero_parcelas', str(parcelas)))
    requests.append(get_replace_field('numero_parcelas_extenso', str(numero_parcelas_extenso)))
    requests.append(get_replace_field('valor_parcela', str(valor_parcela)))
    requests.append(get_replace_field('valor_parcela_extenso', str(valor_parcela_extenso)))

    # busca diretórios
    dir_contrato_id = '18r1sUgnI_Y9Cu5ERhjkG4lkOwk_yb4nP'

    # Busca pasta do ano atual
    dirs = drive_service.files().list(
        q="name='"+ano+"' and mimeType='application/vnd.google-apps.folder'" \
            "and '" +dir_contrato_id+ "' in parents"
    ).execute()

    # Cria pasta do ano atual caso não tenha sido criada
    if not dirs.get('files'):
        dir_ano = drive_service.files().create(
            body={
                'mimeType':'application/vnd.google-apps.folder',
                'parents':[dir_contrato_id],
                'name':str(ano)
            }
        ).execute()
        dir_ano_id = dir_ano.id
    else:
        dir_ano = dirs.get('files')
        dir_ano_id = dir_ano[0]['id']

    # Busca pasta do curso
    dirs = drive_service.files().list(
        q="name='"+str(curso_id)+"' and mimeType='application/vnd.google-apps.folder'" \
            "and '" +dir_ano_id+ "' in parents"
    ).execute()

    # Cria pasta do curso caso não tenha sido criada
    if not dirs.get('files'):
        dir_curso = drive_service.files().create(
            body={
                'mimeType':'application/vnd.google-apps.folder',
                'parents':[dir_ano_id],
                'name':str(curso_id)
            }
        ).execute()
    else:
        dir_curso = dirs.get('files')
        dir_curso_id = dir_curso[0]['id']


    new_file = drive_service.files().copy(
        body={
            'fileId': file_id,
            'mimeType':'application/vnd.google-apps.file',
            'name':'contrato_'+str(pessoa.id)+'_'+str(matricula_id),
            'parents':[dir_curso_id],
            # 'name': str(pessoa.nome + ' ' + pessoa.sobrenome)
        },
        fileId=file_id,
    ).execute()
    print ('File ID: %s' % new_file.get('id'))

    # subistitui campos
    result = docs_service.documents().batchUpdate(
        documentId=new_file.get('id'), body={'requests': requests}
    ).execute()

    documento_id = db.documento.insert(
        nome='contrato_'+str(pessoa.id)+'_'+str(matricula_id),
        arquivo=None,
        id_ged=None,
        codigo_drive=new_file.get('id')
    )

    db.contrato_matricula.insert(
        contrato=documento_id,
        contratante=pessoa.id,
        codigo_aceitacao=None,
        data_aceite=datetime.date.today(),
    )

    # definindo permissões
    permissao = drive_service.permissions().create(
        body={
            'fileId': new_file.get('id'),
            'role':'reader',
            'type':'anyone',
            'allowFileDiscovery':False,
            # 'emailAddress':''
        },
        fileId=new_file.get('id'),
    ).execute()




    return new_file.get('id')
