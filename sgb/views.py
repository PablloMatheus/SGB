from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError
from datetime import datetime
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from sgb.forms import (ProfessorForm, AlunoForm, NewForm, LoginForm, TccForm,
    SalasForm, BancaForm, DispForm, CursoForm)
from sgb.models import (Professor, Aluno, Tcc, Salas, Banca, Disponibilidade,
    Curso)


################################################################################
#                                                                              #
#                                LÓGICAS DIVERSAS                              #
#                                                                              #
################################################################################

#View que lista todos os objetos de Aluno e Professor,
    #que são tratados com javascript para gerar uma pesquisa
    #das duas listas no html.
def pesquisa_global(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        #Armazena em "lista_disp" todos os objetos de disponibilidade
            # que ainda não foram atribuidos a uma banca.
        #(1= não foram atribuidos a nenhuma banca, 2= foram atribuidos
            #a alguma banca)
        data['lista_professores'] = Professor.objects.all()
        data['lista_alunos'] = Aluno.objects.all()
        return render(request, 'pesquisa_global.html', data)

#View que lista os objetos de Disponibilidade e Banca no calendario.
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        data = {}
        data['lista_disp'] = Disponibilidade.objects.filter(situacao='1')
        data['lista_bancas'] = Banca.objects.all()
        return render(request, 'index.html', data)

#View responsável por gerar o calenario em tela cheia, acessivel pela aba
    #"calendario" na navbar do index.
def calendar(request):
    if not request.user.is_authenticated():
        return render(request, 'calendar.html')
    else:
        data = {}
        data['lista_disp'] = Disponibilidade.objects.all()
        return render(request, 'calendar.html', data)
        # return HttpResponseRedirect('/login/')

#View responsável por mandar a variável 'time' para o html de relatorios.
def datetimenow(request):
    return render_to_response("relatorios.html", {
    'time': datetime.now(),
    }, context_instance=RequestContext(request))

#View principal de relatorios, envia a banca de acordo com o pk(chave primaria)
    #para o html de relatorios.
def testerel(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        banca = get_object_or_404(Banca, pk=pk)
        bancas = Banca.objects.get(pk=pk)
        return render(request, 'relatorios.html', {'form' : banca,
    'object':bancas})

#View principal de etiquetas responsável por enviar a banca de acordo com o pk para o html
    #de etiquetas.
def etiqueterel(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        banca = get_object_or_404(Banca, pk=pk)
        bancas = Banca.objects.get(pk=pk)
        return render(request, 'etiquetas.html', {'form':banca, 'object':bancas})

#View princpal de declaracão, responsavel por receber o pk de professor e
    #receber as bancas das quais ele participou.
def declaracao(request, pk, curso):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        else:
            # q = declarogica(pk)
            professor = Professor.objects.get(pk=pk)
            time = datetime.now().date()
            #Variavel usada para printar tal texto quando o curso do tcc da
                #banca for tecnologo.
            text = "CURSO TECNOLÔGICO EM"
            #Estes ifs recebem o objeto curso da tabela curso/coordenador de
                #acordo com o curso do tcc da banca que o professor em questão
                #avaliou.
            if curso == 'cc':
                coord = Curso.objects.get(curso_nome='Ciência da Computação')
                if coord.coordenador.pk == professor.pk:
                    coord = Curso.objects.get(curso_nome='Sistemas para Internet')
                text = "CURSO BACHARELADO EM"
            elif curso == 'gti':
                coord = Curso.objects.get(curso_nome='Gestão da Tecnologia da Informação')
                if coord.coordenador.pk == professor.pk:
                    coord = Curso.objects.get(curso_nome='Ciência da Computação')
            elif curso == 'spi':
                coord = Curso.objects.get(curso_nome='Sistemas para Internet')
                if coord.coordenador.pk == professor.pk:
                    coord = Curso.objects.get(curso_nome='Ciência da Computação')
            else:
                coord = Curso.objects.get(curso_nome='Redes de Computadores')
                if coord.coordenador.pk == professor.pk:
                    coord = Curso.objects.get(curso_nome='Ciência da Computação')
            #Converte a variavel abreviada para o nome completo do curso
            if curso == 'cc':
                curso = 'Ciência da Computação'
            elif curso == 'gti':
                curso = 'Gestão da Tecnologia da Informação'
            elif curso == 'spi':
                curso = 'Sistemas para Internet'
            else:
                curso = 'Redes de Computadores'
            #Banca é uma lista que recebe as bancas onde esse professor(pk) é
            #examinador 1, ou/e examinador 2, ou/e orientador, a mesma será
            #usada na lógica a seguir.
            banca = []
            blista = Banca.objects.filter(examinador_1__examinador__pk=pk,
             titulo_tcc__aluno__curso=curso)
            for item in blista:
                banca.append(item)
            blista = Banca.objects.filter(examinador_2__examinador__pk=pk,
             titulo_tcc__aluno__curso=curso)
            for item in blista:
                banca.append(item)
            blista = Banca.objects.filter(titulo_tcc__orientador__pk=pk,
             titulo_tcc__aluno__curso=curso)
            for item in blista:
                banca.append(item)
            q = banca
            #Cont armazena a quantidade de elementos contidos na lista banca,
            #na logica abaixo organizamos a impressão da declaração de Bancas
            #de professor.
            cont = len(banca)
            largura = []
            if cont == 4:
                #x[inicia em:para antes:pula]
                bancap2 = q[:3]
                banca = q[:4]
            elif cont > 4:
                bancap2 = q[4:]
                banca = q[:4]
            else:
                banca = q
                bancap2 = None
            return render(request, 'declaracao.html', {'object':professor,
        'banca':banca, 'curso':curso,'cont':cont, 'bancap2':bancap2,
        'time':time, 'coord': coord, 'text':text})

#Verifica se examinador1,2 e orientador existem e popula a variavel banca com
#trabalhos em que este professor atuou.
def declarogica(pk):
    professor = Professor.objects.get(pk=pk)
    examinador1 = Banca.objects.filter(examinador_1__examinador=professor)
    examinador2 = Banca.objects.filter(examinador_2__examinador=professor)
    orientador = Banca.objects.filter(titulo_tcc__orientador=pk)
    bancas = None
    if examinador1.exists() or examinador2.exists() or orientador.exists():
        bancas = Banca.objects.filter(Q(examinador_1__examinador=professor) |
        Q(examinador_2__examinador=professor) | Q(titulo_tcc__orientador=pk))
    return bancas


################################################################################
#                                                                              #
#                                  CRUDS                                       #
#                                                                              #
################################################################################

                        #############################
                        #                           #
                        #    VIEWS DE LISTAGEM      #
                        #                           #
                        #############################

#View responsavel por enviar a lista de professores para a html de professor.
def professor_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['lista_professores'] = Professor.objects.all()
        return render(request, 'professor.html', data)

def aluno_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['lista_alunos'] = Aluno.objects.all()
        return render(request, 'aluno.html', data)

def salas_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['lista_salas'] = Salas.objects.all()
        return render(request, 'salas.html', data)

def curso_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['lista_curso'] = Curso.objects.all()
        return render(request, 'curso.html', data)

def tcc_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['lista_tcc'] = Tcc.objects.all()
        return render(request, 'tcc.html', data)

def banca_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['titulo'] = 'Bancas '
        data['br'] = '<br>'
        data['v'] = '<div style="width: 180px; word-wrap: break-word;">'
        data['v1'] = '</div>'
        data['lista_bancas'] = Banca.objects.all()
        periodo = Banca.objects.all().first()
        if periodo:
            data['ano']=periodo.data_banca.year
            if periodo.data_banca.month>=6:
                data['periodo']=2
            else:
                data['periodo']=1
        return render(request, 'banca.html', data)

def listar_cc(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        else:
            data = {}
            data['titulo'] = 'Curso Ciência da Computação - Banca do 8° periodo - '
            data['br'] = '<br>'
            data['v'] = '<div style="width: 180px; word-wrap: break-word;">'
            data['v1'] = '</div>'
            data['lista_bancas'] = Banca.objects.filter(titulo_tcc__aluno__curso='Ciência da Computação')
            periodo = Banca.objects.filter(titulo_tcc__aluno__curso='Ciência da Computação').first()
            if periodo:
                data['ano']=periodo.data_banca.year
                if periodo.data_banca.month>=6:
                    data['periodo']=2
                else:
                    data['periodo']=1
            return render(request, 'banca.html', data)

def listar_spi(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        else:
            data = {}
            data['titulo'] = 'Curso Sistemas para Internet - Banca do 5° periodo - '
            data['br'] = '<br>'
            data['v'] = '<div style="width: 180px; word-wrap: break-word;">'
            data['v1'] = '</div>'
            data['lista_bancas'] = Banca.objects.filter(titulo_tcc__aluno__curso='Sistemas para Internet')
            periodo = Banca.objects.filter(titulo_tcc__aluno__curso='Sistemas para Internet').first()
            if periodo:
                data['ano']=periodo.data_banca.year
                if periodo.data_banca.month>=6:
                    data['periodo']=2
                else:
                    data['periodo']=1
            return render(request, 'banca.html', data)

def listar_gti(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        else:
            data = {}
            data['titulo'] = 'Curso Gestão da Tecnologia da Informação - Banca do 5° periodo - '
            data['br'] = '<br>'
            data['v'] = '<div style="width: 180px; word-wrap: break-word;">'
            data['v1'] = '</div>'
            data['lista_bancas'] = Banca.objects.filter(titulo_tcc__aluno__curso='Gestão da Tecnologia da Informação')
            periodo = Banca.objects.filter(titulo_tcc__aluno__curso='Gestão da Tecnologia da Informação').first()
            if periodo:
                data['ano']=periodo.data_banca.year
                if periodo.data_banca.month>=6:
                    data['periodo']=2
                else:
                    data['periodo']=1
            return render(request, 'banca.html', data)

def listar_rc(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        else:
            data = {}
            data['titulo'] = 'Curso Redes de Computadores - Banca do 5° periodo - '
            data['br'] = '<br>'
            data['v'] = '<div style="width: 180px; word-wrap: break-word;">'
            data['v1'] = '</div>'
            data['lista_bancas'] = Banca.objects.filter(titulo_tcc__aluno__curso='Redes de Computadores')
            periodo = Banca.objects.filter(titulo_tcc__aluno__curso='Redes de Computadores').first()
            if periodo:
                data['ano']=periodo.data_banca.year
                if periodo.data_banca.month>=6:
                    data['periodo']=2
                else:
                    data['periodo']=1
            return render(request, 'banca.html', data)

def disp_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['lista_disp'] = Disponibilidade.objects.all()
        return render(request, 'disponibilidade.html', data)

def user_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = {}
        data['lista_usuarios'] = User.objects.all()
        return render(request, 'user.html', data)


                        #############################
                        #                           #
                        #      VIEWS DE CRIAÇÃO     #
                        #                           #
                        #############################

#View responsavel pela criação de professor.
def professor_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        professor_form = ProfessorForm(request.POST or None)
        #Variavel que recebe mensagem de confirmação.
        corf = ''
        if request.method == 'POST':
            if professor_form.is_valid():
                professor_form.save()
                confirm_prof = request.POST['professor_nome']
                corf = 'O PROFESSOR %s FOI CADASTRADO COM SUCESSO' %confirm_prof
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/professor/")
        return render(request, 'professor_novo.html', {'form': professor_form,
                        'sucess_message': corf})

def curso_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        professor = Professor.objects.all().order_by('professor_nome')
        curso_form = CursoForm(request.POST or None)
        confirmacao = None
        if request.method == 'POST':
            if curso_form.is_valid():
                curso_form.save()
                curso_form = CursoForm()
                confirmacao = 'CORDENADOR CADASTRADO COM SUCESSO!'
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/curso/")
        return render(request, 'curso_novo.html', {'form': curso_form,
    'professor': professor, 'sucess_message': confirmacao})

def aluno_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        aluno_form = AlunoForm(request.POST or None)
        confirmacao = None
        if request.method == 'POST':
            if aluno_form.is_valid():
                aluno_form.save()
                nome_aluno = request.POST['aluno_nome']
                confirmacao = 'O ALUNO %s FOI CADASTRADO COM SUCESSO' % nome_aluno
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/aluno/")
        return render(request, 'aluno_novo.html', {'form': aluno_form,
        'sucess_message': confirmacao})

def salas_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        salas_form = SalasForm(request.POST or None)
        salas = Salas.objects.all()
        confirmacao = ''
        if request.method == 'POST':
            if salas_form.is_valid():
                salas_form.save()
                confirmacao = 'SALA CADASTRADA COM SUCESSO'
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/salas/")
        return render(request, 'salas_novo.html', {'form': salas_form,
    'salas': salas, 'sucess_message':confirmacao})

def tcc_create_cc(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        aluno = Aluno.objects.filter(curso='Ciência da Computação').order_by('aluno_nome')
        tcc_form = TccForm(request.POST or None)
        professor = Professor.objects.all().order_by('professor_nome')
        confirmacao = None
        if request.method == 'POST':
            if tcc_form.is_valid():
                tcc_form.save()
                confirmacao = 'Trabalho já cadastrado!!! Verifique se os campos não foram repetidos.'
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/tcc/")
        return render(request, 'tcc_novo_cc.html', {'form': tcc_form,
    'aluno': aluno, 'professor': professor, 'sucess_message': confirmacao})

def tcc_create_gti(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        tcc_form = TccForm(request.POST or None)
        aluno = Aluno.objects.filter(curso='Gestão da Tecnologia da Informação').order_by('aluno_nome')
        professor = Professor.objects.all().order_by('professor_nome')
        confirmacao = None
        if request.method == 'POST':
            if tcc_form.is_valid():
                tcc_form.save()
                confirmacao = 'TRABALHO CADASTRADO COM SUCESSO'
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/tcc/")
        return render(request, 'tcc_novo_gti.html', {'form': tcc_form,
    'aluno': aluno, 'professor': professor, 'sucess_message': confirmacao})

def tcc_create_spi(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        tcc_form = TccForm(request.POST or None)
        aluno = Aluno.objects.filter(curso='Sistemas para Internet').order_by('aluno_nome')
        professor = Professor.objects.all().order_by('professor_nome')
        confirmacao = ''
        if request.method == 'POST':
            if tcc_form.is_valid():
                tcc_form.save()
                confirmacao = 'TRABALHO CADASTRADO COM SUCESSO'
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/tcc/")
        return render(request, 'tcc_novo_spi.html', {'form': tcc_form,
    'aluno': aluno, 'professor': professor, 'sucess_message': confirmacao})

def tcc_create_redes(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        tcc_form = TccForm(request.POST or None)
        aluno = Aluno.objects.filter(curso='Redes de Computadores').order_by('aluno_nome')
        professor = Professor.objects.all().order_by('professor_nome')
        confirmacao = ''
        if request.method == 'POST':
            if tcc_form.is_valid():
                tcc_form.save()
                confirmacao = 'TRABALHO CADASTRADO COM SUCESSO'
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/tcc/")
        return render(request, 'tcc_novo_redes.html', {'form': tcc_form,
    'aluno': aluno, 'professor': professor, 'sucess_message':confirmacao})

def banca_data(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'banca_data.html')

def banca_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        data = request.GET['data']
        time = request.GET['time']

        ex1 = Disponibilidade.objects.filter(situacao='1', data=data, hora_inicio=time)
        ex1count = ex1.count()
        tcc = Tcc.objects.filter(situacao='1')
        erro = 0
        errmsg = ''
        sala = Salas.objects.all()
        form = BancaForm(request.POST or None)
        confirmacao = '' #MATHEUS
        if (ex1count > 1):
            if form.is_valid():
                banca = form.save(commit=False)
                banca.hora_inicio = time
                # banca.hora_termino = time
                banca.data_banca = data
                try:
                    examinador_1 = Disponibilidade.objects.get(pk=request.POST['examinador_1'])
                    examinador_2 = Disponibilidade.objects.get(pk=request.POST['examinador_2'])
                    orientador = Tcc.objects.get(pk=request.POST['titulo_tcc'])
                    orientador = orientador.orientador
                    examinador1 = examinador_1.examinador
                    examinador2 = examinador_2.examinador
                    if (examinador1 == orientador) or (examinador2 == orientador):
                        errmsg = 'Examinadores devem ser diferentes do orientador %s' % orientador
                        erro = 1
                        return render(request, 'banca_novo.html', {
                    'form': form, 'ex1': ex1, 'tcc': tcc,
                    'sucess_message':confirmacao, 'erro': erro,
                    'sala': sala, 'errmsg': errmsg})
                    form.save()
                    examinador_1.situacao ='2'
                    examinador_2.situacao ='2'
                    tcc = Tcc.objects.get(pk=request.POST['titulo_tcc'])
                    tcc.situacao='2'
                    tcc.save()
                    examinador_1.save()
                    examinador_2.save()
                    confirmacao = 'BANCA CADASTRADA COM SUCESSO' #MATHEUS
                    if request.POST.get('btn') == 's':
                        return HttpResponseRedirect("/banca/")
                    return render(request, 'banca_data.html', {'sucess_message': confirmacao}) #MATHEUS
                except IntegrityError as e:
                    if 'unique constraint':
                        erro = 1
                        s = Salas.objects.get(pk=request.POST['sala'])
                        errmsg = 'A sala %s já foi agendada para outra banca nesta mesma data e hora.' % s
            return render(request, 'banca_novo.html', {'form': form,
        'ex1': ex1, 'tcc': tcc, 'sucess_message':confirmacao, 'erro': erro,
        'sala': sala, 'errmsg': errmsg})

        elif(ex1count == 1):
            databr = data.split('-')
            errmsg = 'Há apenas um examinador disponível em %s/%s/%s às %s. É necessário pelo menos dois examinadores para agendamento de banca.' % (databr[2], databr[1], databr[0], time)
        else:
            databr = data.split('-')
            errmsg = 'Não há examinadores disponíveis em %s/%s/%s às %s' % (databr[2], databr[1], databr[0], time)
        return render(request, 'banca_data.html', {'form': form, 'ex1': ex1,
    'tcc': tcc, 'sucess_message':confirmacao, 'erro': erro, 'sala': sala,
    'errmsg' : errmsg, 'ex1count': ex1count})

def register(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        message = None
        if request.method == 'POST':
            form = NewForm(request.POST)
            if form.is_valid:
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                try:
                    User.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name, is_active = True, is_staff = False, is_superuser = False)
                except:
                    erro = 'Usuário com este login ou email já existe'
                    return render(request, 'user_novo.html', {'erro':erro})
                message = 'SUCESSO!! -- O USUARIO {} FOI CRIADO'.format(username)
                if request.POST.get('btn') == 's':
                    return HttpResponseRedirect("/user/")
        form = NewForm()
        return render(request, 'user_novo.html', {'form':form,
    'sucess_message':message})

                        #############################
                        #                           #
                        #      VIEWS DE EDIÇÃO      #
                        #                           #
                        #############################

#View de edição de professor e parte da logica de declaração.
def professor_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        cc= 0
        gti= 0
        spi= 0
        rc= 0
        coordcc = None
        coordgti = None
        coordspi = None
        coordrc = None
        coordspicc = 0
        professor = Professor.objects.get(pk=pk)
        #Aqui nesta variavel recebemos as informações da view acima.
        bancas = declarogica(pk)
        #Caso a variavel bancas não esteja vazia, checamos os cursos destas
        #bancas em que o professor atuou(logica de botão de impressão de declaração)
        if bancas != None:
            for banca in bancas:
                if banca.titulo_tcc.aluno.curso == 'Ciência da Computação':
                    cc = 1
                    try:
                        coordcc = Curso.objects.get(curso_nome='Ciência da Computação')
                    except:
                        coordcc = None
                if banca.titulo_tcc.aluno.curso == 'Gestão da Tecnologia da Informação':
                    gti = 1
                    try:
                        coordgti = Curso.objects.get(curso_nome='Gestão da Tecnologia da Informação')
                    except:
                        coordgti = None
                if banca.titulo_tcc.aluno.curso == 'Sistemas para Internet':
                    spi = 1
                    try:
                        coordspi = Curso.objects.get(curso_nome='Sistemas para Internet')
                    except:
                        coordspi = None
                if banca.titulo_tcc.aluno.curso == 'Redes de Computadores':
                    rc = 1
                    try:
                        coordrc = Curso.objects.get(curso_nome='Redes de Computadores')
                    except:
                        coordrc = None
        try: #logica para verificação de coordenador relacionado ao botão de impressão.
            ccc = Curso.objects.get(curso_nome='Ciência da Computação')
        except:
            ccc = None
        try:
            cgti = Curso.objects.get(curso_nome='Gestão da Tecnologia da Informação')
        except:
            cgti = None
        try:
            cspi = Curso.objects.get(curso_nome='Sistemas para Internet')
        except:
            cspi = None
        try:
            crc = Curso.objects.get(curso_nome='Redes de Computadores')
        except:
            crc = None
        #logica do botão de impressão, parte da lógica está no arquivo
        #html(professor_editar).
        if ccc == None or crc == None or cgti == None or cspi == None:
            coordspicc = 1
        else:
            coordspicc = 2
        professor_form = ProfessorForm(request.POST or None, instance=professor)
        if professor_form.is_valid():
            professor_form.save()
            return HttpResponseRedirect("/professor/")
        return render(request, 'professor_editar.html', {'object': professor,
    'form': professor_form, 'bancas': bancas, 'cc':cc, 'gti':gti, 'spi':spi,
    'rc':rc, 'coordcc':coordcc, 'coordgti':coordgti, 'coordspi':coordspi,
    'coordrc':coordrc, 'coordspicc':coordspicc})

def aluno_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        aluno = Aluno.objects.get(pk=pk)

        aluno_form = AlunoForm(request.POST or None, instance=aluno)
        if aluno_form.is_valid():
            aluno_form.save()
            return HttpResponseRedirect("/aluno/")
        return render(request, 'aluno_editar.html', {'object': aluno,
                    'form': aluno_form})

def curso_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        curso = Curso.objects.get(pk=pk)
        errmsg = None

        curso_form = CursoForm(request.POST or None, instance=curso)
        if curso_form.is_valid():
            curso_form.save()
            return HttpResponseRedirect("/curso/")
        errmsg = "Curso já cadastrado"
        return render(request, 'curso_editar.html', {'object': curso,
                        'form': curso_form, 'errmsg': errmsg})

def salas_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        salas = Salas.objects.get(pk=pk)

        salas_form = SalasForm(request.POST or None, instance=salas)
        if salas_form.is_valid():
            salas_form.save()
            return HttpResponseRedirect('/salas/')
        return render(request, 'salas_editar.html', {'object': salas,
    'form': salas_form})

def tcc_update_gti(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        tcc = Tcc.objects.get(pk=pk)
        aluno = Aluno.objects.filter(curso='Gestão da Tecnologia da Informação')
        tcc_form = TccForm(request.POST or None, instance=tcc)
        errmsg = None
        if tcc_form.is_valid():
            tcc_form.save()
            return HttpResponseRedirect("/tcc/")
        errmsg = "Trabalho com este nome já existente"
        return render(request, 'tcc_editar_gti.html', {'object': tcc,
    'form': tcc_form, 'aluno': aluno, 'errmsg': errmsg})

def tcc_update_cc(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        tcc = Tcc.objects.get(pk=pk)
        aluno = Aluno.objects.filter(curso='Ciência da Computação')
        tcc_form = TccForm(request.POST or None, instance=tcc)
        errmsg = None
        if tcc_form.is_valid():
            tcc_form.save()
            return HttpResponseRedirect("/tcc/")
        errmsg = "Trabalho com este nome já existente"
        return render(request, 'tcc_editar_cc.html', {'object': tcc,
    'form': tcc_form, 'aluno': aluno, 'errmsg': errmsg})

def tcc_update_spi(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        tcc = Tcc.objects.get(pk=pk)
        aluno = Aluno.objects.filter(curso='Sistemas para Internet')
        tcc_form = TccForm(request.POST or None, instance=tcc)
        errmsg = None
        if tcc_form.is_valid():
            tcc_form.save()
            return HttpResponseRedirect("/tcc/")
        errmsg = "Trabalho com este nome já existente"
        return render(request, 'tcc_editar_spi.html', {'object': tcc,
    'form': tcc_form, 'aluno': aluno, 'errmsg': errmsg})

def tcc_update_redes(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        tcc = Tcc.objects.get(pk=pk)
        aluno = Aluno.objects.filter(curso='Redes de Computadores')
        tcc_form = TccForm(request.POST or None, instance=tcc)
        errmsg = None
        if tcc_form.is_valid():
            tcc_form.save()
            return HttpResponseRedirect("/tcc/")
        errmsg = "Trabalho com este nome já existente"
        return render(request, 'tcc_editar_redes.html', {'object': tcc,
    'form': tcc_form, 'aluno': aluno, 'errmsg': errmsg})

def banca_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        banca = Banca.objects.get(pk=pk)

        banca_form = BancaForm(request.POST or None, instance=banca)
        if banca_form.is_valid():
            banca_form.save()
            return HttpResponseRedirect("/banca/")
        return render(request, 'banca_editar.html', {'object': banca,
    'form': banca_form})

def disp_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        disp = Disponibilidade.objects.get(pk=pk)

        disp_form = DispForm(request.POST or None, instance=disp)
        if disp_form.is_valid():
            disp_form.save()
            return HttpResponseRedirect("/disponibilidade/")
        return render(request, 'disponibilidade_editar.html', {'object': disp,
    'form': disp_form})

def user_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        user = User.objects.get(pk=pk)

        user_form = NewForm(request.POST or None, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect("/user/")
        return render(request, 'user_info.html', {'object': user,
    'form': user_form})

                        #############################
                        #                           #
                        #      VIEWS DE DELEÇÃO     #
                        #                           #
                        #############################

#View responsavel pela deleção de professor.
def professor_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        #Testa se vai dar erro de objeto protegido contra efeito de cascata
        #caso haja erro, armazena valor 1 na variavel, parte da logica esta no
        #html, o mesmo para todas as outras deleções.
        try:
            professor = Professor.objects.get(pk=pk)
            professor_form = ProfessorForm(request.POST or None, instance=professor)
            professor.delete()
            error = 0
            return render(request, 'professor_remover_confirmar.html', {
        'object': professor, 'error': error})
        except:
            error = 1
            return render(request, 'professor_remover_confirmar.html', {
        'object': professor, 'error': error})

def curso_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
            curso = Curso.objects.get(pk=pk)
            curso_form = CursoForm(request.POST or None, instance=curso)
            curso.delete()
            return HttpResponseRedirect('/curso/')

def aluno_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        try:
            aluno = Aluno.objects.get(pk=pk)
            aluno.delete()
            error = 0
            return render(request, 'aluno_remover_confirmar.html', {
        'object': aluno, 'error': error})
        except:
            error = 1
            return render(request, 'aluno_remover_confirmar.html', {
        'object': aluno, 'error': error})

def salas_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        try:
            salas = Salas.objects.get(pk=pk)
            salas_form = SalasForm(request.POST or None, instance=salas)
            salas.delete()
            error = 0
            return render(request, 'salas_remover_confirmar.html', {
        'object': salas, 'error': error})
        except:
            error = 1
            return render(request, 'salas_remover_confirmar.html', {
        'object': salas, 'error': error})

def tcc_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        try:
            tcc = Tcc.objects.get(pk=pk)
            tcc_form = TccForm(request.POST or None, instance=tcc)
            tcc.delete()
            error = 0
            return render(request, 'tcc_remover_confirmar.html', {
        'object': tcc, 'error': error})
        except:
            error = 1
            return render(request, 'tcc_remover_confirmar.html', {
        'object': tcc, 'error': error})


def banca_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        banca = Banca.objects.get(pk=pk)
        if request.method == 'POST':
            examinador_1 = banca.examinador_1
            examinador_2 = banca.examinador_2
            tcc = banca.titulo_tcc
            examinador_1.situacao='1'
            examinador_2.situacao='1'
            examinador_1.save()
            examinador_2.save()
            tcc.situacao='1'
            tcc.save()
            banca_form = BancaForm(request.POST or None, instance=banca)
            banca.delete()
            return HttpResponseRedirect("/banca/")
        return render(request, 'banca_remover_confirmar.html', {'object': banca})

def disp_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        disp_form = DispForm(request.POST or None)
        professor = Professor.objects.all().order_by('professor_nome')
        confirmacao = ''
        erro = None
        errmsg = None

        if disp_form.is_valid():
            erro = []
            h = "14"
            for i in range(0,9):
                cb = request.POST[h]
                if cb == h:
                    try:
                        form = disp_form.save(commit=False)
                        form.hora_inicio = '%s:00' %h
                        disp_form.save()
                        disp = Professor.objects.get(pk=request.POST['examinador'])
                        disp = disp.professor_nome
                        confirmacao = 'A DISPONIBILIDADE DO PROFESSOR %s FOI CADASTRADO COM SUCESSO' %disp
                    except IntegrityError as e:
                        if 'unique constraint':
                            erro.append("%s:00" %h)
                    disp_form = DispForm(request.POST)
                h = int(h)
                h += 1
                h = str(h)
            if (len(erro) > 0 and len(erro) < 9):
                errmsg = "Esse(a) professor(a) já tem disponilidade salva no(s) horário(s) %s. Os outros horários selecionados foram salvos corretamente" %', '.join(str(p) for p in erro)
            else:
                errmsg = "Esse(a) professor(a) já tem disponilidade salva no(s) horário(s) %s. Nada vai ser alterado." %', '.join(str(p) for p in erro)
            lista_disp = Disponibilidade.objects.all()
            if request.POST.get('btn') == 's':
                return render(request, 'disponibilidade.html', {
            'errmsg': errmsg, 'lista_disp': lista_disp, 'erro': erro,
            'professor': professor})
        return render(request, 'disponibilidade_novo.html', {'form': disp_form,
    'professor': professor, 'sucess_message': confirmacao, 'errmsg': errmsg,
    'erro': erro })

def disp_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        disp = Disponibilidade.objects.get(pk=pk)

        if request.method == 'POST':
            disp_form = DispForm(request.POST or None, instance=disp)
            disp.delete()
            return HttpResponseRedirect("/disponibilidade/")
        return render(request, 'disponibilidade_remover_confirmar.html', {
    'object': disp})

def user_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        user = User.objects.get(pk=pk)

        if request.method == 'POST':
            user_form = NewForm(request.POST or None, instance=user)
            user.delete()
            return HttpResponseRedirect("/user/")
        return render(request, 'user_remover_confirmar.html', {'object': user})
