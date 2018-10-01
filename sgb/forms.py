from django import forms
from django.forms import ModelForm
from sgb.models import Professor, Aluno, Tcc, Salas, Banca, Disponibilidade, Curso
from django.contrib.auth.models import User

class ProfessorForm(forms.ModelForm):
    professor_nome = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'nome','autofocus':'autofocus'}))
    professor_matricula = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'matricula','maxlength':6}))
    area_de_atuacao = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'area_de_atuacao'}), required=False)
    graduacao = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'graduacao'}), required=False)
    especializacao = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'especializacao'}), required=False)
    mestrado = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'mestrado'}), required=False)
    doutorado = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'doutorado'}), required=False)
    pos_doutorado = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'pos_doutorado'}), required=False)
    area_de_conhecimentos = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'area_de_conhecimentos'}), required=False)
    area_de_orientacao = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'area_de_orientacao'}), required=False)
    info_relevante = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'info_relevante'}), required=False)
    class Meta():
        model = Professor
        fields = ('professor_nome','professor_matricula','area_de_atuacao','formacao','graduacao','especializacao','mestrado','doutorado','pos_doutorado','area_de_conhecimentos','area_de_orientacao','info_relevante')

class CursoForm(ModelForm):
    class Meta:
        model = Curso
        exclude = ['']

class AlunoForm(forms.ModelForm):
    aluno_nome = forms.CharField(label='', widget=forms.TextInput(attrs={'id':'nome', 'name': 'nome', 'data-error': '.errorTxt1', 'type': 'text'}))
    aluno_telefone = forms.CharField(label='', widget=forms.TextInput(attrs={'id':'telefone','maxlength':11}),required=False)
    aluno_email = forms.CharField(label='',widget=forms.TextInput(attrs={'type':'email','id':'mail'}), required=False)
    aluno_matricula = forms.CharField(label='', widget=forms.TextInput(attrs={'id': 'matricula',  'maxlength' :10}))
    PERIODO = [(p, p) for p in ('P5', 'P7', 'P8')]
    periodo = forms.CharField(label='', widget=forms.Select(attrs={'id': 'id_periodo'}, choices=PERIODO))
    CURSO = [(c,c) for c in ('Ciência da Computação', 'Sistemas para Internet', 'Gestão da Tecnologia da Informação', 'Redes de Computadores')]
    curso = forms.CharField(label='', widget=forms.Select(attrs={'id': 'id_curso'}, choices=CURSO))
    class Meta():
        model = Aluno
        fields = ('aluno_nome','aluno_telefone','aluno_matricula','aluno_email','curso','periodo' )

class SalasForm(forms.ModelForm):
    class Meta:
        model = Salas
        fields = ('blocos','numero_do_bloco')

class NewForm(forms.ModelForm):
    first_name = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'first_name'}))
    last_name = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'last_name'}))
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'type':'email','id':'email'}))
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'username'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id':'password'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name','email','username','password')

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		fields = ('username', 'password')

class TccForm(forms.ModelForm):
    titulo_tcc = forms.CharField(label='',widget=forms.TextInput(attrs={'id':'titulo_tcc'}))
    class Meta:
        model = Tcc
        fields = ('titulo_tcc','aluno','aluno2','aluno3','aluno4','orientador')

class BancaForm(ModelForm):
    class Meta:
        model = Banca
        fields = ('titulo_tcc', 'sala', 'examinador_1', 'examinador_2')
        exclude = ['']

class DispForm(forms.ModelForm):
    data = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'text', 'id': 'data', 'class' : 'datepicker'}))
    # hora_inicio = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'text', 'id': 'ini', 'class' : 'timepicker'}))
    # hora_termino = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'text', 'id': 'end', 'class' : 'timepicker'}))
    class Meta:
        model = Disponibilidade
        fields = ('examinador', 'data')
