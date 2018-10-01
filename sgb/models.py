from django.db import models
from django.core.validators import RegexValidator

CC = 'Ciência da Computação'
SPI = 'Sistemas para Internet'
GTI = 'Gestão da Tecnologia da Informação'
RC = 'Redes de Computadores'
CURSO = (
    (CC, 'Ciência da Computação'),
    (SPI, 'Sistemas para Internet'),
    (GTI, 'Gestão da Tecnologia da Informação'),
    (RC, 'Redes de Computadores'),
)

P5 = 'P5'
P7 = 'P7'
P8 = 'P8'
PERIODO = (
    (P5, '5° '),
    (P7, '7° '),
    (P8, '8° '),
)

class Professor(models.Model):
    ESP = 'ESP'
    MS = 'MS'
    DR = 'DR'
    PDR = 'PÓS Dr'
    FORMACAO = (
        (ESP, 'ESPECIALISTA'),
        (MS, 'MESTRE'),
        (DR, 'DOUTOR'),
        (PDR, 'PÓS DOUTORADO'),
    )

    professor_nome = models.CharField(max_length=100, blank = False)
    professor_matricula = models.CharField(max_length = 6, blank = False, unique = True, validators=[RegexValidator(r'^[0-9]*$', 'Digite um número de matricula válido')])
    area_de_atuacao = models.CharField(max_length=50, blank=False)
    formacao = models.CharField(max_length=100, choices=FORMACAO, blank=False)
    graduacao = models.CharField(max_length=500, blank=False)
    especializacao = models.CharField(max_length=500, blank=True)
    mestrado = models.CharField(max_length=500, blank=True)
    doutorado = models.CharField(max_length=500, blank=True)
    pos_doutorado = models.CharField(max_length=500, blank=True)
    area_de_conhecimentos = models.CharField(max_length=500, blank=False)
    area_de_orientacao = models.CharField(max_length=500, blank=False)
    info_relevante = models.CharField(max_length=1000, blank=True)


    def __str__(self):
        return self.professor_nome

class Curso(models.Model):
    curso_nome = models.CharField(max_length=50, choices=CURSO, blank=False, unique=True)
    coordenador = models.ForeignKey(Professor, on_delete=models.PROTECT, blank = False, null = False, related_name = 'coordenador', default = '')

    def __str__(self):
        return self.curso_nome


class Aluno(models.Model):

    aluno_nome = models.CharField(max_length=100)
    aluno_telefone = models.CharField(max_length = 11,blank=False, null=False, validators=[RegexValidator(r'^\d{10,11}$', 'Digite um número de matricula válido')])
    aluno_matricula = models.CharField(max_length = 10, blank = False, unique = True, validators=[RegexValidator(r'^[0-9]*$', 'Digite um número de matricula válido')])
    aluno_email = models.EmailField(blank=False, null=False)
    curso = models.CharField(max_length=50, choices=CURSO, blank=False)
    periodo = models.CharField(max_length=2, choices=PERIODO, blank=False)

    def __str__(self):
        return self.aluno_nome

class User(models.Model):
	username = models.CharField('Username', max_length = 50, unique = True)
	email = models.EmailField(unique = True)
	password = models.CharField('Password', max_length = 50)

class Tcc(models.Model):
    titulo_tcc = models.CharField(max_length = 220, blank = False, unique=True)
    aluno = models.OneToOneField(Aluno, blank = False, null = False, on_delete=models.PROTECT, related_name = 'aluno', unique = True)
    aluno2 = models.OneToOneField(Aluno, blank = True, null = True, on_delete=models.PROTECT, related_name = 'aluno2', unique = True)
    aluno3 = models.OneToOneField(Aluno, blank = True, null = True, on_delete=models.PROTECT, related_name = 'aluno3', unique = True)
    aluno4 = models.OneToOneField(Aluno, blank = True, null = True, on_delete=models.PROTECT, related_name = 'aluno4', unique = True)
    orientador = models.ForeignKey(Professor, blank = False, on_delete=models.PROTECT)
    situacao = models.CharField(default='1', max_length=1)

    def __str__(self):
        return self.titulo_tcc

class Salas(models.Model):

    EVA = 'EVA'
    CT = 'CT'
    BF = 'B.F'
    BLOCOS = (
        (EVA, 'EVA'),
        (CT, 'CENTRO DE TECNOLOGIA'),
        (BF, 'BLOCO F'),
    )
    blocos = models.CharField(max_length=3, choices=BLOCOS, blank=False)
    numero_do_bloco = models.CharField(max_length = 3, unique = True, validators=[RegexValidator(r'^[0-9]*$', 'Digite um número de sala válido')])

    def __str__(self):
        return self.blocos + ' - ' + str(self.numero_do_bloco)
    class Meta:
        unique_together = (("blocos", "numero_do_bloco"))


class Disponibilidade(models.Model):

    #Define estaticamente se a Disponibilidade esta relacoinada ou não relacionada
    Situacao_Choices  = (
    	('1', 'Não Relacionado'),
    	('2', 'Relacionado')

    	)

    data = models.DateField(blank = False)
    hora_inicio = models.CharField(max_length=5, blank = False, validators=[RegexValidator(r'^[012]\d:[0-5]\d')])
    # hora_termino = models.CharField(max_length=5, blank = False, validators=[RegexValidator(r'^[012]\d:[0-5]\d')])
    examinador = models.ForeignKey(Professor, blank = False, related_name = 'examinador')
    situacao = models.CharField(choices=Situacao_Choices, default='1', max_length=1)

    def __str__(self):
        return str(self.examinador) + ' - Data: ' + str(self.data) + ' das ' + self.hora_inicio
    class Meta:
        unique_together = (("data", "hora_inicio", "examinador"))

class Banca(models.Model):
    titulo_tcc = models.OneToOneField(Tcc, blank = False, on_delete=models.PROTECT, unique = True)
    sala = models.ForeignKey(Salas, blank = False, on_delete=models.PROTECT, related_name = 'sala')
    hora_inicio = models.CharField(max_length=5, blank = False, validators=[RegexValidator(r'^[012]\d:[0-5]\d')])
    # hora_termino = models.CharField(max_length=5, blank = False, validators=[RegexValidator(r'^[012]\d:[0-5]\d')])
    data_banca = models.DateField(blank = False)
    examinador_1 = models.ForeignKey(Disponibilidade, blank = False, on_delete=models.PROTECT, related_name = 'examinador1')
    examinador_2 = models.ForeignKey(Disponibilidade, blank = False, on_delete=models.PROTECT, related_name = 'examinador2')

    def __str__(self):
        return str(self.titulo_tcc)
    class Meta:
        unique_together = (("sala", "hora_inicio", "data_banca"))
